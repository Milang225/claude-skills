#!/usr/bin/env python3
"""Reconstruit etat/ETAT_COURANT.md : clients, documents récents, suivi, mémoire.
Lancer : python3 ~/.claude/skills/mdc/etat/rafraichir.py"""
import os, time, glob, datetime
H = os.path.expanduser("~")
DOC = f"{H}/Documents"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ETAT_COURANT.md")
SKIP = {".DS_Store"}
def recents(root, n=40, depth=4):
    items = []
    for dp, dn, fn in os.walk(root):
        if dp[len(root):].count(os.sep) >= depth: dn[:] = []
        dn[:] = [d for d in dn if not d.startswith((".", "_OBSOLETE"))]
        for f in fn:
            if f in SKIP or f.startswith(("~$", ".")): continue
            p = os.path.join(dp, f)
            try: items.append((os.path.getmtime(p), p))
            except OSError: pass
    return sorted(items, reverse=True)[:n]
def d(t): return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d")
L = [f"# État courant MDC — généré le {datetime.date.today()}", ""]
cl = f"{DOC}/DOSSIER CLIENTS"
L += ["## Clients (dossiers dans DOSSIER CLIENTS)", ""]
if os.path.isdir(cl):
    for c in sorted(os.listdir(cl)):
        p = os.path.join(cl, c)
        if os.path.isdir(p) and not c.startswith("."):
            r = recents(p, 1, 6)
            L.append(f"- {c.strip()} — dernier fichier : {d(r[0][0]) if r else 'vide'}")
for title, root in [("Documents récents SUPERVISEUR GENERAL", f"{DOC}/SUPERVISEUR GENERAL"),
                    ("Documents récents DOSSIER CLIENTS", cl)]:
    L += ["", f"## {title}", ""]
    for t, p in recents(root): L.append(f"- {d(t)} · {p.replace(H, '~')}")
L += ["", "## Fichiers de suivi à lire", ""]
for g in ["SUIVI CLIENTS/SUIVI_DES_DOSSIERS_MDC.xlsx", "SUPERVISEUR GENERAL/00_REGISTRE_DES_DOCUMENTS_VALIDES.xlsx",
          "SUPERVISEUR GENERAL/00_JOURNAL_DE_PRODUCTION.xlsx", "SUIVI CLIENTS/VUE_360_DES_DOSSIERS_MDC.pdf"]:
    p = f"{DOC}/{g}"
    L.append(f"- ~/Documents/{g} — {'modifié le ' + d(os.path.getmtime(p)) if os.path.exists(p) else 'ABSENT'}")
mem = glob.glob(f"{H}/.claude/projects/*SUPERVISEUR-GENERAL/memory/MEMORY.md")
if mem:
    L += ["", "## Mémoire du Superviseur (index)", "", open(mem[0], encoding="utf-8").read()]
open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(OUT, len(L), "lignes")
