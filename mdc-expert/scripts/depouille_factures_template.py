#!/usr/bin/env python3
"""Construit DEPOUILLEMENT_FACTURES_BNA.xlsx — 4 onglets MDC."""
import os, re, glob, json
from collections import defaultdict, Counter
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OCR_DIR = "/tmp/bna_ocr/txt"
OUT_DIR = "/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/EXERCICE_2025"
os.makedirs(OUT_DIR, exist_ok=True)
OUT = f"{OUT_DIR}/DEPOUILLEMENT_FACTURES_BNA.xlsx"

# === Référentiel catégories SYSCOHADA (grandes masses) ===
CATS = [
    ("MATERIAUX_BTP",   "60110000", "Achats matériaux BTP (béton, fer, ciment, agrégats)",
     [r"\bb[ée]ton\b", r"\bbpe\b", r"\bciment\b", r"\bfer\s*[àa]?\s*b[ée]ton\b",
      r"technic\s*b[ée]ton", r"\bsecifab\b", r"\bagb\b", r"\bsotaci\b",
      r"agr[ée]gat", r"\bgravier", r"\bsable\b", r"\bparpaing", r"\btole\b",
      r"f500", r"hls?\s*lg\d+", r"d\d+\s*hle", r"fer\s*[àa]?\s*b[ée]ton"]),
    ("SOUS_TRAITANCE_COFFRAGE", "60580000", "Sous-traitance / Matériel coffrage et étaiement",
     [r"sous[\s-]?trait", r"coffrage", r"panneau\s*hsa", r"clip\s*de\s*cale",
      r"[ée]tai\s*m[ée]tal", r"cadre\s*acier", r"peri\s*ref",
      r"distribution\s*de\s*marchandises", r"\bdmd\b"]),
    ("CARBURANT", "62810000", "Carburant véhicules (TotalEnergies, Shell, Petroci, Oryx)",
     [r"\btotal\s*[ec]nergies", r"\btotal\s*c[ôo]te", r"\btotal\b\s*$",
      r"\bshell\b", r"\bpetroci\b", r"\boryx\b", r"vivo\s*[ée]nergies",
      r"\bcorlay\b", r"\bgazole\b", r"sans\s*plomb", r"agence\s*ang(?:r[ée])?",
      r"zmpx\d+", r"\bpompe\b"]),
    ("TELECOM_INTERNET", "62820000", "Télécoms (Orange, MTN, Moov) — fixe, mobile, internet",
     [r"\borange\b", r"\bmtn\b", r"\bmoov\b", r"\binternet\b",
      r"\badsl\b", r"\bfibre\b", r"ofibre", r"facture\s*internet"]),
    ("PEAGE_TRANSPORTS", "62480000", "Péage/Pont, BIP PASS, transports divers",
     [r"\bsocoprim\b", r"\bbip\s*pass\b", r"\bp[ée]age\b",
      r"pont\s*d.?abidjan", r"hkb"]),
    ("LOCATION_MATERIEL", "62240000", "Location matériel/engins BTP",
     [r"location\s+(de\s+)?(mat[ée]riel|engin|grue|b[ée]tonni|vibreur|pelle|camion)",
      r"loyer\s+(mat[ée]riel|engin)"]),
    ("LOCATIONS_LOCAUX", "62220000", "Loyers bureaux/locaux",
     [r"\bloyer\s+(local|bureau|immeuble)", r"location\s+(local|bureau)"]),
    ("EAU_ELECTRICITE", "60510000", "Eau / Électricité (CIE, SODECI)",
     [r"\bcie\b\s+", r"\bsodeci\b", r"compagnie\s*ivoirienne",
      r"facture\s*d.?eau", r"\bkwh\b", r"\bm3\b"]),
    ("HONORAIRES_CONSEIL", "63210000", "Honoraires (PwC, audit, conseil, avocat, notaire)",
     [r"\bpwc\b", r"pricewaterhouse", r"\bdeloitte\b", r"\bkpmg\b",
      r"\bey\b", r"ernst\s*young", r"\bmazars\b",
      r"honoraires?", r"avocat", r"\bnotaire\b", r"\baudit\b",
      r"expert[\s-]?comptable"]),
    ("IMPRIMERIE_PUB", "62700000", "Impression, publicité, supports communication",
     [r"\bimprim", r"\bnetfox\b", r"flyers?", r"affich", r"kakemono",
      r"\benseigne\b", r"tampon", r"brochure", r"carte\s*de\s*visite"]),
    ("FOURNITURES_BUREAU", "60550000", "Fournitures bureau, papeterie, livres",
     [r"\bm[ée]mento\b", r"code\s*g[ée]n[ée]ral\s*d.?imp[ôo]ts",
      r"\bouvrag", r"\bpapier\b\s*[Aa]4", r"toner", r"cartouche"]),
    ("ASSURANCES", "62500000", "Primes d'assurances",
     [r"\bassurance", r"\bnsia\s*assurance", r"\bsunu\b",
      r"\ballianz\b", r"\bsaham\b"]),
    ("FRAIS_BANCAIRES", "63110000", "Frais bancaires",
     [r"frais\s*bancaire", r"commission\s*bancaire", r"agios?",
      r"tenue\s*de\s*compte"]),
    ("MISSIONS_DEPLACEMENT", "62560000", "Missions, hôtel, restaurant, déplacements",
     [r"\bh[ôo]tel\b", r"\brestaurant\b", r"billet\s*d.?avion",
      r"\bs[ée]minaire\b", r"\br[ée]ception"]),
    ("IMPOTS_TAXES", "64180000", "Impôts, taxes, patente, vignettes",
     [r"\bpatente\b", r"vignette", r"taxe\s*foncière",
      r"droits?\s*de\s*timbre"]),
    ("ENTRETIEN_REPARATIONS", "62320000", "Entretien et réparations",
     [r"r[ée]paration", r"\bentretien\b", r"vidange", r"\bpneu\b",
      r"plaquette", r"garage", r"m[ée]canique"]),
]

DEFAULT = ("AUTRES_CHARGES", "65880000", "Autres charges diverses", [])

# === Patterns ===
PAT_YEAR = re.compile(r"\b(20[12]\d)\b")
PAT_DATE = re.compile(r"(\d{1,2})[/\-\.\s](\d{1,2}|janvier|f[ée]vrier|mars|avril|mai|juin|juillet|ao[ûu]t|septembre|octobre|novembre|d[ée]cembre)[/\-\.\s](20\d{2})", re.I)
MOIS = {"janvier":1,"février":2,"fevrier":2,"mars":3,"avril":4,"mai":5,"juin":6,
        "juillet":7,"août":8,"aout":8,"septembre":9,"octobre":10,"novembre":11,"décembre":12,"decembre":12}

def extract_date(text):
    m = PAT_DATE.search(text)
    if not m:
        y = PAT_YEAR.search(text)
        return (None, None, int(y.group(1))) if y else (None, None, None)
    j = int(m.group(1))
    mo_raw = m.group(2).lower()
    mo = int(mo_raw) if mo_raw.isdigit() else MOIS.get(mo_raw, None)
    y = int(m.group(3))
    return (j, mo, y)

def normalize_montant(s):
    if not s: return None
    s = s.strip()
    # Détection format avec décimales ",XX" ou ".XX"
    has_dec = bool(re.search(r"[,.]\d{2}\s*$", s))
    digits = re.sub(r"\D", "", s)
    if not digits: return None
    try:
        v = int(digits)
        if has_dec: v = v // 100
        return v if 100 <= v <= 999_999_999 else None
    except: return None

def extract_ttc_ht_tva(text):
    """Retourne (ttc, ht, tva) — None si non trouvé."""
    ttc = ht = tva = None
    # Net à payer / Total TTC
    for pat in [r"net\s*[àa]?\s*payer\s*[:.]?\s*(\d[\d\s.,]{2,15})",
                r"montant\s*ttc\s*[:.]?\s*(\d[\d\s.,]{2,15})",
                r"total\s*ttc\s*[:.]?\s*(\d[\d\s.,]{2,15})",
                r"total\s*[àa]\s*payer\s*[:.]?\s*(\d[\d\s.,]{2,15})",
                r"montant\s*net\s*[àa]?\s*payer\s*[:.]?\s*(\d[\d\s.,]{2,15})"]:
        m = re.search(pat, text, re.I)
        if m:
            ttc = normalize_montant(m.group(1)); break
    # HT
    for pat in [r"total\s*ht\s*[:.]?\s*(\d[\d\s.,]{2,15})",
                r"montant\s*ht\s*[:.]?\s*(\d[\d\s.,]{2,15})",
                r"base\s*ht\s*[:.]?\s*(\d[\d\s.,]{2,15})"]:
        m = re.search(pat, text, re.I)
        if m: ht = normalize_montant(m.group(1)); break
    # TVA 18%
    for pat in [r"tva\s*(?:facturée\s*)?\(?18\s*%\)?\s*[:.]?\s*(\d[\d\s.,]{2,12})",
                r"tva\s*[àa]\s*18\s*%\s*[:.]?\s*(\d[\d\s.,]{2,12})",
                r"montant\s*tva\s*[:.]?\s*(\d[\d\s.,]{2,12})"]:
        m = re.search(pat, text, re.I)
        if m: tva = normalize_montant(m.group(1)); break
    return ttc, ht, tva

def categorize(text):
    low = text.lower()
    best = (DEFAULT, 0)
    for cat in CATS:
        code, cmpt, lib, kws = cat
        score = sum(1 for kw in kws if re.search(kw, low, re.I))
        if score > best[1]:
            best = (cat, score)
    return best[0] if best[1] > 0 else DEFAULT

def detect_supplier(text):
    """Détection fournisseur par marqueurs spécifiques."""
    low = text.lower()
    rules = [
        (r"pwc|pricewaterhouse", "PricewaterhouseCoopers Tax & Legal"),
        (r"technic\s*b[ée]ton", "TECHNIC BETON"),
        (r"\bsecifab\b", "SECIFAB"),
        (r"\bsotaci\b", "SOTACI"),
        (r"\bagb\b", "AGB"),
        (r"distribution\s*de\s*marchandises|\bdmd\b", "DMD SARL"),
        (r"\borange\b", "ORANGE CI"),
        (r"\bsocoprim\b|pont\s*d.?abidjan", "SOCOPRIM (Pont HKB)"),
        (r"\btotal\s*[ec]nergies|agence\s*ang", "TOTAL ENERGIES CI"),
        (r"\bshell\b", "SHELL CI"),
        (r"\bpetroci\b", "PETROCI"),
        (r"\boryx\b", "ORYX CI"),
        (r"\bcorlay\b", "CORLAY"),
        (r"\bcie\b\s+", "CIE"),
        (r"\bsodeci\b", "SODECI"),
        (r"\bnetfox\b", "NETFOX"),
        (r"\bnsia\s*assurance", "NSIA ASSURANCE"),
    ]
    for pat, name in rules:
        if re.search(pat, low):
            return name
    # Fallback: première ligne ALL CAPS non générique
    for l in text.split("\n")[:6]:
        l = l.strip()
        if len(l) >= 4 and l.isupper() and not re.search(r"\d{3}", l):
            if any(g in l.upper() for g in ["FACTURE","RECU","REÇU","CLIENT","TVA","TOTAL","DATE","DEVIS","BORDEREAU","BON DE"]):
                continue
            return l[:60]
    return "FOURNISSEUR_INDETERMINE"

def is_continuation_page(text):
    """Détecte page BL/continuation à attacher à doc précédent."""
    low = text.lower()
    has_doc = bool(re.search(r"facture|reçu|recu|devis", low))
    has_bl_only = bool(re.search(r"bordereau\s*de\s*livraison|bon\s*de\s*livraison|^bl\s*\d+", low, re.M))
    return has_bl_only and not has_doc

# === Lecture OCR ===
files = sorted(glob.glob(f"{OCR_DIR}/*.txt"))
pages = []
for f in files:
    with open(f) as fh: txt = fh.read()
    pages.append({"file": os.path.basename(f), "text": txt})

# === Groupement par document (FACTURE + BL associés) ===
docs = []
current = None
for p in pages:
    if not p["text"].strip(): continue
    if is_continuation_page(p["text"]) and current is not None:
        current["pages"].append(p["file"])
        current["text"] += "\n---PAGE SUIV---\n" + p["text"]
    else:
        if current: docs.append(current)
        current = {"pages": [p["file"]], "text": p["text"]}
if current: docs.append(current)

# === Enrichissement ===
for d in docs:
    j, mo, y = extract_date(d["text"])
    ttc, ht, tva = extract_ttc_ht_tva(d["text"])
    cat = categorize(d["text"])
    d.update({
        "fournisseur": detect_supplier(d["text"]),
        "date_jour": j, "date_mois": mo, "annee": y,
        "ttc": ttc, "ht": ht, "tva": tva,
        "cat_code": cat[0], "compte": cat[1], "cat_libelle": cat[2],
        "nb_pages": len(d["pages"]),
        "has_ncc_fournisseur": bool(re.search(r"n[°o]\s*cc\s*[:.]?\s*\d", d["text"], re.I)),
        "regime_tee": bool(re.search(r"r[ée]gime.*?(t\.?e\.?e|entreprenant)", d["text"], re.I)),
        "espece": bool(re.search(r"esp[èe]ces?\b|cash", d["text"], re.I)),
        "premiere_page": d["pages"][0],
        "excerpt": d["text"][:200].replace("\n"," | "),
    })

# Estimation TTC si absent : analyse contextuelle ligne-par-ligne
# Filtre : numéros de facture, NCC, dates, téléphones, codes
PAT_AMOUNT_LINE = re.compile(r"^\s*(?:total|net|montant|sous[\s-]?total|prix|à\s*payer)", re.I)
PAT_NUM = re.compile(r"\b(\d{1,3}(?:[\s.]\d{3}){1,4}(?:[,.]\d{2})?)\b")
def is_suspect_number(s, line):
    """Filtre NCC, téléphones, dates, références facture, BL."""
    low = line.lower()
    if re.search(r"\b(?:ncc|n[°o]\s*cc|t[ée]l|tel|fax|cc\s*[°:]|facture\s*n|bl\s*\d|bon\s*n|ref|code|client|adresse|bp|cedex)", low):
        return True
    if re.search(r"\b20[12]\d\b", s): return True  # année
    digits = re.sub(r"\D", "", s)
    if len(digits) > 9: return True  # numéro long suspect
    return False

for d in docs:
    if d["ttc"] is None:
        candidates = []
        for line in d["text"].split("\n"):
            for m in PAT_NUM.finditer(line):
                raw = m.group(1)
                if is_suspect_number(raw, line): continue
                v = normalize_montant(raw)
                if v and 500 <= v <= 100_000_000:
                    weight = 5 if PAT_AMOUNT_LINE.search(line) else 1
                    candidates.append((v, weight, line.strip()[:60]))
        if candidates:
            # Priorité aux montants sur ligne "total/net/montant" sinon max
            weighted = [c for c in candidates if c[1] >= 5]
            if weighted:
                d["ttc"] = max(c[0] for c in weighted)
            else:
                d["ttc"] = max(c[0] for c in candidates)
            d["ttc_estime"] = True

print(f"\n{len(pages)} pages → {len(docs)} documents groupés")
print(f"Pages BL fusionnées: {sum(d['nb_pages']-1 for d in docs)}")
print(f"\nPAR ANNÉE:")
for y, n in Counter(d["annee"] for d in docs).most_common():
    s = sum(d["ttc"] or 0 for d in docs if d["annee"]==y)
    print(f"  {y}: {n} docs / TTC ≈ {s:,}".replace(",", " "))
print(f"\nPAR CATÉGORIE:")
for code in [c[0] for c in CATS] + [DEFAULT[0]]:
    sub = [d for d in docs if d["cat_code"]==code]
    if not sub: continue
    total = sum(d["ttc"] or 0 for d in sub)
    print(f"  {len(sub):>3}  {code:<26}  TTC ≈ {total:>15,}".replace(",", " "))

# === GÉNÉRATION EXCEL MDC ===
wb = Workbook()
NAVY = "1A1A2E"; OR = "E8C547"; OR_PALE = "F5E5A5"; GRIS = "F4F4F8"
ROUGE_PALE = "F8E8E8"; CREME = "FFFBE8"

def style_header(cell, fill=NAVY, font_color="FFFFFF"):
    cell.font = Font(name="Calibri", size=11, bold=True, color=font_color)
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = Border(left=Side(style="thin"), right=Side(style="thin"),
                          top=Side(style="thin"), bottom=Side(style="thin"))

def style_data(cell, fill=None, bold=False):
    cell.font = Font(name="Calibri", size=10, bold=bold)
    if fill: cell.fill = PatternFill("solid", fgColor=fill)
    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    cell.border = Border(left=Side(style="thin", color="DDDDDD"),
                         right=Side(style="thin", color="DDDDDD"),
                         top=Side(style="thin", color="DDDDDD"),
                         bottom=Side(style="thin", color="DDDDDD"))

def add_mdc_header(ws, title):
    ws.merge_cells("A1:H1")
    c = ws.cell(1, 1, "LA MAISON DE LA CONFORMITÉ SARL")
    c.font = Font(name="Calibri", size=14, bold=True, color=OR)
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28
    ws.merge_cells("A2:H2")
    c = ws.cell(2, 1, title)
    c.font = Font(name="Calibri", size=11, italic=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 20

# ─────── Onglet 1 : RÉCAP PAR CHARGE ───────
ws = wb.active
ws.title = "1-Récap par charge"
ws.sheet_properties.tabColor = NAVY
add_mdc_header(ws, "DÉPOUILLEMENT FACTURES BNA — Récap par catégorie de charge")
headers = ["Code MDC", "Compte SYSCOHADA", "Libellé", "Nb pièces", "Σ TTC (estimé)", "Σ HT identifiés", "Σ TVA identifiée", "Part %"]
for j, h in enumerate(headers, 1):
    style_header(ws.cell(4, j, h))
ws.row_dimensions[4].height = 35

cat_stats = defaultdict(lambda: {"n":0,"ttc":0,"ht":0,"tva":0})
for d in docs:
    s = cat_stats[d["cat_code"]]
    s["n"] += 1
    s["ttc"] += d["ttc"] or 0
    s["ht"] += d["ht"] or 0
    s["tva"] += d["tva"] or 0
total_ttc = sum(s["ttc"] for s in cat_stats.values())
row = 5
all_cats = [(c[0], c[1], c[2]) for c in CATS] + [(DEFAULT[0], DEFAULT[1], DEFAULT[2])]
sorted_cats = sorted(all_cats, key=lambda c: -cat_stats[c[0]]["ttc"])
fmt_fcfa = '#,##0_- "FCFA";[RED]-#,##0_- "FCFA";"-"'
for code, cmpt, lib in sorted_cats:
    s = cat_stats[code]
    if s["n"] == 0: continue
    fill = GRIS if row % 2 == 0 else None
    pct = (s["ttc"]/total_ttc*100) if total_ttc else 0
    vals = [code, cmpt, lib, s["n"], s["ttc"], s["ht"], s["tva"], pct/100]
    for j, v in enumerate(vals, 1):
        c = ws.cell(row, j, v)
        style_data(c, fill)
        if j in (5,6,7): c.number_format = fmt_fcfa
        if j == 8: c.number_format = "0.0%"
        if j in (1,2): c.alignment = Alignment(horizontal="center")
    row += 1
# Total
for j in range(1, 9):
    c = ws.cell(row, j)
    style_data(c, OR_PALE, bold=True)
ws.cell(row, 1, "TOTAL").font = Font(name="Calibri", size=11, bold=True)
ws.cell(row, 4, sum(s["n"] for s in cat_stats.values())).number_format = "#,##0"
ws.cell(row, 5, total_ttc).number_format = fmt_fcfa
ws.cell(row, 6, sum(s["ht"] for s in cat_stats.values())).number_format = fmt_fcfa
ws.cell(row, 7, sum(s["tva"] for s in cat_stats.values())).number_format = fmt_fcfa
ws.cell(row, 8, 1).number_format = "0.0%"
# Widths
widths = [22, 16, 50, 10, 18, 16, 16, 10]
for j, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(j)].width = w
ws.freeze_panes = "A5"

# ─────── Onglet 2 : JOURNAL D'ÉCRITURES SYSCOHADA ───────
ws2 = wb.create_sheet("2-Journal écritures")
ws2.sheet_properties.tabColor = NAVY
add_mdc_header(ws2, "Journal d'écritures SYSCOHADA — Imputation D 6xx / C 4011 Fournisseurs")
hdr2 = ["N° pièce", "Date", "Journal", "Compte D", "Compte C", "Libellé écriture", "Débit (FCFA)", "Crédit (FCFA)", "Fournisseur", "Référence OCR"]
for j, h in enumerate(hdr2, 1):
    style_header(ws2.cell(4, j, h))
ws2.row_dimensions[4].height = 35

# Format date
def fmt_date(j, m, y):
    if y and m and j: return f"{j:02d}/{m:02d}/{y}"
    if y and m: return f"--/{m:02d}/{y}"
    if y: return f"--/--/{y}"
    return "?"

row = 5
seq = 1
total_d = total_c = 0
sorted_docs = sorted(docs, key=lambda d: (d["annee"] or 9999, d["date_mois"] or 99, d["date_jour"] or 99))
for d in sorted_docs:
    if not d["ttc"]: continue
    piece = f"ACH-{seq:04d}"
    dt = fmt_date(d["date_jour"], d["date_mois"], d["annee"])
    fill = GRIS if seq % 2 == 0 else None
    libelle = f"{d['cat_libelle']} — {d['fournisseur']}"[:80]
    # Ligne débit
    vals_d = [piece, dt, "ACH", d["compte"], "", libelle, d["ttc"], "", d["fournisseur"], d["premiere_page"]]
    for j, v in enumerate(vals_d, 1):
        c = ws2.cell(row, j, v); style_data(c, fill)
        if j in (7,8): c.number_format = fmt_fcfa
        if j in (1,2,3,4,5): c.alignment = Alignment(horizontal="center")
    total_d += d["ttc"]
    row += 1
    # Ligne crédit
    vals_c = [piece, dt, "ACH", "", "40110000", libelle, "", d["ttc"], d["fournisseur"], d["premiere_page"]]
    for j, v in enumerate(vals_c, 1):
        c = ws2.cell(row, j, v); style_data(c, fill)
        if j in (7,8): c.number_format = fmt_fcfa
        if j in (1,2,3,4,5): c.alignment = Alignment(horizontal="center")
    total_c += d["ttc"]
    row += 1
    seq += 1

# Total
for j in range(1, 11):
    c = ws2.cell(row, j); style_data(c, OR_PALE, bold=True)
ws2.cell(row, 6, "TOTAL JOURNAL").font = Font(name="Calibri", size=11, bold=True)
ws2.cell(row, 7, total_d).number_format = fmt_fcfa
ws2.cell(row, 8, total_c).number_format = fmt_fcfa
# Test équilibre
row += 1
c = ws2.cell(row, 6, f"Équilibre D=C : {'✅ OUI' if total_d==total_c else '❌ NON'}")
c.font = Font(name="Calibri", size=11, bold=True, color="155724" if total_d==total_c else "C0392B")

widths2 = [12, 12, 10, 12, 12, 60, 16, 16, 32, 28]
for j, w in enumerate(widths2, 1):
    ws2.column_dimensions[get_column_letter(j)].width = w
ws2.freeze_panes = "A5"

# ─────── Onglet 3 : DÉTAIL PIÈCES ───────
ws3 = wb.create_sheet("3-Détail pièces")
ws3.sheet_properties.tabColor = NAVY
add_mdc_header(ws3, "Détail exhaustif de toutes les pièces dépouillées")
hdr3 = ["#", "Fournisseur", "Date", "Année", "Catégorie", "Compte", "TTC", "HT", "TVA", "NCC frn ?", "Régime TEE", "Cash ?", "Nb pages", "Page n°", "Extrait OCR"]
for j, h in enumerate(hdr3, 1):
    style_header(ws3.cell(4, j, h))
ws3.row_dimensions[4].height = 35
for i, d in enumerate(sorted_docs, 1):
    fill = GRIS if i % 2 == 0 else None
    vals = [i, d["fournisseur"], fmt_date(d["date_jour"], d["date_mois"], d["annee"]),
            d["annee"] or "?", d["cat_code"], d["compte"], d["ttc"] or 0,
            d["ht"] or "", d["tva"] or "",
            "OUI" if d["has_ncc_fournisseur"] else "NON",
            "OUI" if d["regime_tee"] else "",
            "OUI" if d["espece"] else "",
            d["nb_pages"], d["premiere_page"], d["excerpt"]]
    for j, v in enumerate(vals, 1):
        c = ws3.cell(4+i, j, v); style_data(c, fill)
        if j in (7,8,9): c.number_format = fmt_fcfa
        if j in (1,3,4,6,10,11,12,13): c.alignment = Alignment(horizontal="center")

widths3 = [5, 32, 12, 8, 22, 14, 14, 14, 14, 10, 12, 8, 9, 28, 80]
for j, w in enumerate(widths3, 1):
    ws3.column_dimensions[get_column_letter(j)].width = w
ws3.freeze_panes = "B5"

# ─────── Onglet 4 : ALERTES FISCALES ───────
ws4 = wb.create_sheet("4-Alertes fiscales")
ws4.sheet_properties.tabColor = "C0392B"
add_mdc_header(ws4, "Alertes fiscales et points de vigilance")
hdr4 = ["#", "Code alerte", "Fournisseur", "Date", "Montant TTC", "Nature alerte", "Référence légale", "Impact"]
for j, h in enumerate(hdr4, 1):
    style_header(ws4.cell(4, j, h), fill="C0392B")
ws4.row_dimensions[4].height = 35

alertes = []
for d in sorted_docs:
    # ALERTE 1 : Espèces > 250K (art. 373 CGI — TVA non déductible)
    if d["espece"] and d["ttc"] and d["ttc"] > 250000:
        alertes.append({
            "code": "ART-373",
            "frn": d["fournisseur"], "date": fmt_date(d["date_jour"], d["date_mois"], d["annee"]),
            "ttc": d["ttc"],
            "nature": "Paiement espèces > 250 000 FCFA",
            "ref": "Art. 373 CGI CI — TVA non récupérable",
            "impact": f"TVA non déductible ≈ {int((d['ttc'] or 0)*0.18/1.18):,} FCFA".replace(",", " "),
        })
    # ALERTE 2 : NCC absent
    if not d["has_ncc_fournisseur"]:
        alertes.append({
            "code": "NCC-ABS", "frn": d["fournisseur"],
            "date": fmt_date(d["date_jour"], d["date_mois"], d["annee"]),
            "ttc": d["ttc"] or 0,
            "nature": "NCC fournisseur absent / illisible",
            "ref": "Art. 144 CGI CI — facture non conforme",
            "impact": "Charge potentiellement non déductible IS",
        })
    # ALERTE 3 : Régime TEE (fournisseur non assujetti)
    if d["regime_tee"]:
        alertes.append({
            "code": "TEE-FRN", "frn": d["fournisseur"],
            "date": fmt_date(d["date_jour"], d["date_mois"], d["annee"]),
            "ttc": d["ttc"] or 0,
            "nature": "Fournisseur en régime TEE (non assujetti TVA)",
            "ref": "Art. 348 CGI CI",
            "impact": "Aucune TVA récupérable (normal)",
        })
    # ALERTE 4 : Année hors exercice clôturé
    if d["annee"] and d["annee"] < 2024:
        alertes.append({
            "code": "EX-ANT", "frn": d["fournisseur"],
            "date": fmt_date(d["date_jour"], d["date_mois"], d["annee"]),
            "ttc": d["ttc"] or 0,
            "nature": f"Pièce d'exercice antérieur ({d['annee']})",
            "ref": "Principe de spécialisation des exercices",
            "impact": "À RATTACHER à l'exercice d'origine, pas 2025",
        })

# Dédoublonner par couple (frn, date, code)
seen = set()
unique = []
for a in alertes:
    k = (a["code"], a["frn"], a["date"])
    if k in seen: continue
    seen.add(k); unique.append(a)

for i, a in enumerate(unique, 1):
    fill = ROUGE_PALE if i % 2 == 0 else None
    vals = [i, a["code"], a["frn"], a["date"], a["ttc"], a["nature"], a["ref"], a["impact"]]
    for j, v in enumerate(vals, 1):
        c = ws4.cell(4+i, j, v); style_data(c, fill)
        if j == 5: c.number_format = fmt_fcfa
        if j in (1,2,4): c.alignment = Alignment(horizontal="center")

widths4 = [5, 12, 30, 12, 16, 50, 36, 50]
for j, w in enumerate(widths4, 1):
    ws4.column_dimensions[get_column_letter(j)].width = w
ws4.freeze_panes = "A5"

# Synthèse alertes
row = 4 + len(unique) + 3
ws4.cell(row, 2, "SYNTHÈSE ALERTES").font = Font(name="Calibri", size=12, bold=True, color=NAVY)
row += 1
for code in ["ART-373", "NCC-ABS", "TEE-FRN", "EX-ANT"]:
    n = sum(1 for a in unique if a["code"]==code)
    tot = sum(a["ttc"] for a in unique if a["code"]==code)
    ws4.cell(row, 2, code).font = Font(bold=True)
    ws4.cell(row, 3, f"{n} pièces")
    ws4.cell(row, 4, tot).number_format = fmt_fcfa
    row += 1

# === Export JSON propre pour cross-check ===
import json
json_clean = []
for d in sorted_docs:
    json_clean.append({
        "supplier": d["fournisseur"],
        "year": d["annee"],
        "month": d["date_mois"],
        "day": d["date_jour"],
        "category_code": d["cat_code"],
        "compte": d["compte"],
        "ttc": d["ttc"],
        "ht": d["ht"],
        "tva": d["tva"],
        "ttc_estime": d.get("ttc_estime", False),
        "nb_pages": d["nb_pages"],
        "file": d["premiere_page"],
        "raw_excerpt": d["excerpt"],
        "has_ncc_fournisseur": d["has_ncc_fournisseur"],
        "regime_tee": d["regime_tee"],
        "espece": d["espece"],
    })
with open("/tmp/bna_ocr/factures_clean.json", "w") as f:
    json.dump(json_clean, f, ensure_ascii=False, indent=2)
print(f"✅ JSON propre : /tmp/bna_ocr/factures_clean.json ({len(json_clean)} docs)")

# === SAUVEGARDE ===
wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print(f"\n✅ EXCEL généré : {OUT}")
print(f"   {len(docs)} documents traités → {seq-1} écritures journalisées")
print(f"   {len(unique)} alertes fiscales détectées")
