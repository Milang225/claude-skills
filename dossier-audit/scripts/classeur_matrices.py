# -*- coding: utf-8 -*-
"""Classeur des matrices d'anomalies et des chiffrages.

Le classeur S'EXTRAIT DU RAPPORT ET DES LIVRABLES, jamais d'une saisie : aucun chiffre
n'est ecrit ici, tous sont relus dans les sources .md du dossier. C'est la regle apprise
sur MABEK, ou un classeur produit avant la derniere correction du rapport a contredit le
dossier de 941 257.

Il refuse de travailler sur un rapport qui porte encore une consigne « A REDIGER », et il
ecrit, a cote du classeur, la date de derniere modification de chaque source : le controle
de coherence s'en sert pour verifier que le classeur est bien posterieur au rapport.

  python3 classeur_matrices.py LBTECH "<dossier d'audit>"
"""
import datetime, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from donnees_dossier import charger, pivots

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
except ImportError:
    raise SystemExit("Le classeur a besoin d'openpyxl. Installer : python3 -m pip install openpyxl")

NAVY, GRIS, OR = "1A1A2E", "EEF0F4", "8A6D1F"
FIN = Side(style="thin", color="B8BCC6")
BORD = Border(left=FIN, right=FIN, top=FIN, bottom=FIN)
NUM = '#,##0;-#,##0;"-"'
MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre")


# ───────────────────────── lecture des sources ─────────────────────────

def sans_accent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if unicodedata.category(c) != "Mn").lower()


def source(src_dir, prefixe):
    for f in sorted(os.listdir(src_dir)):
        if f.endswith(".md") and f.startswith(prefixe):
            return os.path.join(src_dir, f)
    return None


def sections(txt):
    """[(titre, corps)] pour chaque « ## n. Titre » du document."""
    out = []
    for m in re.finditer(r"\n##\s+(?:\d+\.\s*)?(.+?)\n(.*?)(?=\n##\s|\Z)", txt, re.S):
        out.append((m.group(1).strip(), m.group(2)))
    return out


def trouver(secs, *mots):
    """Le corps de la premiere section dont le titre porte tous les mots."""
    for titre, corps in secs:
        t = sans_accent(titre)
        if all(sans_accent(m) in t for m in mots):
            return corps
    return None


def tableaux(corps):
    """Les tableaux markdown d'un corps de section, sans la ligne de separation."""
    out, cur = [], []
    for ligne in (corps or "").split("\n"):
        if ligne.startswith("|"):
            cells = [c.strip().replace("**", "") for c in ligne.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            cur.append(cells)
        elif cur:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def paragraphes(corps):
    """Les paragraphes d'un corps de section, hors tableaux et hors titres."""
    out = []
    for bloc in re.split(r"\n\s*\n", corps or ""):
        b = bloc.strip()
        if not b or b.startswith(("|", "#", ">")):
            continue
        out.append(re.sub(r"\s+", " ", b.replace("**", "")))
    return out


# ───────────────────────────── le classeur ─────────────────────────────

class Classeur(object):
    def __init__(self, sous_titre):
        self.wb = openpyxl.Workbook()
        self.wb.remove(self.wb.active)
        self.sous = sous_titre
        self.onglets = []

    def feuille(self, titre, onglet, head, rows, widths, numcols=()):
        if not rows:
            return None
        ws = self.wb.create_sheet(onglet[:31])
        ws.sheet_view.showGridLines = False
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
        last = chr(65 + len(widths) - 1)
        ws.merge_cells("A1:%s1" % last)
        c = ws["A1"]
        c.value = "LA MAISON DE LA CONFORMITÉ — " + titre
        c.font = Font(bold=True, size=13, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(vertical="center", indent=1)
        ws.row_dimensions[1].height = 30
        ws.merge_cells("A2:%s2" % last)
        s = ws["A2"]
        s.value = self.sous
        s.font = Font(italic=True, size=9)
        s.alignment = Alignment(indent=1)
        ws.row_dimensions[2].height = 18
        for j, h in enumerate(head):
            c = ws.cell(4, j + 1, h)
            c.font = Font(bold=True, size=10)
            c.fill = PatternFill("solid", fgColor=GRIS)
            c.border = BORD
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.row_dimensions[4].height = 32
        r = 5
        for row in rows:
            titre_de_bloc = bool(row) and len([x for x in row if str(x).strip()]) == 1 and str(row[0]).isupper()
            gras = titre_de_bloc or (bool(row) and sans_accent(str(row[0])).startswith(("total", "totaux")))
            for j, v in enumerate(list(row)[:len(head)]):
                val = v
                if j in numcols and isinstance(v, str):
                    n = v.replace(" ", "").replace(" ", "").replace(" ", "")
                    if re.fullmatch(r"-?\d+", n):
                        val = int(n)
                c = ws.cell(r, j + 1, val)
                c.border = BORD
                c.alignment = Alignment(vertical="top", wrap_text=True, indent=1,
                                        horizontal="right" if isinstance(val, int) else "left")
                if isinstance(val, int):
                    c.number_format = NUM
                c.font = Font(size=9, bold=gras, color=NAVY if titre_de_bloc else "000000")
            r += 1
        ws.freeze_panes = "A5"
        self.onglets.append(onglet)
        return ws


def entier(s):
    n = str(s).replace(" ", "").replace(" ", "").replace(" ", "")
    return int(n) if re.fullmatch(r"-?\d+", n) else None


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        raise SystemExit(__doc__)
    dossier, dest = a[0], a[1]
    D, _ = charger(dossier, a[a.index("--json") + 1] if "--json" in a else None)
    p = pivots(D)
    src_dir = os.path.join(dest, "_SOURCES_MD")

    f_rap = source(src_dir, "RAPPORT_AUDIT_CONFORMITE")
    f_doc = source(src_dir, "AUDIT_DOCUMENTAIRE")
    f_exp = source(src_dir, "NOTE_DE_CHIFFRAGE")
    f_tab = source(src_dir, "TABLEAU_D_EXPOSITION")
    if not f_rap:
        raise SystemExit("Aucun rapport d'audit dans %s : le classeur s'extrait du rapport." % src_dir)
    rap = open(f_rap, encoding="utf-8").read()
    if "À RÉDIGER" in rap:
        raise SystemExit("Le rapport porte encore des consignes à rédiger : le classeur ne s'extrait "
                         "que d'un rapport achevé.")
    s_rap = sections(rap)
    s_doc = sections(open(f_doc, encoding="utf-8").read()) if f_doc else []
    s_exp = sections(open(f_exp, encoding="utf-8").read()) if f_exp else []
    s_tab = sections(open(f_tab, encoding="utf-8").read()) if f_tab else []

    jour = datetime.date.today()
    ref = "MC-MAT-%s-%d-001" % (p["secteur"], jour.year)
    sous = ("Client : %s (NCC %s)    |    Exercices %s    |    Référence : %s    |    "
            "Extrait du rapport d'audit de conformité du %d %s %d"
            % (p["raison_sociale"], p["ncc"], p["exercices"], ref,
               jour.day, MOIS[jour.month - 1], jour.year))
    cl = Classeur(sous)
    manques = []

    # 1. Synthese : l'etat recapitulatif du rapport
    rec = trouver(s_rap, "recapitulatif")
    tb = tableaux(rec) if rec else []
    if len(tb) >= 2:
        rows = [["PAR DOMAINE ET PAR GRAVITÉ", "", "", "", ""]] + \
               [r + [""] * (5 - len(r)) for r in tb[0]] + \
               [["", "", "", "", ""], ["PAR NATURE D'IMPÔT OU DE COTISATION, ET PAR SCÉNARIO", "", "", "", ""]] + \
               [r + [""] * (5 - len(r)) for r in tb[1]]
        if len(tb) >= 3:
            rows += [["", "", "", "", ""], ["LES EXPOSITIONS ALTERNATIVES, HORS TOTAL", "", "", "", ""]] + \
                    [r + [""] * (5 - len(r)) for r in tb[2]]
        cl.feuille("ÉTAT RÉCAPITULATIF", "1 Synthèse",
                   ["Domaine ou nature", "Anomalies, ou droits", "Critiques, ou favorable",
                    "Majeures, ou central", "Mineures, ou haut"],
                   rows, [62, 20, 20, 20, 20], numcols=(1, 2, 3, 4))
    else:
        manques.append("l'état récapitulatif du rapport")

    # 2 a 5. Les matrices
    for mots, onglet, titre in ((("matrice", "fiscal"), "2 Matrice fiscale", "MATRICE DES ANOMALIES FISCALES"),
                                (("matrice", "social"), "3 Matrice sociale", "MATRICE DES ANOMALIES SOCIALES"),
                                (("matrice", "comptable"), "4 Matrice comptable", "MATRICE DES ANOMALIES COMPTABLES"),
                                (("matrice", "procedure"), "5 Matrice procédures", "MATRICE DES PROCÉDURES")):
        corps = trouver(s_rap, *mots)
        t = tableaux(corps)
        if t:
            head = t[0][0]
            cl.feuille(titre, onglet, head, t[0][1:],
                       [10, 60, 16] + [34] * (len(head) - 6) + [14, 14, 14])
        else:
            manques.append(titre.lower())

    # 6. Audit documentaire
    inv = trouver(s_doc, "inventaire") if s_doc else None
    score = trouver(s_doc, "score") if s_doc else None
    rows = []
    if score:
        t = tableaux(score)
        if t:
            rows += [["LE SCORE PAR DOMAINE", "", "", "", ""]] + [r + [""] * (5 - len(r)) for r in t[0]] + \
                    [["", "", "", "", ""]]
    if inv:
        t = tableaux(inv)
        if t:
            rows += [["L'INVENTAIRE, PIÈCE PAR PIÈCE", "", "", "", ""]] + [r + [""] * (5 - len(r)) for r in t[0]]
    if rows:
        cl.feuille("AUDIT DOCUMENTAIRE — INVENTAIRE DES PIÈCES", "6 Audit documentaire",
                   ["Domaine", "Document", "Situation", "Ce que l'absence coûte", "Critique"],
                   rows, [16, 46, 16, 80, 12], numcols=(1, 2, 3, 4))
    else:
        manques.append("l'inventaire documentaire")

    # 7. Conventions
    conv = trouver(s_rap, "convention")
    t = tableaux(conv) if conv else []
    if t:
        cl.feuille("LES CONVENTIONS QUE LA SOCIÉTÉ N'A PAS ÉTABLIES", "7 Conventions",
                   t[0][0], t[0][1:], [8, 46, 70, 40, 14])
    elif conv:
        cl.feuille("LES CONVENTIONS QUE LA SOCIÉTÉ N'A PAS ÉTABLIES", "7 Conventions",
                   ["Ce que le rapport établit"], [[x] for x in paragraphes(conv)], [150])
    else:
        manques.append("les conventions non établies")

    # 8. Les details de calcul, poste par poste
    rows, lignes_chiffrees = [], []
    for titre, corps in s_exp:
        if "poste" not in sans_accent(titre):
            continue
        t = tableaux(corps)
        if not t:
            continue
        head = t[0][0]
        rows.append([titre.upper()] + [""] * (len(head) - 1))
        rows.append(head)
        for l in t[0][1:]:
            rows.append(l)
            lignes_chiffrees.append((titre, l))
        rows.append([""] * len(head))
    if rows:
        cl.feuille("LE DÉTAIL DE CHAQUE CALCUL, POSTE PAR POSTE", "8 Détails de calcul",
                   ["Élément", "Exercice", "Période", "Situation", "Base", "Taux ou article",
                    "Droits", "Bas", "Central", "Haut", "Pièce"],
                   rows, [60, 11, 16, 18, 16, 30, 14, 14, 14, 14, 54], numcols=(4, 6, 7, 8, 9))
    else:
        manques.append("le détail des calculs de la note de chiffrage")

    # 9. Interets et majorations, avec la methode de chaque ligne
    methodes = {}
    t_tab = tableaux(open(f_tab, encoding="utf-8").read()) if f_tab else []
    if t_tab:
        for l in t_tab[0][1:]:
            if len(l) >= 4:
                methodes[sans_accent(l[0])[:60]] = l[3]
    rows = []
    for titre, l in lignes_chiffrees:
        if len(l) < 10:
            continue
        d, b, c, h = (entier(l[6]), entier(l[7]), entier(l[8]), entier(l[9]))
        if d is None or c is None:
            continue
        if sans_accent(l[0]).startswith("total"):
            continue
        meth = methodes.get(sans_accent(l[0])[:60], "")
        rows.append([l[0], titre.split("—")[-1].strip(), d, b, c, h, c - d,
                     ("%.1f %%" % (100.0 * (c - d) / d)) if d else "", meth])
    if rows:
        td = sum(r[2] for r in rows); tb_ = sum(r[3] or 0 for r in rows)
        tc = sum(r[4] for r in rows); th = sum(r[5] or 0 for r in rows)
        rows.append(["TOTAL", "", td, tb_, tc, th, tc - td,
                     ("%.1f %%" % (100.0 * (tc - td) / td)) if td else "",
                     "Les intérêts de retard et les majorations sont la différence entre le "
                     "scénario central et les droits simples. Les majorations propres à la caisse "
                     "de prévoyance sociale n'y sont pas comprises."])
        cl.feuille("INTÉRÊTS DE RETARD ET MAJORATIONS, LIGNE PAR LIGNE", "9 Intérêts et majorations",
                   ["Élément", "Poste", "Droits simples", "Favorable", "Central", "Haut",
                    "Intérêts et majorations au central", "Poids sur les droits", "Méthode"],
                   rows, [58, 30, 15, 15, 15, 15, 18, 14, 60], numcols=(2, 3, 4, 5, 6))
    else:
        manques.append("les intérêts et majorations ligne par ligne")

    # 10. Les postes alternatifs et ce qui n'est pas chiffre
    rows = []
    if rec:
        t = tableaux(rec)
        if len(t) >= 3:
            rows += [["LES EXPOSITIONS ALTERNATIVES, QUI NE SE CUMULENT JAMAIS", "", ""]] + \
                    [r + [""] * (3 - len(r)) for r in t[2]] + [["", "", ""]]
    nc = trouver(s_exp, "cumule") or trouver(s_exp, "additionne")
    if nc:
        rows += [["CE QUI S'ADDITIONNE, ET CE QUI NE SE CUMULE JAMAIS", "", ""]] + \
                [[x, "", ""] for x in paragraphes(nc)] + [["", "", ""]]
    if rec:
        rows += [["CE QUI N'EST PAS CHIFFRÉ, FAUTE DE PIÈCES", "", ""]]
        garde = False
        for bloc in re.split(r"\n\s*\n", rec):
            b = bloc.strip().replace("**", "")
            if not b:
                continue
            if b.startswith("|"):
                continue
            if sans_accent(b).startswith("ce qui n'est pas chiffre"):
                garde = True; continue
            if sans_accent(b).startswith("ce qui joue en faveur"):
                garde = False; rows += [["", "", ""], ["CE QUI JOUE EN FAVEUR DE LA SOCIÉTÉ", "", ""]]
                continue
            if b.startswith("#"):
                continue
            rows.append([re.sub(r"\s+", " ", b), "", ""])
    if rows:
        cl.feuille("LES POSTES ALTERNATIFS ET CE QUI N'EST PAS CHIFFRÉ", "10 Postes alternatifs",
                   ["Objet", "Montant en cause", "Pourquoi il reste hors total"],
                   rows, [110, 24, 70])
    else:
        manques.append("les postes alternatifs")

    nom = re.sub(r"[^A-Z0-9]+", "_", p["raison_sociale"].upper()).strip("_")
    out = os.path.join(dest, "MATRICES_ANOMALIES_ET_CHIFFRAGES_%s_%s.xlsx" % (nom, jour.isoformat()))
    if os.path.exists(out):
        arch = os.path.join(dest, "_OBSOLETE", "VERSIONS_MODIFIEES")
        os.makedirs(arch, exist_ok=True)
        h = datetime.datetime.now().strftime("%Hh%M%S")
        os.rename(out, os.path.join(arch, os.path.basename(out)[:-5] + "_AVANT_%s.xlsx" % h))
    cl.wb.save(out)

    # la trace de fraicheur : le classeur doit etre posterieur a chaque source
    trace = {"classeur": os.path.basename(out), "reference": ref,
             "ecrit_le": datetime.datetime.now().isoformat(timespec="seconds"),
             "sources": {}}
    for f in sorted(os.listdir(src_dir)):
        if f.endswith(".md"):
            trace["sources"][f] = datetime.datetime.fromtimestamp(
                os.path.getmtime(os.path.join(src_dir, f))).isoformat(timespec="seconds")
    with open(os.path.join(src_dir, "_classeur_extrait_de.json"), "w", encoding="utf-8") as fh:
        json.dump(trace, fh, ensure_ascii=False, indent=1)

    print("Classeur écrit : %s" % os.path.basename(out))
    print("  %d onglet(s) : %s" % (len(cl.onglets), ", ".join(cl.onglets)))
    print("  extrait de : %s" % os.path.basename(f_rap))
    if manques:
        print("\n  Non repris, faute de matière dans les sources :")
        for m in manques:
            print("    - %s" % m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
