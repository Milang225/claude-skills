---
name: regle-jamais-cloturer-mois
description: "RÈGLE gérant : ne jamais clôturer ni verrouiller un mois du journal — on revient ajouter des factures oubliées ; l'intégrité passe par la traçabilité"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6aef6690-0ffd-4549-80a2-d8ab236265a5
  modified: 2026-11-07T16:45:52.754Z
---

Le gérant refuse toute clôture ou tout verrou de mois sur le journal (décision du 07/11/2026) : « on peut oublier des factures et revenir plusieurs mois après pour ajouter des opérations ».

**Why:** la réalité des clients MDC, c'est des pièces qui arrivent en retard ; un verrou bloquerait la tenue.

**How to apply:** ne jamais proposer de verrou de période. Pour l'intégrité, passer par l'historique des versions, l'annulation tracée, le marquage « saisie tardive », les photographies d'empreinte à chaque transmission et la liste des écarts depuis la transmission. Prompts de mise en œuvre : `~/CRM/PROMPTS_INTEGRITE_COMPTABLE.md` (P0–P6, non exécutés à cette date ; ne pas toucher le staging). Voir [[pre-controle-anti-redressement]].

**État au 07/11/2026 (en attente, « pas maintenant ») :** prompts simplifiés en A/B/C dans `~/CRM/PROMPTS_INTEGRITE_COMPTABLE.md`. Deux bugs du moteur repérés sur la copie locale du 06/10, NON corrigés : (1) `eqEcrituresAuto` retire TOUTES les pièces `reglement-facture` dès qu'un relevé existe, y compris les règlements caisse → caisse sous-évaluée ; (2) contrôle E3 codé `ok: true` en dur. Le gérant veut d'abord « écritures justes, balance équilibrée, grand livre à jour » et ne veut pas qu'on complique : trancher soi-même les détails.

**Mise à jour 07/11/2026 — A, B, C CODÉS (non déployés)** : branche locale `integrite-comptable` du dépôt `~/Desktop/02_MDC INTERNE/SITE` (commits 5da768e, 77eb220, 2f96fc2, non poussés). Les deux bugs sont corrigés (caisse, E3). 21/21 tests OK ; VERIF_CONTRAT ne signale que la rupture préexistante `/equipe/staff/*/activity`. Les tests sur banc (`test_import_libre`, `test_reglements_achats`) exigent un `test-server.js` NEUF (port 4100) pour chacun. ⚠ La lecture de la production a été refusée : comparer la copie locale au serveur AVANT tout déploiement. Les déclencheurs SQLite (`trg_jl_*`) tracent toute modification du journal ; ils sont recréés au montage d'après les colonnes réelles.
