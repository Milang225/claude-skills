#!/usr/bin/env python3
"""Inventorie les documents d'un dossier MDC : un document = une ligne, tous formats regroupés."""
import sys, os, re, datetime
from collections import defaultdict

EXT = {".md", ".pdf", ".docx", ".xlsx", ".doc", ".xls", ".pptx", ".txt"}
REF = re.compile(r"\bMC-[A-Z]{2,6}(?:-[A-Z]{2,6})?-\d{4}-\d{3}\b")

def refs_in(path):
    """Cherche une référence MDC dans le nom, puis dans le contenu si c'est du texte."""
    m = REF.search(os.path.basename(path))
    if m:
        return m.group(0)
    # Un document déclare sa référence sur une ligne « Référence : … », ou tout en tête.
    # Chercher plus loin confondrait sa référence avec celle d'un document qu'il cite —
    # un fichier de mails cite les références de ses pièces jointes sans être aucune d'elles.
    if path.endswith((".md", ".txt")):
        try:
            head = open(path, encoding="utf-8", errors="ignore").read(3000)
        except OSError:
            return ""
        for line in head.splitlines():
            if re.search(r"r[ée]f[ée]rence", line, re.I):
                m = REF.search(line)
                if m:
                    return m.group(0)
        m = REF.search(head[:200])
        if m:
            return m.group(0)
    return ""

def main(root):
    if not os.path.isdir(root):
        sys.exit(f"Dossier introuvable : {root}")
    docs = defaultdict(lambda: {"formats": [], "mtime": 0, "ref": "", "dir": ""})
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "_pages"))]
        for fn in filenames:
            if fn.startswith(("~$", ".")):
                continue
            stem, ext = os.path.splitext(fn)
            if ext.lower() not in EXT:
                continue
            p = os.path.join(dirpath, fn)
            d = docs[(os.path.relpath(dirpath, root), stem)]
            d["formats"].append(ext.lstrip(".").lower())
            d["mtime"] = max(d["mtime"], os.path.getmtime(p))
            d["dir"] = os.path.relpath(dirpath, root)
            d["ref"] = d["ref"] or refs_in(p)

    if not docs:
        print("Aucun document trouvé."); return
    rows = sorted(docs.items(), key=lambda kv: -kv[1]["mtime"])
    print(f"{len(rows)} document(s) — {sum(len(v['formats']) for _, v in rows)} fichier(s)\n")
    w = min(58, max(len(k[1]) for k in docs))
    print(f"{'DOCUMENT':<{w}}  {'RÉFÉRENCE':<18} {'FORMATS':<20} {'MODIFIÉ':<10} EMPLACEMENT")
    print("-" * (w + 70))
    for (rel, stem), v in rows:
        date = datetime.date.fromtimestamp(v["mtime"]).isoformat()
        fmts = ",".join(sorted(set(v["formats"])))
        loc = "." if rel == "." else rel
        print(f"{stem[:w]:<{w}}  {v['ref'] or '—':<18} {fmts:<20} {date:<10} {loc}")
    sans = [s for (_, s), v in rows if not v["ref"]]
    if sans:
        print(f"\n⚠ {len(sans)} document(s) sans référence MDC — brouillons, sources, ou à référencer.")

if __name__ == "__main__":
    main(os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "."))
