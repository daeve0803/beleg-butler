#!/usr/bin/env python3
"""
Reddit Thread Deep Scraper via Reddit JSON API + ScrapingBee.

Extrahiert ALLE Comments inkl. nested replies mit Metadaten (score, author, etc.).
Nutzt Reddit's eingebaute JSON-API (.json suffix) mit ScrapingBee für Bot-Protection-Bypass.
"""
import argparse
import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
import time
import re
from pathlib import Path

# Lade .env wenn vorhanden
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

SCRAPINGBEE_API_KEY = os.getenv("SCRAPINGBEE_API_KEY")
SCRAPINGBEE_BASE_URL = "https://app.scrapingbee.com/api/v1/"


def normalize_reddit_url(url: str) -> str:
    """
    Normalisiert Reddit URL und entfernt .json suffix falls vorhanden.
    """
    # Entferne trailing slash
    url = url.rstrip("/")
    # Entferne .json suffix falls vorhanden
    if url.endswith(".json"):
        url = url[:-5]
    # Stelle sicher dass es www.reddit.com ist (nicht old.reddit.com etc.)
    url = re.sub(r"(old|new|np)\.reddit\.com", "www.reddit.com", url)
    return url


def fetch_reddit_json(url: str, after: Optional[str] = None) -> Optional[Dict]:
    """
    Holt Reddit Thread als JSON via ScrapingBee.

    Reddit's JSON API: Füge .json an die URL an.
    ScrapingBee umgeht Bot-Detection.
    """
    if not SCRAPINGBEE_API_KEY:
        raise ValueError("SCRAPINGBEE_API_KEY nicht gesetzt in .env")

    # Normalisiere und füge .json hinzu
    base_url = normalize_reddit_url(url)
    json_url = f"{base_url}.json"

    # Füge Pagination hinzu wenn vorhanden (für mehr Comments)
    if after:
        json_url += f"?after={after}"

    params = {
        "api_key": SCRAPINGBEE_API_KEY,
        "url": json_url,
        "render_js": "false",  # JSON braucht kein JS rendering
        "premium_proxy": "true",  # Reddit blockiert Standard-Proxies
    }

    try:
        response = requests.get(SCRAPINGBEE_BASE_URL, params=params, timeout=60)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"  Fehler: Status {response.status_code}")
            print(f"  Response: {response.text[:500]}")
            return None

    except json.JSONDecodeError as e:
        print(f"  JSON Parse Error: {e}")
        print(f"  Response war kein valides JSON")
        return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None


def extract_comment_tree(comment_data: Dict, depth: int = 0) -> Optional[Dict]:
    """
    Extrahiert einen Comment mit allen nested Replies rekursiv.
    """
    # Skip "more" placeholders (Pagination-Marker)
    if comment_data.get("kind") == "more":
        return None

    data = comment_data.get("data", {})

    # Skip gelöschte/entfernte Comments ohne Body
    body = data.get("body", "")
    if not body or body in ["[deleted]", "[removed]"]:
        return None

    created_utc = data.get("created_utc", 0)
    comment = {
        "id": data.get("id", ""),
        "author": data.get("author", "[deleted]"),
        "body": body,
        "score": data.get("score", 0),
        "created_utc": created_utc,
        "created_at": datetime.utcfromtimestamp(created_utc).isoformat() if created_utc > 0 else None,
        "depth": depth,
        "permalink": f"https://reddit.com{data.get('permalink', '')}",
        "is_submitter": data.get("is_submitter", False),  # OP markieren
        "replies": []
    }

    # Rekursiv Replies extrahieren
    replies_data = data.get("replies", "")
    if isinstance(replies_data, dict):
        children = replies_data.get("data", {}).get("children", [])
        for child in children:
            reply = extract_comment_tree(child, depth + 1)
            if reply:
                comment["replies"].append(reply)

    return comment


def scrape_thread(url: str) -> Optional[Dict]:
    """
    Scrapt einen Reddit Thread vollständig.

    Args:
        url: Reddit Thread URL

    Returns:
        Dict mit Post-Daten und allen Comments
    """
    print(f"  Lade JSON von: {url}")

    raw_data = fetch_reddit_json(url)

    if not raw_data or not isinstance(raw_data, list) or len(raw_data) < 2:
        print(f"  Ungültige Response-Struktur")
        return None

    # Reddit JSON Struktur: [post_data, comments_data]
    post_listing = raw_data[0]
    comments_listing = raw_data[1]

    # Post extrahieren
    post_data = post_listing.get("data", {}).get("children", [{}])[0].get("data", {})
    post_created_utc = post_data.get("created_utc", 0)

    thread = {
        "id": post_data.get("id", ""),
        "title": post_data.get("title", ""),
        "author": post_data.get("author", "[deleted]"),
        "selftext": post_data.get("selftext", ""),
        "score": post_data.get("score", 0),
        "upvote_ratio": post_data.get("upvote_ratio", 0),
        "num_comments": post_data.get("num_comments", 0),
        "created_utc": post_created_utc,
        "created_at": datetime.utcfromtimestamp(post_created_utc).isoformat() if post_created_utc > 0 else None,
        "subreddit": post_data.get("subreddit", ""),
        "url": url,
        "permalink": f"https://reddit.com{post_data.get('permalink', '')}",
        "scraped_at": datetime.now().isoformat(),
        "comments": [],
        "comments_flat": []  # Für einfachere Analyse
    }

    # Comments extrahieren
    comments_children = comments_listing.get("data", {}).get("children", [])

    for child in comments_children:
        comment = extract_comment_tree(child, depth=0)
        if comment:
            thread["comments"].append(comment)

    # Flatten für Analyse
    thread["comments_flat"] = flatten_comments(thread["comments"])

    return thread


def flatten_comments(comments: List[Dict], parent_author: str = None) -> List[Dict]:
    """
    Flacht nested Comments für einfachere Analyse.
    Behält depth-Information für Kontext.
    """
    flat = []

    for c in comments:
        flat.append({
            "id": c["id"],
            "author": c["author"],
            "body": c["body"],
            "score": c["score"],
            "depth": c["depth"],
            "created_at": c["created_at"],
            "parent_author": parent_author,
            "is_submitter": c["is_submitter"],
            "permalink": c["permalink"]
        })

        if c.get("replies"):
            flat.extend(flatten_comments(c["replies"], c["author"]))

    return flat


def format_for_analysis(thread: Dict, max_chars: int = 50000) -> str:
    """
    Formatiert Thread-Daten für Claude-Analyse.
    Priorisiert high-score Comments.
    """
    lines = []

    # Post Header
    lines.append(f"# {thread['title']}")
    lines.append(f"[r/{thread['subreddit']} | Score: {thread['score']} | {thread['num_comments']} Comments]")
    lines.append("")

    if thread.get("selftext"):
        lines.append(f"**OP schreibt:**")
        lines.append(thread["selftext"][:2000])
        lines.append("")

    lines.append("---")
    lines.append("## Comments (sortiert nach Score)")
    lines.append("")

    # Sortiere flat comments nach Score (wichtigste zuerst)
    sorted_comments = sorted(
        thread.get("comments_flat", []),
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    char_count = len("\n".join(lines))

    for c in sorted_comments:
        depth_marker = ">" * c["depth"] if c["depth"] > 0 else ""
        op_marker = " [OP]" if c.get("is_submitter") else ""

        comment_text = f"{depth_marker}**{c['author']}{op_marker}** ({c['score']} points):\n{depth_marker}{c['body']}\n"

        if char_count + len(comment_text) > max_chars:
            lines.append(f"\n... [{len(sorted_comments) - len([l for l in lines if l.startswith('**')])} weitere Comments abgeschnitten]")
            break

        lines.append(comment_text)
        char_count += len(comment_text)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Reddit Thread Deep Scraper via JSON API + ScrapingBee"
    )
    parser.add_argument(
        "--urls_file",
        help="JSON-Datei mit URLs (aus search_niche.py)"
    )
    parser.add_argument(
        "--url",
        help="Einzelne Reddit URL"
    )
    parser.add_argument(
        "--format_for_analysis",
        action="store_true",
        help="Formatiert Output für Claude-Analyse (priorisiert high-score)"
    )

    args = parser.parse_args()

    if not SCRAPINGBEE_API_KEY:
        print("Fehler: SCRAPINGBEE_API_KEY nicht in .env gesetzt")
        return

    urls = []

    if args.url:
        urls = [{"url": args.url, "title": "Direct URL"}]
    elif args.urls_file:
        if not os.path.exists(args.urls_file):
            print(f"Datei nicht gefunden: {args.urls_file}")
            return
        with open(args.urls_file, "r", encoding="utf-8") as f:
            all_urls = json.load(f)
            # Nur Reddit-URLs filtern
            urls = [u for u in all_urls if "reddit.com" in u.get("url", "")]
            print(f"Gefiltert: {len(urls)} Reddit-URLs von {len(all_urls)} gesamt")
    else:
        print("Fehler: --url oder --urls_file erforderlich")
        return

    if not urls:
        print("Keine Reddit-URLs gefunden.")
        return

    print(f"Scrape {len(urls)} Reddit Threads...")

    results = []

    for i, item in enumerate(urls, 1):
        url = item.get("url")
        print(f"\n[{i}/{len(urls)}] {url}")

        try:
            thread_data = scrape_thread(url)

            if thread_data:
                # Statistiken
                total_comments = len(thread_data.get("comments_flat", []))
                print(f"  -> {total_comments} Comments extrahiert, Thread-Score: {thread_data['score']}")

                if args.format_for_analysis:
                    thread_data["formatted_content"] = format_for_analysis(thread_data)

                results.append(thread_data)
            else:
                print(f"  -> Fehlgeschlagen")

        except Exception as e:
            print(f"  -> Exception: {e}")

        # Rate-Limiting (ScrapingBee hat eigenes, aber sicherheitshalber)
        if i < len(urls):
            time.sleep(2)

    # Speichern
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = ".tmp"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/reddit_threads_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*50}")
    print(f"Scraping abgeschlossen!")
    print(f"Threads: {len(results)}/{len(urls)}")
    print(f"Gespeichert: {output_file}")

    # Zusammenfassung
    total_comments = sum(len(t.get("comments_flat", [])) for t in results)
    print(f"Gesamte Comments: {total_comments}")


if __name__ == "__main__":
    main()
