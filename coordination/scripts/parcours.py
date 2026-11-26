"""Date le parcours d'un nouveau client à partir de sa signature, pour que le Coordinateur sache
quoi lancer, dans quel ordre, par qui, et pour quand.

    python3 parcours.py diagnostic "SAVANE SERVICES SARL" 2026-12-01
    python3 parcours.py suivi "LUMIERE BTP SARL" 2026-12-01 --csv plan.csv
    python3 parcours.py mois "LUMIERE BTP SARL" 2026-12-15      # le cycle d'une échéance

Les étapes, les responsables et les portes de sortie viennent des procédures du cabinet
(04_PROCESSUS_ET_DOCUMENTATION.md et 07_PARCOURS_TYPES.md). Rien n'est inventé ici : ce script ne
fait que poser les dates. Les dates tombent sur des jours ouvrés. Elles restent des PROPOSITIONS :
le Gérant arbitre avant que quoi que ce soit ne devienne une directive.
"""
import argparse
import csv
import datetime as dt
import sys

# Responsables tels qu'ils existent dans le CRM (table teams), et ceux qui n'y sont pas encore.
EQUIPES = {
    "G": ("Gérant", None),
    "CM": ("Chargé de mission", "compta"),
    "FISC": ("Équipe Fiscalité & Droit des Affaires", "fiscal"),
    "JUR": ("Département Juridique", "juridique"),
    "2L": ("Département Supervision (second lecteur)", "superviseur"),
    "AD": ("Assistante de direction", "assistantededirection"),
    "DI": ("Département informatique", None),   # pas encore une équipe du CRM
    "CLIENT": ("Le client", None),
}

# (décalage en jours depuis J0, étape, qui, porte de sortie, bloquant)
DIAGNOSTIC = [
    (0, "Engagement : vérifier la lettre signée ET l'acompte reçu", "G",
     "Lettre signée, bénéficiaire effectif identifié (LBC/FT), acompte encaissé", True),
    (0, "Lancement : réunion de lancement, dossier et espace client créés", "CM",
     "Réunion tenue, dossier créé, espace de dépôt ouvert", True),
    (0, "Ouvrir l'espace client sur la plateforme et les accès nominatifs", "DI",
     "Accès remis, catégories de dépôt calquées sur la demande de pièces, dépôt test réussi", False),
    (1, "Envoyer la demande de pièces et la procédure de transmission", "CM",
     "Demande de pièces envoyée avec sa date limite, procédure expliquée", True),
    (3, "Relance 1 de la collecte : lister les pièces manquantes par écrit", "CM",
     "Liste des manquantes envoyée", False),
    (7, "Relance 2 de la collecte : appel du Gérant au dirigeant", "G",
     "Appel passé, engagement du client daté", False),
    (10, "Si des pièces manquent : courrier de périmètre réduit", "G",
     "Courrier envoyé ; les contrôles sans pièce passent en non vérifiable et le délai repart d'ici", False),
    (10, "Cohérence des sources", "CM",
     "Relevés rapprochés de leurs totaux, déclarations rapprochées de leurs accusés ; "
     "incohérences comptables listées pour l'expert-comptable, jamais retraitées par MDC", True),
    (12, "Évaluation des 45 contrôles", "G",
     "Chaque P/NC adossé à une pièce ouvrable, moteur de l'Indice sans erreur", True),
    (20, "Chiffrage de l'exposition", "G",
     "Trois scénarios, chaque montant sourcé sur sa base et son article", True),
    (21, "Revue qualité par le second lecteur", "2L",
     "Checklist qualité signée ; chaque NC critique relu et maintenu", True),
    (22, "Projet de rapport envoyé au client, second acompte facturé", "G",
     "Projet envoyé, facture du solde émise", True),
    (22, "Contradictoire : 8 jours ouvrés laissés au client", "CLIENT",
     "Réponses reçues et intégrées, Indice recalculé si besoin", True),
    (31, "Restitution (1 h 30) : rapport définitif, plan d'action, et proposition de suite "
         "remise séance tenante", "G",
     "Rapport définitif remis, attestation si éligible, proposition de suite remise sur place", True),
    (36, "Clôture : archivage, registre des missions, journal de méthode", "AD",
     "Dossier archivé, registre à jour", False),
    (46, "Relance commerciale planifiée", "G", "Relance faite ou reprogrammée", False),
]

# (semaine, étape, qui, porte de sortie, bloquant)
SUIVI = [
    (1, "Qualification et formule arrêtée (effectif, sites)", "G",
     "Formule arrêtée et écrite", True),
    (1, "Engagement : lettre de Suivi 12 mois + lettre de Diagnostic d'entrée", "G",
     "Les deux lettres signées, LBC/FT fait, premier trimestre encaissé", True),
    (1, "Cadrage tripartite (1 h 30) avec le client, son comptable et l'informatique", "CM",
     "Circuit mensuel fixé par écrit : quoi, qui, quand, format, notifications, validation. "
     "Compte rendu signé", True),
    (1, "Lancer le diagnostic d'entrée (les 13 étapes du parcours DIAGNOSTIC)", "CM",
     "Diagnostic lancé, demande de pièces envoyée", True),
    (2, "Implémentation et test de l'espace client", "DI",
     "Espace créé, accès nominatifs du comptable et du dirigeant, échéances paramétrées "
     "avec rappel à J−7, dépôt test réussi", True),
    (3, "Cartographie des risques par nature d'impôt", "FISC",
     "Cartographie écrite, validée par le Gérant", True),
    (3, "Protocole de conformité signé par le dirigeant", "JUR",
     "Protocole signé", True),
    (3, "Indices d'alerte et leurs seuils propres à l'entreprise", "FISC",
     "Seuils écrits et paramétrés", False),
    (4, "Calendrier personnalisé des 12 mois, un responsable par ligne", "FISC",
     "Toutes les échéances fiscales et sociales datées, avec pour chacune : le comptable, MDC "
     "ou le dirigeant", True),
    (4, "Procédure de transmission et engagements mensuels réciproques signés", "CM",
     "Procédure remise et signée, engagements signés", True),
    (4, "Fixer la revue du circuit à 30 jours", "CM", "Date de revue posée", False),
]

# Le cycle de chaque échéance (décalage par rapport à la date d'échéance légale J)
CYCLE = [
    (-7, "Le comptable du client transmet : paie, factures émises et reçues, relevés, "
         "projets de déclarations", "CLIENT", "Tout est déposé sur la plateforme"),
    (-5, "Contrôle avant dépôt : concordance factures / CA déclaré, paie, banque, retenues, calculs",
     "CM", "Contrôle fait, écarts listés"),
    (-3, "Retour écrit au comptable : « bon pour dépôt » ou liste de corrections", "CM",
     "Retour envoyé par écrit"),
    (0, "Dépôt et paiement par le comptable — MDC ne dépose pas", "CLIENT",
     "Déclaration déposée et payée"),
    (2, "Vérifier les accusés de dépôt et les preuves de paiement, les classer au dossier de défense",
     "CM", "Accusés et preuves classés"),
    (5, "Note mensuelle d'une page au dirigeant : ce qui est parti, ce qui a été corrigé, "
        "les alertes du mois suivant", "G", "Note envoyée"),
]


# Jours fériés ivoiriens à date fixe. Les fêtes mobiles (Pâques, Ascension, fêtes musulmanes)
# ne sont PAS ici : elles changent chaque année. Le Gérant corrige la date si une étape tombe
# sur l'une d'elles — le script ne devine pas.
FERIES_FIXES = {(1, 1), (5, 1), (8, 7), (8, 15), (11, 1), (11, 15), (12, 25)}


def ouvre(d):
    """Repousse au prochain jour ouvré, samedis, dimanches et fériés fixes exclus."""
    while d.weekday() >= 5 or (d.month, d.day) in FERIES_FIXES:
        d += dt.timedelta(days=1)
    return d


def ligne(date, etape, qui, porte, bloquant=False):
    nom, cle = EQUIPES.get(qui, (qui, None))
    return {
        "date": date.isoformat(),
        "jour": ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"][date.weekday()],
        "etape": etape,
        "qui": nom,
        "equipe_crm": cle or "",
        "porte_de_sortie": porte,
        "bloquant": "oui" if bloquant else "",
    }


def plan(parcours, client, depart):
    out = []
    if parcours == "diagnostic":
        for dec, etape, qui, porte, bloq in DIAGNOSTIC:
            out.append(ligne(ouvre(depart + dt.timedelta(days=dec)), etape, qui, porte, bloq))
    elif parcours == "suivi":
        for sem, etape, qui, porte, bloq in SUIVI:
            out.append(ligne(ouvre(depart + dt.timedelta(days=(sem - 1) * 7)), etape, qui, porte, bloq))
    elif parcours == "mois":
        for dec, etape, qui, porte in CYCLE:
            out.append(ligne(ouvre(depart + dt.timedelta(days=dec)), etape, qui, porte, dec <= 0))
    else:
        raise SystemExit("parcours inconnu : diagnostic, suivi ou mois")
    out.sort(key=lambda x: x["date"])
    return out


EN_TETE = {
    "diagnostic": "Parcours DIAGNOSTIC — 13 étapes, à partir de la signature",
    "suivi": "Parcours SUIVI — l'entrée, à partir de la signature",
    "mois": "Le cycle d'une échéance — J est la date d'échéance légale",
}

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("parcours", choices=["diagnostic", "suivi", "mois", "creation"])
    p.add_argument("client")
    p.add_argument("date", help="date de signature, ou date d'échéance pour « mois » (AAAA-MM-JJ)")
    p.add_argument("--csv", default=None, help="écrit aussi le plan en CSV (point-virgule)")
    a = p.parse_args()

    if a.parcours == "creation":
        print("Parcours CRÉATION — les étapes ne sont pas reprises ici pour ne rien inventer.\n"
              "Ouvrir la checklist du cabinet :\n"
              "  ~/Documents/BASE DOCUMENTAIRE LMDC/06_PROCEDURES/CHECKLIST_PIECES_CREATION_MDC.xlsx\n"
              "et le dossier ~/DEMARRAGE CLIENT, puis demander au Gérant l'ordre des démarches\n"
              "avant d'en faire des directives. Le CRM a une table dossiers_creation pour le suivi.")
        sys.exit(0)

    try:
        depart = dt.date.fromisoformat(a.date)
    except ValueError:
        raise SystemExit("date illisible : attendu AAAA-MM-JJ")

    lignes = plan(a.parcours, a.client, depart)

    print(f"# {EN_TETE[a.parcours]}")
    print(f"\n**{a.client}** — départ le {depart.strftime('%d/%m/%Y')}. "
          f"{len(lignes)} étapes, dernière le {dt.date.fromisoformat(lignes[-1]['date']).strftime('%d/%m/%Y')}.\n")
    print("| Date | Jour | Étape | Qui | Porte de sortie | Bloquant |")
    print("|---|---|---|---|---|---|")
    for l in lignes:
        d = dt.date.fromisoformat(l["date"]).strftime("%d/%m")
        print(f"| {d} | {l['jour']} | {l['etape']} | {l['qui']} | {l['porte_de_sortie']} | {l['bloquant']} |")

    manque = sorted({l["qui"] for l in lignes if not l["equipe_crm"] and l["qui"] not in ("Gérant", "Le client")})
    print("\n**À savoir avant d'en faire des directives :**")
    print("- Ces dates sont des propositions. Le Gérant arbitre les responsables et les dates.")
    print("- Une étape marquée bloquante ne se saute pas : sans sa porte de sortie, la suivante n'ouvre pas.")
    if manque:
        print(f"- {', '.join(manque)} n'est pas une équipe du CRM : à créer dans `teams`, "
              "ou à confier nommément à quelqu'un.")
    if a.parcours == "diagnostic":
        print("- Les cinq interdits : pas de démarrage sans acompte · pas d'évaluation avant la "
              "cohérence des sources · pas de projet sans revue qualité · pas de rapport définitif "
              "sans contradictoire · pas de restitution sans proposition de suite.")

    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()), delimiter=";")
            w.writeheader()
            w.writerows(lignes)
        sys.stderr.write(f"CSV écrit : {a.csv}\n")
