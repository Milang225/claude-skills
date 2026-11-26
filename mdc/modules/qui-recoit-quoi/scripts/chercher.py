#!/usr/bin/env python3
"""Cherche un terme dans les documents d'une arborescence (md, txt, pdf, docx, xlsx).

Sert à mesurer la portée d'un changement : le nom d'une personne qui part, un régime
qui change, une référence qui bouge. Dit dans quel document le terme apparaît et dans
quel contexte, pour qu'on puisse juger si c'est une mention anodine ou un engagement.
"""
import sys, os, re, zipfile

SKIP_DIRS = {".git", "node_modules", "Library", ".Trash", "__pycache__", "venv", ".venv"}

def txt_md(p):
    return open(p, encoding="utf-8", errors="ignore").read()

def txt_pdf(p):
    from pypdf import PdfReader
    return "\n".join(pg.extract_text() or "" for pg in PdfReader(p).pages)

def txt_zip(p):
    """docx / xlsx / pptx : on lit le XML interne et on retire les balises."""
    out = []
    with zipfile.ZipFile(p) as z:
        for n in z.namelist():
            if n.endswith(".xml") and any(k in n for k in ("document", "sharedStrings", "sheet", "slide")):
                out.append(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8", "ignore")))
    return "\n".join(out)

READERS = {".md": txt_md, ".txt": txt_md, ".pdf": txt_pdf,
           ".docx": txt_zip, ".xlsx": txt_zip, ".pptx": txt_zip}

def main(term, root, ctx=110):
    rx = re.compile(re.escape(term), re.I)
    hits = 0
    for dirpath, dirnames, filenames in os.walk(os.path.expanduser(root)):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.startswith(("~$", ".")):
                continue
            ext = os.path.splitext(fn)[1].lower()
            reader = READERS.get(ext)
            if not reader:
                continue
            p = os.path.join(dirpath, fn)
            try:
                text = reader(p)
            except Exception:
                continue
            found = list(rx.finditer(text))
            if not found:
                continue
            hits += 1
            print(f"\n### {p}   ({len(found)} occurrence(s))")
            for m in found[:4]:
                a, b = max(0, m.start() - ctx), min(len(text), m.end() + ctx)
                print("   … " + " ".join(text[a:b].split()) + " …")
            if len(found) > 4:
                print(f"   … et {len(found) - 4} autre(s)")
    print(f"\n{'='*60}\n{hits} document(s) contiennent « {term} ».")
    if hits:
        print("Pour chacun : ce document est-il déjà sorti de l'agence, et que PROMET-il\n"
              "à propos de ce terme ? Une mention anodine se corrige ; un engagement se notifie.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage : chercher.py "TERME" [dossier]')
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "~/Desktop")
