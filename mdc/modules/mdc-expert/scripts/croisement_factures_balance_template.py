#!/usr/bin/env python3
"""
CROISEMENT FACTURES BNA ↔ BALANCE SAGE
Objectif : répondre à l'accusation DGI « charges enregistrées sans factures »
Méthode  : pour chaque catégorie de charge facturée, agréger TTC factures
           par exercice, mapper aux comptes SYSCOHADA, comparer aux soldes balance.
Référentiel : Guide d'application SYSCOHADA (Loé-Mié & Tari) + RÈGLE MEMORY.md
"""
import json, os, sys
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# --- INPUTS ---
sys.path.insert(0, "/tmp/bna_ocr")
from balance_bna_2022 import BALANCE_BNA_2022
FACTURES = json.load(open("/tmp/bna_ocr/factures_clean.json"))
BALANCE = BALANCE_BNA_2022
EXERCICE = 2022

OUT_DIR = "/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/EXERCICE_2025"
OUT = f"{OUT_DIR}/CROISEMENT_FACTURES_BALANCE_BNA.xlsx"

# --- Globaux 2022 (issus MEMORY.md + SYNTHESE_TRAVAUX_BNA_MDC.md) ---
GLOBAUX_2022 = {
    "CA_706_HT": 161_736_732,
    "Resultat_net": 27_567_383,
    "TVA_facturee": 29_112_610,
    "411_solde_fin": 43_233_648,  # Débiteur = clients qui doivent encore
    "411_encaissements_TTC": 147_615_694,
}
CHARGES_TOTALES_2022_HT_DEDUITES = GLOBAUX_2022["CA_706_HT"] - GLOBAUX_2022["Resultat_net"]
# = 134 169 349 HT (toutes charges déclarées 6xx confondues)

# --- Balance 2022 : isoler classes 6 (charges) ---
charges_balance = []
for cpt, lib, mvt_d, mvt_c, solde_d, solde_c in BALANCE:
    if cpt.startswith("6"):
        charges_balance.append({
            "compte": cpt,
            "libelle": lib.strip(),
            "mvt_d": mvt_d,
            "solde_n": solde_d - solde_c,
        })
charges_2025 = charges_balance  # alias pour compat code en aval

# --- Mapping catégorie fact → comptes SYSCOHADA balance ---
# Codes réalignés sur le SYSCOHADA révisé le 10/10/2026 : le préfixe numérique de chaque code
# est le compte officiel de la catégorie (AUDCIF, liste des comptes p. 257-265) ; les valeurs
# sont les comptes de la balance où la charge peut se trouver (y compris ceux utilisés par BNA).
CAT_TO_COMPTES = {
    "601_MATERIAUX_BTP":       ["60410000", "60110000"],  # Matières + achats marchandises (à arbitrer : 6021/6041 si incorporés aux ouvrages)
    "6058_SOUS_TRAITANCE_BTP": ["60580000", "60570000"],
    "6044_FOURNITURES_ATELIER":["60440000", "60560000", "60410000"],
    "605_FOURNITURES_NON_STOCKABLES": ["60510000", "60520000"],  # eau 6051, électricité 6052 (6053 autres énergies : voir carburant)
    "6055_FOURNITURES_BUREAU": ["60550000", "60470000"],
    "6265_DOCUMENTATION":      ["62650000"],
    "6222_LOCATIONS_IMMO":     ["62221000", "62280000"],
    "6223_LOCATION_MATERIEL":  ["62230000"],
    "614_TRANSPORT_PERS":      ["61400000", "66340000"],  # 614 transports du personnel ; 6634 indemnités de transport
    "618_TRANSPORTS_DIVERS":   ["61800000"],
    "638_PEAGE_FRAIS_ROUTE":   ["63800000"],
    "6053_FRAIS_CARBURANT":    ["60530000", "62810000"],  # BNA a codifié le carburant en 6281 (frais de téléphone) : ATTENTION
    "628_FRAIS_TELECOMS":      ["62810000", "62880000"],
    "627_PUBLICITE_IMPRESSION": ["62700000", "62720000", "62880000"],  # 62880000 : mapping BNA d'origine, à vérifier
    "6324_HONORAIRES_CONSEIL": ["63240000", "63270000", "60570000"],
    "631_FRAIS_BANCAIRES":     ["63100000", "63180000"],
    "6745_AGIOS_INTERETS":     ["67450000"],
    "6384_MISSION_DEPLACEMENT":["63840000"],
    "624_ENTRETIEN_REPARATIONS": ["62410000", "62420000"],
    "625_PRIMES_ASSURANCE":    ["62500000", "62520000"],
    "64_IMPOTS_TAXES":         ["64110000", "64120000", "64180000", "64620000", "64640000"],
    "6588_AUTRES_CHARGES_DIVERSES": ["65880000"],
}

# Anciens codes (préfixes erronés) et codes produits par depouille_factures_template.py,
# ramenés aux codes ci-dessus pour pouvoir relire les JSON déjà produits.
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
    "MATERIAUX_BTP": "601_MATERIAUX_BTP",
    "SOUS_TRAITANCE_COFFRAGE": "6058_SOUS_TRAITANCE_BTP",
    "CARBURANT": "6053_FRAIS_CARBURANT",
    "TELECOM_INTERNET": "628_FRAIS_TELECOMS",
    "PEAGE_TRANSPORTS": "638_PEAGE_FRAIS_ROUTE",
    "LOCATION_MATERIEL": "6223_LOCATION_MATERIEL",
    "LOCATIONS_LOCAUX": "6222_LOCATIONS_IMMO",
    "EAU": "605_FOURNITURES_NON_STOCKABLES",
    "ELECTRICITE": "605_FOURNITURES_NON_STOCKABLES",
    "EAU_ELECTRICITE": "605_FOURNITURES_NON_STOCKABLES",
    "HONORAIRES_CONSEIL": "6324_HONORAIRES_CONSEIL",
    "IMPRIMERIE_PUB": "627_PUBLICITE_IMPRESSION",
    "FOURNITURES_BUREAU": "6055_FOURNITURES_BUREAU",
    "DOCUMENTATION": "6265_DOCUMENTATION",
    "ASSURANCES": "625_PRIMES_ASSURANCE",
    "FRAIS_BANCAIRES": "631_FRAIS_BANCAIRES",
    "AGIOS_INTERETS": "6745_AGIOS_INTERETS",
    "MISSIONS_DEPLACEMENT": "6384_MISSION_DEPLACEMENT",
    "PATENTE": "64_IMPOTS_TAXES",
    "IMPOTS_FONCIERS": "64_IMPOTS_TAXES",
    "DROITS_TIMBRE_VIGNETTES": "64_IMPOTS_TAXES",
    "IMPOTS_TAXES": "64_IMPOTS_TAXES",
    "ENTRETIEN_REPARATIONS": "624_ENTRETIEN_REPARATIONS",
    "FOURNITURES_ATELIER": "6044_FOURNITURES_ATELIER",
    "AUTRES_CHARGES": "6588_AUTRES_CHARGES_DIVERSES",
}
for _f in FACTURES:
    _f["category_code"] = ALIAS_CATEGORIES.get(_f.get("category_code"), _f.get("category_code"))

# --- Agrégation factures par catégorie × année ---
agg = defaultdict(lambda: defaultdict(lambda: {"n":0,"ttc":0,"ht":0}))
for f in FACTURES:
    cat = f["category_code"]
    y = f["year"] or "ND"
    ttc = f.get("ttc") or 0
    ht_est = int(ttc / 1.18) if ttc else 0
    agg[cat][y]["n"] += 1
    agg[cat][y]["ttc"] += ttc
    agg[cat][y]["ht"] += ht_est

# --- Style ---
NAVY="1A1A2E"; OR="E8C547"; ORPALE="F5E5A5"; GRIS="F4F4F8"
ROUGE="C0392B"; ROUGEPALE="F8E8E8"; VERT="27AE60"; VERTPALE="E8F5E9"
CREME="FFFBE8"
fmt_fcfa = '#,##0_- "FCFA";[RED]-#,##0_- "FCFA";"-"'

def H(c, fill=NAVY, fg="FFFFFF", size=11):
    c.font = Font(name="Calibri", size=size, bold=True, color=fg)
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
    ws.row_dimensions[2].height = 20
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=cols)
    c = ws.cell(3,1,"Référentiel : Guide SYSCOHADA + Plan comptable révisé OHADA — Loé-Mié & Tari (L'Harmattan 2018)")
    c.font = Font(name="Calibri", size=9, italic=True, color="666666")
    c.alignment = Alignment(horizontal="center")
    ws.row_dimensions[3].height = 16

# === EXCEL ===
wb = Workbook()

# ─────── Onglet 1 : SYNTHÈSE EXÉCUTIVE ───────
ws = wb.active
ws.title = "0-Synthèse exécutive"
ws.sheet_properties.tabColor = ROUGE
banner(ws, "CROISEMENT FACTURES ↔ BALANCE SAGE — Réponse accusation DGI « charges sans factures »", cols=6)

# Bloc 1 — Question DGI
row = 5
ws.cell(row,1,"❓ ACCUSATION DGI").font = Font(size=13, bold=True, color=ROUGE)
row += 1
ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
ws.cell(row,1, "« BUILDING NEW AFRICA a enregistré comptablement des charges sans pièces justificatives correspondantes »").alignment = Alignment(wrap_text=True)
ws.cell(row,1).font = Font(italic=True, size=11)
ws.row_dimensions[row].height = 30

# Bloc 2 — Méthodologie
row += 2
ws.cell(row,1,"📋 MÉTHODOLOGIE MDC").font = Font(size=13, bold=True, color=NAVY)
row += 1
methodo = [
    "1. Dépouillement OCR de toutes les factures fournies par BNA (144 pages PDF scannées)",
    "2. Catégorisation SYSCOHADA des pièces par grandes masses (Matériaux, Sous-traitance, Carburant, etc.)",
    "3. Pour chaque catégorie : Σ TTC facturée par exercice + ventilation HT estimée (÷ 1,18)",
    "4. Confrontation aux soldes de la balance Sage par compte SYSCOHADA correspondant",
    "5. Calcul du taux de couverture documentaire : Charges balance ÷ Σ Factures (par compte)",
    "6. Conclusion :  Taux > 100 % = manque factures (cas DGI) | Taux < 100 % = factures non comptabilisées",
]
for m in methodo:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    ws.cell(row,1,m).alignment = Alignment(wrap_text=True)
    ws.row_dimensions[row].height = 18
    row += 1

# Bloc 3 — Verdict 2022
row += 1
ws.cell(row,1,"📊 VERDICT EXERCICE 2022 — celui visé par redressement DGI").font = Font(size=13, bold=True, color=NAVY)
row += 1

tot_fact_2022_ttc = sum(d["ttc"] for cat in agg.values() for y, d in cat.items() if y==2022)
tot_fact_2022_ht  = sum(d["ht"]  for cat in agg.values() for y, d in cat.items() if y==2022)
nb_fact_2022      = sum(d["n"]   for cat in agg.values() for y, d in cat.items() if y==2022)
charges_2022_declarees_HT = CHARGES_TOTALES_2022_HT_DEDUITES

bloc = [
    ("CA 2022 déclaré (706 HT)",               GLOBAUX_2022["CA_706_HT"]),
    ("Résultat net 2022 comptabilisé",         GLOBAUX_2022["Resultat_net"]),
    ("→ Charges totales 2022 (déduites = CA − Résultat)", charges_2022_declarees_HT),
    ("", ""),
    ("Nombre de factures 2022 dépouillées",    nb_fact_2022),
    ("Σ Factures 2022 (TTC)",                  tot_fact_2022_ttc),
    ("Σ Factures 2022 (HT estimé ÷ 1,18)",     tot_fact_2022_ht),
    ("", ""),
    ("ÉCART : Factures HT − Charges HT déclarées", tot_fact_2022_ht - charges_2022_declarees_HT),
    ("Ratio Factures / Charges déclarées",      tot_fact_2022_ht / charges_2022_declarees_HT if charges_2022_declarees_HT else 0),
]
for lbl, val in bloc:
    if lbl == "":
        row += 1
        continue
    ws.cell(row,1, lbl).font = Font(bold=True if "ÉCART" in lbl or "Ratio" in lbl or "Résultat" in lbl or "CA" in lbl else False)
    if isinstance(val, (int,float)):
        c = ws.cell(row,3, val)
        if "Ratio" in lbl:
            c.number_format = "0.00"
        elif isinstance(val, int) and val > 100:
            c.number_format = fmt_fcfa
        else:
            c.number_format = "#,##0"
        c.alignment = Alignment(horizontal="right")
        c.font = Font(bold=True, color=VERT if "ÉCART" in lbl and val > 0 else (ROUGE if "ÉCART" in lbl else NAVY))
    row += 1

row += 1
ws.cell(row,1,"🎯 CONCLUSION DÉFENSIVE").font = Font(size=13, bold=True, color=VERT)
row += 1
ratio = tot_fact_2022_ht / charges_2022_declarees_HT if charges_2022_declarees_HT else 0
if ratio >= 1:
    concl = (
        f"✅ ARGUMENT RECEVABLE — Le total des factures 2022 dépouillées ({tot_fact_2022_ht:,} HT) est SUPÉRIEUR "
        f"au total des charges 2022 comptabilisées ({charges_2022_declarees_HT:,} HT). "
        f"Ratio = {ratio:.2f}. Ceci INVALIDE l'accusation DGI : non seulement les charges sont justifiées, "
        f"mais BNA dispose même de factures qui n'ont pas été comptabilisées (sous-déclaration de charges, "
        f"impact résultat fiscal FAVORABLE au contribuable)."
    ).replace(",", " ")
else:
    concl = (
        f"⚠️ VIGILANCE — Le total factures 2022 ({tot_fact_2022_ht:,} HT) est INFÉRIEUR aux charges déclarées "
        f"({charges_2022_declarees_HT:,} HT). Ratio = {ratio:.2f}. Il manque "
        f"{charges_2022_declarees_HT - tot_fact_2022_ht:,} HT de factures pour justifier intégralement les charges. "
        f"À demander au client : compléments de factures, tickets, contrats."
    ).replace(",", " ")
ws.merge_cells(start_row=row, start_column=1, end_row=row+3, end_column=6)
c = ws.cell(row,1, concl)
c.alignment = Alignment(wrap_text=True, vertical="top")
c.fill = PatternFill("solid", fgColor=VERTPALE if ratio>=1 else ROUGEPALE)
c.font = Font(size=11)
ws.row_dimensions[row].height = 100
row += 5

# Note 2025
ws.cell(row,1,"📌 EXERCICE 2025 — limite de l'analyse").font = Font(size=12, bold=True, color=NAVY)
row += 1
note_2025 = (
    "Les factures fournies portent à 96 % sur l'exercice 2022 (77 docs). Pour l'exercice 2025, "
    "seules quelques pièces 2023 et indatées sont présentes. Le détail charge-par-charge ne peut être conduit "
    "que pour 2022. Pour répondre à une accusation DGI portant sur 2025, il faudra : "
    "(i) factures 2025 complémentaires ; (ii) balance Sage 2022 export EXCEL pour passer du global au détail compte par compte."
)
ws.merge_cells(start_row=row, start_column=1, end_row=row+2, end_column=6)
c = ws.cell(row,1,note_2025)
c.alignment = Alignment(wrap_text=True, vertical="top")
c.fill = PatternFill("solid", fgColor=CREME)
ws.row_dimensions[row].height = 75

for j, w in enumerate([55, 18, 22, 12, 12, 12], 1):
    ws.column_dimensions[get_column_letter(j)].width = w

# ─────── Onglet 2 : MATRICE CROISEMENT par catégorie × année ───────
ws2 = wb.create_sheet("1-Matrice factures x année")
ws2.sheet_properties.tabColor = NAVY
banner(ws2, "Matrice complète : factures dépouillées par catégorie × année (HT estimé)", cols=10)

years_present = sorted({y for cat in agg.values() for y in cat.keys() if y!="ND"}) + ["ND"]
hdr = ["Catégorie SYSCOHADA"] + [f"{y} (nb)" for y in years_present] + [f"{y} HT" for y in years_present] + ["Total HT"]
for j, h in enumerate(hdr, 1):
    H(ws2.cell(5, j, h))
ws2.row_dimensions[5].height = 30

cats_sorted = sorted(agg.keys(), key=lambda c: -sum(d["ht"] for d in agg[c].values()))
r = 6
for cat in cats_sorted:
    fill = GRIS if r%2==0 else None
    D(ws2.cell(r,1,cat), fill, bold=True)
    j_off = 2
    for y in years_present:
        D(ws2.cell(r, j_off, agg[cat][y]["n"]), fill, align="center")
        j_off += 1
    for y in years_present:
        c = ws2.cell(r, j_off, agg[cat][y]["ht"])
        D(c, fill, align="right"); c.number_format = fmt_fcfa
        j_off += 1
    tot = sum(d["ht"] for d in agg[cat].values())
    c = ws2.cell(r, j_off, tot); D(c, fill, bold=True, align="right"); c.number_format = fmt_fcfa
    r += 1

# Total ligne
for j in range(1, len(hdr)+1):
    D(ws2.cell(r,j), ORPALE, bold=True)
ws2.cell(r,1,"TOTAL").font = Font(bold=True)
j_off = 2
for y in years_present:
    c = ws2.cell(r, j_off, sum(agg[cat][y]["n"] for cat in agg)); c.number_format = "#,##0"; c.alignment = Alignment(horizontal="center")
    j_off += 1
for y in years_present:
    c = ws2.cell(r, j_off, sum(agg[cat][y]["ht"] for cat in agg)); c.number_format = fmt_fcfa
    j_off += 1
c = ws2.cell(r, j_off, sum(sum(d["ht"] for d in agg[cat].values()) for cat in agg)); c.number_format = fmt_fcfa
c.font = Font(bold=True, color=NAVY)

widths = [38] + [9]*len(years_present) + [16]*len(years_present) + [18]
for j, w in enumerate(widths, 1):
    ws2.column_dimensions[get_column_letter(j)].width = w
ws2.freeze_panes = "B6"

# ─────── Onglet 3 : COUVERTURE BALANCE 2025 ───────
ws3 = wb.create_sheet(f"2-Couverture compte {EXERCICE}")
ws3.sheet_properties.tabColor = NAVY
banner(ws3, f"Couverture documentaire — Comptes de charge balance {EXERCICE} vs Factures {EXERCICE} dépouillées", cols=8)

hdr3 = ["Compte", "Libellé Sage", "Solde Charge 2025 (HT)", "Catégorie factures liée", "Σ Factures HT (ttes années)", "Couverture %", "Verdict", "Commentaire"]
for j, h in enumerate(hdr3, 1):
    H(ws3.cell(5,j,h))
ws3.row_dimensions[5].height = 35

# Reverse map : compte balance → catégorie facture
compte_to_cat = {}
for cat, comptes in CAT_TO_COMPTES.items():
    for cpt in comptes:
        compte_to_cat.setdefault(cpt, []).append(cat)

r = 6
for ch in sorted(charges_2025, key=lambda x: -x["solde_n"]):
    fill = GRIS if r%2==0 else None
    cpt = ch["compte"]
    cats_liees = compte_to_cat.get(cpt, [])
    # Pour la couverture par compte : ne prendre que les factures de l'exercice cible
    fact_ht = sum(d["ht"] for c in cats_liees for y, d in agg[c].items() if y==EXERCICE) if cats_liees else 0
    couv = (fact_ht / ch["solde_n"]) if ch["solde_n"] > 0 else 0
    if not cats_liees:
        verdict = "❓ Pas de factures liées"; comment = "Pas de catégorie facture mappée — vérifier nature"
        vfill = CREME
    elif couv >= 1:
        verdict = "✅ COUVERT"; comment = f"Factures HT couvrent la charge ({couv:.0%})"
        vfill = VERTPALE
    elif couv >= 0.5:
        verdict = "🟡 PARTIEL"; comment = f"Factures couvrent {couv:.0%} — compléments à demander"
        vfill = CREME
    elif couv > 0:
        verdict = "🔴 FAIBLE"; comment = f"Factures couvrent {couv:.0%} — charge sans pièces (cas DGI)"
        vfill = ROUGEPALE
    else:
        verdict = "❌ AUCUNE"; comment = "Aucune facture trouvée — risque rejet DGI"
        vfill = ROUGEPALE
    vals = [cpt, ch["libelle"], ch["solde_n"], ", ".join(cats_liees) or "—", fact_ht, couv, verdict, comment]
    for j, v in enumerate(vals, 1):
        c = ws3.cell(r, j, v)
        D(c, vfill if j==7 else fill, align="center" if j in (1,7) else "left")
        if j in (3,5): c.number_format = fmt_fcfa; c.alignment = Alignment(horizontal="right")
        if j == 6: c.number_format = "0.0%"; c.alignment = Alignment(horizontal="center")
    r += 1
# Total
total_balance = sum(ch["solde_n"] for ch in charges_2025)
total_fact_lies = sum(sum(d["ht"] for c in compte_to_cat.get(ch["compte"], []) for y, d in agg[c].items() if y==EXERCICE) for ch in charges_2025)
for j in range(1,9): D(ws3.cell(r,j), ORPALE, bold=True)
ws3.cell(r,2,"TOTAL CHARGES BALANCE 2025").font = Font(bold=True)
ws3.cell(r,3,total_balance).number_format = fmt_fcfa
ws3.cell(r,5,total_fact_lies).number_format = fmt_fcfa
c = ws3.cell(r,6, total_fact_lies/total_balance if total_balance else 0); c.number_format = "0.0%"
ws3.cell(r,7,f"Couverture globale {(total_fact_lies/total_balance*100 if total_balance else 0):.1f}%").font = Font(bold=True, color=NAVY)

widths3 = [12, 38, 18, 28, 18, 12, 22, 50]
for j, w in enumerate(widths3, 1):
    ws3.column_dimensions[get_column_letter(j)].width = w
ws3.freeze_panes = "C6"

# ─────── Onglet 4 : DÉTAIL FACTURES 2022 ───────
ws4 = wb.create_sheet("3-Détail factures 2022")
ws4.sheet_properties.tabColor = NAVY
banner(ws4, "Pièces 2022 — exercice visé par redressement DGI NRD12739430", cols=8)
hdr4 = ["#", "Fournisseur", "Catégorie", "Compte mappé", "TTC", "HT estimé", "Page OCR", "Extrait"]
for j, h in enumerate(hdr4,1): H(ws4.cell(5,j,h))
ws4.row_dimensions[5].height = 30

fact_2022 = [f for f in FACTURES if f["year"]==2022]
fact_2022.sort(key=lambda f: -(f.get("ttc") or 0))
for i, f in enumerate(fact_2022, 1):
    fill = GRIS if i%2==0 else None
    ttc = f.get("ttc") or 0
    ht_est = int(ttc/1.18) if ttc else 0
    cats_liees = CAT_TO_COMPTES.get(f["category_code"], [])
    vals = [i, f["supplier"], f["category_code"], ", ".join(cats_liees) or "—",
            ttc, ht_est, f["file"], f.get("raw_excerpt","")[:150]]
    for j, v in enumerate(vals, 1):
        c = ws4.cell(5+i,j,v); D(c, fill)
        if j in (5,6): c.number_format = fmt_fcfa
        if j == 1: c.alignment = Alignment(horizontal="center")

# Total
r = 6 + len(fact_2022)
for j in range(1,9): D(ws4.cell(r,j), ORPALE, bold=True)
ws4.cell(r,2,f"TOTAL — {len(fact_2022)} pièces 2022").font = Font(bold=True)
ws4.cell(r,5, sum((f.get("ttc") or 0) for f in fact_2022)).number_format = fmt_fcfa
ws4.cell(r,6, sum(int((f.get("ttc") or 0)/1.18) for f in fact_2022)).number_format = fmt_fcfa

widths4 = [5, 32, 28, 22, 14, 14, 30, 80]
for j, w in enumerate(widths4, 1):
    ws4.column_dimensions[get_column_letter(j)].width = w
ws4.freeze_panes = "B6"

# ─────── Onglet 5 : ARGUMENT DÉFENSE DGI ───────
ws5 = wb.create_sheet("4-Argument défense DGI")
ws5.sheet_properties.tabColor = OR
banner(ws5, "Argumentaire de défense — Notification NRD12739430", cols=4)

texte = [
    ("§1. RAPPEL DU CHEF DE REDRESSEMENT", True, NAVY),
    ("", False, None),
    ("La DGI reproche à BNA d'avoir comptabilisé des charges sans pièces justificatives. "
     "Sur l'exercice 2022 (chef E1 TVA), le rappel s'élève à 8 372 434 FCFA (principal + pénalités).", False, None),
    ("", False, None),
    ("§2. ÉLÉMENTS FACTUELS PRODUITS PAR BNA", True, NAVY),
    ("", False, None),
    (f"• 77 factures originales fournisseurs pour l'exercice 2022 ont été remises au Cabinet MDC", False, None),
    (f"• Σ TTC vérifiable = {tot_fact_2022_ttc:,} FCFA".replace(",", " "), False, None),
    (f"• Σ HT correspondant = {tot_fact_2022_ht:,} FCFA".replace(",", " "), False, None),
    (f"• Charges 2022 déclarées (CA − Résultat) = {charges_2022_declarees_HT:,} FCFA".replace(",", " "), False, None),
    (f"• Ratio Factures/Charges = {ratio:.2f}", False, None),
    ("", False, None),
    ("§3. RÉFÉRENTIEL JURIDIQUE OPPOSÉ À LA DGI", True, NAVY),
    ("", False, None),
    ("• Art. 35 CGI CI : déductibilité conditionnée à pièces justificatives → FOURNIES", False, None),
    ("• Art. 36 AUDCIF : preuve par tout moyen — les factures originales font foi", False, None),
    ("• Art. 361 CGI CI : TVA exigible à l'encaissement → CA 706 = encaissements bancaires confirmés (147,6M TTC)", False, None),
    ("• Guide SYSCOHADA p.343-394 : présentation normalisée — la liasse SN produite respecte ces formes", False, None),
    ("", False, None),
    ("§4. CONCLUSION", True, VERT),
    ("", False, None),
    (concl, False, None),
    ("", False, None),
    ("§5. PIÈCES JOINTES AU MÉMOIRE", True, NAVY),
    ("", False, None),
    ("• DEPOUILLEMENT_FACTURES_BNA.xlsx — détail 120 documents OCR + catégorisation", False, None),
    ("• CROISEMENT_FACTURES_BALANCE_BNA.xlsx — présent fichier", False, None),
    ("• Recueil des 77 factures originales 2022 numérotées et indexées", False, None),
]

r = 5
for txt, bold, color in texte:
    ws5.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    c = ws5.cell(r,1,txt)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if bold:
        c.font = Font(size=12, bold=True, color=color or NAVY)
        c.fill = PatternFill("solid", fgColor=ORPALE if color==NAVY else VERTPALE)
        ws5.row_dimensions[r].height = 22
    elif txt == "":
        ws5.row_dimensions[r].height = 8
    else:
        c.font = Font(size=11)
        ws5.row_dimensions[r].height = 28
    r += 1

for j, w in enumerate([20, 30, 30, 20], 1):
    ws5.column_dimensions[get_column_letter(j)].width = w

# === SAVE ===
wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print(f"\n✅ {OUT}")
print(f"   {len(fact_2022)} factures 2022 / Σ TTC = {tot_fact_2022_ttc:,} / HT = {tot_fact_2022_ht:,}".replace(",", " "))
print(f"   Charges 2022 déclarées (CA-Résultat) = {charges_2022_declarees_HT:,}".replace(",", " "))
print(f"   Ratio Fact/Charges = {ratio:.2f}")
print(f"   Comptes balance 2025 analysés: {len(charges_2025)}")
