#!/usr/bin/env python3
"""LISTE EXHAUSTIVE des dépenses BNA — Fournisseur / Date / Nature / Montant."""
import json, re, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FACTURES = json.load(open("/tmp/bna_ocr/factures_tva.json"))
OCR_DIR = "/tmp/bna_ocr/txt"
OUT = "/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/EXERCICE_2025/LISTE_DEPENSES_BNA.xlsx"

# Libellés humains des catégories
# Codes réalignés sur le SYSCOHADA révisé le 10/10/2026 (préfixe = compte officiel, AUDCIF p. 257-265).
# Codes sans préfixe = codes de depouille_factures_template.py ; codes préfixés = croisement_factures_balance_template.py.
CAT_LABEL = {
    "MATERIAUX_BTP":            "Matériaux BTP (béton, fer, ciment)",
    "601_MATERIAUX_BTP":        "Matériaux BTP (béton, fer, ciment)",
    "SOUS_TRAITANCE_COFFRAGE":  "Sous-traitance / Matériel coffrage",
    "6058_SOUS_TRAITANCE_BTP":  "Sous-traitance BTP",
    "CARBURANT":                "Carburant véhicules (6053)",
    "6053_FRAIS_CARBURANT":     "Carburant véhicules (6053)",
    "TELECOM_INTERNET":         "Télécoms / Internet (628)",
    "628_FRAIS_TELECOMS":       "Télécoms / Internet (628)",
    "PEAGE_TRANSPORTS":         "Péage / frais de route (638)",
    "638_PEAGE_FRAIS_ROUTE":    "Péage / frais de route (638)",
    "618_TRANSPORTS_DIVERS":    "Autres frais de transport (618)",
    "614_TRANSPORT_PERS":       "Transports du personnel (614)",
    "EAU":                      "Eau (6051)",
    "ELECTRICITE":              "Électricité (6052)",
    "EAU_ELECTRICITE":          "Eau / Électricité (6051 / 6052)",
    "605_FOURNITURES_NON_STOCKABLES": "Eau / Électricité, fournitures non stockables (6051 / 6052)",
    "HONORAIRES_CONSEIL":       "Honoraires des professions réglementées (6324)",
    "6324_HONORAIRES_CONSEIL":  "Honoraires des professions réglementées (6324)",
    "IMPRIMERIE_PUB":           "Imprimerie / Publicité (627)",
    "627_PUBLICITE_IMPRESSION": "Imprimerie / Publicité (627)",
    "FOURNITURES_BUREAU":       "Fournitures de bureau (6055)",
    "6055_FOURNITURES_BUREAU":  "Fournitures de bureau (6055)",
    "DOCUMENTATION":            "Documentation générale, livres (6265)",
    "6265_DOCUMENTATION":       "Documentation générale, livres (6265)",
    "ASSURANCES":               "Primes d'assurance (625)",
    "625_PRIMES_ASSURANCE":     "Primes d'assurance (625)",
    "FRAIS_BANCAIRES":          "Frais bancaires (6318)",
    "631_FRAIS_BANCAIRES":      "Frais bancaires (631)",
    "AGIOS_INTERETS":           "Agios, intérêts bancaires (6745)",
    "6745_AGIOS_INTERETS":      "Agios, intérêts bancaires (6745)",
    "MISSIONS_DEPLACEMENT":     "Missions / Déplacements (6384)",
    "6384_MISSION_DEPLACEMENT": "Missions / Déplacements (6384)",
    "LOCATIONS_LOCAUX":         "Loyers bureaux / Locaux (6222)",
    "6222_LOCATIONS_IMMO":      "Loyers bureaux (6222)",
    "LOCATION_MATERIEL":        "Location matériel BTP (6223)",
    "6223_LOCATION_MATERIEL":   "Location matériel BTP (6223)",
    "PATENTE":                  "Patente (6412)",
    "IMPOTS_FONCIERS":          "Impôts fonciers (6411)",
    "DROITS_TIMBRE_VIGNETTES":  "Droits de timbre / vignettes (646)",
    "IMPOTS_TAXES":             "Impôts / Taxes (64)",
    "64_IMPOTS_TAXES":          "Impôts / Taxes (64)",
    "ENTRETIEN_REPARATIONS":    "Entretien / Réparations (6242)",
    "624_ENTRETIEN_REPARATIONS":"Entretien / Réparations (624)",
    "FOURNITURES_ATELIER":      "Fournitures d'atelier (6044)",
    "6044_FOURNITURES_ATELIER": "Fournitures d'atelier (6044)",
    "AUTRES_CHARGES":           "Autres charges diverses (6588)",
    "6588_AUTRES_CHARGES_DIVERSES": "Autres charges diverses (6588)",
}
# Anciens codes à préfixe erroné (JSON produits avant le 10/10/2026) → codes corrigés
ALIAS_CATEGORIES = {
    "6052_FOURNITURES_ATELIER": "6044_FOURNITURES_ATELIER",
    "6053_FOURNITURES_NON_STOCKABLES": "605_FOURNITURES_NON_STOCKABLES",
    "6051_FOURNITURES_BUREAU": "6055_FOURNITURES_BUREAU",
    "6224_LOCATION_MATERIEL": "6223_LOCATION_MATERIEL",
    "6242_TRANSPORT_PERS": "614_TRANSPORT_PERS",
    "6248_TRANSPORTS_DIVERS": "618_TRANSPORTS_DIVERS",
    "6322_FRAIS_CARBURANT": "6053_FRAIS_CARBURANT",
    "6271_FRAIS_TELECOMS": "628_FRAIS_TELECOMS",
    "6271_PUBLICITE_IMPRESSION": "627_PUBLICITE_IMPRESSION",
    "6321_HONORAIRES_CONSEIL": "6324_HONORAIRES_CONSEIL",
    "6311_FRAIS_BANCAIRES": "631_FRAIS_BANCAIRES",
    "6256_MISSION_DEPLACEMENT": "6384_MISSION_DEPLACEMENT",
    "6232_ENTRETIEN_REPARATIONS": "624_ENTRETIEN_REPARATIONS",
    "6161_PRIMES_ASSURANCE": "625_PRIMES_ASSURANCE",
    "6418_IMPOTS_TAXES": "64_IMPOTS_TAXES",
    "65880000_AUTRES_CHARGES_DIVERSES": "6588_AUTRES_CHARGES_DIVERSES",
}
for _d in FACTURES:
    _d["category_code"] = ALIAS_CATEGORIES.get(_d.get("category_code", ""), _d.get("category_code", ""))

# Extraction d'une nature précise depuis l'OCR (1ère ligne désignation)
def extract_nature_precise(d):
    """Cherche un libellé de produit/service précis dans le texte OCR."""
    txt_path = os.path.join(OCR_DIR, d["file"])
    try:
        with open(txt_path) as f: text = f.read()
    except: return d.get("category_code", "")

    # Chercher après mots-clés DESIGNATION/LIBELLE
    m = re.search(r"(?:d[ée]signation|libell[ée]|d[ée]tail|article)\s*[:.]?\s*\n(.+?)(?:\n|$)",
                  text, re.I)
    candidates = []
    if m:
        candidates.append(m.group(1).strip())

    # Mots-clés métier BTP
    btp_pats = [
        r"FER\s*[ÀA]?\s*B[ÉE]TON\s*[A-Z0-9Ф* ]*",
        r"B[ÉE]TON\s*PR[ÊE]T\s*[ÀA]?\s*L[' ]?EMPLOI",
        r"PANNEAU\s*[A-Z0-9 ]*COFFRAGE\s*[A-Z0-9 ]*",
        r"[ÉE]TAI\s*M[ÉE]TALLIQUE\s*[A-Z0-9.,\- ]*",
        r"CADRE\s*ACIER[A-Z0-9 ]*",
        r"CLIP\s*[DE]*\s*CALE[A-Z0-9 ]*",
        r"VIBREUR[A-Z0-9 ]*",
        r"B[ÉE]TONNI[ÈE]RE[A-Z0-9 ]*",
        r"CIMENT[A-Z0-9 ]*",
        r"M[ÉE]MENTO\s*FISCAL\s*\d*",
        r"CODE\s*G[ÉE]N[ÉE]RAL\s*(?:DES\s*)?IMP[ÔO]TS\s*\d*",
        r"RECHARGE\s*[A-Z0-9 ]*BIP\s*PASS",
        r"FACTURE\s*(?:INTERNET|MOBILE|FIXE)",
        r"LOCATION\s*[A-Z0-9 ]+",
        r"GAZOLE|ESSENCE|SANS\s*PLOMB",
    ]
    for pat in btp_pats:
        m = re.search(pat, text, re.I)
        if m:
            candidates.append(m.group(0).strip().title())

    # Filtrer candidats utiles
    for c in candidates:
        if len(c) >= 5 and not c.isdigit() and "fournisseur" not in c.lower():
            return c[:80]

    # Fallback : libellé catégorie
    return CAT_LABEL.get(d["category_code"], d["category_code"].replace("_", " "))

# === Enrichissement ===
for d in FACTURES:
    d["nature_precise"] = extract_nature_precise(d)
    d["categorie_lib"] = CAT_LABEL.get(d["category_code"], d["category_code"].replace("_", " "))

def date_sort_key(d):
    """Tri chronologique."""
    return (d.get("year") or 9999, d.get("month") or 99, d.get("day") or 99)

def fmt_date(d):
    j, m, y = d.get("day"), d.get("month"), d.get("year")
    if y and m and j: return f"{j:02d}/{m:02d}/{y}"
    if y and m: return f"--/{m:02d}/{y}"
    if y: return f"---/---/{y}"
    return "Non datée"

FACTURES_SORT = sorted(FACTURES, key=date_sort_key)

# === EXCEL ===
NAVY="1A1A2E"; OR="E8C547"; ORPALE="F5E5A5"; GRIS="F4F4F8"
VERT="27AE60"; VERTPALE="E8F5E9"; ROUGE="C0392B"; ROUGEPALE="F8E8E8"; CREME="FFFBE8"
fmt = '#,##0_- "FCFA";[RED]-#,##0_- "FCFA";"-"'

def H(c, fill=NAVY, fg="FFFFFF"):
    c.font = Font(name="Calibri", size=11, bold=True, color=fg)
    c.fill = PatternFill("solid", fgColor=fill)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = Border(*([Side(style="thin")]*4))

def D(c, fill=None, bold=False, align="left"):
    c.font = Font(name="Calibri", size=10, bold=bold)
    if fill: c.fill = PatternFill("solid", fgColor=fill)
    c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True)
    c.border = Border(*([Side(style="thin", color="DDDDDD")]*4))

def banner(ws, title, cols=10):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=cols)
    c = ws.cell(1,1,"LA MAISON DE LA CONFORMITÉ SARL")
    c.font = Font(name="Calibri", size=14, bold=True, color=OR)
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=cols)
    c = ws.cell(2,1,title)
    c.font = Font(name="Calibri", size=11, italic=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 22

wb = Workbook()

# ─── Onglet 1 : TOUTES LES DÉPENSES (chronologique) ───
ws = wb.active
ws.title = "1-Toutes dépenses"
ws.sheet_properties.tabColor = NAVY
banner(ws, f"LISTE EXHAUSTIVE DES DÉPENSES BNA — {len(FACTURES)} opérations dépouillées et dédoublonnées", cols=8)

hdr = ["#", "Date", "Fournisseur", "Nature de l'opération", "Catégorie SYSCOHADA", "Montant TTC (FCFA)", "Statut TVA", "Réf. pièce OCR"]
for j, h in enumerate(hdr, 1): H(ws.cell(4, j, h))
ws.row_dimensions[4].height = 30

for i, d in enumerate(FACTURES_SORT, 1):
    fill = GRIS if i%2==0 else None
    statut = d.get("tva_status", "?").replace("_", " ")
    tva_fill = VERTPALE if statut=="AVEC TVA" else (ROUGEPALE if statut=="SANS TVA" else CREME)
    vals = [i, fmt_date(d), d["supplier"], d["nature_precise"], d["categorie_lib"],
            d["ttc"] or 0, statut, d["file"]]
    for j, v in enumerate(vals, 1):
        c = ws.cell(4+i, j, v)
        if j == 7: D(c, tva_fill)
        else: D(c, fill)
        if j == 6: c.number_format = fmt; c.alignment = Alignment(horizontal="right")
        if j in (1, 2, 7): c.alignment = Alignment(horizontal="center", vertical="center")

# Total
r = 5 + len(FACTURES_SORT)
for j in range(1, 9): D(ws.cell(r, j), ORPALE, bold=True)
ws.cell(r, 3, f"TOTAL — {len(FACTURES_SORT)} dépenses").font = Font(bold=True, color=NAVY)
ws.cell(r, 6, sum(d["ttc"] or 0 for d in FACTURES_SORT)).number_format = fmt
ws.cell(r, 6).font = Font(bold=True, size=11, color=NAVY)

widths = [5, 13, 32, 45, 32, 18, 14, 28]
for j, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(j)].width = w
ws.freeze_panes = "C5"

# ─── Onglet 2 : DÉPENSES 2022 SEULES (focus DGI) ───
ws2 = wb.create_sheet("2-Dépenses 2022")
ws2.sheet_properties.tabColor = ROUGE
banner(ws2, "Dépenses exercice 2022 — Cible redressement DGI NRD12739430", cols=8)
for j, h in enumerate(hdr, 1): H(ws2.cell(4, j, h))
ws2.row_dimensions[4].height = 30

fact_2022 = sorted([d for d in FACTURES if d.get("year")==2022], key=date_sort_key)
for i, d in enumerate(fact_2022, 1):
    fill = GRIS if i%2==0 else None
    statut = d.get("tva_status", "?").replace("_", " ")
    tva_fill = VERTPALE if statut=="AVEC TVA" else (ROUGEPALE if statut=="SANS TVA" else CREME)
    vals = [i, fmt_date(d), d["supplier"], d["nature_precise"], d["categorie_lib"],
            d["ttc"] or 0, statut, d["file"]]
    for j, v in enumerate(vals, 1):
        c = ws2.cell(4+i, j, v)
        if j == 7: D(c, tva_fill)
        else: D(c, fill)
        if j == 6: c.number_format = fmt; c.alignment = Alignment(horizontal="right")
        if j in (1, 2, 7): c.alignment = Alignment(horizontal="center", vertical="center")

r2 = 5 + len(fact_2022)
for j in range(1, 9): D(ws2.cell(r2, j), ORPALE, bold=True)
ws2.cell(r2, 3, f"TOTAL 2022 — {len(fact_2022)} dépenses").font = Font(bold=True, color=ROUGE)
ws2.cell(r2, 6, sum(d["ttc"] or 0 for d in fact_2022)).number_format = fmt
ws2.cell(r2, 6).font = Font(bold=True, size=11, color=ROUGE)

for j, w in enumerate(widths, 1):
    ws2.column_dimensions[get_column_letter(j)].width = w
ws2.freeze_panes = "C5"

# ─── Onglet 3 : REGROUPEMENT PAR FOURNISSEUR ───
ws3 = wb.create_sheet("3-Par fournisseur")
ws3.sheet_properties.tabColor = OR
banner(ws3, "Synthèse par fournisseur — Top dépenses BNA", cols=5)
hdr3 = ["Fournisseur", "Nb opérations", "Σ TTC", "1ère date", "Dernière date"]
for j, h in enumerate(hdr3, 1): H(ws3.cell(4, j, h))
ws3.row_dimensions[4].height = 30

from collections import defaultdict
by_frn = defaultdict(lambda: {"n": 0, "ttc": 0, "dates": []})
for d in FACTURES:
    f = d["supplier"]
    by_frn[f]["n"] += 1
    by_frn[f]["ttc"] += d["ttc"] or 0
    if d.get("year") and d.get("month") and d.get("day"):
        by_frn[f]["dates"].append((d["year"], d["month"], d["day"]))

frn_sorted = sorted(by_frn.items(), key=lambda x: -x[1]["ttc"])
for i, (frn, stats) in enumerate(frn_sorted, 1):
    fill = GRIS if i%2==0 else None
    dts = sorted(stats["dates"])
    date_min = f"{dts[0][2]:02d}/{dts[0][1]:02d}/{dts[0][0]}" if dts else "?"
    date_max = f"{dts[-1][2]:02d}/{dts[-1][1]:02d}/{dts[-1][0]}" if dts else "?"
    vals = [frn, stats["n"], stats["ttc"], date_min, date_max]
    for j, v in enumerate(vals, 1):
        c = ws3.cell(4+i, j, v); D(c, fill)
        if j == 3: c.number_format = fmt; c.alignment = Alignment(horizontal="right")
        if j in (2, 4, 5): c.alignment = Alignment(horizontal="center")

r3 = 5 + len(frn_sorted)
for j in range(1, 6): D(ws3.cell(r3, j), ORPALE, bold=True)
ws3.cell(r3, 1, f"TOTAL — {len(frn_sorted)} fournisseurs").font = Font(bold=True)
ws3.cell(r3, 2, sum(s["n"] for s in by_frn.values()))
ws3.cell(r3, 3, sum(s["ttc"] for s in by_frn.values())).number_format = fmt
ws3.cell(r3, 3).font = Font(bold=True, color=NAVY)

widths3 = [38, 14, 18, 14, 14]
for j, w in enumerate(widths3, 1):
    ws3.column_dimensions[get_column_letter(j)].width = w
ws3.freeze_panes = "A5"

wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print(f"\n✅ {OUT}")
print(f"   {len(FACTURES_SORT)} dépenses listées dans Onglet 1")
print(f"   {len(fact_2022)} dépenses 2022 dans Onglet 2")
print(f"   {len(frn_sorted)} fournisseurs uniques dans Onglet 3")

# === IMPRESSION CONSOLE (LISTE COMPLÈTE) ===
print("\n" + "="*120)
print(f"{'#':>3} | {'DATE':>11} | {'FOURNISSEUR':<32} | {'NATURE':<40} | {'MONTANT TTC':>15} | TVA")
print("="*120)
for i, d in enumerate(FACTURES_SORT, 1):
    nature = d["nature_precise"][:40]
    ttc = d["ttc"] or 0
    statut = d.get("tva_status","?")[:8]
    print(f"{i:>3} | {fmt_date(d):>11} | {d['supplier'][:32]:<32} | {nature:<40} | {ttc:>15,} | {statut}".replace(",", " "))
print("="*120)
print(f"TOTAL {len(FACTURES_SORT)} dépenses — Σ TTC = {sum(d['ttc'] or 0 for d in FACTURES_SORT):,} FCFA".replace(",", " "))
