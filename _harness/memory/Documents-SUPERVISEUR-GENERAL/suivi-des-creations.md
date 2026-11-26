---
name: suivi-des-creations
description: Tableau SUIVI_DES_DOSSIERS_MDC.xlsx (onglet Créations SCI/SARL, propriétaire, étape, avancement) — état au 12/10/2026 et points ouverts
metadata:
  type: project
---
Le gérant voulait voir les créations de SCI et de SARL avec leur propriétaire et leur avancement. Le tableau `Documents/SUIVI CLIENTS/SUIVI_DES_DOSSIERS_MDC.xlsx` répond à cette demande ; il est généré par `SUIVI CLIENTS/_sources/build_suivi_dossiers.py`.

**Contenu :**
- **Onglets :** Synthèse, Créations, Suivis, Diagnostics.
- **Onglet Créations :** 16 dossiers. Ce sont les 14 du récapitulatif de la coordinatrice (« MON SUIVIE D'ENTREPRISE », 08/10/2026), plus SIM CONSULTING SARL de FOUSSENI et la SCI K FAMILLE de KONE Ibrahim, qui manquaient au récapitulatif.
- **Étapes :** 10 étapes ; l'avancement est égal au rang de l'étape divisé par 10.
- **Deux colonnes séparées :** le statut déclaré par la coordinatrice et l'étape constatée sur les pièces.

**Points ouverts au 12/10/2026 :**
- **RCCM introuvables :** aucun numéro de RCCM ni de NCC n'a été trouvé pour ces 16 dossiers. Il faut obtenir de N'CHO son tableau de bord des dossiers (pièce jointe Gmail du 09/10).
- **Actes à valider par le gérant :** ceux d'OR BLEU (05/10) et de SMART CORPORATION (03/09).
- **Sociétés minières :** IMO, AMT et AMG ont toutes pour associé unique OUATTARA Bazoumana, déclaré chauffeur ; le donneur d'ordre (lien AMOC présumé) n'est pas établi. C'est un sujet de bénéficiaire effectif et de vigilance anti-blanchiment.
- **Rangement :** le dossier d'archives « L'ATELIER DE REVE BY BGK » contient les actes de Winn'Art.

**Why :** pilotage des créations par le gérant.

**How to apply :** mettre à jour le script, puis le relancer. Ne jamais écrire un RCCM qui n'a pas été lu sur une pièce. Voir [[charte-2026]] : la création d'entreprise est hors gamme après la bascule, mais les dossiers en cours sont menés à terme.

**Extension du 12/10/2026** : le PDF annotable (VUE_360_DES_DOSSIERS_MDC.pdf (ex-SUIVI_DES_CREATIONS_A_ANNOTER), 7 pages) couvre aussi les suivis complets (10 étapes calquées sur MC-PROC-ACC-2026-001) et les diagnostics (13 étapes du manuel M03). Les listes ETAPES_SUIVI, ETAPES_DIAGNOSTIC et le dictionnaire ETAT (étapes constatées par client) sont dans build_suivi_dossiers.py. Les onglets Suivis et Diagnostics du classeur ont une colonne « Dernière étape franchie » avec une liste déroulante. Les deux fichiers sont régénérés par script : les saisies manuelles faites dans le classeur sont écrasées.

12/10/2026 : AVE MARIA (renommé « AVE MARIA TRANSIT CI (futur TRACE LOGISTICS CI) ») et ECOMAF 2S ont été ajoutés avec leurs étapes de suivi. AVE MARIA : étapes 1, 2, 3, 5, 6 et 9 ; ECOMAF 2S : 1, 2, 3, 5 et 6. Il leur manque la visite, le plan d'action signé et la formation, et l'Indice reste à recalculer (ancienne note du 08/10). Le classeur a deux colonnes de plus, « Étapes franchies » et « Observation ».

**Vue à 360° et fiches de la semaine (12/10/2026)** : le gérant appelle ce PDF d'ensemble la « vue à 360° des dossiers » ; il a été renommé VUE_360_DES_DOSSIERS_MDC.pdf (l'ancien nom est dans SUIVI CLIENTS/_OBSOLETE). Fiches de la semaine : une page par dossier à annoter au stylet (actions de la semaine, où nous en sommes, blocages, pièces attendues), avec sommaire cliquable et signets. Fichier FICHES_DE_LA_SEMAINE_<lundi>.pdf, produit par `_sources/build_fiches_semaine.py [AAAA-MM-JJ]` ; on en génère un nouveau chaque semaine.

**13/10/2026 : la partie « Suivis complets » de la vue à 360° devient « Travaux préliminaires ».**
- Phase 1, profil de l'entreprise : étapes 1 à 8. Phase 2, plan d'action : étapes 9 à 14. Un trait doré sépare les deux phases.
- L'onglet Excel « Suivis » est renommé « Travaux préliminaires ».
- Variables utilisées : ETAPES_SUIVI (14 étapes) et PHASE_1 = 8.
- ETAT reclassé :
  - Collège {3,4,5,7} ;
  - AVE MARIA {1,2,3,4,5,7} ;
  - ECOMAF {1,2,3,4,5,7}.
- Attention : régénérer les fiches de la semaine écrase les annotations portées sur le fichier de la même semaine. Il faut vérifier avec le gérant avant de le faire.

**Découpage en phases (13/10/2026, demande du gérant).** Dans la vue à 360°, chaque phase a sa colonne et ses cases. Les phases sont définies dans `build_suivi_dossiers.py` :
- PHASES_CREATION : Proposition (étapes 1-2), Actes (3-6), Formalités (7-10) ;
- PHASES_SUIVI : Profil de l'entreprise (1-8), Plan d'action (9-14) ;
- PHASES_DIAGNOSTIC : Engagement (1-3), Collecte et analyse (4-9), Rapport et restitution (10-13).

Les fiches de la semaine affichent aussi les cases par phase, à partir de la semaine du 19/10. Celles du 12/10 n'ont pas été régénérées, pour ne pas écraser les annotations.
- **Créations, mises à jour le 13/10/2026 :**
  - La phase « Proposition » est supprimée : selon le gérant, elle n'existe pas.
  - Il reste 8 étapes en 2 phases : Actes (1 pièces reçues, 2 actes rédigés, 3 validés par le gérant, 4 signés) et Formalités (5 CEPICI, 6 RCCM, 7 rattachement fiscal, 8 terminé).
  - ROBINX n'a aucune étape (proposition non encore acceptée).
  - L'avancement Excel est calculé sur 8.
- 14/10/2026, consigne du gérant :
  - ROBINX est retiré des créations.
  - « KF GROUP (ex-KF IMMO) » est en réalité K FAMILLE SCI. Il est fusionné avec l'ancienne ligne « SCI de M. KONE Ibrahim (SCI K FAMILLE) » en une seule ligne « K FAMILLE SCI » (SCI, création, étape 2 Actes rédigés).
  - Il reste 14 créations.
  - La ligne « KF GROUP » de l'onglet Travaux préliminaires (suivi) n'a pas été touchée.
- Copie de travail demandée par le gérant (14/10/2026) : `Downloads/PROCEDURES LMDC /TRAVAUX PRELIMINIAIRES/` (attention, le nom du dossier se termine par une espace). Après chaque régénération, y recopier la vue à 360°, les fiches de la semaine et le classeur, en remplaçant les anciens fichiers.
