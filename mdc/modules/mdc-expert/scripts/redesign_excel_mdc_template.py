#!/usr/bin/env python3
"""Redesign TIM 7 Excel workbook with MDC professional styling."""
from openpyxl import load_workbook, Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, NamedStyle
)
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter
from copy import copy

SRC = "/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/TIM 7/COMPTABILITE/TIM7_FACTURES_JOURNAUX_2025-2026.xlsx"
DST = "/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/TIM 7/COMPTABILITE/TIM7_FACTURES_JOURNAUX_2025-2026.xlsx"

# === Palette MDC ===
NAVY = "1A1A2E"
NAVY_LIGHT = "2D2D4E"
GOLD = "E8C547"
GOLD_LIGHT = "F5E5A5"
GRAY_LIGHT = "F4F4F8"
GRAY_BORDER = "C8C8D0"
RED = "C0392B"
GREEN = "27AE60"
WHITE = "FFFFFF"

THIN = Side(border_style="thin", color=GRAY_BORDER)
MEDIUM_NAVY = Side(border_style="medium", color=NAVY)
BORDER_ALL = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BORDER_TOP_NAVY = Border(left=THIN, right=THIN, top=MEDIUM_NAVY, bottom=THIN)
BORDER_BOTTOM_NAVY = Border(left=THIN, right=THIN, top=THIN, bottom=MEDIUM_NAVY)


def fill(color):
    return PatternFill(start_color=color, end_color=color, fill_type="solid")


def style_brand_header(ws, last_col, title, subtitle):
    """En-tête société : 2 lignes de branding MDC, fond navy + or."""
    # Ligne 1 : MDC + cabinet
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=last_col)
    c = ws.cell(row=1, column=1, value="LA MAISON DE LA CONFORMITÉ SARL  —  Cabinet auditeur de TIM 7 MULTISERVICE")
    c.font = Font(name="Calibri", size=10, bold=True, color=GOLD, italic=True)
    c.fill = fill(NAVY)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 22

    # Ligne 2 : titre du document
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=last_col)
    c = ws.cell(row=2, column=1, value=title)
    c.font = Font(name="Calibri", size=14, bold=True, color=WHITE)
    c.fill = fill(NAVY)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 28

    # Ligne 3 : sous-titre / contexte
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=last_col)
    c = ws.cell(row=3, column=1, value=subtitle)
    c.font = Font(name="Calibri", size=10, italic=True, color=NAVY)
    c.fill = fill(GOLD_LIGHT)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[3].height = 20


def style_table_header(ws, row, last_col):
    """Ligne d'en-tête de tableau : navy + texte blanc gras."""
    for col in range(1, last_col + 1):
        c = ws.cell(row=row, column=col)
        c.font = Font(name="Calibri", size=10, bold=True, color=WHITE)
        c.fill = fill(NAVY)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER_ALL
    ws.row_dimensions[row].height = 32


def style_data_row(ws, row, last_col, even=False, money_cols=()):
    """Ligne de données avec lignes alternées."""
    bg = GRAY_LIGHT if even else WHITE
    for col in range(1, last_col + 1):
        c = ws.cell(row=row, column=col)
        c.font = Font(name="Calibri", size=10, color="000000")
        c.fill = fill(bg)
        c.border = BORDER_ALL
        if col in money_cols:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '#,##0_- "FCFA";[RED]-#,##0_- "FCFA";"-"'
        else:
            c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 22


def style_total_row(ws, row, last_col, money_cols=()):
    """Ligne de totaux : fond navy + texte blanc gras."""
    for col in range(1, last_col + 1):
        c = ws.cell(row=row, column=col)
        c.font = Font(name="Calibri", size=11, bold=True, color=WHITE)
        c.fill = fill(NAVY)
        c.border = BORDER_BOTTOM_NAVY
        if col in money_cols:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '#,##0_- "FCFA";[RED]-#,##0_- "FCFA";"-"'
        else:
            c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[row].height = 26


def style_subtotal_row(ws, row, last_col, money_cols=()):
    """Sous-total : fond gold light + texte navy gras."""
    for col in range(1, last_col + 1):
        c = ws.cell(row=row, column=col)
        c.font = Font(name="Calibri", size=10, bold=True, color=NAVY)
        c.fill = fill(GOLD_LIGHT)
        c.border = BORDER_ALL
        if col in money_cols:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '#,##0_- "FCFA";[RED]-#,##0_- "FCFA";"-"'
        else:
            c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 24


def add_footer(ws, row, last_col):
    """Pied de page MDC."""
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=last_col)
    c = ws.cell(row=row, column=1, value=(
        "LA MAISON DE LA CONFORMITÉ SARL  |  NCC : 2506426B  |  RCCM : CI-ABJ-03-2025-B13-10831  |  "
        "Tél : 07 19 31 49 04  |  lamaisondelaconformitesarl@outlook.com  |  www.lamaisondelaconformitesarl.net"
    ))
    c.font = Font(name="Calibri", size=8, italic=True, color="555566")
    c.fill = fill("F8F8FA")
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[row].height = 20


def auto_width(ws, last_col, mins=None):
    mins = mins or {}
    for col in range(1, last_col + 1):
        letter = get_column_letter(col)
        max_len = mins.get(col, 8)
        for row in ws.iter_rows(min_col=col, max_col=col, values_only=True):
            v = row[0]
            if v is None:
                continue
            l = len(str(v))
            if l > max_len:
                max_len = l
        ws.column_dimensions[letter].width = min(max_len + 3, 50)


def freeze(ws, row, col):
    ws.freeze_panes = ws.cell(row=row, column=col)


# === Charge le workbook source pour récupérer les données ===
src = load_workbook(SRC, data_only=False)


# === Construit un nouveau workbook redesigné ===
new = Workbook()
new.remove(new.active)


# ============================================================
# 1. SYNTHÈSE TVA & MARGE
# ============================================================
ws = new.create_sheet("Synthèse TVA & Marge")
src_ws = src["Synthèse TVA & Marge"]
last_col = 5

style_brand_header(
    ws, last_col,
    "SYNTHÈSE TVA & MARGE BRUTE — TIM 7 MULTISERVICE",
    "NCC 2046563Z  |  RCCM CI-ABJ-2020-B-15355  |  Bingerville  |  Restauration cantine d'entreprise  |  Période : Mars 2025 → Mars 2026",
)
ws.row_dimensions[4].height = 8  # spacer

# Section 1 : Tableau ventes par client
header_row = 5
headers = ["Période / Source", "Nb factures", "CA TTC (FCFA)", "TVA Collectée (FCFA)", "TVA Déductible (FCFA)"]
for i, h in enumerate(headers, 1):
    ws.cell(row=header_row, column=i, value=h)
style_table_header(ws, header_row, last_col)

# Données ventes
ventes_data = [
    ("VENTES 2025 — CML (mars-déc.)", 10, 187_012_000, 0, "—"),
    ("VENTES 2025 — DE HEUS (mai-déc.)", 18, 36_168_670, 5_376_270, "—"),
    ("Sous-total VENTES 2025", 28, 223_180_670, 5_376_270, "—"),
    ("VENTES 2026 — CML (janvier)", 1, 18_388_000, 0, "—"),
    ("VENTES 2026 — DE HEUS (janvier)", 4, 7_400_724, 1_128_924, "—"),
    ("Sous-total VENTES 2026", 5, 25_788_724, 1_128_924, "—"),
]
r = header_row + 1
for i, row in enumerate(ventes_data):
    for j, v in enumerate(row, 1):
        ws.cell(row=r, column=j, value=v)
    if "Sous-total" in row[0]:
        style_subtotal_row(ws, r, last_col, money_cols=(2, 3, 4, 5))
    else:
        style_data_row(ws, r, last_col, even=(i % 2 == 0), money_cols=(2, 3, 4, 5))
    r += 1

# Total ventes
ws.cell(row=r, column=1, value="TOTAL CA HORS TVA & TTC PÉRIODE")
ws.cell(row=r, column=2, value=33)
ws.cell(row=r, column=3, value=248_969_394)
ws.cell(row=r, column=4, value=6_505_194)
ws.cell(row=r, column=5, value=0)
style_total_row(ws, r, last_col, money_cols=(2, 3, 4, 5))
r += 2

# Section 2 : Achats
ws.cell(row=r, column=1, value="ACHATS / FOURNISSEURS — Période complète")
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=last_col)
c = ws.cell(row=r, column=1)
c.font = Font(name="Calibri", size=12, bold=True, color=WHITE)
c.fill = fill(NAVY_LIGHT)
c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws.row_dimensions[r].height = 24
r += 1

ach_headers = ["Fournisseur", "Régime", "Nb factures", "Total TTC (FCFA)", "TVA Déductible"]
for i, h in enumerate(ach_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_table_header(ws, r, last_col)
r += 1

ach_data = [
    ("ETS KONATE FATOUMATA", "TEE / non assujetti TVA", 60, 38_257_700, 0),
    ("KASSIM (Marché Gouro)", "Non assujetti TVA", 8, 12_456_160, 0),
    ("Mme Koné ALL FOOD (cash)", "Reçu non normalisé", 5, 4_000_000, 0),
    ("Sous-total ACHATS 2025", "—", 73, 54_713_860, 0),
    ("ACHATS 2026 (jan-mars)", "Idem fournisseurs", 11, 4_586_410, 0),
]
for i, row in enumerate(ach_data):
    for j, v in enumerate(row, 1):
        ws.cell(row=r, column=j, value=v)
    if "Sous-total" in str(row[0]):
        style_subtotal_row(ws, r, last_col, money_cols=(3, 4, 5))
    else:
        style_data_row(ws, r, last_col, even=(i % 2 == 0), money_cols=(3, 4, 5))
    r += 1

ws.cell(row=r, column=1, value="TOTAL ACHATS PÉRIODE")
ws.cell(row=r, column=2, value="—")
ws.cell(row=r, column=3, value=84)
ws.cell(row=r, column=4, value=59_300_270)
ws.cell(row=r, column=5, value=0)
style_total_row(ws, r, last_col, money_cols=(3, 4, 5))
r += 2

# Section 3 : Indicateurs clés
ws.cell(row=r, column=1, value="INDICATEURS CLÉS DE GESTION")
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=last_col)
c = ws.cell(row=r, column=1)
c.font = Font(name="Calibri", size=12, bold=True, color=WHITE)
c.fill = fill(NAVY_LIGHT)
c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws.row_dimensions[r].height = 24
r += 1

kpi_headers = ["Indicateur", "2025 (12 mois)", "2026 (Q1)", "Norme secteur", "Verdict"]
for i, h in enumerate(kpi_headers, 1):
    ws.cell(row=r, column=i, value=h)
style_table_header(ws, r, last_col)
r += 1

kpis = [
    ("CA TTC", 223_180_670, 25_788_724, "—", "✅"),
    ("Total Achats TTC", 54_713_860, 4_586_410, "—", "✅"),
    ("Marge brute apparente (%)", "75,5%", "82,2%", "25-35% standard restauration", "⚠️ Anormalement haute"),
    ("TVA collectée", 5_376_270, 1_128_924, "—", "À reverser DGI"),
    ("TVA déductible", 0, 0, "—", "❌ Aucun crédit"),
    ("TVA nette à reverser", 5_376_270, 1_128_924, "—", "🔴 6 505 194 FCFA cumulés"),
]
for i, row in enumerate(kpis):
    for j, v in enumerate(row, 1):
        ws.cell(row=r, column=j, value=v)
    style_data_row(ws, r, last_col, even=(i % 2 == 0), money_cols=(2, 3) if isinstance(row[1], (int, float)) else ())
    r += 1

# Footer
r += 1
add_footer(ws, r, last_col)

# Largeurs
ws.column_dimensions["A"].width = 38
ws.column_dimensions["B"].width = 18
ws.column_dimensions["C"].width = 18
ws.column_dimensions["D"].width = 22
ws.column_dimensions["E"].width = 26
freeze(ws, header_row + 1, 1)


# ============================================================
# 2/3. JOURNAUX DE VENTES (2025 et 2026)
# ============================================================
def build_ventes_sheet(name, src_name, year_label, period_subtitle):
    ws = new.create_sheet(name)
    src_ws = src[src_name]
    last_col = 9
    style_brand_header(
        ws, last_col,
        f"JOURNAL DES VENTES {year_label} — TIM 7 MULTISERVICE",
        f"NCC : 2046563Z  |  RCCM : CI-ABJ-2020-B-15355  |  Régime : Réel Simplifié (RSI) à compter de mai 2025  |  {period_subtitle}",
    )
    ws.row_dimensions[4].height = 8

    headers = ["Date", "N° Facture", "Client", "NCC Client", "Désignation", "HT (FCFA)", "TVA (FCFA)", "TTC (FCFA)", "Régime"]
    header_row = 5
    for i, h in enumerate(headers, 1):
        ws.cell(row=header_row, column=i, value=h)
    style_table_header(ws, header_row, last_col)

    # Lecture des données du fichier source à partir de ligne 5
    rows = list(src_ws.iter_rows(min_row=5, values_only=True))
    r = header_row + 1
    total_ht = 0
    total_tva = 0
    total_ttc = 0
    nb = 0
    even = False
    for row in rows:
        if not row or not row[0]:
            continue
        # Skip totals rows from source
        if isinstance(row[0], str) and "TOTAL" in row[0].upper():
            continue
        for j, v in enumerate(row, 1):
            ws.cell(row=r, column=j, value=v)
        style_data_row(ws, r, last_col, even=even, money_cols=(6, 7, 8))
        even = not even
        try:
            total_ht += float(row[5] or 0)
            total_tva += float(row[6] or 0)
            total_ttc += float(row[7] or 0)
            nb += 1
        except (TypeError, ValueError):
            pass
        r += 1

    # Ligne de total
    ws.cell(row=r, column=1, value=f"TOTAL VENTES {year_label}")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
    ws.cell(row=r, column=6, value=total_ht)
    ws.cell(row=r, column=7, value=total_tva)
    ws.cell(row=r, column=8, value=total_ttc)
    ws.cell(row=r, column=9, value=f"{nb} fact.")
    style_total_row(ws, r, last_col, money_cols=(6, 7, 8))
    r += 2
    add_footer(ws, r, last_col)

    widths = {"A": 12, "B": 22, "C": 26, "D": 14, "E": 38, "F": 18, "G": 16, "H": 18, "I": 14}
    for k, v in widths.items():
        ws.column_dimensions[k].width = v
    freeze(ws, header_row + 1, 1)


build_ventes_sheet("Ventes 2025", "Ventes 2025", "2025", "Période : mars → décembre 2025")
build_ventes_sheet("Ventes 2026", "Ventes 2026", "2026", "Période : janvier 2026")


# ============================================================
# 4/5. JOURNAUX D'ACHATS
# ============================================================
def build_achats_sheet(name, src_name, year_label, period_subtitle):
    ws = new.create_sheet(name)
    src_ws = src[src_name]
    last_col = 6
    style_brand_header(
        ws, last_col,
        f"JOURNAL DES ACHATS {year_label} — TIM 7 MULTISERVICE",
        f"Tous fournisseurs « Facturation TVA non autorisée » → TVA déductible = 0  |  {period_subtitle}",
    )
    ws.row_dimensions[4].height = 8

    headers = ["Date", "N° Facture", "Fournisseur", "Désignation", "TTC (FCFA)", "TVA déductible"]
    header_row = 5
    for i, h in enumerate(headers, 1):
        ws.cell(row=header_row, column=i, value=h)
    style_table_header(ws, header_row, last_col)

    rows = list(src_ws.iter_rows(min_row=5, values_only=True))
    r = header_row + 1
    total_ttc = 0
    nb = 0
    even = False
    for row in rows:
        if not row or not row[0]:
            continue
        if isinstance(row[0], str) and "TOTAL" in row[0].upper():
            continue
        for j, v in enumerate(row, 1):
            ws.cell(row=r, column=j, value=v)
        style_data_row(ws, r, last_col, even=even, money_cols=(5, 6))
        even = not even
        try:
            total_ttc += float(row[4] or 0)
            nb += 1
        except (TypeError, ValueError):
            pass
        r += 1

    ws.cell(row=r, column=1, value=f"TOTAL ACHATS {year_label}")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    ws.cell(row=r, column=5, value=total_ttc)
    ws.cell(row=r, column=6, value=0)
    style_total_row(ws, r, last_col, money_cols=(5, 6))
    r += 2
    add_footer(ws, r, last_col)

    widths = {"A": 12, "B": 18, "C": 28, "D": 36, "E": 18, "F": 18}
    for k, v in widths.items():
        ws.column_dimensions[k].width = v
    freeze(ws, header_row + 1, 1)


build_achats_sheet("Achats 2025", "Achats 2025", "2025", "Période : avril → décembre 2025")
build_achats_sheet("Achats 2026", "Achats 2026", "2026", "Période : janvier → mars 2026")


# ============================================================
# 6/7. JOURNAUX SYSCOHADA (Ventes / Achats)
# ============================================================
def build_journal_sheet(name, src_name, journal_type):
    ws = new.create_sheet(name)
    src_ws = src[src_name]
    last_col = 8
    if journal_type == "VTE":
        title = "JOURNAL DES VENTES — ÉCRITURES SYSCOHADA RÉVISÉ"
        sub = "Schéma : D 411 Client / C 7061 Restauration / C 4431 TVA collectée  |  Devise : XOF (FCFA)"
    else:
        title = "JOURNAL DES ACHATS — ÉCRITURES SYSCOHADA RÉVISÉ"
        sub = "Schéma : D 6021 Achats matières / C 401 Fournisseur (TVA déductible = 0)  |  Devise : XOF (FCFA)"

    style_brand_header(ws, last_col, title, sub)
    ws.row_dimensions[4].height = 8

    headers = ["Date", "Pièce", "Compte", "Libellé compte", "Libellé écriture", "Débit", "Crédit", "Journal"]
    header_row = 5
    for i, h in enumerate(headers, 1):
        ws.cell(row=header_row, column=i, value=h)
    style_table_header(ws, header_row, last_col)

    rows = list(src_ws.iter_rows(min_row=5, values_only=True))
    r = header_row + 1
    total_d = 0
    total_c = 0
    even = False
    last_piece = None
    for row in rows:
        if not row or not row[0]:
            continue
        if isinstance(row[0], str) and "TOTAL" in row[0].upper():
            continue
        for j, v in enumerate(row, 1):
            ws.cell(row=r, column=j, value=v)
        # Alterner par paire d'écritures (par pièce)
        piece = row[1]
        if piece != last_piece:
            even = not even
            last_piece = piece
        style_data_row(ws, r, last_col, even=even, money_cols=(6, 7))
        # Couleur D/C : débit en bleu nuit, crédit en gris
        c_d = ws.cell(row=r, column=6)
        c_c = ws.cell(row=r, column=7)
        if c_d.value:
            c_d.font = Font(name="Calibri", size=10, bold=True, color="0F3D5C")
        if c_c.value:
            c_c.font = Font(name="Calibri", size=10, bold=True, color="6B0F3D")
        try:
            total_d += float(row[5] or 0)
            total_c += float(row[6] or 0)
        except (TypeError, ValueError):
            pass
        r += 1

    # Ligne totaux
    ws.cell(row=r, column=1, value=f"TOTAL JOURNAL {journal_type}")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
    ws.cell(row=r, column=6, value=total_d)
    ws.cell(row=r, column=7, value=total_c)
    ws.cell(row=r, column=8, value=journal_type)
    style_total_row(ws, r, last_col, money_cols=(6, 7))
    r += 1

    # Vérification équilibre
    ecart = total_d - total_c
    ws.cell(row=r, column=1, value="Contrôle équilibre Σ Débit = Σ Crédit")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
    ws.cell(row=r, column=6, value=ecart)
    msg = "✅ ÉQUILIBRÉ" if ecart == 0 else "🔴 ÉCART"
    ws.cell(row=r, column=7, value=msg)
    ws.merge_cells(start_row=r, start_column=7, end_row=r, end_column=8)
    for col in range(1, last_col + 1):
        c = ws.cell(row=r, column=col)
        c.font = Font(name="Calibri", size=10, bold=True, color=GREEN if ecart == 0 else RED)
        c.fill = fill(GOLD_LIGHT)
        c.border = BORDER_ALL
        if col == 6:
            c.number_format = '#,##0_- "FCFA";[RED]-#,##0_- "FCFA";"-"'
            c.alignment = Alignment(horizontal="right", vertical="center")
        else:
            c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[r].height = 24
    r += 2

    add_footer(ws, r, last_col)

    widths = {"A": 12, "B": 12, "C": 14, "D": 38, "E": 50, "F": 16, "G": 16, "H": 10}
    for k, v in widths.items():
        ws.column_dimensions[k].width = v
    freeze(ws, header_row + 1, 1)


build_journal_sheet("Journal Ventes (SYSCOHADA)", "Journal Ventes (SYSCOHADA)", "VTE")
build_journal_sheet("Journal Achats (SYSCOHADA)", "Journal Achats (SYSCOHADA)", "ACH")


# ============================================================
# Sauvegarde
# ============================================================
new.save(DST)
print(f"OK -> {DST}")
print(f"Onglets : {new.sheetnames}")
