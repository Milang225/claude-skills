#!/usr/bin/env python3
# publish_livrable_mdc.py — RÈGLE D'OR : ne publie un livrable Word QUE s'il passe le contrôle qualité.
# Génère en fichier tampon via md2docx_mdc.js, vérifie (structure + logo + zéro Markdown résiduel + rendu QuickLook),
# et ne copie vers la destination QUE si TOUT passe. Sinon : AUCUN fichier produit + rapport d'échec.
# Usage: python3 publish_livrable_mdc.py SOURCE.md DEST.docx "Titre" "Client" "Réf"
import sys, os, subprocess, zipfile, tempfile, shutil

if len(sys.argv) < 3:
    print("Usage: publish_livrable_mdc.py SOURCE.md DEST.docx [Titre] [Client] [Réf]"); sys.exit(1)
SRC, DEST = sys.argv[1], sys.argv[2]

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
    leaks = [s for s in ("**", "*", "##", "](", "<br", "`") if s in alltxt]
    checks.append(("Aucun symbole Markdown résiduel", len(leaks) == 0))
    # 3 bis) CHARTE 2026 : zéro jargon technique et zéro ancien vocabulaire dans le rendu
    import re as _re
    _tech = sorted(set(_re.findall(r"\b[\w-]+\.(?:md|py|json|js|txt)\b|python3|/Users/|~/", alltxt)))
    checks.append(("Aucun jargon technique (noms de fichiers, commandes, chemins)", len(_tech) == 0))
    _old = [w for w in ("Agence de Notation", "AGENCE DE NOTATION", "ertifié conforme", "Réviseur de", "Visé et certifié", "Visa d'auditeur", "VISA D'AUDITEUR") if w in alltxt]
    checks.append(("Vocabulaire charte 2026 (ni notation, ni visa, ni certification)", len(_old) == 0))
    if _tech: print(f"   (jargon technique : {_tech[:8]})")
    if _old: print(f"   (ancien vocabulaire : {_old})")
    # 3 ter) RÈGLE DU GÉRANT (13/11/2026) : jamais « gratuit » dans un document MDC
    _grat = sorted(set(_re.findall(r"(?i)\bgratuit\w*", alltxt)))
    checks.append(("Aucune mention « gratuit »", len(_grat) == 0))
    if _grat: print(f"   (mention interdite : {_grat})")
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
