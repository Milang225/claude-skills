#!/usr/bin/env python3
# publish_pdf_mdc_public.py — variante PUBLIQUE de publish_pdf_mdc.py, pour les documents
# commerciaux/marketing destinés à être diffusés à des prospects (catalogues, plaquettes) :
# même règle d'or (contrôle qualité bloquant), mais génère via build_mdc_pdf_public.py
# (sans filigrane CONFIDENTIEL ni mention « Document confidentiel »).
# Usage: python3 publish_pdf_mdc_public.py SOURCE.md DEST.pdf "Titre" "Client" "Réf"
import sys, os, subprocess, tempfile, shutil

if len(sys.argv) < 3:
    print("Usage: publish_pdf_mdc.py SOURCE.md DEST.pdf [Titre] [Client] [Réf]"); sys.exit(1)
SRC, DEST = sys.argv[1], sys.argv[2]
TITLE  = sys.argv[3] if len(sys.argv) > 3 else "LIVRABLE"
CLIENT = sys.argv[4] if len(sys.argv) > 4 else ""
REF    = sys.argv[5] if len(sys.argv) > 5 else ""
HERE = os.path.dirname(os.path.abspath(__file__))
GEN  = os.path.join(HERE, "build_mdc_pdf_public.py")

# --- Garde-fou glyphes : les polices de base du PDF (Times/Helvetica/Courier) sont en
# --- Latin-1. Tout caractere hors de cette couverture sort en carre noir dans le PDF.
TOFU = {"\u1d49":"e (ordinal 1er)", "\u02b3":"r (ordinal 1er)", "\u26a0":"symbole attention",
        "\u2705":"emoji coche", "\u274c":"emoji croix", "\u2b50":"emoji etoile",
        "\u2610":"case a cocher", "\ufe0f":"selecteur de variante"}
def _scan_tofu(path):
    try: t = open(path, encoding="utf8").read()
    except Exception: return []
    out = []
    for ch, lab in TOFU.items():
        n = t.count(ch)
        if n: out.append(f"{n}x U+{ord(ch):04X} ({lab})")
    return out
_bad = _scan_tofu(SRC)
if _bad:
    print(f"\u274c PUBLISH_FAIL [{os.path.basename(DEST)}] : glyphes non rendus par la police")
    for b in _bad: print("   -", b)
    print("   \u2192 regle d'or : aucun document produit.")
    sys.exit(4)


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
    leaks = [s for s in ("**", "##", "](", "<br", "`") if s in txt]
    checks.append(("Aucun symbole Markdown résiduel", len(leaks) == 0))
    # RÈGLE DU GÉRANT (13/11/2026) : jamais « gratuit » dans un document MDC
    import re as _re
    _grat = sorted(set(_re.findall(r"(?i)\bgratuit\w*", txt)))
    checks.append(("Aucune mention « gratuit »", len(_grat) == 0))
    if _grat: print(f"   (mention interdite : {_grat})")
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
