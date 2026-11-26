---
name: egci-etats-financiers-2022-2025
description: EGCI SARL (NCC 2242336W) — hypothèses retenues par le Gérant pour les états financiers 2022-2025 et état du dossier au 13/11/2026
metadata:
  node_type: memory
  type: project
  originSessionId: ec76ffa0-2e6d-45cc-b991-5809e98ccd65
  modified: 2026-11-13T22:07:49.602Z
---

EGCI SARL, NCC 2242336W, Gérante Mme ATTOLOU MONVIGNON Martine. Projet d'états financiers 2022-2025 établi le 13/11/2026 dans `~/Documents/DOSSIER CLIENTS/EGCI SARL/ETATS_FINANCIERS_2022-2025/` (scripts régénérables dans `_TRAVAIL/`).

Décisions du Gérant (13/11/2026) :
- création 06/03/2022 ; capital 1 000 000 libéré en numéraire ; SARL ;
- CA **nul de 2022 à 2024, 5 000 000 en 2025** (3ᵉ version du 13/11/2026, après 0/0/14 M/0 puis 5 M par an) ;
- **charges de chantier seulement en 2025** (matériaux 2 500 000, tâcherons 1 000 000 en 621, carburant 200 000), toutes réglées ; constitution 350 000 en 2022, réglée ; TEE 2022 payée selon e-impôts. Le Gérant voulait une caisse à 21 000 : impossible sans inventer d'opération (caisse 483 334 en 2022-2024, 1 683 234 en 2025 après le dépôt en banque) ;
- régime TEE ; aucune paie 2022-2025 (pas d'immatriculation CNPS sur ces exercices). **Mise à jour 19/11/2026 : immatriculation employeur CNPS n° 411 507** ; bordereau 4T 2026 enregistré le 18/11/2026 (2 salariés à 75 000/mois, base 450 000, cotisations 111 375) ; d'après le Gérant, 4 trimestres déclarés car l'attestation de mise à jour exige une année de cotisations payée — seul le bordereau 4T 2026 est en pièce (`PIECES_ADMINISTRATIVES/`). Certificat de non-ouverture de procédure collective obtenu le 18/11/2026 ;
- banque : **compte GTCO** CI163 01206 000000368709 06, relevé 2025 reçu le 17/11/2026 (`PIECES/RELEVE_GTCO_EGCI_2025.pdf`) : solde 0 au 01/01 et au 31/12/2025, dépôt de 100 100 le 14/07 (traité comme versement de la caisse via 585), frais et TOB 120 050 en 6318, agios 104, RCCM 6 500, régularisation « fees recovery » 26 554 en 758. Aucune banque avant 2025 (ne pas en inventer). Résultat 2025 : 939 900 ;
- charges « de base » estimées ; **charges fiscales constatées dans l'exercice de la période même si payées en 2026** (TEE émise relevée sur e-impôts : 2022 166 666 payée 15/11/2022 ; 2023 250 000 ; 2024 260 000 ; 2025 260 000 ; 2026 275 000 ; total en cours 1 045 000).

**Why:** le Gérant a corrigé deux fois (banque inventée, TEE estimée) : ne rien inventer qu'il n'a pas donné.
**How to apply:** à réception des pièces, remplacer les estimations dans `generer_ecritures_egci.py`, relancer `construire_classeur_egci.py`, puis le contrôle, l'auditeur et `verifier_egci.py` (vérification indépendante, rapprochement ligne à ligne avec le relevé GTCO). Points ouverts : capitaux propres sous la moitié du capital 2022-2024 (−26 666 en 2024) ; caisse à justifier ; DTEE 2023-2024 à 0 ; dettes fournisseurs à confirmer ; tiers « à nommer » ; PV d'AGO non tenus (résultats en 1301/1309). Contrôlé et validé le 14/11/2026 (0 bloquant ; classeur régénéré). Le 14/11/2026 le Gérant a précisé que l'envoi va d'abord au superviseur comptable M. SOGBOU (lmdccomptabilitesup@gmail.com) pour corrections, liasses SMT 2022-2025 et ordre de saisie Sage, retour au Gérant avant visa : brouillon créé. Brouillon client supprimé à sa demande : le mail à la Gérante (egcicorporate@gmail.com) sera refait après le retour du superviseur. Attention : le mail du 13/11 22:20 (envoyé à l'adresse perso du Gérant) décrivait encore la v2 (5 M/an, dettes 15,15 M). Voir aussi [[jamais-gratuit-ni-delais]].
