#!/bin/bash
# Installation de la façon de travailler MDC sur un Mac (ou Linux)
# Usage : bash ~/.claude/skills/_harness/install.sh [BASE]
#   BASE : dossier où vous ouvrirez vos projets (défaut : votre dossier personnel).
#          Les mémoires de chaque projet sont installées pour BASE/<NOM DU PROJET>.
set -e
BASE="${1:-$HOME}"
H="$(cd "$(dirname "$0")" && pwd)"
DEPOT="$(dirname "$H")"
C="$HOME/.claude"; mkdir -p "$C"

# 1. Skills
if [ ! -e "$C/skills" ]; then ln -s "$DEPOT" "$C/skills"; echo "Skills : lien $C/skills -> $DEPOT"
elif [ "$(cd "$C/skills" && pwd -P)" = "$(cd "$DEPOT" && pwd -P)" ]; then echo "Skills : déjà en place"
else echo "Skills : $C/skills existe déjà (laissé tel quel). Renommez-le puis relancez."; fi

# 2. Agents et tâches planifiées
for d in agents scheduled-tasks; do mkdir -p "$C/$d"; cp -R "$H/$d/." "$C/$d/"; echo "$d : copiés"; done

# 3. Mémoires
for m in "$H"/memory/*/; do
  n="$(basename "$m")"; cle="$(printf '%s' "$BASE/$n" | sed 's/[^A-Za-z0-9]/-/g')"
  mkdir -p "$C/projects/$cle/memory"; cp "$m"* "$C/projects/$cle/memory/"; echo "Mémoire $n -> projet $BASE/$n"
done
echo; echo "Terminé. Plateforme MDC : voir _harness/README.md (étape manuelle)."
