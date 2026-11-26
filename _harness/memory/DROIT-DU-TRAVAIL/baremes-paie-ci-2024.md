---
name: baremes-paie-ci-2024
description: "Barèmes fiscaux et sociaux de la paie ivoirienne 2024-2026 (ITS réforme 2024, CNPS, RICF, CMU, FDFP) pour calcul de paie et coût employeur"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d1bfb113-1f9c-4d68-8a1e-b5fb07d505c7
  modified: 2026-07-27T18:00:03.688Z
---

Barèmes de PAIE Côte d'Ivoire 2024-2026 (vérifiés par recherche web juil. 2026 : CLEISS, calculateurs pro, communiqués réforme ITS). Complète [[code-travail-ci-2015]] (qui couvre le Code du travail mais PAS les taux fiscaux/sociaux). Utilisés pour le module de formation RH/paie et l'app « Académie RH & Paie ».

## SMIG
- **75 000 FCFA/mois** depuis le 01/01/2023 (40 h/sem). Sert de base à plusieurs plafonds.

## ITS — Impôt sur Traitements et Salaires (réforme annexe fiscale 2024, en vigueur 01/01/2024)
- Fusion des 3 anciens impôts (IS 1,5 % + Contribution Nationale + IGR) en un **barème progressif UNIQUE**.
- **Base = salaire brut imposable** : PLUS d'abattement 20 %, et la CNPS n'est PLUS déduite de la base (point qui divisait les sources ; retenu : base = brut imposable). Éléments exonérés à retrancher : prime de transport ≤ 30 000 F (**à confirmer**), allocations familiales, remboursements de frais.
- **Barème mensuel marginal (par tranches)** : 0 % ≤ 75 000 · 16 % de 75 001 à 240 000 · 21 % de 240 001 à 800 000 · 24 % de 800 001 à 2 400 000 · 28 % de 2 400 001 à 8 000 000 · **32 %** au-delà de 8 000 000. (Barème annuel = ×12.)
- **RICF (réduction pour charges de famille)** remplace le quotient familial : **5 500 F par demi-part au-delà de la 1re part**, imputée sur l'ITS, plafond **44 000 F (5 parts)**. Formule : réduction = (parts − 1) × 11 000. Parts : célibataire 1, marié 2, **+0,5/enfant** à charge, plafond 5. Ex. marié 2 enfants = 3 parts → 22 000 F ; marié 3 enfants = 3,5 parts → 27 500 F. ⚠️ Beaucoup de calculateurs en ligne se trompent (appliquent 5 500 × (parts−1) au lieu de 11 000 × (parts−1)).

## CNPS (taux 2025, source CLEISS)
- **Retraite/vieillesse 14 %** : **7,70 % employeur + 6,30 % salarié**. Plafond mensuel d'assiette = 45 × SMIG = **3 375 000 F**. (Seule cotisation SALARIALE.)
- **Prestations familiales 5 %** (employeur) · **Maternité 0,75 %** (employeur) · **Accidents du travail/MP 2 à 5 %** selon risque (employeur). Ces 3 branches : plafond d'assiette **70 000 F/mois** → cotisations patronales quasi forfaitaires par salarié.

## CMU (Couverture Maladie Universelle)
- **1 000 F/mois par personne** (assuré + ayants droit), réparti **500 F employeur / 500 F salarié** (CLEISS). En pratique certains employeurs précomptent 1 000 F au salarié.

## FDFP (formation professionnelle, employeur)
- Taxe d'apprentissage **0,4 %** + Taxe formation continue **1,2 %** de la masse salariale = **1,6 %**.

## Contribution employeur (part patronale impôt sur salaires) — À CONFIRMER
- Souvent citée **2,8 % (personnel local) / 12 % (expatrié)** sur le brut. Réforme 2024 a surtout touché la part SALARIALE ; taux patronal post-réforme à vérifier auprès de la DGI.

## Cascade de calcul du net
Brut = base + primes imposables + transport + avantages en nature.
Base ITS = brut − exonérés. ITS net = barème(base ITS) − RICF. CNPS sal = min(assiette; 3 375 000) × 6,3 %. **Net = brut − ITS net − CNPS sal − CMU (500)**.
Coût employeur = brut + CNPS pat (7,7 % plaf. 3,375M + 5,75 % plaf. 70k + AT plaf. 70k) + CMU 500 + FDFP 1,6 % + contribution employeur.

## Déclarations
- CNPS : mensuelle (ou trimestrielle petits effectifs) via e-CNPS.
- Impôts sur salaires (ITS + part patronale + FDFP) : e-impôts, au plus tard le 15 du mois suivant.
