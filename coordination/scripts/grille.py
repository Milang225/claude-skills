"""Grille du POINT GLOBAL DES DOSSIERS (une ligne par dossier en cours).

Même grille pour tous les collaborateurs : le modèle Excel (modele_point.py) et la consolidation
(consolider.py) la lisent ici, pour qu'une colonne ajoutée le soit partout.
Chaque colonne : (clé, titre affiché, aide, type, liste de valeurs ou None, obligatoire).
Types : texte, mois (AAAA-MM), date (AAAA-MM-JJ), montant (FCFA), liste.
"""

STATUTS_DSF = ["Déposés", "En cours", "Non commencés", "Non concerné"]
PAIE = ["À jour", "En retard", "Sans salariés"]
SUIVI = ["Mensuel", "Ponctuel", "Annuel"]
REGIMES = ["RNI", "RSI", "RME", "TEE", "Autre"]
CONTROLE = ["Non", "Oui"]

COLONNES = [
    ("client", "Client (raison sociale)", "Nom exact du client.", "texte", None, True),
    ("collaborateur", "Collaborateur responsable", "Qui tient ce dossier aujourd'hui.", "texte", None, True),
    ("suivi", "Type de suivi", "Mensuel, ponctuel (mission isolée) ou annuel.", "liste", SUIVI, True),
    ("regime", "Régime fiscal", "RNI, RSI, RME, TEE ou autre.", "liste", REGIMES, False),
    ("compta_a_jour", "Comptabilité à jour jusqu'à (mois)", "Dernier mois entièrement saisi et rapproché, ex. 2026-10.", "mois", None, True),
    ("fiscal_depose", "Dernière déclaration fiscale déposée (mois)", "Dernier mois de TVA / impôts mensuels déposé, ex. 2026-10.", "mois", None, True),
    ("social_depose", "Dernière déclaration sociale déposée (mois)", "Dernière période CNPS / ITS déposée, ex. 2026-10 (vide si pas de salariés).", "mois", None, False),
    ("paie", "Paie", "À jour, en retard, ou sans salariés.", "liste", PAIE, False),
    ("dsf", "États financiers de l'exercice précédent", "Déposés, en cours, non commencés, non concerné.", "liste", STATUTS_DSF, True),
    ("pieces_manquantes", "Pièces manquantes chez le client", "Quoi, depuis quand, déjà relancé ?", "texte", None, False),
    ("controle", "Contrôle fiscal ou redressement en cours", "Oui ou non (préciser dans le commentaire).", "liste", CONTROLE, True),
    ("honoraires_impayes", "Honoraires impayés (FCFA)", "Montant dû par le client au cabinet, 0 si rien.", "montant", None, False),
    ("prochaine_echeance", "Prochaine échéance (date)", "Date de la prochaine obligation ou livraison, ex. 2026-12-15.", "date", None, True),
    ("objet_echeance", "Objet de l'échéance", "Ex. TVA de novembre, DSF, réponse au contrôleur…", "texte", None, False),
    ("derniere_intervention", "Dernière intervention (date)", "Dernier jour où quelqu'un a travaillé sur ce dossier.", "date", None, True),
    ("blocage", "Blocage principal", "Ce qui empêche d'avancer (vide si rien).", "texte", None, False),
    ("action_proposee", "Action proposée", "Ce que le collaborateur propose de faire ensuite (un verbe).", "texte", None, True),
    ("pour_quand", "Pour quand (date)", "Échéance de l'action proposée.", "date", None, True),
    ("besoin_gerant", "Besoin du gérant", "Décision ou validation attendue du gérant.", "texte", None, False),
    ("commentaire", "Commentaire", "Tout autre point utile.", "texte", None, False),
]
CLES = [c[0] for c in COLONNES]
TITRES = {c[0]: c[1] for c in COLONNES}
OBLIGATOIRES = [c[0] for c in COLONNES if c[5]]
