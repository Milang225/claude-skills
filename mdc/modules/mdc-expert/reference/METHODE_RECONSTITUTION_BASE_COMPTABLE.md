# MÉTHODE MDC — RECONSTITUTION DE LA BASE COMPTABLE À PARTIR DES ÉTATS FINANCIERS
> CŒUR DE MÉTIER MDC. Sens INVERSE de §13 (qui va balance→états). Ici : états financiers → base comptable → matrice anomalies → propositions.
> Sources : SYSCOHADA révisé 2017, AUDCIF, manuels Doumbia & Kadouamai, CGI CI. Cas type : FAMILLE KRA SARL.

## PROTOCOLE EN 7 ÉTAPES

### Étape 1 — Collecte & inventaire de ce qui est disponible
Liasse DGI : Page de garde, Fiches R1-R4, **Bilan** (actif/passif), **Compte de Résultat**, **TFT** (si SN), **Notes annexes 1-36**, SUPPL4 (immo). Noter ce qui MANQUE (un manque = première anomalie : ex. SUPPL4 vide).

### Étape 2 — Tests de bouclage AVANT toute reconstitution (bloquant)
- Bilan : **Total Actif = Total Passif** (BZ = DZ) ?
- CR : **Résultat CR = Résultat du Bilan** (XI = CJ = solde du compte 13, même signe, même montant) ?
- TFT (SN) : **ZH = BT − DT de N** et **ZA = BT − DT de N-1** (AUDCIF p. 997) ?
- Notes : Σ détail des notes = totaux bilan/CR ?
- Si écart → ne pas reconstituer une base saine sur des états faux → c'est déjà une anomalie (codes P/A/R).

### Étape 3 — Reconstituer la BALANCE par DÉ-MAPPING (états → comptes)
Chaque poste de bilan/CR se décompose en comptes SYSCOHADA. On a 2 soldes par poste (N et N-1) → on obtient **Solde d'ouverture (N-1)** et **Solde de clôture (N)** par compte.

**Référence unique des postes : `reference/TABLE_CORRESPONDANCE_POSTES_SYSCOHADA.md`** (table officielle AUDCIF p. 1049 pour le bilan, p. 1050 pour le compte de résultat). Les deux tableaux ci-dessous en sont la lecture inverse ; en cas d'écart, la table de référence l'emporte. Ne jamais renuméroter une lettre : la table saute des lettres (pas de CC, CI, CK, DE, DG…).

**MAPPING INVERSE — BILAN → comptes** (brut / amortissements et dépréciations)
| Poste bilan (réf SN) | Comptes à reconstituer |
|---|---|
| AD Immobilisations incorporelles (titre = AE + AF + AG + AH) | AE : 211, 2181, 2191 / 2811, 2818 p, 2911, 2918 p, 2919 p · AF : 212, 213, 214, 2193 / 2812, 2813, 2814, 2912, 2913, 2914, 2919 p · AG : 215, 216 / 2815, 2816, 2915, 2916 · AH : 217, 218 (sauf 2181), 2198 / 2817, 2818 p, 2917, 2918 p, 2919 p |
| AI Immobilisations corporelles (titre = AJ à AN) | AJ : 22 / 282, 292 · AK : 231, 232, 233, 237, 2391 / 2831, 2832, 2833, 2837, 2931, 2932, 2933, 2937, 2939 p · AL : 234, 235, 238, 2392, 2393 / 2834, 2835, 2838, 2934, 2935, 2938, 2939 p · AM : 24 (sauf 245 et 2495) / 284 (sauf 2845), 294 (sauf 2945, 2949), 2949 p · AN : 245, 2495 / 2845, 2945, 2949 p |
| AP Avances et acomptes versés sur immobilisations | 251, 252 / 2951, 2952 |
| AQ Immobilisations financières (titre = AR + AS) | AR : 26 / 296 · AS : 27 / 297 |
| BA Actif circulant HAO | 485, 488 / 498 |
| BB Stocks et encours | 31 à 38 / 39 |
| BG Créances et emplois assimilés (titre = BH + BI + BJ) | pas de compte propre |
| BH Fournisseurs avances versées | 409 / 490 |
| BI Clients | 41 (sauf 419) / 491 |
| BJ Autres créances | soldes débiteurs 185, 42, 43, 44, 45, 46, 47 (sauf 478) / 492 à 497 — 476 inclus, 478 va en BU ; 47111 et 47112 débiteurs inclus |
| BQ Titres de placement | 50 / 590 |
| BR Valeurs à encaisser | 51 / 591 |
| BS Banques, chèques postaux, caisse et assimilés (trésorerie-actif) | soldes débiteurs 52, 53, 54, 55, 57, 581, 582 / 592, 593, 594 — **55 = monnaie électronique (552 Mobile Money)** ; 585 et 588 doivent être soldés (AUDCIF p. 434 et p. 1049) |
| BU Écart de conversion-Actif | 478 |
| CA Capital | 101 à 104 (101 capital social en PM ; 104 compte de l'exploitant en PP/EI) |
| CB Apporteurs capital non appelé (−) | 109 |
| CD Primes liées au capital social | 105 |
| CE Écarts de réévaluation | 106 |
| CF Réserves indisponibles | 111, 112, 113 |
| CG Réserves libres | 118 |
| CH Report à nouveau (+ ou −) | 12 (121 créditeur ou 129 débiteur) |
| CJ Résultat net de l'exercice | 13 (131 bénéfice ou 139 perte) (AUDCIF p. 1049) — les comptes 103 et 104 (PP/EI) relèvent de CA, pas de CJ |
| CL Subventions d'investissement | 14 |
| CM Provisions réglementées | 15 |
| DA Emprunts et dettes financières diverses | 16, 181, 182, 183, 184 (AUDCIF p. 1049) |
| DB Dettes de location acquisition | 17 (AUDCIF p. 1049) |
| DC Provisions pour risques et charges | 19 |
| DH Dettes circulantes HAO | 481, 482, 484, 4998 (AUDCIF p. 1049) |
| DI Clients, avances reçues | 419 (AUDCIF p. 1049) |
| DJ Fournisseurs d'exploitation | 40 (sauf 409) : 401, 402, 404, 408 — le 409 va à l'actif en BH, jamais en DJ |
| DK Dettes fiscales et sociales | soldes créditeurs 42, 43, 44 |
| DM Autres dettes | soldes créditeurs 185, 45, 46, 47 (sauf 479) (AUDCIF p. 1049) — 419 va en DI ; 47121 et 47122 créditeurs inclus |
| DN Provisions pour risques à court terme | 499 (sauf 4998), 599 (AUDCIF p. 1049) — 4998 va en DH |
| DQ Banques, crédits d'escompte | 564, 565 (AUDCIF p. 1049) |
| DR Banques, établissements financiers et crédits de trésorerie | soldes créditeurs 52, 53, 561, 566 (AUDCIF p. 1049) — un compte bancaire créditeur à la clôture va en DR, sans compensation avec les comptes débiteurs (p. 419) |
| DV Écart de conversion-Passif | 479 |

**MAPPING INVERSE — CR → comptes** (AUDCIF p. 1050 ; comptes pris en entier, sans exclusion)
| Poste CR | Comptes |
|---|---|
| TA / RA / RB Ventes, achats et variation de stocks de marchandises | 701 / 601 / 6031 |
| TB Ventes de produits fabriqués | 702, 703, 704 |
| TC Travaux, services vendus | 705, 706 |
| TD Produits accessoires | 707 (pas de 708 dans le plan révisé) |
| TE Production stockée | 73 |
| TF Production immobilisée | 72 |
| TG Subventions d'exploitation | 71 |
| TH Autres produits | 75 (dont 754 et 759) |
| TI Transferts de charges d'exploitation | 781 |
| RC / RD Achats et variation de stocks de matières premières | 602 / 6032 |
| RE / RF Autres achats et variation de stocks d'autres approvisionnements | 604, 605, 608 / 6033 |
| RG Transports | 61 |
| RH Services extérieurs | 62, 63 (dont 631 frais bancaires) |
| RI Impôts et taxes | 64 (dont 647 pénalités) |
| RJ Autres charges | 65 (dont 654 et 659) |
| RK Charges de personnel | 66 |
| TJ Reprises d'amortissements, de provisions et dépréciations | 791, 798, 799 |
| RL Dotations aux amortissements, aux provisions et dépréciations | 681, 691 (659 est en RJ) |
| TK / TL / TM Revenus financiers, reprises financières, transferts de charges financières | 77 / 797 / 787 |
| RM / RN Frais financiers, dotations financières | 67 / 697 |
| TN / RO Produits et valeurs comptables des cessions d'immobilisations | 82 / 81 |
| TO Autres produits HAO | 84, 86, 88 |
| RP Autres charges HAO | 83, 85 |
| RQ Participation des travailleurs | 87 |
| RS Impôts sur le résultat | 89 (891, 892, 895, 899) |

### Étape 4 — Reconstituer les MOUVEMENTS & écritures (le récit derrière chaque variation)
Pour chaque compte : **Mouvement net = Solde N − Solde N-1**. On reconstitue l'écriture qui l'explique, à l'aide :
- des **Notes de mouvements** (Note 3A immo brutes A/B/C/D, 3C amort, 28 provisions, 14 réserves) → donnent acquisitions, cessions, dotations ;
- du **TFT** → flux trésorerie (investissement, financement) ;
- des **écritures-types** SYSCOHADA (cf. FICHE_COMPTA_SYSCOHADA §patterns).
Règle d'or §12.9 : « toute ligne raconte au moins une opération ; s'il y a un D ou un C, il y a eu un événement, donc une pièce, donc une contrepartie. »

### Étape 5 — Lancer la MATRICE D'ANOMALIES (cf. §12.5 : 16 tests + codes)
Codes : **P-** passif, **A-** actif, **R-** résultat, **T-** trésorerie, **N-** notes, **F-** fiscal, **S-** social. Tests-clés en reconstitution :
- Confusion **Résultat ↔ Capitaux propres** (résultat logé hors du compte 13, poste CJ) → P-1/P-2.
- **Stocks** : variation de BB au bilan ≠ variation au CR (6031 en RB, 6032 en RD, 6033 en RF, 73 en TE) ; inventaire absent → A-1/R-2/N-1.
- **Trésorerie** non réconciliée (caisse/banque ≠ ouverture+flux) → T-1/T-2/T-3 (triangles MDLC).
- **Immo/amortissements absents** alors que SUPPL4 référence des actifs → A-2/R-3/N-3.
- **Social** : NCC/CNPS (ZG=0) avec salarié déclaré → S-x.
- **Fiscal** : régime déclaré incohérent (cf. NOTE_CODES_REGIMES_DGI : code 3 = ex-synthétique obsolète).

### Étape 6 — PROPOSITIONS : écritures de régularisation + plan
Format REG-xx (cf. §14.5) : base légale, D/C, impact résultat, impact bilan. Catalogue : reclassement résultat (13), variation stocks (31/6031), dotations rattrapage (681/28), CNPS (664/431), correction capital, apurement des sous-comptes de 471 (47111 décaissements à justifier, 47121 encaissements à justifier, 47112 et 47122 écarts de rapprochement ; jamais 476 à 479, dont le solde de clôture est normal).

### Étape 7 — AUDIT CONTRADICTOIRE + VERDICT + LIVRABLES
Déployer l'auditeur indépendant (§14.3) qui challenge. Verdict noté AAA→D (§4). Livrables : LIASSE reconstituée + matrice anomalies + REG + plan d'action J+7→J+60 + visa ou refus.

## RÈGLE D'OR
Une reconstitution n'est valable QUE si la base reconstituée **boucle** (ΣD=ΣC, BZ = DZ, XI = CJ). Si la liasse source ne boucle pas, la première livraison est la **liste des anomalies de bouclage**, pas une base « propre » fabriquée par-dessus.
