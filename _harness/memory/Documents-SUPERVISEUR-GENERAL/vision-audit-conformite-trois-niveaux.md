---
name: vision-audit-conformite-trois-niveaux
description: "Vision de l'audit de conformité fixée par le gérant le 18/10/2026 — trois niveaux dans l'ordre (obligations, justesse du déclaré, exposition) ; kit d'outils dans SUPERVISEUR GENERAL/KIT_COLLABORATEUR_DIAGNOSTIC_2026"
metadata:
  node_type: memory
  type: project
  originSessionId: 6b365445-a2c7-4961-aa58-be2b71df576b
  modified: 2026-10-18T03:56:39.238Z
---

Le gérant veut un audit de conformité simple, dont la vision est fixée en amont (fiche de cadrage à la réunion de lancement). Trois questions dans l'ordre :
1. L'entreprise remplit-elle ses obligations déclaratives, de paiement et documentaires (fiscal, comptable, social CNPS, droit du travail) ? Outils : grilles déclaratives fiscale et CNPS au format de la grille TIM7, audit documentaire.
2. Ce qu'elle déclare est-il juste ? Outils : étude comparée du CA (relevé, déclaré, états financiers), dépouillement des relevés, masse salariale à 4 sources, concordance.
3. Combien risque-t-elle ? Droits simples par nature (BIC, IMF, TVA, TSE, patente, TEE, RME, IRVM, retenues, ITS, CNPS) puis 3 scénarios et Indice.
Puis mise en conformité (mise à jour documentaire, régularisation) au plan d'action.

**Why :** demande du gérant le 18/10/2026 ; il dit « audit » (sa procédure de l'audit complet en 20 étapes, 16/10/2026, fait foi) alors que la charte dit « diagnostic » — ne pas le reprendre à chaque fois.

**How to apply :** tout nouvel outil ou livrable d'audit se range dans l'un des trois niveaux. Note de vision : KIT_COLLABORATEUR_DIAGNOSTIC_2026/00_VISION_DE_L_AUDIT_DE_CONFORMITE (MC-PROC-AUD-2026-008). Taux vérifiés dans le CGI 2026 : TSE 0,1 % art. 1084 ; TEE 5 %/4 % art. 77. Voir [[charte-2026]] et [[documents-sobres-sans-style-ia]].

**Kit définitif (18/10/2026)** : SUPERVISEUR GENERAL/AUDIT_DE_CONFORMITE_MDC — 00_LE_DISPOSITIF (document maître), 1_CADRE, 2_OUTILS (13 outils numérotés 0.x, Q1.x, Q2.x, Q3.x, FIN), 3_MODELES_DE_LIVRABLES (L01 à L20, PDF et Word). Questions dans les mots du gérant : obligations de déclaration et de paiement ; déclarations conformes à la réalité ; combien vous risquez. Générateur : _SOURCES/build_kit_definitif.py.

**Réorganisation du 18/10/2026 (après-midi)** : le kit s'appelle désormais SUPERVISEUR GENERAL/DIAGNOSTIC_COMPLET (ex-AUDIT_DE_CONFORMITE_MDC) — 00_BRIEFING_OUTILS_ET_LIVRABLES et 00_LE_DISPOSITIF à la racine ; 1_OUTILS/1_DOCUMENTS_DE_CADRE (1.1 à 1.7, livret refait : LIVRET_DU_COLLABORATEUR_AUDIT) et 1_OUTILS/2_OUTILS_DE_TRAVAIL ; 2_LIVRABLES (L01 à L22). Ordre voulu par le gérant : Q2.1 étude comparée du CA, Q2.2 matrice des anomalies comptables (juste après), Q2.3 catégorisation des relevés bancaires (ex-dépouillement), Q2.4 concordance. Calendrier de l'outil 0.1 = étapes du dispositif (J0, 10, 12, 20, 26, 28, 30, 31, 39, 44). L22 Tableau de bord de synthèse : demandé par le gérant parce que le client ne peut pas tout lire — en tête du dossier définitif. Sources des outils : KIT_COLLABORATEUR_DIAGNOSTIC_2026/_SOURCES (build_*.py).

**Formulation fixée le 26/10/2026 (bandeau de l'atelier et document explicatif MC-PROC-AUD-2026-012, DIAGNOSTIC_COMPLET/00_LES_TROIS_QUESTIONS_DE_L_AUDIT) :** 1. Vos obligations : l'entreprise remplit-elle ses obligations fiscales, comptables et sociales ? 2. La réalité : ce qu'elle déclare et ce qu'elle paie correspond-il à la réalité ? 3. Le risque : en cas de non-conformité, à quoi s'expose-t-elle ? En une phrase : ce qu'elle devait faire, l'a-t-elle fait ? ; ce qu'elle a fait, l'a-t-elle bien fait ? ; si ce n'est pas le cas, combien cela peut-il coûter ?

**Couverture des obligations (26/10/2026)** : à partir de l'aide-mémoire « Obligations comptables, fiscales et sociales » et de la formation MC-FORM-CREA-2026-001, matrice DIAGNOSTIC_COMPLET/3_ANALYSES/COUVERTURE_DES_OBLIGATIONS (v2 : 83/83 couvertes ; générateur _SOURCES/couverture_des_obligations.py). Source unique des obligations : atelier/revue_des_obligations.json (117 lignes, 23 ajoutées). Nouvel outil Q1.0 Grille des obligations (KIT_COLLABORATEUR_DIAGNOSTIC_2026/_SOURCES/build_grille_obligations.py : profil Oui/Non → applicable, statut par exercice, synthèse). Q1.1 : 13 natures ajoutées (IME, TCE, IRC, contribution employeur annuelle, taxes communales, voirie, accises…), intitulés alignés sur atelier/regimes.py. Q1.2 : DASC + feuille « Contrôle de la paie » (minimum, ancienneté, heures sup., transport, brut et cotisations CNPS, sanction en argent ; plafonds et barèmes marqués « à vérifier »). 6 pièces ajoutées (catalogue_pieces.py et audit documentaire 60 pièces).
