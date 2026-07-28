#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""xlsx_to_pdf_mdc.py — Convertit un classeur Excel en PDF aux couleurs MDC.
Usage : python3 xlsx_to_pdf_mdc.py SOURCE.xlsx [DEST.pdf]
Chaque onglet devient une section du PDF. Orientation paysage, largeurs auto.
"""
import sys, os
import openpyxl
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak

NAVY = colors.HexColor("#1A1A2E")
OR   = colors.HexColor("#E8C547")
GREY = colors.HexColor("#F4F4F8")
DARK = colors.HexColor("#222222")

def fmt(v, nf=""):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "Oui" if v else "Non"
    if isinstance(v, (int, float)):
        neg = v < 0
        a = abs(v)
        s = f"{a:,.0f}".replace(",", " ") if float(a).is_integer() else f"{a:,.2f}".replace(",", " ")
        return f"({s})" if neg else s
    return str(v)

def used_bounds(ws):
    maxr = maxc = 0
    for row in ws.iter_rows():
        for c in row:
            if c.value not in (None, ""):
                if c.row > maxr: maxr = c.row
                if c.column > maxc: maxc = c.column
    return maxr, maxc

def sheet_table(ws, maxr, maxc, font_size):
    data, styles = [], []
    for r in range(1, maxr + 1):
        line = []
        for c in range(1, maxc + 1):
            cell = ws.cell(r, c)
            txt = fmt(cell.value, cell.number_format)
            if len(txt) > 90:
                txt = txt[:88] + "…"
            line.append(txt)
            try:
                if cell.font and cell.font.bold and txt:
                    styles.append(("FONTNAME", (c - 1, r - 1), (c - 1, r - 1), "Helvetica-Bold"))
            except Exception:
                pass
        data.append(line)
    return data, styles

def convert(src, dest=None):
    dest = dest or os.path.splitext(src)[0] + ".pdf"
    wb = openpyxl.load_workbook(src, data_only=True)
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
        maxr, maxc = used_bounds(ws)
        if maxr == 0:
            continue
        if i:
            story.append(PageBreak())
        ban = Table([[Paragraph("LA MAISON DE LA CONFORMITE SARL — Agence de Notation Administrative · Comptable · Fiscal · Social", h_ban)]],
                    colWidths=[doc.width])
        ban.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 5),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
        story += [ban, Spacer(1, 3 * mm),
                  Paragraph(f"{os.path.splitext(name)[0]} — onglet : {ws.title}", h_tit),
                  Spacer(1, 2 * mm)]
        fs = 7 if maxc > 10 else 8
        data, extra = sheet_table(ws, maxr, maxc, fs)
        # largeurs proportionnelles au contenu
        wmax = [max((len(data[r][c]) for r in range(len(data))), default=1) for c in range(maxc)]
        wmax = [min(max(w, 3), 46) for w in wmax]
        tot = sum(wmax) or 1
        widths = [doc.width * w / tot for w in wmax]
        t = Table(data, colWidths=widths, repeatRows=0)
        st = [("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
              ("FONTSIZE", (0, 0), (-1, -1), fs),
              ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
              ("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D9D9E0")),
              ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
              ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
        for r in range(len(data)):
            if r % 2:
                st.append(("BACKGROUND", (0, r), (-1, r), GREY))
        st += extra
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
