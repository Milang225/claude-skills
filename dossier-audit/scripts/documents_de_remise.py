# -*- coding: utf-8 -*-
"""Sommaire, bordereau de transmission et cartographie des destinataires.

Les trois se construisent sur l'INVENTAIRE REEL du dossier : ce qui est dans `_SOURCES_MD/`,
jamais une liste tenue a la main. C'est ce qui evite d'annoncer six documents quand le dossier
en contient treize — le huitieme point bloquant du dossier MABEK.

  python3 documents_de_remise.py LBTECH "<dossier d'audit>"
"""
import os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from donnees_dossier import charger, pivots
from squelettes_audit import entete, aujourdhui, ref

# socle du nom de fichier -> (ordre, titre, objet, destinataire, type de reference, canal)
CATALOGUE = [
    ("SYNTHESE_DE_L_EXPOSITION", "Synthèse de l'exposition",
     "Nature d'impôt par nature d'impôt : ce que la loi imposait, ce qui a été fait, ce que l'écart expose. Commencez par là",
     "client", "SYNT", "espace du client"),
    ("TABLEAU_D_EXPOSITION", "Tableau d'exposition",
     "L'exposition sur une page : nature, exercice, base, droits, position, pièce", "client", "TAB", "espace du client"),
    ("CONSTAT_DE_NON_CONFORMITE", "Constat de non-conformité",
     "L'Indice de conformité, sa décomposition par domaine et les leviers de relèvement", "client", "NCF", "espace du client"),
    ("RAPPORT_AUDIT_CONFORMITE", "Rapport d'audit de conformité",
     "Le rapport principal : méthode, limites, matrices d'anomalies, conseils", "client", "AUD", "espace du client"),
    ("GRILLE_DES_DECLARATIONS", "Grille des déclarations",
     "Nature par nature et période par période : ce qui a été déclaré, ce qui a été payé", "client", "GRILLE", "espace du client"),
    ("AUDIT_DES_PROCEDURES", "Audit des procédures internes et externes",
     "La manière dont les chiffres se forment : qui fait quoi, avec quelle pièce, et ce qui se perd", "client", "PROC", "espace du client"),
    ("AUDIT_DOCUMENTAIRE", "Audit documentaire",
     "Les pièces inventoriées une à une, et le score documentaire", "client", "DOC", "espace du client"),
    ("MATRICES_ANOMALIES_ET_CHIFFRAGES", "Classeur des matrices d'anomalies et des chiffrages",
     "Le détail de chaque calcul, poste par poste, avec sa méthode", "client", "MAT", "espace du client"),
    ("LE_POINT_ET_LES_BONS_USAGES", "Le point et les bons usages",
     "Les sujets arrêtés avec le dirigeant, et ce que chacun coûte", "client", "PT", "espace du client"),
    ("PLAN_D_ACTION", "Plan d'action de mise en conformité",
     "Quatre rangs : les pièces, les actes, les déclarations, les usages", "client", "PLAN", "espace du client"),
    ("PROFIL_ET_VENTE_DE_VEHICULES", "Note particulière au dossier",
     "La question posée par le dirigeant, traitée à part", "client", "PROF", "espace du client"),
    ("NOTE_DE_CHIFFRAGE_DES_EXPOSITIONS", "Note de chiffrage des expositions",
     "Poste par poste : assiette, taux, droits, intérêts, majoration", "sensible", "EXPO", "remise séparée"),
    ("NOTE_AU_COMPTABLE", "Note d'instructions au comptable",
     "Les instructions de tenue, les écritures de régularisation, le calendrier déclaratif", "comptable", "NC", "par le dirigeant"),
    ("MODELES_ACTES_JURIDIQUES", "Modèles d'actes et instructions juridiques",
     "Les bases de travail des actes à prendre", "conseil", "ACT", "par le dirigeant"),
    ("SCRIPT_DE_RESTITUTION", "Script de restitution", "Conduite de l'entretien", "interne", "SCR", "ne se remet pas"),
]
QUI = {"client": "Le dirigeant", "sensible": "Le dirigeant, lui seul",
       "comptable": "**Le comptable**, ou le cabinet qui prendra le dossier",
       "conseil": "**L'avocat ou le notaire** qui établira les actes", "interne": "Interne à l'Agence"}
USAGE = {"client": "", "sensible": "Document sensible : ne pas faire circuler",
         "comptable": "Les instructions de tenue et de régularisation",
         "conseil": "Les bases de travail des actes à prendre", "interne": "Ne figure sur aucun bordereau"}


def inventaire(dest):
    """Ce que le dossier contient reellement, dans l'ordre de lecture du catalogue."""
    src = os.path.join(dest, "_SOURCES_MD")
    presents = [x[:-3] for x in os.listdir(src) if x.endswith(".md")] if os.path.isdir(src) else []
    presents += [os.path.splitext(x)[0] for x in os.listdir(dest) if x.endswith(".xlsx")]
    publies = [x for x in os.listdir(dest) if x.endswith((".pdf", ".docx", ".xlsx"))]
    out, hors, attente = [], list(presents), []
    for socle, titre, objet, qui, type_, canal in CATALOGUE:
        trouve = [x for x in presents if x.startswith(socle)]
        if not trouve:
            continue
        for x in trouve:
            if x in hors: hors.remove(x)
        if any(q.startswith(socle) for q in publies):
            out.append((titre, objet, qui, type_, canal))
        else:
            attente.append(titre)      # encore un squelette : il n'entre dans aucun inventaire
    garder = lambda x: not x.startswith(("SOMMAIRE", "BORDEREAU", "CARTOGRAPHIE", "evaluation", "synthese_indice", "build_"))
    return out, [x for x in hors if garder(x)], attente


def sommaire(p, inv):
    remis = [x for x in inv if x[3] != "interne"]
    t = entete(p, "sommaire du dossier d'audit de conformité de %s" % p["raison_sociale"], p["formule"], "SOM")
    t += ("Le dossier compte %d documents. Ils se lisent dans l'ordre ci-dessous : les premiers disent où vous en "
          "êtes et combien cela pèse, les suivants établissent les constats, les derniers disent quoi faire et à "
          "qui les remettre.\n\n" % len(remis))
    t += "| Ordre | Document | Ce qu'il contient | Référence |\n|---|---|---|---|\n"
    for i, (titre, objet, qui, type_, canal) in enumerate(remis, 1):
        t += "| %d | %s | %s | %s |\n" % (i, titre, objet, ref(p, type_))
    t += "\nLa cartographie des destinataires, jointe au dossier, indique qui reçoit quoi.\n"
    return t


def bordereau(p, inv):
    joints = [x for x in inv if x[3] == "client"]
    part = [x for x in inv if x[3] in ("comptable", "conseil")]
    sens = [x for x in inv if x[3] == "sensible"]
    t = entete(p, "bordereau de transmission du dossier d'audit de conformité", p["formule"], "BT")
    t += "Nous vous remettons, à la date ci-dessus, les documents suivants. Ils sont déposés dans votre espace et s'y consultent.\n\n"
    t += "| N° | Document | Référence |\n|---|---|---|\n"
    for i, (titre, objet, qui, type_, canal) in enumerate(joints + part, 1):
        t += "| %d | %s | %s |\n" % (i, titre, ref(p, type_))
    for titre, objet, qui, type_, canal in sens:
        t += ("\n**Remis séparément, à vous-même :** %s, %s. Ce document est sensible : il n'est pas joint au "
              "présent envoi et ne doit pas circuler.\n" % (titre.lower(), ref(p, type_)))
    t += "\nPour La Maison de la Conformité SARL, le Gérant\n"
    return t


def cartographie(p, inv):
    t = entete(p, "cartographie des destinataires du dossier d'audit de %s" % p["raison_sociale"], p["formule"], "CARTO")
    t += ("Chaque document du dossier a un destinataire et un seul usage. Ceux qui portent la mention « par le "
          "dirigeant » vous sont remis pour que vous les transmettiez vous-même à vos conseils.\n\n")
    t += "| Document | Qui le reçoit | Par quel canal | Ce qu'il en fait |\n|---|---|---|---|\n"
    for titre, objet, qui, type_, canal in inv:
        if qui == "interne":
            continue
        t += "| %s | %s | %s | %s |\n" % (titre, QUI[qui], canal, USAGE[qui] or objet)
    t += ("\nLes travaux internes de notre Agence — conduite de l'entretien de restitution, feuilles de contrôle — "
          "ne figurent pas au dossier remis et ne vous sont pas transmis.\n")
    return t


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        raise SystemExit(__doc__)
    dossier, dest = a[0], a[1]
    D, source = charger(dossier, a[a.index("--json") + 1] if "--json" in a else None)
    p = pivots(D); p["lignes_sans_piece"] = 0
    inv, hors, attente = inventaire(dest)
    print("INVENTAIRE RÉEL : %d document(s) au catalogue" % len(inv))
    for titre, objet, qui, type_, canal in inv:
        print("   %-52s %s" % (titre[:52], qui))
    for x in hors:
        print("   hors catalogue, à rattacher à la main : %s" % x)
    for x in attente:
        print("   PAS AU DOSSIER, encore en squelette : %s" % x)
    nom = p["raison_sociale"].replace(" ", "_").replace("'", "")
    src = os.path.join(dest, "_SOURCES_MD")
    for cle, fonc in (("SOMMAIRE_DU_DOSSIER", sommaire), ("BORDEREAU_DE_TRANSMISSION", bordereau),
                      ("CARTOGRAPHIE_DES_DESTINATAIRES", cartographie)):
        q = os.path.join(src, "%s_%s.md" % (cle, nom))
        open(q, "w", encoding="utf-8").write(fonc(p, inv))
        print("   écrit : %s" % os.path.basename(q))
    print("\nCes trois documents se régénèrent à chaque remise : l'inventaire doit rester celui du dossier.")


if __name__ == "__main__":
    main()
