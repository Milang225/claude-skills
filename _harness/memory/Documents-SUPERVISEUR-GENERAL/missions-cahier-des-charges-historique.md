---
name: missions-cahier-des-charges-historique
description: Bouton Missions du formulaire (8775) : cahier des charges visé + délais par mission, historique par client
metadata:
  type: project
---

Demande du gérant (24/10/2026) : « en plus du profil, un cahier des charges pour chaque mission, intégré à un historique de missions pour chaque client, cahier des charges plus délai ». Mise en œuvre dans le formulaire du profil : bouton Missions (en-tête, client ouvert) = historique des missions du client ; carte d'accueil « Toutes les missions » = vue de tous les clients (retards, prochaines échéances).

- Code : `_FORMULAIRE/missions.py` (trames, contrôles, journal, génération du document) + routes /api/mission* dans profil_app.py + JS `missions()` dans page.html. Données : DOSSIER CLIENTS/<client>/MISSIONS/<M001_TITRE>/mission.json (+ document Word et PDF, _historique).
- Trames : états financiers (12 étapes tirées du cahier MABEK MC-CDC-TRANS-2026-001), diagnostic de conformité, suivi mensuel, mission libre. Référence MC-CDC-<CLIENT>-<année>-<n°>.
- Règles de la note MC-NS-2026-009 appliquées par le code : par étape porteur (département + nom), livrable, critère de sortie, date réelle ; visa du Superviseur seulement si complet et sans alerte ; alertes : montant, délai en jours, date antérieure à l'étape dont elle dépend, report sans motif ; après le visa la date initiale est figée, tout report exige un motif ; mission « En cadrage » tant que non visée ; journal automatique ; état du vendredi (faites, en cours, en retard en jours ouvrés, bloquées). Le document n'est établi que sans alerte ; il sort avec « Projet en attente du visa » tant que non visé.
- Visa : décision du gérant (26/10) : le visa revient au Superviseur général de l'annuaire (SOGBOU), le gérant ne figure plus dans la liste de ceux qui visent. « Je suis » (liste de l'annuaire, mémorisé dans le navigateur) signe le journal.
- Testé sur TESTPROFIL (nettoyé). Les cahiers MABEK et Collège existants (hors plateforme) ne sont pas repris dans l'historique. Voir [[cahiers-des-charges-et-delais]] et [[formulaire-profil-entreprise]].

- 26/10/2026 : conformément à [[equipe-definit-les-etapes]] et à la décision du gérant, les trames ne préchargent AUCUNE étape : elles donnent le cadre (objet, règles communes, préalables, conditions de clôture, partage des travaux). La mission naît avec zéro étape ; le contrôle réclame « aucune étape définie » ; Superviseur et Coordination ajoutent chaque étape (bouton Ajouter une étape). Les listes d'étapes de TRAMES dans missions.py ne servent plus qu'à mémoire, non chargées.
