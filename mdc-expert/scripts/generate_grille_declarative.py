#!/usr/bin/env python3
# Générateur de grille déclarative format LERO (MDC) — 1 ou plusieurs exercices.
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

NAVY="1A1A2E"; GOLD="E8C547"; GOLDP="F5E5A5"; PURP="512E5F"
FILLS={
 "D":("27AE60","FFFFFF"), "D*":("E67E22","FFFFFF"), "N":("C0392B","FFFFFF"),
 "TO":("7B241C","FFFFFF"), "—":("BFC9CA","1A1A2E"), "~":("5D6D7E","FFFFFF"),
 "CR":("117A65","FFFFFF"),
}
thin=Side(style="thin",color="C9C9D2"); BORD=Border(left=thin,right=thin,top=thin,bottom=thin)

def cell(ws,r,c,v,fill=None,font=None,align="center",wrap=False):
    x=ws.cell(r,c,v); x.alignment=Alignment(horizontal=align,vertical="center",wrap_text=wrap); x.border=BORD
    if font: x.font=font
    if fill: x.fill=PatternFill("solid",fgColor=fill)
    return x

def build(path, ident, blocks, monthly, annual, note, legende):
    wb=openpyxl.Workbook(); ws=wb.active; ws.title="Grille déclarative"
    allm=[m for _,_,ms in blocks for m in ms]; ncol=1+len(allm); last=get_column_letter(ncol)
    ws.merge_cells(f"A1:{last}1"); cell(ws,1,1,"LA MAISON DE LA CONFORMITÉ SARL — Agence de Notation Administrative · Comptable · Fiscal · Social",fill=NAVY,font=Font(bold=True,color="FFFFFF",size=11))
    ws.merge_cells(f"A2:{last}2"); cell(ws,2,1,"AUDIT DES DÉCLARATIONS — GRILLE COMPLÈTE PAR NATURE D'IMPÔT × PAR PÉRIODE",fill=GOLD,font=Font(bold=True,color="1A1A2E",size=11))
    ws.merge_cells(f"A3:{last}3"); cell(ws,3,1,ident,font=Font(bold=True,size=9))
    ws.merge_cells(f"A4:{last}4"); cell(ws,4,1,legende,align="left",font=Font(italic=True,size=8))
    ws.merge_cells("A5:A6"); cell(ws,5,1,"Nature d'impôt",fill=NAVY,font=Font(bold=True,color="FFFFFF",size=9),wrap=True)
    c=2; blockcols=[]
    for label,color,ms in blocks:
        ws.merge_cells(start_row=5,start_column=c,end_row=5,end_column=c+len(ms)-1)
        cell(ws,5,c,label,fill=color,font=Font(bold=True,color="FFFFFF",size=9))
        for i,m in enumerate(ms): cell(ws,6,c+i,m,fill=color,font=Font(bold=True,color="FFFFFF",size=8))
        blockcols.append((c,len(ms))); c+=len(ms)
    r=7; ws.merge_cells(f"A{r}:{last}{r}"); cell(ws,r,1,"NATURES MENSUELLES",fill=GOLDP,font=Font(bold=True,size=9),align="left"); r+=1
    for nature,codes in monthly:
        cell(ws,r,1,nature,font=Font(bold=True,size=9),align="left")
        for i,code in enumerate(codes):
            bg,fg=FILLS.get(code,("FFFFFF","000000")); cell(ws,r,2+i,code,fill=bg,font=Font(bold=True,size=9,color=fg))
        r+=1
    ws.merge_cells(f"A{r}:{last}{r}"); cell(ws,r,1,"NATURES ANNUELLES / PÉRIODIQUES / OCCASIONNELLES  (statut par exercice)",fill=GOLDP,font=Font(bold=True,size=9),align="left"); r+=1
    for nature,perblock in annual:
        cell(ws,r,1,nature,font=Font(bold=True,size=9),align="left")
        for (c0,n),(txt,col) in zip(blockcols,perblock):
            ws.merge_cells(start_row=r,start_column=c0,end_row=r,end_column=c0+n-1)
            cell(ws,r,c0,txt,fill=col,font=Font(bold=True,size=8,color="FFFFFF"),wrap=True)
        r+=1
    r+=1; ws.merge_cells(f"A{r}:{last}{r+4}"); cell(ws,r,1,note,fill="FFFBE8",font=Font(italic=True,size=8),align="left",wrap=True)
    ws.column_dimensions["A"].width=30
    for cc in range(2,ncol+1): ws.column_dimensions[get_column_letter(cc)].width=6.6
    for rr in range(12,12+len(annual)): ws.row_dimensions[rr].height=26
    ws.sheet_view.showGridLines=False; ws.freeze_panes="B7"
    wb.save(path); print("OK",path)
