# FICHE DE DOCTRINE — DÉCLARATIONS FISCALES e-impôts.gouv.ci (EDI / EFI) — Côte d'Ivoire

> Assimilation intégrale des formulaires de télédéclaration DGI. Source : templates officiels EDI/EFI (`efi-declaration.xlsm` + 10 annexes `edi-*.xlsm`) + captures réelles du dossier RESEAU IVOIRIEN DE MAINTENANCE (NCC 2300433S). **62 natures d'impôt, 1476 champs.** Montants en FCFA.

---

## 0. EDI vs EFI — le mécanisme de télédéclaration

La DGI met à disposition des fichiers Excel à macros pour préparer une déclaration **hors-ligne** puis l'injecter sur le portail sous forme de **fichier XML**. Deux briques :

| Brique | Sigle | Fichier | Rôle | Injection |
|---|---|---|---|---|
| **EFI** | Échange de **Formulaire** Informatisé | `efi-declaration.xlsm` | Formulaire **maître** : choisir le code impôt (62), saisir NCC+période, remplir les champs → **« Génération du XML »** | **Étape 2** de la déclaration en ligne |
| **EDI** | Échange de **Données** Informatisé | 10 fichiers `edi-*.xlsm` | **Annexes détaillées** (listes nominatives ligne par ligne : salariés, retenues, véhicules, déductions TVA…) | **Étape 3** — section *« Transmission des annexes détaillées par EDI »* |


**Procédure type (identique pour toutes les natures) :**
1. Ouvrir le fichier, **activer les macros** (« activer le contenu »).
2. Feuille `DETAIL`/`SAISIE` : choisir le **code impôt** (liste déroulante), saisir **NCC** (format `1234567A`), **mois** et **année**.
3. Renseigner les champs de **saisie [S]** ; les champs **calculés [C]** se remplissent seuls.
4. Cliquer **« Génération du XML »** → le fichier XML est déposé dans `/Documents`.
5. Sur e-impôts : étape 2 (formulaire principal, EFI) ou étape 3 (annexe détaillée, EDI), **charger le XML**.
6. Pièces jointes → Prévisualisation → Confirmation → **télépaiement**.


**Étapes du parcours e-impôts :** `1. Présentation → 2. Formulaire → 3. Pièces jointes → 4. Prévisualisation → 5. Confirmation`.


> ⚠️ **Cohérence code impôt** : le code choisi dans le fichier Excel doit être **identique** à celui sur lequel on déclare en ligne. Éviter les caractères spéciaux. XML trop volumineux → fractionner l'annexe en plusieurs imports.


---

## 1. Catalogue des 62 natures d'impôt (par famille)

Légende : **[S]** champ à saisir · **[C]** champ calculé automatiquement · **\*** obligatoire · *taux* = taux par défaut du template (⚠️ **à revérifier contre l'Annexe Fiscale en vigueur** — cf. mémoire `toujours-verifier-dgi-2026`).


## ▸ TVA & taxes sur le chiffre d'affaires


### TVA — Taxe sur la valeur ajoutée (hors CME/DGE)

*Périodicité : Mensuelle · Échéance : 15 du mois suivant (DGE/CME : 10/15/20) · 23 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **OPERATIONS REALISEES** | | | |
| 1.1 | Chiffre d’affaires total HT | S |  | ✱ |
| 1.2 | Exportations | S |  |  |
| 1.3 | Opérations exonérées légales | S |  |  |
| 1.4 | Opérations exonérées conventionnelles | S |  |  |
| 1.5 | Autres opérations non taxables | S |  |  |
| 1.6 | Différence | C |  | ✱ |
| 1.8 | Livraisons à soi même taxables | S |  |  |
| 1.9 | Chiffre d’affaires taxable HT | C |  | ✱ |
| **§2** | **TVA BRUTE** | | | |
| 2.1 | Chiffre d’affaires taxable HT au taux 18% | S |  |  |
| 2.2 | Chiffre d’affaires taxable HT au taux 9% | S |  |  |
| 2.4 | Montant Taxe au taux 18% | C | 18% | ✱ |
| 2.5 | Montant Taxe au taux 9% | C | 9% | ✱ |
| **§3** | **REGULARISATION TVA ANTERIEUREMENT DEDUITE A REVERSER** | | | |
| 3.1 | Régularisation TVA antérieurement déduite à reverser | S |  |  |
| **§4** | **TOTAL TVA BRUTE (11 + 12 + 13)** | | | |
| 4.1 | Total TVA brute | C |  | ✱ |
| **§5** | **DEDUCTIONS** | | | |
| 5.1 | Taxes déductibles du mois | S |  |  |
| 5.2 | Crédit reporté du mois précédent | S |  |  |
| 5.3 | Total déduction | C |  | ✱ |
| **§6** | **MONTANT DE L’IMPÔT** | | | |
| 6.1 | TVA nette à payer | C |  | ✱ |
| 6.2 | Crédit à reporter | C |  | ✱ |
| 6.3 | Crédit demandé en remboursement | C |  |  |
| 6.4 | En cas de crédit de TVA, merci d’indiquer si vous allez en demander le remboursement | S |  |  |
| 2.3 | Chiffre d’affaires taxable HT au taux 21.31% | S |  |  |
| 2.6 | Montant de la Taxe | C | 21.31% | ✱ |

### TVA_S — Taxe sur la valeur ajoutée (CME/DGE)

*Périodicité : Mensuelle · Échéance : 10/15/20 (DGE/CME) · 23 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **OPERATIONS REALISEES** | | | |
| 1.1 | Chiffre d’affaires total HT | S |  | ✱ |
| 1.2 | Exportations | S |  |  |
| 1.3 | Opérations exonérées légales | S |  |  |
| 1.4 | Opérations exonérées conventionnelles | S |  |  |
| 1.5 | Autres opérations non taxables | S |  |  |
| 1.6 | Différence | C |  |  |
| 1.7 | Livraisons à soi même taxables | S |  |  |
| 1.8 | Chiffre d’affaires taxable HT | C |  |  |
| **§2** | **TVA BRUTE** | | | |
| 2.1 | Chiffre d’affaires taxable HT (taux 18%) | S |  |  |
| 2.2 | Chiffre d’affaires taxable HT (taux 9%) | S |  |  |
| 2.3 | Chiffre d’affaires taxable HT (taux 21.31%) | S |  |  |
| 2.4 | Montant de la Taxe | C | 18% |  |
| 2.5 | Montant de la Taxe | C | 9% |  |
| 2.6 | Montant de la Taxe | C | 21.31% |  |
| **§3** | **REGULARISATION TVA ANTERIEUREMENT DEDUITE A REVERSER** | | | |
| 3.1 | Régularisation TVA antérieurement déduite à reverser | S |  |  |
| **§4** | **TOTAL TVA BRUTE (03 + 04)** | | | |
| 4.1 | Total TVA brute | C |  |  |
| **§5** | **DEDUCTIONS** | | | |
| 5.1 | Taxes déductibles du mois | S |  |  |
| 5.2 | Crédit reporté du mois précédent | S |  |  |
| 5.3 | Total déduction | C |  |  |
| **§6** | **MONTANT DE L'IMPÔT** | | | |
| 6.1 | TVA nette à payer | C |  |  |
| 6.4 | En cas de crédit de TVA, merci d’indiquer si vous allez en demander le remboursement | S |  |  |
| 6.2 | Crédit à reporter | C |  |  |
| 6.3 | Crédit demandé en remboursement | C |  |  |

### TVA_CT — TVA pour compte de Tiers

*Périodicité : Mensuelle · Échéance : 15 du mois suivant · 161 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **TIERS 1** | | | |
| 1.1 | Nom ou Raison sociale du tiers | S |  | ✱ |
| 1.2 | Pays d’origine | S |  | ✱ |
| 1.3 | Nature de la prestation | S |  |  |
| 1.4 | Montant facturé hors taxes | S |  |  |
| 1.5 | Taux (exemple : saisir 18 pour 18%) | S |  |  |
| 1.8 | Montant net de la TVA retenue | C |  |  |
| **§2** | **TIERS 2** | | | |
| 2.1 | Nom ou Raison sociale du tiers | S |  |  |
| 2.2 | Pays d’origine | S |  |  |
| 2.3 | Nature de la prestation | S |  |  |
| 2.4 | Montant facturé hors taxes | S |  |  |
| 2.5 | Taux | S |  |  |
| 2.8 | Montant net de la TVA retenue | C |  |  |
| **§3** | **TIERS 3** | | | |
| 3.1 | Nom ou Raison sociale du tiers | S |  |  |
| 3.2 | Pays d’origine | S |  |  |
| 3.3 | Nature de la prestation | S |  |  |
| 3.4 | Montant facturé hors taxes | S |  |  |
| 3.5 | Taux | S |  |  |
| 3.8 | Montant de la TVA retenue | C |  |  |
| **§4** | **TIERS 4** | | | |
| 4.1 | Nom ou Raison sociale du tiers | S |  |  |
| 4.2 | Pays d’origine | S |  |  |
| 4.3 | Nature de la prestation | S |  |  |
| 4.4 | Montant facturé hors taxes | S |  |  |
| 4.5 | Taux | S |  |  |
| 4.8 | Montant net de la TVA retenue | C |  |  |
| **§5** | **TIERS 5** | | | |
| 5.1 | Nom ou Raison sociale du tiers | S |  |  |
| 5.2 | Pays d’origine | S |  |  |
| 5.3 | Nature de la prestation | S |  |  |
| 5.4 | Montant facturé hors taxes | S |  |  |
| 5.5 | Taux | S |  |  |
| 5.8 | Montant net de la TVA retenue | C |  |  |
| **§6** | **TIERS 6** | | | |
| 6.1 | Nom ou Raison sociale du tiers | S |  |  |
| 6.2 | Pays d’origine | S |  |  |
| 6.3 | Nature de la prestation | S |  |  |
| 6.4 | Montant facturé hors taxes | S |  |  |
| 6.5 | Taux | S |  |  |
| 6.8 | Montant net de la TVA retenue | C |  |  |
| **§7** | **TIERS 7** | | | |
| 7.1 | Nom ou Raison sociale du tiers | S |  |  |
| 7.2 | Pays d’origine | S |  |  |
| 7.3 | Nature de la prestation | S |  |  |
| 7.4 | Montant facturé hors taxes | S |  |  |
| 7.5 | Taux | S |  |  |
| 7.8 | Montant net de la TVA retenue | C |  |  |
| **§8** | **TIERS 8** | | | |
| 8.1 | Nom ou Raison sociale du tiers | S |  |  |
| 8.2 | Pays d’origine | S |  |  |
| 8.3 | Nature de la prestation | S |  |  |
| 8.4 | Montant facturé hors taxes | S |  |  |
| 8.5 | Taux | S |  |  |
| 8.8 | Montant net de la TVA retenue | C |  |  |
| **§9** | **TIERS 9** | | | |
| 9.1 | Nom ou Raison sociale du tiers | S |  |  |
| 9.2 | Pays d’origine | S |  |  |
| 9.3 | Nature de la prestation | S |  |  |
| 9.4 | Montant facturé hors taxes | S |  |  |
| 9.5 | Taux | S |  |  |
| 9.8 | Montant net de la TVA retenue | C |  |  |
| **§10** | **TIERS 10** | | | |
| 10.1 | Nom ou Raison sociale du tiers | S |  |  |
| 10.2 | Pays d’origine | S |  |  |
| 10.3 | Nature de la prestation | S |  |  |
| 10.4 | Montant facturé hors taxes | S |  |  |
| 10.5 | Taux | S |  |  |
| 10.8 | Montant net de la TVA retenue | C |  |  |
| **§11** | **TIERS 11** | | | |
| 11.1 | Nom ou Raison sociale du tiers | S |  |  |
| 11.2 | Pays d’origine | S |  |  |
| 11.3 | Nature de la prestation | S |  |  |
| 11.4 | Montant facturé hors taxes | S |  |  |
| 11.5 | Taux | S |  |  |
| 11.8 | Montant net de la TVA retenue | C |  |  |
| **§12** | **TIERS 12** | | | |
| 12.1 | Nom ou Raison sociale du tiers | S |  |  |
| 12.2 | Pays d’origine | S |  |  |
| 12.3 | Nature de la prestation | S |  |  |
| 12.4 | Montant facturé hors taxes | S |  |  |
| 12.5 | Taux | S |  |  |
| 12.8 | Montant net de la TVA retenue | C |  |  |
| **§13** | **TIERS 13** | | | |
| 13.1 | Nom ou Raison sociale du tiers | S |  |  |
| 13.2 | Pays d’origine | S |  |  |
| 13.3 | Nature de la prestation | S |  |  |
| 13.4 | Montant facturé hors taxes | S |  |  |
| 13.5 | Taux | S |  |  |
| 13.8 | Montant net de la TVA retenue | C |  |  |
| **§14** | **TIERS 14** | | | |
| 14.1 | Nom ou Raison sociale du tiers | S |  |  |
| 14.2 | Pays d’origine | S |  |  |
| 14.3 | Nature de la prestation | S |  |  |
| 14.4 | Montant net de la TVA retenue | S |  |  |
| 14.5 | Taux | S |  |  |
| 14.8 | Montant net de la TVA retenue | C |  |  |
| **§15** | **TIERS 15** | | | |
| 15.1 | Nom ou Raison sociale du tiers | S |  |  |
| 15.2 | Pays d’origine | S |  |  |
| 15.3 | Nature de la prestation | S |  |  |
| 15.4 | Montant facturé hors taxes | S |  |  |
| 15.5 | Taux | S |  |  |
| 15.8 | Montant net de la TVA retenue | C |  |  |
| **§16** | **TIERS 16** | | | |
| 16.1 | Nom ou Raison sociale du tiers | S |  |  |
| 16.2 | Pays d’origine | S |  |  |
| 16.3 | Nature de la prestation | S |  |  |
| 16.4 | Montant facturé hors taxes | S |  |  |
| 16.5 | Taux | S |  |  |
| 16.8 | Montant net de la TVA retenue | C |  |  |
| **§17** | **TIERS 17** | | | |
| 17.1 | Nom ou Raison sociale du tiers | S |  |  |
| 17.2 | Pays d’origine | S |  |  |
| 17.3 | Nature de la prestation | S |  |  |
| 17.4 | Montant facturé hors taxes | S |  |  |
| 17.5 | Taux | S |  |  |
| 17.8 | Montant net de la TVA retenue | C |  |  |
| **§18** | **TIERS 18** | | | |
| 18.1 | Nom ou Raison sociale du tiers | S |  |  |
| 18.2 | Pays d’origine | S |  |  |
| 18.3 | Nature de la prestation | S |  |  |
| 18.4 | Montant facturé hors taxes | S |  |  |
| 18.5 | Taux | S |  |  |
| 18.8 | Montant net de la TVA retenue | C |  |  |
| **§19** | **TIERS 19** | | | |
| 19.1 | Nom ou Raison sociale du tiers | S |  |  |
| 19.2 | Pays d’origine | S |  |  |
| 19.3 | Nature de la prestation | S |  |  |
| 19.4 | Montant facturé hors taxes | S |  |  |
| 19.5 | Taux | S |  |  |
| 19.8 | Montant net de la TVA retenue | C |  |  |
| **§20** | **TIERS 20** | | | |
| 20.1 | Nom ou Raison sociale du tiers | S |  |  |
| 20.2 | Pays d’origine | S |  |  |
| 20.3 | Nature de la prestation | S |  |  |
| 20.4 | Montant facturé hors taxes | S |  |  |
| 20.5 | Taux | S |  |  |
| 20.8 | Montant net de la TVA retenue | C |  |  |
| **§21** | **MONTANT TOTAL** | | | |
| 21.1 | TOTAL DE LA TVA POUR COMPTE DE TIERS A PAYER | F |  | ✱ |
| 1.6 | Montant brut de la TVA retenue | C |  |  |
| 2.6 | Montant brut de la TVA retenue | C |  |  |
| 3.6 | Montant brut de la TVA retenue | C |  |  |
| 4.6 | Montant brut de la TVA retenue | C |  |  |
| 5.6 | Montant brut de la TVA retenue | C |  |  |
| 6.6 | Montant brut de la TVA retenue | C |  |  |
| 7.6 | Montant brut de la TVA retenue | C |  |  |
| 8.6 | Montant brut de la TVA retenue | C |  |  |
| 9.6 | Montant brut de la TVA retenue | C |  |  |
| 10.6 | Montant brut de la TVA retenue | C |  |  |
| 11.6 | Montant brut de la TVA retenue | C |  |  |
| 12.6 | Montant brut de la TVA retenue | C |  |  |
| 13.6 | Montant brut de la TVA retenue | C |  |  |
| 14.6 | Montant brut de la TVA retenue | C |  |  |
| 15.6 | Montant brut de la TVA retenue | C |  |  |
| 16.6 | Montant brut de la TVA retenue | C |  |  |
| 17.6 | Montant brut de la TVA retenue | C |  |  |
| 18.6 | Montant brut de la TVA retenue | C |  |  |
| 19.6 | Montant brut de la TVA retenue | C |  |  |
| 20.6 | Montant brut de la TVA retenue | C |  |  |
| 1.7 | Déductions | S |  |  |
| 2.7 | Déductions | S |  |  |
| 3.7 | Déductions | S |  |  |
| 4.7 | Déductions | S |  |  |
| 5.7 | Déductions | S |  |  |
| 6.7 | Déductions | S |  |  |
| 7.7 | Déductions | S |  |  |
| 8.7 | Déductions | S |  |  |
| 9.7 | Déductions | S |  |  |
| 10.7 | Déductions | S |  |  |
| 11.7 | Déductions | S |  |  |
| 12.7 | Déductions | S |  |  |
| 13.7 | Déductions | S |  |  |
| 14.7 | Déductions | S |  |  |
| 15.7 | Déductions | S |  |  |
| 16.7 | Déductions | S |  |  |
| 17.7 | Déductions | S |  |  |
| 18.7 | Déductions | S |  |  |
| 19.7 | Déductions | S |  |  |
| 20.7 | Déductions | S |  |  |

### TVAPSE — Taxe sur la valeur ajoutée (Producteurs d'Electricité)

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 23 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **OPERATIONS REALISEES** | | | |
| 1.1 | Chiffre d’affaires total HT | S |  | ✱ |
| 1.2 | Exportations | S |  |  |
| 1.3 | Opérations exonérées légales | S |  |  |
| 1.4 | Opérations exonérées conventionnelles | S |  |  |
| 1.5 | Autres opérations non taxables | S |  |  |
| 1.6 | Différence | C |  | ✱ |
| 1.7 | Livraisons à soi même taxables | S |  |  |
| 1.8 | Chiffre d’affaires taxable HT | C |  | ✱ |
| **§2** | **TVA BRUTE** | | | |
| 2.1 | Chiffre d’affaires taxable HT (taux 18%) | S |  |  |
| 2.2 | Chiffre d’affaires taxable HT (taux 9%) | S |  |  |
| 2.3 | Montant de la Taxe | C | 18% | ✱ |
| 2.4 | Montant de la Taxe | C | 9% | ✱ |
| **§3** | **REGULARISATION TVA ANTERIEUREMENT DEDUITE A REVERSER** | | | |
| 3.1 | Régularisation TVA antérieurement déduite à reverser | S |  |  |
| **§4** | **TOTAL TVA BRUTE (03 + 04)** | | | |
| 4.1 | Total TVA brute | C |  | ✱ |
| **§5** | **DEDUCTIONS (état détaillé à joindre)** | | | |
| 5.1 | Taxes déductibles du mois | S |  |  |
| 5.2 | Crédit reporté du mois précédent | S |  |  |
| 5.3 | Total déduction | C |  | ✱ |
| **§6** | **MONTANT DE L’IMPÔT** | | | |
| 6.1 | TVA nette à payer | C |  | ✱ |
| 6.2 | dont Part Etat | S |  | ✱ |
| 6.3 | dont Part Secteur de l’Energie | S |  | ✱ |
| 6.6 | En cas de crédit de TVA, merci d’indiquer si vous allez en demander le remboursement | S |  |  |
| 6.4 | Crédit à reporter | C |  | ✱ |
| 6.5 | Crédit demandé en remboursement | C |  | ✱ |

### TSE — Taxe Spéciale d'Equipement (TSE)

*Périodicité : Mensuelle · Échéance : 15 du mois suivant · 8 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA BASE IMPOSABLE** | | | |
| 1.1 | Chiffre d’affaires total HT | S |  | ✱ |
| 1.2 | A déduire : Opérations exonérées (produits pétroliers) | S |  |  |
| 1.3 | A déduire : Livraisons à soi-même taxables | S |  |  |
| 1.4 | Chiffre d’affaires taxable | C |  |  |
| **§3** | **MONTANT DE LA TAXE** | | | |
| 3.1 | Montant de la taxe à payer | C |  | ✱ |
| **§2** | **REGULARISATION** | | | |
| 2.1 | Régularisation | S |  |  |
| 1.5 | Montant de la taxe sur la période | C | 0.1% |  |
| 3.2 | Montant à reporter | C |  |  |

### TOB — Taxe sur les Opérations Bancaires (TOB)

*Périodicité : Mensuelle · Échéance : 15 du mois suivant · 11 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **CHIFFRE D'AFFAIRES** | | | |
| 1 | Chiffre d’affaires total HT | S |  | ✱ |
| **§2** | **A DEDUIRE** | | | |
| 2.1 | Crédit-bail | S |  |  |
| 2.2 | Exportation et opérations assimilées | S |  |  |
| 2.3 | Opérations exonérées légales | S |  |  |
| 2.4 | Opérations exonérées conventionnelles | S |  |  |
| **§3** | **SYNTHESE** | | | |
| 3.1 | Chiffre d’affaires taxable au Taux 10% | S |  | ✱ |
| 3.2 | Montant de la Taxe | C | 10% |  |
| 3.3 | Chiffre d’affaires taxable au Taux 5% | S |  |  |
| 3.4 | Montant de la Taxe | C | 5% |  |
| 3.5 | Montant de la taxe à payer | C |  | ✱ |
| 2.5 | Montant total des déductions | C |  |  |

## ▸ Salaires (ITS & FDFP)


### ITS — Impôts sur les traitements et salaires (ITS)

*Périodicité : Mensuelle · Échéance : 15 du mois suivant · 76 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE L’ASSIETTE - A - TRAITEMENTS ET SALAIRES** | | | |
| 1.1 | Rémunérations versées | S |  | ✱ |
| 1.2 | Avantages en nature (évaluation) | S |  |  |
| 1.3 | Autres (à préciser) | S |  |  |
| 1.4 | Montant total brut | C |  |  |
| 1.5 | Rémunérations et avantages - Revenu net imposable après abattement | C | 20% |  |
| 2.3 | Pensions inférieures ou égales à 300000 FCFA - Montant brut | C |  |  |
| 2.4 | Pensions inférieures ou égales à 300000 FCFA - Revenu net imposable après abattement | C | 100% |  |
| 3.3 | Rentes viagères inférieures ou égales à 300000 FCFA - Montant brut | C |  |  |
| 3.4 | Rentes viagères inférieures ou égales à 300000 FCFA - Revenu net imposable après abattement | C | 100% |  |
| **§4** | **DETERMINATION DE L’ASSIETTE - TOTAL IMPOSABLE** | | | |
| 4.1 | TOTAL DU REVENU NET IMPOSABLE | C |  |  |
| **§5** | **IMPOTS RETENUS AUX SALARIES DU SECTEUR PRIVE** | | | |
| 5.1 | Impôt sur salaire (IS) - Base imposable | S |  |  |
| 5.2 | Impôt sur salaire (IS) - Montant de l’impôt | C | 1.5% |  |
| 5.4 | Contribution nationale (CN) - Base imposable | C |  |  |
| 5.5 | Contribution nationale (CN) - Montant de l’impôt | S |  |  |
| 5.7 | Impôt général sur le revenu (IGR) - Base imposable | S |  |  |
| 5.8 | Impôt général sur le revenu (IGR) - Montant de l’impôt | S |  |  |
| **§9** | **IMPOTS RETENUS AUX SALARIES** | | | |
| 9.1 | TOTAL DES RETENUS AUX SALARIES | C |  |  |
| **§10** | **CONTRIBUTIONS A LA CHARGE DE L'EMPLOYEUR - TOUS SECTEURS** | | | |
| 10.1 | (CE) Effectifs du Personnel local | S |  |  |
| 10.2 | (CE) Revenu net imposable du Personnel local | S |  |  |
| 10.3 | (CE) Effectifs du Personnel expatriés | S |  |  |
| 10.4 | (CE) Revenu net imposable du Personnel expatrié | S |  |  |
| 10.5 | (CE) Montant de la contribution pour le Personnel expatrié | C | 11.5% |  |
| 10.7 | (CN) Effectifs du Personnel local | C |  |  |
| 10.8 | (CN) Revenu net imposable du Personnel local | C |  |  |
| 10.9 | (CN) Montant de la contribution pour le Personnel local | C | 1.5% |  |
| 10.11 | (CN) Effectifs du Personnel expatrié | C |  |  |
| 10.12 | (CN) Revenu net imposable du Personnel expatrié | C |  |  |
| 10.13 | (CN) Montant de la contribution pour le Personnel expatrié | C | 1.5% |  |
| **§12** | **CONTRIBUTIONS A LA CHARGE DE L'EMPLOYEUR - TOTAL** | | | |
| 12.1 | TOTAL DES CONTRIBUTIONS | C |  |  |
| **§16** | **MONTANT TOTAL A PAYER** | | | |
| 16.1 | MONTANT TOTAL DE L’ITS A PAYER | C |  | ✱ |
| **§6** | **IMPOTS RETENUS AUX SALARIES DU SECTEUR PUBLIC** | | | |
| 6.1 | Impôt sur salaire (IS) - Base imposable | S |  |  |
| 6.2 | Impôt sur salaire (IS) - Montant de l’impôt | C | 1.5% |  |
| 6.4 | Contribution nationale (CN) - Base imposable | C |  |  |
| 6.6 | Contribution nationale (CN) - Montant de l’impôt | S |  |  |
| 6.7 | Impôt général sur le revenu (IGR) - Base imposable | S |  |  |
| 6.8 | Impôt général sur le revenu (IGR) - Montant de l’impôt | S |  |  |
| **§7** | **IMPOTS RETENUS AUX SALARIES DU SECTEUR PARA PUBLIC** | | | |
| 7.1 | Impôt sur salaire (IS) - Base imposable | S |  |  |
| 7.2 | Impôt sur salaire (IS) - Montant de l’impôt | C | 1.5% |  |
| 7.4 | Contribution nationale (CN) - Base imposable | C |  |  |
| 7.5 | Contribution nationale (CN) - Montant de l’impôt | S |  |  |
| 7.7 | Impôt général sur le revenu (IGR) - Base imposable | S |  |  |
| 7.8 | Impôt général sur le revenu (IGR) - Montant de l’impôt | S |  |  |
| **§8** | **IMPOTS RETENUS AUX SALARIES DU SECTEUR AGRICOLE** | | | |
| 8.1 | Impôt général sur le revenu (IGR) - Base imposable | S |  |  |
| 8.2 | Impôt général sur le revenu (IGR) - Montant de l’impôt | S |  |  |
| **§11** | **CONTRIBUTIONS A LA CHARGE DE L'EMPLOYEUR - ENTREPRISES AGRICOLES, AGRO-INDUSTRIELLES ET ASSIMILEES** | | | |
| 11.1 | (CN) Effectifs du Personnel | S |  |  |
| 11.2 | (CN) Revenu net imposable du Personnel | S |  |  |
| 11.3 | (CN) Montant de la contribution pour le Personnel | C | 2% |  |
| **§13** | **RETENUE SPECIFIQUE DU REGIME FORESTIER EN CAS DE FERMAGE** | | | |
| 13.1 | Fermage forestier - Revenu net imposable | S |  |  |
| 13.2 | Fermage forestier - Montant de la retenue | C | 35% |  |
| **§2** | **DETERMINATION DE L’ASSIETTE - B - PENSIONS** | | | |
| 2.1 | Pensions inférieures ou égales à 300000 FCFA - Montant total | S |  |  |
| 2.2 | Pensions inférieures ou égales à 300000 FCFA - Effectifs | S |  |  |
| 2.5 | Pensions supérieures à 300000 FCFA - Montant total | S |  |  |
| 2.6 | Pensions supérieures à 300000 FCFA - Effectifs | S |  |  |
| 2.7 | Pensions supérieures à 300000 FCFA - Montant brut | C |  |  |
| 2.8 | Pensions supérieures à 300000 FCFA - Revenu net imposable après abattement | C | 20% |  |
| **§3** | **DETERMINATION DE L’ASSIETTE - C - RENTES VIAGERES** | | | |
| 3.1 | Rentes viagères inférieures ou égales à 300000 FCFA - Montant total | S |  |  |
| 3.2 | Rentes viagères inférieures ou égales à 300000 FCFA - Effectifs | S |  |  |
| 3.5 | Rentes viagères supérieures à 300000 FCFA - Montant total | S |  |  |
| 3.6 | Rentes viagères supérieures à 300000 FCFA - Effectifs | S |  |  |
| 3.7 | Rentes viagères supérieures à 300000 FCFA - Montant brut | C |  |  |
| 3.8 | Rentes viagères supérieures à 300000 FCFA - Revenu net imposable après abattement | C | 20% |  |
| 5.3 | Régularisation - Impôt sur salaire (IS) - Montant de l’impôt | S |  |  |
| 5.6 | Régularisation - Contribution nationale (CN) - Montant de l’impôt | S |  |  |
| 5.9 | Régularisation - Impôt général sur le revenu (IGR) - Montant de l’impôt | S |  |  |
| 10.6 | Régularisation - (CE) Montant de la contribution pour le Personnel expatrié | S |  |  |
| 10.10 | Régularisation - (CN) Montant de la contribution pour le Personnel local | S |  |  |
| 10.14 | Régularisation - (CN) Montant de la contribution pour le Personnel expatrié | S |  |  |
| 6.3 | Régularisation - Impôt sur salaire (IS) - Montant de l’impôt | S |  |  |
| 6.5 | Régularisation - Contribution nationale (CN) - Montant de l’impôt | S |  |  |
| 6.9 | Régularisation - Impôt général sur le revenu (IGR) - Montant de l’impôt | S |  |  |
| 7.3 | Régularisation - Impôt sur salaire (IS) - Montant de l’impôt | S |  |  |
| 7.6 | Régularisation - Contribution nationale (CN) - Montant de l’impôt | S |  |  |
| 7.9 | Régularisation - Impôt général sur le revenu (IGR) - Montant de l’impôt | S |  |  |
| 11.4 | (Régularisation - CN) Montant de la contribution pour le Personnel | S |  |  |
| 13.3 | Régularisation - Fermage forestier - Montant de la retenue | S |  |  |
| 8.3 | Régularisation - Impôt général sur le revenu (IGR) - Montant de l’impôt | S |  |  |

### ITSPGAZ — Impôts sur les traitements et salaires (ITS) Pétrole / Gaz

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 17 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **REMUNERATION BRUTE TOTALE ** | | | |
| 1.1 | Rémunération brute totale | S |  | ✱ |
| **§2** | **A DEDUIRE (joindre les pièces justificatives des déductions)** | | | |
| 2.1 | Sommes reçues au titre de la mobilisation et de la démobilisation du matériel et de l’équipage | S |  |  |
| 2.2 | Remboursements de dépenses et de fournitures accessoires facturés séparément | S |  |  |
| **§3** | **MASSE SALARIALE** | | | |
| 3.1 | Masse salariale forfaitaire | C | 8% |  |
| **§4** | **IMPOTS DUS PAR LES SALARIES** | | | |
| 4.1 | Impôt sur salaire (IS) | C | 1.5% |  |
| 4.3 | Contribution Nationale (CN) | C | 6.25% |  |
| 4.5 | Impôt Général sur le revenu (IGR) (personnel expatrié seul ; retenu pour 80% de la masse salariale) | C | 10% |  |
| 4.7 | Total des impôts dus par les salariés | C |  |  |
| **§5** | **IMPOTS DUS PAR L'EMPLOYEUR** | | | |
| 5.1 | Contributions pour le personnel expatrié (CE) | C | 12% |  |
| 5.3 | Contributions pour le personnel local (CN) | C | 0.7% |  |
| 5.5 | Total des impôts dus par l’employeur | C |  |  |
| **§6** | **TOTAL A PAYER** | | | |
| 6.1 | Montant total de l’ITS à payer | C |  |  |
| 4.2 | Régularisation - Impôt sur salaire (IS) | S |  |  |
| 4.4 | Régularisation - Contribution Nationale (CN) | S | 5% |  |
| 4.6 | Régularisation - Impôt Général sur le revenu (IGR) (personnel expatrié seul ; retenu pour 80% de la | S |  |  |
| 5.2 | Régularisation - Contributions pour le personnel expatrié (CE) | S |  |  |
| 5.4 | Régularisation - Contributions pour le personnel local (CN) | S |  |  |

### ITSREGUL — Etat des salaires et des rémunérations assimilées payes durant l'année (Etat 301)

*Périodicité : Annuelle · Échéance : ≈17/02 / avec État 301 · 64 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE L’ASSIETTE** | | | |
| 1.1 | Montant des salaires non déclarés (inférieurs au minimum) - 12 mois | S |  | ✱ |
| 1.2 | Montant des salaires non déclarés (inférieurs au minimum) - Ajustement | S |  |  |
| 1.3 | Montant des salaires non déclarés (inférieurs au minimum) - Total | C |  |  |
| 1.4 | Indemnités de départ - 12 mois | S |  |  |
| 1.5 | Indemnités de départ - Ajustement | S |  |  |
| 1.6 | Indemnités de départ - Total | C |  |  |
| 1.7 | Montant brut imposable - 12 mois | S |  |  |
| 1.8 | Montant brut imposable - Ajustement | S |  |  |
| 1.9 | Montant brut imposable - Total | C |  |  |
| 1.10 | Revenus brut total - 12 mois | S |  |  |
| 1.11 | Revenus brut total - Ajustement | S |  |  |
| 1.12 | Revenus brut total - Total | C |  |  |
| 1.13 | Montant net imposable - 12 mois | S |  |  |
| 1.14 | Montant net imposable - Ajustement | S |  |  |
| 1.15 | Montant net imposable - Total | C |  |  |
| **§2** | **ENTREPRISES DU SECTEUR PRIVE** | | | |
| 2.1 | Impôt sur salaire (IS) - Montant des 12 mois | S |  |  |
| 2.2 | Impôt sur salaire (IS) - Ajustement mois 13 | S |  |  |
| 2.3 | Impôt sur salaire (IS) - Montant de l’impôt | C |  |  |
| 2.4 | Contribution nationale (CN) - Montant des 12 mois | S |  |  |
| 2.5 | Contribution nationale (CN) - Ajustement mois 13 | S |  |  |
| 2.6 | Contribution nationale (CN) - Montant de l’impôt | C |  |  |
| 2.7 | Impôt général sur le revenu (IGR) - Montant des 12 mois | S |  |  |
| 2.8 | Impôt général sur le revenu (IGR) - Ajustement mois 13 | S |  |  |
| 2.9 | Impôt général sur le revenu (IGR) - Montant de l’impôt | C |  |  |
| **§3** | **ENTREPRISES DU SECTEUR PUBLIC** | | | |
| 3.1 | Impôt sur salaire (IS) - Montant des 12 mois | S |  |  |
| 3.2 | Impôt sur salaire (IS) - Ajustement mois 13 | S |  |  |
| 3.3 | Impôt sur salaire (IS) - Montant de l’impôt | C |  |  |
| 3.4 | Contribution nationale (CN) - Montant des 12 mois | S |  |  |
| 3.5 | Contribution nationale (CN) - Ajustement mois 13 | S |  |  |
| 3.6 | Contribution nationale (CN) - Montant de l’impôt | C |  |  |
| 3.7 | Impôt général sur le revenu (IGR) - Montant des 12 mois | S |  |  |
| 3.8 | Impôt général sur le revenu (IGR) - Ajustement mois 13 | S |  |  |
| 3.9 | Impôt général sur le revenu (IGR) - Montant de l’impôt | C |  |  |
| **§4** | **ENTREPRISES DU SECTEUR PARAPUBLIC** | | | |
| 4.1 | Impôt sur salaire (IS) - Montant des 12 mois | S |  |  |
| 4.2 | Impôt sur salaire (IS) - Ajustement mois 13 | S |  |  |
| 4.3 | Impôt sur salaire (IS) - Montant de l’impôt | C |  |  |
| 4.4 | Contribution nationale (CN) - Montant des 12 mois | S |  |  |
| 4.5 | Contribution nationale (CN) - Ajustement mois 13 | S |  |  |
| 4.6 | Contribution nationale (CN) - Montant de l’impôt | C |  |  |
| 4.7 | Impôt général sur le revenu (IGR) - Montant des 12 mois | S |  |  |
| 4.8 | Impôt général sur le revenu (IGR) - Ajustement mois 13 | S |  |  |
| 4.9 | Impôt général sur le revenu (IGR) - Montant de l’impôt | C |  |  |
| **§5** | **ENTREPRISES DU SECTEUR AGRICOLE** | | | |
| 5.1 | Impôt général sur le revenu (IGR) - Montant des 12 mois | S |  |  |
| 5.2 | Impôt général sur le revenu (IGR) - Ajustement mois 13 | S |  |  |
| 5.3 | Impôt général sur le revenu (IGR) - Montant de l’impôt | C |  |  |
| **§6** | **ENTREPRISES DE TOUS SECTEURS** | | | |
| 6.1 | Personnel expatrié (CE) - Montant des 12 mois | S |  |  |
| 6.2 | Personnel expatrié (CE) - Ajustement mois 13 | S |  |  |
| 6.3 | Personnel expatrié (CE) - Montant de l’impôt | C |  |  |
| 6.4 | Personnel local (CN) - Montant des 12 mois | S |  |  |
| 6.5 | Personnel local (CN) - Ajustement mois 13 | S |  |  |
| 6.6 | Personnel local (CN) - Montant de l’impôt | C |  |  |
| 6.7 | Personnel expatrié (CN) - Montant des 12 mois | S |  |  |
| 6.8 | Personnel expatrié (CN) - Ajustement mois 13 | S |  |  |
| 6.9 | Personnel expatrié (CN) - Montant de l’impôt | C |  |  |
| **§7** | **ENTREPRISES AGRICOLES, AGRO-INDUSTRIELLES ET ASSIMILEES** | | | |
| 7.1 | Contribution employeur pour régime agricole (CE) - Montant des 12 mois | S |  |  |
| 7.2 | Contribution employeur pour régime agricole (CE) - Ajustement mois 13 | S |  |  |
| 7.3 | Contribution employeur pour régime agricole (CE) - Montant de l’impôt | C |  |  |
| **§8** | **RETENUE SPECIFIQUE DU REGIME FORESTIER EN CAS DE FERMAGE** | | | |
| 8.1 | Retenue sur le revenu des exploitants forestiers à titre de fermage - Montant des 12 mois | S |  |  |
| 8.2 | Retenue sur le revenu des exploitants forestiers à titre de fermage - Ajustement mois 13 | S |  |  |
| 8.3 | Retenue sur le revenu des exploitants forestiers à titre de fermage - Montant de l’impôt | C |  |  |
| **§9** | **MONTANT TOTAL** | | | |
| 9.1 | MONTANT D’ITS ETAT 301 A PAYER | C |  |  |
| **§0** | **Période comptable concernée** | | | |
| 0.1 | Date de début de l’exercice comptable (saisir au format JJ/MM/AAAA) | S |  |  |
| 0.2 | Date de fin de l’exercice comptable (saisir au format JJ/MM/AAAA) | S |  |  |
| 0.3 | Nombre des établissements auxquels la déclaration s’applique | S |  |  |

### FDFP — Taxe d'apprentissage et de Formation Continue

*Périodicité : Mensuelle+Annuelle · Échéance : 15 du mois suivant + régul. · 13 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DES TAXES** | | | |
| 1.1 | Taxe d’Apprentissage (TA) : Rémunérations brutes totales | S |  | ✱ |
| 1.2 | Taxe d’Apprentissage (TA) : Montant à payer | C | 0.4% | ✱ |
| 1.3 | Taxe à la Formation Continue (TFC) : Rémunérations brutes totales | C |  | ✱ |
| 1.4 | Taxe à la Formation Continue (TFC) : Montant à payer | C | 0.6% | ✱ |
| 1.5 | Montant cumulé de la TFC conservée depuis le début d’année (y compris montant déclaré pour ce mois) | S |  |  |
| **§2** | **REGULARISATION ANNUELLE DE LA TFC** | | | |
| 2.1 | Masse salariale annuelle | S |  |  |
| 2.2 | Montant annuel de la TFC (masse salariale x 1.2%) | C | 1.2% |  |
| 2.3 | Montant total de la TFC payée au cours de l’année | C |  |  |
| 2.4 | Engagement sur plans agréés par le FDFP (utilisation directe) | S |  |  |
| 2.5 | Versement complémentaire à effectuer (régularisation) | C |  |  |
| 2.6 | Montant total de la taxe à la formation continue à payer | C |  | ✱ |
| 1.6 | Prise en compte de la régularisation ? | S |  |  |
| **§3** | **MONTANT TOTAL A PAYER** | | | |
| 3.1 | MONTANT TOTAL A PAYER (FDFP) | C |  | ✱ |

## ▸ Retenues à la source


### RIBIC — Retenue à la source au titre de l'impôt BIC

*Périodicité : Mensuelle · Échéance : 15 du mois suivant · 51 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **Entreprises de transport de bois en grumes et d’hydrocarbures** | | | |
| 1.1 | Montant des rémunérations brutes versées | S |  |  |
| **§2** | **Agents mandataires et apporteurs d’affaires** | | | |
| 2.1 | Secteur Assurance - Montant des rémunérations brutes versées | S |  |  |
| 2.3 | Autre secteur - Montant des rémunérations brutes versées | S |  |  |
| **§3** | **Revendeurs des importateurs / fabricants grossistes et demi-grossistes** | | | |
| 3.1 | Montant des rémunérations brutes versées | S |  |  |
| **§4** | **Sous-traitants/architectes/métreurs/géomètres et autres professionnels utilisés pour le BTP** | | | |
| 4.1 | Montant des rémunérations brutes versées | S |  |  |
| **§5** | **Exportateurs et Pisteurs de produits du café et du cacao** | | | |
| 5.1 | Pisteurs de café et cacao - Montant des rémunérations brutes versées | S |  |  |
| **§6** | **Producteurs de palmiers à huile, ananas, bois en grume et produits hévéicoles** | | | |
| 6.1 | Montant des rémunérations brutes versées - Palmiers à huile | S |  |  |
| 6.3 | Montant des rémunérations brutes versées - Produits hévéicoles | S |  |  |
| 6.5 | Montant des rémunérations brutes versées - Ananas | S |  |  |
| 6.7 | Montant des rémunérations brutes versées - Bois en grume | S |  |  |
| **§7** | **Clients revendeurs des scieries** | | | |
| 7.1 | Montant des rémunérations brutes versées | S |  |  |
| **§8** | **Clients de la SODEFOR pour les ventes de bois sur pied** | | | |
| 8.1 | Montant des rémunérations brutes versées | S |  |  |
| 5.3 | Traitants utilisés par les exportateurs de café - Poids des produits livrés (kg) | S |  |  |
| 5.5 | Traitants utilisés par les exportateurs de cacao - Poids des produits livrés (kg) | S |  |  |
| 1.4 | Montant de la retenue (avec régularisation) | C |  |  |
| 2.2 | Secteur Assurance - Montant de la retenue sur la période | C | 7.5% |  |
| 2.4 | Autre secteur - Montant de la retenue sur la période | C | 7.5% |  |
| 3.4 | Montant de la retenue (avec régularisation) | C |  |  |
| 4.4 | Montant de la retenue (avec régularisation) | C |  |  |
| 5.2 | Pisteurs de café et cacao - Montant de la retenue sur la période | C | 7.5% |  |
| 6.2 | Montant de la retenue sur la période - Palmiers à huile | C | 1.5% |  |
| 6.4 | Montant de la retenue sur la période - Produits hévéicoles | C | 2.5% |  |
| 6.6 | Montant de la retenue sur la période - Ananas | C | 2.5% |  |
| 6.8 | Montant de la retenue sur la période - Bois en grume | C | 5% |  |
| 7.4 | Montant de la retenue (avec régularisation) | C |  |  |
| 8.4 | Montant de la retenue (avec régularisation) | C |  |  |
| 5.4 | Traitants utilisés par les exportateurs de café - Montant de la retenue sur la période | C | 200% |  |
| 5.6 | Traitants utilisés par les exportateurs de cacao - Montant de la retenue sur la période | C | 250% |  |
| **§9** | **SYNTHESE** | | | |
| 9.1 | TOTAL DES RETENUES SUR LA PERIODE | C |  | ✱ |
| 2.7 | Total des retenues effectués sur les agents mandataires et apporteurs d’affaires - art. 57 et 57 bis | C |  |  |
| 5.9 | Total des retenues effectués sur les exportateurs et pisteurs de café et cacao - art. 60 et 60 bis ( | C |  |  |
| 6.11 | Total des retenues sur palmiers, ananas, bois en grume, produits hévéicoles - art. 61 (avec régulari | C |  |  |
| 9.2 | TOTAL REGULARISATION | C |  |  |
| 9.3 | MONTANT NET A REVERSER | C |  |  |
| 1.2 | Montant de la retenue sur la période | C | 7.5% |  |
| 2.5 | Total des retenues effectués sur les agents mandataires et apporteurs d’affaires - art. 57 et 57 bis | C | 7.5% |  |
| 3.2 | Montant de la retenue sur la période | C | 7.5% |  |
| 4.2 | Montant de la retenue sur la période | C | 7.5% |  |
| 5.7 | Total des retenues effectués sur les exportateurs et pisteurs de café et cacao (art. 60 et 60 bis) | C |  |  |
| 6.9 | Total des retenues sur palmiers, ananas, bois en grume, produits hévéicoles (art. 61) | C |  |  |
| 7.2 | Montant de la retenue sur la période | C | 10% |  |
| 8.2 | Montant de la retenue sur la période | C | 5% |  |
| 1.3 | Régularisation sur périodes précédentes | S |  |  |
| 2.6 | Régularisation sur périodes précédentes | S |  |  |
| 3.3 | Régularisation sur périodes précédentes | S |  |  |
| 4.3 | Régularisation sur périodes précédentes | S |  |  |
| 5.8 | Régularisation sur périodes précédentes | S |  |  |
| 6.10 | Régularisation sur périodes précédentes | S |  |  |
| 7.3 | Régularisation sur périodes précédentes | S |  |  |
| 8.3 | Régularisation sur périodes précédentes | S |  |  |
| 9.4 | MONTANT A REPORTER | C |  |  |

### RIBNC — Retenue à la source au titre de l'impôt BNC

*Périodicité : Mensuelle · Échéance : 15 du mois suivant · 56 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **Personnes n’ayant pas d’installation professionnelle en Côte d’Ivoire** | | | |
| 1.1 | Montant des rémunérations brutes versées | S |  |  |
| 1.3 | Montant de la retenue sur la période | C | 25% |  |
| 2.3 | Montant de la retenue sur la période | C | 25% |  |
| 3.5 | Montant de la retenue sur la période | C |  |  |
| 5.4 | Montant de la retenue (avec régularisation) | C |  |  |
| 6.4 | Montant de la retenue (avec régularisation) | C |  |  |
| 7.4 | Montant de la retenue (avec régularisation) | C |  |  |
| **§2** | **Compagnie de réassurance non domiciliée en Côte d’Ivoire** | | | |
| 2.1 | Montant des rémunérations brutes versées | S |  |  |
| **§3.1** | **Retenue au titre des conventions fiscales internationales - Type 1** | | | |
| 3.1 | Montant des rémunérations brutes versées | S |  |  |
| **§5** | **Profession médicales ou paramédicales** | | | |
| 5.1 | Montant des rémunérations brutes versées | S |  |  |
| **§6** | **Revendeurs de billets de jeux de hasard / courtiers / intermédiaires** | | | |
| 6.1 | Montant des rémunérations brutes versées | S |  |  |
| **§7** | **Enseignants vacataires / prestations de consultance ou d’expertise** | | | |
| 7.1 | Montant des rémunérations brutes versées | S |  |  |
| **§8** | **Artistes musiciens / sportifs / organisateurs de spectacles** | | | |
| 8.1 | Montant des rémunérations brutes versées | S |  |  |
| **§9** | **Collaborateurs non-salariés des avocats/notaires/huissiers/commissaires-priseurs** | | | |
| 9.1 | Montant des rémunérations brutes versées | S |  |  |
| **§10** | **Avocats/Huissiers/Conseils juridiques et fiscaux/Comptables/Commissaires-priseurs/Notaires** | | | |
| 10.1 | Montant des rémunérations brutes versées | S |  |  |
| **§11** | **Greffiers-notaires** | | | |
| 11.1 | Montant des rémunérations brutes versées | S |  |  |
| 8.4 | Montant de la retenue (avec régularisation) | C |  |  |
| 9.4 | Montant de la retenue (avec régularisation) | C |  |  |
| 10.4 | Montant de la retenue (avec régularisation) | C |  |  |
| 11.4 | Montant de la retenue (avec régularisation) | C |  |  |
| **§12** | **Synthèse** | | | |
| 12.1 | TOTAL DES RETENUES SUR LA PERIODE | C |  |  |
| 1.2 | Base imposable après abattement | C | 20% |  |
| 2.2 | Base imposable après abattement | C | 50% |  |
| 3.2 | Déduction  (exemple : saisir 20 pour 20% ; décimales avec des ".") | S |  |  |
| 3.3 | Base imposable après abattement | C |  |  |
| 3.4 | Taux d’imposition à appliquer (exemple : saisir 20 pour 20% ; décimales avec des ".") | S |  |  |
| 4.3 | Retenues sur les contribuables n’ayant pas d’installation professionnelle en Côte d’Ivoire - art. 92 | C |  |  |
| 12.2 | TOTAL REGULARISATION | C |  |  |
| 12.3 | MONTANT NET A REVERSER | C |  | ✱ |
| 12.4 | MONTANT A REPORTER | C |  |  |
| 5.2 | Montant de la retenue sur la période | C | 7.5% |  |
| 6.2 | Montant de la retenue sur la période | C | 7.5% |  |
| 7.2 | Montant de la retenue sur la période | C | 7.5% |  |
| 8.2 | Montant de la retenue sur la période | C | 7.5% |  |
| 9.2 | Montant de la retenue sur la période | C | 7.5% |  |
| 10.2 | Montant de la retenue sur la période | C | 7.5% |  |
| 11.2 | Montant de la retenue sur la période | C | 50% |  |
| **§4** | **Sous-total - Retenues sur les contribuables Non-résidents (sections 1 + 2 + 3,1 + 3,2 +3,3)** | | | |
| 4.1 | Retenues sur les contribuables n’ayant pas d’installation professionnelle en Côte d’Ivoire (art. 92) | C |  |  |
| 4.2 | Régularisation sur périodes précédentes | S |  |  |
| 5.3 | Régularisation sur périodes précédentes | S |  |  |
| 6.3 | Régularisation sur périodes précédentes | S |  |  |
| 7.3 | Régularisation sur périodes précédentes | S |  |  |
| 8.3 | Régularisation sur périodes précédentes | S |  |  |
| 9.3 | Régularisation sur périodes précédentes | S |  |  |
| 10.3 | Régularisation sur périodes précédentes | S |  |  |
| 11.3 | Régularisation sur périodes précédentes | S |  |  |
| 3.2 | Déduction  (exemple : saisir 20 pour 20% ; décimales avec des ".") | S |  |  |
| 3.3 | Base imposable après abattement | C |  |  |
| 3.4 | Taux d’imposition à appliquer (exemple : saisir 20 pour 20% ; décimales avec des ".") | S |  |  |
| 3.5 | Montant de la retenue sur la période | C |  |  |
| **§3.3** | **Retenue au titre des conventions fiscales internationales - Type 3** | | | |
| 3.1 | Montant des rémunérations brutes versées | S |  |  |
| 3.2 | Déduction  (exemple : saisir 20 pour 20% ; décimales avec des ".") | S |  |  |
| 3.3 | Base imposable après abattement | C |  |  |
| 3.4 | Taux d’imposition à appliquer (exemple : saisir 20 pour 20% ; décimales avec des ".") | S |  |  |
| 3.5 | Montant de la retenue sur la période | C |  |  |
| **§3.2** | **Retenue au titre des conventions fiscales internationales - Type 2** | | | |
| 3.1 | Montant des rémunérations brutes versées | S |  |  |

### AIRSI — Acompte d'Impôt sur les Revenus du Secteur Informel (AIRSI)

*Périodicité : Mensuelle · Échéance : 15 du mois suivant · 20 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **CHIFFRE D'AFFAIRES** | | | |
| 1.1 | Chiffre d’affaires TTC | S |  | ✱ |
| 2.2 | Ventes aux opérateurs du secteur agricole | S |  |  |
| 2.3 | Vente portant sur l’eau- l’électricité- le gaz- les produits pétroliers- miniers et pharmaceutiques | S |  |  |
| 2.4 | Vente aux contribuables relevant d’un régime réel d’imposition | S |  |  |
| 2.5 | Total Affaires exonérées | C |  |  |
| **§3** | **DETERMINATION DE L'IMPOT SUR LA PERIODE** | | | |
| 3.1 | Total du Chiffre d’affaires taxable | C |  |  |
| 3.2 | Chiffre d’affaires taxable TTC (taux 7.5%) | S |  |  |
| 3.3 | Montant de la Taxe | C | 7.5% |  |
| 3.4 | Chiffre d’affaires taxable TTC (taux 2%) | S |  |  |
| 3.5 | Montant de la Taxe | C | 2% |  |
| 3.6 | Chiffre d’affaires taxable TTC (taux 1.5%) | S |  |  |
| 3.7 | Montant de la Taxe | C | 1.5% |  |
| 3.8 | Chiffre d’affaires taxable TTC (taux 0.2%) | S |  |  |
| 3.9 | Montant de la Taxe | C | 0.2% |  |
| 4.2 | Montant total de la taxe à payer | C |  | ✱ |
| 3.10 | Montant total de la taxe calculée sur la période | C |  | ✱ |
| **§4** | **SYNTHESE DE L'IMPOT A PAYER** | | | |
| 4.1 | Régularisation | S |  |  |
| 4.3 | Montant à reporter (à déduire le mois prochain) | C |  |  |
| **§2** | **AFFAIRES EXONEREES A DEDUIRE** | | | |
| 2.1 | Exportations | S |  |  |
| 2.5 | Chiffre d’affaires hors du champ d’application de l’AIRSI (prestation de service) | S |  |  |

### PPSSI — Retenue à la source sur les paiements faits aux prestataires de services du secteur informel

*Périodicité : Mensuelle · Échéance : 15 du mois suivant · 5 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA RETENUE** | | | |
| 1.1 | Montant total des prestations de service | S |  | ✱ |
| 1.2 | Montant de la retenue | C | 7.5% | ✱ |
| 2.2 | Total à payer | C |  | ✱ |
| **§2** | **TOTAL A PAYER** | | | |
| 2.1 | Régularisation | S |  | ✱ |
| 2.3 | Montant à reporter (à déduire le mois prochain) | C |  | ✱ |

### PPSSIREGUL — Etat récapitulatif des retenues sur le montant des prestations de services des entreprises soumises au régime de l'impôt synthétique (PPSSIREGUL)

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 6 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
|  | Forme juridique | S |  |  |
| **§1** | **REGISTRE DE COMMERCE** | | | |
| 1.1 | Numéro du registre de commerce | S |  | ✱ |
| 1.2 | Délivré le (Jour/Mois/Année) | S |  | ✱ |
| 1.3 | Délivré à | S |  | ✱ |
| **§2** | **RETRIBUTIONS** | | | |
| 2.1 | Total - Montant brut TTC | S |  |  |
| 2.2 | Total - Retenues opérées (7,5% du brut versé) | S |  |  |

### RIRL — Retenue à la source à titre d'acompte d'impôt sur les revenus locatifs (RIRL)

*Périodicité : Mensuelle · Échéance : 15 du mois suivant · 27 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **RETENUES AU TITRE DES PERSONNES PHYSIQUES** | | | |
| 1.1 | Agences immobilières - Montant brut des loyers versés | S |  |  |
| 1.2 | Agences immobilières - Montant de la retenue | C | 12% |  |
| 1.3 | Syndics d’immeubles - Montant brut des loyers versés | S |  |  |
| 1.4 | Syndics d’immeubles - Montant de la retenue | C | 12% |  |
| 1.5 | Gérants de biens - Montant brut des loyers versés | S |  |  |
| 1.6 | Gérants de biens - Montant de la retenue | C | 12% |  |
| 1.7 | Sociétés civiles immobilières - Montant brut des loyers versés | S |  |  |
| 1.8 | Sociétés civiles immobilières - Montant de la retenue | C | 12% |  |
| 1.9 | Autres intermédiaires(Régis: FACI, Police, Eaux et forêts ...) - Montant brut des loyers versés | S |  |  |
| 1.10 | Autres intermédiaires(Régis: FACI, Police, Eaux et forêts ...) - Montant de la retenue | C | 12% |  |
| 1.11 | Entreprises soumises au régime du réel d’imposition - Montant brut des loyers versés | S |  |  |
| 1.12 | Entreprises soumises au régime du réel d’imposition - Montant de la retenue | C | 12% |  |
| 1.13 | TOTAL - Montant de la retenue | C |  |  |
| **§2** | **RETENUES AU TITRE DES PERSONNES MORALES** | | | |
| 2.1 | Agences immobilières - Montant brut des loyers versés | S |  |  |
| 2.2 | Agences immobilières - Montant de la retenue | C | 15% |  |
| 2.3 | Syndics d'immeubles - Montant brut des loyers versés | S |  |  |
| 2.4 | Syndics d'immeubles - Montant de la retenue | C | 15% |  |
| 2.5 | Gérants de biens - Montant brut des loyers versés | S |  |  |
| 2.6 | Gérants de biens - Montant de la retenue | C | 15% |  |
| 2.7 | Sociétés civiles immobilières - Montant brut des loyers versés | S |  |  |
| 2.8 | Sociétés civiles immobilières - Montant de la retenue | C | 15% |  |
| 2.9 | Autres intermédiaires(Régis: FACI, Police, Eaux et forêts ...) - Montant brut des loyers versés | S |  |  |
| 2.10 | Autres intermédiaires(Régis: FACI, Police, Eaux et forêts ...) - Montant de la retenue | C | 15% |  |
| 2.11 | Entreprises soumises au régime du réel d'imposition - Montant brut des loyers versés | S |  |  |
| 2.12 | Entreprises soumises au régime du réel d'imposition - Montant de la retenue | C | 15% |  |
| 2.13 | TOTAL - Montant de la retenue | C |  |  |
| **§3** | **TOTAL A REVERSER** | | | |
| 3.1 | TOTAL A REVERSER | C |  | ✱ |

### IRVM — Impôt sur le Revenu des Valeurs Mobilières

*Périodicité : Sur distribution · Échéance : Mois de mise en paiement · 21 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **RESULTATS ET RESERVES** | | | |
| 1.1 | Résultat déclaré après impôt | S |  | ✱ |
| 1.2 | Réserves constituées | S |  |  |
| 1.3 | Bénéfice incorporé au capital | S |  |  |
| 1.4 | Investissement de bénéfice | S |  |  |
| 1.5 | Autres | S |  |  |
| 1.7 | Résultats distribués (1.7 = 1.1 - 1.2 - 1.3 - 1.4 - 1.5) | C |  | ✱ |
| 1.6 | Préciser la nature des Autres résultats et réserves | S |  |  |
| **§2** | **REVENUS DISTRIBUES** | | | |
| 2.1 | Lots d’obligations : Base d’imposition | S |  |  |
| 2.3 | Distributions de bénéfices exonérés de l’impôt BIC : Base d’imposition | S |  |  |
| 2.5 | Dividendes régulièrement mis en paiement par les sociétés cotées : Base d’imposition | S |  |  |
| 2.7 | Produits / Lots / Primes de remboursement payés sur obligations de plus de 5 ans : Base d’imposition | S |  |  |
| 2.9 | Autres produits et sommes imposables : Base d’imposition | S |  |  |
| 2.2 | Lots d’obligations : Montant à payer | C | 15% |  |
| 2.4 | Distributions de bénéfices exonérés de l’impôt BIC : Montant à payer | C | 15% |  |
| 2.6 | Dividendes régulièrement mis en paiement par les sociétés cotées : Montant à payer | C | 10% |  |
| 2.8 | Produits / Lots / Primes de remboursement payés sur obligations de plus de 5 ans : Montant à payer | C | 2% |  |
| 2.10 | Autres produits et sommes imposables : Montant à payer | C | 15% |  |
| 2.14 | MONTANT TOTAL A PAYER | C |  | ✱ |
| 2.11 | Indemnités de fonction : Base d’imposition | S |  |  |
| 2.12 | Indemnités de fonction : Taux | S |  |  |
| 2.13 | Indemnités de fonction : Montant à payer | C |  |  |

### IRVMPGAZ — Impôts sur les revenus de valeurs mobilières (IRVM) Pétrole / Gaz

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 5 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **REMUNERATION BRUTE TOTALE ** | | | |
| 1.1 | Rémunération brute totale | S |  | ✱ |
| **§2** | **A DEDUIRE (joindre les pièces justificatives des déductions)** | | | |
| 2.1 | Sommes reçues au titre de la mobilisation et de la démobilisation du matériel et de l’équipage | S |  |  |
| 2.2 | Remboursements de dépenses et de fournitures accessoires facturés séparément | S |  |  |
| **§3** | **SYNTHESE** | | | |
| 3.1 | Base d’imposition | C | 5% |  |
| 3.2 | Impôt IRVM à payer | C | 15% |  |

### IRC — Impôt sur le Revenu des Créances

*Périodicité : Sur échéance · Échéance : Dans le mois · 1 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE L'IMPOT** | | | |
|  | Montant à payer | S |  | ✱ |

### FIRCA — Cotisations professionnelles pour le FIRCA

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 66 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **RESSOURCES ANIMALES - BOVINS** | | | |
| 1.1 | Bovin sur pied : Quantité (têtes) | S |  |  |
| 1.2 | Bovin sur pied : Tarif (FCFA/têtes) | S |  |  |
| 1.3 | Bovin sur pied : Montant à payer | C |  |  |
| **§2** | **RESSOURCES ANIMALES - OVINS** | | | |
| 2.1 | Ovin sur pied : Quantité (têtes) | S |  |  |
| 2.2 | Ovin sur pied : Tarif (FCFA/têtes) | S |  |  |
| 2.3 | Ovin sur pied : Montant à payer | C |  |  |
| **§3** | **RESSOURCES ANIMALES - CAPRINS** | | | |
| 3.1 | Caprin sur pied : Quantité (têtes) | S |  |  |
| 3.2 | Caprin sur pied : Tarif (FCFA/têtes) | S |  |  |
| 3.3 | Caprin sur pied : Montant à payer | C |  |  |
| **§4** | **RESSOURCES ANIMALES - PORCS** | | | |
| 4.1 | Contribution des éleveurs : Quantité (têtes) | S |  |  |
| 4.2 | Contribution des éleveurs : Tarif (FCFA/têtes) | S |  |  |
| 4.3 | Contribution des éleveurs : Montant à payer | C |  |  |
| 4.4 | Contribution des industriels : Quantité (têtes) | S |  |  |
| 4.5 | Contribution des industriels : Tarif (FCFA/têtes) | S |  |  |
| 4.6 | Contribution des industriels : Montant à payer | C |  |  |
| **§5** | **RESSOURCES ANIMALES - VOLAILLES MODERNES** | | | |
| 5.1 | Poussins Chair : Quantité (têtes) | S |  |  |
| 5.2 | Poussins Chair : Tarif (FCFA/têtes) | S |  |  |
| 5.3 | Poussins Chair : Montant à payer | C |  |  |
| 5.4 | Poussins Ponte : Quantité (têtes) | S |  |  |
| 5.5 | Poussins Ponte : Tarif (FCFA/têtes) | S |  |  |
| 5.6 | Poussins Ponte : Montant à payer | C |  |  |
| 5.7 | Aliment de bétail : Quantité (kg) | S |  |  |
| 5.8 | Aliment de bétail : Tarif (/kg) | S |  |  |
| 5.9 | Aliment de bétail : Montant à payer | C |  |  |
| **§6** | **RESSOURCES ANIMALES - TOTAL DES COTISATIONS** | | | |
| 6.1 | TOTAL | C |  | ✱ |
| **§7** | **RESSOURCES VEGETALES - HEVEA** | | | |
| 7.1 | Contribution des planteurs : Quantité | S |  |  |
| 7.2 | Contribution des planteurs : Tarif | S |  |  |
| 7.3 | Contribution des planteurs : Montant à payer | C |  |  |
| 7.4 | Contribution des usiniers : Quantité | S |  |  |
| 7.5 | Contribution des usiniers : Tarif | S |  |  |
| 7.6 | Contribution des usiniers : Montant à payer | C |  |  |
| **§8** | **RESSOURCES VEGETALES - ANANAS** | | | |
| 8.1 | Ananas : Quantité | S |  |  |
| 8.2 | Ananas : Tarif | S |  |  |
| 8.3 | Ananas : Montant à payer | C |  |  |
| **§9** | **RESSOURCES VEGETALES - BANANES** | | | |
| 9.1 | Banane : Quantité | S |  |  |
| 9.2 | Banane : Tarif | S |  |  |
| 9.3 | Banane : Montant à payer | C |  |  |
| **§10** | **RESSOURCES VEGETALES - MANGUES** | | | |
| 10.1 | Mangue : Quantité | S |  |  |
| 10.2 | Mangue : Tarif | S |  |  |
| 10.3 | Mangue : Montant à payer | C |  |  |
| **§11** | **RESSOURCES VEGETALES - PALMIER A HUILE** | | | |
| 11.1 | Contribution des planteurs : Quantité | S |  |  |
| 11.2 | Contribution des planteurs : Tarif | S |  |  |
| 11.3 | Contribution des planteurs : Montant à payer | C |  |  |
| 11.4 | Contribution des agro-industriels : Quantité | S |  |  |
| 11.5 | Contribution des agro-industriels : Tarif | S |  |  |
| 11.6 | Contribution des agro-industriels : Montant à payer | C |  |  |
| 11.7 | Contribution des usiniers : Quantité | S |  |  |
| 11.8 | Contribution des usiniers : Tarif | S |  |  |
| 11.9 | Contribution des usiniers : Montant à payer | C |  |  |
| **§12** | **RESSOURCES VEGETALES - COTON** | | | |
| 12.1 | Coton graine : Quantité | S |  |  |
| 12.2 | Coton graine : Tarif | S |  |  |
| 12.3 | Coton graine : Montant à payer | C |  |  |
| 12.4 | Coton fibre : Quantité | S |  |  |
| 12.5 | Coton fibre : Tarif | S |  |  |
| 12.6 | Coton fibre : Montant à payer | C |  |  |
| 12.7 | Contribution des usiniers : Quantité | S |  |  |
| 12.8 | Contribution des usiniers : Tarif | S |  |  |
| 12.9 | Contribution des usiniers : Montant à payer | C |  |  |
| **§13** | **RESSOURCES VEGETALES - ANACARDES** | | | |
| 13.1 | Noix de cajou : Quantité | S |  |  |
| 13.2 | Noix de cajou : Tarif | S |  |  |
| 13.3 | Noix de cajou : Montant à payer | C |  |  |
| 13.4 | Contribution des usiniers : Quantité | S |  |  |
| 13.5 | Contribution des usiniers : Tarif | S |  |  |
| 13.6 | Contribution des usiniers : Montant à payer | C |  |  |
| **§14** | **RESSOURCES VEGETALES - TOTAL DES COTISATIONS** | | | |
| 14.1 | TOTAL | C |  | ✱ |
| **§15** | **COTISATIONS FIRCA - TOTAL DES PRELEVEMENTS A REVERSER** | | | |
| 15.1 | MONTANT TOTAL A PAYER | C |  | ✱ |

## ▸ Impôts sur les bénéfices & avis de versement


### IBIC — Déclaration de l'Impôt BIC/BA

*Périodicité : Annuelle (DSF) · Échéance : 30 mai (30 juin si CAC) · 104 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **IDENTIFICATION DU CONTRIBUABLE - Entreprise individuelle** | | | |
| 1.1 | Nom et prénom de l’exploitant | S |  |  |
| 1.2 | Nom commercial | S |  |  |
| 1.3 | Activité principale | S |  |  |
| 1.4 | Activité secondaire | S |  |  |
| 1.5 | Lieu d’exercice des activités | S |  |  |
| 1.6 | Etablissements secondaires | S |  |  |
| 1.7 | Domicile de l’exploitant | S |  |  |
| **§2** | **IDENTIFICATION DU CONTRIBUABLE - Personne morale** | | | |
| 2.1 | Raison sociale | S |  |  |
| 2.2 | Sigle | S |  |  |
| 2.3 | Forme juridique | S |  |  |
| 2.4 | Activité principale | S |  |  |
| 2.5 | Activité secondaire | S |  |  |
| 2.6 | Principal établissement | S |  |  |
| 2.7 | Etablissements secondaires | S |  |  |
| 2.8 | Siège social | S |  |  |
| **§3** | **IDENTIFICATION DU CONTRIBUABLE - Informations complémentaires** | | | |
| 3.1 | Numéro de code importateur | S |  |  |
| 3.2 | Numéro du Registre du Commerce et du Crédit Mobilier (RCCM) | S |  |  |
| 3.3 | Date de début d’activité (saisir au format JJ/MM/AAAA) | S |  |  |
| 3.4 | Nom et adresse du comptable ou du conseil | S |  |  |
|  | Date de début de l’exercice (saisir au format JJ/MM/AAAA) | S |  | ✱ |
|  | Date de fin de l’exercice (saisir au format JJ/MM/AAAA) | S |  | ✱ |
| **§4** | **DETERMINATION DU RESULTAT FISCAL - Résultat net comptable** | | | |
| 4.1 | BENEFICE NET | S |  |  |
| 4.2 | PERTE NETTE | S |  |  |
| **§5** | **DETERMINATION DU RESULTAT FISCAL - Réintégrations (Charges ou pertes non déductibles ou partiellement)** | | | |
| 5.1 | Amortissements non déductibles | S |  |  |
| 5.2 | Provisions non déductibles | S |  |  |
| 5.3 | Intérêts excédentaires des comptes courants d’associés | S |  |  |
| 5.4 | Rémunérations allouées à l’exploitation individuel et aux associés des sociétés de personnes | S |  |  |
| 5.5 | Avantages en nature de l’exploitant individuel et des associés de personnes (marchandises,services.. | S |  |  |
| 5.6 | Impôts non déductibles (IMF - BIC - IGR - impôts non payés…) | S |  |  |
| 5.7 | Amendes et pénalités de toute nature | S |  |  |
| 5.8 | Plus-values exonérées non réinvesties | S |  |  |
| 5.9 | Dons et subventions | S |  |  |
| 5.10 | Rémunérations des gérants majoritaires de SARL | S |  |  |
| 5.11 | Indemnités de fonction et autres rémunérations allouées aux administrateurs | S |  |  |
| 5.12 | Autres charges non déductibles (à détailler sur feuillet séparé) | S |  |  |
| 5.13 | TOTAL DES REINTEGRATIONS | C |  | ✱ |
| **§6** | **DETERMINATION DU RESULTAT FISCAL - Déductions (Produits non ou partiellement imposables à détailler obligatoirement sur feuillet séparé)** | | | |
| 6.1 | Provisions antérieurement taxées ou définitivement exonérées réintégrées | S |  |  |
| 6.2 | Réfactions sur produits financiers | S |  |  |
| 6.3 | Réfactions sur produits d’actions | S |  |  |
| 6.4 | Déduction Art. 110 du CGI | S |  |  |
| 6.5 | Divers | S |  |  |
| 6.6 | TOTAL DES DEDUCTIONS | C |  | ✱ |
| **§7** | **DETERMINATION DU RESULTAT FISCAL - Résultat fiscal avant imputation des déficits** | | | |
| 7.1 | Résultat fiscal avant imputation des déficits | C |  | ✱ |
| **§8** | **DETERMINATION DU RESULTAT FISCAL - Imputations et Réintégrations** | | | |
| 8.1 | Déficits antérieurs imputés sur le résultat de l’exercice (ne pas saisir le symbole "-") | S |  |  |
| 8.2 | Amortissements réputés différés créés au titre de l’exercice | S |  |  |
| 8.3 | Amortissements réputés différés imputés sur le résultat | S |  |  |
| 8.4 | BENEFICE OU PERTE | C |  | ✱ |
| **§9** | **DETERMINATION DE L'IMPOT - IMPOT SUR LES BENEFICES** | | | |
| 9.1 | Bénéfice | C |  |  |
| 9.2 | Taux (en %, par ex. saisir 30 pour 30% ; décimales avec des ".") | S |  |  |
| 9.3 | Impôt sur les BIC | C |  |  |
| 9.4 | Acomptes à imputer | S |  |  |
| 9.5 | Crédit d’impôt à imputer | S |  |  |
| 9.6 | Impôt BIC à acquitter | S |  |  |
| **§10** | **DETERMINATION DE L'IMPOT - IMPOT MINIMUM FORFAITAIRE** | | | |
| 10.1 | Chiffre d’affaires TTC | S |  |  |
| 10.2 | Taux (en %, par ex. saisir 30 pour 30% ; décimales avec des ".") | S |  |  |
| 10.3 | IMF | C |  |  |
| 10.4 | Acomptes à imputer | S |  |  |
| 10.5 | Crédit d’impôt à imputer | S |  |  |
| 10.6 | IMF à acquitter | S |  |  |
| **§11** | **TABLEAU DES DEFICITS REPORTABLES AUTRES QUE LES AMORTISSEMENTS REPUTES DIFFERES EN PERIODE DEFICITAIRES** | | | |
| 11.1 | N-5 - Déficits reportables | S |  |  |
| 11.2 | N-5 - Déficits imputés sur l’exercice | S |  |  |
| 11.3 | N-4 - Déficits reportables | S |  |  |
| 11.4 | N-4 - Déficits imputés sur l’exercice | S |  |  |
| 11.5 | N-4 - Déficits restant à reporter | C |  |  |
| 11.6 | N-3 - Déficits reportables | S |  |  |
| 11.7 | N-3 - Déficits imputés sur l’exercice | S |  |  |
| 11.8 | N-3 - Déficits restant à reporter | C |  |  |
| 11.9 | N-2 - Déficits reportables | S |  |  |
| 11.10 | N-2 - Déficits imputés sur l’exercice | S |  |  |
| 11.11 | N-2 - Déficits restant à reporter | C |  |  |
| 11.12 | N-1 - Déficits reportables | S |  |  |
| 11.13 | N-1 - Déficits imputés sur l’exercice | S |  |  |
| 11.14 | N-1 - Déficits restant à reporter | C |  |  |
| **§12** | **TABLEAU DES AMORTISSEMENTS REPUTES DIFFERES EN PERIODE DEFICITAIRE (ARD)** | | | |
| 12.1 | Amortissements réputés différés reportables au titre des exercices | S |  |  |
| 12.2 | Amortissements réputés différés imputés sur le résultat de l’exercice | S |  |  |
| 12.3 | Amortissements réputés différés restant éventuellement à reporter | S |  |  |
| 12.4 | Amortissements réputés différés créés au titre de l’exercice | S |  |  |
| **§13** | **TABLEAU DES ACOMPTES D'IMPOTS SUR LES BIC ACQUITTES IMPUTABLES** | | | |
| 13.1 | Acompte 1 - Nature de l’acompte | S |  |  |
| 13.2 | Acompte 1 - Montant | S |  |  |
| 13.3 | Acompte 1 - Référence des attestations | S |  |  |
| 13.4 | Acompte 2 - Nature de l’acompte | S |  |  |
| 13.5 | Acompte 2 - Montant | S |  |  |
| 13.6 | Acompte 2 - Référence des attestations | S |  |  |
| 13.7 | Acompte 3 - Nature de l’acompte | S |  |  |
| 13.8 | Acompte 3 - Montant | S |  |  |
| 13.9 | Acompte 3 - Référence des attestations | S |  |  |
| 13.10 | Acompte 4 - Nature de l’acompte | S |  |  |
| 13.11 | Acompte 4 - Montant | S |  |  |
| 13.12 | Acompte 4 - Référence des attestations | S |  |  |
| 13.13 | Acompte 5 - Nature de l’acompte | S |  |  |
| 13.14 | Acompte 5 - Montant | S |  |  |
| 13.15 | Acompte 5 - Référence des attestations | S |  |  |
| 13.16 | Acompte 6 - Nature de l’acompte | S |  |  |
| 13.17 | Acompte 6 - Montant | S |  |  |
| 13.18 | Acompte 6 - Référence des attestations | S |  |  |
| **§14** | **TABLEAU DE SUIVI DES EXONERATIONS DES CONTRIBUABLES SOUS REGIME SPECIAL** | | | |
| 14.1 | Nature du régime d’exonération | S |  |  |
| 14.2 | Merci de préciser le régime d’exonération si "Autres" | S |  |  |
| 14.3 | Date de début de l’exonération (saisir au format JJ/MM/AAAA) | S |  |  |
| 14.4 | Date de fin de l’exonération (saisir au format JJ/MM/AAAA) | S |  |  |
| 14.5 | Année de l’exonération (Préciser: "1ère année","2ème année",etc.) | S |  |  |
| 14.6 | Sélectionner le taux appliqué (Code des investissements) | S |  |  |
| 14.7 | Saisir le taux appliqué si autre (Préciser la nature de l’éxonération et le taux) | S |  |  |
| 14.8 | Montant de l’exonération | S |  |  |
| 1.8 | Bénéficiez-vous de l’IMF réduit des stations services et distributeurs de gaz butane ? | S |  |  |

### IBNC — Déclaration Impôt BNC

*Périodicité : Annuelle (DSF) · Échéance : 30 mai (30 juin si CAC) · 99 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **RENSEIGNEMENTS DIVERS / APPORTS ET PRELEVEMENTS** | | | |
| 1.1 | Apports effectués à titre personnel - Montant | S |  |  |
| 1.2 | Apports effectués à titre personnel - Date (saisir au format JJ/MM/AAAA) | S |  |  |
| 1.3 | Apports effectués à titre personnel - Pièces justificatives | S |  |  |
| 1.4 | Prélèvements financiers effectués à titre personnel - Montant | S |  |  |
| 1.5 | Prélèvements financiers effectués à titre personnel - Date (saisir au format JJ/MM/AAAA) | S |  |  |
| 1.6 | Prélèvements financiers effectués à titre personnel - Pièces justificatives | S |  |  |
| **§1** | **RENSEIGNEMENTS DIVERS / COMPTABLE NON SALARIE** | | | |
| 1.7 | Nom et adresse du comptable non salarié | S |  |  |
| 1.8 | Nom et adresse du conseil | S |  |  |
| **§2** | **RECETTE / SOMME DES RECETTES** | | | |
| 2.1 | Recettes brutes proprement dites (honoraires, commissions, vacations, ristournes, courtage, ...) | S |  |  |
| 2.2 | Provisions ou avances sur honoraires, prestations futures | S |  |  |
| 2.3 | Remboursements de frais | S |  |  |
| 2.4 | Revenus de créances, dépôts, cautionnements, comptes courants | S |  |  |
| 2.5 | Indemnités (d’éviction, de compensation pour perte de recette) | S |  |  |
| 2.6 | Honoraires rétrocédés par des confrères | S |  |  |
| 2.7 | Subventions, cadeaux et dons reçus | S |  |  |
| 2.8 | Recettes et autres profits accessoires (*) | S |  |  |
| 2.9 | TOTAL I | C |  |  |
| **§3** | **RECETTE / A DEDUIRE** | | | |
| 3.1 | Débours payés pour le compte de clients (1) | S |  |  |
| 3.2 | Honoraires rétrocédés à des confrères (2) | S |  |  |
| 3.3 | TOTAL II | C |  |  |
| 3.4 | Base imposable à l’IMF (Total I - Total II) | C |  |  |
| 3.5 | TOTAL III | C |  |  |
| **§4** | **RECETTE / A AJOUTER** | | | |
| 4.1 | Gains provenant de la réalisation d’éléments d’actif | S |  |  |
| 4.2 | Gains provenant des sommes ou indemnités perçues en contrepartie de la cession d’activité | S |  |  |
| 4.3 | TOTAL IV | C |  |  |
| 4.4 | RECETTE BRUTE TOTAL V (TOTAL III + TOTAL IV) | C |  |  |
| **§5** | **DEPENSES** | | | |
| 5.1 | Achats de fournitures produits - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.2 | Achats de fournitures produits - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.3 | Achats de fournitures produits - Montant net déductible | C |  |  |
| 5.4 | Rémunérations versées au personnel - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.5 | Rémunérations versées au personnel - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.6 | Rémunérations versées au personnel - Montant net déductible | C |  |  |
| 5.7 | Charges sociales patronales - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.8 | Charges sociales patronales - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.9 | Charges sociales patronales - Montant net déductible | C |  |  |
| 5.10 | Contribution des patentes - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.11 | Contribution des patentes - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.12 | Contribution des patentes - Montant net déductible | C |  |  |
| 5.13 | Impôt foncier du local d’exploitation, propriété de l’entreprise - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.14 | Impôt foncier du local d’exploitation, propriété de l’entreprise-Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.15 | Impôt foncier du local d’exploitation, propriété de l’entreprise - Montant net déductible | C |  |  |
| 5.16 | Autres impôts (sauf IMF, BNC, IGR, amendes et pénalités) - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.17 | Autres impôts (sauf IMF, BNC, IGR, amendes et pénalités) - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.18 | Autres impôts (sauf IMF, BNC, IGR, amendes et pénalités) - Montant net déductible | C |  |  |
| 5.19 | Loyers des locaux professionnels loués - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.20 | Loyers des locaux professionnels loués - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.21 | Loyers des locaux professionnels loués - Montant net déductible | C |  |  |
| 5.22 | Dépenses d’entretien et de réparation - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.23 | Dépenses d’entretien et de réparation - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.24 | Dépenses d’entretien et de réparation - Montant net déductible | C |  |  |
| 5.25 | Frais de transport, déplacements - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.26 | Frais de transport, déplacements - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.27 | Frais de transport, déplacements - Montant net déductible | C |  |  |
| 5.28 | Frais de missions, réceptions - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.29 | Frais de missions, réceptions - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.30 | Frais de missions, réceptions - Montant net déductible | C |  |  |
| 5.31 | Frais divers de gestion - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.32 | Frais divers de gestion - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.33 | Frais divers de gestion - Montant net déductible | C |  |  |
| 5.34 | Frais financiers - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.35 | Frais financiers - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.36 | Frais financiers - Montant net déductible | C |  |  |
| 5.37 | Autres frais professionnels - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.38 | Autres frais professionnels - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.39 | Autres frais professionnels - Montant net déductible | C |  |  |
| 5.40 | Dotation aux amortissements - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.41 | Dotation aux amortissements - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.42 | Dotation aux amortissements - Montant net déductible | C |  |  |
| 5.43 | Pertes provenant de la réalisation d’éléments d’actif - Montant payé hors TVA _(Montant payé)_ | S |  |  |
| 5.44 | Pertes provenant de la réalisation d’éléments d’actif - Quote part privée ou non déductible _(Quote part)_ | S |  |  |
| 5.45 | Pertes provenant de la réalisation d’éléments d’actif - Montant net déductible | C |  |  |
| 5.46 | TOTAL MONTANT PAYE HORS TVA | C |  |  |
| 5.47 | TOTAL QUOTE-PART (privée ou non déductible) | C |  |  |
| 5.48 | TOTAL MONTANT NET DEDUCTIBLE | C |  |  |
| **§6** | **RESULTAT** | | | |
| 6.1 | Bénéfice (+) | C |  |  |
| 6.2 | Perte (-) | C |  |  |
| 6.3 | Déficits antérieurs | S |  |  |
| 6.4 | RESULTAT | C |  |  |
| **§7** | **DETERMINATION DE L'IMPOT - IMPOT SUR LES BENEFICES** | | | |
| 7.1 | Résultat | C |  |  |
| 7.2 | Taux (en %, par ex. saisir 30 pour 30% ; décimales avec des ".") | S |  |  |
| 7.3 | Impôt sur les BNC | C |  |  |
| 7.4 | Acomptes à imputer | S |  |  |
| 7.5 | Crédit d’impôt à imputer | S |  |  |
| 7.6 | Impôt BNC à acquitter | S |  |  |
| **§8** | **DETERMINATION DE L'IMPOT - IMPOT MINIMUM FORFAITAIRE** | | | |
| 8.1 | Chiffre d’affaires TTC | S |  |  |
| 8.2 | IMF | C | 5% |  |
| 8.3 | Acomptes à imputer | S |  |  |
| 8.4 | Crédit d’impôt à imputer | S |  |  |
| 8.5 | IMF à acquitter | S |  |  |
| **§9** | **DEFICITS REPORTABLES** | | | |
| 9.1 | N-3 - Déficits reportables | S |  |  |
| 9.2 | N-3 - Déficits imputés sur l’exercice | S |  |  |
| 9.3 | N-2 - Déficits reportables | S |  |  |
| 9.4 | N-2 - Déficits imputés sur l’exercice | S |  |  |
| 9.5 | N-2 - Déficits restant à reporter | C |  |  |
| 9.6 | N-1 - Déficits reportables | S |  |  |
| 9.7 | N-1 - Déficits imputés sur l’exercice | S |  |  |
| 9.8 | N-1 - Déficits restant à reporter | C |  |  |
|  | Date de début de l’exercice (saisir au format JJ/MM/AAAA) | S |  | ✱ |
|  | Date de fin de l’exercice (saisir au format JJ/MM/AAAA) | S |  | ✱ |

### IBICPGAZ — Impôt BIC Pétrole / Gaz

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 8 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§2** | **REMUNERATION BRUTE TOTALE ** | | | |
| 2.1 | Rémunération brute totale | S |  |  |
| **§3** | **A DEDUIRE (joindre les poèces justificatives des déductions)** | | | |
| 3.1 | Sommes reçues au titre de la mobilisation et de la démobilisation du matériel et de l’équipage | S |  |  |
| 3.2 | Remboursements de dépenses et de fournitures accessoires facturés séparément | S |  |  |
| **§4** | **SYNTHESE** | | | |
| 4.1 | Base d’imposition | C | 10% |  |
| 4.2 | Impôt BIC | C | 25% |  |
| **§5** | **CAS D'APPLICATION PETROLE / GAZ** | | | |
| 5.1 | Merci de préciser le cas d’application (secteur d’activité) : | S |  | ✱ |
| 5.2 | Montant de l’impôt BIC Pétrole | C |  |  |
| 5.3 | Montant de l’impôt BIC Gaz | C |  |  |

### IBICPGAZ_P — Impôt BIC Pétrole / Gaz - Déclaration du Prestataire de service

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 14 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§3** | **REMUNERATION BRUTE TOTALE ** | | | |
| 3.1 | Rémunération brute totale | S |  |  |
| **§4** | **A DEDUIRE (joindre les pièces justificatives des déductions)** | | | |
| 4.1 | Sommes reçues au titre de la mobilisation et de la démobilisation du matériel et de l’équipage | S |  |  |
| 4.2 | Remboursements de dépenses et de fournitures accessoires facturés séparément | S |  |  |
| **§5** | **SYNTHESE** | | | |
| 5.1 | Base d’imposition | C | 10% | ✱ |
| 5.2 | Impôt BIC | C | 25% | ✱ |
| **§1** | **SOCIETE PETROLIERE TITULAIRE DU CONTRAT DE PARTAGE DE PRODUCTION** | | | |
| 1.1 | Raison sociale de la Société pétrolière titulaire du contrat de partage de production | S |  | ✱ |
| 1.2 | NCC de la Société pétrolière | S |  | ✱ |
| **§2** | **INFORMATIONS RELATIVES AU CONTRAT DE PRESTATION** | | | |
| 2.1 | Objet de la prestation | S |  | ✱ |
| 2.2 | Date et référence du contrat de prestation | S |  | ✱ |
| 2.3 | Adresse en Côte d’Ivoire ou adresse du représentant | S |  |  |
| 2.4 | Adresse du siège social | S |  |  |
| **§5** | **CAS D'APPLICATION PETROLE / GAZ** | | | |
| 5.1 | Merci de préciser le cas d’application (secteur d’activité) : | S |  | ✱ |
| 5.2 | Montant de l’impôt BIC Pétrole | C |  |  |
| 5.3 | Montant de l’impôt BIC Gaz | C |  |  |

### AVIB — Avis de versement Impôt BIC / RNI

*Périodicité : Acompte · Échéance : 10/04, 15/06, 20/09 (RNI) · 21 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE L'IMPOT** | | | |
| 1.1 | Résultat fiscal | S |  | ✱ |
| 1.2 | Chiffre d’affaires TTC | S |  | ✱ |
| 1.3 | Impôt annuel à acquitter : BIC | S |  |  |
| 1.4 | Impôt annuel à acquitter : IMF | S |  |  |
| 1.5 | Tiers exigible | C |  | ✱ |
| 2.2 | Montant à payer 1er versement | S |  |  |
| 2.3 | Retenues et imputations, ou crédits | S |  |  |
| 2.4 | Montant total du 1er versement | C |  |  |
| **§2** | **1er VERSEMENT - DETAIL** | | | |
| 2.1 | Date du 1er versement (saisir au format JJ/MM/AAAA) | S |  |  |
| **§3** | **2ème VERSEMENT - DETAIL (laisser vide si c'est le 1er versement)** | | | |
| 3.1 | Date du 2ème versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 3.2 | Montant à payer 2eme versement | S |  |  |
| 3.3 | Retenues et imputations, ou crédits | S |  |  |
| 3.4 | Montant total du 2ème versement | C |  |  |
| **§4** | **3ème VERSEMENT - DETAIL (laisser vide si c'est le 1er ou 2ème versement)** | | | |
| 4.1 | Date du 3ème versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 4.2 | Montant à payer 3eme versement | S |  |  |
| 4.3 | Retenues et imputations, ou crédits | S |  |  |
| 4.4 | Montant total du 3ème versement | C |  |  |
| **§5** | **SYNTHESE** | | | |
| 5.1 | MONTANT A PAYER PAR TELEPAIEMENT --- BIC | F |  | ✱ |
| 5.3 | Cumul des paiements | C |  | ✱ |
| 5.4 | Reste à payer | C |  | ✱ |
| 5.2 | MONTANT A PAYER PAR TELEPAIEMENT --- IMF | F |  | ✱ |

### AVIS — Avis de versement Impôt BIC / RSI

*Périodicité : Acompte · Échéance : Fractions (RSI) · 21 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE L'IMPOT** | | | |
| 1.1 | Résultat fiscal | S |  | ✱ |
| 1.2 | Chiffre d’affaires TTC | S |  | ✱ |
| 1.3 | Impôt annuel à acquitter : BIC | S |  |  |
| 1.4 | Impôt annuel à acquitter : IMF | S |  |  |
| 1.5 | Tiers exigible | C |  | ✱ |
| 2.2 | Montant à payer 1er versement | S |  |  |
| 2.3 | Retenues et imputations | S |  |  |
| 2.4 | Montant total du 1er versement | C |  |  |
| **§2** | **1er VERSEMENT - DETAIL** | | | |
| 2.1 | Date du 1er versement (saisir au format JJ/MM/AAAA) | S |  |  |
| **§3** | **2ème VERSEMENT - DETAIL (laisser vide si c'est le 1er versement)** | | | |
| 3.1 | Date du 2ème versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 3.2 | Montant à payer 2eme versement | S |  |  |
| 3.3 | Retenues et imputations | S |  |  |
| 3.4 | Montant total du 2ème versement | C |  |  |
| **§4** | **3ème VERSEMENT - DETAIL (laisser vide si c'est le 1er ou 2ème versement)** | | | |
| 4.1 | Date du 3ème versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 4.2 | Montant à payer 3eme versement | S |  |  |
| 4.3 | Retenues et imputations | S |  |  |
| 4.4 | Montant total du 3ème versement | C |  |  |
| **§5** | **SYNTHESE** | | | |
| 5.1 | MONTANT A PAYER PAR TELEPAIEMENT --- BIC | F |  | ✱ |
| 5.3 | Cumul des paiements | C |  | ✱ |
| 5.4 | Reste à payer | C |  | ✱ |
| 5.2 | MONTANT A PAYER PAR TELEPAIEMENT --- IMF | F |  | ✱ |

### AVBA — Avis de versement Impôt BA

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 21 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE L'IMPOT** | | | |
| 1.1 | Résultat fiscal | S |  | ✱ |
| 1.2 | Chiffre d’affaires TTC | S |  | ✱ |
| 1.3 | Impôt annuel à acquitter : BA | S |  |  |
| 1.4 | Impôt annuel à acquitter : IMF | S |  |  |
| 1.5 | Tiers exigible | C |  | ✱ |
| 2.2 | Montant à payer 1er versement | S |  |  |
| 2.3 | Retenues et imputations | S |  |  |
| 2.4 | Montant total du 1er versement | C |  |  |
| **§2** | **1er VERSEMENT - DETAIL** | | | |
| 2.1 | Date du 1er versement (saisir au format JJ/MM/AAAA) | S |  |  |
| **§3** | **2ème VERSEMENT - DETAIL (laisser vide si c'est le 1er versement)** | | | |
| 3.1 | Date du 2ème versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 3.2 | Montant à payer 2eme versement | S |  |  |
| 3.3 | Retenues et imputations | S |  |  |
| 3.4 | Montant total du 2ème versement | C |  |  |
| **§4** | **3ème VERSEMENT - DETAIL (laisser vide si c'est le 1er ou 2ème versement)** | | | |
| 4.1 | Date du 3ème versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 4.2 | Montant à payer 3eme versement | S |  |  |
| 4.3 | Retenues et imputations | S |  |  |
| 4.4 | Montant total du 3ème versement | C |  |  |
| **§5** | **SYNTHESE** | | | |
| 5.1 | MONTANT A PAYER PAR TELEPAIEMENT --- BA | F |  | ✱ |
| 5.2 | MONTANT A PAYER PAR TELEPAIEMENT --- IMF | F |  | ✱ |
| 5.3 | Cumul des paiements | C |  | ✱ |
| 5.4 | Reste à payer | C |  | ✱ |

### AVNC — Avis de versement Impôt BNC

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 21 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE L'IMPOT** | | | |
| 1.1 | Résultat fiscal | S |  | ✱ |
| 1.2 | Chiffre d’affaires TTC | S |  | ✱ |
| 1.3 | Impôt annuel à acquitter : BNC | S |  |  |
| 1.4 | Impôt annuel à acquitter : IMF | S |  |  |
| 1.5 | Tiers exigible | C |  | ✱ |
| 2.2 | Montant à payer 1er versement | S |  |  |
| 2.3 | Retenues et imputations | S |  |  |
| 2.4 | Montant total du 1er versement | C |  |  |
| **§2** | **1er VERSEMENT - DETAIL** | | | |
| 2.1 | Date du 1er versement (saisir au format JJ/MM/AAAA) | S |  |  |
| **§3** | **2ème VERSEMENT - DETAIL (laisser vide si c'est le 1er versement)** | | | |
| 3.1 | Date du 2ème versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 3.2 | Montant à payer 2eme versement | S |  |  |
| 3.3 | Retenues et imputations | S |  |  |
| 3.4 | Montant total du 2ème versement | C |  |  |
| **§4** | **3ème VERSEMENT - DETAIL (laisser vide si c'est le 1er ou 2ème versement)** | | | |
| 4.1 | Date du 3ème versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 4.2 | Montant à payer 3eme versement | S |  |  |
| 4.3 | Retenues et imputations | S |  |  |
| 4.4 | Montant total du 3ème versement | C |  |  |
| **§5** | **SYNTHESE** | | | |
| 5.1 | MONTANT A PAYER PAR TELEPAIEMENT --- BNC | F |  | ✱ |
| 5.2 | MONTANT A PAYER PAR TELEPAIEMENT --- IMF | F |  | ✱ |
| 5.3 | Cumul des paiements | C |  | ✱ |
| 5.4 | Reste à payer | C |  | ✱ |

## ▸ Patente


### PATCOM — Patente commerce (hors DGE)

*Périodicité : Annuelle · Échéance : Selon avis · 52 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **IDENTIFICATION DE L'ETABLISSEMENT** | | | |
| 1.1 | Localité | S |  | ✱ |
| 1.2 | Commune | S |  | ✱ |
| 1.10 | Autres indications | S |  |  |
| 1.11 | Date de début d’activité (saisir au format JJ/MM/AAAA) | S |  | ✱ |
| **§2** | **DROITS SUR LE CHIFFRE D'AFFAIRES** | | | |
| 2.1 | Chiffre d’affaires HT imposable au taux 0.50% | S |  |  |
| 2.2 | Droits sur Chiffre d’affaires au taux 0.50% | F | 0.5% |  |
| 2.3 | Chiffre d’affaires HT imposable au taux 0.70% | S |  |  |
| 2.4 | Droits sur Chiffre d’affaires au taux 0.70% | C | 0.7% |  |
| 2.5 | Total Chiffre d’affaires hors taxes | C |  | ✱ |
| 2.6 | Total Droits sur le chiffre d’affaires | C |  | ✱ |
| **§3** | **DROITS SUR LA VALEUR LOCATIVE / C1 - Loyer annuel** | | | |
| 3.1 | Loyer annuel | S |  |  |
| **§4** | **DROITS SUR LA VALEUR LOCATIVE / C2 - Valeurs locatives des locaux et terrains non compris dans le loyer** | | | |
| 4.1 | Type d’établissement (pour application des taux correspondants) | S |  | ✱ |
| 4.2 | Constructions - Valeur brute au bilan | S |  |  |
| 4.3 | Constructions - Valeur locative | F | 15% |  |
| 4.4 | Bureaux - Valeur brute au bilan | S |  |  |
| 4.5 | Bureaux - Valeur locative | F | 15% |  |
| 4.6 | Magasins - Valeur brute au bilan | S |  |  |
| 4.7 | Magasins - Valeur locative | F | 15% |  |
| 4.8 | Hangars - Valeur brute au bilan | S |  |  |
| 4.9 | Hangars - Valeur locative | F | 15% |  |
| 4.10 | Usines - Valeur brute au bilan | S |  |  |
| 4.11 | Usines - Valeur locative | F | 5.6% |  |
| 4.12 | Bâtiments - Valeur brute au bilan | S |  |  |
| 4.13 | Bâtiments - Valeur locative | F | 5.6% |  |
| 4.14 | Terrains - Valeur brute au bilan | S |  |  |
| 4.15 | Terrains - Valeur locative | F | 5.6% |  |
| 4.16 | Sous-total des valeurs locatives des locaux et terrains | C |  | ✱ |
| **§5** | **DROITS SUR LA VALEUR LOCATIVE / Synthèse** | | | |
| 5.1 | Valeur locative (C1 + C2) | C |  | ✱ |
| 5.2 | Taux selon le périmètre communale | S |  | ✱ |
| 5.3 | Droit sur la valeur locative | C |  | ✱ |
| 5.4 | Droit sur la valeur locative reporté de la déclaration additive | S |  |  |
| **§6** | **SYNTHESE DE LA PATENTE** | | | |
| 6.1 | Patente (M1 + M2 + M3) | C |  | ✱ |
| 6.2 | Taux d’application des droits de la patente | S |  |  |
| 6.3 | Nature du régime d’exonération | S |  |  |
| 6.4 | Montant de l’exonération | S |  |  |
| 6.5 | Date du début de l’exonération (saisir au format JJ/MM/AAAA) | S |  |  |
| 6.6 | Date de fin de l’exonération (saisir au format JJ/MM/AAAA) | S |  |  |
| 6.7 | Année de l’exonération (saisir "1ère année", "2ème année", ...) | S |  |  |
| 6.8 | Patente due | C |  | ✱ |
| **§7** | **LICENCES** | | | |
| 7.1 | Montant des Licences | S |  |  |
| **§8** | **ENTREPRISES CREEES DURANT L'EXERCICE PRECEDENT** | | | |
| 8.1 | Patente payée à la création | S |  |  |
| 8.2 | Régularisation | S |  |  |
| **§9** | **PATENTE ET LICENCE A PAYER** | | | |
| 9.1 | Montant total de la Patente et des Licences à payer | C |  | ✱ |
| 1.3 | Quartier (ou zone) | S |  |  |
| 1.4 | Rue | S |  |  |
| 1.5 | Ilôt | S |  |  |
| 1.6 | Numéro de lot | S |  |  |
| 1.7 | Section/Parcelle | S |  |  |
| 1.8 | BP | S |  |  |
| 1.9 | Téléphone | S |  |  |
|  | Merci de bien vouloir sélectionner le Poste Comptable de la DGI concerné par cette déclaration : | S |  | ✱ |
| 1.12 | L’établissement est-il un entrepôt ? (pour application de l’exonération du Droits sur le CA) | S |  |  |

### PATCOM_S — Patente commerce (DGE)

*Périodicité : Annuelle · Échéance : Selon avis (DGE) · 52 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **IDENTIFICATION DE L'ETABLISSEMENT** | | | |
| 1.1 | Localité | S |  | ✱ |
| 1.2 | Commune | S |  | ✱ |
| 1.10 | Autres indications | S |  |  |
| 1.11 | Date de début d’activité (saisir au format JJ/MM/AAAA) | S |  |  |
| **§2** | **DROITS SUR LE CHIFFRE D'AFFAIRES** | | | |
| 2.1 | Chiffre d’affaires HT imposable au taux 0.50% | S |  |  |
| 2.2 | Droits sur Chiffre d’affaires au taux 0.50% | F | 0.5% |  |
| 2.3 | Chiffre d’affaires HT imposable au taux 0.70% | S |  |  |
| 2.4 | Droits sur Chiffre d’affaires au taux 0.70% | C | 0.7% |  |
| 2.5 | Total Chiffre d’affaires hors taxes | C |  | ✱ |
| 2.6 | Total Droits sur le chiffre d’affaires | C |  | ✱ |
| **§3** | **DROITS SUR LA VALEUR LOCATIVE / C1 - Loyer annuel** | | | |
| 3.1 | Loyer annuel | S |  |  |
| **§4** | **DROITS SUR LA VALEUR LOCATIVE / C2 - Valeurs locatives des locaux et terrains non compris dans le loyer** | | | |
| 4.1 | Type d’établissement (pour application des taux correspondants) | S |  | ✱ |
| 4.2 | Constructions - Valeur brute au bilan | S |  |  |
| 4.3 | Constructions - Valeur locative | F | 15% |  |
| 4.3 | Bureaux - Valeur brute au bilan | S |  |  |
| 4.4 | Bureaux - Valeur locative | F | 15% |  |
| 4.5 | Magasins - Valeur brute au bilan | S |  |  |
| 4.6 | Magasins - Valeur locative | F | 15% |  |
| 4.7 | Hangars - Valeur brute au bilan | S |  |  |
| 4.8 | Hangars - Valeur locative | F | 15% |  |
| 4.9 | Usines - Valeur brute au bilan | S |  |  |
| 4.10 | Usines - Valeur locative | F | 5.6% |  |
| 4.11 | Bâtiments - Valeur brute au bilan | S |  |  |
| 4.12 | Bâtiments - Valeur locative | F | 5.6% |  |
| 4.13 | Terrains - Valeur brute au bilan | S |  |  |
| 4.14 | Terrains - Valeur locative | F | 5.6% |  |
| 4.15 | Sous-total des valeurs locatives des locaux et terrains | C |  | ✱ |
| **§5** | **DROITS SUR LA VALEUR LOCATIVE / Synthèse** | | | |
| 5.1 | Valeur locative (C1 + C2) | C |  | ✱ |
| 5.2 | Taux selon le périmètre communale | S |  | ✱ |
| 5.3 | Droit sur la valeur locative | C |  | ✱ |
| 5.4 | Droit sur la valeur locative reporté de la déclaration additive | S |  |  |
| **§6** | **SYNTHESE DE LA PATENTE** | | | |
| 6.1 | Patente (M1 + M2 + M3) | C |  | ✱ |
| 6.2 | Taux d’application des droits de la patente | S |  |  |
| 6.3 | Nature du régime d’exonération | S |  |  |
| 6.4 | Montant de l’exonération | S |  |  |
| 6.5 | Date du début de l’exonération (saisir au format JJ/MM/AAAA) | S |  |  |
| 6.6 | Date de fin de l’exonération (saisir au format JJ/MM/AAAA) | S |  |  |
| 6.7 | Année de l’exonération (saisir "1ère année", "2ème année", ...) | S |  |  |
| 6.8 | Patente due | C |  | ✱ |
| **§7** | **LICENCES** | | | |
| 7.1 | Montant des Licences | S |  |  |
| **§8** | **ENTREPRISES CREEES DURANT L'EXERCICE PRECEDENT** | | | |
| 8.1 | Patente payée à la création | S |  |  |
| 8.2 | Régularisation | S |  |  |
| **§9** | **PATENTE ET LICENCE A PAYER** | | | |
| 9.1 | Montant total de la Patente et des Licences à payer | C |  | ✱ |
| 1.3 | Quartier (ou zone) | S |  |  |
| 1.4 | Rue | S |  |  |
| 1.5 | Ilôt | S |  |  |
| 1.6 | Numéro de lot | S |  |  |
| 1.7 | Section/Parcelle | S |  |  |
| 1.8 | BP | S |  |  |
| 1.9 | Téléphone | S |  |  |
|  | Merci de bien vouloir sélectionner le Poste Comptable de la DGI concerné par cette déclaration : | S |  | ✱ |
| 1.12 | L’établissement est-il un entrepôt ? (pour application de l’exonération du Droits sur le CA) | S |  |  |

### AVPA — Avis de versement Patente commerce (hors DGE)

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 12 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE L'IMPOT** | | | |
| 1.1 | Impôt annuel à acquitter (de l’ensemble des établissements et succursales y compris le siège) | S |  | ✱ |
| 1.2 | Fraction exigible | C | 50% | ✱ |
| 2.2 | Montant du 1er versement | S |  |  |
| **§2** | **1er VERSEMENT - DETAIL** | | | |
| 2.1 | Date du 1er versement (saisir au format JJ/MM/AAAA) | S |  |  |
| **§3** | **2ème VERSEMENT - DETAIL (laisser vide si c'est le 1er versement)** | | | |
| 3.1 | Date du 2ème versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 3.2 | Montant 2ème du versement | S |  |  |
| **§4** | **SYNTHESE** | | | |
| 4.1 | MONTANT TOTAL A PAYER POUR CE VERSEMENT | F |  | ✱ |
| 4.4 | Cumul des paiements | C |  | ✱ |
| 4.5 | Reste à payer | C |  | ✱ |
|  | Merci de bien vouloir sélectionner le Poste Comptable de la DGI concerné par cette déclaration : | S |  | ✱ |
| 4.2 |   - dont montant à payer pour la PATENTE | S |  | ✱ |
| 4.3 |   - dont montant à payer pour la LICENCE | S |  | ✱ |

### AVPA_S — Avis de versement Patente commerce (DGE)

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 12 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE L'IMPOT** | | | |
| 1.1 | Impôt annuel à acquitter (de l’ensemble des établissements et succursales y compris le siège) | S |  | ✱ |
| 1.2 | Fraction exigible | C | 50% | ✱ |
| **§2** | **1er VERSEMENT - DETAIL** | | | |
| 2.1 | Date du 1er versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 2.2 | Montant du 1er versement | S |  |  |
| **§3** | **2ème VERSEMENT - DETAIL (laisser vide si c'est le 1er versement)** | | | |
| 3.1 | Date du 2ème versement (saisir au format JJ/MM/AAAA) | S |  |  |
| 3.2 | Montant 2ème du versement | S |  |  |
| **§4** | **SYNTHESE** | | | |
| 4.1 | MONTANT TOTAL A PAYER POUR CE VERSEMENT | F |  | ✱ |
| 4.4 | Cumul des paiements | C |  | ✱ |
| 4.5 | Reste à payer | C |  | ✱ |
|  | Merci de bien vouloir sélectionner le Poste Comptable de la DGI concerné par cette déclaration : | S |  | ✱ |
| 4.2 |   - dont montant à payer pour la PATENTE | S |  | ✱ |
| 4.3 |   - dont montant à payer pour la LICENCE | S |  | ✱ |

## ▸ Assurances


### TASSUR — Taxe sur les contrats d'Assurances

*Périodicité : Mensuelle · Échéance : 15 du mois suivant · 33 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **NAVIGATION MARITIME, FLUVIALE OU AERIENNE** | | | |
| 1.1 | Primes et accessoires encaissées | S |  |  |
| 1.2 | Primes ou fractions de primes remboursées | S |  |  |
| 1.3 | Base d’imposition | C |  | ✱ |
| 1.4 | Montant de l’impôt | C | 7% | ✱ |
| **§2** | **INCENDIE** | | | |
| 2.1 | Primes et accessoires encaissées | S |  |  |
| 2.2 | Primes ou fractions de primes remboursées | S |  |  |
| 2.3 | Base d’imposition | C |  | ✱ |
| 2.4 | Montant de l’impôt | C | 25% | ✱ |
| **§3** | **RENTE VIAGERE** | | | |
| 3.1 | Primes et accessoires encaissées | S |  |  |
| 3.2 | Primes ou fractions de primes remboursées | S |  |  |
| 3.3 | Base d’imposition | C |  | ✱ |
| 3.4 | Montant de l’impôt | C | 5% | ✱ |
| **§4** | **CREDITS A L'EXPORTATION** | | | |
| 4.1 | Primes et accessoires encaissées | S |  |  |
| 4.2 | Primes ou fractions de primes remboursées | S |  |  |
| 4.3 | Base d’imposition | C |  | ✱ |
| 4.4 | Montant de l’impôt | C | 0.1% | ✱ |
| **§5** | **RISQUE AUTOMOBILE** | | | |
| 5.1 | Primes et accessoires encaissées | S |  |  |
| 5.2 | Primes ou fractions de primes remboursées | S |  |  |
| 5.3 | Base d’imposition | C |  | ✱ |
| 5.4 | Montant de l’impôt | C | 14.5% | ✱ |
| **§6** | **MALADIE INDIVIDUELLE** | | | |
| 6.1 | Primes et accessoires encaissées | S |  |  |
| 6.2 | Primes ou fractions de primes remboursées | S |  |  |
| 6.3 | Base d’imposition | C |  | ✱ |
| 6.4 | Montant de l’impôt | C | 8% | ✱ |
| **§7** | **MALADIE DE GROUPE** | | | |
| 7.1 | Primes et accessoires encaissées | S |  |  |
| 7.2 | Primes ou fractions de primes remboursées | S |  |  |
| 7.3 | Base d’imposition | C |  | ✱ |
| 7.4 | Montant de l’impôt | C | 3% | ✱ |
| **§8** | **AUTRES RISQUES** | | | |
| 8.1 | Primes et accessoires encaissées | S |  |  |
| 8.2 | Primes ou fractions de primes remboursées | S |  |  |
| 8.3 | Base d’imposition | C |  | ✱ |
| 8.4 | Montant de l’impôt | C | 14.5% | ✱ |
| **§9** | **MONTANT TOTAL A PAYER** | | | |
| 9.1 | Montant total de la taxe à payer | C |  | ✱ |

### TASSURPGAZ — Taxe sur les contrats d'assurance Pétrole / Gaz

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 5 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **REMUNERATION BRUTE TOTALE ** | | | |
| 1.1 | Rémunération brute totale | S |  | ✱ |
| **§2** | **A DEDUIRE (joindre les pièces justificatives des déductions)** | | | |
| 2.1 | Sommes reçues au titre de la mobilisation et de la démobilisation du matériel et de l’équipage | S |  |  |
| 2.2 | Remboursements de dépenses et de fournitures accessoires facturés séparément | S |  |  |
| **§3** | **SYNTHESE** | | | |
| 3.1 | Base d’imposition | C |  |  |
| 3.2 | Taxe sur les contrats d’assurance à payer | C | 0.1% |  |

## ▸ Accises, tabac, boissons, produits spécifiques


### TSTBC — Droits d'accises (Tabac, Boissons et autres taxes spécifiques)

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 49 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **TABACS** | | | |
| 1.1 | Cigares - Quantité | S |  |  |
| 1.2 | Cigares - Base d’imposition | S |  |  |
| 1.3 | Cigares - Montant de la taxe | C | 35% |  |
| 1.4 | Cigarillos - Quantité | S |  |  |
| 1.5 | Cigarillos - Base d’imposition | S |  |  |
| 1.6 | Cigarillos - Montant de la taxe | C | 35% |  |
| 1.7 | Cigarettes - Quantité | S |  |  |
| 1.8 | Cigarettes - Base d’imposition | S |  |  |
| 1.9 | Cigarettes - Montant de la taxe | C | 35% |  |
| 1.12 | Tabac à fumer - Montant | C | 35% |  |
| 1.15 | Autres tabacs - Montant | C | 35% |  |
| 1.18 | Succédanés de tabacs - Montant | C | 35% |  |
| 1.10 | Tabac à fumer - Quantité | S |  |  |
| 1.13 | Autres tabacs - Quantité | S |  |  |
| 1.16 | Succédanés de tabacs - Quantité | S |  |  |
| 1.11 | Tabac à fumer - Base d’imposition | S |  |  |
| 1.14 | Autres tabacs - Base d’imposition | S |  |  |
| 1.17 | Succédanés de tabacs - Base d’imposition | S |  |  |
| **§2** | **BOISSONS** | | | |
| 2.1 | Champagnes - Quantité | S |  |  |
| 2.2 | Champagnes - Base d’imposition | S |  |  |
| 2.3 | Champagnes - Montant | C | 25% |  |
| 2.4 | Vins ordinaires - Quantité | S |  |  |
| 2.5 | Vins ordinaires - Base d’imposition | S |  |  |
| 2.6 | Vins ordinaires - Montant | C | 25% |  |
| 2.7 | Vins mousseux et vins AC et assimilés - Quantité | S |  |  |
| 2.8 | Vins mousseux et vins AC et assimilés - Base d’imposition | S |  |  |
| 2.9 | Vins mousseux et vins AC et assimilés - Montant | C | 30% |  |
| 2.10 | Bières et cidres - Quantité | S |  |  |
| 2.11 | Bières et cidres - Base d’imposition | S |  |  |
| 2.12 | Bières et cidres - Montant | C | 15% |  |
| 2.13 | Autres boissons alcoolisées titrant moins de 35° d’alcool - Quantité | S |  |  |
| 2.14 | Autres boissons alcoolisées titrant moins de 35° d’alcool - Base d’imposition | S |  |  |
| 2.15 | Autres boissons alcoolisées titrant moins de 35° d’alcool - Montant | C | 35% |  |
| 2.16 | Autres boissons alcoolisées titrant plus de 35° d’alcool - Quantité | S |  |  |
| 2.17 | Autres boissons alcoolisées titrant plus de 35° d’alcool - Base d’imposition | S |  |  |
| 2.18 | Autres boissons alcoolisées titrant plus de 35° d’alcool - Montant | C | 45% |  |
| 2.20 | Boissons non alcoolisées à l’exclusion de l’eau - Quantité | S |  |  |
| 2.21 | Boissons non alcoolisées à l’exclusion de l’eau - Base d’imposition | S |  |  |
| 2.22 | Total de la Taxe sur les Boissons non alcoolisées à l’exclusion de l’eau | C | 12% |  |
| **§3** | **CARTOUCHES** | | | |
| 3.1 | Cartouches chargées - Quantité | S |  |  |
| 3.2 | Cartouches chargées - Tarif | S |  |  |
| 3.3 | Cartouches chargées - Montant | C |  |  |
| 3.4 | Douilles amorcées ou amorces - Quantité | S |  |  |
| 3.5 | Douilles amorcées ou amorces - Tarif | S |  |  |
| 3.6 | Douilles amorcées ou amorces - Montant | C |  |  |
| 1.19 | Total de la Taxe sur le Tabac | C |  |  |
| 2.23 | Total de la Taxe sur les Boissons | C |  |  |
| 3.7 | Total de la Taxe sur les Cartouches | C |  |  |
| 2.19 | Total de la Taxe sur les Boissons Alcoolisés | C |  |  |

### TSTDS — Taxe Spéciale sur le Tabac pour le Développement du Sport

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 19 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE** | | | |
| 1.1 | Cigares - Quantité | S |  |  |
| 1.2 | Cigares - Base d’imposition | S |  |  |
| 1.3 | Cigares - Montant de la taxe | C | 5% |  |
| 1.4 | Cigarillos - Quantité | S |  |  |
| 1.5 | Cigarillos - Base d’imposition | S |  |  |
| 1.6 | Cigarillos - Montant de la taxe | C | 5% |  |
| 1.7 | Cigarettes - Quantité | S |  |  |
| 1.8 | Cigarettes - Base d’imposition | S |  |  |
| 1.9 | Cigarettes - Montant de la taxe | C | 5% |  |
| 1.10 | Tabac à fumer - Quantité | S |  |  |
| 1.11 | Tabac à fumer - Base d’imposition | S |  |  |
| 1.12 | Tabac à fumer - Montant | C | 5% |  |
| 1.13 | Autres tabacs - Quantité | S |  |  |
| 1.14 | Autres tabacs - Base d’imposition | S |  |  |
| 1.15 | Autres tabacs - Montant | C | 5% |  |
| 1.16 | Succédanés de tabacs - Quantité | S |  |  |
| 1.17 | Succédanés de tabacs - Base d’imposition | S |  |  |
| 1.18 | Succédanés de tabacs - Montant | C | 5% |  |
| **§2** | **MONTANT DE LA TAXE** | | | |
| 2.1 | Montant de la taxe à payer | C |  | ✱ |

### TSIDA — Taxe de Solidarité de Lutte contre le SIDA et le Tabagisme

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 19 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE** | | | |
| 1.1 | Cigares - Quantité | S |  |  |
| 1.2 | Cigares - Base d’imposition | S |  |  |
| 1.3 | Cigares - Montant de la taxe | C | 2% |  |
| 1.4 | Cigarillos - Quantité | S |  |  |
| 1.5 | Cigarillos - Base d’imposition | S |  |  |
| 1.6 | Cigarillos - Montant de la taxe | C | 2% |  |
| 1.7 | Cigarettes - Quantité | S |  |  |
| 1.8 | Cigarettes - Base d’imposition | S |  |  |
| 1.9 | Cigarettes - Montant de la taxe | C | 2% |  |
| 1.10 | Tabac à fumer - Quantité | S |  |  |
| 1.11 | Tabac à fumer - Base d’imposition | S |  |  |
| 1.12 | Tabac à fumer - Montant | C | 2% |  |
| 1.13 | Autres tabacs - Quantité | S |  |  |
| 1.14 | Autres tabacs - Base d’imposition | S |  |  |
| 1.15 | Autres tabacs - Montant | C | 2% |  |
| 1.16 | Succédanés de tabacs - Quantité | S |  |  |
| 1.17 | Succédanés de tabacs - Base d’imposition | S |  |  |
| 1.18 | Succédanés de tabacs - Montant | C | 2% |  |
| **§2** | **MONTANT DE LA TAXE** | | | |
| 2.1 | Montant de la taxe à payer | C |  | ✱ |

### TADV — Taxe Ad Valorem

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 6 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **CALCUL DE LA TAXE MINIERE** | | | |
| 1.1 | Chiffre d’affaires HT Total | S |  | ✱ |
| 1.2 | Frais de déduction | S |  | ✱ |
| 1.3 | Assiette de la taxe | C |  | ✱ |
| 1.4 | TAXE MINIERE DUE | S |  | ✱ |
| 1.5 | Part DGI à payer | C | 85% | ✱ |
| 1.6 | Part Ministère des Mines | C | 15% | ✱ |

### TCPP — Taxe de Consommation sur les Produits Pétroliers

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 2 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE** | | | |
| 1.1 | Montant déclaré | S |  | ✱ |
| 1.2 | Montant à payer | S |  | ✱ |

### TABATTAGE — Taxe d'Abattage

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 5 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE** | | | |
| 1.1 | Montant déclaré | S |  | ✱ |
| 1.2 | Montant à payer | S |  | ✱ |
| **§2** | **PRECISION DU CAS D'APPLICATION** | | | |
| 2.1 | Merci de préciser le cas d’application : | S |  | ✱ |
| 2.2 | Montant de la Taxe d’abattage | C |  | ✱ |
| 2.3 | Montant de la Retenue à la source SODEFOR | C |  | ✱ |

### TCGS — Taxe sur le Caoutchouc Granulé Spécifié

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 3 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE** | | | |
| 1.1 | Cours international moyen mensuel du caoutchouc (CIM) | S |  | ✱ |
| 1.2 | Chiffre d’affaires mensuel hors taxes | S |  | ✱ |
| 1.3 | Montant à payer | C |  | ✱ |

### TSPMP — Taxe Spéciale sur certains Produits en Matière Plastique

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 6 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA BASE IMPOSABLE** | | | |
| 1.1 | Matières plastiques (en kg) | S |  |  |
| 1.2 | Sacs (en kg) | S |  |  |
| 1.3 | Sachets (en kg) | S |  |  |
| 1.4 | Film plastique (en kg) | S |  |  |
| 1.5 | Quantité total | C |  | ✱ |
| **§2** | **MONTANT DE LA TAXE** | | | |
| 2.1 | Montant de la taxe à payer | C | 5000% | ✱ |

### TEP — Taxe d'Exploitation Pétrolière

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 4 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE** | | | |
|  | Montant de la taxe à payer | S |  | ✱ |
| **§2** | **CAS D'APPLICATION PETROLE / GAZ** | | | |
| 2.1 | Merci de préciser le cas d’application (secteur d’activité) : | S |  | ✱ |
| 2.2 | Montant de la Taxe d’Exploitation Pétrole | C |  |  |
| 2.3 | Montant de la Taxe d’Exploitation Gaz | C |  |  |

### TEFPF — Taxe sur l'Exportation de la Ferraille et des Produits Ferreux

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 1 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **MONTANT DE LA TAXE** | | | |
|  | Montant de la taxe à payer | S |  | ✱ |

## ▸ Télécoms, jeux, culture, tourisme, environnement


### TETTIC — Taxe sur les Entreprises de Télécommunication et des Technologies de l'Information et de la Communication

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 2 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE** | | | |
| 1.1 | Chiffre d’affaires mensuel hors taxes | S |  | ✱ |
| 1.2 | Montant de la taxe à payer | C | 5% | ✱ |

### TSCT — Taxe Spécifique sur les Communications Téléphoniques et les Technologies de l'Information et de la Communication

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 4 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE** | | | |
| 1.1 | Chiffre d’affaire taxable hors taxe | S |  | ✱ |
| 1.2 | Montant | C | 3% | ✱ |
| 1.3 | Régularisation annuelle | S |  |  |
| 1.4 | Montant à payer | C |  | ✱ |

### TDNTZR — Taxe pour le Développement des Nouvelles Technologies en Zones Rurales

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 11 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **BASE IMPOSABLE** | | | |
| 1.1 | Chiffre d’affaires mensuel HT | S |  | ✱ |
| **§2** | **DETERMINATION DE LA TAXE** | | | |
| 2.1 | Montant de la taxe pour le mois | C | 2% |  |
| **§3** | **REGULARISATION ANNUELLE (15 janvier)** | | | |
| 3.1 | Chiffre d’affaires annuel régularisé | S |  |  |
| 3.2 | Chiffre d’affaires total mensuel déclaré pendant l’année (y compris déclaré ce mois) | S |  |  |
| 3.3 | Différence | C |  |  |
| 3.4 | Solde de régularisation | C | 2% |  |
| **§4** | **CREDIT** | | | |
| 4.1 | Montant du crédit de régularisation | C |  |  |
| 4.2 | Imputation du mois | S |  |  |
| 4.3 | Solde à reporter | C |  | ✱ |
| **§5** | **MONTANT A PAYER** | | | |
| 5.1 | Montant de la taxe à payer | C |  | ✱ |
| **§6** | **MONTANT CUMULE AU TITRE DE L'ANNEE** | | | |
| 6.1 | Montant cumulé de la taxe acquittée au titre de l’année | S |  | ✱ |

### PJC — Prélèvement Jeux Casino

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 7 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **Chiffre d'affaires mensuel hors taxes (CA HT) inférieur à 200 millions FCFA** | | | |
| 1.1 | Recette brute | S |  | ✱ |
| 1.2 | Montant de l’impôt | C | 5% |  |
| **§4** | **MONTANT TOTAL DU PRELEVEMENT** | | | |
| 4.1 | MONTANT TOTAL A PAYER | C |  |  |
| **§2** | **Chiffre d'affaires mensuel hors taxes (CA HT) entre 200 et 400 millions FCFA** | | | |
| 2.1 | Recette brute | S |  |  |
| 2.2 | Montant de l’impôt | C | 20% |  |
| **§3** | **Chiffre d'affaires mensuel hors taxes (CA HT) supérieur à 400 millions FCFA** | | | |
| 3.1 | Recette brute | S |  |  |
| 3.2 | Montant de l’impôt | C | 25% |  |

### PAJC — Prélèvement Additionnel sur les Jeux de Casino, de machines à sous et sur les jeux de hasard organisés par la LONACI

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 9 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **MONTANT DE LA TAXE** | | | |
| 1.1 | Chiffre d’affaires total HT | S |  | ✱ |
| 1.2 | Montant du prélèvement | C | 5% | ✱ |
| **§2** | **REGULARISATION ANNUELLE** | | | |
| 2.1 | Chiffre d’affaire annuel | S |  |  |
| 2.2 | Montant de la taxe exigible | C | 5% |  |
| 2.3 | Montant de la taxe déclarée (y compris le montant de la taxe de ce mois) | S |  |  |
| 2.4 | Différence | C |  |  |
| 2.5 | Crédit reporté | S |  |  |
| **§3** | **SYNTHESE** | | | |
| 3.1 | Montant à payer | C |  | ✱ |
| 3.2 | Crédit à reporter | C |  | ✱ |

### TPUB — Taxe sur la Publicité

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 6 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA BASE IMPOSABLE** | | | |
| 1.1 | Chiffre d’affaires total TTC réalisé sur les messages publicitaires | S |  | ✱ |
| 1.2 | A déduire : Chiffre d’affaires exonéré | S |  |  |
| 1.3 | Différence | C |  | ✱ |
| 1.4 | A ajouter : Livraisons à soi-même | S |  |  |
| 1.5 | Chiffre d’affaires total taxable | C |  | ✱ |
| **§2** | **MONTANT DE LA TAXE** | | | |
| 2.1 | Montant de la taxe à payer | C | 3% | ✱ |

### PPPC — Prélèvement au Profit de la Promotion de la Culture

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 8 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE L'IMPOT** | | | |
| 1.1 | Chiffre d’affaires taxable HT | S |  | ✱ |
| 1.2 | Montant de l’impôt | C | 0.2% | ✱ |
| **§2** | **REGULARISATION ANNUELLE (15 janvier)** | | | |
| 2.1 | Chiffre d’affaires annuel régularisé | S |  |  |
| 2.2 | Montant de la taxe exigible sur l’année | C | 0.2% |  |
| 2.3 | Montant de la taxe déclarée sur l’année (y compris le montant de ce mois-ci) | S |  |  |
| 2.4 | Différence | C |  |  |
| **§3** | **SYNTHESE** | | | |
| 3.1 | Montant à payer | C |  | ✱ |
| 3.2 | Montant à reporter | C |  | ✱ |

### TDT — Taxe pour le Développement Touristique

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 2 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE** | | | |
| 1.1 | Chiffre d’affaire taxable HT | S |  | ✱ |
| 1.2 | Montant | C | 1.5% | ✱ |

### TSPE — Taxe de Salubrité et de Protection de l'Environnement

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 7 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE - VEHICULES D'OCCASION IMPORTES DE PLUS DE 5 ANS** | | | |
| 1.1 | Transport de personnes / Véhicules agés de 5 à 10 ans --- Quantité importée | S |  |  |
| 1.2 | Montant de la taxe | C | 5e+06% |  |
| 1.3 | Transport de marchandises / Véhicules < 4 tonnes et agés de 5 à 10 ans  --- Quantité importée | S |  |  |
| 1.4 | Montant de la taxe | C | 5e+06% |  |
| 1.5 | Transport de marchandises / Véhicules > 4 tonnes  et agés de 10 à 15 ans --- Quantité importée | S |  |  |
| 1.6 | Montant de la taxe | C | 1e+07% |  |
| **§1** | **MONTANT DE LA TAXE** | | | |
| 1.7 | Montant total de la taxe à payer | C |  | ✱ |

### RRTI — Redevance Radio Télévision Ivoirienne

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 2 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA REDEVANCE** | | | |
| 1.1 | Montant déclaré | S |  | ✱ |
| 1.2 | Montant à payer | S |  | ✱ |

### CSBA — Contribution de Solidarité sur les Billets d'Avion

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 7 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA CONTRIBUTION** | | | |
| 1.1 | Billets en classe économique : Nombre de passagers | S |  | ✱ |
| 1.2 | Billets en classe économique : Montant de la taxe collectée | C | 200000% | ✱ |
| 1.3 | Billets en classe affaires : Nombre de passagers | S |  | ✱ |
| 1.4 | Billets en classe affaires : Montant de la taxe collectée | C | 500000% | ✱ |
| 1.5 | Billets en première classe : Nombre de passagers | S |  | ✱ |
| 1.6 | Billets en première classe : Montant de la taxe collectée | C | 1e+06% | ✱ |
| **§2** | **TOTAL A PAYER** | | | |
| 2.1 | Montant total de la contribution | C |  | ✱ |

### TEBA — Taxe d'Embarquement sur les Titres de Transport Aérien

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 7 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DELA BASE IMPOSABLE** | | | |
| 1.1 | Nombre de billets vendus : Vols domestiques | S |  | ✱ |
| 1.2 | Montant de la taxe collectée | C | 200000% | ✱ |
| 1.3 | Nombre de billets vendus : Vols à destination des pays de la CEDEAO | S |  | ✱ |
| 1.4 | Montant de la taxe collectée | C | 300000% | ✱ |
| 1.5 | Nombre de billets vendus : Autres vols | S |  | ✱ |
| 1.6 | Montant de la taxe collectée | C | 400000% | ✱ |
| 1.7 | Total à payer | C |  | ✱ |

### RRMP — Redevance de Régulation des Marchés Publics

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 7 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **IDENTIFICATION DU MARCHE OU DE LA CONVENTION** | | | |
| 1.1 | Nature | S |  |  |
| 1.2 | Objet | S |  |  |
| 1.3 | Date d’approbation (saisir au format JJ/MM/AAAA) | S |  |  |
| 1.4 | Numéro du marché ou de la convention | S |  |  |
| 1.5 | Montant total hors taxes | S |  | ✱ |
| **§2** | **DETERMINATION DE LA REDEVANCE** | | | |
| 2.1 | Montant total HT du marché ou de la convention | C |  | ✱ |
| 2.2 | Montant de la redevance | C | 0.5% | ✱ |

### TSPDF — Taxe Spéciale pour la Préservation et le Développement Forestier

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 7 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **ESSENCES FORESTIERES DE CATEGORIE 1** | | | |
| 1.1 | Cubage de bois total (par m3) | S |  |  |
| 1.2 | Montant à payer | C | 50000% |  |
| **§2** | **ESSENCES FORESTIERES DE CATEGORIE 2** | | | |
| 2.1 | Cubage de bois total (par m3) | S |  |  |
| 2.2 | Montant à payer | C | 30000% |  |
| **§3** | **ESSENCES FORESTIERES DE CATEGORIE 3** | | | |
| 3.1 | Cubage de bois total (par m3) | S |  |  |
| 3.2 | Montant à payer | C | 20000% |  |
| **§4** | **TOTAL** | | | |
| 4.1 | MONTANT TOTAL DE LA TAXE A PAYER | C |  |  |

## ▸ Droits de timbre & enregistrement


### DTIMBRE — Droits de timbre et quittances

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 70 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§4** | **MONTANT TOTAL DES DROITS** | | | |
| 4.1 | TOTAL A REVERSER | C |  | ✱ |
| 3.31 | Total droits proportionnel | C |  |  |
| 3.30 | Droit proportionnel 6 - Total | C |  |  |
| 3.28 | Droit proportionnel 6 - Taux | S |  |  |
| 3.27 | Droit proportionnel 6 - Montant (en FCFA) | S |  |  |
| 3.26 | Droit proportionnel 6 - Nature opération | S |  |  |
| 3.25 | Droit proportionnel 5 - Total | C |  |  |
| 3.23 | Droit proportionnel 5 - Taux | S |  |  |
| 3.22 | Droit proportionnel 5 - Montant (en FCFA) | S |  |  |
| 3.21 | Droit proportionnel 5 - Nature opération | S |  |  |
| 3.20 | Droit proportionnel 4 - Total | C |  |  |
| 3.18 | Droit proportionnel 4 - Taux | S |  |  |
| 3.17 | Droit proportionnel 4 - Montant (en FCFA) | S |  |  |
| 3.16 | Droit proportionnel 4 - Nature opération | S |  |  |
| 3.15 | Droit proportionnel 3 - Total | C |  |  |
| 3.13 | Droit proportionnel 3 - Taux | S |  |  |
| 3.12 | Droit proportionnel 3 - Montant (en FCFA) | S |  |  |
| 3.11 | Droit proportionnel 3 - Nature opération | S |  |  |
| 3.10 | Droit proportionnel 2 - Total | C |  |  |
| 3.8 | Droit proportionnel 2 - Taux | S |  |  |
| 3.7 | Droit proportionnel 2 - Montant (en FCFA) | S |  |  |
| 3.6 | Droit proportionnel 2 - Nature opération | S |  |  |
| 3.5 | Droit proportionnel 1 - Total | C |  |  |
| 3.3 | Droit proportionnel 1 - Taux (18 pour 18%) | S |  |  |
| 3.2 | Droit proportionnel 1 - Montant (en FCFA) | S |  |  |
| **§3** | **DROITS PROPORTIONNEL** | | | |
| 3.1 | Droit proportionnel 1 - Nature opération | S |  |  |
| 2.25 | Total droits fixes | C |  |  |
| 2.24 | Droit fixe 6 - Total | C |  |  |
| 2.23 | Droit fixe 6 - Nombre d’opérations | S |  |  |
| 2.22 | Droit fixe 6 - Droits dus (en FCFA) | S |  |  |
| 2.21 | Droit fixe 6 - Nature opération | S |  |  |
| 2.20 | Droit fixe 5 - Total | C |  |  |
| 2.19 | Droit fixe 5 - Nombre d’opérations | S |  |  |
| 2.18 | Droit fixe 5 - Droits dus (en FCFA) | S |  |  |
| 2.17 | Droit fixe 5 - Nature opération | S |  |  |
| 2.16 | Droit fixe 4 - Total | C |  |  |
| 2.15 | Droit fixe 4 - Nombre d’opérations | S |  |  |
| 2.14 | Droit fixe 4 - Droits dus (en FCFA) | S |  |  |
| 2.13 | Droit fixe 4 - Nature opération | S |  |  |
| 2.12 | Droit fixe 3 - Total | C |  |  |
| 2.11 | Droit fixe 3 - Nombre d’opérations | S |  |  |
| 2.10 | Droit fixe 3 - Droits dus (en FCFA) | S |  |  |
| 2.9 | Droit fixe 3 - Nature opération | S |  |  |
| 2.8 | Droit fixe 2 - Total | C |  |  |
| 2.7 | Droit fixe 2 - Nombre d’opérations | S |  |  |
| 2.6 | Droit fixe 2 - Droits dus (en FCFA) | S |  |  |
| 2.5 | Droit fixe 2 - Nature opération | S |  |  |
| 2.4 | Droit fixe 1 - Total | C |  |  |
| 2.3 | Droit fixe 1 - Nombre d’opérations | S |  |  |
| 2.2 | Droit fixe 1 - Droits dus (en FCFA) | S |  |  |
| **§2** | **DROITS FIXE** | | | |
| 2.1 | Droit fixe 1 - Nature opération | S |  |  |
| 1.13 | Total droits progressif | C |  |  |
| 1.12 | Total : Tranche (5 000 001 et plus) | C | 500000% |  |
| 1.11 | Nombre de versements/factures : Tranche (5 000 001 et plus) | S |  |  |
| 1.10 | Total : Tranche (1 000 001 - 5 000 000) | C | 200000% |  |
| 1.9 | Nombre de versements/factures : Tranche (1 000 001 - 5 000 000) | S |  |  |
| 1.8 | Total : Tranche (500 001 - 1 000 000) | C | 100000% |  |
| 1.7 | Nombre de versements/factures : Tranche (500 001 - 1 000 000) | S |  |  |
| 1.6 | Total : Tranche (100 001 - 500 000) | C | 50000% |  |
| 1.5 | Nombre de versements/factures : Tranche (100 001 - 500 000) | S |  |  |
| 1.4 | Total : Tranche (5 001 - 100 000) | C | 10000% |  |
| 1.3 | Nombre de versements/factures : Tranche (5 001 - 100 000) | S |  |  |
| 1.2 | Total : Tranche (0 - 5 000) | C |  |  |
| **§1** | **DROITS PROGRESSIF** | | | |
| 1.1 | Nombre de versements/factures : Tranche (0 - 5 000) | S |  |  |
| 3.29 | Droit proportionnel 6 - Nombre d’année | S |  |  |
| 3.24 | Droit proportionnel 5 - Nombre d’année | S |  |  |
| 3.19 | Droit proportionnel 4 - Nombre d’année | S |  |  |
| 3.14 | Droit proportionnel 3 - Nombre d’année | S |  |  |
| 3.9 | Droit proportionnel 2 - Nombre d’année | S |  |  |
| 3.4 | Droit proportionnel 1 - Nombre d’année | S |  |  |

### ENRCACAO — Taxe d'enregistrement sur les actes de confirmation de vente du cacao

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 16 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE DE LA PERIODE** | | | |
| 1.1 | Cacao - Quantité enregistrée (kg) | S |  | ✱ |
| 1.2 | Cacao - Valeur CAF enregistrée (Coût, Assurance, Fret) | C |  | ✱ |
| 1.4 | Cacao - Montant dû pour la période | C |  | ✱ |
| **§2** | **REGULARISATION EVENTUELLE DE LA TAXE DE LA PERIODE ANTERIEURE** | | | |
| 2.1 | Valeur totale déclarée en douane sur la période antérieure | S |  |  |
| 2.2 | Montant réellement dû sur la période antérieure | S |  |  |
| 2.3 | Montant à régulariser (2.2 - 2.1) | C |  |  |
| **§3** | **TOTAL A PAYER** | | | |
| 3.1 | Montant total à payer (1.4 + 2.3) | C |  | ✱ |
| 1.3 | Taux d’imposition à appliquer (droit commun 5% ; taux préférentiel 2,835%) | S |  | ✱ |
| 1.2 | Cacao - Prix CFA du Kg | S |  | ✱ |
| 1.2 | Cacao - Prix CFA du Kg | S |  | ✱ |
| 1.2 | Cacao - Valeur CAF enregistrée (Coût, Assurance, Fret) | C |  | ✱ |
| 1.3 | Taux d’imposition à appliquer (droit commun 5% ; taux préférentiel 2,835%) | S |  | ✱ |
| 1.4 | Cacao - Montant dû pour la période | C |  | ✱ |
| **§2** | **REGULARISATION EVENTUELLE DE LA TAXE DE LA PERIODE ANTERIEURE** | | | |
| 2.1 | Valeur totale déclarée en douane sur la période antérieure | S |  |  |
| 2.2 | Montant réellement dû sur la période antérieure | S |  |  |
| 2.3 | Montant à régulariser (2.2 - 2.1) | C |  |  |

### ENRPEXPORT — Taxe d'enregistrement sur les actes de confirmation de vente du café, de l'anacarde, du coton, du karité et de la cola

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 25 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **DETERMINATION DE LA TAXE DE LA PERIODE / CAFE** | | | |
| 1.1 | Café - Quantité enregistrée (kg) | S |  |  |
| 1.2 | Café - Prix CFA du Kg | S |  |  |
| 1.3 | Café - Valeur CAF enregistrée (Coût, Assurance, Fret) | C |  |  |
| 1.4 | Café - Montant dû pour la période | C | 5% |  |
| **§2** | **DETERMINATION DE LA TAXE DE LA PERIODE / ANACARDE** | | | |
| 2.1 | Anacarde - Quantité enregistrée (kg) | S |  |  |
| 2.2 | Anacarde - Prix CFA du Kg | S |  |  |
| 2.3 | Anacarde - Valeur CAF enregistrée (Coût, Assurance, Fret) | C |  |  |
| 2.4 | Anacarde - Montant dû pour la période | C | 2.5% |  |
| **§3** | **DETERMINATION DE LA TAXE DE LA PERIODE / COTON** | | | |
| 3.1 | Coton - Quantité enregistrée (kg) | S |  |  |
| 3.2 | Coton - Prix CFA du Kg | S |  |  |
| 3.3 | Coton - Valeur CAF enregistrée (Coût, Assurance, Fret) | C |  |  |
| 3.4 | Coton - Montant dû pour la période | C | 2.5% |  |
| **§4** | **DETERMINATION DE LA TAXE DE LA PERIODE / KARITE** | | | |
| 4.1 | Karité - Quantité enregistrée (kg) | S |  |  |
| 4.2 | Karité - Prix CFA du Kg | S |  |  |
| 4.3 | Karité - Valeur CAF enregistrée (Coût, Assurance, Fret) | C |  |  |
| 4.4 | Karité - Montant dû pour la période | C | 2.5% |  |
| **§5** | **DETERMINATION DE LA TAXE DE LA PERIODE / COLA** | | | |
| 5.1 | Cola - Quantité enregistrée (kg) | S |  |  |
| 5.2 | Cola - Prix CFA du Kg | S |  |  |
| 5.3 | Cola - Valeur CAF enregistrée (Coût, Assurance, Fret) | C |  |  |
| 5.4 | Cola - Montant dû pour la période | C | 2.5% |  |
| **§6** | **SYNTHESE POUR LA PERIODE** | | | |
| 6.1 | Total de la taxe sur la période | C |  |  |
| **§7** | **REGULARISATION EVENTUELLE DE LA TAXE DE LA PERIODE ANTERIEURE** | | | |
| 7.1 | Valeur totale déclarée en douane sur la période antérieure | S |  |  |
| 7.2 | Montant réellement dû sur la période antérieure | S |  |  |
| 7.3 | Montant à régulariser (7.2 -7.1) | C |  |  |
| **§8** | **TOTAL A PAYER** | | | |
| 8.1 | Montant total à payer (6.1 + 7.3) | C |  | ✱ |

## ▸ Vignette


### VIGNETTE — Taxe sur les véhicules à moteur (Vignette)

*Périodicité : Annuelle · Échéance : Campagne vignette · 7 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **VIGNETTES AUTO** | | | |
| 1.1 | Vignettes Auto (taxe sur véhicules à moteur) | S |  |  |
| 1.3 | Montant à payer - Vignettes Auto | C |  | ✱ |
| **§2** | **VIGNETTES BATEAU** | | | |
| 2.1 | Vignettes Bateau (taxe sur véhicules à moteur) | S |  |  |
| 2.2 | Montant à payer - Vignettes Bateau | C |  | ✱ |
| **§1** | **VIGNETTES AUTO** | | | |
| 1.2 | Vignettes proportionnelles auto | S |  |  |
| **§2** | **VIGNETTES BATEAU** | | | |
| 2.2 | Vignettes proportionnelles bateau | S |  |  |
| **§3** | **MONTANT TOTAL A PAYER** | | | |
| 3.1 | Montant total de la vignette à payer | C |  | ✱ |

## ▸ États récapitulatifs (annexes annuelles)


### BNCREGUL — Etat récapitulatif des rémunérations à des contribuables sans salariés dans l'entreprise (Etat 302)

*Périodicité : — · Échéance : À vérifier selon l'AF en vigueur · 3 champs*

| Indice | Champ | Type | Taux | Obl. |
|---|---|:--:|:--:|:--:|
| **§1** | **Détermination des honoraires rétrocédés à des confrères** | | | |
| 1.1 | Effectif | S |  | ✱ |
| 1.2 | Montant brut TTC - Total des rétributions | S |  | ✱ |
| 1.3 | Montant BNC état 302 à payer | S |  | ✱ |

---

## 2. Annexes détaillées EDI (import ligne par ligne — étape 3)


### ETAT301 — État 301 — État individuel des rémunérations brutes (salariés)

*Fichier : `edi-annexe-ETAT301.xlsm` · Rattaché à : Déclaration État 301 (ITSREGUL) — annuel, avant 30/06 (ou 17/02 régul.) · Codes : ITS (privé), ITSPUB (public), ITSPARA (parapublic)*

Colonnes :

1. #
2. N° CNPS
3. Nom et prénoms
4. Type de travailleur
5. Emploi ou Qualité
6. Code Emploi (DR/CS/AM/CM/EQ/EN/OQ/ON/A)
7. Régime (G Général / A Agricole)
8. Sexe (M/F)
9. Nationalité (I/AA/F/SL/A)
10. Local (L) / Expatrié (E)
11. Situation de famille (C/M/D/V)
12. Nombre d'enfants à charge
13. Nombre de parts
14. Nombre de jours d'application des paies
15. Montant des salaires et rémunérations
16. Montant avantages en nature (barème)
17. Montant avantages en nature (réel)
18. Rémunération totale brute (annuel)
19. Revenus non imposables (annuel)
20. Rémunération brute imposable (annuel)
21. Réduction d'impôt charges de famille
22. ITS Salariés (Brut/Net/Ajustement/Net à payer)
23. Indemnités frais d'emploi
24. Ventilation par tranches (6 tranches)
25. ITS brut total annuel

### ETAT302 — État 302 — Rémunérations versées à des NON-salariés (BNC)

*Fichier : `edi-annexe-ETAT302.xlsm` · Rattaché à : Déclaration État 302 (BNCREGUL) — annuel · Codes : BNCREGUL*

Colonnes :

1. N°
2. Noms
3. Prénoms
4. NCC
5. Activité ou Profession
6. Adresse géographique
7. BP
8. Montant brut TTC
9. Nature

### RETENUE — États nominatifs des retenues à la source / AIRSI / PPSSI / FIRCA / IRVM / RIRL

*Fichier : `edi-annexe-retenue.xlsm` · Rattaché à : Déclarations de retenues (étape 3, annexe EDI) · Codes : AIRSI, AIRSIREGUL, FIRCA, IRVM, PPSSI, PPSSIREGUL, RIBIC, RIBIC_RE, RIBNC, RIBNC_D, RIBNC_RE, RIBNC_RE_D, RIRL*

Colonnes :

1. NCC (du tiers)
2. Raison sociale
3. Activité
4. Adresse
5. Téléphone
6. Nature des biens et prestations
7. Références de la facture
8. Montant total de la facture
9. Montant de la retenue / AIRSI collectée
10. Date de l'opération (JJ/MM/AAAA)

### PATENTE_TRANSPORT — Patente transport — 1 ligne par véhicule

*Fichier : `edi-annexe-patente.xlsm` · Rattaché à : Patente transport (PATTRAN) · Codes : PATTRAN*

Colonnes :

1. #
2. Nature de l'activité de transport (liste)
3. Nombre de passagers
4. Charge utile totale du véhicule
5. Numéro d'immatriculation
6. Numéro de chassis
7. Numéro de carte grise
8. Marque (liste)
9. N° série
10. Puissance CV
11. Couleur
12. Date acquisition
13. Date de mise en service
14. Droit sur le Chiffre d'Affaires (calc)
15. Montant de l'impôt BIC (calc)
16. Montant total à payer (calc)

### PATCOM_REG — Régularisation patente commerce — par établissement

*Fichier : `edi-annexe-patcom_re.xlsm` · Rattaché à : Patente commerce REG (PATCOM_REG) · Codes : PATCOM_REG*

Colonnes :

1. N°
2. Commune ou Sous-préfecture
3. Adresse géographique
4. Références cadastrales
5. Titre foncier
6. Chiffre d'affaires
7. Droit sur le chiffre d'affaires (calc)
8. Loyer ou valeur locative
9. Droit sur la valeur locative (calc)
10. Montant total (calc)

### TVA_DEDUCTIONS — État des déductions de TVA (achats donnant droit à déduction)

*Fichier : `edi-annexe-TVA.xlsm` · Rattaché à : Déclaration TVA / TVA_S (annexe déductions, étape 3) · Codes : TVA, TVA_S*

Colonnes :

1. type_operation_odr
2. specification
3. date_facture
4. raison_sociale_fournisseur
5. ncc_fournisseur
6. pays_fournisseur
7. ref_facture
8. nature_bien_odr
9. date_reglement
10. montant_ht
11. montant_val_douane
12. montant_tva
13. type_redevable
14. prorata_deduction
15. montant_taxe_deductible

### TVA_EXPORT — Détail des exportations / opérations assimilées (ligne 1.2 TVA)

*Fichier : `edi-operations-assimilees_exportations-TVA.xlsm` · Rattaché à : Annexe TVA — ligne 1.2 · Codes : TVA, TVA_S*

Colonnes :

1. Détail des opérations d'exportation et assimilées (client, facture, montant, destination)

### TVA_EXO_CONV — Détail des exonérations conventionnelles (ligne 1.4 TVA)

*Fichier : `edi-exoneration-conventionnelle-TVA.xlsm` · Rattaché à : Annexe TVA — ligne 1.4 · Codes : TVA, TVA_S*

Colonnes :

1. Détail des opérations exonérées par convention (référence convention, client, montant)

### TVA_NON_TAX — Détail des autres opérations non taxables (ligne 1.5 TVA)

*Fichier : `edi-autres-operations-non-taxables-TVA.xlsm` · Rattaché à : Annexe TVA — ligne 1.5 · Codes : TVA, TVA_S*

Colonnes :

1. Détail des opérations non taxables (nature, client, montant)

### TVA_AUTRES_PROD — Détail des autres produits (hors champ TVA)

*Fichier : `edi-autres-produits-TVA.xlsm` · Rattaché à : Annexe TVA — autres produits · Codes : TVA, TVA_S*

Colonnes :

1. Détail des autres produits hors champ (nature, montant)


---

## 3. Référentiels (listes déroulantes normalisées)


**Code Emploi** : `DR`=Directeur · `CS`=Cadre supérieur · `AM`=Agent de maîtrise · `CM`=Cadre moyen · `EQ`=Employé qualifié · `EN`=Employé non qualifié · `OQ`=Ouvrier qualifié · `ON`=Ouvrier non qualifié · `A`=Autre

**Régime** : `G`=Général · `A`=Agricole

**Sexe** : `M`=Masculin · `F`=Féminin

**Nationalité** : `I`=Ivoirien · `AA`=Autre Africain · `F`=Français · `SL`=Syrien ou Libanais · `A`=Autre

**Local/Expatrié** : `L`=Local · `E`=Expatrié

**Situation famille** : `C`=Célibataire · `M`=Marié · `D`=Divorcé · `V`=Veuf

**Taux TVA** : `18%`=taux normal · `9%`=taux réduit · `21.31%`=taux majoré (spécifique)


---

## 4. Dossier de référence — RESEAU IVOIRIEN DE MAINTENANCE (NCC 2300433S)

Déclarations réellement souscrites (captures PDF), par nature et période :

| Nature déclarée | Code | Période observée |
|---|---|---|
| Avis de versement Impôt BIC (tiers/acompte) | AV/AVIB | TIERS 01 2024 |
| État récapitulatif rémunérations (État 301) | ETAT3/ITSREGUL | 2025 |
| Impôt sur le Revenu des Valeurs Mobilières | IRVM | Janvier 2026 |
| Impôts sur les traitements et salaires | ITS | Mai 2026 |
| Régularisation annuelle des ITS (secteur privé) | ITSREG | 2025 |
| État des salaires et rémunérations assimilées | ETATITSR | 2025 |
| Patente commerce (hors DGE) | PATCO | 2025 |
| Patente transport | PATTRAN | 2025 |
| Prélèvement à la source sur paiements | PPS/PPSSI | Janvier 2026 |
| Retenue à la source impôt BIC | RIBIC | 2025 / Janvier 2026 |
| Retenue à la source impôt BNC | RIBNC | 2025 / Février 2026 |
| Régularisation patente commerce (hors DGE) | PATCOM_REG | 2025 |
| Taxe Spéciale d'Équipement | TSE | Mai 2026 |
| Taxe sur la valeur ajoutée (hors CME/DGE) | TVA | Mai 2026 |


> **Note ITS (réforme 2024)** : le template porte des taux par défaut (ex. IS 1,5 %, CE expatrié 11,5 %, CN 1,5 %) ; le formulaire e-impôts en ligne affiche pour le personnel expatrié **CE 9,2 %** et **CN 1,2 %** (cf. capture ITS mai 2026). Le barème ITS est unifié/progressif depuis l'AF 2024 : **toujours revérifier les taux applicables à la période déclarée**.


---

## 5. Réflexes de contrôle avant injection du XML

- **NCC** au format exact `1234567A` (7 chiffres + 1 lettre), sans espace.
- **Période** = période fiscale réelle (attention au piège de millésime des déclarations annuelles, cf. mémoire §27).
- **Champs [C]** jamais forcés à la main : ils découlent des [S] et des taux.
- **TVA** : 1.1 CA total HT − (1.2 export + 1.3 exo légales + 1.4 exo conv. + 1.5 non taxables) = base ; TVA nette 6.1 = TVA brute 4.1 − déductions 5.3 ; crédit reporté 6.2.
- **ITS** : ne pas oublier les contributions employeur (CE local/expat, CN) et le FDFP (TA 0,4 % + TFPC 0,6 %).
- **Annexes obligatoires** : ITS→État 301 ; retenues→états nominatifs ; TVA→état des déductions + détails export/exo ; patente transport→liste véhicules.
- Chaque montant à la source doit être **rapproché de la comptabilité** (§16 rapprochement bancaire, §12 lecture balance).

