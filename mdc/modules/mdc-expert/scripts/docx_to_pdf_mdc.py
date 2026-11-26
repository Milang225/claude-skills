#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docx_to_pdf_mdc.py — Convertit un .docx en PDF aux couleurs MDC.

POURQUOI : Microsoft Word refuse l'export PDF par AppleScript sur ce poste
(« active document ne comprend pas le message save as », -1708), et LibreOffice
est absent. Ce convertisseur maison (python-docx + reportlab) est donc la voie
fiable pour livrer en PDF un Word dont la source markdown a été perdue.
Pendant de xlsx_to_pdf_mdc.py (§9.5) pour les documents Word.

Usage :
  python3 docx_to_pdf_mdc.py SOURCE.docx [DEST.pdf]
  python3 docx_to_pdf_mdc.py --lot "DOSSIER"      # tous les .docx sans PDF

Rendu : en-tête à logo sur chaque page, filigrane CONFIDENTIEL, titres à filet
or, tableaux navy à lignes alternées, pied de page légal MDC.
"""
import os, sys, glob
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "logo-mdc.jpg")
NAVY = colors.HexColor("#1A1A2E")
OR = colors.HexColor("#E8C547")
ORPALE = colors.HexColor("#F5E5A5")
GRIS = colors.HexColor("#F4F4F8")

ENTITE = "LA MAISON DE LA CONFORMITÉ SARL"
SOUS = "Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social"
PIED = ("LA MAISON DE LA CONFORMITÉ SARL  |  NCC : 2506426B  |  RCCM : CI-ABJ-03-2025-B13-10831\n"
        "Tél : 07 19 31 49 04  |  lamaisondelaconformitesarl@outlook.com  |  www.lamaisondelaconformitesarl.net")

CORPS = ParagraphStyle("corps", fontName="Times-Roman", fontSize=10, leading=14,
                       alignment=TA_JUSTIFY, spaceAfter=5, textColor=colors.HexColor("#222222"))
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=17,
                    textColor=NAVY, spaceBefore=12, spaceAfter=6)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11, leading=15,
                    textColor=NAVY, spaceBefore=9, spaceAfter=4)
PUCE = ParagraphStyle("puce", parent=CORPS, leftIndent=10, bulletIndent=2)
CELL = ParagraphStyle("cell", fontName="Helvetica", fontSize=8, leading=10,
                      textColor=colors.HexColor("#222222"))
CELLH = ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=8, leading=10,
                       textColor=colors.white)


def inline(par):
    """Restitue gras et italique des runs d'un paragraphe."""
    out = []
    for r in par.runs:
        t = escape(r.text)
        if not t:
            continue
        if r.bold:
            t = f"<b>{t}</b>"
        if r.italic:
            t = f"<i>{t}</i>"
        out.append(t)
    return "".join(out) or escape(par.text)


def decor(canv, doc, titre, ref):
    canv.saveState()
    L, H = A4
    # bandeau d'en-tête
    canv.setFillColor(NAVY); canv.rect(0, H - 26 * mm, L, 26 * mm, fill=1, stroke=0)
    if os.path.exists(LOGO):
        try:
            canv.drawImage(LOGO, 14 * mm, H - 23 * mm, width=20 * mm, height=18 * mm,
                           preserveAspectRatio=True, mask="auto")
        except Exception:
            pass
    canv.setFillColor(OR); canv.setFont("Helvetica-Bold", 10.5)
    canv.drawRightString(L - 14 * mm, H - 12 * mm, ENTITE)
    canv.setFillColor(colors.white); canv.setFont("Helvetica-Oblique", 6.8)
    canv.drawRightString(L - 14 * mm, H - 16.5 * mm, SOUS)
    canv.setFont("Helvetica", 6.5)
    canv.drawRightString(L - 14 * mm, H - 21 * mm, (ref or "")[:80])
    canv.setFillColor(OR); canv.rect(0, H - 27.2 * mm, L, 1.2 * mm, fill=1, stroke=0)
    # filigrane
    canv.saveState(); canv.translate(L / 2, H / 2); canv.rotate(38)
    canv.setFillColor(colors.Color(0.10, 0.10, 0.18, alpha=0.06))
    canv.setFont("Helvetica-Bold", 62); canv.drawCentredString(0, 0, "CONFIDENTIEL")
    canv.restoreState()
    # pied
    canv.setStrokeColor(OR); canv.setLineWidth(0.8)
    canv.line(14 * mm, 17 * mm, L - 14 * mm, 17 * mm)
    canv.setFillColor(colors.HexColor("#555555")); canv.setFont("Helvetica-Oblique", 6.2)
    for i, ln in enumerate(PIED.split("\n")):
        canv.drawCentredString(L / 2, 13 * mm - i * 3.4 * mm, ln)
    canv.setFont("Helvetica", 7); canv.setFillColor(NAVY)
    canv.drawRightString(L - 14 * mm, 6 * mm, f"page {doc.page}")
    canv.restoreState()


def convertir(src, dst=None):
    dst = dst or os.path.splitext(src)[0] + ".pdf"
    doc = Document(src)
    titre = os.path.splitext(os.path.basename(src))[0].replace("_", " ")
    ref = ""
    flow = []
    # bandeau titre
    flow.append(Table([[Paragraph(f"<b>{escape(titre)}</b>",
                                  ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=12,
                                                 leading=15, textColor=colors.white,
                                                 alignment=TA_CENTER))]],
                      colWidths=[168 * mm],
                      style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                                        ("LINEBELOW", (0, 0), (-1, -1), 1.4, OR),
                                        ("TOPPADDING", (0, 0), (-1, -1), 7),
                                        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)])))
    flow.append(Spacer(1, 7 * mm))

    # parcours du corps dans l'ordre réel (paragraphes et tableaux)
    body = doc.element.body
    itab = iter(doc.tables)
    ipar = iter(doc.paragraphs)
    pmap = {p._p: p for p in doc.paragraphs}
    tmap = {t._tbl: t for t in doc.tables}
    for child in body.iterchildren():
        if child in pmap:
            p = pmap[child]
            txt = inline(p)
            if not txt.strip():
                continue
            st = ((p.style.name if p.style is not None else "") or "").lower()
            if "heading 1" in st or "titre 1" in st:
                flow.append(Paragraph(txt, H1))
            elif "heading" in st or "titre" in st:
                flow.append(Paragraph(txt, H2))
            elif "list" in st or p.text.lstrip().startswith(("•", "-", "·")):
                flow.append(Paragraph(txt.lstrip("•-· "), PUCE, bulletText="•"))
            else:
                flow.append(Paragraph(txt, CORPS))
        elif child in tmap:
            t = tmap[child]
            data = []
            for ri, row in enumerate(t.rows):
                data.append([Paragraph(escape(c.text.strip()), CELLH if ri == 0 else CELL)
                             for c in row.cells])
            if not data:
                continue
            n = max(len(r) for r in data)
            data = [r + [Paragraph("", CELL)] * (n - len(r)) for r in data]
            w = 168 * mm
            cols = [w * 0.34] + [(w * 0.66) / (n - 1)] * (n - 1) if n > 1 else [w]
            style = [("BACKGROUND", (0, 0), (-1, 0), NAVY),
                     ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D8D8E0")),
                     ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                     ("TOPPADDING", (0, 0), (-1, -1), 3),
                     ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
            for ri in range(1, len(data)):
                lbl = str(getattr(data[ri][0], "text", "")).upper()
                if "TOTAL" in lbl:
                    style.append(("BACKGROUND", (0, ri), (-1, ri), ORPALE))
                elif ri % 2 == 0:
                    style.append(("BACKGROUND", (0, ri), (-1, ri), GRIS))
            flow.append(Spacer(1, 3 * mm))
            flow.append(Table(data, colWidths=cols, style=TableStyle(style), repeatRows=1))
            flow.append(Spacer(1, 3 * mm))

    tpl = BaseDocTemplate(dst, pagesize=A4, leftMargin=21 * mm, rightMargin=21 * mm,
                          topMargin=32 * mm, bottomMargin=22 * mm, title=titre)
    frame = Frame(tpl.leftMargin, tpl.bottomMargin, tpl.width, tpl.height, id="f")
    tpl.addPageTemplates([PageTemplate(id="p", frames=[frame],
                                       onPage=lambda c, d: decor(c, d, titre, ref))])
    tpl.build(flow)
    return dst


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 1
    if sys.argv[1] == "--lot":
        racine = sys.argv[2]
        cibles = [f for f in glob.glob(os.path.join(racine, "**", "*.docx"), recursive=True)
                  if not os.path.basename(f).startswith("~$")
                  and not os.path.exists(os.path.splitext(f)[0] + ".pdf")]
        ok = ko = 0
        for f in sorted(cibles):
            try:
                convertir(f); ok += 1
                print(f"  ✅ {os.path.basename(f)}")
            except Exception as e:
                ko += 1
                print(f"  ❌ {os.path.basename(f)} — {str(e)[:90]}")
        print(f"\n{ok} PDF produit(s), {ko} échec(s)")
        return 1 if ko else 0
    out = convertir(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print(f"✅ {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
