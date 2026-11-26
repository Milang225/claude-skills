#!/usr/bin/env python3
"""Registre des documents de méthode de l'Agence : où se trouve chaque document validé ou en cours de validation.
Ajouter une ligne à DOCS, puis : python3 build_registre.py
"""
import os
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

SG = os.path.expanduser("~/Documents/SUPERVISEUR GENERAL")
OUT = os.path.join(SG, "00_REGISTRE_DES_DOCUMENTS_VALIDES.xlsx")
# (famille, document, référence, date, statut, dossier relatif à SUPERVISEUR GENERAL, fichier)
DOCS = [
    ("Travaux préliminaires", "Procédure des travaux préliminaires, version 2 (16 étapes)", "MC-PROC-PRE-2026-001", "13/10/2026", "En cours de validation", "TRAVAUX_PRELIMINAIRES_2026", "00_PROCEDURE_DES_TRAVAUX_PRELIMINAIRES (pdf, docx)"),
    ("Travaux préliminaires", "Les deux phases et leurs étapes (16 étapes)", "MC-PROC-PRE-2026-002", "13/10/2026", "Validé", "TRAVAUX_PRELIMINAIRES_2026", "01_LES_DEUX_PHASES_ET_LEURS_ETAPES (pdf, docx)"),
    ("Travaux préliminaires", "Modèle de profil de l'entreprise, complet", "MC-MOD-PROF-2026-002", "12/10/2026", "En cours de validation", "TRAVAUX_PRELIMINAIRES_2026/PHASE_1_PROFIL_DE_L_ENTREPRISE", "1.01_MODELE_PROFIL_DE_L_ENTREPRISE (pdf, docx)"),
    ("Profil de l'entreprise", "Modèle de profil de l'entreprise, version 9 : partie J, le dossier juridique (actes, concordance, registre des décisions, contrats, obligations annuelles, régularisations, bibliothèque de modèles)", "MC-MOD-PROF-2026-002", "06/11/2026", "En cours de validation", "PROFIL_ENTREPRISE_2026", "MODELE_PROFIL_ENTREPRISE_COMPLET (pdf, docx)"),
    ("Travaux préliminaires", "Outils de l'étape 1 (demande de pièces, guide d'entretien, classeur de diagnostic, inventaire des tiers, feuille de chiffrage…)", "—", "12/10/2026", "En cours de validation", "TRAVAUX_PRELIMINAIRES_2026/PHASE_1_PROFIL_DE_L_ENTREPRISE", "1.02 à 1.12"),
    ("Travaux préliminaires", "Modèle de plan d'action", "MC-MOD-PLA-2026-001", "12/10/2026", "En cours de validation", "TRAVAUX_PRELIMINAIRES_2026/PHASE_2_PLAN_D_ACTION_ET_MISE_EN_PLACE", "2.01_MODELE_PLAN_D_ACTION (pdf, docx)"),
    ("Travaux préliminaires", "Pièces jointes au plan d'action et exemple du Collège", "—", "12/10/2026", "En cours de validation", "TRAVAUX_PRELIMINAIRES_2026/PHASE_2_PLAN_D_ACTION_ET_MISE_EN_PLACE", "2.02 à 2.07"),
    ("Suivi complet", "Procédure du suivi complet", "MC-PROC-SUI-2026-001", "12/10/2026", "En cours de validation", "SUIVI_COMPLET_2026", "00_PROCEDURE_DU_SUIVI_COMPLET (pdf, docx)"),
    ("Suivi complet", "Classeur de contrôle mensuel", "—", "12/10/2026", "En cours de validation", "SUIVI_COMPLET_2026", "01_CLASSEUR_DE_CONTROLE_MENSUEL.xlsx"),
    ("Suivi complet", "Modèle de note mensuelle", "MC-NMS", "12/10/2026", "En cours de validation", "SUIVI_COMPLET_2026", "02_MODELE_NOTE_MENSUELLE (pdf, docx)"),
    ("Suivi complet", "Modèle de fiche problématique", "MC-PBQ", "12/10/2026", "En cours de validation", "SUIVI_COMPLET_2026", "03_MODELE_FICHE_PROBLEMATIQUE (pdf, docx)"),
    ("Suivi complet", "Plan de classement", "MC-PLAN-CLASSEMENT-2026-002", "12/10/2026", "En cours de validation", "SUIVI_COMPLET_2026", "14_PLAN_DE_CLASSEMENT (pdf, docx)"),
    ("Suivi complet", "Guide de collaboration remis au client (attentes de l'Agence)", "MC-GUIDE-CLIENT-2026-002", "12/10/2026", "En cours de validation", "SUIVI_COMPLET_2026", "15_GUIDE_DE_COLLABORATION_CLIENT (pdf, docx)"),
    ("Suivi complet", "Autres outils (DEE, engagements, indices d'alerte, cartographie, Indice, contrôle de l'administration, profil)", "—", "12/10/2026", "En cours de validation", "SUIVI_COMPLET_2026", "04 à 13"),
    ("Audit complet", "Procédure de l'audit complet (20 étapes, 4 phases)", "MC-MOD-AUD-2026-000", "16/10/2026", "En cours de validation", "AUDIT_COMPLET_2026", "00_PROCEDURE_DE_L_AUDIT_COMPLET (pdf, docx)"),
    ("Audit complet", "Lettre de mission, programme de travail, grille des observations, modèle de rapport de diagnostic, attestation de diagnostic, note de restitution et de clôture", "MC-MOD-AUD-2026-001 à 006", "16/10/2026", "En cours de validation", "AUDIT_COMPLET_2026", "01 à 06 (pdf, docx)"),
    ("Diagnostic complet", "Le dispositif de l'audit de conformité (document maître : trois questions, outils, livrables L01 à L22)", "MC-PROC-AUD-2026-009", "18/10/2026", "Validé", "DIAGNOSTIC_COMPLET", "00_LE_DISPOSITIF_DE_L_AUDIT_DE_CONFORMITE (pdf, docx)"),
    ("Diagnostic complet", "Briefing : outils et livrables de l'audit", "MC-PROC-AUD-2026-010", "18/10/2026", "Validé", "DIAGNOSTIC_COMPLET", "00_BRIEFING_OUTILS_ET_LIVRABLES (pdf, docx)"),
    ("Diagnostic complet", "Documents de cadre 1.1 à 1.7, dont le nouveau livret du collaborateur", "MC-GUI-AUD-2026-001 et autres", "18/10/2026", "Validé", "DIAGNOSTIC_COMPLET/1_OUTILS/1_DOCUMENTS_DE_CADRE", "1.1 à 1.7 (pdf, docx)"),
    ("Diagnostic complet", "Outils de travail 0.1 à Q3.4 (Q2.2 matrice des anomalies comptables, Q2.3 catégorisation des relevés)", "—", "18/10/2026", "Validé", "DIAGNOSTIC_COMPLET/1_OUTILS/2_OUTILS_DE_TRAVAIL", "13 outils (xlsx, docx, pdf)"),
    ("Diagnostic complet", "Modèles des livrables L01 à L22, dont L22 Tableau de bord de synthèse", "MC-MOD-AUD-2026-xxx", "18/10/2026", "Validé", "DIAGNOSTIC_COMPLET/2_LIVRABLES", "L01 à L22 (pdf, docx)"),
    ("Diagnostic complet", "Atelier du diagnostic complet : formulaire, génération du tableau de bord, outils et modèles (application Atelier Diagnostic MDC, http://localhost:8770)", "—", "18/10/2026", "En cours de validation", "DIAGNOSTIC_COMPLET/_SOURCES/atelier", "atelier.py ; tableau_de_bord.py ; exemple_lbtech.json"),
    ("Diagnostic complet", "L'audit de conformité en trois questions (document explicatif, remis au client)", "MC-PROC-AUD-2026-012", "26/10/2026", "En cours de validation", "DIAGNOSTIC_COMPLET", "00_LES_TROIS_QUESTIONS_DE_L_AUDIT (pdf, docx)"),
    ("Diagnostic complet", "Q1.0 Grille des obligations (117 obligations, profil, statut par exercice) et contrôle de la paie (Q1.2)", "—", "26/10/2026", "En cours de validation", "DIAGNOSTIC_COMPLET/1_OUTILS/2_OUTILS_DE_TRAVAIL", "Q1.0_GRILLE_DES_OBLIGATIONS.xlsx ; Q1.2_GRILLE_DECLARATIVE_CNPS.xlsx"),
    ("Diagnostic complet", "Couverture des obligations par le dispositif (matrice, version 2)", "MC-PROC-AUD-2026-013", "26/10/2026", "En cours de validation", "DIAGNOSTIC_COMPLET/3_ANALYSES", "COUVERTURE_DES_OBLIGATIONS (pdf, docx)"),
    ("Identité", "Papier à en-tête 2026, lettre type, note de service", "MC-NS-2026-008", "12/10/2026", "Validé", "PAPIER_EN_TETE_2026 (copie dans Documents/PAPIER EN TETE)", "PAPIER_EN_TETE_MDC_2026, MODELE_LETTRE_MDC_2026"),
    ("Identité", "Signatures électroniques de l'équipe", "—", "12/10/2026", "Validé", "Documents/PAPIER EN TETE/SIGNATURES_COLLABORATEURS", "SIGNATURE_<NOM>.html"),
    ("Pilotage", "Vue à 360° des dossiers et fiches de la semaine", "—", "12/10/2026", "Validé", "Documents/SUIVI CLIENTS", "VUE_360_DES_DOSSIERS_MDC.pdf ; FICHES_DE_LA_SEMAINE_<lundi>.pdf ; SUIVI_DES_DOSSIERS_MDC.xlsx"),
    ("Remplacé", "Procédure d'accompagnement d'un nouveau client (4 phases)", "MC-PROC-ACC-2026-001", "12/10/2026", "Remplacé", "PROCEDURES_GERANT", "Remplacée par MC-PROC-PRE-2026-001 et MC-PROC-SUI-2026-001"),
    ("Remplacé", "Les étapes et les documents du parcours client", "MC-PROC-DOC-2026-001", "12/10/2026", "Remplacé", "PROCEDURES_GERANT", "Remplacée par la section « documents » des deux nouvelles procédures"),
    ("Remplacé", "Dispositif « déployez la machine » (antérieur à la charte)", "—", "06/10/2026", "Remplacé", "DISPOSITIF_DECLENCHEMENT_MISSIONS", "À ne plus utiliser pour un nouveau client"),
]


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Registre"
    ws["A1"] = "LA MAISON DE LA CONFORMITÉ — REGISTRE DES DOCUMENTS DE MÉTHODE"
    ws["A1"].font = Font(bold=True, size=13, color="1A1A2E")
    ws["A2"] = ("Tout document de méthode validé par le gérant est rangé dans le dossier SUPERVISEUR GENERAL indiqué ci-dessous. "
                "La source modifiable de chaque document est dans le sous-dossier _SOURCES du même dossier.")
    ws["A2"].font = Font(italic=True, color="666666")
    cols = [("Famille", 20), ("Document", 55), ("Référence", 24), ("Date", 11), ("Statut", 20), ("Dossier (dans SUPERVISEUR GENERAL)", 48), ("Fichiers", 48)]
    th = Side(style="thin", color="BBBBBB")
    b = Border(left=th, right=th, top=th, bottom=th)
    for j, (c, w) in enumerate(cols, 1):
        x = ws.cell(row=4, column=j, value=c)
        x.font, x.fill, x.border = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1A1A2E"), b
        x.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[x.column_letter].width = w
    couleur = {"Validé": "E2F0D9", "En cours de validation": "FFF2CC", "Remplacé": "EDEDED"}
    for i, d in enumerate(DOCS, 5):
        for j, v in enumerate(d, 1):
            x = ws.cell(row=i, column=j, value=v)
            x.border, x.alignment = b, Alignment(wrap_text=True, vertical="top")
        ws.cell(row=i, column=5).fill = PatternFill("solid", fgColor=couleur.get(d[4], "FFFFFF"))
    dv = DataValidation(type="list", formula1='"Validé,En cours de validation,Remplacé"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"E5:E{len(DOCS) + 40}")
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:G{4 + len(DOCS)}"
    wb.save(OUT)
    print("OK", OUT, len(DOCS), "lignes")


if __name__ == "__main__":
    main()
