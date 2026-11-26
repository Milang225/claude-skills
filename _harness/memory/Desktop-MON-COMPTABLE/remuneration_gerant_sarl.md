---
name: remuneration-gerant-sarl
description: "Traitement fiscal, social et comptable SYSCOHADA de la rémunération du gérant SARL et de ses avantages en nature — CI régime réel (IS 25%). Produit session 21/06/2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 489d2c42-e377-49c0-9928-1f3fbf20f979
---

# Rémunération du gérant de SARL — Côte d'Ivoire (régime réel IS)

## I. STATUT JURIDIQUE DU GÉRANT

| Catégorie | Parts sociales | Statut social | CT possible ? |
|---|---|---|---|
| Gérant **majoritaire** | > 50% | Non-salarié (TNS) | ❌ NON |
| Gérant **égalitaire** | = 50% | Non-salarié | ⚠️ sous conditions |
| Gérant **minoritaire** | < 50% | Assimilé salarié | ✅ OUI (fonctions techniques distinctes) |

> Base légale fixation rémunération : **statuts ou AGO** (AUSCGIE art. 323). Jamais unilatérale.

---

## II. DÉDUCTIBILITÉ IS (Art. 18 CGI CI) — 3 conditions cumulatives

1. **Travail effectif** (fonctions réelles documentées)
2. **Montant non excessif** (proportionnel au CA et aux services)
3. **Décision formelle** (PV d'AGO ou clause statutaire)

> ⚠️ **RISQUE** : si rémunération jugée excessive par la DGI → excédent requalifié en **dividendes déguisés** :
> - Réintégration IS : résultat SARL majoré
> - Imposition gérant : **IRVM 15%** (Art. 182 CGI CI)

---

## III. FISCALITÉ DU GÉRANT — ITS (Art. 115 CGI CI)

La rémunération du gérant SARL est **toujours soumise à ITS** (barème progressif), quelle que soit sa quote-part.

**Charges sur rémunération gérant :**

| Charge | Taux (réforme 2024) | Base | Débiteur |
|---|---|---|---|
| ITS (barème) | Progressif − RICF | Brut × 80% | Gérant (retenu SARL) |
| Part Employeur (CE) | **1,2%** (confirmé progiciel 2024) | Brut | SARL |
| FDFP TA | **0,4%** | Brut | SARL |
| FDFP TFPC | **1,2%** (réforme 2024 — doublé) | Brut | SARL |
| **FDFP total** | **1,6%** | Brut | SARL |
| **CNPS** | ❌ **0%** | — | Gérant majoritaire NON affilié |

---

## IV. SCHÉMA D'ÉCRITURES — RÉMUNÉRATION GÉRANT (méthode MDC deux temps)

### Pièce 1 — Constatation bulletin
```
D  6611    Appointements, salaires (gérant)        [brut]
     C  422000  Personnel — rémunérations dues          [net]
     C  447202  État — ITS retenu (salarié)              [ITS]
```

### Pièce 2 — Règlement net par caisse ou banque
```
D  422000  Personnel — rémunérations dues          [net]
     C  571000  Caisse  (ou C 521000 Banque)               [net]
```

### Pièce 3 — Charges patronales ITS (CE+CN) — constatation
```
D  6413    Taxes sur appointements et salaires (CN 1,2 %) [%×brut]
     C  447201  État — CE+CN à reverser                    [%×brut]
```

### Pièce 4 — FDFP (1,6% réforme 2024) — constatation
```
D  6414    FDFP — TA (0,40%)                       [0,40%×brut]
D  6415    FDFP — TFPC (1,20% — réforme 2024)      [1,20%×brut]
     C  4478    État — FDFP à reverser                    [1,60%×brut]
```

### Pièce 5 — Reversement DGI
```
D  447201  CE+CN                                   [montant]
D  447202  ITS retenu                              [montant]
D  4478    FDFP                                    [montant]
     C  521000  Banque (virement DGI e-impots)             [total]
```

---

## V. AVANTAGES EN NATURE (AN)

### Catégories et déductibilité

| Avantage | Compte charge | Déductibilité IS | Base ITS |
|---|---|---|---|
| Logement de fonction | 622000 (loyer) | ✅ si nécessaire | ✅ valeur locative |
| Véhicule — part pro | 624xxx | ✅ quote-part pro | ✅ part perso seule |
| Véhicule — part perso | 624xxx | ❌ à réintégrer | ✅ inclus base ITS |
| Téléphone pro/perso | 6281 | ✅ partiel | ✅ part perso |
| Repas d'affaires justifiés | 625xxx | ✅ | selon montant |
| Domesticité (ménage perso) | — | ❌ | ✅ valeur réelle |

### Écriture AN (neutralisation côté SARL)
```
D  6617    Rémunérations en nature (AN)            [valeur AN]
     C  781000  Transferts de charges d'exploitation     [valeur AN]
```

> Le compte 781 neutralise la charge 6617 dans la classe 6.
> La valeur AN s'additionne au brut en espèces pour **former la base ITS élargie**.

```
Base ITS = Rémunération espèces brute + Valeur des avantages en nature
```

---

## VI. DIVIDENDES vs RÉMUNÉRATION — Arbitrage fiscal

| Critère | Rémunération | Dividendes |
|---|---|---|
| Déductible IS SARL | ✅ OUI | ❌ NON |
| Imposition bénéficiaire | ITS progressif | **IRVM 15%** (Art. 182) |
| CNPS gérant majoritaire | ❌ NON | ❌ NON |
| Charges patronales (CE+CN+FDFP) | ✅ OUI | ❌ NON |
| Compte comptable | 6611 / 6661 | **465000** Associés dividendes |
| Décision | Statuts ou AGO | AGO obligatoire après approbation comptes |

> **Optimum MDC** : mix calibré — rémunération raisonnable (déductible) + dividendes (IRVM flat 15%).

---

## VII. RÉSERVE LÉGALE (rappel SARL)

Avant toute distribution : **10% du bénéfice → réserve légale** (AUSCGIE art. 346)
jusqu'à ce que la réserve atteigne **20% du capital social**.

```
D  130100  Résultat en instance d'affectation   [10% bénéf]
     C  111000  Réserve légale                      [10% bénéf]
```

**Why** : Produit lors de la session de formation fiscale SARL du 21/06/2026, à l'occasion de la question client sur la gestion du gérant de TRACE LOGISTICS (SARL IS 25%).
