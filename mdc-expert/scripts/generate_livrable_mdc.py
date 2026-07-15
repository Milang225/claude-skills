#!/usr/bin/env python3
"""Générateur de livrables MDC (python-docx) — tête de lettre LOGO + filigrane CONFIDENTIEL.
Usage: script.py source.md dest.docx "Titre" "Client" "Réf".
Design juillet 2026 (aligné sur build_mdc_docx_hf.py) : logo gauche / identité droite,
double filet navy-or, filigrane CONFIDENTIEL, tableaux à filets horizontaux fins,
montants à droite, lignes TOTAL sur or pâle."""
import sys, re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml

LOGO = Path(__file__).parent / "logo-mdc.jpg"
NAVY = RGBColor(0x1A,0x1A,0x2E); GOLD="E8C547"; GOLD_DARK_HEX="C9A227"
GOLD_DARK = RGBColor(0xC9,0xA2,0x27); NAVYHEX="1A1A2E"; GREY=RGBColor(0x66,0x66,0x66)
INK = RGBColor(0x22,0x22,0x22)

import re as _re
_MAP={"☐":"[  ]","☑":"[X]","✅":"Oui","❌":"Non","⚠️":"Reserve","⚠":"Reserve",
"\U0001f534":"Critique","\U0001f7e0":"Majeur","\U0001f7e1":"Mineur","\U0001f7e2":"OK","\U0001f535":"",
"\U0001f4a1":"Reco :","▸":"–","\U0001f4ca":"","\U0001f4cc":"","⚖️":"","⚖":"",
"\U0001f4b0":"","⭐":"","\U0001f50d":"","\U0001f3db️":"","\U0001f3db":"","▶":"","↗":"",
"\U0001f7e3":"","➤":"–"}
_EMO=_re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000026FF\U00002700-\U000027BF\U0001F1E6-\U0001F1FF\U00002B00-\U00002BFF️]")
def sober(t):
    if t is None: return t
    t=str(t)
    for k,v in _MAP.items(): t=t.replace(k,v)
    t=_EMO.sub("",t)
    return _re.sub(r"  +"," ",t).strip()

def shade(cell, hexcolor):
    sh=OxmlElement('w:shd'); sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),hexcolor)
    cell._tc.get_or_add_tcPr().append(sh)
def no_borders(tbl):
    tblPr=tbl._tbl.tblPr; b=OxmlElement('w:tblBorders')
    for e in ('top','left','bottom','right','insideH','insideV'):
        el=OxmlElement(f'w:{e}'); el.set(qn('w:val'),'none'); b.append(el)
    tblPr.append(b)
def cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr=cell._tc.get_or_add_tcPr(); tb=OxmlElement('w:tcBorders')
    for name,spec in (('top',top),('bottom',bottom),('left',left),('right',right)):
        e=OxmlElement('w:'+name)
        if spec is None: e.set(qn('w:val'),'nil')
        else:
            e.set(qn('w:val'),'single'); e.set(qn('w:sz'),str(spec[0]))
            e.set(qn('w:space'),'0'); e.set(qn('w:color'),spec[1])
        tb.append(e)
    tcPr.append(tb)
def bottom_rule(p, hexcolor, sz="18"):
    pPr=p._p.get_or_add_pPr(); bdr=OxmlElement('w:pBdr'); bot=OxmlElement('w:bottom')
    bot.set(qn('w:val'),'single'); bot.set(qn('w:sz'),sz); bot.set(qn('w:space'),'4'); bot.set(qn('w:color'),hexcolor)
    bdr.append(bot); pPr.append(bdr)
def page_field(p):
    for t,val in [('begin',None),('text','PAGE'),('end',None)]:
        if t=='text':
            r=OxmlElement('w:r'); f=OxmlElement('w:instrText'); f.set(qn('xml:space'),'preserve'); f.text=' PAGE '; r.append(f); p._p.append(r)
        else:
            r=OxmlElement('w:r'); fc=OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'),t); r.append(fc); p._p.append(r)

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

def build_header(section):
    h=section.header; h.is_linked_to_previous=False
    # filigrane CONFIDENTIEL
    wp=h.add_paragraph(); wr=wp.add_run(); wr._r.append(parse_xml(WM_XML))
    # table 2 cols : logo | identité
    t=h.add_table(rows=1, cols=2, width=Cm(17)); no_borders(t); t.alignment=WD_TABLE_ALIGNMENT.CENTER
    c0,c1=t.rows[0].cells
    if LOGO.exists():
        c0.paragraphs[0].add_run().add_picture(str(LOGO), width=Cm(4.6))
    p=c1.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    r=p.add_run("LA MAISON DE LA CONFORMITÉ"); r.bold=True; r.font.color.rgb=NAVY; r.font.size=Pt(12); r.font.name="Times New Roman"
    p2=c1.add_paragraph(); p2.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    r2=p2.add_run("Agence de Notation Administrative — Comptable · Fiscal · Social")
    r2.italic=True; r2.font.color.rgb=GOLD_DARK; r2.font.size=Pt(8.5); r2.font.name="Times New Roman"
    p3=c1.add_paragraph(); p3.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    r3=p3.add_run("Abidjan — Côte d'Ivoire  ·  +225 07 19 31 49 04  ·  www.lamaisondelaconformitesarl.net")
    r3.font.color.rgb=GREY; r3.font.size=Pt(7.5); r3.font.name="Calibri"
    # double filet navy + or
    p4=h.add_paragraph(); bottom_rule(p4, NAVYHEX, "16"); p4.paragraph_format.space_after=Pt(0)
    p5=h.add_paragraph(); bottom_rule(p5, GOLD_DARK_HEX, "8"); p5.paragraph_format.space_after=Pt(0)

def build_footer(section):
    f=section.footer; f.is_linked_to_previous=False
    rule=f.paragraphs[0]; bottom_rule(rule, GOLD_DARK_HEX, "10")
    lines=["LA MAISON DE LA CONFORMITÉ SARL — NCC : 2506426B — RCCM : CI-ABJ-03-2025-B13-10831 — Capital : 1 000 000 FCFA",
           "Tél : 07 19 31 49 04 — lamaisondelaconformitesarl@outlook.com — www.lamaisondelaconformitesarl.net — Document confidentiel — Secret professionnel"]
    for ln in lines:
        p=f.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        r=p.add_run(ln); r.font.size=Pt(7); r.font.color.rgb=GREY; r.font.name="Calibri"
    pg=f.add_paragraph(); pg.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    rr=pg.add_run("Page "); rr.font.size=Pt(7.5); rr.italic=True; rr.font.color.rgb=NAVY; page_field(pg)

def add_runs(p, text):
    text=sober(text)
    for i,part in enumerate(text.split("**")):
        if part:
            r=p.add_run(part); r.bold=(i%2==1); r.font.name="Times New Roman"; r.font.size=Pt(11)

def looks_amount(s):
    return bool(re.match(r'^[\d\s.,]+$', re.sub(r'\*|FCFA|—|-', '', s).strip())) and any(ch.isdigit() for ch in s)

def render_md(doc, md):
    lines=md.split("\n"); i=0
    while i<len(lines):
        ln=lines[i].rstrip()
        if not ln.strip(): i+=1; continue
        if ln.startswith("### "):
            p=doc.add_paragraph(); r=p.add_run(sober(ln[4:])); r.bold=True; r.font.color.rgb=NAVY; r.font.size=Pt(11.5); r.font.name="Times New Roman"
            p.paragraph_format.space_before=Pt(6)
        elif ln.startswith("## "):
            p=doc.add_paragraph(); r=p.add_run(sober(ln[3:])); r.bold=True; r.font.color.rgb=NAVY; r.font.size=Pt(12.5); r.font.name="Times New Roman"
            p.paragraph_format.space_before=Pt(10); p.paragraph_format.space_after=Pt(1)
            p2=doc.add_paragraph(); rr=p2.add_run("——"); rr.bold=True; rr.font.color.rgb=GOLD_DARK; rr.font.size=Pt(10)
            p2.paragraph_format.space_after=Pt(4)
        elif ln.startswith("# "):
            p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            r=p.add_run(sober(ln[2:])); r.bold=True; r.font.color.rgb=NAVY; r.font.size=Pt(14.5); r.font.name="Times New Roman"
            p2=doc.add_paragraph(); p2.alignment=WD_ALIGN_PARAGRAPH.CENTER
            rr=p2.add_run("———"); rr.bold=True; rr.font.color.rgb=GOLD_DARK; rr.font.size=Pt(11)
            p2.paragraph_format.space_after=Pt(6)
        elif ln.startswith("> "):
            p=doc.add_paragraph()
            pPr=p._p.get_or_add_pPr(); sh=OxmlElement('w:shd')
            sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),'FFFBE8'); pPr.append(sh)
            bdr=OxmlElement('w:pBdr'); lft=OxmlElement('w:left')
            lft.set(qn('w:val'),'single'); lft.set(qn('w:sz'),'18'); lft.set(qn('w:space'),'4'); lft.set(qn('w:color'),GOLD_DARK_HEX)
            bdr.append(lft); pPr.append(bdr)
            p.paragraph_format.left_indent=Pt(8)
            for j,part in enumerate(sober(ln[2:]).split("**")):
                if part:
                    r=p.add_run(part); r.bold=(j%2==1); r.font.color.rgb=NAVY; r.font.name="Times New Roman"
        elif ln.startswith(("- ","* ")):
            p=doc.add_paragraph(style="List Bullet"); add_runs(p, ln[2:])
        elif ln.startswith("|"):
            block=[]
            while i<len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i]); i+=1
            rows=[[c.strip() for c in r.strip().strip("|").split("|")] for r in block if not re.match(r'^\s*\|[\s:\-|]+\|\s*$', r)]
            if rows:
                cols=len(rows[0])
                total_rows=[ri for ri in range(1,len(rows)) if re.search(r'\bTOTAL', sober(rows[ri][0]) or '', re.I)]
                tbl=doc.add_table(rows=0, cols=cols); tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
                for ri,row in enumerate(rows):
                    cells=tbl.add_row().cells
                    for ci,val in enumerate(row[:cols]):
                        cell=cells[ci]; cp=cell.paragraphs[0]; add_runs(cp, val)
                        for rn in cp.runs: rn.font.size=Pt(9.5)
                        amount=ci==cols-1 and (looks_amount(sober(val) or '') or sober(val)=='')
                        if amount and ri>0: cp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
                        if ri==0:
                            shade(cell, NAVYHEX); cell_borders(cell, bottom=(12, GOLD_DARK_HEX))
                            for rn in cp.runs: rn.bold=True; rn.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); rn.font.name="Calibri"
                            if ci==cols-1: cp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
                        else:
                            is_total=ri in total_rows; last=ri==len(rows)-1
                            if is_total: shade(cell,'F5E5A5')
                            cell_borders(cell, bottom=(12,NAVYHEX) if last else (4,'C9C9D2'))
                            for rn in cp.runs:
                                rn.font.color.rgb=NAVY if is_total else INK
                                if is_total: rn.bold=True
            continue
        else:
            p=doc.add_paragraph(); add_runs(p, ln); p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
        i+=1

def main(md_path, dest, titre="LIVRABLE", client="", ref=""):
    doc=Document()
    st=doc.styles["Normal"]; st.font.name="Times New Roman"; st.font.size=Pt(11)
    sec=doc.sections[0]
    sec.top_margin=Cm(4.2); sec.bottom_margin=Cm(2.5); sec.left_margin=Cm(2.0); sec.right_margin=Cm(2.0)
    sec.header_distance=Cm(0.8); sec.footer_distance=Cm(1.0)
    build_header(sec); build_footer(sec)
    # bloc titre navy
    t=doc.add_table(rows=1, cols=1); no_borders(t)
    cell=t.rows[0].cells[0]; shade(cell, NAVYHEX); cell_borders(cell, bottom=(14, GOLD_DARK_HEX))
    p=cell.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run(sober(titre)); r.bold=True; r.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); r.font.size=Pt(14); r.font.name="Times New Roman"
    sub=cell.add_paragraph(); sub.alignment=WD_ALIGN_PARAGRAPH.CENTER
    meta=[]
    if client: meta.append("Client : "+client)
    if ref: meta.append("Réf. : "+ref)
    meta.append("Devise : FCFA · Droit ivoirien & OHADA")
    rs=sub.add_run("   |   ".join(meta)); rs.font.color.rgb=RGBColor(0xE8,0xC5,0x47); rs.font.size=Pt(9.5); rs.font.name="Calibri"
    doc.add_paragraph()
    render_md(doc, Path(md_path).read_text(encoding="utf-8"))
    doc.save(dest); print("OK ->", dest)

if __name__=="__main__":
    a=sys.argv; main(a[1],a[2], a[3] if len(a)>3 else "LIVRABLE", a[4] if len(a)>4 else "", a[5] if len(a)>5 else "")
