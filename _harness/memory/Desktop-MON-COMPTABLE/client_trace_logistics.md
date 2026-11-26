---
name: client-trace-logistics
description: Client TRACE LOGISTICS — SARL PM CI — Dossier exercice 2025 — Balance SMT et écritures SYSCOHADA produites 21/06/2026.
metadata: 
  node_type: memory
  type: project
  originSessionId: 489d2c42-e377-49c0-9928-1f3fbf20f979
---

# Client : TRACE LOGISTICS

> ⛔ **Correctif 11/11/2026 (notes de revue de visa)** : comptes vérifiés dans le plan AUDCIF. Anciennes erreurs : 6313 (= location de coffres) → **6413** ; 4611 (= apports en nature) → **4621** CCA ; 4616 → **4612** souscription ; 629000 (inexistant) → **6318** ; 624100/624200 (entretien) → **6052/6051** ; 626000 (études) → **6281** ; 604000 → **6055** ; 6631 (indemnité de logement) → **6611** ; 701 pour des services → **7061**. Toute écriture passe par le module skill `ecritures-sans-faute` (script de contrôle obligatoire).

> ⚠️ L'**ordre de saisie du 21/06/2026** (`ORDRE_SAISIE_TRACE_LOGISTICS_20260621.pdf`) contient ces erreurs (12 erreurs bloquantes au contrôle du 11/11/2026) et toutes ses écritures sont datées du 31/12 : il est à refaire avant toute saisie Sage.

## Identité

| Champ | Valeur |
|---|---|
| Raison sociale | TRACE LOGISTICS |
| NCC | 2404990E |
| Forme juridique | SARL (PM) |
| Secteur | Transport / Logistique |
| Banque | BMS (Banque — RIB fourni en PDF image, non OCRisable) |
| Régime fiscal | TEE (Taxe État Entreprenant) — Liasse SMT |

## Données exercice 2025

| Paramètre | Valeur |
|---|---|
| Période | 01/01/2025 → 31/12/2025 |
| Capital social | 25 000 000 FCFA (entièrement libéré) |
| CCA gérant (4621) | 27 000 000 FCFA |
| Versement bancaire | 52 000 000 FCFA le **15/07/2025** (BMS) |
| Solde BMS au 31/12 | **51 706 150 FCFA** (relevé réel) |
| Frais bancaires déduits | 293 850 FCFA (52 000 000 − 51 706 150) |
| Chiffre d'affaires | 5 000 000 FCFA (encaissé en **caisse**) |
| Caisse finale | ~600 000 FCFA (⚠️ rapprochement non bouclé — voir note) |
| Effectif | 1 employé |
| Salaire brut mensuel | 75 000 FCFA |
| Loyer mensuel | 60 000 FCFA |
| TEE | 250 000 FCFA (annuel) |
| CNPS | **Non applicable** (pas de charge sociale CNPS déclarée) |

## Résumé comptable 2025 (RÉVISÉ — taux ITS réforme 2024 confirmés)

| Indicateur | Montant |
|---|---|
| CA | 5 000 000 |
| Total charges constatées | **2 789 050** |
| **Résultat net** | **+ 2 210 950** |
| Total Actif (bilan SMT) | **54 486 150** |
| Capital | 25 000 000 |
| CCA (HC) | 27 000 000 |
| Dettes fiscales (HD) | **275 200** |
| Balance soldes D=C | **57 275 200** |

### Détail charges 2025

| Compte | Libellé | Montant |
|---|---|---|
| 661000 | Salaires bruts (75K × 12) | 900 000 |
| 6413 | CE patronale **1,2%** × 900K | **10 800** |
| 6414 | FDFP TA 0,4% × 900K | 3 600 |
| 6415 | FDFP TFPC **1,2%** × 900K | **10 800** |
| 6418 | TEE | 250 000 |
| 6055 | Fournitures | 120 000 |
| 622000 | Loyer (60K × 12) | 720 000 |
| 6052 | Électricité (15K × 12) | 180 000 |
| 6051 | Eau (5K × 12) | 60 000 |
| 6281 | Télécoms (20K × 12) | 240 000 |
| 6318 | Frais bancaires BMS | 293 850 |
| **TOTAL** | | **2 789 050** |

### Dettes restantes au 31/12 (HD)

| Compte | Libellé | Montant |
|---|---|---|
| 447201 | CE à payer (1,2%) | 10 800 |
| 447202 | ITS salarié (= 0, SMIG exonéré) | 0 |
| 4478 | FDFP à payer (1,6%) | 14 400 |
| 446 | TEE à payer | 250 000 |
| **TOTAL HD** | | **275 200** |

### Taux ITS 2024 appliqués
| Composante | Taux | Montant annuel |
|---|---|---|
| ITS salarié SMIG 75K | **0 FCFA** (exonéré) | 0 |
| CE Part Employeur | **1,2%** | 10 800 |
| FDFP TA | 0,4% | 3 600 |
| FDFP TFPC (réforme 2024) | **1,2%** | 10 800 |
| FDFP total | **1,6%** | **14 400** |

## ⚠️ Note de rapprochement caisse (non résolue au 21/06/2026)

```
CA encaissé caisse               + 5 000 000
Charges payées caisse            − 2 220 000
  (loyer 720K + élec 180K + eau 60K
   + télécoms 240K + fournitures 120K
   + salaire net 900K — ITS = 0, net = brut)
─────────────────────────────────────────────
Solde théorique calculé          = 2 780 000
Solde annoncé par le client      ≈   600 000
Écart non documenté              = 2 180 000
→ Transactions caisse complémentaires à identifier
```

## Fichier modèle Excel
`/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/TRACE LOGISTICS/MODELE_SAISIE_TRACE_LOGISTICS_20260620.xlsm`
- Macros VBA : MDC_FilterPeriod() + MDC_ShowAllYears()
- Feuilles : PARAMETRES / SAISIE / BALANCE / TRESORERIE
- Exercices couverts : 2019–2026 (colonnes dynamiques filtrées par date)

## Méthode comptable appliquée (confirmée 21/06/2026)

**MÉTHODE MDC OBLIGATOIRE :** toujours deux temps :
1. Constatation : D Charge / C Tiers
2. Règlement : D Tiers / C Caisse ou Banque

**NE PAS aller directement D Charge / C Caisse — refusé par le client.**

**Why** : Lors de la session 21/06/2026, le client a explicitement recadré la méthodologie
après une première version qui allait directement en Charge/Caisse.
Cela s'applique à TOUS les dossiers MDC, pas seulement TRACE LOGISTICS.

**How to apply** : Pour chaque charge ou opération, toujours passer par un compte tiers
intermédiaire (401, 422, 447, 446, 4478, etc.) avant de pointer vers 521 ou 571.
