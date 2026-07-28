#!/usr/bin/env python3
# publish_pdf_mdc.py — RÈGLE D'OR (PDF) : ne publie un PDF QUE s'il passe le contrôle qualité.
# Génère en tampon via build_mdc_pdf.py, vérifie (pages, logo, zéro Markdown résiduel, rendu),
# et ne copie vers la destination QUE si tout passe. Sinon : AUCUN fichier + rapport d'échec.
# Usage: python3 publish_pdf_mdc.py SOURCE.md DEST.pdf "Titre" "Client" "Réf"
import sys, os, subprocess, tempfile, shutil

if len(sys.argv) < 3:
    print("Usage: publish_pdf_mdc.py SOURCE.md DEST.pdf [Titre] [Client] [Réf]"); sys.exit(1)
SRC, DEST = sys.argv[1], sys.argv[2]
TITLE  = sys.argv[3] if len(sys.argv) > 3 else "LIVRABLE"
CLIENT = sys.argv[4] if len(sys.argv) > 4 else ""
REF    = sys.argv[5] if len(sys.argv) > 5 else ""
HERE = os.path.dirname(os.path.abspath(__file__))
GEN  = os.path.join(HERE, "build_mdc_pdf.py")

def fail(msg):
    print(f"❌ PUBLISH_FAIL [{os.path.basename(DEST)}] : {msg}")
    print("   → règle d'or : aucun document produit.")
    sys.exit(3)

tmpdir = tempfile.mkdtemp(prefix="mdc_pdf_")
tmp = os.path.join(tmpdir, "out.pdf")
try:
    r = subprocess.run([sys.executable, GEN, SRC, tmp, TITLE, CLIENT, REF], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(tmp):
        fail(f"génération PDF échouée : {(r.stderr or r.stdout).strip()[:200]}")

    checks = []
    try:
        import fitz
        doc = fitz.open(tmp)
    except Exception as e:
        fail(f"PDF illisible : {e}")
    checks.append(("Pages présentes", doc.page_count >= 1))
    txt = "".join(p.get_text() for p in doc)
    leaks = [s for s in ("**", "##", "](", "<br") if s in txt]
    checks.append(("Aucun symbole Markdown résiduel", len(leaks) == 0))
    checks.append(("Logo/image en page 1", len(doc[0].get_images()) >= 1))
    # rendu non blanc
    pix = doc[0].get_pixmap(dpi=90); png = os.path.join(tmpdir, "p1.png"); pix.save(png)
    checks.append(("Rendu page 1 OK", os.path.getsize(png) > 5000))

    print(f"— Contrôle qualité PDF [{os.path.basename(DEST)}] —")
    for name, ok in checks:
        print(f"   {'✅' if ok else '❌'} {name}")
    failed = [n for n, ok in checks if not ok]
    if failed:
        if leaks: print(f"   (Markdown résiduel : {leaks})")
        fail("échec(s) : " + " ; ".join(failed))

    os.makedirs(os.path.dirname(os.path.abspath(DEST)), exist_ok=True)
    shutil.move(tmp, DEST)
    print(f"✅ PUBLISH_OK → {DEST}")
finally:
    shutil.rmtree(tmpdir, ignore_errors=True)
