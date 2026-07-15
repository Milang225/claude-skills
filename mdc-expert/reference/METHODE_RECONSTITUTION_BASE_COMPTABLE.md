# MÉTHODE MDC — RECONSTITUTION DE LA BASE COMPTABLE À PARTIR DES ÉTATS FINANCIERS
> CŒUR DE MÉTIER MDC. Sens INVERSE de §13 (qui va balance→états). Ici : états financiers → base comptable → matrice anomalies → propositions.
> Sources : SYSCOHADA révisé 2017, AUDCIF, manuels Doumbia & Kadouamai, CGI CI. Cas type : FAMILLE KRA SARL.

## PROTOCOLE EN 7 ÉTAPES

### Étape 1 — Collecte & inventaire de ce qui est disponible
Liasse DGI : Page de garde, Fiches R1-R4, **Bilan** (actif/passif), **Compte de Résultat**, **TFT** (si SN), **Notes annexes 1-36**, SUPPL4 (immo). Noter ce qui MANQUE (un manque = première anomalie : ex. SUPPL4 vide).

### Étape 2 — Tests de bouclage AVANT toute reconstitution (bloquant)
- Bilan : **Total Actif = Total Passif** ?
- CR : **Résultat CR = Résultat du Bilan** (même signe, même montant) ?
- Notes : Σ détail des notes = totaux bilan/CR ?
- Si écart → ne pas reconstituer une base saine sur des états faux → c'est déjà une anomalie (codes P/A/R).

### Étape 3 — Reconstituer la BALANCE par DÉ-MAPPING (états → comptes)
Chaque poste de bilan/CR se décompose en comptes SYSCOHADA. On a 2 soldes par poste (N et N-1) → on obtient **Solde d'ouverture (N-1)** et **Solde de clôture (N)** par compte.

**MAPPING INVERSE — BILAN → comptes**
| Poste bilan (réf SN) | Comptes à reconstituer |
|---|---|
| AD/AF Immo incorporelles | 21x (brut) / 281x (amort) |
| AI-AN Immo corporelles | 22x,23x,24x / 283-284 |
| AQ Immo financières | 26,27 / 296,297 |
| BB Stocks | 31-38 / 39 |
| BG-BI Créances clients | 411,416 / 491 |
| BJ Autres créances | 42x(D),44x(D),46x(D),476 |
| BS Trésorerie actif | 50,52,521,53,57,581 / 59 |
| CA Capital | 101 (PM) / 104 (PP/EI) |
| CE-CF Réserves/RAN | 111,112,118,121,129 |
| CG Résultat | 13 (PM) / 103 (PP) |
| CH Subventions invest. | 14 |
| CJ Provisions réglementées | 15 |
| DA Dettes financières | 16,17 |
| DC Provisions R&C | 19 |
| DJ Fournisseurs | 401,408 / 409(D) |
| DK Dettes fiscales & sociales | 42(C),43,44(C) |
| DM Autres dettes | 419,46x(C),47x(C),477 |
| DR Trésorerie passif | 561,564,565 |

**MAPPING INVERSE — CR → comptes**
| Poste CR | Comptes |
|---|---|
| TA/RA Ventes/Achats m'ses | 701 / 601 + 6031 |
| TB-TD CA production/services | 702-708 |
| RC-RF Achats MP & autres | 602,604,605,608 + 6032/6033 |
| RG-RJ Services ext./impôts/autres | 61,62,63,64,65 |
| RK Charges de personnel | 66 |
| RL Dotations | 681,691,659 |
| RM/TK Charges/produits financiers | 67 / 77 |
| RS Impôts sur résultat | 891 |

### Étape 4 — Reconstituer les MOUVEMENTS & écritures (le récit derrière chaque variation)
Pour chaque compte : **Mouvement net = Solde N − Solde N-1**. On reconstitue l'écriture qui l'explique, à l'aide :
- des **Notes de mouvements** (Note 3A immo brutes A/B/C/D, 3C amort, 28 provisions, 14 réserves) → donnent acquisitions, cessions, dotations ;
- du **TFT** → flux trésorerie (investissement, financement) ;
- des **écritures-types** SYSCOHADA (cf. FICHE_COMPTA_SYSCOHADA §patterns).
Règle d'or §12.9 : « toute ligne raconte au moins une opération ; s'il y a un D ou un C, il y a eu un événement, donc une pièce, donc une contrepartie. »

### Étape 5 — Lancer la MATRICE D'ANOMALIES (cf. §12.5 : 16 tests + codes)
Codes : **P-** passif, **A-** actif, **R-** résultat, **T-** trésorerie, **N-** notes, **F-** fiscal, **S-** social. Tests-clés en reconstitution :
- Confusion **Résultat ↔ Capitaux propres** (résultat logé hors compte 13/103) → P-1/P-2.
- **Stocks** : variation bilan ≠ variation CR (6031) ; inventaire absent → A-1/R-2/N-1.
- **Trésorerie** non réconciliée (caisse/banque ≠ ouverture+flux) → T-1/T-2/T-3 (triangles MDLC).
- **Immo/amortissements absents** alors que SUPPL4 référence des actifs → A-2/R-3/N-3.
- **Social** : NCC/CNPS (ZG=0) avec salarié déclaré → S-x.
- **Fiscal** : régime déclaré incohérent (cf. NOTE_CODES_REGIMES_DGI : code 3 = ex-synthétique obsolète).

### Étape 6 — PROPOSITIONS : écritures de régularisation + plan
Format REG-xx (cf. §14.5) : base légale, D/C, impact résultat, impact bilan. Catalogue : reclassement résultat (13), variation stocks (31/6031), dotations rattrapage (681/28), CNPS (664/431), correction capital, apurement suspens (47x).

### Étape 7 — AUDIT CONTRADICTOIRE + VERDICT + LIVRABLES
Déployer l'auditeur indépendant (§14.3) qui challenge. Verdict noté AAA→D (§4). Livrables : LIASSE reconstituée + matrice anomalies + REG + plan d'action J+7→J+60 + visa ou refus.

## RÈGLE D'OR
Une reconstitution n'est valable QUE si la base reconstituée **boucle** (ΣD=ΣC, Actif=Passif, Résultat CR=Bilan). Si la liasse source ne boucle pas, la première livraison est la **liste des anomalies de bouclage**, pas une base « propre » fabriquée par-dessus.
