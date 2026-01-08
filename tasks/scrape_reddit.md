# Task: Reddit Thread Scrapen

## Ziel

Extrahiere einen Reddit Thread mit allen Comments (inkl. nested Replies) fuer Community-Research und Content-Analyse.

## Eingaben

- `--url`: Einzelne Reddit Thread URL
- `--urls_file`: JSON-Datei mit mehreren URLs (aus search_niche.py)
- `--format_for_analysis` (optional): Formatiert Output fuer Claude-Analyse

## Ausgaben

- JSON-Datei in `.tmp/reddit_threads_TIMESTAMP.json`
- Formatierter Markdown (wenn `--format_for_analysis`)

**Output-Struktur:**
```json
{
  "id": "abc123",
  "title": "Thread Title",
  "author": "username",
  "selftext": "Post body text",
  "score": 500,
  "upvote_ratio": 0.95,
  "num_comments": 234,
  "created_at": "2024-01-08T12:00:00",
  "subreddit": "programming",
  "url": "https://reddit.com/r/...",
  "permalink": "https://reddit.com/r/.../comments/...",
  "comments": [/* nested Struktur */],
  "comments_flat": [/* flache Liste fuer Analyse */]
}
```

## Tool

`tools/scrape_reddit.py`

## Ablauf

1. URL(s) uebergeben (einzeln oder aus Datei)
2. Script normalisiert Reddit URL
3. Fuegt `.json` an URL an (Reddit's JSON-API)
4. Holt Daten via ScrapingBee (umgeht Bot-Detection)
5. Extrahiert Post-Daten und alle Comments rekursiv
6. Flacht Comment-Tree fuer einfachere Analyse
7. Speichert in `.tmp/`

## Beispiel

```bash
# Einzelner Thread
python tools/scrape_reddit.py --url "https://www.reddit.com/r/programming/comments/abc123/title/"

# Mehrere URLs aus Datei
python tools/scrape_reddit.py --urls_file .tmp/search_urls.json

# Mit Analyse-Formatierung
python tools/scrape_reddit.py --url "..." --format_for_analysis
```

## Randfaelle

- Geloeschte/entfernte Comments (`[deleted]`, `[removed]`) werden uebersprungen
- "more" Pagination-Marker werden uebersprungen (nicht alle Comments bei sehr grossen Threads)
- Rate-Limiting: 2 Sekunden Pause zwischen Requests
- old.reddit.com, new.reddit.com, np.reddit.com werden zu www.reddit.com normalisiert

## Abhaengigkeiten

**Erforderliche Umgebungsvariablen:**
- `SCRAPINGBEE_API_KEY`: ScrapingBee API Key

**Kosten:**
- ScrapingBee Credits (Premium Proxy noetig fuer Reddit)
- Kein JS-Rendering noetig (JSON-API)

## Gelernte Lektionen

- Reddit's JSON-API ist stabil und strukturiert
- Bot-Detection erfordert Premium Proxy bei ScrapingBee
- `is_submitter` Flag markiert OP-Comments (wichtig fuer Analyse)
- Sehr grosse Threads haben "more" Placeholders (nicht vollstaendig extrahiert)
