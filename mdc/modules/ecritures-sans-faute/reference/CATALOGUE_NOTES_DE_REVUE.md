# Catalogue des observations des réviseurs → règles MDC

Sources (copies locales) :
- FAMILLE KRA SARL, note de revue du 11/11/2026 — `~/Documents/DOCUMENTS_RECUS_PAR_MAIL/2026-11-11 — Nadège Lou BAH — Note de revue famille KRA/`
- KWAANI SERVICES, note de revue du 11/11/2026 — `.../2026-11-11 — Nadège Lou BAH — Note de revue de KWAANI/`
- KG CONSULTING (EI KOUAME Georges), programme de travail visa du 11/11/2026 — `.../2026-11-11 — Nadège Lou BAH — Note de revue KG consulting/`
- TIM 7 MULTISERVICES SARL, note de revue du 13/10/2026 — `~/Downloads/Note_de_revue_Visa_TIM7_2025_CLV13102026.docx`
- Auto-contrôle MDC : ordre de saisie TRACE LOGISTICS du 21/06/2026 (contrôle du 11/11/2026 : 12 erreurs bloquantes).

À compléter à chaque nouvelle note de revue : une ligne par observation, la règle (§1 du module), et si possible une règle du script.

## A. Numéros de comptes

| Dossier | Observation | Règle | Script |
|---|---|---|---|
| KRA 3.6 | Salaires en 401 au lieu de 661/422 | §2 | oui |
| KRA 3.6, KWAANI 3.2 | Taxes sur salaires non ventilées CN 6413 / TA 6414 / FPC 6415 | §2 | oui |
| KG Q1 | TA en 6413 au lieu de 6414 | §2 | oui |
| KG Q1 | Compte 89 en à-nouveau (résultat N-1) | R7 | oui |
| KG Q1 | Compte 89000000 chez une entreprise au forfait (TEE) : la classe 89 est réservée au régime du réel (précision du gérant, 11/11/2026) | R13 | oui (`--regime TEE`) |
| KG Q1 | 4478 à-nouveau de 750 non justifié | R10 | alerte balance |
| KG Q1 | Intitulés faux du plan Sage (641 « rémunérations », 411 « dégrèvement ») | §2 note | non |
| KG État | Patente transitant par 446 | §2 | oui |
| KWAANI 3.1 | Loyer en 422 au lieu de 401 | §2 | oui |
| KWAANI 3.5 | Pénalités fiscales en 4486 au lieu de dettes fiscales | §2 | oui |
| TIM 7 n° 4 | Services vendus en 702 au lieu de 706 | §2 | oui (701-704) |
| TIM 7 n° 4 | Provision litiges en 196 (retraite) au lieu de 191 | §2 | oui |
| TIM 7 n° 6 | 462100 « Le principal » utilisé comme compte d'attente | R10 | partiel |
| TRACE (MDC) | 6313 pour la contribution employeur (= location de coffres) | §2 | oui |
| TRACE (MDC) | 4616 pour la souscription (= versements anticipés) | §2, 3.1 | oui |
| TRACE (MDC) | 4611 pour le compte courant d'associé (= apports en nature) | §2 | oui |
| TRACE (MDC) | 629000 frais bancaires (compte inexistant) | §2 | oui |
| TRACE (MDC) | 624100/624200 électricité et eau (624 = entretien) | §2 | oui |
| TRACE (MDC) | 626000 télécoms (626 = études) ; 604000 fournitures non stockées | §2 | oui |
| TRACE (MDC) | 701 pour des prestations de services | §2 | oui |

## B. Tenue et rattachement

| Dossier | Observation | Règle | Script |
|---|---|---|---|
| KG, TIM 7 n° 3/10/14 | Écritures globales au 31/12 sans pièces | R1 | oui |
| TRACE (MDC) | Toutes les écritures 2025 datées du 31/12 | R1 | oui |
| KG, TIM 7 n° 13 | Tiers anonymes (« CLT », FNP sans fournisseur) | R2 | oui |
| TIM 7 n° 13 | FNP soldées dans l'exercice | §3.6 | oui |
| KG | Opérations 2024 saisies dans le journal d'à-nouveaux 2025 | R7 | oui (date AN) |
| KRA 3.8, TIM 7 n° 5, KWAANI §5 | À-nouveaux ≠ EF N-1 visés | R7, G1 | non (grille) |
| KRA 2.5 | AMR 2025 payé en 2026 non comptabilisé en 2025 | R6 | non (grille G4/G5) |
| KG | Impôt foncier 2024 passé en charge 2025 | R6 | non (grille G5) |
| TIM 7 n° 24 | Opérations de carte de 2026 en 2025 | R6 | oui (dates) |
| TIM 7 n° 27 | Caisse créditrice chaque fin de mois | R8 | oui |
| KRA 3.10 | Un seul compte pour plusieurs banques | R9 | non |
| TIM 7 n° 28-29 | 462/471 servant à équilibrer ; soldes inexpliqués | R10 | oui (471, 585) |
| TIM 7 n° 25 | Retraits du gérant présentés en règlements fournisseurs | §3.5 | non |
| KRA 2.1 | Trésorerie virée en stock sans facture ni inventaire | R11 | non |
| KRA 2.2 | CA réduit aux commissions sans contrat de mandat | R11 | non |
| KRA 2.3 | Emprunt au nominal au lieu du capital restant dû | §2, G10 | non |
| KRA 3.1 | AIRSI immobilisée ; amortissement avant mise en service | §2 | non |

## C. Concordance avec les déclarations

| Dossier | Observation | Règle |
|---|---|---|
| KRA 3.4 | TEE comptabilisée ≠ TEE émise | R5, G5 |
| KRA 3.7, KWAANI 3.3 | ITS/FDFP comptabilisés ≠ déclarés ; paiements manquants | R5, G4, G6 |
| KG tableaux 1-2 | Paiements à l'État surévalués ; dette foncier 2025 omise | R5, G4, G5 |
| TIM 7 n° 17 | Salaires : comptabilité ≠ ITS ≠ État 301 | R5, G7 |
| TIM 7 n° 18 | Charges sociales très inférieures aux cotisations théoriques | G8 |
| TIM 7 n° 19 | Impôts sur salaires déclarés > charge comptabilisée | R5, G6 |
| TIM 7 n° 20 | TVA collectée impayée ; exonération non justifiée | G4 |

## D. Préalables et liasse (motifs de rejet)

| Dossier | Observation |
|---|---|
| KRA 1.1, KWAANI 1.1, KG Q3, TIM 7 n° 1 | **Aucun n° CNPS alors qu'il y a des salariés : rejet du visa** |
| KWAANI 1.2, KG | RCCM, DFE, statuts non transmis |
| KWAANI 2.4, TIM 7 n° 7 | Résultat N-1 affecté sans PV d'AGO |
| TIM 7 n° 2 | SMT alors que le CA dépasse le seuil (30 M prestataires) : liasse au système normal |
| KG | EI présentée comme SARL (forme 09, « gérant », « approuvés par l'AG ») |
| KG | Résultat de la liasse « corrigé » par une fausse variation de dettes (ligne VC) |
| KG, KWAANI | Fiche R1 incomplète (IDU, CNPS, date de signature) ; Note 2 générique ; colonne N-1 vide |
| KWAANI 2.2 | Capitaux propres < moitié du capital : décision des associés à documenter |

## E. FAMILLE KRA — écritures produites le 02/11/2026 (`ECRITURES_MENSUELLES` et `ECRITURES_SAGE`)

Contrôle du 11/11/2026 : version mensuelle 167 erreurs bloquantes, version Sage 76.

| Observation | Version | Règle | Script |
|---|---|---|---|
| Salaires en 661 réglés en caisse dans la même pièce, sans 422 ni retenue | mensuelle | 3.2, R4 | oui |
| « 6414/5 » : TA et FPC fusionnées sur un pseudo-compte, FDFP à 1 %, CN absente | mensuelle | 3.2 | oui |
| 2,8 % passés en 6413 sous « CE et CN » ; TA et FPC absentes | Sage | 3.2 | oui |
| Dette ITS/FDFP sur la racine 447 | Sage | 3.2 | oui |
| Un seul paiement ITS au 30/12 (8 400) au lieu d'un par quittance ; dette 29 400 contre 16 800 réels | Sage | 3.2, G4 | alerte |
| D 311 / C 5211 + 571 « affectation du financement en stock » 41 800 413 | mensuelle | 3.8, R11 | oui |
| Stock initial 3 253 700 jamais soldé par 6031 | mensuelle | 3.8 | oui |
| Stock final 0 sans PV d'inventaire ; aucun achat 601 dans l'année | Sage | 3.8 | alerte |
| Mandants en 4671/4672 (inexistants), commission en 7062 (hors Région) | mensuelle | §2 | oui |
| Loyer 6132, carburant 6041, transport 6271, entretien camion 6241, « autres charges » 6388 | mensuelle/Sage | §2 | oui (sauf 6241) |
| Capital en 103 dans une SARL | mensuelle | R12 | oui |
| Deux versions contradictoires des mêmes écritures dans le même dossier | — | une seule version remise, l'autre archivée en _OBSOLETE | non |

## F. FAMILLE KRA — journal Sage du client et reconstruction MDC du 17/11/2026

Journal Sage du client (export « Brouillard des journaux », 341 lignes) : 43 erreurs bloquantes au contrôle du 17/11/2026, dont 12 fausses alertes du script, corrigées le même jour.

| Observation | Règle | Script |
|---|---|---|
| D 311 / C 521 + 571 « affectation du financement en stock » 41 800 413 — **née de la reconstitution MDC du 04/08/2026** (trésorerie de fin d'année estimée, écart porté en stock), recopiée dans Sage. Supprimée de la base MDC du 02/11/2026 le 17/11/2026 | R11, R14 | oui |
| Négoce enregistré en mandat : ventes et achats en 467, « commission » 7072 = ventes − achats ; ventes = achats × 1,100671 les 12 mois | R18 | oui (alerte marge constante) |
| Charges identiques 12 mois sur 12 (carburant 250 000, électricité 60 000, entretien 75 000, transport 47 500, téléphone 20 000) ; carburant et entretien avant l'achat du camion | R15 | oui (alerte) |
| Pièces mensuelles coupées sur 2 ou 3 numéros (OD 13/75/77, CAIS 14/76, OD 68/73, CAIS 69/74) | R19 | oui |
| Taxes sur salaires en 4428 ; dotation en 68112 ; intérêts courus en 166 | §2, R19 | oui |
| Fournisseur 401002 réglé au débit du 411 | R2 | non (contrôle du dossier KRA) |
| Prêts de microfinance BAOBAB et GESCI en 521 ; GESCI inscrit pour 50 000 000 alors que l'échéancier porte 40 588 413 de capital | R17 | oui (alerte) |
| Quittances e-impôts par mobile passées en banque sans relevé | R14, R16 | oui (552 créditeur) |
| Résultat 2024 fondu dans le report à nouveau sans PV d'AGO | R7 | oui |

Fausses alertes du script corrigées le 17/11/2026 : libellé Sage abrégé « TAXE SUR APPOINT.ET SALAIRE » pris pour un salaire ; « taxes sur salaires sans aucun paiement » quand les paiements sont sur un mauvais compte de dette (4428) ; « stock final 0 » quand le stock a été alimenté hors 6031.

Décisions du Gérant (17/11/2026) : négociant en gros et demi-gros (pas de mandat) ; régime TEE maintenu dans les écritures ; aucun mouvement bancaire sans relevé (seuls les échéanciers BAOBAB LD2435470324 et GESCI A01CRD2025051U00117 sont au dossier) ; aucune écriture CNPS sans instruction ; aucun chiffre « diversifié ».
