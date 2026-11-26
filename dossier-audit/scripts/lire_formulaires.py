# -*- coding: utf-8 -*-
"""Lit le classeur des formulaires REMPLI et en fait la matière du dossier.

Il reconnait les tableaux a leur ligne d'en-tete (fond bleu nuit), lit les lignes
renseignees, et ecrit `collecte.json` a cote du classeur. Les squelettes s'en servent
ensuite : ce que vous avez rempli devient le contenu des livrables.

  python3 lire_formulaires.py "<le classeur rempli.xlsx>"
  python3 lire_formulaires.py "<dossier d'audit>"            (prend le classeur le plus recent)
"""
import json, os, sys, datetime

try:
    import openpyxl
except ImportError:
    raise SystemExit("La lecture des formulaires a besoin d'openpyxl.")

NAVY = "1A1A2E"


def est_entete(ws, r, larg):
    c = ws.cell(r, 1)
    if not c.value or not isinstance(c.value, str):
        return False
    try:
        rgb = (c.fill.fgColor.rgb or "")[-6:].upper()
    except Exception:
        rgb = ""
    return rgb == NAVY and r > 3


def tableaux_de(ws, larg=14):
    """Les tableaux de la feuille : (en-tetes, lignes renseignees)."""
    out, entete, lignes = [], None, []
    for r in range(1, ws.max_row + 2):
        if est_entete(ws, r, larg):
            if entete and lignes:
                out.append((entete, lignes))
            entete = [str(ws.cell(r, j).value).strip() for j in range(1, larg + 1)
                      if ws.cell(r, j).value not in (None, "")]
            lignes = []
            continue
        if entete:
            dans_le_tableau = False
            try:
                dans_le_tableau = ws.cell(r, 1).border.left.style == "thin"
            except Exception:
                pass
            if not dans_le_tableau:          # un titre de section n'est pas une ligne du tableau
                continue
            vals = [ws.cell(r, j).value for j in range(1, len(entete) + 1)]
            if any(v not in (None, "") for v in vals):
                lignes.append(["" if v is None else (v if not isinstance(v, datetime.datetime)
                                                     else v.strftime("%d/%m/%Y")) for v in vals])
    if entete and lignes:
        out.append((entete, lignes))
    return out


def lire(chemin):
    wb = openpyxl.load_workbook(chemin, data_only=True)
    D = {"classeur": os.path.basename(chemin), "lu_le": datetime.date.today().isoformat(), "feuilles": {}}
    for nom in wb.sheetnames:
        ws = wb[nom]
        blocs = []
        for entete, lignes in tableaux_de(ws):
            blocs.append({"colonnes": entete,
                          "lignes": [dict(zip(entete, l)) for l in lignes]})
        if blocs:
            D["feuilles"][nom] = blocs
    return D


def dernier_classeur(dossier):
    cands = [x for x in os.listdir(dossier) if x.startswith("FORMULAIRES_DE_COLLECTE") and x.endswith(".xlsx")]
    if not cands:
        raise SystemExit("Aucun classeur de formulaires dans %s" % dossier)
    return os.path.join(dossier, sorted(cands)[-1])


def main():
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    cible = a[0]
    if os.path.isdir(cible):
        chemin, dest = dernier_classeur(cible), cible
    else:
        chemin, dest = cible, os.path.dirname(os.path.abspath(cible))
    D = lire(chemin)
    print("CLASSEUR LU : %s\n" % D["classeur"])
    total = 0
    for nom, blocs in D["feuilles"].items():
        n = sum(len(b["lignes"]) for b in blocs)
        total += n
        print("  %-30s %d tableau(x), %d ligne(s) renseignée(s)" % (nom[:30], len(blocs), n))
    q = os.path.join(dest, "collecte.json")
    json.dump(D, open(q, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n%d lignes au total.\nÉcrit : %s" % (total, q))
    print("Les squelettes reprennent cette matière avec : squelettes_audit.py <DOSSIER> \"<dossier>\" --collecte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
