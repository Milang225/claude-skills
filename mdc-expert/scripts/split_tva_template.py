#!/usr/bin/env python3
"""Sépare les factures BNA en 2 catégories : AVEC TVA / SANS TVA."""
import json, re, os
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FACTURES = json.load(open("/tmp/bna_ocr/factures_dedup.json"))
OCR_DIR = "/tmp/bna_ocr/txt"
OUT = "/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/EXERCICE_2025/FACTURES_AVEC_SANS_TVA_BNA.xlsx"

# === DÉTECTION TVA pour chaque facture ===
# Critères :
# - Mention explicite "TVA facturée 18%" + montant > 0
# - Présence "TVA récupérable", "TVA à 18%"
# - À l'inverse : "Exonéré de TVA", "TVA non facturée", régime TEE, "Exo TVA"

def detect_tva_status(d):
    """Retourne ('AVEC_TVA' | 'SANS_TVA' | 'INDETERMINE', motif, montant_tva_estime)."""
    # Recharger texte complet
    txt_path = os.path.join(OCR_DIR, d["file"])
    try:
        with open(txt_path) as f: text = f.read()
    except: text = d.get("raw_excerpt", "")
    low = text.lower()

    # Motifs SANS TVA explicites
    sans_tva_patterns = [
        (r"exon[ée]r[ée]\s*de\s*tva", "Exonéré de TVA explicite"),
        (r"tva\s*non\s*factur[ée]e", "TVA non facturée mentionnée"),
        (r"r[ée]gime.*?(t\.?e\.?e|entreprenant)", "Fournisseur régime TEE"),
        (r"article\s*355[\s-]?6", "Exonération art. 355-6 CGI"),
        (r"hors\s*champ\s*tva", "Hors champ TVA"),
        (r"sans\s*tva", "Mention 'sans TVA'"),
    ]
    for pat, motif in sans_tva_patterns:
        if re.search(pat, low):
            return ("SANS_TVA", motif, 0)

    # Détection montant TVA explicite
    # Pattern 1 : "TVA 18% ... <montant>" ou "TVA facturée (18%) <montant>"
    tva_montant = None
    for pat in [
        r"tva\s*facturée\s*\(?18\s*%\)?\s*[:.]?\s*(\d[\d\s.,]{2,12})",
        r"tva\s*[àa]\s*18\s*%\s*[:.]?\s*(\d[\d\s.,]{2,12})",
        r"\btva\s*18\s*%\s*[:.]?\s*(\d[\d\s.,]{2,12})",
        r"montant\s*tva\s*[:.]?\s*(\d[\d\s.,]{2,12})",
        r"tva\s*r[ée]cup[ée]rable\s*[:.]?\s*(\d[\d\s.,]{2,12})",
    ]:
        m = re.search(pat, low)
        if m:
            raw = m.group(1).strip()
            digits = re.sub(r"\D", "", raw)
            if digits:
                v = int(digits)
                if 100 <= v <= 50_000_000:
                    tva_montant = v
                    return ("AVEC_TVA", f"TVA détectée: {tva_montant:,}".replace(",", " "), tva_montant)

    # Indicateurs régime fournisseur (CI)
    has_ncc = bool(re.search(r"n[°o]\s*cc\s*[:.]?\s*\d|\bcc\s*[°:n]\s*\d", low))
    has_reel = bool(re.search(r"r[ée]gime.*?(r[ée]el|rni|rsi|rme)|reel\s*normal", low))
    has_dge = bool(re.search(r"centre\s*des?\s*imp[ôo]ts?\s*[:.]?\s*(dge|grandes?\s*entreprises?|anyama|plateau|cocody|yopougon|treichville|adjam[ée]|abobo|marcory|koumassi)", low))
    has_tva_mention = bool(re.search(r"\btva\b", low))
    has_tva_recup = bool(re.search(r"tva\s*r[ée]cup", low))

    # PRÉSOMPTION CI : tout fournisseur avec NCC + régime Réel est assujetti TVA
    # (sauf mention contraire explicite déjà testée ci-dessus)
    ttc = d.get("ttc") or 0

    if has_ncc and (has_reel or has_dge or has_tva_mention or has_tva_recup):
        if ttc:
            tva_est = int(round(ttc * 18 / 118))
            motifs = []
            if has_reel: motifs.append("régime Réel")
            if has_dge: motifs.append("Centre impôts identifié")
            if has_tva_mention: motifs.append("mention TVA")
            return ("AVEC_TVA", "NCC + " + " + ".join(motifs) + " (TVA estimée 18%)", tva_est)
        return ("AVEC_TVA", "NCC + régime Réel (TVA présumée)", 0)

    if has_ncc:
        # NCC seul → probable AVEC TVA mais à vérifier
        if ttc:
            tva_est = int(round(ttc * 18 / 118))
            return ("AVEC_TVA", "NCC fournisseur présent (TVA présumée 18%)", tva_est)
        return ("AVEC_TVA", "NCC présent (présomption TVA)", 0)

    if has_tva_mention and ttc:
        tva_est = int(round(ttc * 18 / 118))
        return ("AVEC_TVA", "Mention TVA dans le doc (présomption 18%)", tva_est)

    # Si rien d'identifiable
    return ("INDETERMINE", "Ni NCC ni mention TVA — vérification manuelle", 0)

# === Application ===
for d in FACTURES:
    status, motif, tva_est = detect_tva_status(d)
    d["tva_status"] = status
    d["tva_motif"] = motif
    d["tva_estime"] = tva_est
    if d.get("ttc"):
        d["ht_estime"] = d["ttc"] - tva_est if status=="AVEC_TVA" else d["ttc"]
    else:
        d["ht_estime"] = 0

# === Stats ===
from collections import Counter
print(f"=== Répartition statut TVA (toutes années) ===")
for s, n in Counter(d["tva_status"] for d in FACTURES).most_common():
    sub = [d for d in FACTURES if d["tva_status"]==s]
    ttc_tot = sum(d["ttc"] or 0 for d in sub)
    tva_tot = sum(d["tva_estime"] for d in sub)
    print(f"  {s:<15} {n:>3} docs / TTC = {ttc_tot:>15,} / TVA = {tva_tot:>15,}".replace(",", " "))

print(f"\n=== Exercice 2022 uniquement ===")
fact_2022 = [d for d in FACTURES if d.get("year")==2022]
for s, n in Counter(d["tva_status"] for d in fact_2022).most_common():
    sub = [d for d in fact_2022 if d["tva_status"]==s]
    ttc_tot = sum(d["ttc"] or 0 for d in sub)
    tva_tot = sum(d["tva_estime"] for d in sub)
    ht_tot = sum(d["ht_estime"] for d in sub)
    print(f"  {s:<15} {n:>3} docs / TTC = {ttc_tot:>15,} / HT = {ht_tot:>15,} / TVA récup = {tva_tot:>15,}".replace(",", " "))

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
    ws.row_dimensions[2].height = 20

wb = Workbook()

# ─── Onglet 0 : SYNTHÈSE ───
ws = wb.active
ws.title = "0-Synthèse TVA"
ws.sheet_properties.tabColor = OR
banner(ws, "FACTURES BNA — Ventilation AVEC TVA / SANS TVA / INDÉTERMINÉ", cols=6)

# Tableau récap (toutes années)
row = 5
ws.cell(row,1,"📊 SYNTHÈSE GLOBALE (toutes années)").font = Font(size=13, bold=True, color=NAVY)
row += 2
hdr = ["Statut TVA", "Nb factures", "Σ TTC", "Σ HT estimé", "Σ TVA estimée", "Part TTC"]
for j, h in enumerate(hdr, 1): H(ws.cell(row, j, h))
ws.row_dimensions[row].height = 30
row += 1

total_ttc_all = sum(d["ttc"] or 0 for d in FACTURES)
for status, color in [("AVEC_TVA", VERTPALE), ("SANS_TVA", ROUGEPALE), ("INDETERMINE", CREME)]:
    sub = [d for d in FACTURES if d["tva_status"]==status]
    nb = len(sub)
    ttc = sum(d["ttc"] or 0 for d in sub)
    ht = sum(d["ht_estime"] for d in sub)
    tva = sum(d["tva_estime"] for d in sub)
    part = ttc / total_ttc_all if total_ttc_all else 0
    vals = [status.replace("_"," "), nb, ttc, ht, tva, part]
    for j, v in enumerate(vals, 1):
        c = ws.cell(row, j, v); D(c, color)
        if j in (3,4,5): c.number_format = fmt; c.alignment = Alignment(horizontal="right")
        if j == 6: c.number_format = "0.0%"; c.alignment = Alignment(horizontal="center")
        if j in (1,2): c.alignment = Alignment(horizontal="center")
    row += 1
# Total
for j in range(1, 7): D(ws.cell(row, j), ORPALE, bold=True)
ws.cell(row, 1, "TOTAL").font = Font(bold=True)
ws.cell(row, 2, len(FACTURES))
ws.cell(row, 3, total_ttc_all).number_format = fmt
ws.cell(row, 4, sum(d["ht_estime"] for d in FACTURES)).number_format = fmt
ws.cell(row, 5, sum(d["tva_estime"] for d in FACTURES)).number_format = fmt
ws.cell(row, 6, 1).number_format = "0.0%"
row += 3

# Synthèse 2022 ciblée
ws.cell(row,1,"📊 SYNTHÈSE EXERCICE 2022 (cible redressement DGI)").font = Font(size=13, bold=True, color=ROUGE)
row += 2
for j, h in enumerate(hdr, 1): H(ws.cell(row, j, h))
ws.row_dimensions[row].height = 30
row += 1
fact_2022 = [d for d in FACTURES if d.get("year")==2022]
total_ttc_2022 = sum(d["ttc"] or 0 for d in fact_2022)
for status, color in [("AVEC_TVA", VERTPALE), ("SANS_TVA", ROUGEPALE), ("INDETERMINE", CREME)]:
    sub = [d for d in fact_2022 if d["tva_status"]==status]
    nb = len(sub)
    ttc = sum(d["ttc"] or 0 for d in sub)
    ht = sum(d["ht_estime"] for d in sub)
    tva = sum(d["tva_estime"] for d in sub)
    part = ttc / total_ttc_2022 if total_ttc_2022 else 0
    vals = [status.replace("_"," "), nb, ttc, ht, tva, part]
    for j, v in enumerate(vals, 1):
        c = ws.cell(row, j, v); D(c, color)
        if j in (3,4,5): c.number_format = fmt; c.alignment = Alignment(horizontal="right")
        if j == 6: c.number_format = "0.0%"; c.alignment = Alignment(horizontal="center")
        if j in (1,2): c.alignment = Alignment(horizontal="center")
    row += 1
for j in range(1, 7): D(ws.cell(row, j), ORPALE, bold=True)
ws.cell(row, 1, "TOTAL 2022").font = Font(bold=True)
ws.cell(row, 2, len(fact_2022))
ws.cell(row, 3, total_ttc_2022).number_format = fmt
ws.cell(row, 4, sum(d["ht_estime"] for d in fact_2022)).number_format = fmt
tva_2022 = sum(d["tva_estime"] for d in fact_2022)
ws.cell(row, 5, tva_2022).number_format = fmt
ws.cell(row, 6, 1).number_format = "0.0%"
row += 3

# Argument fiscal
ws.cell(row,1,"💡 IMPACT FISCAL").font = Font(size=13, bold=True, color=VERT)
row += 1
arg = (
    f"L'exercice 2022 comporte {sum(1 for d in fact_2022 if d['tva_status']=='AVEC_TVA')} factures AVEC TVA "
    f"facturée (Σ TVA récupérable estimée = {tva_2022:,} FCFA). ".replace(",", " ") +
    f"Or la balance Sage 2022 ne montre que 14 349 535 FCFA de TVA récupérable (compte 44500000), "
    f"soit potentiellement {tva_2022 - 14349535:,} FCFA de TVA NON DÉDUITE. ".replace(",", " ") +
    f"Cette sous-déduction renforce la défense contre le chef E1 (rappel TVA 8,37M) : "
    f"BNA dispose de davantage de TVA déductible que ce qui lui est imputé."
)
ws.merge_cells(start_row=row, start_column=1, end_row=row+3, end_column=6)
c = ws.cell(row, 1, arg)
c.fill = PatternFill("solid", fgColor=VERTPALE)
c.alignment = Alignment(wrap_text=True, vertical="top")
c.font = Font(size=11)
ws.row_dimensions[row].height = 100

for j, w in enumerate([22, 12, 18, 18, 18, 12], 1):
    ws.column_dimensions[get_column_letter(j)].width = w

# ─── Onglet 1 : FACTURES AVEC TVA ───
ws1 = wb.create_sheet("1-AVEC TVA")
ws1.sheet_properties.tabColor = VERT
banner(ws1, "Factures AVEC TVA — TVA récupérable / déductible (compte 4452 à constater)", cols=10)
hdr1 = ["#", "Fournisseur", "Date", "Année", "Catégorie", "TTC", "HT", "TVA", "Motif détection", "Page OCR"]
for j, h in enumerate(hdr1, 1): H(ws1.cell(4, j, h))
ws1.row_dimensions[4].height = 30

avec_tva = sorted([d for d in FACTURES if d["tva_status"]=="AVEC_TVA"],
                  key=lambda d: (-(d.get("year") or 0), -(d["ttc"] or 0)))
def fmt_date(d):
    j, m, y = d.get("day"), d.get("month"), d.get("year")
    if y and m and j: return f"{j:02d}/{m:02d}/{y}"
    if y: return f"??/??/{y}"
    return "?"

for i, d in enumerate(avec_tva, 1):
    fill = GRIS if i%2==0 else None
    vals = [i, d["supplier"], fmt_date(d), d.get("year") or "?", d["category_code"],
            d["ttc"] or 0, d["ht_estime"], d["tva_estime"], d["tva_motif"], d["file"]]
    for j, v in enumerate(vals, 1):
        c = ws1.cell(4+i, j, v); D(c, fill)
        if j in (6,7,8): c.number_format = fmt
        if j in (1,3,4): c.alignment = Alignment(horizontal="center")
# Total
r = 5 + len(avec_tva)
for j in range(1, 11): D(ws1.cell(r, j), ORPALE, bold=True)
ws1.cell(r, 2, f"TOTAL — {len(avec_tva)} factures avec TVA").font = Font(bold=True)
ws1.cell(r, 6, sum(d["ttc"] or 0 for d in avec_tva)).number_format = fmt
ws1.cell(r, 7, sum(d["ht_estime"] for d in avec_tva)).number_format = fmt
ws1.cell(r, 8, sum(d["tva_estime"] for d in avec_tva)).number_format = fmt

widths1 = [5, 32, 12, 8, 22, 14, 14, 14, 36, 28]
for j, w in enumerate(widths1, 1):
    ws1.column_dimensions[get_column_letter(j)].width = w
ws1.freeze_panes = "B5"

# ─── Onglet 2 : FACTURES SANS TVA ───
ws2 = wb.create_sheet("2-SANS TVA")
ws2.sheet_properties.tabColor = ROUGE
banner(ws2, "Factures SANS TVA — Charges déductibles IS, aucune TVA récupérable", cols=10)
hdr2 = ["#", "Fournisseur", "Date", "Année", "Catégorie", "Montant", "Motif exonération", "Article CGI", "Page OCR", "Extrait OCR"]
for j, h in enumerate(hdr2, 1): H(ws2.cell(4, j, h))
ws2.row_dimensions[4].height = 30

sans_tva = sorted([d for d in FACTURES if d["tva_status"]=="SANS_TVA"],
                  key=lambda d: (-(d.get("year") or 0), -(d["ttc"] or 0)))
for i, d in enumerate(sans_tva, 1):
    fill = GRIS if i%2==0 else None
    # Article CGI selon motif
    art = "Art. 348 CGI" if "tee" in d["tva_motif"].lower() else \
          "Art. 355-6 CGI" if "355" in d["tva_motif"] else \
          "Art. 240+ CGI (exonération)"
    vals = [i, d["supplier"], fmt_date(d), d.get("year") or "?", d["category_code"],
            d["ttc"] or 0, d["tva_motif"], art, d["file"], (d.get("raw_excerpt","")[:120])]
    for j, v in enumerate(vals, 1):
        c = ws2.cell(4+i, j, v); D(c, fill)
        if j == 6: c.number_format = fmt
        if j in (1,3,4): c.alignment = Alignment(horizontal="center")
r = 5 + len(sans_tva)
for j in range(1, 11): D(ws2.cell(r, j), ORPALE, bold=True)
ws2.cell(r, 2, f"TOTAL — {len(sans_tva)} factures sans TVA").font = Font(bold=True)
ws2.cell(r, 6, sum(d["ttc"] or 0 for d in sans_tva)).number_format = fmt

widths2 = [5, 32, 12, 8, 22, 14, 32, 16, 28, 60]
for j, w in enumerate(widths2, 1):
    ws2.column_dimensions[get_column_letter(j)].width = w
ws2.freeze_panes = "B5"

# ─── Onglet 3 : INDÉTERMINÉ ───
ws3 = wb.create_sheet("3-INDETERMINÉ")
ws3.sheet_properties.tabColor = "F4F4F8"
banner(ws3, "Factures INDÉTERMINÉES — Statut TVA à clarifier manuellement", cols=9)
hdr3 = ["#", "Fournisseur", "Date", "Année", "Catégorie", "Montant TTC", "Motif", "Page OCR", "Extrait OCR"]
for j, h in enumerate(hdr3, 1): H(ws3.cell(4, j, h))
ws3.row_dimensions[4].height = 30

indet = sorted([d for d in FACTURES if d["tva_status"]=="INDETERMINE"],
               key=lambda d: (-(d.get("year") or 0), -(d["ttc"] or 0)))
for i, d in enumerate(indet, 1):
    fill = GRIS if i%2==0 else None
    vals = [i, d["supplier"], fmt_date(d), d.get("year") or "?", d["category_code"],
            d["ttc"] or 0, d["tva_motif"], d["file"], (d.get("raw_excerpt","")[:150])]
    for j, v in enumerate(vals, 1):
        c = ws3.cell(4+i, j, v); D(c, fill)
        if j == 6: c.number_format = fmt
        if j in (1,3,4): c.alignment = Alignment(horizontal="center")
r = 5 + len(indet)
for j in range(1, 10): D(ws3.cell(r, j), ORPALE, bold=True)
ws3.cell(r, 2, f"TOTAL — {len(indet)} indéterminés").font = Font(bold=True)
ws3.cell(r, 6, sum(d["ttc"] or 0 for d in indet)).number_format = fmt

widths3 = [5, 32, 12, 8, 22, 14, 32, 28, 70]
for j, w in enumerate(widths3, 1):
    ws3.column_dimensions[get_column_letter(j)].width = w
ws3.freeze_panes = "B5"

# Sauvegarde du JSON enrichi
with open("/tmp/bna_ocr/factures_tva.json", "w") as f:
    json.dump(FACTURES, f, ensure_ascii=False, indent=2)

wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print(f"\n✅ {OUT}")
print(f"   AVEC TVA : {len(avec_tva)} factures")
print(f"   SANS TVA : {len(sans_tva)} factures")
print(f"   INDÉTERMINÉ : {len(indet)} factures")
