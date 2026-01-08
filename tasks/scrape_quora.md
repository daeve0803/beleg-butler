# Task: Quora Frage Scrapen

## Ziel

Extrahiere eine Quora-Frage mit allen Answers fuer Content-Research und Themenfindung.

## Eingaben

- `--url`: Quora Question URL (z.B. `https://www.quora.com/What-is-the-best-way-to-learn-Python`)
- `--output` (optional): Pfad fuer JSON-Output

## Ausgaben

- JSON-Datei mit Frage und allen Answers (wenn `--output` angegeben)
- Formatierter Markdown-Output auf stdout (wenn kein `--output`)

**Output-Struktur:**
```json
{
  "url": "https://quora.com/...",
  "title": "Frage-Titel",
  "num_answers": 15,
  "top_answer_upvotes": 1234,
  "scraped_at": "2024-01-08T12:00:00",
  "answers": [
    {
      "id": "1",
      "author": "Username",
      "body": "Answer text...",
      "upvotes": 500,
      "depth": 0
    }
  ],
  "answers_flat": [/* identisch, da Quora keine nested replies hat */]
}
```

## Tool

`tools/scrape_quora.py`

## Ablauf

1. URL uebergeben
2. Script normalisiert URL (fuegt https:// hinzu wenn noetig)
3. Scrapt Seite mit ScrapingBee (JS-Rendering + Premium Proxy)
4. Parst HTML mit BeautifulSoup
5. Extrahiert Frage-Titel und alle Answers
6. Sortiert Answers nach Upvotes
7. Bei Fehlschlag: Fallback auf Jina Reader

## Beispiel

```bash
# Frage scrapen
python tools/scrape_quora.py --url "https://www.quora.com/What-is-the-best-way-to-learn-Python"

# Mit JSON-Output
python tools/scrape_quora.py --url "https://www.quora.com/What-is-the-best-way-to-learn-Python" --output .tmp/quora_question.json
```

## Randfaelle

- Quora hat kein stabiles HTML (CSS-Selectors aendern sich oft)
- Kurze Answers (<50 Zeichen) werden uebersprungen
- Upvotes im "K"-Format (z.B. "1.2K") werden zu Zahlen konvertiert
- Wenn ScrapingBee fehlschlaegt, wird Jina Reader als Fallback versucht
- Geloeschte/anonyme Autoren werden als "Anonymous-N" markiert

## Abhaengigkeiten

**Erforderliche Umgebungsvariablen:**
- `SCRAPINGBEE_API_KEY`: ScrapingBee API Key

**Kosten:**
- ScrapingBee Credits werden verbraucht (Premium Proxy + JS-Rendering)
- Ca. 25 Credits pro Request

## Gelernte Lektionen

- Quora blockiert Standard-Scraper aggressiv
- Premium Proxy bei ScrapingBee ist erforderlich
- HTML-Struktur ist instabil, mehrere Fallback-Selectors noetig
- Jina Reader als Fallback liefert weniger strukturierte Daten, aber funktioniert
