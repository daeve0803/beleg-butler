#!/usr/bin/env python3
"""
Social Media Content Scraper.

Delegiert URLs an plattform-spezifische Scraper:
- Reddit -> scrape_reddit.py
- HackerNews -> scrape_hn.py
- ProductHunt -> scrape_producthunt.py
- Quora -> scrape_quora.py
- Andere -> Jina Reader
"""
import argparse
import os
import json
import sys
import requests
from datetime import datetime
from pathlib import Path
import time

# Stelle sicher dass tools/ im Path ist für Imports (nur einmal)
_tools_dir = Path(__file__).parent
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

# Jina API Key (optional für den Free Tier, aber empfohlen für höhere Limits)
JINA_API_KEY = os.getenv("JINA_API_KEY")


def is_reddit_url(url: str) -> bool:
    """Prüft ob URL ein Reddit-Thread ist."""
    return "reddit.com" in url or "redd.it" in url


def is_hn_url(url: str) -> bool:
    """Prüft ob URL ein HackerNews-Thread ist."""
    return "news.ycombinator.com" in url or "hacker-news.firebaseio.com" in url


def is_producthunt_url(url: str) -> bool:
    """Prüft ob URL ein ProductHunt-Post ist."""
    return "producthunt.com" in url


def is_quora_url(url: str) -> bool:
    """Prüft ob URL eine Quora-Frage ist."""
    return "quora.com" in url


def scrape_with_jina(url):
    """
    Scrapt eine URL mit Jina Reader (r.jina.ai).
    """
    jina_url = f"https://r.jina.ai/{url}"
    
    headers = {}
    if JINA_API_KEY:
        headers["Authorization"] = f"Bearer {JINA_API_KEY}"
        
    try:
        response = requests.get(jina_url, headers=headers, timeout=60)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Fehler beim Scrapen von {url}: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception beim Scrapen von {url}: {e}")
        return None

def scrape_reddit_urls(reddit_urls: list) -> list:
    """
    Delegiert Reddit-URLs an scrape_reddit.py für Deep Thread Reading.
    """
    from scrape_reddit import scrape_thread, format_for_analysis

    results = []
    for i, item in enumerate(reddit_urls, 1):
        url = item.get("url")
        title = item.get("title", "")
        print(f"  [{i}/{len(reddit_urls)}] Reddit Deep Scrape: {url}")

        try:
            thread_data = scrape_thread(url)
            if thread_data:
                # Formatiere für Analyse (priorisiert high-score comments)
                formatted = format_for_analysis(thread_data)
                results.append({
                    "url": url,
                    "title": thread_data.get("title", title),
                    "content": formatted,
                    "scraped_at": datetime.now().isoformat(),
                    "source": "reddit_deep",
                    "metadata": {
                        "score": thread_data.get("score", 0),
                        "num_comments": len(thread_data.get("comments_flat", [])),
                        "subreddit": thread_data.get("subreddit", ""),
                        "upvote_ratio": thread_data.get("upvote_ratio", 0)
                    }
                })
                print(f"    -> {len(thread_data.get('comments_flat', []))} Comments, Score: {thread_data.get('score', 0)}")
            else:
                print(f"    -> Fehlgeschlagen")
        except Exception as e:
            print(f"    -> Fehler: {e}")

        time.sleep(2)  # Rate-Limiting

    return results


def scrape_hn_urls(hn_urls: list) -> list:
    """
    Delegiert HackerNews-URLs an scrape_hn.py für Deep Thread Reading.
    """
    from scrape_hn import scrape_story, format_for_analysis

    results = []
    for i, item in enumerate(hn_urls, 1):
        url = item.get("url")
        title = item.get("title", "")
        print(f"  [{i}/{len(hn_urls)}] HackerNews Deep Scrape: {url}")

        try:
            story_data = scrape_story(url)
            if story_data:
                formatted = format_for_analysis(story_data)
                results.append({
                    "url": url,
                    "title": story_data.get("title", title),
                    "content": formatted,
                    "scraped_at": datetime.now().isoformat(),
                    "source": "hn_deep",
                    "metadata": {
                        "score": story_data.get("score", 0),
                        "num_comments": len(story_data.get("comments_flat", [])),
                        "author": story_data.get("author", "")
                    }
                })
                print(f"    -> {len(story_data.get('comments_flat', []))} Comments, Score: {story_data.get('score', 0)}")
            else:
                print(f"    -> Fehlgeschlagen")
        except Exception as e:
            print(f"    -> Fehler: {e}")

        time.sleep(1)  # Rate-Limiting (fair use)

    return results


def scrape_producthunt_urls(ph_urls: list) -> list:
    """
    Delegiert ProductHunt-URLs an scrape_producthunt.py für Deep Scraping.
    """
    from scrape_producthunt import scrape_post, format_for_analysis

    results = []
    for i, item in enumerate(ph_urls, 1):
        url = item.get("url")
        title = item.get("title", "")
        print(f"  [{i}/{len(ph_urls)}] ProductHunt Deep Scrape: {url}")

        try:
            post_data = scrape_post(url)
            if post_data:
                formatted = format_for_analysis(post_data)
                results.append({
                    "url": url,
                    "title": post_data.get("name", title),
                    "content": formatted,
                    "scraped_at": datetime.now().isoformat(),
                    "source": "producthunt_deep",
                    "metadata": {
                        "votes": post_data.get("votes", 0),
                        "num_comments": len(post_data.get("comments_flat", [])),
                        "tagline": post_data.get("tagline", "")
                    }
                })
                print(f"    -> {len(post_data.get('comments_flat', []))} Comments, {post_data.get('votes', 0)} Votes")
            else:
                print(f"    -> Fehlgeschlagen")
        except Exception as e:
            print(f"    -> Fehler: {e}")

        time.sleep(1)  # Rate-Limiting

    return results


def scrape_quora_urls(quora_urls: list) -> list:
    """
    Delegiert Quora-URLs an scrape_quora.py für Deep Scraping.
    """
    from scrape_quora import scrape_question, format_for_analysis

    results = []
    for i, item in enumerate(quora_urls, 1):
        url = item.get("url")
        title = item.get("title", "")
        print(f"  [{i}/{len(quora_urls)}] Quora Deep Scrape: {url}")

        try:
            question_data = scrape_question(url)
            if question_data:
                formatted = format_for_analysis(question_data)
                results.append({
                    "url": url,
                    "title": question_data.get("title", title),
                    "content": formatted,
                    "scraped_at": datetime.now().isoformat(),
                    "source": "quora_deep",
                    "metadata": {
                        "num_answers": question_data.get("num_answers", 0),
                        "top_answer_upvotes": question_data.get("top_answer_upvotes", 0)
                    }
                })
                print(f"    -> {question_data.get('num_answers', 0)} Answers")
            else:
                print(f"    -> Fehlgeschlagen")
        except Exception as e:
            print(f"    -> Fehler: {e}")

        time.sleep(2)  # Rate-Limiting (ScrapingBee Credits schonen)

    return results


def main():
    parser = argparse.ArgumentParser(description="Scrape Social Media Inhalte.")
    parser.add_argument("--urls_file", required=True, help="Pfad zur JSON-Datei mit den URLs (aus search_niche.py).")

    args = parser.parse_args()

    if not os.path.exists(args.urls_file):
        print(f"Datei nicht gefunden: {args.urls_file}")
        return

    with open(args.urls_file, "r", encoding="utf-8") as f:
        urls_data = json.load(f)

    # Separiere URLs nach Plattform
    reddit_urls = [u for u in urls_data if is_reddit_url(u.get("url", ""))]
    hn_urls = [u for u in urls_data if is_hn_url(u.get("url", ""))]
    ph_urls = [u for u in urls_data if is_producthunt_url(u.get("url", ""))]
    quora_urls = [u for u in urls_data if is_quora_url(u.get("url", ""))]
    other_urls = [u for u in urls_data if not any([
        is_reddit_url(u.get("url", "")),
        is_hn_url(u.get("url", "")),
        is_producthunt_url(u.get("url", "")),
        is_quora_url(u.get("url", ""))
    ])]

    print(f"Gefunden: {len(reddit_urls)} Reddit, {len(hn_urls)} HackerNews, {len(ph_urls)} ProductHunt, {len(quora_urls)} Quora, {len(other_urls)} andere URLs")

    scraped_data = []

    # Reddit Deep Scraping (via scrape_reddit.py)
    if reddit_urls:
        print(f"\n=== Reddit Deep Scraping ({len(reddit_urls)} Threads) ===")
        reddit_results = scrape_reddit_urls(reddit_urls)
        scraped_data.extend(reddit_results)

    # HackerNews Deep Scraping (via scrape_hn.py)
    if hn_urls:
        print(f"\n=== HackerNews Deep Scraping ({len(hn_urls)} Stories) ===")
        hn_results = scrape_hn_urls(hn_urls)
        scraped_data.extend(hn_results)

    # ProductHunt Deep Scraping (via scrape_producthunt.py)
    if ph_urls:
        print(f"\n=== ProductHunt Deep Scraping ({len(ph_urls)} Posts) ===")
        ph_results = scrape_producthunt_urls(ph_urls)
        scraped_data.extend(ph_results)

    # Quora Deep Scraping (via scrape_quora.py)
    if quora_urls:
        print(f"\n=== Quora Deep Scraping ({len(quora_urls)} Fragen) ===")
        quora_results = scrape_quora_urls(quora_urls)
        scraped_data.extend(quora_results)

    # Andere URLs mit Jina
    if other_urls:
        print(f"\n=== Jina Scraping ({len(other_urls)} URLs) ===")
        for item in other_urls:
            url = item.get("url")
            title = item.get("title")

            if not url:
                continue

            print(f"Scrape: {url}")
            content = scrape_with_jina(url)

            if content:
                if len(content) < 200:
                    print(f"Warnung: Inhalt sehr kurz ({len(content)} Zeichen). Eventuell Blocked/Login.")

                scraped_data.append({
                    "url": url,
                    "title": title,
                    "content": content,
                    "scraped_at": datetime.now().isoformat(),
                    "source": "jina"
                })

            time.sleep(1.5)

    # Speichern
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = ".tmp"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = f"{output_dir}/scraped_content_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*50}")
    print(f"Scraping abgeschlossen. {len(scraped_data)} Seiten erfolgreich geladen.")
    print(f"  - Reddit Deep: {len([s for s in scraped_data if s.get('source') == 'reddit_deep'])}")
    print(f"  - HackerNews Deep: {len([s for s in scraped_data if s.get('source') == 'hn_deep'])}")
    print(f"  - ProductHunt Deep: {len([s for s in scraped_data if s.get('source') == 'producthunt_deep'])}")
    print(f"  - Quora Deep: {len([s for s in scraped_data if s.get('source') == 'quora_deep'])}")
    print(f"  - Jina: {len([s for s in scraped_data if s.get('source') == 'jina'])}")
    print(f"Daten gespeichert in: {output_file}")

if __name__ == "__main__":
    main()
