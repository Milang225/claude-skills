---
name: journal-portail-ecritures
description: Le journal tenu au portail produit enfin des écritures (nature → compte, TVA 18/118), et le Suivi fiscal voit les dossiers sans fichier importé
metadata:
  type: project
---

**28/08/2026 — le journal saisi au portail était comptablement invisible.** Deux aveuglements successifs, corrigés :

1. **`eqComputeTraitement` ne lisait que les fichiers importés** (`depot_balance_ouverture`, `depot_entreprise_journal`). Cinq dossiers réels — GLOBE, TIM 7, Winn'ART, ASLA, ECOMAF-2S — tiennent leur comptabilité au portail et recevaient « Importez d'abord la balance d'ouverture ». Il se replie désormais sur `eqBaseComptable` (le MÊME générateur que la base comptable) quand aucun fichier n'est importé, et le retour porte `origine` / `sur_pieces`.
2. **`eqEcrituresAuto` ne lisait pas `depot_journal_lignes`.** Il connaissait ventes FNE, achats TVA, paie, impôts et relevés — pas le journal du client. GLOBE : 41 lignes, 11,5 M de ventes espèces, **produits affichés = 0**.

**La traduction nature → compte** (section 5 de `eqEcrituresAuto`), sur la liste FERMÉE des 23 natures du journal. Trois règles, aucune invention :
- **La contrepartie va en compte d'attente 471** quand le `support` n'est pas renseigné — et il est **vide sur 100 % des lignes**. Ce n'est pas un pis-aller : le relevé écrit « D 521 / C 471100 » (l'argent est arrivé), le journal écrit « D 471100 / C 701 + TVA » (voici pourquoi). **Les deux attentes s'annulent** — c'est ce qui empêche de compter la banque deux fois.
- **La TVA ne se présume pas** : calculée à **18/118 sur le TTC** uniquement si le dossier est au réel (RSI/RNI). Au TEE l'impôt est libératoire → aucune TVA. Régime non renseigné → aucune TVA, et on le dit.
- **Une nature de charge au CRÉDIT n'est pas elle-même** (une réparation qui rapporte de l'argent) → attente + motif. Même doctrine qu'au relevé.

**Trois natures restent en attente d'arbitrage de la Direction**, nommées à l'écran plutôt que devinées : *Achat de matériel* (immobilisation 244 ou petit matériel 6056), *Transport / carburant* (6053 ou 61), *Eau / électricité / télécom* (605 ou 628). Les natures qui ne disent que le moyen de paiement (« Virement reçu », « Chèque émis »…) restent aussi en attente : le moyen ne qualifie pas l'opération.

**Résultat mesuré sur GLOBE** : produits **15 952 330** (ventes 9 813 770 + services 6 138 559), charges 5 664 376, **TVA collectée 2 871 419**, balance à écart **0**. 6 lignes en attente.

⚠ **PIÈGE RENCONTRÉ, À NE PAS REFAIRE** : `eqEcrituresAuto` n'a PAS accès au tableau `warnings` de `eqBaseComptable` — y écrire lève « warnings is not defined », l'exception est avalée par le `try` de l'appelant, **et le dossier se présente comme VIDE**. Le générateur a maintenant son propre canal `avis`, propagé par `eqEcrituresAplat` (`out.avis`). ⚠ Corrigé aussi : le refus « Aucune donnée comptable » **jetait ses avertissements** — il les porte désormais, sinon la vraie cause reste invisible.

Test durable : `tests/test_suivi_tenue_main.js`. Voir [[base-comptable-crm]] et [[crm-architecture-deploy]].
