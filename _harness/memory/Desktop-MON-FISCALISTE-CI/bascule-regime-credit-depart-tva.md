---
name: bascule-regime-credit-depart-tva
description: "Changement de régime en cours d'année : ventiler TVA/AIRSI/TSE/paliers pré/post bascule ; crédit de départ = récupérer la TVA des achats de la période non-assujettie"
metadata:
  type: reference
---

**Une entreprise peut changer de régime EN COURS D'ANNÉE** (LERO : TEE jusqu'au 15/09/2025, RSI après). Des factures **sans TVA** et des factures **à 18 %** sur le **même NCC** ne sont PAS une contradiction : c'est la bascule. Vérifier par les **dates** (0 % avant, 18 % après).

**Ventilation du chiffrage :**
- **Période TEE (avant)** : CA taxé aux **paliers TEE+RME** (libératoire) — pas de TVA/AIRSI/TSE sur cette période. Paliers = 50 M×5 % + (CA_TEE−50 M)×6 %.
- **Période RSI (après)** : TVA 18 %, AIRSI 5 %, TSE 0,1 %, IMF sur le seul CA de la période.
- Natures de structure (IMF, IRVM, RIBNC, patente, ITS, CNPS) au niveau annuel tant que les dates des flux manquent.
- **Verrou** : l'attestation de changement de régime (date certaine). Sans elle, garder l'hypothèse haute en variante. Risque inverse : assujettissement rétroactif.

**⭐ CRÉDIT DE DÉPART TVA** (décision gérant LERO, août 2026 : « on va déduire les montants facturés lorsque nous étions à la TEE ») : au passage non-assujetti → réel, on **récupère la TVA d'amont des achats de la période non-assujettie dont les biens ont alimenté des ventes désormais taxées** (neutralité TVA). La déductible n'est donc PAS limitée à la période RSI. À sécuriser par la traçabilité achat TEE → vente RSI. Cas LERO : déductible 3 415 788 → **14 977 683**, TVA nette 2025 → **10 245 427**, exposition consolidée → **91 684 469**.

**Tableau de passage compta→fiscal obligatoire** quand la TVA comptable (tout le CA à 18 %) ≠ la TVA fiscale due (période RSI) : documenter l'écart, sinon on croit à une contradiction. Skill mdc-expert **§36.4/§36.5/§36.6**. [[toujours-verifier-dgi-2026]] [[paliers-franchis-changement-regime]] [[client-lero-forage]]
