#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_detail_ca_achats.py — Génère l'ÉTAT DÉTAILLÉ DU CA et l'ÉTAT DÉTAILLÉ DES ACHATS
à partir d'un GRAND LIVRE Sage 100 exporté en PDF (texte).

RÈGLE MDC : à produire d'office sur CHAQUE dossier disposant d'un grand livre exploitable.
- CA : comptes 70xxxxx (produits / Travaux facturés) → détail des factures émises (date, n°, montant, libellé).
- Achats : comptes 60xxxxx (achats/charges) → détail des factures d'achat, catégorisé.
Si le grand livre n'est pas exploitable (base .mae, factures scannées) → réclamer l'export Excel
du grand livre, ou OCR ; ce script ne traite que le PDF texte Sage.

Usage:
  python3 build_detail_ca_achats.py GRAND_LIVRE.pdf "CLIENT" DEST_DIR [compte_CA=70510000] [comptes_achats=60570000,60571000]
Produit : DEST_DIR/DETAIL_CA_<CLIENT>.xlsx et DETAIL_ACHATS_<CLIENT>.xlsx
"""
import sys, os, re
import fitz, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from collections import defaultdict

if len(sys.argv) < 4:
    print("Usage: build_detail_ca_achats.py GRAND_LIVRE.pdf \"CLIENT\" DEST_DIR [compteCA] [comptesAchats]"); sys.exit(1)
GL, CLIENT, DEST = sys.argv[1], sys.argv[2], sys.argv[3]
CA_ACCTS = (sys.argv[4] if len(sys.argv) > 4 else "70510000").split(",")
ACH_ACCTS = (sys.argv[5] if len(sys.argv) > 5 else "60570000,60571000,60572000").split(",")

NAVY="1F2A44"; bd=Border(*[Side(style="thin",color="B0B0B0")]*4)
DATE=re.compile(r'^\d{6}$'); NUM=re.compile(r'^-?\d{1,3}(?:\.\d{3})*$')
amt=lambda s: NUM.match(s) and ("." in s or s.startswith("-") or len(s.replace('.',''))>=4)
val=lambda s: int(s.replace(".",""))

d=fitz.open(GL); L=[]
for p in range(d.page_count): L+=[x.strip() for x in d[p].get_text().split("\n")]

def parse_account(code):
    idx=[i for i,x in enumerate(L) if x==code]
    if not idx: return []
    seg=L[idx[0]+1:]
    e=[j for j,x in enumerate(seg) if x.startswith("Total compte "+code)]
    seg=seg[:e[0]] if e else seg
    out=[]; i=0
    while i<len(seg):
        if DATE.match(seg[i]):
            dte=seg[i]; nx=i+1
            while nx<len(seg) and not DATE.match(seg[nx]): nx+=1
            toks=seg[i+1:nx]; jr=toks[0] if toks else ""
            piece=next((t for t in toks[1:4] if t.upper().startswith(("VTE","ACH","FAC"))), "")
            m=None
            for t in range(len(toks)-1):
                if amt(toks[t]) and amt(toks[t+1]): m=val(toks[t]); pos=t; break
            if m is not None:
                lib=re.sub(r'\s+',' ', re.sub(r'-?\d[\d\.]*','',' '.join(toks[pos+2:]))).strip()[:50]
                out.append((f"{dte[:2]}/{dte[2:4]}/{dte[4:]}", jr, piece, m, lib))
            i=nx
        else: i+=1
    return out

def cat_achat(l):
    u=l.upper()
    if "APPORTEUR" in u or "COMMISSION" in u: return "Commission / apporteur d'affaires"
    if any(k in u for k in ["LAPTOP","DELL","HP ","SERVEUR","MACBOOK","TABLETTE","GPS","DRONE","IMPRIMANTE","SCANNER","LENOVO","OMNI","RAM","SSD","NAS","CAMERA","CAMÉRA","STARLINK","VSAT","ÉCRAN","ECRAN","UC","KIT"]): return "Matériel informatique / équipement"
    if any(k in u for k in ["RENOUVELLEMENT","CLOUD","OFFICE","GOOGLE","HÉBERG","HEBERG","LICENCE","DOMAINE","ANTIVIRUS","ABONNEMENT","O365","MICROSOFT","VPN","MESSAGERIE"]): return "Abonnements / licences / cloud"
    return "Autres achats & frais"

def header(ws, title, cols):
    ws.merge_cells(start_row=1,start_column=1,end_row=1,end_column=len(cols))
    c=ws.cell(1,1,title); c.font=Font(bold=True,size=12,color=NAVY)
    ws.merge_cells(start_row=2,start_column=1,end_row=2,end_column=len(cols))
    ws.cell(2,1,f"{CLIENT} — source : grand livre — FCFA").font=Font(italic=True,size=9)
    for j,h in enumerate(cols,1):
        x=ws.cell(4,j,h); x.font=Font(bold=True,color="FFFFFF"); x.fill=PatternFill("solid",fgColor=NAVY); x.border=bd; x.alignment=Alignment(horizontal="center",wrap_text=True)

# ---- CA ----
ca=[]
for a in CA_ACCTS: ca+= [r for r in parse_account(a) if r[1]=="VTE" and r[3]>0]
wb=openpyxl.Workbook(); ws=wb.active; ws.title="Détail CA"
header(ws,"ÉTAT DÉTAILLÉ DU CHIFFRE D'AFFAIRES — factures émises",["Date","N°","Objet / libellé","Montant"])
r=5
for dte,jr,pc,mt,lib in sorted(ca,key=lambda x:-x[3]):
    ws.cell(r,1,dte); ws.cell(r,2,pc); ws.cell(r,3,lib); ws.cell(r,4,mt).number_format='#,##0'; ws.cell(r,4).alignment=Alignment(horizontal="right")
    for j in range(1,5): ws.cell(r,j).border=bd; ws.cell(r,j).font=Font(size=9)
    r+=1
ws.cell(r,3,"TOTAL CA FACTURÉ").font=Font(bold=True,color="FFFFFF"); ws.cell(r,4,sum(x[3] for x in ca)).number_format='#,##0'; ws.cell(r,4).font=Font(bold=True,color="FFFFFF")
for j in range(1,5): ws.cell(r,j).fill=PatternFill("solid",fgColor=NAVY); ws.cell(r,j).border=bd
for col,w in zip("ABCD",[12,12,50,16]): ws.column_dimensions[col].width=w
ws.freeze_panes="A5"
out_ca=os.path.join(DEST,f"DETAIL_CA_{CLIENT}.xlsx"); wb.save(out_ca)

# ---- ACHATS ----
ach=[]
for a in ACH_ACCTS: ach+= [r for r in parse_account(a) if r[3]>0]
byc=defaultdict(lambda:[0,0])
for r in ach: byc[cat_achat(r[4])][0]+=r[3]; byc[cat_achat(r[4])][1]+=1
wb2=openpyxl.Workbook(); s=wb2.active; s.title="Synthèse achats"
header(s,"ÉTAT DÉTAILLÉ DES ACHATS — par catégorie",["Catégorie","Nb","Montant"])
r=5
for c,(mt,nb) in sorted(byc.items(),key=lambda x:-x[1][0]):
    s.cell(r,1,c); s.cell(r,2,nb).alignment=Alignment(horizontal="center"); s.cell(r,3,mt).number_format='#,##0'; s.cell(r,3).alignment=Alignment(horizontal="right")
    for j in range(1,4): s.cell(r,j).border=bd
    r+=1
s.cell(r,1,"TOTAL").font=Font(bold=True,color="FFFFFF"); s.cell(r,3,sum(x[3] for x in ach)).number_format='#,##0'; s.cell(r,3).font=Font(bold=True,color="FFFFFF")
for j in range(1,4): s.cell(r,j).fill=PatternFill("solid",fgColor=NAVY); s.cell(r,j).border=bd
for col,w in zip("ABC",[42,10,18]): s.column_dimensions[col].width=w
w2=wb2.create_sheet("Détail achats")
header(w2,"ACHATS — détail ligne à ligne",["Date","Journal","Montant","Libellé"])
r=5
for dte,jr,pc,mt,lib in sorted(ach,key=lambda x:-x[3]):
    w2.cell(r,1,dte); w2.cell(r,2,jr).alignment=Alignment(horizontal="center"); w2.cell(r,3,mt).number_format='#,##0'; w2.cell(r,3).alignment=Alignment(horizontal="right"); w2.cell(r,4,lib)
    for j in range(1,5): w2.cell(r,j).border=bd; w2.cell(r,j).font=Font(size=9)
    r+=1
for col,w in zip("ABCD",[11,9,14,52]): w2.column_dimensions[col].width=w
w2.freeze_panes="A5"
out_ach=os.path.join(DEST,f"DETAIL_ACHATS_{CLIENT}.xlsx"); wb2.save(out_ach)

print(f"OK CA : {len(ca)} factures, total {sum(x[3] for x in ca):,} -> {out_ca}".replace(","," "))
print(f"OK ACHATS : {len(ach)} lignes, total {sum(x[3] for x in ach):,} -> {out_ach}".replace(","," "))
print("→ publier en PDF brandé via xlsx_to_pdf_mdc.py")
