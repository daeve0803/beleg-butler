# Context-Session System

## Zweck

Das Context-Session-System ermoeglicht geteiltes Wissen zwischen dem Haupt-Agent und Subagents. Da Claude Code Subagents keinen geteilten Kontext haben, dient die Session-Datei als Workaround fuer komplexe Aufgaben.

## Eingaben

| Eingabe | Datei | Beschreibung |
|---------|-------|--------------|
| Template | `.claude/context/templates/session_template.md` | Vorlage fuer neue Sessions |
| Aktive Session | `.claude/context/session_current.md` | Aktuelle Arbeits-Session |

## Dateien

### Session-Template
Befindet sich in `.claude/context/templates/session_template.md`:

```markdown
# Session: [Kurztitel]

## Auftrag
[Was soll erreicht werden?]

## Status
IN_PROGRESS | COMPLETED | BLOCKED

## Delegierte Tasks
### Task 1: [Name]
- **Subagent:** reviewer | documenter | linkedin | ralph
- **Status:** PENDING | IN_PROGRESS | DONE | FAILED
- **Ergebnis:** [Zusammenfassung]

## Offene Fragen
- [Was ist noch unklar?]

## Learnings (Self-Annealing)
- [Was wurde gelernt?]

## Finales Ergebnis
[Output fuer User]
```

### Aktive Session
`.claude/context/session_current.md` - Wird vor komplexen Aufgaben erstellt und waehrend der Arbeit aktualisiert.

## Prozess

### 1. Session erstellen (bei komplexen Aufgaben)
```bash
# Template kopieren
cp .claude/context/templates/session_template.md .claude/context/session_current.md

# Bearbeiten mit Auftragsdetails
```

### 2. Waehrend der Arbeit
- Status aktualisieren (IN_PROGRESS, BLOCKED, etc.)
- Delegierte Tasks dokumentieren
- Ergebnisse von Subagents eintragen
- Offene Fragen notieren

### 3. Nach Abschluss
- Status auf COMPLETED setzen
- Learnings dokumentieren (Self-Annealing)
- Finales Ergebnis eintragen
- Optional: Session archivieren nach `.claude/context/archive/`

## Wann verwenden

**Verwenden bei:**
- Komplexen Aufgaben (> 2 Schritte)
- Delegation an Subagents
- Multi-Session-Aufgaben
- Wenn Kontext zwischen Agents geteilt werden muss

**NICHT verwenden bei:**
- Einzeilige Aenderungen
- Einfache Dateien lesen
- Direkte Fragen beantworten
- Tasks < 2 Schritte

## SessionStart Hook

Der Hook `.claude/hooks/session_context_reminder.py` wird bei jedem Session-Start ausgeloest und:
1. Liest die aktuelle Session-Datei
2. Zeigt den aktuellen Status an
3. Erinnert an das Aktualisieren der Session bei komplexen Aufgaben

## Integration

### Mit Ralph-Loop
Ralph nutzt das Context-Session-System fuer:
- Uebergabe von Kontext zwischen Loops
- Dokumentation von Learnings
- Koordination mit anderen Subagents

### Mit Subagents
Subagents lesen `.claude/context/session_current.md` fuer:
- Auftragskontext
- Bisherige Ergebnisse
- Status anderer Tasks

## Archivierung

Nach Abschluss einer Session:
```bash
# Session archivieren mit Timestamp
mv .claude/context/session_current.md \
   .claude/context/archive/session_$(date +%Y%m%d_%H%M%S).md

# Neue leere Session aus Template erstellen (optional)
cp .claude/context/templates/session_template.md \
   .claude/context/session_current.md
```

## Randfaelle

### Session-Datei fehlt
- Hook zeigt "KEINE SESSION-DATEI" an
- Erstelle neue Session aus Template wenn noetig

### Session ist veraltet
- Pruefe Timestamp und Status
- Archiviere alte Session wenn nicht mehr relevant
- Erstelle neue Session fuer aktuelle Aufgabe

## Learnings

- Context-Sessions sind besonders wichtig bei Subagent-Delegation
- Immer Learnings dokumentieren (Self-Annealing-Prinzip)
- Sessions regelmaessig archivieren um Uebersicht zu behalten
