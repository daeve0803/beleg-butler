#!/usr/bin/env python3
"""
HackerNews Deep Thread Scraper.

Nutzt die kostenlose Firebase API um Stories und alle nested Comments zu extrahieren.
API Docs: https://github.com/HackerNews/API
"""
import argparse
import json
import re
import time
from datetime import datetime
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# HackerNews Firebase API
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"


def extract_story_id(url: str) -> Optional[str]:
    """Extrahiert die Story-ID aus einer HN-URL."""
    # Patterns:
    # https://news.ycombinator.com/item?id=12345
    # https://hacker-news.firebaseio.com/v0/item/12345
    match = re.search(r'[?&]id=(\d+)', url)
    if match:
        return match.group(1)
    match = re.search(r'/item/(\d+)', url)
    if match:
        return match.group(1)
    return None


def fetch_item(item_id: str) -> Optional[Dict]:
    """Holt ein einzelnes Item (Story oder Comment) von der API."""
    url = f"{HN_API_BASE}/item/{item_id}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"  Fehler beim Laden von Item {item_id}: {e}")
    return None


def fetch_items_batch(item_ids: List[str], max_workers: int = 10) -> Dict[str, Dict]:
    """Holt mehrere Items parallel."""
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_id = {executor.submit(fetch_item, item_id): item_id for item_id in item_ids}
        for future in as_completed(future_to_id):
            item_id = future_to_id[future]
            try:
                result = future.result()
                if result:
                    results[item_id] = result
            except Exception:
                pass
    return results


def extract_comment_tree(item_data: Dict, depth: int = 0, items_cache: Dict = None) -> Optional[Dict]:
    """
    Extrahiert einen Comment mit allen nested Replies.

    Args:
        item_data: Das Item-Dictionary von der API
        depth: Aktuelle Verschachtelungstiefe
        items_cache: Cache für bereits geladene Items

    Returns:
        Strukturiertes Comment-Dictionary oder None
    """
    if items_cache is None:
        items_cache = {}

    # Skip deleted/dead comments
    if item_data.get("deleted") or item_data.get("dead"):
        return None

    text = item_data.get("text", "")
    if not text:
        return None

    # HTML-Tags bereinigen (HN speichert HTML)
    text = re.sub(r'<p>', '\n\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip()

    comment = {
        "id": str(item_data.get("id", "")),
        "author": item_data.get("by", "[deleted]"),
        "body": text,
        "score": item_data.get("score", 0),  # HN zeigt keine Comment-Scores, aber manche haben welche
        "depth": depth,
        "created_at": datetime.fromtimestamp(item_data.get("time", 0)).isoformat() if item_data.get("time") else "",
        "permalink": f"https://news.ycombinator.com/item?id={item_data.get('id', '')}",
        "replies": []
    }

    # Rekursiv Replies laden
    kids = item_data.get("kids", [])
    if kids:
        # Batch-Load der Replies
        kids_to_fetch = [str(k) for k in kids if str(k) not in items_cache]
        if kids_to_fetch:
            fetched = fetch_items_batch(kids_to_fetch)
            items_cache.update(fetched)

        for kid_id in kids:
            kid_data = items_cache.get(str(kid_id))
            if kid_data:
                reply = extract_comment_tree(kid_data, depth + 1, items_cache)
                if reply:
                    comment["replies"].append(reply)

    return comment


def flatten_comments(comments: List[Dict], parent_author: str = None) -> List[Dict]:
    """
    Macht die nested Comment-Struktur flach für einfachere Analyse.
    Behält aber die depth-Information.
    """
    flat = []
    for c in comments:
        flat_comment = {
            "id": c["id"],
            "author": c["author"],
            "body": c["body"],
            "score": c["score"],
            "depth": c["depth"],
            "created_at": c["created_at"],
            "parent_author": parent_author,
            "permalink": c["permalink"]
        }
        flat.append(flat_comment)

        if c.get("replies"):
            flat.extend(flatten_comments(c["replies"], c["author"]))

    return flat


def scrape_story(url: str) -> Optional[Dict]:
    """
    Scrapt eine HN-Story mit allen Comments.

    Args:
        url: HackerNews Story URL

    Returns:
        Dictionary mit Story-Daten und allen Comments
    """
    story_id = extract_story_id(url)
    if not story_id:
        print(f"Konnte Story-ID nicht aus URL extrahieren: {url}")
        return None

    print(f"  Lade Story {story_id}...")
    story_data = fetch_item(story_id)
    if not story_data:
        print(f"  Story nicht gefunden: {story_id}")
        return None

    # Story-Grunddaten
    result = {
        "id": story_id,
        "title": story_data.get("title", ""),
        "url": story_data.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
        "score": story_data.get("score", 0),
        "author": story_data.get("by", "[deleted]"),
        "num_comments": story_data.get("descendants", 0),
        "created_at": datetime.fromtimestamp(story_data.get("time", 0)).isoformat() if story_data.get("time") else "",
        "text": story_data.get("text", ""),  # Bei Ask HN gibt es Text
        "comments": [],
        "comments_flat": []
    }

    # Comments laden
    kids = story_data.get("kids", [])
    if kids:
        print(f"  Lade {len(kids)} Top-Level Comments...")

        # Erst alle Top-Level Comments laden
        items_cache = fetch_items_batch([str(k) for k in kids])

        # Dann rekursiv alle Replies
        for kid_id in kids:
            kid_data = items_cache.get(str(kid_id))
            if kid_data:
                comment = extract_comment_tree(kid_data, depth=0, items_cache=items_cache)
                if comment:
                    result["comments"].append(comment)

        # Flatten für Analyse
        result["comments_flat"] = flatten_comments(result["comments"])
        print(f"  -> {len(result['comments_flat'])} Comments total extrahiert")

    return result


def format_for_analysis(story_data: Dict, max_chars: int = 50000) -> str:
    """
    Formatiert die Story-Daten als Markdown für Claude-Analyse.
    Priorisiert Comments mit vielen Replies (Engagement-Signal).
    """
    lines = []

    # Story Header
    lines.append(f"# {story_data.get('title', 'Untitled')}")
    lines.append(f"**Score:** {story_data.get('score', 0)} | **Comments:** {story_data.get('num_comments', 0)}")
    lines.append(f"**Author:** {story_data.get('author', 'unknown')}")
    lines.append("")

    # Story Text (bei Ask HN)
    if story_data.get("text"):
        lines.append("## Original Post")
        lines.append(story_data["text"][:2000])
        lines.append("")

    # Comments - in Thread-Reihenfolge (bereits korrekt strukturiert)
    comments_flat = story_data.get("comments_flat", [])
    if comments_flat:
        lines.append("## Comments")
        lines.append("")

        for comment in comments_flat:
            depth_marker = ">" * comment["depth"] if comment["depth"] > 0 else ""
            author = comment["author"]
            body = comment["body"][:1500]  # Limit pro Comment

            if depth_marker:
                lines.append(f"{depth_marker} **{author}:**")
                lines.append(f"{depth_marker} {body}")
            else:
                lines.append(f"**{author}:**")
                lines.append(body)
            lines.append("")

    result = "\n".join(lines)

    # Truncate wenn nötig
    if len(result) > max_chars:
        result = result[:max_chars] + "\n\n[... truncated ...]"

    return result


def main():
    parser = argparse.ArgumentParser(description="Scrape HackerNews Story mit allen Comments.")
    parser.add_argument("--url", required=True, help="HackerNews Story URL")
    parser.add_argument("--output", help="Output JSON file (optional)")

    args = parser.parse_args()

    print(f"Scraping HackerNews: {args.url}")
    story_data = scrape_story(args.url)

    if story_data:
        # Formatiere für Analyse
        formatted = format_for_analysis(story_data)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(story_data, f, indent=2, ensure_ascii=False)
            print(f"Gespeichert: {args.output}")
        else:
            # Ausgabe auf stdout
            print("\n" + "="*50)
            print(formatted[:3000])
            print("="*50)
            print(f"\nStory: {story_data['title']}")
            print(f"Score: {story_data['score']}")
            print(f"Comments: {len(story_data['comments_flat'])}")
    else:
        print("Scraping fehlgeschlagen.")


if __name__ == "__main__":
    main()
