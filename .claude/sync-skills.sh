#!/bin/bash
# SessionStart hook: sync skills from agentic-skills/ into .claude/commands/
# This ensures any skill added to the agentic-skills folder is available
# as a slash command (/skill-name) in Claude Code.

REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null)"

if [ -z "$REPO_ROOT" ]; then
  echo "sync-skills: could not determine repo root, skipping." >&2
  exit 0
fi

SRC="$REPO_ROOT/agentic-skills"
DEST="$REPO_ROOT/.claude/commands"

mkdir -p "$DEST"

for skill in "$SRC"/*.md; do
  [ -f "$skill" ] || continue
  name="$(basename "$skill")"
  if ! cmp -s "$skill" "$DEST/$name"; then
    cp "$skill" "$DEST/$name"
    echo "sync-skills: loaded $name"
  fi
done
