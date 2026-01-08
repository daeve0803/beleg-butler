#!/usr/bin/env python3
"""
Quora Deep Question Scraper.

Nutzt ScrapingBee um Quora-Fragen mit allen Answers zu extrahieren.
Quora hat keine offizielle API, daher Web Scraping.

Voraussetzungen:
- SCRAPINGBEE_API_KEY in .env (bereits vorhanden)
"""
import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import requests

# Lade .env
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

SCRAPINGBEE_API_KEY = os.getenv("SCRAPINGBEE_API_KEY", "")
SCRAPINGBEE_URL = "https://app.scrapingbee.com/api/v1/"


def scrape_with_scrapingbee(url: str, wait_for: str = None) -> Optional[str]:
    """
    Scrapt eine URL mit ScrapingBee.

    Args:
        url: Die zu scrapende URL
        wait_for: CSS Selector auf den gewartet werden soll

    Returns:
        HTML-Content oder None bei Fehler
    """
    if not SCRAPINGBEE_API_KEY:
        print("Fehler: SCRAPINGBEE_API_KEY nicht in .env gesetzt.")
        return None

    params = {
        "api_key": SCRAPINGBEE_API_KEY,
        "url": url,
        "render_js": "true",  # JavaScript rendern für dynamischen Content
        "premium_proxy": "true",  # Premium Proxy für Anti-Bot Bypass
        "country_code": "us",
    }

    if wait_for:
        params["wait_for"] = wait_for

    try:
        response = requests.get(SCRAPINGBEE_URL, params=params, timeout=60)
        if response.status_code == 200:
            return response.text
        else:
            print(f"ScrapingBee Fehler: {response.status_code}")
            return None
    except Exception as e:
        print(f"ScrapingBee Request fehlgeschlagen: {e}")
        return None


def extract_question_title(soup: BeautifulSoup) -> str:
    """Extrahiert den Frage-Titel."""
    # Quora speichert den Titel in verschiedenen Elementen
    selectors = [
        'div[class*="q-text"] span[class*="q-text"]',
        'h1 span',
        'div[class*="puppeteer_test_question_title"]',
        '.q-box h1',
    ]

    for selector in selectors:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            return element.get_text(strip=True)

    # Fallback: Title-Tag
    title = soup.find('title')
    if title:
        text = title.get_text(strip=True)
        # Entferne " - Quora" Suffix
        return re.sub(r'\s*-\s*Quora\s*$', '', text)

    return "Unbekannte Frage"


def extract_answers(soup: BeautifulSoup) -> List[Dict]:
    """
    Extrahiert alle Answers aus der Seite.

    Returns:
        Liste von Answer-Dictionaries
    """
    answers = []

    # Quora hat verschiedene Answer-Container
    # Diese Selectors können sich ändern, da Quora kein stabiles HTML hat
    answer_containers = soup.select('div[class*="q-box"][class*="qu-borderAll"]')

    if not answer_containers:
        # Alternativer Selector
        answer_containers = soup.select('div[class*="Answer"]')

    if not answer_containers:
        # Noch ein Versuch
        answer_containers = soup.select('div[class*="spacing_log_answer_content"]')

    for i, container in enumerate(answer_containers):
        try:
            # Author
            author_elem = container.select_one('span[class*="q-text"] a')
            author = author_elem.get_text(strip=True) if author_elem else f"Anonymous-{i+1}"

            # Content
            content_elem = container.select_one('div[class*="q-text"][class*="qu-wordBreak"]')
            if not content_elem:
                content_elem = container.select_one('span[class*="q-text"]')

            content = ""
            if content_elem:
                # Extrahiere Text, behalte Absätze
                for p in content_elem.find_all(['p', 'span'], recursive=True):
                    text = p.get_text(strip=True)
                    if text and len(text) > 20:  # Filtere kurze Snippets
                        content += text + "\n\n"

                if not content:
                    content = content_elem.get_text(strip=True)

            if not content or len(content) < 50:
                continue  # Skip sehr kurze oder leere Answers

            # Upvotes (schwer zu extrahieren, Quora zeigt "K" Format)
            upvotes = 0
            upvote_elem = container.select_one('button[class*="Upvote"] span')
            if upvote_elem:
                upvote_text = upvote_elem.get_text(strip=True)
                # Parse "1.2K" -> 1200
                if 'K' in upvote_text:
                    try:
                        upvotes = int(float(upvote_text.replace('K', '')) * 1000)
                    except ValueError:
                        pass
                else:
                    try:
                        upvotes = int(upvote_text)
                    except ValueError:
                        pass

            answers.append({
                "id": str(i + 1),
                "author": author,
                "body": content.strip(),
                "upvotes": upvotes,
                "depth": 0
            })

        except Exception as e:
            print(f"  Fehler beim Parsen von Answer {i+1}: {e}")
            continue

    return answers


def scrape_question(url: str) -> Optional[Dict]:
    """
    Scrapt eine Quora-Frage mit allen Answers.

    Args:
        url: Quora Question URL

    Returns:
        Dictionary mit Frage-Daten und allen Answers
    """
    print(f"  Scrape Quora: {url}")

    # Normalisiere URL
    if not url.startswith("http"):
        url = "https://" + url

    # Scrape mit ScrapingBee
    html = scrape_with_scrapingbee(url, wait_for='div[class*="q-text"]')
    if not html:
        print("  -> HTML konnte nicht geladen werden")
        return None

    if len(html) < 1000:
        print(f"  -> Warnung: Sehr wenig Content ({len(html)} chars)")

    soup = BeautifulSoup(html, 'html.parser')

    # Extrahiere Frage
    question_title = extract_question_title(soup)
    print(f"  -> Frage: {question_title[:80]}...")

    # Extrahiere Answers
    answers = extract_answers(soup)
    print(f"  -> {len(answers)} Answers gefunden")

    if not answers:
        # Fallback: Versuche Jina Reader
        print("  -> Keine Answers gefunden, versuche Jina Reader als Fallback...")
        jina_url = f"https://r.jina.ai/{url}"
        try:
            response = requests.get(jina_url, timeout=60)
            if response.status_code == 200:
                # Parse als einfacher Text
                text = response.text
                answers = [{
                    "id": "1",
                    "author": "Quora User",
                    "body": text[:10000],
                    "upvotes": 0,
                    "depth": 0
                }]
                print(f"  -> Jina Fallback: {len(text)} chars")
        except Exception as e:
            print(f"  -> Jina Fallback fehlgeschlagen: {e}")

    # Sortiere nach Upvotes
    answers.sort(key=lambda x: x.get("upvotes", 0), reverse=True)

    # Top Answer Upvotes
    top_upvotes = answers[0].get("upvotes", 0) if answers else 0

    result = {
        "url": url,
        "title": question_title,
        "num_answers": len(answers),
        "top_answer_upvotes": top_upvotes,
        "scraped_at": datetime.now().isoformat(),
        "answers": answers,
        "answers_flat": answers  # Quora hat keine nested replies
    }

    return result


def format_for_analysis(question_data: Dict, max_chars: int = 50000) -> str:
    """
    Formatiert die Quora-Daten als Markdown für Claude-Analyse.
    """
    lines = []

    # Question Header
    lines.append(f"# {question_data.get('title', 'Unbekannte Frage')}")
    lines.append(f"**Answers:** {question_data.get('num_answers', 0)}")
    if question_data.get('top_answer_upvotes', 0) > 0:
        lines.append(f"**Top Answer Upvotes:** {question_data['top_answer_upvotes']}")
    lines.append("")

    # Answers
    answers = question_data.get("answers", [])
    if answers:
        lines.append("## Answers")
        lines.append("")

        for answer in answers:
            author = answer.get("author", "Anonymous")
            body = answer.get("body", "")[:2000]  # Limit pro Answer
            upvotes = answer.get("upvotes", 0)

            lines.append(f"### {author}" + (f" ({upvotes} upvotes)" if upvotes > 0 else ""))
            lines.append(body)
            lines.append("")

    result = "\n".join(lines)

    if len(result) > max_chars:
        result = result[:max_chars] + "\n\n[... truncated ...]"

    return result


def main():
    parser = argparse.ArgumentParser(description="Scrape Quora Question mit allen Answers.")
    parser.add_argument("--url", required=True, help="Quora Question URL")
    parser.add_argument("--output", help="Output JSON file (optional)")

    args = parser.parse_args()

    print(f"Scraping Quora: {args.url}")
    question_data = scrape_question(args.url)

    if question_data:
        formatted = format_for_analysis(question_data)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(question_data, f, indent=2, ensure_ascii=False)
            print(f"Gespeichert: {args.output}")
        else:
            print("\n" + "="*50)
            print(formatted[:3000])
            print("="*50)
            print(f"\nFrage: {question_data['title'][:80]}")
            print(f"Answers: {question_data['num_answers']}")
    else:
        print("Scraping fehlgeschlagen.")


if __name__ == "__main__":
    main()
