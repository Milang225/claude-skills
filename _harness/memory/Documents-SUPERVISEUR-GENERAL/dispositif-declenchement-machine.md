---
name: dispositif-declenchement-machine
description: "« Déployez la machine » — dispositif de déclenchement des missions Suivi global / Audit (fiches client, procédures, outil machine.py)"
metadata:
  node_type: memory
  type: project
  originSessionId: a5fbd61b-6be8-4016-b815-ce1a7f62cbe8
  modified: 2026-10-06T12:44:19.813Z
---

Le 06/10/2026, le gérant a demandé que l'ordre « déployez la machine du suivi / de l'audit » déroule automatiquement un ensemble de procédures. Il veut aussi qu'une fiche courte soit remise au client, avec les objectifs, les étapes et les délais.

Le dispositif se trouve dans `SUPERVISEUR GENERAL/DISPOSITIF_DECLENCHEMENT_MISSIONS/` :
- **0_LIRE_D_ABORD :** note de service MC-NS-2026-007 ;
- **1_SUIVI_GLOBAL :** fiche client MC-PRES-SUIVI-2026-001 et procédure MC-PROC-DEPL-SUIVI-2026-001 ;
- **2_AUDIT :** fiche client MC-PRES-AUDIT-2026-001 et procédure MC-PROC-DEPL-AUDIT-2026-001 ;
- **3_OUTIL_DE_DECLENCHEMENT :** registre des déclenchements ;
- **_SOURCES/machine.py :** il porte toutes les données (étapes A01 à A26, S01 à S28, cycle mensuel C01 à C11).

**Commandes :**
- `python3 machine.py modeles` régénère les modèles ;
- `python3 machine.py declencher --client X --offre suivi|audit|audit-suivi --lancement AAAA-MM-JJ [--echeance 10|15|20] [--profil existante|debut] [--sans-paie] [--chef] [--reception] [--exercices] [--essai]`. La sortie va dans `DOSSIER CLIENTS/<client>/00_LANCEMENT_<OFFRE>_<date>/` : la fiche datée à remettre au client, l'ordre de déclenchement et le plan Excel.

**Doctrine retenue (tirée des mails et des documents existants) :**
- **Audit :** 4 semaines à compter du PV de réception complète des pièces. Honoraires réglés avant le démarrage. Seuls les exercices clos sont audités. La DEE appelle une réponse sous 5 jours ouvrés.
- **Suivi (révisé le 06/10/2026 à la demande du gérant), 5 étapes S01 à S28 :**
  - lancement (1 semaine) ; diagnostic d'entrée (2 semaines : audit documentaire, audit des immobilisations, diagnostic du système comptable et du logiciel, social, déclaratif ; remplacé par l'audit dans le parcours audit puis suivi, sauf le diagnostic du logiciel) ;
  - implantation du dispositif comptable (4 semaines : cahier de paramétrage, emboîtement du logiciel du client avec la plateforme documentaire lamaisondelaconformitesarl.net/gestiondocumentaire, qui est la source de vérité, caisse, paie, manuel, formation) ;
  - bilan d'ouverture et mise en service (2 semaines). Option `--profil debut` : le bilan d'ouverture est l'inventaire global de constitution (apports, frais de constitution, investissements, cautions, stock initial, financements, dépenses des fondateurs). Option `--sans-paie`.
  - cycle mensuel C01 à C11 : pièces avant le 5, travaux le 10, arbitrages le 12 (jamais après la communication des montants), montants communiqués 3 jours ouvrés avant l'échéance, visa 2 jours ouvrés avant, échéance le 10, le 15 ou le 20, variables de paie le 20, bulletins et reporting le 25 ;
  - note de conformité trimestrielle.

**Points laissés à l'arbitrage du gérant :**
- première note trimestrielle : trimestre de la mise en service (décision du gérant, 06/10/2026) ; ajout des étapes régularisation CNPS, registres légaux, baux et retenues sur loyers (CGI art. 169 : 12 %, 15 % si bailleur personne morale).
- honoraires du suivi payables d'avance le 5 (contrat AVE MARIA) ou à terme échu (St-Exupéry, MFD) ;
- deux RCCM différents dans les signatures e-mail ;
- modèles automatiques signés « Cabinet de Conseil ».

Voir [[departements-mdc]], [[profil-conformite-client]], [[guide-collaborateur-stabiliser-base]].

**Manuel de procédures type, version 2 (07/10/2026)** : `ECOSYSTEME_SYSTEME_COMPTABLE/4_MANUEL_DE_PROCEDURES/generer_manuel.py`, 16 chapitres numérotés automatiquement, aligné sur le suivi global.
- Paramètres facultatifs : `mission.profil` (existante | debut), `outil.tenue` (agence | client | partagee), `associes[]`, `baux[]`, `mobile_money[]`, secteur `transit` (débours).
- Textes vérifiés dans le CGI 2026 : art. 18 bis, 84 bis (2 %), 169 (12 %, ou 15 % si le bailleur est une personne morale), 180-1, 852-4 et 854. Vérifié aussi dans l'AUSCGIE : approbation des comptes dans les 6 mois.
- Exemple : ETS NOUVELLE DISTRIBUTION, MC-PROC-NEGOCE-2026-012.
- La v1 est dans `_OBSOLETE/`. Les trois copies (ECOSYSTEME, ECOSYSTEME_1, BASE DOCUMENTAIRE/KIT) sont synchronisées par rsync.

**Modèle du diagnostic d'entrée (07/10/2026)** : MC-DIAG-ENT-2026-001, dans `1_SUIVI_GLOBAL/DIAGNOSTIC_ENTREE/`, généré par `_SOURCES/build_diagnostic_entree.py`.
- Classeur de 11 onglets ; la note d'entrée est calculée à partir des constats (−5, −3 ou −1, sur 7 domaines pondérés).
- Rapport type pour le dirigeant.
- Formules vérifiées avec la bibliothèque `formulas`, car Excel ne répond pas à l'AppleScript. Éviter l'apostrophe dans les noms d'onglets portant des formules.
- `machine.py` copie le classeur dans `2_INTERNE` à chaque suivi.

**Manuel du Collège Saint-Exupéry** : MC-MAN-PROC-EDUC-2026-001 (projet, 24 p.), dans `COLLEGE ST EXUPERY 2/08_MANUELS_PROCEDURES/`.
- Script `_SOURCES/personnaliser_manuel.py --publish` : générateur v2, puis adaptations (recettes scolaires, régime de transition RME → RSI, deux caisses, vacataires, calendrier du plan d'action).

**Charte 2026 (11/10/2026)** : ce dispositif est antérieur à la charte ([[charte-2026]]) ; avertissement ajouté au LISEZ-MOI. Le 11/10, l'audit a reçu une phase « profil de l'entreprise » avec les trois inventaires (machine.py, A01 à A30, MC-PROC-DEPL-AUDIT-2026-002) et le classeur a été enrichi (personnel croisé à 4 sources, grille de 62 points et non 64) ; la référence reste M03 et M03 A.
