---
description: Pushe alle Änderungen nach GitHub
allowed-tools: Bash(git:*)
---

## Context

- Git Status: !`git status --short`
- Branch: !`git branch --show-current`
- Diff Stats: !`git diff --stat`

## Anweisungen

1. Stage alle Änderungen mit `git add -A`
2. Analysiere die Änderungen und erstelle eine passende Commit-Message
3. Committe mit Format: `<type>: <beschreibung>` (feat/fix/docs/refactor)
4. Pushe zum Remote mit `git push`
5. Zeige Bestätigung

Führe direkt aus ohne Rückfragen. Bei Konflikten: stoppe und informiere.
