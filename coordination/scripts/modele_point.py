"""Produit le modèle Excel du point global des dossiers (à envoyer aux collaborateurs).

    python3 modele_point.py SORTIE.xlsx [--collaborateur "Awa Koné"] [--clients "ACME;BETA;…"]

--collaborateur pré-remplit la colonne « Collaborateur responsable » ; --clients pré-remplit une
ligne par client (séparés par « ; »). Feuilles : « Point des dossiers » (à remplir, listes déroulantes),
« Mode d'emploi », « Listes » (valeurs permises, masquée).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grille import COLONNES  # noqa: E402

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

LIGNES = 60


def produire(sortie, collaborateur="", clients=()):
    wb = Workbook()
    ws = wb.active
    ws.title = "Point des dossiers"
    fin = Side(style="thin", color="D5DAE1")
    entete = PatternFill("solid", fgColor="172033")
    oblig = PatternFill("solid", fgColor="7A2E1F")
    for i, (cle, titre, aide, typ, liste, obligatoire) in enumerate(COLONNES, start=1):
        c = ws.cell(row=1, column=i, value=titre + (" *" if obligatoire else ""))
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.fill = oblig if obligatoire else entete
        c.alignment = Alignment(wrap_text=True, vertical="center")
        a = ws.cell(row=2, column=i, value=aide)
        a.font = Font(italic=True, size=8, color="5B6472")
        a.alignment = Alignment(wrap_text=True, vertical="top")
        ws.column_dimensions[get_column_letter(i)].width = 34 if typ == "texte" else 18
        for r in range(3, LIGNES + 3):
            ws.cell(row=r, column=i).border = Border(top=fin, bottom=fin, left=fin, right=fin)
            if typ == "montant":
                ws.cell(row=r, column=i).number_format = "# ##0"
    ws.row_dimensions[1].height = 42
    ws.row_dimensions[2].height = 54
    ws.freeze_panes = "B3"

    listes = wb.create_sheet("Listes")
    for i, (cle, titre, aide, typ, liste, obl) in enumerate(COLONNES, start=1):
        if not liste:
            continue
        col = get_column_letter(i)
        for j, v in enumerate(liste, start=1):
            listes.cell(row=j, column=i, value=v)
        dv = DataValidation(type="list", formula1=f"=Listes!${col}$1:${col}${len(liste)}", allow_blank=True,
                            showErrorMessage=True, errorTitle="Valeur non prévue", error="Choisissez une valeur de la liste.")
        ws.add_data_validation(dv)
        dv.add(f"{col}3:{col}{LIGNES + 2}")
    listes.sheet_state = "hidden"

    noms = [x.strip() for x in clients if x.strip()]
    for k, nom in enumerate(noms):
        ws.cell(row=3 + k, column=1, value=nom)
    if collaborateur:
        for r in range(3, 3 + (len(noms) if noms else LIGNES)):
            ws.cell(row=r, column=2, value=collaborateur)

    me = wb.create_sheet("Mode d'emploi", 0)
    texte = [
        "POINT GLOBAL DES DOSSIERS — La Maison de la Conformité",
        "",
        "Une ligne par dossier EN COURS dont vous êtes responsable (clients suivis chaque mois et missions ponctuelles non terminées).",
        "Les colonnes marquées * (en rouge) sont obligatoires. Utilisez les listes déroulantes quand il y en a.",
        "Mois au format AAAA-MM (ex. 2026-10) ; dates au format AAAA-MM-JJ (ex. 2026-12-15) ; montants en FCFA, sans espace.",
        "",
        "Soyez factuel : « comptabilité à jour jusqu'à » = dernier mois entièrement saisi ET rapproché avec la banque.",
        "Action proposée : un verbe et un livrable (« Relancer le client pour les relevés d'octobre », pas « voir le dossier »).",
        "Si vous ne savez pas, écrivez « À vérifier » plutôt que de laisser vide : un vide sera relancé.",
        "",
        "Exemple :",
    ]
    for i, t in enumerate(texte, start=1):
        me.cell(row=i, column=1, value=t).font = Font(bold=(i == 1), size=12 if i == 1 else 10)
    exemple = {"client": "ACME SARL (exemple fictif)", "collaborateur": "Awa Koné", "suivi": "Mensuel", "regime": "RSI",
               "compta_a_jour": "2026-09", "fiscal_depose": "2026-10", "social_depose": "2026-10", "paie": "À jour",
               "dsf": "Déposés", "pieces_manquantes": "Relevés bancaires d'octobre (relancé le 20/11)", "controle": "Non",
               "honoraires_impayes": 150000, "prochaine_echeance": "2026-12-15", "objet_echeance": "TVA de novembre",
               "derniere_intervention": "2026-11-24", "blocage": "Relevés d'octobre manquants",
               "action_proposee": "Relancer le gérant d'ACME par téléphone pour les relevés", "pour_quand": "2026-11-28",
               "besoin_gerant": "", "commentaire": ""}
    for i, (cle, titre, *_r) in enumerate(COLONNES, start=1):
        me.cell(row=len(texte) + 1, column=i, value=titre).font = Font(bold=True, size=9)
        me.cell(row=len(texte) + 2, column=i, value=exemple.get(cle, "")).font = Font(size=9)
    me.column_dimensions["A"].width = 30
    wb.active = wb.sheetnames.index("Point des dossiers")
    wb.save(sortie)
    return sortie


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sortie")
    p.add_argument("--collaborateur", default="")
    p.add_argument("--clients", default="")
    a = p.parse_args()
    print(produire(a.sortie, a.collaborateur, a.clients.split(";") if a.clients else ()))
