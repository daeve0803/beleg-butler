#!/usr/bin/env python3
"""
SessionStart Hook: Erinnert an Context-Session-Management.

Dieser Hook wird bei jedem Session-Start ausgeloest und:
1. Liest die aktuelle Session-Datei
2. Zeigt den aktuellen Status an
3. Erinnert an das Aktualisieren der Session bei komplexen Aufgaben
"""

import json
import sys
from pathlib import Path

# Projekt-Root ermitteln
PROJECT_DIR = Path(__file__).parent.parent.parent
SESSION_FILE = PROJECT_DIR / ".claude" / "context" / "session_current.md"
TEMPLATE_FILE = PROJECT_DIR / ".claude" / "context" / "templates" / "session_template.md"


def get_session_status() -> str:
    """Liest den aktuellen Session-Status."""
    if not SESSION_FILE.exists():
        return "KEINE SESSION-DATEI"

    content = SESSION_FILE.read_text()

    # Status extrahieren
    for line in content.split("\n"):
        if line.startswith("## Status"):
            # Naechste nicht-leere Zeile ist der Status
            idx = content.split("\n").index(line)
            next_lines = content.split("\n")[idx+1:]
            for next_line in next_lines:
                if next_line.strip():
                    return next_line.strip()

    return "UNBEKANNT"


def main():
    # Hook Input lesen (optional)
    try:
        input_data = json.load(sys.stdin)
        source = input_data.get("source", "unknown")
    except:
        source = "unknown"

    session_status = get_session_status()

    # Context-Reminder erstellen
    reminder = f"""
## Context-Session Reminder

**Aktueller Session-Status:** {session_status}
**Session-Datei:** `.claude/context/session_current.md`

### Bei komplexen Aufgaben (> 2 Schritte):

1. **Session-Datei aktualisieren** mit:
   - Auftrag (Was soll erreicht werden?)
   - Status: IN_PROGRESS
   - Geplante Tasks

2. **An Subagents delegieren** (sie lesen die Session-Datei):
   - `reviewer` - Nach Code-Aenderungen in tools/
   - `documenter` - Nach Script-Aenderungen
   - `linkedin` - Fuer LinkedIn-Content

3. **Nach Abschluss:**
   - Session-Status auf COMPLETED setzen
   - Learnings dokumentieren (Self-Annealing)

### Template verwenden:
Kopiere `.claude/context/templates/session_template.md` nach `session_current.md`
"""

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": reminder
        }
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()