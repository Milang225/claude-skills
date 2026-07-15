#!/usr/bin/env python3
"""Markdown -> DOCX avec VRAIE tete de lettre MDC (LOGO + identite) repetee sur chaque page.
Usage: build_mdc_docx_hf.py SOURCE.md DEST.docx
Gere: # h1, ## h2, ### h3, **gras**, *italique*, ***les deux***, listes '-', listes numerotees,
tableaux | | |, '---' (filet), '> ' (encadre creme), <br>.
Design 2026-07 : logo gauche / identite droite + double filet navy-or, titres centres,
tableaux a filets horizontaux, montants a droite, lignes TOTAL sur or pale.
"""
import sys, re, os
from docx import Document
from docx.shared import Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x1A, 0x1A, 0x2E)
GOLD = RGBColor(0xE8, 0xC5, 0x47)
GOLD_DARK = RGBColor(0xC9, 0xA2, 0x27)
GREY = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x22, 0x22, 0x22)
LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo-mdc.jpg')


def shade(paragraph, fill):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill)
    pPr.append(shd)


def shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill)
    tcPr.append(shd)


def border(paragraph, edge, color, sz=18):
    pPr = paragraph._p.get_or_add_pPr()
    pbdr = pPr.find(qn('w:pBdr'))
    if pbdr is None:
        pbdr = OxmlElement('w:pBdr'); pPr.append(pbdr)
    e = OxmlElement('w:' + edge)
    e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz))
    e.set(qn('w:space'), '4'); e.set(qn('w:color'), color)
    pbdr.append(e)


def cell_borders(cell, top=None, bottom=None, left=None, right=None):
    """each arg: (sz, color) or None"""
    tcPr = cell._tc.get_or_add_tcPr()
    tb = OxmlElement('w:tcBorders')
    for name, spec in (('top', top), ('bottom', bottom), ('left', left), ('right', right)):
        e = OxmlElement('w:' + name)
        if spec is None:
            e.set(qn('w:val'), 'nil')
        else:
            e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(spec[0]))
            e.set(qn('w:space'), '0'); e.set(qn('w:color'), spec[1])
        tb.append(e)
    tcPr.append(tb)


def _emit_run(paragraph, txt, base_size, color, bold, italic, font=None):
    if txt == '':
        return
    r = paragraph.add_run(txt)
    r.font.size = Pt(base_size)
    if color is not None:
        r.font.color.rgb = color
    if font:
        r.font.name = font
    if bold:
        r.bold = True
    if italic:
        r.italic = True


def add_runs(paragraph, text, base_size=11, color=None, font=None):
    pattern = re.compile(r'(\*\*\*.+?\*\*\*|\*\*.+?\*\*|\*.+?\*)')
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            _emit_run(paragraph, text[pos:m.start()], base_size, color, False, False, font)
        tok = m.group(0)
        if tok.startswith('***'):
            _emit_run(paragraph, tok[3:-3], base_size, color, True, True, font)
        elif tok.startswith('**'):
            _emit_run(paragraph, tok[2:-2], base_size, color, True, False, font)
        else:
            _emit_run(paragraph, tok[1:-1], base_size, color, False, True, font)
        pos = m.end()
    if pos < len(text):
        _emit_run(paragraph, text[pos:], base_size, color, False, False, font)


WM_XML = (
    '<w:pict xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">'
    '<v:shape id="MDCWatermark" type="#_x0000_t136" '
    'style="position:absolute;margin-left:0;margin-top:0;width:480pt;height:120pt;rotation:315;'
    'z-index:-251654144;mso-position-horizontal:center;mso-position-horizontal-relative:margin;'
    'mso-position-vertical:center;mso-position-vertical-relative:margin" '
    'o:allowincell="f" fillcolor="#1A1A2E" stroked="f">'
    '<v:fill opacity="0.07"/>'
    '<v:textpath style="font-family:&quot;Calibri&quot;;font-size:1pt;font-weight:bold" string="CONFIDENTIEL"/>'
    '</v:shape></w:pict>'
)


def add_watermark(hdr):
    from docx.oxml import parse_xml
    p = hdr.add_paragraph()
    r = p.add_run()
    r._r.append(parse_xml(WM_XML))


def build_header(section):
    hdr = section.header
    hdr.is_linked_to_previous = False
    add_watermark(hdr)
    # table 2 colonnes : logo | identite
    t = hdr.add_table(rows=1, cols=2, width=Mm(170))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.columns[0].width = Mm(70); t.columns[1].width = Mm(100)
    lc, rc = t.rows[0].cells
    lc.width, rc.width = Mm(70), Mm(100)
    for c in (lc, rc):
        cell_borders(c)
    # logo
    pl = lc.paragraphs[0]
    pl.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if os.path.exists(LOGO):
        pl.add_run().add_picture(LOGO, width=Mm(46))
    # identite a droite
    pr = rc.paragraphs[0]
    pr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r1 = pr.add_run('LA MAISON DE LA CONFORMITÉ')
    r1.bold = True; r1.font.size = Pt(12); r1.font.color.rgb = NAVY
    r1.font.name = 'Times New Roman'
    r1.add_break()
    r2 = pr.add_run("Agence de Notation Administrative — Comptable · Fiscal · Social")
    r2.italic = True; r2.font.size = Pt(8.5); r2.font.color.rgb = GOLD_DARK
    r2.font.name = 'Times New Roman'
    r2.add_break()
    r3 = pr.add_run('Abidjan — Côte d’Ivoire  ·  +225 07 19 31 49 04')
    r3.font.size = Pt(7.5); r3.font.color.rgb = GREY; r3.font.name = 'Calibri'
    r3.add_break()
    r4 = pr.add_run('www.lamaisondelaconformitesarl.net')
    r4.font.size = Pt(7.5); r4.font.color.rgb = GREY; r4.font.name = 'Calibri'
    # double filet sous la tete de lettre
    p1 = hdr.add_paragraph()
    p1.paragraph_format.space_before = Pt(4); p1.paragraph_format.space_after = Pt(0)
    border(p1, 'bottom', '1A1A2E', 16)
    p2 = hdr.add_paragraph()
    p2.paragraph_format.space_before = Pt(1); p2.paragraph_format.space_after = Pt(0)
    border(p2, 'bottom', 'C9A227', 8)


def build_footer(section):
    ftr = section.footer
    ftr.is_linked_to_previous = False
    p = ftr.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    border(p, 'top', 'C9A227', 10)
    r1 = p.add_run('LA MAISON DE LA CONFORMITÉ SARL — NCC : 2506426B — RCCM : CI-ABJ-03-2025-B13-10831 — Capital : 1 000 000 FCFA')
    r1.font.size = Pt(7); r1.font.color.rgb = GREY; r1.font.name = 'Calibri'
    r1.add_break()
    r2 = p.add_run('Tél : 07 19 31 49 04 — lamaisondelaconformite@gmail.com — www.lamaisondelaconformitesarl.net — Document confidentiel')
    r2.font.size = Pt(7); r2.font.color.rgb = GREY; r2.font.name = 'Calibri'


def h1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(14.5); r.font.color.rgb = NAVY
    r.font.name = 'Times New Roman'
    p.paragraph_format.space_after = Pt(2)
    # petit filet or centre
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rr = p2.add_run('———')
    rr.font.color.rgb = GOLD_DARK; rr.font.size = Pt(11); rr.bold = True
    p2.paragraph_format.space_after = Pt(8)


def h2(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(12); r.font.color.rgb = NAVY
    r.font.name = 'Times New Roman'
    p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(2)
    p2 = doc.add_paragraph()
    rr = p2.add_run('——')
    rr.font.color.rgb = GOLD_DARK; rr.font.size = Pt(10); rr.bold = True
    p2.paragraph_format.space_before = Pt(0); p2.paragraph_format.space_after = Pt(5)


def looks_amount(s):
    return bool(re.match(r'^[\d\s.,]+$', re.sub(r'\*|FCFA|—|-', '', s).strip())) and any(ch.isdigit() for ch in s)


def add_table(doc, rows):
    cols = len(rows[0])
    t = doc.add_table(rows=0, cols=cols)
    total_rows = [ri for ri in range(1, len(rows)) if re.search(r'\bTOTAL', rows[ri][0], re.I)]
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for ci, val in enumerate(row):
            cell = cells[ci]
            cell.text = ''
            para = cell.paragraphs[0]
            is_amount_col = ci == cols - 1 and (looks_amount(val) or val == '')
            if is_amount_col and ri > 0:
                para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if ri == 0:
                shade_cell(cell, '1A1A2E')
                cell_borders(cell, bottom=(12, 'C9A227'))
                add_runs(para, val, base_size=9.5, color=WHITE, font='Calibri')
                for run in para.runs:
                    run.bold = True
                if ci == cols - 1:
                    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                is_total = ri in total_rows
                if is_total:
                    shade_cell(cell, 'F5E5A5')
                last = ri == len(rows) - 1
                cell_borders(cell, bottom=(12, '1A1A2E') if last else (4, 'C9C9D2'))
                add_runs(para, val, base_size=10, color=NAVY if is_total else INK)
                if is_total:
                    for run in para.runs:
                        run.bold = True
    return t


def convert(md_path, docx_path):
    lines = open(md_path, encoding='utf-8').read().split('\n')
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Mm(42); sec.bottom_margin = Mm(25)
    sec.left_margin = Mm(20); sec.right_margin = Mm(20)
    sec.header_distance = Mm(8); sec.footer_distance = Mm(10)
    build_header(sec); build_footer(sec)
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'; style.font.size = Pt(11)

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1; continue
        if line.startswith('# '):
            h1(doc, line[2:].strip())
        elif line.startswith('## '):
            h2(doc, line[3:].strip())
        elif line.startswith('### '):
            p = doc.add_paragraph(); r = p.add_run(line[4:].strip())
            r.bold = True; r.font.size = Pt(11.5); r.font.color.rgb = NAVY
            r.font.name = 'Times New Roman'
        elif line.strip() == '<br>':
            doc.add_paragraph()
        elif line.strip().startswith('>'):
            raw = line.strip().lstrip('>').strip()
            mq = re.match(r'^(#+)\s*(.*)$', raw)
            p = doc.add_paragraph()
            shade(p, 'FFFBE8')
            border(p, 'left', 'C9A227', 18)
            p.paragraph_format.left_indent = Pt(8)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            add_runs(p, ('**' + mq.group(2) + '**') if mq else raw, color=NAVY)
        elif set(line.strip()) <= set('-') and len(line.strip()) >= 3:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
        elif line.lstrip().startswith('|'):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                block.append(lines[i]); i += 1
            rows = []
            for bl in block:
                if re.match(r'^\s*\|[\s:\-|]+\|\s*$', bl):
                    continue
                cells = [c.strip() for c in bl.strip().strip('|').split('|')]
                rows.append(cells)
            if rows:
                add_table(doc, rows)
            continue
        elif line.lstrip().startswith('- ') or line.lstrip().startswith('• '):
            p = doc.add_paragraph(style='List Bullet')
            add_runs(p, line.lstrip()[2:].strip())
        elif re.match(r'^\d+\.\s', line.strip()):
            p = doc.add_paragraph(style='List Number')
            add_runs(p, re.sub(r'^\d+\.\s', '', line.strip()))
        else:
            p = doc.add_paragraph()
            add_runs(p, line.strip())
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        i += 1

    doc.save(docx_path)
    print('OK ->', docx_path)


if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2])
