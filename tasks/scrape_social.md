# Task: Social Media Content Scrapen (Multi-Plattform)

## Ziel

Scrape Social Media Inhalte von mehreren Plattformen mit automatischer Erkennung und Delegation an spezialisierte Scraper.

## Eingaben

- `--urls_file`: JSON-Datei mit URLs (typischerweise aus search_niche.py)

**Format der Eingabe-Datei:**
```json
[
  {"url": "https://reddit.com/r/...", "title": "Thread Title"},
  {"url": "https://news.ycombinator.com/item?id=...", "title": "Story Title"},
  {"url": "https://producthunt.com/posts/...", "title": "Product Name"},
  {"url": "https://quora.com/...", "title": "Question"},
  {"url": "https://example.com/blog/...", "title": "Blog Post"}
]
```

## Ausgaben

- JSON-Datei in `.tmp/scraped_content_TIMESTAMP.json`

**Output-Struktur:**
```json
[
  {
    "url": "https://...",
    "title": "Content Title",
    "content": "Formatierter Markdown-Content",
    "scraped_at": "2024-01-08T12:00:00",
    "source": "reddit_deep|hn_deep|producthunt_deep|quora_deep|jina",
    "metadata": {
      "score": 500,
      "num_comments": 234,
      "subreddit": "programming"
    }
  }
]
```

## Tool

`tools/scrape_social.py`

## Ablauf

1. Lade URLs aus JSON-Datei
2. Erkenne Plattform fuer jede URL:
   - `reddit.com`, `redd.it` -> Reddit
   - `news.ycombinator.com`, `hacker-news.firebaseio.com` -> HackerNews
   - `producthunt.com` -> ProductHunt
   - `quora.com` -> Quora
   - Andere -> Jina Reader
3. Delegiere an entsprechenden Scraper:
   - Reddit -> `scrape_reddit.py`
   - HackerNews -> `scrape_hn.py`
   - ProductHunt -> `scrape_producthunt.py`
   - Quora -> `scrape_quora.py`
   - Andere -> Jina Reader API
4. Sammle alle Ergebnisse
5. Speichere in `.tmp/`

## Beispiel

```bash
# URLs aus search_niche.py scrapen
python tools/scrape_social.py --urls_file .tmp/search_urls_20240108.json
```

## Randfaelle

- Jina Reader fuer unbekannte Plattformen (Blogs, News-Seiten, etc.)
- Kurze Inhalte (<200 Zeichen) werden mit Warnung geloggt (evtl. Login-Wall)
- Rate-Limiting:
  - Reddit: 2 Sekunden
  - HackerNews: 1 Sekunde
  - ProductHunt: 1 Sekunde
  - Quora: 2 Sekunden
  - Jina: 1.5 Sekunden

## Abhaengigkeiten

**Erforderliche Umgebungsvariablen:**
- `SCRAPINGBEE_API_KEY`: Fuer Reddit und Quora
- `PH_CLIENT_ID`, `PH_CLIENT_SECRET`: Fuer ProductHunt
- `JINA_API_KEY` (optional): Fuer hoehere Limits bei Jina Reader

**Importierte Module:**
- `scrape_reddit.py`
- `scrape_hn.py`
- `scrape_producthunt.py`
- `scrape_quora.py`

## Gelernte Lektionen

- Multi-Plattform-Scraping ist komplex, Delegation an spezialisierte Scraper vereinfacht
- Source-Feld im Output wichtig fuer spaetere Filterung
- Metadata-Feld enthaelt plattform-spezifische Informationen
- Jina Reader ist guter Fallback fuer unbekannte Plattformen
