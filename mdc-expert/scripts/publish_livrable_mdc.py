#!/usr/bin/env python3
# publish_livrable_mdc.py — RÈGLE D'OR : ne publie un livrable Word QUE s'il passe le contrôle qualité.
# Génère en fichier tampon via md2docx_mdc.js, vérifie (structure + logo + zéro Markdown résiduel + rendu QuickLook),
# et ne copie vers la destination QUE si TOUT passe. Sinon : AUCUN fichier produit + rapport d'échec.
# Usage: python3 publish_livrable_mdc.py SOURCE.md DEST.docx "Titre" "Client" "Réf"
import sys, os, subprocess, zipfile, tempfile, shutil

if len(sys.argv) < 3:
    print("Usage: publish_livrable_mdc.py SOURCE.md DEST.docx [Titre] [Client] [Réf]"); sys.exit(1)
SRC, DEST = sys.argv[1], sys.argv[2]
TITLE  = sys.argv[3] if len(sys.argv) > 3 else "LIVRABLE"
CLIENT = sys.argv[4] if len(sys.argv) > 4 else ""
REF    = sys.argv[5] if len(sys.argv) > 5 else ""
HERE = os.path.dirname(os.path.abspath(__file__))
GEN  = os.path.join(HERE, "md2docx_mdc.js")
NODE_MODULES = "/Users/bilefilsseverin/.nvm/versions/node/v22.22.2/lib/node_modules"

def fail(msg):
    print(f"❌ PUBLISH_FAIL [{os.path.basename(DEST)}] : {msg}")
    print("   → règle d'or : aucun document produit.")
    sys.exit(3)

tmpdir = tempfile.mkdtemp(prefix="mdc_pub_")
tmp = os.path.join(tmpdir, "out.docx")
try:
    # 1) GÉNÉRATION
    env = dict(os.environ, NODE_PATH=NODE_MODULES)
    r = subprocess.run(["node", GEN, SRC, tmp, TITLE, CLIENT, REF], capture_output=True, text=True, env=env)
    if r.returncode != 0 or not os.path.exists(tmp):
        fail(f"génération docx-js échouée : {(r.stderr or r.stdout).strip()[:200]}")

    checks = []
    # 2) STRUCTURE (python-docx)
    try:
        from docx import Document
        d = Document(tmp)
    except Exception as e:
        fail(f"document illisible : {e}")
    paras = d.paragraphs
    para_txt = "\n".join(p.text for p in paras)
    cell_txt = "\n".join(c.text for t in d.tables for row in t.rows for c in row.cells)
    alltxt = para_txt + "\n" + cell_txt
    checks.append(("Paragraphes présents", len(paras) > 3))
    # 3) ZÉRO Markdown résiduel (** gras, * italique, ## titres, []() liens) dans le rendu
    leaks = [s for s in ("**", "*", "##", "](", "<br") if s in alltxt]
    checks.append(("Aucun symbole Markdown résiduel", len(leaks) == 0))
    # 4) Tables présentes si la source en contient
    src_has_table = any(l.lstrip().startswith("|") for l in open(SRC, encoding="utf-8"))
    checks.append(("Tableaux rendus (si attendus)", (not src_has_table) or len(d.tables) >= 1))
    # 5) LOGO embarqué
    z = zipfile.ZipFile(tmp)
    media = [n for n in z.namelist() if n.startswith("word/media/") and z.getinfo(n).file_size > 1000]
    checks.append(("Logo/en-tête embarqué", len(media) >= 1))
    # 6) RENDU visuel QuickLook (le doc s'ouvre et se rend)
    png = os.path.join(tmpdir, "out.docx.png")
    subprocess.run(["qlmanage", "-t", "-s", "1000", "-o", tmpdir, tmp],
                   capture_output=True, text=True)
    rendered = os.path.exists(png) and os.path.getsize(png) > 5000
    checks.append(("Rendu QuickLook OK", rendered))

    print(f"— Contrôle qualité [{os.path.basename(DEST)}] —")
    for name, ok in checks:
        print(f"   {'✅' if ok else '❌'} {name}")
    failed = [n for n, ok in checks if not ok]
    if failed:
        if leaks: print(f"   (Markdown résiduel détecté : {leaks})")
        fail("échec(s) : " + " ; ".join(failed))

    # 7) TOUT PASSE → publication (fermer l'éventuelle version ouverte au préalable est à la charge de l'appelant)
    os.makedirs(os.path.dirname(os.path.abspath(DEST)), exist_ok=True)
    shutil.move(tmp, DEST)
    print(f"✅ PUBLISH_OK → {DEST}")
finally:
    shutil.rmtree(tmpdir, ignore_errors=True)
