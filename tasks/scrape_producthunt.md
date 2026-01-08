# Task: ProductHunt Post Scrapen

## Ziel

Extrahiere einen ProductHunt Post mit allen Comments und Replies fuer Marktrecherche und Wettbewerbsanalyse.

## Eingaben

- `--url`: ProductHunt Post URL (z.B. `https://www.producthunt.com/posts/notion`)
- `--output` (optional): Pfad fuer JSON-Output

## Ausgaben

- JSON-Datei mit Post-Daten und allen Comments (wenn `--output` angegeben)
- Formatierter Markdown-Output auf stdout (wenn kein `--output`)

**Output-Struktur:**
```json
{
  "id": "12345",
  "name": "Product Name",
  "tagline": "Short description",
  "description": "Full description",
  "url": "https://producthunt.com/...",
  "product_url": "https://product-website.com",
  "votes": 1234,
  "num_comments": 56,
  "created_at": "2024-01-08T12:00:00",
  "comments": [/* mit replies */],
  "comments_flat": [/* flache Liste */]
}
```

## Tool

`tools/scrape_producthunt.py`

## Ablauf

1. URL uebergeben
2. Script extrahiert Slug aus URL (`/posts/slug` oder `/products/slug`)
3. Holt OAuth Access Token (Client Credentials Flow)
4. Fuehrt GraphQL Query aus
5. Extrahiert Post + Comments + Replies
6. Formatiert als Markdown (sortiert nach Votes)

## Beispiel

```bash
# Post scrapen
python tools/scrape_producthunt.py --url "https://www.producthunt.com/posts/notion"

# Mit JSON-Output
python tools/scrape_producthunt.py --url "https://www.producthunt.com/posts/notion" --output .tmp/ph_post.json
```

## Randfaelle

- GraphQL Complexity-Limit: Nur 15 Top-Level Comments und 5 Replies pro Comment
- Token wird fuer 1 Woche gecached
- Wenn Slug nicht gefunden wird, schlaegt Scraping fehl

## Abhaengigkeiten

**Erforderliche Umgebungsvariablen:**
- `PH_CLIENT_ID`: ProductHunt OAuth Client ID
- `PH_CLIENT_SECRET`: ProductHunt OAuth Client Secret

**Setup:**
1. Erstelle Developer Account: https://api.producthunt.com/v2/oauth/applications
2. Erstelle neue Application
3. Kopiere Client ID und Secret in `.env`

## Gelernte Lektionen

- ProductHunt API hat Complexity-Limits fuer GraphQL Queries
- Token ist 2 Wochen gueltig, Script cached fuer 1 Woche
- Nicht alle Posts haben `description` (kann leer sein)
