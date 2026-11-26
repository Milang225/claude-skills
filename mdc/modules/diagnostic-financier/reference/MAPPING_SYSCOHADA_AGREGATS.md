# Correspondance balance SYSCOHADA → agrégats financiers

Fiche de référence du skill `diagnostic-financier`. Les clés ci-dessous sont celles attendues
par le paramètre `--json` de `build_classeur_diagnostic.py` et par le moteur de calcul.
Elles sont définies une seule fois, dans `scripts/moteur_diagnostic.py` (constante `POSTES`) :
cette fiche en est le reflet, ne pas les redéfinir ailleurs.

## 1. Les 48 postes de saisie

### Compte de résultat

| Clé | Libellé | Comptes SYSCOHADA |
|---|---|---|
| `v_march` | Ventes de marchandises | 701 |
| `a_march` | Achats de marchandises | 601 |
| `var_march` | Variation de stocks de marchandises | 6031  (+) si baisse du stock |
| `v_prod` | Ventes de produits, travaux et services | 702 à 706 |
| `prod_imm` | Production immobilisée et variation stocks produits | 72 / 73 |
| `a_mat` | Achats de matières, fournitures et énergie | 602 / 604 / 605 / 608 |
| `transp` | Transports | 61 |
| `serv` | Services extérieurs | 62 / 63 |
| `subv` | Subventions d'exploitation | 71 |
| `imp_tax` | Impôts et taxes | 64 |
| `autres_ch` | Autres charges | 65 |
| `pers` | Charges de personnel | 66 |
| `autres_pr` | Autres produits | 75 |
| `dot` | Dotations aux amortissements et provisions d'exploitation | 68 |
| `repr` | Reprises de provisions et transferts de charges | 78 / 79 |
| `rev_fin` | Revenus financiers | 77 |
| `fr_fin` | Frais financiers | 67 |
| `hao` | Résultat HAO net | 82 à 84 |
| `partic` | Participation des travailleurs | 87 |
| `impot` | Impôts sur le résultat (IS ou IMF) | 89 |

### Bilan — actif

| Clé | Libellé | Comptes SYSCOHADA |
|---|---|---|
| `im_inc` | Immobilisations incorporelles brutes | 21 |
| `im_cor` | Immobilisations corporelles brutes | 22 à 24 |
| `im_fin` | Immobilisations financières | 26 / 27 |
| `amort` | Amortissements et dépréciations des immobilisations | 28 / 29 |
| `stock_b` | Stocks bruts | 31 à 38 |
| `stock_d` | Dépréciations des stocks | 39 |
| `cli_b` | Créances clients brutes | 411 / 412 / 416 / 418 |
| `cli_d` | Dépréciations des créances clients | 491 |
| `aut_cr` | Autres créances d'exploitation (État, personnel, divers) | 44 déb. / 42 déb. / 47 déb. |
| `cr_hao` | Créances HAO | 485 / 488 |
| `titres` | Titres de placement | 50 |
| `banque` | Banques, chèques postaux, caisse | 52 / 53 / 57 |

### Bilan — passif

| Clé | Libellé | Comptes SYSCOHADA |
|---|---|---|
| `capital` | Capital social | 101 / 103 |
| `reserv` | Primes, écarts et réserves | 104 à 11 |
| `ran` | Report à nouveau (+/-) | 12 |
| `res_bil` | Résultat net de l'exercice (au bilan) | 13 |
| `subv_inv` | Subventions d'investissement | 14 |
| `prov_regl` | Provisions réglementées | 15 |
| `emprunt` | Emprunts et dettes financières | 16 |
| `cbail` | Dettes de location-acquisition (crédit-bail) | 17 |
| `prov_risq` | Provisions pour risques et charges | 19 |
| `cca` | Comptes courants d'associés | 462 |
| `fourn` | Fournisseurs d'exploitation | 401 / 408 |
| `d_fisc` | Dettes fiscales | 44 |
| `d_soc` | Dettes sociales | 42 / 43 |
| `aut_det` | Autres dettes d'exploitation | 47 créd. |
| `det_hao` | Dettes HAO | 481 / 482 |
| `decouv` | Banques, crédits de trésorerie et découverts | 56 |

## 2. Règles de signe

| Poste | Règle |
|---|---|
| `var_march` (6031) | **Positif si le stock diminue**, négatif s'il augmente. Coût d'achat des marchandises vendues = `601 + 6031`. |
| `amort` (28/29) | Saisi en **valeur positive** ; les formules le soustraient de l'actif brut. |
| `stock_d` (39), `cli_d` (491) | Idem : dépréciations en **positif**. |
| `ran` (12) | Report à nouveau **signé** : négatif si débiteur (pertes antérieures). |
| `res_bil` (13) | Résultat **signé**. Doit égaler le résultat recalculé (contrôle bloquant). |
| `hao` (82 à 84) | Résultat HAO **net et signé**. |

## 3. Les agrégats

### 3.1 Soldes intermédiaires de gestion

| Agrégat | Formule |
|---|---|
| Chiffre d'affaires | `701 + (702 à 706)` |
| Coût d'achat des marchandises vendues | `601 + 6031` |
| Marge commerciale | Ventes de marchandises − CAMV |
| Production de l'exercice | `(702 à 706) + 72 + 73` |
| Consommations intermédiaires | `(602 à 608) + 61 + 62 + 63` |
| **Valeur ajoutée** | Marge commerciale + Production − Consommations intermédiaires |
| **EBE** | VA + `71` − `64` − `66` − `65` |
| Résultat d'exploitation | EBE + `75` + `78/79` − `68` |
| Résultat financier | `77` − `67` |
| Résultat des activités ordinaires | Résultat d'exploitation + Résultat financier |
| **Résultat net** | RAO + Résultat HAO − `87` − `89` |
| CAF (approchée) | Résultat net + `68` − `78/79` |

> La CAF est **approchée** : elle ne neutralise pas les plus ou moins-values de cession, qui
> transitent par le HAO. Sur un dossier comportant des cessions significatives, la retraiter à la
> main et le signaler dans le rapport.

### 3.2 Bilan financier

| Agrégat | Formule |
|---|---|
| Immobilisations nettes | `21 + (22 à 24) + 26/27 − 28/29` |
| **BFR d'exploitation** | (Stocks nets + Clients nets + Autres créances d'exploitation) − (`401/408` + `44` + `42/43` + `47` créditeur) |
| BFR hors activités ordinaires | Créances HAO − Dettes HAO |
| **Actif économique** | Immobilisations nettes + BFR total |
| **Capitaux propres** | `101/103 + 104 à 11 + 12 + 13 + 14 + 15` |
| Trésorerie actif | `50 + 52 + 53 + 57` |
| Endettement financier brut | `16 + 17 + 462 + 56` |
| **Endettement net** | Endettement brut − Trésorerie actif |
| Trésorerie nette | Trésorerie actif − `56` |

**Bouclage (contrôle bloquant) :** Actif économique = Capitaux propres + Endettement net + Provisions pour risques (`19`).

### 3.3 Choix de méthode assumés

| Point | Choix MDC | Motif |
|---|---|---|
| Comptes courants d'associés (`462`) | Classés en **endettement**, pas en fonds propres | Tant qu'ils ne sont pas bloqués par convention, ils sont exigibles. Si une convention de blocage existe, la mentionner et retraiter. |
| Crédit-bail (`17`) | Inclus dans l'endettement | SYSCOHADA révisé retraite déjà la location-acquisition au bilan. |
| Découverts (`56`) | Dans l'endettement brut **et** suivis à part | Un endettement massivement à court terme est un risque de liquidité distinct. |
| Provisions pour risques (`19`) | **Hors** capitaux propres et hors dette | Elles apparaissent dans le bouclage de l'actif économique. |
| Base de jours | **360** par défaut | Usage de place ; Vernimmen retient 365. Paramétrable. |
| Charges fixes / variables | Convention : variables = achats + transports ; fixes = services extérieurs + personnel + impôts et taxes + autres charges + dotations + frais financiers − autres produits | Donne un **point mort financier**. À ajuster pour un client industriel. |

## 4. Ratios calculés

| Étape | Ratios |
|---|---|
| 1 — Marges | croissance du CA, taux de marge commerciale, taux de VA, taux d'EBE, taux de résultat d'exploitation, poids du personnel, effet de ciseau, point mort, marge de sécurité |
| 2 — BFR | BFR en jours de CA, délai clients, délai stocks, délai fournisseurs, dettes fiscales et sociales en jours, investissements |
| 3 — Financement | gearing, endettement net / EBE, couverture des frais financiers, CAF / endettement net, autonomie financière, capitaux propres / capital social, part du court terme, trésorerie nette en jours |
| 4 — Rentabilité | rentabilité économique après impôt, coût apparent de la dette, effet de levier, ROE théorique, ROE constaté, écart |
| 5 — Valeur | CMPC, spread, VEA, score Z'' |

**Délai fournisseurs** : dénominateur = `601 + (602 à 608) + 62/63`, hors TVA. Si le poste
fournisseurs est TTC dans la balance, le ratio est surestimé d'environ 18 % — le signaler.
