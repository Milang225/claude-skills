#!/bin/zsh
# Synchronise la bibliothèque MDC vers les deux dossiers FORMATION LMDC.
# À exécuter APRÈS chaque publication de livrable.
set -e
SRC="$HOME/Documents/ARCHIVES DOCUMENTS/FORMATIONS MDC"
DOCS="$HOME/Documents/FORMATION LMDC"
DESK="$HOME/Desktop/FORMATION LMDC"
STAGE="$(mktemp -d)/FORMATION LMDC"

# 1. Construire l'arborescence cible dans une zone de travail
python3 - "$SRC" "$STAGE" <<'PY'
import os, shutil, sys, collections
SRC, DST = sys.argv[1], sys.argv[2]
MAP = {".pdf":"PDF", ".docx":"WORD", ".md":"MD",
       ".xlsx":"OUTILS", ".xlsm":"OUTILS", ".pptx":"OUTILS",
       ".png":"VISUELS", ".jpg":"VISUELS", ".jpeg":"VISUELS", ".svg":"VISUELS"}
SKIP = {"__MACOSX", "COURS_PARLES", "_VERSIONS_ANTERIEURES"}
c = collections.Counter()
for root, dirs, files in os.walk(SRC):
    dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".") and not d.endswith(".zip_1")]
    rel = os.path.relpath(root, SRC); rel = "" if rel == "." else rel
    if rel.startswith("00_TEXTES_OFFICIELS_DGI"):
        out = os.path.join(DST, "00_TEXTES_OFFICIELS"); os.makedirs(out, exist_ok=True)
        for f in files:
            if not f.startswith("."):
                shutil.copy2(os.path.join(root, f), os.path.join(out, f)); c["TEXTES"] += 1
        continue
    for f in files:
        if f.startswith("."): continue
        ext = os.path.splitext(f)[1].lower()
        if ext not in MAP: continue
        o = os.path.join(DST, MAP[ext], rel); os.makedirs(o, exist_ok=True)
        shutil.copy2(os.path.join(root, f), os.path.join(o, f)); c[MAP[ext]] += 1
# Modules récents : dupliqués à la racine et dans chaque format
import re, glob
NOUV = os.path.join(DST, "00_NOUVEAUTES_2026"); os.makedirs(NOUV, exist_ok=True)
PAT = re.compile(r'^(13_|31[A-C]_|32[A-C]_|43[B-C]_|44[B-C]_|50[C-J]_|52[B-D]_)')
n = 0
for sub in ("PDF", "WORD", "MD"):
    d = os.path.join(DST, sub, "00_NOUVEAUTES_2026"); os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(DST, sub, "**", "*"), recursive=True):
        b = os.path.basename(f)
        if os.path.isfile(f) and PAT.match(b) and "00_NOUVEAUTES" not in f:
            shutil.copy2(f, os.path.join(d, b))
            if sub == "PDF": shutil.copy2(f, os.path.join(NOUV, b)); n += 1
print("construit :", dict(c), "· total", sum(c.values()), "· modules récents :", n)
PY

# 2. Récupérer le lisez-moi existant s'il y en a un
[ -f "$DOCS/00_LISEZ_MOI.md" ] && cp "$DOCS/00_LISEZ_MOI.md" "$STAGE/" || true

# 3. Miroir vers les deux destinations
for T in "$DOCS" "$DESK"; do
  mkdir -p "$T"
  rsync -a --delete --exclude '.DS_Store' --exclude '._*' "$STAGE/" "$T/"
  echo "$(basename "$(dirname "$T")")/$(basename "$T") : $(find "$T" -type f ! -name '.DS_Store' | wc -l | tr -d ' ') fichiers · $(du -sh "$T" | cut -f1)"
done
rm -rf "$(dirname "$STAGE")"
