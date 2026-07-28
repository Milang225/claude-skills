#!/usr/bin/env python3
"""Markdown -> PDF MDC : papier a en-tete avec LOGO sur chaque page + pied legal.
Usage: build_mdc_pdf.py SOURCE.md DEST.pdf
Design 2026-07 : tete de lettre (logo gauche / identite droite, double filet navy-or),
titres centres, tableaux a filets horizontaux fins, montants a droite, TOTAL sur or pale.
"""
import sys, re, html, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

NAVY = colors.HexColor('#1A1A2E')
GOLD = colors.HexColor('#E8C547')
GOLD_DARK = colors.HexColor('#C9A227')
GOLD_PALE = colors.HexColor('#F5E5A5')
GREY = colors.HexColor('#666666')
LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo-mdc.jpg')

W, H = A4
LOGO_W, LOGO_H = 46 * mm, 46 * mm * 418.0 / 1024.0   # ratio natif 1024x418


def draw_furniture(canvas, doc):
    canvas.saveState()
    # --- FILIGRANE CONFIDENTIEL (sous le contenu) ---
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.setFillAlpha(0.055)
    canvas.setFont('Helvetica-Bold', 62)
    canvas.translate(W / 2, H / 2)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, 'CONFIDENTIEL')
    canvas.restoreState()
    top = H - 12 * mm
    # --- TETE DE LETTRE : logo a gauche ---
    if os.path.exists(LOGO):
        canvas.drawImage(LOGO, 18 * mm, top - LOGO_H, width=LOGO_W, height=LOGO_H,
                         preserveAspectRatio=True, anchor='nw')
    # identite a droite
    rx = W - 18 * mm
    canvas.setFillColor(NAVY)
    canvas.setFont('Times-Bold', 12.5)
    canvas.drawRightString(rx, top - 5.2 * mm, 'LA MAISON DE LA CONFORMITÉ')
    canvas.setFillColor(GOLD_DARK)
    canvas.setFont('Times-Italic', 8.3)
    canvas.drawRightString(rx, top - 9.4 * mm, "Agence de Notation Administrative — Comptable · Fiscal · Social")
    canvas.setFillColor(GREY)
    canvas.setFont('Helvetica', 7)
    canvas.drawRightString(rx, top - 13.2 * mm, 'Abidjan — Côte d’Ivoire   ·   +225 07 19 31 49 04')
    canvas.drawRightString(rx, top - 16.6 * mm, 'www.lamaisondelaconformitesarl.net')
    # double filet sous la tete de lettre
    y = top - LOGO_H - 3.5 * mm
    canvas.setStrokeColor(NAVY); canvas.setLineWidth(1.4)
    canvas.line(18 * mm, y, W - 18 * mm, y)
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.7)
    canvas.line(18 * mm, y - 1.6 * mm, W - 18 * mm, y - 1.6 * mm)
    # --- PIED ---
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.9)
    canvas.line(18 * mm, 17 * mm, W - 18 * mm, 17 * mm)
    canvas.setFillColor(GREY)
    canvas.setFont('Helvetica', 6.8)
    canvas.drawCentredString(W / 2, 13.4 * mm,
        'LA MAISON DE LA CONFORMITÉ SARL — NCC : 2506426B — RCCM : CI-ABJ-03-2025-B13-10831 — Capital : 1 000 000 FCFA')
    canvas.drawCentredString(W / 2, 10.2 * mm,
        'Tél : 07 19 31 49 04 — lamaisondelaconformite@gmail.com — www.lamaisondelaconformitesarl.net — Document confidentiel')
    # liens cliquables (site web) : zone pied + zone en-tete
    canvas.linkURL('https://lamaisondelaconformitesarl.net',
                   (W/2 - 60*mm, 9*mm, W/2 + 60*mm, 12.5*mm), relative=0)
    canvas.linkURL('https://lamaisondelaconformitesarl.net',
                   (rx - 60*mm, top - 18*mm, rx, top - 14.5*mm), relative=0)
    canvas.setFillColor(NAVY)
    canvas.setFont('Times-Italic', 7.5)
    canvas.drawRightString(W - 18 * mm, 6.8 * mm, 'Page %d' % doc.page)
    canvas.restoreState()


def md_inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # nombres insécables : espace entre chiffres -> espace insécable (évite « 504 072 » coupé)
    text = re.sub(r'(?<=\d)\s+(?=\d)', ' ', text)
    return text


def col_widths(rows, ncol, total):
    """Largeurs proportionnelles au contenu (bornées par un plancher)."""
    weights = []
    for ci in range(ncol):
        L = max((len(re.sub(r'[*]', '', r[ci])) for r in rows if ci < len(r)), default=4)
        weights.append(max(4, min(L, 42)))
    tot = float(sum(weights))
    w = [total * x / tot for x in weights]
    floor = 17 * mm
    small = [k for k in range(ncol) if w[k] < floor]
    if small:
        big = [k for k in range(ncol) if w[k] > floor]
        surplus = sum(w[k] - floor for k in big) or 1.0
        deficit = sum(floor - w[k] for k in small)
        for k in small:
            w[k] = floor
        for k in big:
            w[k] -= deficit * ((w[k] - floor) / surplus)
    return w


def looks_amount(s):
    return bool(re.match(r'^[\d\s.,]+$', re.sub(r'\*|FCFA|—|-', '', s).strip())) and any(ch.isdigit() for ch in s)


def build(md_path, pdf_path):
    styles = getSampleStyleSheet()
    body = ParagraphStyle('body', parent=styles['Normal'], fontName='Times-Roman',
                          fontSize=10.5, leading=15.5, alignment=TA_JUSTIFY, spaceAfter=5)
    h1s = ParagraphStyle('h1', parent=styles['Normal'], fontName='Times-Bold',
                         fontSize=14.5, textColor=NAVY, alignment=TA_CENTER,
                         spaceBefore=4, spaceAfter=2, leading=19)
    h2s = ParagraphStyle('h2', parent=styles['Normal'], fontName='Times-Bold',
                         fontSize=12, textColor=NAVY, spaceBefore=13, spaceAfter=1, leading=15)
    h3s = ParagraphStyle('h3', parent=styles['Normal'], fontName='Times-Bold',
                         fontSize=10.8, textColor=NAVY, spaceBefore=8, spaceAfter=2)
    meta = ParagraphStyle('meta', parent=body, alignment=TA_LEFT, spaceAfter=1.5, fontSize=10.2, leading=14)
    bullet = ParagraphStyle('bullet', parent=body, leftIndent=14, bulletIndent=4, spaceAfter=2.5)
    note = ParagraphStyle('note', parent=body, leftIndent=10, rightIndent=8, textColor=NAVY,
                          backColor=colors.HexColor('#FFFBE8'), borderColor=GOLD, borderWidth=0.8,
                          borderPadding=8, spaceBefore=6, spaceAfter=8, leading=15)

    lines = open(md_path, encoding='utf-8').read().split('\n')
    flow = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        s = line.strip()
        if not s:
            i += 1; continue
        if s.startswith('# '):
            flow.append(Paragraph(md_inline(s[2:]), h1s))
            flow.append(HRFlowable(width='22%', thickness=1.1, color=GOLD_DARK,
                                   spaceBefore=3, spaceAfter=9, hAlign='CENTER'))
        elif s.startswith('## '):
            flow.append(Paragraph(md_inline(s[3:]), h2s))
            flow.append(HRFlowable(width='16%', thickness=0.9, color=GOLD_DARK,
                                   spaceBefore=1.5, spaceAfter=6, hAlign='LEFT'))
        elif s.startswith('### '):
            flow.append(Paragraph(md_inline(s[4:]), h3s))
        elif re.fullmatch(r'(?:<br\s*/?>\s*)+', s):
            flow.append(Spacer(1, 12 * s.count('<br')))
        elif s.startswith('>'):
            raw = s.lstrip('>').strip()
            mq = re.match(r'^(#+)\s*(.*)$', raw)
            if mq:
                flow.append(Paragraph('<b>' + md_inline(mq.group(2)) + '</b>', note))
            else:
                flow.append(Paragraph(md_inline(raw), note))
        elif set(s) <= set('-') and len(s) >= 3:
            flow.append(Spacer(1, 5))
        elif s.startswith('|'):
            block = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                block.append(lines[i].strip()); i += 1
            rows = []
            for bl in block:
                if re.match(r'^\|[\s:\-|]+\|$', bl):
                    continue
                rows.append([c.strip() for c in bl.strip('|').split('|')])
            if rows:
                ncol = len(rows[0])
                total_rows = [r for r in range(1, len(rows))
                              if re.search(r'\bTOTAL', rows[r][0], re.I)]
                data = []
                for r, row in enumerate(rows):
                    cells = []
                    for c_i, c in enumerate(row):
                        if r == 0:
                            st = ParagraphStyle('th', parent=body, fontSize=9.3, leading=12,
                                                textColor=colors.white, fontName='Helvetica-Bold',
                                                alignment=TA_RIGHT if c_i == ncol - 1 else TA_LEFT)
                        else:
                            right = c_i == ncol - 1 and (looks_amount(c) or c == '')
                            st = ParagraphStyle('td', parent=body, fontSize=9.6, leading=13,
                                                textColor=NAVY if r in total_rows else colors.HexColor('#222222'),
                                                fontName='Times-Bold' if r in total_rows else 'Times-Roman',
                                                alignment=TA_RIGHT if right else TA_LEFT)
                        cells.append(Paragraph(md_inline(c), st))
                    data.append(cells)
                colw = col_widths(rows, ncol, 174*mm)
                cmds = [
                    ('BACKGROUND', (0, 0), (-1, 0), NAVY),
                    ('LINEBELOW', (0, 0), (-1, 0), 1.0, GOLD_DARK),
                    ('LINEBELOW', (0, 1), (-1, -1), 0.35, colors.HexColor('#C9C9D2')),
                    ('LINEBELOW', (0, -1), (-1, -1), 0.9, NAVY),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('TOPPADDING', (0, 0), (-1, -1), 5.5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5.5),
                ]
                for tr in total_rows:
                    cmds.append(('BACKGROUND', (0, tr), (-1, tr), GOLD_PALE))
                t = Table(data, colWidths=colw, repeatRows=1)
                t.setStyle(TableStyle(cmds))
                flow.append(Spacer(1, 4)); flow.append(t); flow.append(Spacer(1, 7))
            continue
        elif s.startswith('- ') or s.startswith('• '):
            flow.append(Paragraph(md_inline(s[2:]), bullet, bulletText='—'))
        elif re.match(r'^\d+\.\s', s):
            n = re.match(r'^(\d+)\.\s', s).group(1)
            flow.append(Paragraph(md_inline(re.sub(r'^\d+\.\s', '', s)), bullet,
                                  bulletText='%s.' % n))
        else:
            st = meta if re.match(r'^\*\*[^*]+:\*\*', s) else body
            flow.append(Paragraph(md_inline(s), st))
        i += 1

    header_zone = 12 * mm + LOGO_H + 8 * mm     # ~39 mm reserves en haut
    doc = BaseDocTemplate(pdf_path, pagesize=A4,
                          leftMargin=18*mm, rightMargin=18*mm,
                          topMargin=0, bottomMargin=0)
    frame = Frame(18*mm, 20*mm, W - 36*mm, H - header_zone - 20*mm, id='main')
    doc.addPageTemplates([PageTemplate(id='mdc', frames=[frame], onPage=draw_furniture)])
    doc.build(flow)
    print('OK ->', pdf_path)


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
