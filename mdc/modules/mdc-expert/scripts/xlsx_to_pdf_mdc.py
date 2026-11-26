#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""xlsx_to_pdf_mdc.py — Convertit un classeur Excel en PDF aux couleurs MDC.
Usage : python3 xlsx_to_pdf_mdc.py SOURCE.xlsx [DEST.pdf]
Chaque onglet devient une section du PDF. Orientation paysage, largeurs auto.
"""
import sys, os, re
import openpyxl
from xml.sax.saxutils import escape as _xml_escape
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak

NAVY = colors.HexColor("#1A1A2E")
OR   = colors.HexColor("#E8C547")
GREY = colors.HexColor("#F4F4F8")
DARK = colors.HexColor("#222222")

import datetime as _dt

def fmt(v, nf=""):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "Oui" if v else "Non"
    if isinstance(v, (_dt.datetime, _dt.date)):
        return v.strftime("%d/%m/%Y")
    if isinstance(v, (int, float)):
        neg = v < 0
        a = abs(v)
        s = f"{a:,.0f}".replace(",", " ") if float(a).is_integer() else f"{a:,.2f}".replace(",", " ")
        return f"({s})" if neg else s
    return str(v)

_CELL = re.compile(r"^([A-Z]+)(\d+)$")
_RANGE = re.compile(r"^([A-Z]+)(\d+):([A-Z]+)(\d+)$")

def _col(letters):
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n

def eval_formula(wsf, wsv, coord, depth=0, seen=None):
    """Évalue les formules simples (=SUM(plage/cellules), suites de ±refs) pour
    le PDF, quand Excel n'a pas encore mis en cache la valeur. Récursif."""
    if seen is None:
        seen = set()
    if coord in seen or depth > 40:
        return None
    seen.add(coord)
    m = _CELL.match(coord)
    if not m:
        return None
    r, c = int(m.group(2)), _col(m.group(1))
    vcache = wsv.cell(row=r, column=c).value          # valeur mise en cache par Excel
    if isinstance(vcache, (int, float)) and not isinstance(vcache, bool):
        return vcache
    f = wsf.cell(row=r, column=c).value
    if not (isinstance(f, str) and f.startswith("=")):
        return vcache if isinstance(vcache, (int, float)) else None
    expr = f[1:].replace(" ", "")
    # Découpe l'expression en termes signés (±), chaque terme = SUM(...) ou une cellule.
    # Gère les formes mixtes : =B39+SUM(B40:B49) , =B18+B32+B44 , =B6-B7 …
    termes = re.findall(r"([+\-]?)(SUM\([^)]*\)|[A-Z]+\d+)", expr, re.I)
    reconstruit = "".join(s + t for s, t in termes)
    if reconstruit != expr:          # forme non reconnue → on renonce proprement
        return None
    total = 0.0
    for signe, terme in termes:
        val = 0.0
        ms = re.match(r"^SUM\((.*)\)$", terme, re.I)
        if ms:
            for part in ms.group(1).split(","):
                rg = _RANGE.match(part)
                if rg:
                    c1, r1, c2, r2 = _col(rg.group(1)), int(rg.group(2)), _col(rg.group(3)), int(rg.group(4))
                    for rr in range(min(r1, r2), max(r1, r2) + 1):
                        for cc in range(min(c1, c2), max(c1, c2) + 1):
                            v = eval_formula(wsf, wsv, f"{get_letter(cc)}{rr}", depth + 1, set(seen))
                            if isinstance(v, (int, float)):
                                val += v
                elif _CELL.match(part):
                    v = eval_formula(wsf, wsv, part, depth + 1, set(seen))
                    if isinstance(v, (int, float)):
                        val += v
        else:
            v = eval_formula(wsf, wsv, terme, depth + 1, set(seen))
            val = v if isinstance(v, (int, float)) else 0.0
        total += -val if signe == "-" else val
    return total

def get_letter(n):
    s = ""
    while n:
        n, rem = divmod(n - 1, 26)
        s = chr(65 + rem) + s
    return s

def used_bounds(ws):
    maxr = maxc = 0
    for row in ws.iter_rows():
        for c in row:
            if c.value not in (None, ""):
                if c.row > maxr: maxr = c.row
                if c.column > maxc: maxc = c.column
    return maxr, maxc

def sheet_table(ws, maxr, maxc, font_size, wsf=None):
    """Construit la grille de cellules en Paragraph (pas de chaînes brutes) :
    un Paragraph fait le retour à la ligne DANS sa colonne, une chaîne brute
    dessinée par Table ne le fait pas et déborde visuellement sur la colonne
    voisine dès qu'elle est plus large que la largeur calculée (bug observé
    sur CHECKLIST_AUDIT_MDC_V2, colonnes C/D qui se chevauchaient)."""
    normal = ParagraphStyle("cell", fontName="Helvetica", fontSize=font_size, textColor=DARK, leading=font_size * 1.3)
    data, col_w = [], [1] * maxc
    for r in range(1, maxr + 1):
        line = []
        for c in range(1, maxc + 1):
            cell = ws.cell(r, c)
            v = cell.value
            # formule non mise en cache par Excel : l'évaluer pour le PDF
            if wsf is not None and (v is None or (isinstance(v, str) and v.startswith("="))):
                fv = eval_formula(wsf, ws, cell.coordinate)
                if isinstance(fv, (int, float)):
                    v = fv
            txt = fmt(v, cell.number_format)
            if len(txt) > 600:
                txt = txt[:598] + "…"
            col_w[c - 1] = max(col_w[c - 1], len(txt))
            if not txt:
                line.append("")
                continue
            para_txt = _xml_escape(txt).replace("\n", "<br/>")
            try:
                if cell.font and cell.font.bold:
                    para_txt = f"<b>{para_txt}</b>"
            except Exception:
                pass
            line.append(Paragraph(para_txt, normal))
        data.append(line)
    return data, col_w

def convert(src, dest=None):
    dest = dest or os.path.splitext(src)[0] + ".pdf"
    wb = openpyxl.load_workbook(src, data_only=True)
    wbf = openpyxl.load_workbook(src, data_only=False)   # formules, pour évaluation PDF
    name = os.path.basename(src)
    # orientation selon la largeur max
    widest = 0
    for ws in wb.worksheets:
        _, mc = used_bounds(ws)
        widest = max(widest, mc)
    pagesize = landscape(A3 if widest > 12 else A4)
    doc = SimpleDocTemplate(dest, pagesize=pagesize,
                            leftMargin=10 * mm, rightMargin=10 * mm,
                            topMargin=10 * mm, bottomMargin=10 * mm,
                            title=os.path.splitext(name)[0])
    h_ban = ParagraphStyle("ban", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white, leading=12)
    h_tit = ParagraphStyle("tit", fontName="Helvetica-Bold", fontSize=11, textColor=NAVY, leading=14)
    h_sub = ParagraphStyle("sub", fontName="Helvetica", fontSize=8, textColor=colors.HexColor("#555555"), leading=10)
    story = []
    for i, ws in enumerate(wb.worksheets):
        wsf = wbf[ws.title] if ws.title in wbf.sheetnames else None
        maxr, maxc = used_bounds(ws)
        if maxr == 0:
            continue
        if i:
            story.append(PageBreak())
        ban = Table([[Paragraph("LA MAISON DE LA CONFORMITE SARL — Diagnostic, mise en conformité et défense en contrôle · Fiscal · Social", h_ban)]],
                    colWidths=[doc.width])
        ban.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 5),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
        story += [ban, Spacer(1, 3 * mm),
                  Paragraph(f"{os.path.splitext(name)[0]} — onglet : {ws.title}", h_tit),
                  Spacer(1, 2 * mm)]
        fs = 7 if maxc > 10 else 8
        data, col_w = sheet_table(ws, maxr, maxc, fs, wsf)
        # largeurs proportionnelles au contenu (le texte s'enroule DANS sa colonne, cf. sheet_table)
        wmax = [min(max(w, 3), 46) for w in col_w]
        tot = sum(wmax) or 1
        widths = [doc.width * w / tot for w in wmax]
        t = Table(data, colWidths=widths, repeatRows=0)
        st = [("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D9D9E0")),
              ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
              ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
        for r in range(len(data)):
            if r % 2:
                st.append(("BACKGROUND", (0, r), (-1, r), GREY))
        t.setStyle(TableStyle(st))
        story += [t, Spacer(1, 3 * mm),
                  Paragraph("LA MAISON DE LA CONFORMITE SARL | NCC 2506426B | Tel 07 19 31 49 04 — Document confidentiel", h_sub)]
    doc.build(story)
    return dest

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: xlsx_to_pdf_mdc.py SOURCE.xlsx [DEST.pdf]"); sys.exit(1)
    out = convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print(f"PDF -> {out}")
