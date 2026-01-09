# Ralph Loop - Self-Correction & Autonome Tasks

## Zweck

Ralph Wiggum ist ein autonomer Loop fuer:
- **Self-Healing:** Nach Fehlern automatisch analysieren und Fixes vorschlagen
- **Komplexe Tasks:** Multi-Step Aufgaben iterativ abarbeiten
- **Semi-Autonom:** Ralph schlaegt vor, Mensch genehmigt

## Eingaben

| Eingabe | Datei | Beschreibung |
|---------|-------|--------------|
| Anweisungen | `PROMPT.md` | Grundregeln und Kontext |
| Tasks | `@fix_plan.md` | Priorisierte Aufgabenliste |
| Kontext | `.claude/context/session_current.md` | Optional: Session-Kontext |

## Prozess

### 1. Session vorbereiten
```bash
# @fix_plan.md mit Tasks befuellen
# Beispiel:
cat > @fix_plan.md << 'EOF'
# Fix Plan - 2025-01-09

## Status: PENDING

## Aktuelle Session: Feature X implementieren

## Tasks (priorisiert)
- [ ] Task 1: Requirements analysieren
- [ ] Task 2: Existierende Tools pruefen
- [ ] Task 3: Implementation planen
- [ ] Task 4: Code schreiben
- [ ] Task 5: Testen

## Genehmigungen benoetigt

## Learnings
EOF
```

### 2. Ralph starten
```bash
cd /Users/davidmacbookair/Beleg.Butler
ralph --monitor
# Oder direkt:
.ralph/ralph_loop.sh --monitor
```

### 3. Waehrend Ralph arbeitet
- Ralph liest PROMPT.md und @fix_plan.md
- Arbeitet Tasks ab
- Aktualisiert @fix_plan.md
- Bei Unsicherheit: Stoppt mit BLOCKED

### 4. Bei BLOCKED-Status
1. Lies @fix_plan.md → "Genehmigungen benoetigt"
2. Entscheide (genehmigen, ablehnen, aendern)
3. Aktualisiere @fix_plan.md
4. Ralph setzt fort

### 5. Nach Code-Aenderungen
```bash
# Reviewer-Agent ausfuehren (PFLICHT)
# Ralph empfiehlt dies automatisch
```

### 6. Nach Abschluss
- @fix_plan.md Status: DONE
- Learnings dokumentiert
- Optional: Documenter-Agent fuer tasks/ Update

## Ausgaben

| Ausgabe | Ort | Beschreibung |
|---------|-----|--------------|
| Status | `@fix_plan.md` | DONE, BLOCKED, oder ERROR |
| Logs | `logs/` | Ausfuehrungsprotokolle |
| Learnings | `@fix_plan.md` | Was waehrend Session gelernt wurde |

## CLI-Optionen

```bash
ralph --monitor           # Mit tmux Dashboard (empfohlen)
ralph --verbose           # Detaillierte Ausgabe
ralph --calls 50          # Max 50 API-Calls/Stunde
ralph --timeout 30        # 30 Min Timeout pro Iteration
ralph --status            # Aktuellen Status zeigen
ralph --reset-circuit     # Circuit Breaker zuruecksetzen
```

## Randfaelle

### Rate Limit erreicht
- Ralph pausiert automatisch
- Circuit Breaker oeffnet nach 3 Loops ohne Fortschritt
- Loesung: `ralph --calls 50` fuer niedrigeres Limit

### Endlosschleife
- Circuit Breaker greift nach 5 Loops mit gleichen Fehlern
- Loesung: `ralph --reset-circuit` nach manuellem Fix

### BLOCKED aber kein Eintrag in "Genehmigungen benoetigt"
- Bug: Ralph hat vergessen zu dokumentieren
- Loesung: Lies Logs in `logs/`, identifiziere Issue manuell

## Integration mit Subagents

```
Ralph Loop
    |
    v
[Code-Aenderung erkannt]
    |
    v
Ralph: "Reviewer-Agent sollte ausgefuehrt werden"
    |
    v
[Benutzer triggert Reviewer]
    |
    v
Reviewer: Feedback in Context-Session
    |
    v
Ralph: Verarbeitet Feedback als neuer Task
    |
    v
[Nach Abschluss]
    |
    v
Documenter: Aktualisiert tasks/
```

## Komponenten

### Kern-Skripte (.ralph/)
| Skript | Beschreibung |
|--------|--------------|
| `ralph_loop.sh` | Haupt-Loop mit Rate-Limiting und Circuit-Breaker |
| `ralph_monitor.sh` | Live-Dashboard fuer Status-Anzeige |
| `ralph_import.sh` | PRD-Import und Konvertierung |
| `setup.sh` | Projekt-Setup fuer neue Ralph-Projekte |

### Bibliotheken (.ralph/lib/)
| Library | Beschreibung |
|---------|--------------|
| `circuit_breaker.sh` | Verhindert Token-Verschwendung bei Stagnation |
| `response_analyzer.sh` | Analysiert Claude-Output auf Completion-Signale |
| `date_utils.sh` | Cross-Platform Datum-Utilities (macOS/Linux) |

### Templates (.ralph/templates/)
| Template | Beschreibung |
|----------|--------------|
| `PROMPT.md` | Vorlage fuer Ralph-Anweisungen |
| `fix_plan.md` | Vorlage fuer @fix_plan.md |
| `AGENT.md` | Vorlage fuer Build-Anweisungen |

### Subagent (.claude/agents/)
| Agent | Beschreibung |
|-------|--------------|
| `ralph.md` | Self-Correction Loop Agent fuer Fehler-Analyse |

## Learnings

- Ralph ist NICHT fuer einfache Tasks - nutze Claude Code direkt
- Semi-Autonomie ist wichtig: Immer @fix_plan.md pruefen
- Circuit Breaker schuetzt vor API-Kosten-Explosion
- tmux --monitor ist die beste Art Ralph zu nutzen
- Context-Sessions nutzen fuer Subagent-Koordination (siehe tasks/context_session.md)
