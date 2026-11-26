# -*- coding: utf-8 -*-
"""
GÉNÉRATEUR DU CLASSEUR DE DIAGNOSTIC FINANCIER — MDC

Produit un classeur Excel à formules vivantes : la balance SYSCOHADA saisie sur
trois exercices alimente les soldes intermédiaires, le bilan financier, les
ratios des cinq étapes, le score Z'' d'Altman, la indice de santé financière
MDC et la valeur économique ajoutée.

Usage
-----
  python3 build_classeur_diagnostic.py --client "NOM SARL" --secteur "Négoce" \
      --exercice 2025 --out "/chemin/CLIENT_Diagnostic_Financier.xlsx"

  --vierge          classeur vide (tous les postes à zéro) — pour saisie client
  --exemple         classeur pré-rempli avec le cas de démonstration (défaut)
  --json data.json  pré-remplissage depuis {"N-2": {...}, "N-1": {...}, "N": {...}}

Dépendance : openpyxl.
"""

import argparse
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur_diagnostic import POSTES, BAREME, PARAMS_DEFAUT  # noqa: E402

M = 1_000_000

# Cas de démonstration : société de négoce dont le CA progresse mais dont les
# frais financiers absorbent tout le résultat (effet massue).
EXEMPLE = {
    "N-2": dict(v_march=480, a_march=355, var_march=-8, a_mat=6, transp=12, serv=28,
                imp_tax=6, autres_ch=3, pers=42, autres_pr=2, dot=9, fr_fin=6, impot=6,
                im_inc=4, im_cor=115, im_fin=3, amort=41, stock_b=66, stock_d=2,
                cli_b=88, cli_d=4, aut_cr=8, cr_hao=1, banque=3,
                capital=40, reserv=8, ran=8, res_bil=17, emprunt=40, cbail=14,
                prov_risq=2, cca=10, fourn=68, d_fisc=14, d_soc=11, aut_det=2,
                det_hao=1, decouv=6),
    "N-1": dict(v_march=560, a_march=425, var_march=-12, a_mat=7, transp=15, serv=34,
                imp_tax=7, autres_ch=3, pers=52, autres_pr=2, dot=11, fr_fin=10, impot=3,
                im_inc=4, im_cor=128, im_fin=3, amort=51, stock_b=78, stock_d=3,
                cli_b=118, cli_d=6, aut_cr=10, cr_hao=2, banque=11,
                capital=40, reserv=8, ran=25, res_bil=7, emprunt=48, cbail=11,
                prov_risq=2, cca=14, fourn=80, d_fisc=24, d_soc=15, aut_det=3,
                det_hao=2, decouv=15),
    "N": dict(v_march=610, a_march=455, var_march=-18, a_mat=8, transp=18, serv=42,
              imp_tax=9, autres_ch=4, pers=66, autres_pr=3, dot=13, repr=1, fr_fin=17,
              hao=-2, impot=3,
              im_inc=4, im_cor=145, im_fin=3, amort=62, stock_b=96, stock_d=4,
              cli_b=148, cli_d=10, aut_cr=12, cr_hao=2, banque=8,
              capital=40, reserv=8, ran=32, res_bil=-5, emprunt=55, cbail=8,
              prov_risq=3, cca=20, fourn=88, d_fisc=38, d_soc=21, aut_det=3,
              det_hao=3, decouv=28),
}

# ------------------------------------------------------------------ styles
FONT = "Arial"
BLUE = Font(name=FONT, size=10, color="0000FF")
BLACK = Font(name=FONT, size=10)
GREEN = Font(name=FONT, size=10, color="008000")
BOLD = Font(name=FONT, size=10, bold=True)
BOLD_W = Font(name=FONT, size=10, bold=True, color="FFFFFF")
TITLE = Font(name=FONT, size=14, bold=True, color="1F3864")
SUB = Font(name=FONT, size=10, italic=True, color="595959")
H_FILL = PatternFill("solid", fgColor="1F3864")
S_FILL = PatternFill("solid", fgColor="D9E2F3")
Y_FILL = PatternFill("solid", fgColor="FFFF00")
G_FILL = PatternFill("solid", fgColor="F2F2F2")
RED_F = PatternFill("solid", fgColor="FFC7CE")
ORG_F = PatternFill("solid", fgColor="FFEB9C")
GRN_F = PatternFill("solid", fgColor="C6EFCE")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
TOPB = Border(top=Side(style="medium", color="1F3864"))

FMT_F = '#,##0;(#,##0);-'
FMT_P = '0.0%;(0.0%);-'
FMT_X = '0.00"x"'
FMT_J = '0.0" j"'
FMT_MAP = {"pct": FMT_P, "x": FMT_X, "j": FMT_J, "f": FMT_F}


def construire(chemin, identite, donnees, params):
    wb = Workbook()

    def header(ws, title, subtitle, width=8):
        ws["A1"] = title
        ws["A1"].font = TITLE
        ws["A2"] = subtitle
        ws["A2"].font = SUB
        for c in range(1, width + 1):
            ws.cell(row=3, column=c).border = TOPB
        ws.sheet_view.showGridLines = False

    def sect(ws, row, text, last_col=6):
        for c in range(1, last_col + 1):
            ws.cell(row=row, column=c).fill = H_FILL
            ws.cell(row=row, column=c).font = BOLD_W
        ws.cell(row=row, column=1, value=text).font = BOLD_W

    def yr_head(ws, row, cols=("C", "D", "E")):
        for col, lab in zip(cols, ("N-2", "N-1", "N")):
            c = ws[f"{col}{row}"]
            c.value = lab
            c.font = BOLD
            c.fill = S_FILL
            c.alignment = Alignment(horizontal="center")
            c.border = BOX

    # =============================================================== NOTICE
    ws = wb.active
    ws.title = "Notice"
    header(ws, "MDC — Diagnostic financier & notation",
           "La Maison de la Conformité SARL — Diagnostic, mise en conformité et défense en contrôle")
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 106
    notice = [
        ("s", "1. Objet du classeur"),
        ("t", "Diagnostic financier d'une entreprise à partir de sa balance SYSCOHADA, suivant la démarche "
              "en cinq étapes de Pierre Vernimmen : marges → besoin en fonds de roulement et investissements "
              "→ financement → rentabilité → conclusion."),
        ("t", "Sorties : ratios sur trois exercices, score de défaillance Altman Z'', note de conformité "
              "financière MDC (5 niveaux, de Très solide à Critique) et valeur économique ajoutée."),
        ("b", ""),
        ("s", "2. Mode d'emploi"),
        ("t", "1) Onglet Parametres : identité du client, taux d'impôt, coût du capital, base de jours."),
        ("t", "2) Onglet Saisie_Balance : reporter la balance agrégée de trois exercices. SEUL onglet à remplir."),
        ("t", "3) Vérifier les contrôles en bas de la saisie (bilan équilibré / résultat concordant) AVANT toute lecture."),
        ("t", "4) Lire Retraitements, Diagnostic, Creation_Valeur, Score, puis Synthese."),
        ("t", "5) Reporter la ligne du client dans l'onglet Portefeuille pour bâtir vos références sectorielles."),
        ("b", ""),
        ("s", "3. Code couleur"),
        ("c", "Bleu = donnée saisie en dur (à remplir)"),
        ("k", "Noir = formule de calcul (ne pas écraser)"),
        ("g", "Vert = lien vers un autre onglet"),
        ("y", "Fond jaune = hypothèse clé / cellule à renseigner"),
        ("b", ""),
        ("s", "4. Avertissements"),
        ("t", "• Le score Z'' d'Altman est calibré sur des échantillons américains. Ses seuils (1,1 et 2,6) n'ont "
              "aucune validité statistique établie sur des PME ivoiriennes : à utiliser comme classement ordinal "
              "du portefeuille, pas comme probabilité de défaillance."),
        ("t", "• La note financière MDC repose sur un barème et des pondérations fixés à dire d'expert "
              "(onglet Score, cellules bleues) : à recalibrer au fur et à mesure que le portefeuille grossit."),
        ("t", "• Diffuser une note dégradée à des tiers peut accélérer la dégradation du client. À encadrer "
              "contractuellement avant toute communication externe."),
        ("t", "• Ce classeur mesure la SANTÉ FINANCIÈRE. Il ne se substitue pas à la note de conformité "
              "administrative (skill notateur-conformite, domaines A à G) : il la complète."),
    ]
    r = 5
    for kind, txt in notice:
        cell = ws.cell(row=r, column=2, value=txt)
        if kind == "s":
            cell.font = Font(name=FONT, size=11, bold=True, color="1F3864")
        elif kind == "c":
            cell.font = BLUE
        elif kind == "g":
            cell.font = GREEN
        elif kind == "y":
            cell.font = BLACK
            cell.fill = Y_FILL
        else:
            cell.font = BLACK
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 30 if kind == "t" and len(txt) > 110 else 15
        r += 1

    # ============================================================ PARAMETRES
    ws = wb.create_sheet("Parametres")
    header(ws, "Paramètres", "Cellules bleues = à renseigner")
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 60
    P = {}
    plignes = [
        ("SECT", "Identification du dossier", None, None),
        ("client", "Raison sociale", identite["client"], ""),
        ("forme", "Forme juridique", identite["forme"], ""),
        ("secteur", "Secteur d'activité", identite["secteur"], "Sert au regroupement dans l'onglet Portefeuille"),
        ("exo", "Exercice analysé (N)", identite["exercice"], "Année de clôture"),
        ("audit", "Auditeur MDC", identite["auditeur"], "À renseigner"),
        ("SECT", "Hypothèses de calcul", None, None),
        ("is", "Taux d'impôt sur les sociétés", params["taux_is"], "Côte d'Ivoire — IS de droit commun"),
        ("jours", "Base de jours (ratios de rotation)", params["jours"], "360 (usage) ou 365 (Vernimmen)"),
        ("kcp", "Coût des fonds propres exigé", params["cout_fp"],
         "Jugement — pas de bêta boursier pour une société non cotée"),
        ("kd", "Coût de la dette avant impôt", params["cout_dette"], "Taux moyen bancaire constaté sur le dossier"),
        ("SECT", "Normes d'orthodoxie (seuils d'alerte)", None, None),
        ("n_dnebe", "Endettement net / EBE — maximum", 3.0, "Vernimmen, p. 193"),
        ("n_cfi", "Couverture des frais financiers — minimum", 3.0, "Résultat d'exploitation / frais financiers"),
        ("n_auto", "Autonomie financière — minimum", 0.30, "Capitaux propres / total bilan"),
        ("n_cli", "Délai clients — maximum (jours)", 60, "À adapter au secteur"),
        ("n_dfs", "Dettes fiscales et sociales — maximum (jours de CA)", 20,
         "Indicateur avancé de défaillance (score Banque de France)"),
    ]
    r = 5
    for key, label, val, com in plignes:
        if key == "SECT":
            sect(ws, r, label, 3)
            r += 1
            continue
        ws.cell(row=r, column=1, value=label).font = BLACK
        c = ws.cell(row=r, column=2, value=val)
        c.font = BLUE
        c.fill = Y_FILL
        c.border = BOX
        c.alignment = Alignment(horizontal="center")
        if isinstance(val, float) and 0 < val < 1:
            c.number_format = FMT_P
        elif key in ("n_dnebe", "n_cfi"):
            c.number_format = FMT_X
        ws.cell(row=r, column=3, value=com).font = SUB
        P[key] = f"Parametres!$B${r}"
        r += 1

    # ================================================================ SAISIE
    ws = wb.create_sheet("Saisie_Balance")
    header(ws, "Saisie — balance agrégée SYSCOHADA",
           "Reporter les soldes en FCFA. Seul onglet à remplir.")
    ws.column_dimensions["A"].width = 54
    ws.column_dimensions["B"].width = 26
    for col in ("C", "D", "E"):
        ws.column_dimensions[col].width = 17
    S = {}
    r = 5
    section_courante = None
    titres = {"CR": "COMPTE DE RÉSULTAT", "ACTIF": "BILAN — ACTIF", "PASSIF": "BILAN — PASSIF"}
    for cle, lab, cpt, section in POSTES:
        if section != section_courante:
            sect(ws, r, titres[section], 5)
            yr_head(ws, r)
            section_courante = section
            r += 1
        ws.cell(row=r, column=1, value=lab).font = BLACK
        ws.cell(row=r, column=2, value=cpt).font = SUB
        for col, exo in zip(("C", "D", "E"), ("N-2", "N-1", "N")):
            cell = ws[f"{col}{r}"]
            cell.value = float(donnees[exo].get(cle, 0) or 0)
            cell.font = BLUE
            cell.number_format = FMT_F
            cell.border = BOX
        S[cle] = r
        r += 1

    def sa(key, col):
        return f"Saisie_Balance!{col}{S[key]}"

    ctrl_r = r + 1
    sect(ws, ctrl_r, "CONTRÔLES DE COHÉRENCE — à vérifier avant toute lecture", 5)
    ctrl_r += 1
    for col in ("C", "D", "E"):
        ta = (f"({sa('im_inc',col)}+{sa('im_cor',col)}+{sa('im_fin',col)}-{sa('amort',col)}"
              f"+{sa('stock_b',col)}-{sa('stock_d',col)}+{sa('cli_b',col)}-{sa('cli_d',col)}"
              f"+{sa('aut_cr',col)}+{sa('cr_hao',col)}+{sa('titres',col)}+{sa('banque',col)})")
        tp = (f"({sa('capital',col)}+{sa('reserv',col)}+{sa('ran',col)}+{sa('res_bil',col)}"
              f"+{sa('subv_inv',col)}+{sa('prov_regl',col)}+{sa('emprunt',col)}+{sa('cbail',col)}"
              f"+{sa('prov_risq',col)}+{sa('cca',col)}+{sa('fourn',col)}+{sa('d_fisc',col)}"
              f"+{sa('d_soc',col)}+{sa('aut_det',col)}+{sa('det_hao',col)}+{sa('decouv',col)})")
        ws[f"{col}{ctrl_r}"] = f"={ta}"
        ws[f"{col}{ctrl_r+1}"] = f"={tp}"
        ws[f"{col}{ctrl_r+2}"] = f"={col}{ctrl_r}-{col}{ctrl_r+1}"
        for k in range(4):
            cc = ws[f"{col}{ctrl_r+k}"]
            cc.number_format = FMT_F
            cc.font = BLACK
            cc.border = BOX
        ws[f"{col}{ctrl_r+4}"] = (f'=IF(AND(ABS({col}{ctrl_r+2})<1000,ABS({col}{ctrl_r+3})<1000),'
                                  f'"OK","ANOMALIE")')
        ws[f"{col}{ctrl_r+4}"].font = BOLD
        ws[f"{col}{ctrl_r+4}"].alignment = Alignment(horizontal="center")
    for i, lab in enumerate(["Total actif", "Total passif", "Écart bilan (doit être nul)",
                             "Écart résultat : compte de résultat − bilan", "Verdict"]):
        ws.cell(row=ctrl_r + i, column=1, value=lab).font = BOLD if i == 4 else BLACK
    TOT_ACTIF_ROW = ctrl_r
    CTRL_ROW = ctrl_r + 4
    ws.freeze_panes = "C5"

    # ========================================================= RETRAITEMENTS
    ws = wb.create_sheet("Retraitements")
    header(ws, "Retraitements — soldes intermédiaires et bilan financier",
           "Passage de la balance SYSCOHADA aux agrégats Vernimmen. Aucune saisie.")
    ws.column_dimensions["A"].width = 54
    ws.column_dimensions["B"].width = 26
    for col in ("C", "D", "E"):
        ws.column_dimensions[col].width = 17
    R = {}
    r = 5
    sect(ws, r, "SOLDES INTERMÉDIAIRES DE GESTION", 5)
    yr_head(ws, r)
    r += 1
    state = {"r": r}

    def line(key, label, f, note="", bold=False, fmt=FMT_F):
        rr_ = state["r"]
        ws.cell(row=rr_, column=1, value=label).font = BOLD if bold else BLACK
        ws.cell(row=rr_, column=2, value=note).font = SUB
        for col in ("C", "D", "E"):
            c = ws[f"{col}{rr_}"]
            c.value = f(col)
            c.font = BOLD if bold else BLACK
            c.number_format = fmt
            c.border = BOX
            if bold:
                c.fill = G_FILL
        R[key] = rr_
        state["r"] = rr_ + 1

    def rr(key, col):
        return f"{col}{R[key]}"

    line("ca", "Chiffre d'affaires", lambda c: f"={sa('v_march',c)}+{sa('v_prod',c)}",
         "701 + 702 à 706", bold=True)
    line("camv", "Coût d'achat des marchandises vendues",
         lambda c: f"={sa('a_march',c)}+{sa('var_march',c)}", "601 + 6031")
    line("mc", "Marge commerciale", lambda c: f"={sa('v_march',c)}-{rr('camv',c)}", "", bold=True)
    line("prod", "Production de l'exercice",
         lambda c: f"={sa('v_prod',c)}+{sa('prod_imm',c)}", "702 à 706 + 72 + 73")
    line("conso", "Consommations intermédiaires",
         lambda c: f"={sa('a_mat',c)}+{sa('transp',c)}+{sa('serv',c)}", "602-608 + 61 + 62 + 63")
    line("va", "Valeur ajoutée", lambda c: f"={rr('mc',c)}+{rr('prod',c)}-{rr('conso',c)}", "", bold=True)
    line("ebe", "Excédent brut d'exploitation (EBE)",
         lambda c: f"={rr('va',c)}+{sa('subv',c)}-{sa('imp_tax',c)}-{sa('pers',c)}-{sa('autres_ch',c)}",
         "VA + 71 − 64 − 66 − 65", bold=True)
    line("re", "Résultat d'exploitation",
         lambda c: f"={rr('ebe',c)}+{sa('autres_pr',c)}+{sa('repr',c)}-{sa('dot',c)}", "", bold=True)
    line("rf", "Résultat financier", lambda c: f"={sa('rev_fin',c)}-{sa('fr_fin',c)}", "77 − 67")
    line("rao", "Résultat des activités ordinaires", lambda c: f"={rr('re',c)}+{rr('rf',c)}", "", bold=True)
    line("rn", "Résultat net de l'exercice",
         lambda c: f"={rr('rao',c)}+{sa('hao',c)}-{sa('partic',c)}-{sa('impot',c)}", "", bold=True)
    line("caf", "Capacité d'autofinancement (approchée)",
         lambda c: f"={rr('rn',c)}+{sa('dot',c)}-{sa('repr',c)}", "RN + 68 − 78/79", bold=True)
    RN_ROW = R["rn"]

    state["r"] += 1
    sect(ws, state["r"], "BILAN FINANCIER", 5)
    yr_head(ws, state["r"])
    state["r"] += 1
    line("immo", "Immobilisations nettes",
         lambda c: f"={sa('im_inc',c)}+{sa('im_cor',c)}+{sa('im_fin',c)}-{sa('amort',c)}")
    line("bfr_e", "Besoin en fonds de roulement d'exploitation",
         lambda c: (f"=({sa('stock_b',c)}-{sa('stock_d',c)}+{sa('cli_b',c)}-{sa('cli_d',c)}+{sa('aut_cr',c)})"
                    f"-({sa('fourn',c)}+{sa('d_fisc',c)}+{sa('d_soc',c)}+{sa('aut_det',c)})"),
         "Stocks + clients + autres créances − dettes d'exploitation", bold=True)
    line("bfr_h", "Besoin en fonds de roulement hors activités ordinaires",
         lambda c: f"={sa('cr_hao',c)}-{sa('det_hao',c)}")
    line("bfr", "Besoin en fonds de roulement total",
         lambda c: f"={rr('bfr_e',c)}+{rr('bfr_h',c)}", "", bold=True)
    line("ae", "ACTIF ÉCONOMIQUE", lambda c: f"={rr('immo',c)}+{rr('bfr',c)}",
         "Immobilisations nettes + BFR", bold=True)
    line("cp", "Capitaux propres",
         lambda c: (f"={sa('capital',c)}+{sa('reserv',c)}+{sa('ran',c)}+{sa('res_bil',c)}"
                    f"+{sa('subv_inv',c)}+{sa('prov_regl',c)}"), "", bold=True)
    line("tres_a", "Trésorerie actif", lambda c: f"={sa('titres',c)}+{sa('banque',c)}", "50 + 52 + 53 + 57")
    line("dette_b", "Endettement financier brut",
         lambda c: f"={sa('emprunt',c)}+{sa('cbail',c)}+{sa('cca',c)}+{sa('decouv',c)}", "16 + 17 + 462 + 56")
    line("dn", "ENDETTEMENT NET", lambda c: f"={rr('dette_b',c)}-{rr('tres_a',c)}", "", bold=True)
    line("tres_n", "Trésorerie nette", lambda c: f"={rr('tres_a',c)}-{sa('decouv',c)}")
    line("tot_bil", "Total du bilan", lambda c: f"=Saisie_Balance!{c}{TOT_ACTIF_ROW}")
    line("ctrl_ae", "Contrôle : CP + endettement net + provisions − actif économique",
         lambda c: f"={rr('cp',c)}+{rr('dn',c)}+{sa('prov_risq',c)}-{rr('ae',c)}", "Doit être nul")
    for col in ("C", "D", "E"):
        ws[f"{col}{R['ctrl_ae']}"].font = BOLD
    ws.freeze_panes = "C5"

    wsS = wb["Saisie_Balance"]
    for col in ("C", "D", "E"):
        wsS[f"{col}{CTRL_ROW-1}"] = f"=Retraitements!{col}{RN_ROW}-{sa('res_bil',col)}"
        wsS[f"{col}{CTRL_ROW-1}"].font = GREEN
        wsS[f"{col}{CTRL_ROW-1}"].number_format = FMT_F

    # ============================================================= DIAGNOSTIC
    ws = wb.create_sheet("Diagnostic")
    header(ws, "Diagnostic financier en 5 étapes",
           "Démarche Vernimmen : marges → BFR → financement → rentabilité → conclusion")
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 24
    for col in ("C", "D", "E"):
        ws.column_dimensions[col].width = 15
    ws.column_dimensions["F"].width = 16
    ws.column_dimensions["G"].width = 46
    D = {}
    st = {"r": 5}

    def dline(key, label, f, fmt=FMT_P, alert=None, note="", comment=""):
        rr_ = st["r"]
        ws.cell(row=rr_, column=1, value=label).font = BLACK
        ws.cell(row=rr_, column=2, value=note).font = SUB
        for col in ("C", "D", "E"):
            c = ws[f"{col}{rr_}"]
            c.value = f(col)
            c.font = BLACK
            c.number_format = fmt
            c.border = BOX
        if alert:
            a = ws[f"F{rr_}"]
            # une cellule vide (ratio non calculable) ne doit jamais produire d'alerte :
            # en Excel, "" >= 0,08 vaut VRAI, ce qui afficherait « OK » sur un classeur vierge.
            brut = alert(rr_).lstrip("=")
            a.value = f'=IF(NOT(ISNUMBER(E{rr_})),"—",{brut})'
            a.font = BOLD
            a.alignment = Alignment(horizontal="center")
            a.border = BOX
        ws.cell(row=rr_, column=7, value=comment).font = SUB
        D[key] = rr_
        st["r"] = rr_ + 1

    def dhead(title):
        rr_ = st["r"]
        sect(ws, rr_, title, 7)
        yr_head(ws, rr_)
        ws[f"F{rr_}"].value = "Alerte (N)"
        ws[f"F{rr_}"].font = BOLD_W
        ws[f"F{rr_}"].alignment = Alignment(horizontal="center")
        ws[f"G{rr_}"].value = "Lecture"
        ws[f"G{rr_}"].font = BOLD_W
        st["r"] = rr_ + 1

    JOURS = P["jours"]
    prev = lambda c: chr(ord(c) - 1)

    dhead("ÉTAPE 1 — L'entreprise crée-t-elle de la richesse ? (analyse des marges)")
    dline("croiss", "Croissance du chiffre d'affaires",
          lambda c: ('=""' if c == "C" else
                     f"=IFERROR(Retraitements!{c}{R['ca']}/Retraitements!{prev(c)}{R['ca']}-1,\"\")"),
          comment="Le CA progresse-t-il ?")
    dline("t_mc", "Taux de marge commerciale",
          lambda c: f"=IFERROR(Retraitements!{c}{R['mc']}/Retraitements!{c}{R['ca']},\"\")",
          comment="Marge commerciale / CA")
    dline("t_va", "Taux de valeur ajoutée",
          lambda c: f"=IFERROR(Retraitements!{c}{R['va']}/Retraitements!{c}{R['ca']},\"\")",
          comment="Degré d'intégration de l'activité")
    dline("t_ebe", "Taux d'EBE (marge d'exploitation brute)",
          lambda c: f"=IFERROR(Retraitements!{c}{R['ebe']}/Retraitements!{c}{R['ca']},\"\")",
          alert=lambda w: f'=IF(E{w}>=0.08,"OK",IF(E{w}>=0.04,"Vigilance","ALERTE"))',
          comment="Indicateur central de la rentabilité d'exploitation")
    dline("t_re", "Taux de résultat d'exploitation",
          lambda c: f"=IFERROR(Retraitements!{c}{R['re']}/Retraitements!{c}{R['ca']},\"\")")
    dline("t_pers", "Poids des charges de personnel / CA",
          lambda c: f"=IFERROR({sa('pers',c)}/Retraitements!{c}{R['ca']},\"\")")
    dline("ciseau", "Effet de ciseau : croissance des charges − croissance du CA",
          lambda c: ('=""' if c == "C" else
                     f"=IFERROR(({sa('a_march',c)}+{sa('var_march',c)}+Retraitements!{c}{R['conso']}+{sa('pers',c)})/"
                     f"({sa('a_march',prev(c))}+{sa('var_march',prev(c))}+Retraitements!{prev(c)}{R['conso']}"
                     f"+{sa('pers',prev(c))})-Retraitements!{c}{R['ca']}/Retraitements!{prev(c)}{R['ca']},\"\")"),
          alert=lambda w: f'=IF(E{w}<=0,"OK",IF(E{w}<=0.02,"Vigilance","ALERTE"))',
          comment="Positif = les charges progressent plus vite que le CA")
    dline("cvar", "Charges variables (convention : achats + transports)",
          lambda c: f"={sa('a_march',c)}+{sa('var_march',c)}+{sa('a_mat',c)}+{sa('transp',c)}",
          fmt=FMT_F, comment="Convention à ajuster selon le secteur")
    dline("cfix", "Charges fixes nettes (services ext. + personnel + impôts + dotations + frais fin. − autres produits)",
          lambda c: (f"={sa('serv',c)}+{sa('pers',c)}+{sa('imp_tax',c)}+{sa('autres_ch',c)}+{sa('dot',c)}"
                     f"+{sa('fr_fin',c)}-{sa('autres_pr',c)}-{sa('repr',c)}-{sa('subv',c)}"),
          fmt=FMT_F, comment="Point mort financier : frais financiers inclus")
    dline("pmort", "Point mort (chiffre d'affaires critique)",
          lambda c: f"=IFERROR({c}{D['cfix']}/(1-{c}{D['cvar']}/Retraitements!{c}{R['ca']}),\"\")",
          fmt=FMT_F, comment="CA en deçà duquel l'entreprise perd de l'argent")
    dline("marge_sec", "Marge de sécurité (CA − point mort) / CA",
          lambda c: f"=IFERROR((Retraitements!{c}{R['ca']}-{c}{D['pmort']})/Retraitements!{c}{R['ca']},\"\")",
          alert=lambda w: f'=IF(E{w}>=0.15,"OK",IF(E{w}>=0.05,"Vigilance","ALERTE"))',
          comment="Coussin avant le point mort")

    st["r"] += 1
    dhead("ÉTAPE 2 — Cette richesse exige des investissements (BFR et immobilisations)")
    dline("bfr_j", "BFR d'exploitation en jours de chiffre d'affaires",
          lambda c: f"=IFERROR(Retraitements!{c}{R['bfr_e']}/Retraitements!{c}{R['ca']}*{JOURS},\"\")",
          fmt=FMT_J, alert=lambda w: f'=IF(E{w}<=45,"OK",IF(E{w}<=75,"Vigilance","ALERTE"))',
          comment="Trésorerie immobilisée par le cycle d'exploitation")
    dline("d_cli", "Délai de recouvrement clients",
          lambda c: f"=IFERROR(({sa('cli_b',c)}-{sa('cli_d',c)})/Retraitements!{c}{R['ca']}*{JOURS},\"\")",
          fmt=FMT_J,
          alert=lambda w: f'=IF(E{w}<={P["n_cli"]},"OK",IF(E{w}<={P["n_cli"]}*1.5,"Vigilance","ALERTE"))',
          comment="Un allongement = risque d'impayés ou CA fictif")
    dline("d_stk", "Délai d'écoulement des stocks",
          lambda c: f"=IFERROR(({sa('stock_b',c)}-{sa('stock_d',c)})/Retraitements!{c}{R['camv']}*{JOURS},\"\")",
          fmt=FMT_J, alert=lambda w: f'=IF(E{w}<=60,"OK",IF(E{w}<=90,"Vigilance","ALERTE"))',
          comment="Stock dormant, ou stock fictif gonflant le résultat")
    dline("d_frn", "Délai de règlement fournisseurs",
          lambda c: f"=IFERROR({sa('fourn',c)}/({sa('a_march',c)}+{sa('a_mat',c)}+{sa('serv',c)})*{JOURS},\"\")",
          fmt=FMT_J, alert=lambda w: f'=IF(E{w}<=60,"OK",IF(E{w}<=90,"Vigilance","ALERTE"))',
          comment="Son allongement est un signal avancé de défaillance")
    dline("d_dfs", "Dettes fiscales et sociales en jours de CA",
          lambda c: f"=IFERROR(({sa('d_fisc',c)}+{sa('d_soc',c)})/Retraitements!{c}{R['ca']}*{JOURS},\"\")",
          fmt=FMT_J,
          alert=lambda w: f'=IF(E{w}<={P["n_dfs"]},"OK",IF(E{w}<={P["n_dfs"]}*2,"Vigilance","ALERTE"))',
          comment="Cœur de cible MDC : exposition fiscale ET signal de défaillance")
    dline("invest", "Investissements de l'exercice (variation des immobilisations brutes)",
          lambda c: ('=""' if c == "C" else
                     f"=({sa('im_inc',c)}+{sa('im_cor',c)}+{sa('im_fin',c)})"
                     f"-({sa('im_inc',prev(c))}+{sa('im_cor',prev(c))}+{sa('im_fin',prev(c))})"),
          fmt=FMT_F, comment="Approximation : hors cessions")

    st["r"] += 1
    dhead("ÉTAPE 3 — Ces investissements doivent être financés")
    dline("gearing", "Levier financier (endettement net / capitaux propres)",
          lambda c: f"=IFERROR(Retraitements!{c}{R['dn']}/Retraitements!{c}{R['cp']},\"\")", fmt=FMT_X,
          alert=lambda w: f'=IF(E{w}<=1,"OK",IF(E{w}<=2,"Vigilance","ALERTE"))', comment="Gearing")
    dline("dn_ebe", "Endettement net / EBE",
          lambda c: f"=IFERROR(Retraitements!{c}{R['dn']}/Retraitements!{c}{R['ebe']},\"\")", fmt=FMT_X,
          alert=lambda w: f'=IF(E{w}<={P["n_dnebe"]},"OK",IF(E{w}<={P["n_dnebe"]}*1.5,"Vigilance","ALERTE"))',
          comment="Norme d'orthodoxie : 3x maximum")
    dline("cfi", "Couverture des frais financiers (résultat d'exploitation / frais fin.)",
          lambda c: f"=IFERROR(Retraitements!{c}{R['re']}/{sa('fr_fin',c)},\"\")", fmt=FMT_X,
          alert=lambda w: f'=IF(E{w}>={P["n_cfi"]},"OK",IF(E{w}>=1.5,"Vigilance","ALERTE"))',
          comment="Sous 1x, l'exploitation ne paie plus la banque")
    dline("caf_dn", "CAF / endettement net (capacité de remboursement)",
          lambda c: f"=IFERROR(Retraitements!{c}{R['caf']}/Retraitements!{c}{R['dn']},\"\")",
          comment="Inverse du nombre d'années de remboursement")
    dline("auto", "Autonomie financière (capitaux propres / total bilan)",
          lambda c: f"=IFERROR(Retraitements!{c}{R['cp']}/Retraitements!{c}{R['tot_bil']},\"\")",
          alert=lambda w: f'=IF(E{w}>={P["n_auto"]},"OK",IF(E{w}>={P["n_auto"]}/2,"Vigilance","ALERTE"))')
    dline("cp_cap", "Capitaux propres / capital social (art. 371 AUSCGIE)",
          lambda c: f"=IFERROR(Retraitements!{c}{R['cp']}/{sa('capital',c)},\"\")",
          alert=lambda w: f'=IF(E{w}>=1,"OK",IF(E{w}>=0.5,"Vigilance","ALERTE"))',
          comment="Sous 50 %, régularisation obligatoire (AG dans les 4 mois)")
    dline("ct_dette", "Part de l'endettement à court terme (découverts / dette brute)",
          lambda c: f"=IFERROR({sa('decouv',c)}/Retraitements!{c}{R['dette_b']},\"\")",
          alert=lambda w: f'=IF(E{w}<=0.2,"OK",IF(E{w}<=0.4,"Vigilance","ALERTE"))',
          comment="Financer le long terme par du découvert = risque de liquidité")
    dline("tres_ca", "Trésorerie nette en jours de CA",
          lambda c: f"=IFERROR(Retraitements!{c}{R['tres_n']}/Retraitements!{c}{R['ca']}*{JOURS},\"\")",
          fmt=FMT_J, alert=lambda w: f'=IF(E{w}>=0,"OK",IF(E{w}>=-15,"Vigilance","ALERTE"))')

    st["r"] += 1
    dhead("ÉTAPE 4 — Et être suffisamment rentables (effet de levier)")
    dline("re_eco", "Rentabilité économique après impôt (Re)",
          lambda c: f"=IFERROR(Retraitements!{c}{R['re']}*(1-{P['is']})/Retraitements!{c}{R['ae']},\"\")",
          comment="Résultat d'exploitation après impôt / actif économique")
    dline("i_dette", "Coût apparent de la dette après impôt (i)",
          lambda c: f"=IFERROR({sa('fr_fin',c)}*(1-{P['is']})/Retraitements!{c}{R['dn']},\"\")",
          comment="Frais financiers après impôt / endettement net")
    dline("levier", "Effet de levier = (Re − i) × D/CP",
          lambda c: (f"=IFERROR(({c}{D['re_eco']}-{c}{D['i_dette']})*Retraitements!{c}{R['dn']}"
                     f"/Retraitements!{c}{R['cp']},\"\")"),
          alert=lambda w: f'=IF(E{w}>=0,"OK","EFFET MASSUE")',
          comment="Négatif : l'endettement détruit la rentabilité des associés")
    dline("roe_th", "Rentabilité des capitaux propres théorique (Re + effet de levier)",
          lambda c: f"=IFERROR({c}{D['re_eco']}+{c}{D['levier']},\"\")")
    dline("roe_re", "Rentabilité des capitaux propres constatée (RN / CP)",
          lambda c: f"=IFERROR(Retraitements!{c}{R['rn']}/Retraitements!{c}{R['cp']},\"\")",
          alert=lambda w: f'=IF(E{w}>=0,"OK","PERTE")')
    dline("ecart_roe", "Écart (éléments HAO, IMF, non-récurrents)",
          lambda c: f"=IFERROR({c}{D['roe_re']}-{c}{D['roe_th']},\"\")",
          comment="L'effet de levier est une identité comptable : l'écart vient du hors-exploitation")

    st["r"] += 1
    dhead("ÉTAPE 5 — Conclusion : création de valeur et solvabilité")
    dline("cmpc_d", "Coût moyen pondéré du capital (CMPC)",
          lambda c: '=""', comment="Calculé dans l'onglet Creation_Valeur")
    dline("spread", "Spread : rentabilité économique − coût du capital",
          lambda c: f"=IFERROR({c}{D['re_eco']}-{c}{D['cmpc_d']},\"\")",
          alert=lambda w: (f'=IF(NOT(ISNUMBER(E{w})),"—",'
                           f'IF(E{w}>=0,"CRÉE DE LA VALEUR","DÉTRUIT DE LA VALEUR"))'),
          comment="Le juge de paix : rentabilité dégagée vs rentabilité exigée")
    DIAG_LAST = st["r"]
    ws.freeze_panes = "C5"

    # ======================================================= CREATION_VALEUR
    ws = wb.create_sheet("Creation_Valeur")
    header(ws, "Création de valeur — VEA et coût du capital",
           "Un bénéfice comptable positif peut masquer une destruction de valeur")
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 26
    for col in ("C", "D", "E"):
        ws.column_dimensions[col].width = 17
    V = {}
    sv = {"r": 5}
    sect(ws, sv["r"], "COÛT MOYEN PONDÉRÉ DU CAPITAL", 5)
    yr_head(ws, sv["r"])
    sv["r"] += 1

    def vline(key, label, f, fmt=FMT_F, note="", bold=False):
        rr_ = sv["r"]
        ws.cell(row=rr_, column=1, value=label).font = BOLD if bold else BLACK
        ws.cell(row=rr_, column=2, value=note).font = SUB
        for col in ("C", "D", "E"):
            c = ws[f"{col}{rr_}"]
            c.value = f(col)
            c.font = BOLD if bold else BLACK
            c.number_format = fmt
            c.border = BOX
            if bold:
                c.fill = G_FILL
        V[key] = rr_
        sv["r"] = rr_ + 1

    vline("cp_v", "Capitaux propres", lambda c: f"=Retraitements!{c}{R['cp']}")
    vline("dn_v", "Endettement net", lambda c: f"=Retraitements!{c}{R['dn']}")
    vline("tot_v", "Capitaux engagés", lambda c: f"={c}{V['cp_v']}+{c}{V['dn_v']}", bold=True)
    vline("w_cp", "Poids des fonds propres", lambda c: f"=IFERROR({c}{V['cp_v']}/{c}{V['tot_v']},\"\")", fmt=FMT_P)
    vline("w_d", "Poids de la dette", lambda c: f"=IFERROR({c}{V['dn_v']}/{c}{V['tot_v']},\"\")", fmt=FMT_P)
    vline("kcp_v", "Coût des fonds propres exigé", lambda c: f"={P['kcp']}", fmt=FMT_P, note="Paramètres")
    vline("kd_v", "Coût de la dette après impôt", lambda c: f"={P['kd']}*(1-{P['is']})", fmt=FMT_P)
    vline("cmpc", "CMPC",
          lambda c: f"=IFERROR({c}{V['kcp_v']}*{c}{V['w_cp']}+{c}{V['kd_v']}*{c}{V['w_d']},\"\")",
          fmt=FMT_P, bold=True)

    sv["r"] += 1
    sect(ws, sv["r"], "VALEUR ÉCONOMIQUE AJOUTÉE (VEA)", 5)
    yr_head(ws, sv["r"])
    sv["r"] += 1
    vline("bneai", "Résultat d'exploitation après impôt (BNEAI)",
          lambda c: f"=Retraitements!{c}{R['re']}*(1-{P['is']})")
    vline("ci", "Capital investi (actif économique)", lambda c: f"=Retraitements!{c}{R['ae']}")
    vline("cout_opp", "Coût d'opportunité du capital (CMPC × capital investi)",
          lambda c: f"=IFERROR({c}{V['cmpc']}*{c}{V['ci']},\"\")")
    vline("vea", "VALEUR ÉCONOMIQUE AJOUTÉE",
          lambda c: f"=IFERROR({c}{V['bneai']}-{c}{V['cout_opp']},\"\")", bold=True)
    vline("verdict", "Verdict",
          lambda c: (f'=IF(NOT(ISNUMBER({c}{V["vea"]})),"—",'
                     f'IF({c}{V["vea"]}>=0,"Création de valeur","DESTRUCTION DE VALEUR"))'),
          fmt="General", bold=True)
    vline("rn_cmp", "Pour mémoire : résultat net comptable", lambda c: f"=Retraitements!{c}{R['rn']}")

    ws.cell(row=sv["r"] + 1, column=1,
            value="Lecture : une entreprise peut afficher un résultat net comptable positif tout en détruisant "
                  "de la valeur, parce que la comptabilité traite les fonds propres comme gratuits.").font = SUB
    sv["r"] += 3
    sect(ws, sv["r"], "SENSIBILITÉ DE LA VEA (exercice N)", 6)
    sv["r"] += 2
    ws.cell(row=sv["r"], column=1, value="Coût des fonds propres →").font = SUB
    kcp_vals = [0.12, 0.15, 0.18, 0.21, 0.24]
    for j, k in enumerate(kcp_vals):
        c = ws.cell(row=sv["r"], column=2 + j, value=k)
        c.font = BOLD
        c.number_format = FMT_P
        c.fill = S_FILL
        c.alignment = Alignment(horizontal="center")
        c.border = BOX
    sens_head = sv["r"]
    sv["r"] += 1
    ws.cell(row=sv["r"], column=1, value="Variation du résultat d'exploitation ↓").font = SUB
    sv["r"] += 1
    for i, v in enumerate([-0.30, -0.15, 0.0, 0.15, 0.30]):
        rowi = sv["r"] + i
        lab = ws.cell(row=rowi, column=1, value=v)
        lab.number_format = '+0%;-0%;0%'
        lab.font = BOLD
        lab.fill = S_FILL
        lab.alignment = Alignment(horizontal="center")
        lab.border = BOX
        for j in range(len(kcp_vals)):
            col = get_column_letter(2 + j)
            cell = ws.cell(row=rowi, column=2 + j)
            cell.value = (f"=IFERROR(Retraitements!$E${R['re']}*(1+$A{rowi})*(1-{P['is']})"
                          f"-({col}${sens_head}*$E${V['w_cp']}+$E${V['kd_v']}*$E${V['w_d']})"
                          f"*Retraitements!$E${R['ae']},\"\")")
            cell.number_format = FMT_F
            cell.font = BLACK
            cell.border = BOX

    wsD = wb["Diagnostic"]
    for col in ("C", "D", "E"):
        wsD[f"{col}{D['cmpc_d']}"] = f"=Creation_Valeur!{col}{V['cmpc']}"
        wsD[f"{col}{D['cmpc_d']}"].font = GREEN
        wsD[f"{col}{D['cmpc_d']}"].number_format = FMT_P

    # ================================================================= SCORE
    ws = wb.create_sheet("Score")
    header(ws, "Score de défaillance & indice de santé financière MDC",
           "Altman Z'' (référence académique) + note MDC pondérée (à calibrer sur votre portefeuille)")
    ws.column_dimensions["A"].width = 50
    ws.column_dimensions["B"].width = 12
    for col in "CDEFGH":
        ws.column_dimensions[col].width = 14
    ws.column_dimensions["I"].width = 46
    r = 5
    sect(ws, r, "1. SCORE Z'' D'ALTMAN", 9)
    yr_head(ws, r)
    ws[f"I{r}"] = "Définition"
    ws[f"I{r}"].font = BOLD_W
    r += 1
    Z = {}
    alt = [
        ("x1", "X1 — Fonds de roulement net / total actif", 6.56,
         lambda c: (f"=IFERROR((({sa('stock_b',c)}-{sa('stock_d',c)}+{sa('cli_b',c)}-{sa('cli_d',c)}"
                    f"+{sa('aut_cr',c)}+{sa('cr_hao',c)}+Retraitements!{c}{R['tres_a']})"
                    f"-({sa('fourn',c)}+{sa('d_fisc',c)}+{sa('d_soc',c)}+{sa('aut_det',c)}"
                    f"+{sa('det_hao',c)}+{sa('decouv',c)}))/Retraitements!{c}{R['tot_bil']},0)"),
         "Working capital = actif circulant + trésorerie − passif circulant − découverts. "
         "À NE PAS confondre avec le BFR."),
        ("x2", "X2 — Réserves et report à nouveau / total actif", 3.26,
         lambda c: f"=IFERROR(({sa('reserv',c)}+{sa('ran',c)})/Retraitements!{c}{R['tot_bil']},0)",
         "Bénéfices accumulés non distribués."),
        ("x3", "X3 — Résultat d'exploitation / total actif", 6.72,
         lambda c: f"=IFERROR(Retraitements!{c}{R['re']}/Retraitements!{c}{R['tot_bil']},0)",
         "Rentabilité de l'outil, indépendamment du financement."),
        ("x4", "X4 — Capitaux propres / dettes totales", 1.05,
         lambda c: (f"=IFERROR(Retraitements!{c}{R['cp']}/(Retraitements!{c}{R['tot_bil']}"
                    f"-Retraitements!{c}{R['cp']}),0)"),
         "Coussin de fonds propres face aux créanciers."),
    ]
    for key, lab, coef, f, definition in alt:
        ws.cell(row=r, column=1, value=lab).font = BLACK
        b = ws.cell(row=r, column=2, value=coef)
        b.font = BLUE
        b.fill = Y_FILL
        b.border = BOX
        b.alignment = Alignment(horizontal="center")
        for col in ("C", "D", "E"):
            c = ws[f"{col}{r}"]
            c.value = f(col)
            c.number_format = '0.000'
            c.font = BLACK
            c.border = BOX
        ws.cell(row=r, column=9, value=definition).font = SUB
        Z[key] = r
        r += 1
    ws.cell(row=r, column=1, value="Z'' = 6,56 X1 + 3,26 X2 + 6,72 X3 + 1,05 X4").font = BOLD
    for col in ("C", "D", "E"):
        c = ws[f"{col}{r}"]
        c.value = (f"=$B${Z['x1']}*{col}{Z['x1']}+$B${Z['x2']}*{col}{Z['x2']}"
                   f"+$B${Z['x3']}*{col}{Z['x3']}+$B${Z['x4']}*{col}{Z['x4']}")
        c.number_format = '0.00'
        c.font = BOLD
        c.fill = G_FILL
        c.border = BOX
    Z["z"] = r
    r += 1
    ws.cell(row=r, column=1, value="Zone").font = BOLD
    for col in ("C", "D", "E"):
        c = ws[f"{col}{r}"]
        c.value = (f'=IF({col}{Z["z"]}<1.1,"Zone de défaillance",'
                   f'IF({col}{Z["z"]}<=2.6,"Zone grise","Zone saine"))')
        c.font = BOLD
        c.alignment = Alignment(horizontal="center")
        c.border = BOX
    Z["zone"] = r
    r += 1
    ws.cell(row=r, column=1,
            value="Seuils d'origine : Z'' < 1,1 défaillance probable · 1,1 à 2,6 zone grise · > 2,6 saine. "
                  "Calibrés sur échantillon américain — à traiter comme un classement, pas une probabilité.").font = SUB
    r += 2

    sect(ws, r, "2. INDICE DE SANTÉ FINANCIÈRE MDC", 9)
    r += 1
    for j, h in enumerate(["Critère", "Poids", "Seuil bon", "Seuil moyen", "Valeur N",
                           "Note /100", "Contribution", "", "Commentaire"]):
        c = ws.cell(row=r, column=1 + j, value=h)
        c.font = BOLD
        c.fill = S_FILL
        c.border = BOX
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    r += 1
    first_crit = r
    commentaires = {
        "t_ebe": "Capacité du modèle à dégager de la marge",
        "cfi": "Sous 1x, l'exploitation ne paie plus la banque",
        "dn_ebe": "Norme d'orthodoxie : 3x maximum",
        "auto": "Solidité de la structure",
        "d_dfs": "Critère MDC : exposition fiscale et signal de défaillance",
        "d_frn": "Son allongement précède la cessation de paiements",
        "ct_dette": "Risque de liquidité / transformation",
    }
    for cle, lib, poids, s_bon, s_moy, sens, fmt_k in BAREME:
        fmt_c = FMT_MAP[fmt_k]
        ws.cell(row=r, column=1, value=lib).font = BLACK
        for col_i, val, fmt_v in ((2, poids, FMT_P), (3, s_bon, fmt_c), (4, s_moy, fmt_c)):
            c = ws.cell(row=r, column=col_i, value=val)
            c.font = BLUE
            c.fill = Y_FILL
            c.border = BOX
            c.alignment = Alignment(horizontal="center")
            c.number_format = fmt_v
        v = ws.cell(row=r, column=5, value=f"=Diagnostic!E{D[cle]}")
        v.font = GREEN
        v.number_format = fmt_c
        v.border = BOX
        op = ">=" if sens == "sup" else "<="
        n = ws.cell(row=r, column=6, value=f'=IF(E{r}{op}C{r},100,IF(E{r}{op}D{r},50,0))')
        n.font = BLACK
        n.border = BOX
        n.alignment = Alignment(horizontal="center")
        ct = ws.cell(row=r, column=7, value=f"=B{r}*F{r}")
        ct.font = BLACK
        ct.number_format = '0.0'
        ct.border = BOX
        ws.cell(row=r, column=9, value=commentaires.get(cle, "")).font = SUB
        r += 1
    last_crit = r - 1
    ws.cell(row=r, column=1, value="Total").font = BOLD
    tw = ws.cell(row=r, column=2, value=f"=SUM(B{first_crit}:B{last_crit})")
    tw.number_format = FMT_P
    tw.font = BOLD
    tw.border = BOX
    sc = ws.cell(row=r, column=7, value=f"=SUM(G{first_crit}:G{last_crit})")
    sc.font = BOLD
    sc.number_format = '0.0'
    sc.fill = G_FILL
    sc.border = BOX
    SCORE_ROW = r
    r += 1
    ws.cell(row=r, column=1, value="INDICE DE SANTÉ FINANCIÈRE MDC").font = BOLD
    nt = ws.cell(row=r, column=7,
                 value=f'=IF(Retraitements!E{R["ca"]}=0,"—",'
                       f'IF(G{SCORE_ROW}>=85,"Très solide",IF(G{SCORE_ROW}>=70,"Solide",'
                       f'IF(G{SCORE_ROW}>=55,"À surveiller",IF(G{SCORE_ROW}>=40,"Fragile","Critique")))))')
    nt.font = Font(name=FONT, size=14, bold=True, color="C00000")
    nt.alignment = Alignment(horizontal="center")
    nt.border = BOX
    NOTE_ROW = r
    r += 2
    ws.cell(row=r, column=1,
            value="Niveaux : Très solide ≥ 85 · Solide ≥ 70 · À surveiller ≥ 55 · Fragile ≥ 40 · Critique < 40").font = SUB
    r += 1
    ws.cell(row=r, column=1,
            value="Poids et seuils (cellules bleues) fixés à dire d'expert. Recalibrez-les dès que l'onglet "
                  "Portefeuille contient assez de dossiers pour dégager des médianes sectorielles.").font = SUB

    # ========================================================== PORTEFEUILLE
    ws = wb.create_sheet("Portefeuille")
    header(ws, "Portefeuille MDC — construction de vos références sectorielles",
           "Une ligne par dossier. Les médianes deviennent votre benchmark.")
    cols = ["Client", "Secteur", "Exercice", "CA (FCFA)", "Taux d'EBE", "Délai clients (j)",
            "Délai fournisseurs (j)", "BFR (j de CA)", "DFS (j de CA)", "Gearing",
            "Couverture frais fin.", "Score Z''", "Note MDC"]
    widths = [26, 20, 10, 16, 11, 13, 15, 13, 13, 10, 14, 10, 10]
    for j, (h, w) in enumerate(zip(cols, widths)):
        c = ws.cell(row=5, column=1 + j, value=h)
        c.font = BOLD_W
        c.fill = H_FILL
        c.alignment = Alignment(horizontal="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(1 + j)].width = w
    ws.row_dimensions[5].height = 30
    liens = [f"={P['client']}", f"={P['secteur']}", f"={P['exo']}",
             f"=Retraitements!E{R['ca']}", f"=Diagnostic!E{D['t_ebe']}",
             f"=Diagnostic!E{D['d_cli']}", f"=Diagnostic!E{D['d_frn']}",
             f"=Diagnostic!E{D['bfr_j']}", f"=Diagnostic!E{D['d_dfs']}",
             f"=Diagnostic!E{D['gearing']}", f"=Diagnostic!E{D['cfi']}",
             f"=Score!E{Z['z']}", f"=Score!G{NOTE_ROW}"]
    for j, f in enumerate(liens):
        c = ws.cell(row=6, column=1 + j, value=f)
        c.font = GREEN
        c.border = BOX
    for col, f in (("D", FMT_F), ("E", FMT_P), ("F", FMT_J), ("G", FMT_J), ("H", FMT_J),
                   ("I", FMT_J), ("J", FMT_X), ("K", FMT_X), ("L", '0.00')):
        ws[f"{col}6"].number_format = f
    ws["C6"].number_format = "0"
    for row_ in range(7, 41):
        for j in range(13):
            cc = ws.cell(row=row_, column=1 + j)
            cc.border = BOX
            cc.font = BLUE
    ws.cell(row=42, column=1, value="Médiane du portefeuille").font = BOLD
    ws.cell(row=43, column=1, value="Moyenne du secteur saisi en B44").font = BOLD
    ws["B44"] = identite["secteur"]
    ws["B44"].font = BLUE
    ws["B44"].fill = Y_FILL
    ws["B44"].border = BOX
    for col in "DEFGHIJKL":
        m = ws[f"{col}42"]
        m.value = f"=IFERROR(MEDIAN({col}6:{col}40),\"\")"
        m.font = BOLD
        m.fill = G_FILL
        m.border = BOX
        a = ws[f"{col}43"]
        a.value = f"=IFERROR(AVERAGEIF($B$6:$B$40,$B$44,{col}6:{col}40),\"\")"
        a.font = BOLD
        a.border = BOX
        for cell in (m, a):
            cell.number_format = {"D": FMT_F, "E": FMT_P, "F": FMT_J, "G": FMT_J, "H": FMT_J,
                                  "I": FMT_J, "J": FMT_X, "K": FMT_X, "L": '0.00'}[col]
    ws.cell(row=46, column=1,
            value="Ligne 6 = dossier en cours (liée au classeur). Lignes 7 à 40 : coller les VALEURS des "
                  "dossiers précédents. Un ratio ne vaut que comparé — à lui-même dans le temps, et au secteur.").font = SUB

    # ============================================================== SYNTHESE
    ws = wb.create_sheet("Synthese")
    header(ws, "Synthèse du diagnostic", "Une page — à reprendre dans le rapport d'audit")
    ws.column_dimensions["A"].width = 46
    for col in "BCD":
        ws.column_dimensions[col].width = 18
    ws["A5"] = f"={P['client']}"
    ws["A5"].font = Font(name=FONT, size=13, bold=True)
    ws["A6"] = f'="Secteur : "&{P["secteur"]}&"   |   Exercice analysé : "&{P["exo"]}'
    ws["A6"].font = SUB
    ws["A7"] = f'="Contrôles de cohérence : "&Saisie_Balance!E{CTRL_ROW}'
    ws["A7"].font = BOLD
    r = 9
    sect(ws, r, "CHIFFRES CLÉS", 6)
    yr_head(ws, r, cols=("B", "C", "D"))
    r += 1
    for lab, key in [("Chiffre d'affaires", "ca"), ("Excédent brut d'exploitation", "ebe"),
                     ("Résultat d'exploitation", "re"), ("Résultat net", "rn"),
                     ("Capacité d'autofinancement", "caf"), ("Actif économique", "ae"),
                     ("Capitaux propres", "cp"), ("Endettement net", "dn"),
                     ("Besoin en fonds de roulement", "bfr")]:
        ws.cell(row=r, column=1, value=lab).font = BLACK
        for src, dst in zip(("C", "D", "E"), ("B", "C", "D")):
            c = ws[f"{dst}{r}"]
            c.value = f"=Retraitements!{src}{R[key]}"
            c.number_format = FMT_F
            c.font = GREEN
            c.border = BOX
        r += 1
    r += 1
    sect(ws, r, "VERDICT (exercice N)", 6)
    r += 1
    verdicts = [
        ("Marge d'exploitation (EBE / CA)", f"=Diagnostic!E{D['t_ebe']}", FMT_P, f"=Diagnostic!F{D['t_ebe']}"),
        ("Effet de ciseau", f"=Diagnostic!E{D['ciseau']}", FMT_P, f"=Diagnostic!F{D['ciseau']}"),
        ("BFR en jours de CA", f"=Diagnostic!E{D['bfr_j']}", FMT_J, f"=Diagnostic!F{D['bfr_j']}"),
        ("Délai clients", f"=Diagnostic!E{D['d_cli']}", FMT_J, f"=Diagnostic!F{D['d_cli']}"),
        ("Dettes fiscales et sociales (jours de CA)", f"=Diagnostic!E{D['d_dfs']}", FMT_J,
         f"=Diagnostic!F{D['d_dfs']}"),
        ("Endettement net / EBE", f"=Diagnostic!E{D['dn_ebe']}", FMT_X, f"=Diagnostic!F{D['dn_ebe']}"),
        ("Couverture des frais financiers", f"=Diagnostic!E{D['cfi']}", FMT_X, f"=Diagnostic!F{D['cfi']}"),
        ("Autonomie financière", f"=Diagnostic!E{D['auto']}", FMT_P, f"=Diagnostic!F{D['auto']}"),
        ("Rentabilité économique après impôt", f"=Diagnostic!E{D['re_eco']}", FMT_P, ""),
        ("Coût de la dette après impôt", f"=Diagnostic!E{D['i_dette']}", FMT_P, ""),
        ("Effet de levier", f"=Diagnostic!E{D['levier']}", FMT_P, f"=Diagnostic!F{D['levier']}"),
        ("Coût moyen pondéré du capital", f"=Creation_Valeur!E{V['cmpc']}", FMT_P, ""),
        ("Spread (Re − CMPC)", f"=Diagnostic!E{D['spread']}", FMT_P, f"=Diagnostic!F{D['spread']}"),
        ("Valeur économique ajoutée", f"=Creation_Valeur!E{V['vea']}", FMT_F,
         f"=Creation_Valeur!E{V['verdict']}"),
        ("Score Z'' d'Altman", f"=Score!E{Z['z']}", '0.00', f"=Score!E{Z['zone']}"),
    ]
    SYN_FIRST = r
    for lab, f, fmt_, al in verdicts:
        ws.cell(row=r, column=1, value=lab).font = BLACK
        c = ws[f"B{r}"]
        c.value = f
        c.number_format = fmt_
        c.font = GREEN
        c.border = BOX
        if al:
            a = ws[f"C{r}"]
            a.value = al
            a.font = BOLD
            a.border = BOX
        r += 1
    SYN_LAST = r - 1
    r += 1
    ws.cell(row=r, column=1, value="INDICE DE SANTÉ FINANCIÈRE MDC").font = Font(name=FONT, size=12, bold=True)
    n = ws[f"B{r}"]
    n.value = f"=Score!G{NOTE_ROW}"
    n.font = Font(name=FONT, size=16, bold=True, color="C00000")
    n.alignment = Alignment(horizontal="center")
    n.border = BOX
    ws[f"C{r}"] = f'="Score : "&TEXT(Score!G{SCORE_ROW},"0.0")&" / 100"'
    ws[f"C{r}"].font = BOLD
    r += 2
    ws.cell(row=r, column=1,
            value="Cette note porte sur la SANTÉ FINANCIÈRE. Elle se combine avec la notation de conformité "
                  "comptable, fiscale et sociale (domaines A à G) pour former la note MDC globale.").font = SUB

    # ------------------------------------------------ mises en forme conditionnelles
    def cf(sheet, rng, ref):
        s = wb[sheet]
        rouge = [("ALERTE", "9C0006"), ("MASSUE", "9C0006"), ("DÉTRUIT", "9C0006"), ("PERTE", "9C0006")]
        for mot, coul in rouge:
            s.conditional_formatting.add(rng, FormulaRule(
                formula=[f'ISNUMBER(SEARCH("{mot}",{ref}))'], fill=RED_F,
                font=Font(name=FONT, size=10, bold=True, color=coul)))
        s.conditional_formatting.add(rng, FormulaRule(
            formula=[f'ISNUMBER(SEARCH("Vigilance",{ref}))'], fill=ORG_F,
            font=Font(name=FONT, size=10, bold=True, color="9C6500")))
        for mot in ("OK", "CRÉE"):
            s.conditional_formatting.add(rng, FormulaRule(
                formula=[f'ISNUMBER(SEARCH("{mot}",{ref}))'], fill=GRN_F,
                font=Font(name=FONT, size=10, bold=True, color="006100")))

    cf("Diagnostic", f"F5:F{DIAG_LAST}", "$F5")
    cf("Synthese", f"C{SYN_FIRST}:C{SYN_LAST}", f"$C{SYN_FIRST}")
    wsS = wb["Saisie_Balance"]
    wsS.conditional_formatting.add(f"C{CTRL_ROW}:E{CTRL_ROW}", FormulaRule(
        formula=[f'C{CTRL_ROW}="ANOMALIE"'], fill=RED_F,
        font=Font(name=FONT, size=10, bold=True, color="9C0006")))
    wsS.conditional_formatting.add(f"C{CTRL_ROW}:E{CTRL_ROW}", FormulaRule(
        formula=[f'C{CTRL_ROW}="OK"'], fill=GRN_F,
        font=Font(name=FONT, size=10, bold=True, color="006100")))

    for s in wb.worksheets:
        for row in s.iter_rows():
            for c in row:
                if c.font is None or c.font.name is None:
                    c.font = BLACK
        s.sheet_properties.pageSetUpPr.fitToPage = True

    wb.calculation.fullCalcOnLoad = True
    wb.save(chemin)
    return chemin


def main():
    ap = argparse.ArgumentParser(description="Génère le classeur de diagnostic financier MDC.")
    ap.add_argument("--client", default="CLIENT À RENSEIGNER")
    ap.add_argument("--forme", default="SARL")
    ap.add_argument("--secteur", default="À renseigner")
    ap.add_argument("--exercice", default="")
    ap.add_argument("--auditeur", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--vierge", action="store_true", help="classeur vide (postes à zéro)")
    ap.add_argument("--json", dest="json_path", help="pré-remplissage depuis un JSON")
    ap.add_argument("--taux-is", type=float, default=PARAMS_DEFAUT["taux_is"])
    ap.add_argument("--jours", type=int, default=PARAMS_DEFAUT["jours"])
    ap.add_argument("--cout-fp", type=float, default=PARAMS_DEFAUT["cout_fp"])
    ap.add_argument("--cout-dette", type=float, default=PARAMS_DEFAUT["cout_dette"])
    a = ap.parse_args()

    if a.json_path:
        brut = json.load(open(a.json_path, encoding="utf-8"))
        donnees = {exo: {k: float(v) for k, v in brut.get(exo, {}).items()}
                   for exo in ("N-2", "N-1", "N")}
    elif a.vierge:
        donnees = {exo: {} for exo in ("N-2", "N-1", "N")}
    else:
        donnees = {exo: {k: v * M for k, v in EXEMPLE[exo].items()}
                   for exo in ("N-2", "N-1", "N")}

    identite = {"client": a.client, "forme": a.forme, "secteur": a.secteur,
                "exercice": a.exercice, "auditeur": a.auditeur}
    params = {"taux_is": a.taux_is, "jours": a.jours,
              "cout_fp": a.cout_fp, "cout_dette": a.cout_dette}
    chemin = construire(a.out, identite, donnees, params)
    print(f"Classeur produit : {chemin}")
    if not (a.vierge or a.json_path):
        print("ATTENTION : contient le cas de démonstration NEGOCE IVOIRE SARL. "
              "Remplacer les valeurs de l'onglet Saisie_Balance.")


if __name__ == "__main__":
    main()
