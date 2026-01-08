#!/usr/bin/env python3
"""
ProductHunt Deep Post Scraper.

Nutzt die offizielle GraphQL API um Posts und alle Comments zu extrahieren.
API Docs: https://api.producthunt.com/v2/docs

Voraussetzungen:
- PH_CLIENT_ID und PH_CLIENT_SECRET in .env
- Developer Account: https://api.producthunt.com/v2/oauth/applications
"""
import argparse
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import requests

# Lade .env
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

PH_CLIENT_ID = os.getenv("PH_CLIENT_ID", "")
PH_CLIENT_SECRET = os.getenv("PH_CLIENT_SECRET", "")
PH_API_URL = "https://api.producthunt.com/v2/api/graphql"
PH_TOKEN_URL = "https://api.producthunt.com/v2/oauth/token"

# Token Cache
_access_token = None
_token_expires = 0


def get_access_token() -> Optional[str]:
    """
    Holt einen OAuth Access Token von ProductHunt.
    Token wird gecached bis er abläuft.
    """
    global _access_token, _token_expires

    # Check Cache
    if _access_token and time.time() < _token_expires:
        return _access_token

    if not PH_CLIENT_ID or not PH_CLIENT_SECRET:
        print("Fehler: PH_CLIENT_ID und PH_CLIENT_SECRET müssen in .env gesetzt sein.")
        print("Erstelle einen Developer Account: https://api.producthunt.com/v2/oauth/applications")
        return None

    try:
        response = requests.post(PH_TOKEN_URL, data={
            "client_id": PH_CLIENT_ID,
            "client_secret": PH_CLIENT_SECRET,
            "grant_type": "client_credentials"
        }, timeout=30)

        if response.status_code == 200:
            data = response.json()
            _access_token = data.get("access_token")
            # Token ist 2 Wochen gültig, wir cachen für 1 Woche
            _token_expires = time.time() + (7 * 24 * 60 * 60)
            return _access_token
        else:
            print(f"Token-Fehler: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Token-Anfrage fehlgeschlagen: {e}")
        return None


def extract_slug(url: str) -> Optional[str]:
    """
    Extrahiert den Post-Slug aus einer ProductHunt-URL.

    Beispiele:
    - https://www.producthunt.com/posts/notion -> notion
    - https://www.producthunt.com/products/notion -> notion
    """
    # Pattern: /posts/slug oder /products/slug
    match = re.search(r'/(?:posts|products)/([^/?#]+)', url)
    if match:
        return match.group(1)
    return None


def graphql_query(query: str, variables: Dict = None) -> Optional[Dict]:
    """Führt eine GraphQL Query aus."""
    token = get_access_token()
    if not token:
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            PH_API_URL,
            headers=headers,
            json={"query": query, "variables": variables or {}},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print(f"GraphQL Fehler: {data['errors']}")
                return None
            return data.get("data")
        else:
            print(f"API Fehler: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"GraphQL Query fehlgeschlagen: {e}")
        return None


def scrape_post(url: str) -> Optional[Dict]:
    """
    Scrapt einen ProductHunt-Post mit allen Comments.

    Args:
        url: ProductHunt Post URL

    Returns:
        Dictionary mit Post-Daten und allen Comments
    """
    slug = extract_slug(url)
    if not slug:
        print(f"Konnte Slug nicht aus URL extrahieren: {url}")
        return None

    print(f"  Lade Post: {slug}...")

    # GraphQL Query für Post + Comments (vereinfacht für Complexity-Limit)
    query = """
    query GetPost($slug: String!) {
      post(slug: $slug) {
        id
        name
        tagline
        description
        url
        votesCount
        commentsCount
        createdAt
        comments(first: 15) {
          edges {
            node {
              id
              body
              votesCount
              createdAt
              user {
                name
              }
              replies(first: 5) {
                edges {
                  node {
                    id
                    body
                    votesCount
                    user {
                      name
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    data = graphql_query(query, {"slug": slug})
    if not data or not data.get("post"):
        print(f"  Post nicht gefunden: {slug}")
        return None

    post = data["post"]

    # Extrahiere Comments
    comments = []
    comments_flat = []

    for edge in post.get("comments", {}).get("edges", []):
        node = edge.get("node", {})
        if not node:
            continue

        comment = {
            "id": node.get("id", ""),
            "author": node.get("user", {}).get("name", node.get("user", {}).get("username", "unknown")),
            "body": node.get("body", ""),
            "votes": node.get("votesCount", 0),
            "depth": 0,
            "created_at": node.get("createdAt", ""),
            "replies": []
        }

        # Flat version
        comments_flat.append({
            "id": comment["id"],
            "author": comment["author"],
            "body": comment["body"],
            "votes": comment["votes"],
            "depth": 0,
            "created_at": comment["created_at"],
            "parent_author": None
        })

        # Replies
        for reply_edge in node.get("replies", {}).get("edges", []):
            reply_node = reply_edge.get("node", {})
            if not reply_node:
                continue

            reply = {
                "id": reply_node.get("id", ""),
                "author": reply_node.get("user", {}).get("name", reply_node.get("user", {}).get("username", "unknown")),
                "body": reply_node.get("body", ""),
                "votes": reply_node.get("votesCount", 0),
                "depth": 1,
                "created_at": reply_node.get("createdAt", "")
            }
            comment["replies"].append(reply)

            comments_flat.append({
                "id": reply["id"],
                "author": reply["author"],
                "body": reply["body"],
                "votes": reply["votes"],
                "depth": 1,
                "created_at": reply["created_at"],
                "parent_author": comment["author"]
            })

        comments.append(comment)

    result = {
        "id": post.get("id", ""),
        "name": post.get("name", ""),
        "tagline": post.get("tagline", ""),
        "description": post.get("description", ""),
        "url": url,
        "product_url": post.get("url", ""),
        "votes": post.get("votesCount", 0),
        "num_comments": post.get("commentsCount", 0),
        "created_at": post.get("createdAt", ""),
        "comments": comments,
        "comments_flat": comments_flat
    }

    print(f"  -> {len(comments_flat)} Comments, {result['votes']} Votes")
    return result


def format_for_analysis(post_data: Dict, max_chars: int = 50000) -> str:
    """
    Formatiert die Post-Daten als Markdown für Claude-Analyse.
    """
    lines = []

    # Post Header
    lines.append(f"# {post_data.get('name', 'Untitled')}")
    lines.append(f"**Tagline:** {post_data.get('tagline', '')}")
    lines.append(f"**Votes:** {post_data.get('votes', 0)} | **Comments:** {post_data.get('num_comments', 0)}")
    lines.append("")

    # Description
    if post_data.get("description"):
        lines.append("## Description")
        lines.append(post_data["description"][:2000])
        lines.append("")

    # Comments - sortiert nach Votes
    comments_flat = post_data.get("comments_flat", [])
    if comments_flat:
        lines.append("## Comments")
        lines.append("")

        # Sortiere nach Votes (höchste zuerst)
        sorted_comments = sorted(comments_flat, key=lambda x: (x["depth"], -x.get("votes", 0)))

        for comment in sorted_comments:
            depth_marker = ">" * comment["depth"] if comment["depth"] > 0 else ""
            author = comment["author"]
            body = comment["body"][:1500]
            votes = comment.get("votes", 0)

            if depth_marker:
                lines.append(f"{depth_marker} **{author}** ({votes} votes):")
                lines.append(f"{depth_marker} {body}")
            else:
                lines.append(f"**{author}** ({votes} votes):")
                lines.append(body)
            lines.append("")

    result = "\n".join(lines)

    if len(result) > max_chars:
        result = result[:max_chars] + "\n\n[... truncated ...]"

    return result


def main():
    parser = argparse.ArgumentParser(description="Scrape ProductHunt Post mit allen Comments.")
    parser.add_argument("--url", required=True, help="ProductHunt Post URL")
    parser.add_argument("--output", help="Output JSON file (optional)")

    args = parser.parse_args()

    print(f"Scraping ProductHunt: {args.url}")
    post_data = scrape_post(args.url)

    if post_data:
        formatted = format_for_analysis(post_data)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(post_data, f, indent=2, ensure_ascii=False)
            print(f"Gespeichert: {args.output}")
        else:
            print("\n" + "="*50)
            print(formatted[:3000])
            print("="*50)
            print(f"\nPost: {post_data['name']}")
            print(f"Votes: {post_data['votes']}")
            print(f"Comments: {len(post_data['comments_flat'])}")
    else:
        print("Scraping fehlgeschlagen.")


if __name__ == "__main__":
    main()
