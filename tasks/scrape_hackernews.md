# Task: HackerNews Story Scrapen

## Ziel

Extrahiere eine HackerNews Story mit allen Comments (inkl. nested Replies) fuer Analyse und Content-Research.

## Eingaben

- `--url`: HackerNews Story URL (z.B. `https://news.ycombinator.com/item?id=12345`)
- `--output` (optional): Pfad fuer JSON-Output

## Ausgaben

- JSON-Datei mit Story-Daten und allen Comments (wenn `--output` angegeben)
- Formatierter Markdown-Output auf stdout (wenn kein `--output`)

**Output-Struktur:**
```json
{
  "id": "12345",
  "title": "Story Title",
  "url": "https://...",
  "score": 500,
  "author": "username",
  "num_comments": 234,
  "created_at": "2024-01-08T12:00:00",
  "text": "Bei Ask HN gibt es Text hier",
  "comments": [/* nested Struktur */],
  "comments_flat": [/* flache Liste fuer Analyse */]
}
```

## Tool

`tools/scrape_hn.py`

## Ablauf

1. URL uebergeben (Story oder Item-ID)
2. Script extrahiert Story-ID aus URL
3. Laedt Story-Daten von Firebase API
4. Laedt rekursiv alle Comments (parallel mit ThreadPoolExecutor)
5. Formatiert Comments als Markdown (mit Verschachtelung als `>` Bloecke)
6. Speichert oder gibt aus

## Beispiel

```bash
# Einzelne Story scrapen und auf stdout ausgeben
python tools/scrape_hn.py --url "https://news.ycombinator.com/item?id=12345"

# Mit JSON-Output
python tools/scrape_hn.py --url "https://news.ycombinator.com/item?id=12345" --output .tmp/hn_story.json
```

## Randfaelle

- Geloeschte/tote Comments werden uebersprungen
- Sehr lange Comments werden auf 1500 Zeichen gekuerzt
- Formatierter Output wird auf 50000 Zeichen begrenzt
- HTML-Tags in Comments werden entfernt (HN speichert HTML)

## Abhaengigkeiten

- Keine API-Keys erforderlich (kostenlose Firebase API)
- `requests` Python-Paket

## Gelernte Lektionen

- HackerNews Firebase API ist kostenlos und zuverlaessig
- Parallel-Loading mit ThreadPoolExecutor (max 10 workers) ist wichtig fuer Performance
- Comments koennen tief verschachtelt sein (depth tracking wichtig)
