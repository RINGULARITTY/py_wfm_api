#!/usr/bin/env bash
# Installe les git hooks depuis .hooks/ vers .git/hooks/
# Usage : bash scripts/install_hooks.sh

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_SRC="$REPO_ROOT/.hooks"
HOOKS_DST="$REPO_ROOT/.git/hooks"

if [ ! -d "$HOOKS_SRC" ]; then
    echo "Dossier .hooks/ introuvable." >&2
    exit 1
fi

for hook in "$HOOKS_SRC"/*; do
    name="$(basename "$hook")"
    dst="$HOOKS_DST/$name"
    cp "$hook" "$dst"
    chmod +x "$dst"
    echo "✓  Hook installé : $name"
done

echo ""
echo "Hooks installés avec succès."
echo "Le hook pre-push lancera la testsuite avant chaque 'git push'."
