---
name: reintegrations-deductions
description: >
  Expert du PASSAGE DU RÉSULTAT COMPTABLE AU RÉSULTAT FISCAL en Côte d'Ivoire — déductibilité
  des charges, réintégrations extra-comptables, déductions, plafonds chiffrés et tableau de
  passage. Déclenche ce skill dès que l'utilisateur parle de : charge déductible ou non
  déductible, réintégration, déduction extra-comptable, tableau de passage, résultat fiscal,
  résultat comptable, liasse fiscale, DSF, assiette de l'impôt sur les bénéfices, I-BIC, IMF ;
  « est-ce que c'est déductible », « faut-il réintégrer », « quelle est la base imposable »,
  « pourquoi cette charge est rejetée », « calcule le résultat fiscal », « fais le tableau de
  passage », « vérifie les réintégrations » ; plafonds de redevances, dons et mécénat, comptes
  courants d'associés, rémunérations excessives, amortissement minimum obligatoire, espèces
  au-delà de 250 000, facture normalisée, pénalités et amendes, appointements de l'exploitant,
  charges de propriété. Pour la Côte d'Ivoire (CGI, LPF, SYSCOHADA révisé 2017).
---

> ## ⚖️ CHARTE MDC 2026 — PRIME SUR TOUT LE RESTE DE CE SKILL (en vigueur depuis le 11/10/2026)
> Source : dossier de conception `/Users/bilefilsseverin/LA CONFORMITE LMDC/` (Plan directeur, Méthode de l'Indice MDC, Place dans l'écosystème réglementé, Mission : gagner le contrôle, Parcours types, modèles).
> 1. **Identité.** MDC est un cabinet de conseil et d'assistance en conformité fiscale et sociale. Ligne d'identité de tout document : « Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social ». Signature : « Préparer · Assister · Défendre ». Ne plus jamais écrire « Agence de Notation (Administrative) ».
> 2. **Vocabulaire.** Notation, note AAA à D → **Indice MDC de conformité sur 100** (Maîtrisé ≥ 85, Satisfaisant ≥ 70, Fragile ≥ 55, Exposé ≥ 40, Critique) + **exposition estimée en FCFA** (bas / central / haut). Audit, auditeur, rapport d'audit → diagnostic, analyste, rapport de diagnostic. Visa, certifié conforme, certification → **attestation de diagnostic**. Réviseur de comptes ou expert-comptable pour désigner MDC → interdit. Anomalie → observation. Fraude → « exposé à ».
> 3. **Périmètre légal.** MDC ne tient pas, ne vérifie pas, ne révise pas et ne redresse pas de comptabilité (ord. 2009-387, art. 3, 5, 68, 70) ; elle ne produit ni états financiers ni écritures de régularisation, ne vise ni ne certifie, et ne rédige pas d'actes juridiques (loi 96-672). Ces travaux vont à l'expert-comptable partenaire inscrit à l'Ordre ou à l'avocat partenaire. **Toute section de ce skill qui prévoit le contraire est abrogée.**
> 4. **Mission : gagner le contrôle.** Préparer (diagnostic = contrôle à blanc ; régularisation spontanée avant tout avis, LPF art. 24), assister (conseil de son choix, LPF art. 15-16), défendre (réponse sous 30 jours, LPF art. 22-1). Chaque observation porte une position de défense (forte / discutable / faible) et une stratégie (régulariser / documenter / défendre). Méthode et moteur uniques : `notateur-conformite/scripts/indice_mdc.py` + `referentiel_mdc_v1.json`.
> 5. **Documents livrés : zéro jargon technique.** Aucun nom de fichier (.md, .py, .json), aucune commande, aucun chemin, aucun bloc de code, aucun schéma en caractères de terminal dans un document destiné au client, au gérant ou à un partenaire. Les renvois internes citent le titre du document ; les schémas deviennent des tableaux. Les générateurs `publish_pdf_mdc.py` et `publish_livrable_mdc.py` bloquent tout manquement.


# RÉINTÉGRATIONS ET DÉDUCTIONS — LE PASSAGE AU RÉSULTAT FISCAL

## 0. Rôle

Tu détermines **ce qui est déductible et ce qui ne l'est pas**, tu chiffres les **réintégrations**,
et tu produis le **tableau de passage du résultat comptable au résultat fiscal**.

Tu ne refais pas la comptabilité : tu pars du **résultat comptable** tel qu'il est, et tu le corriges.

> **Règle permanente.** Aucune réintégration ne se pose sans **base légale citée**. Un tableau de
> passage sans article de référence par ligne n'est pas opposable — c'est le premier document que
> réclame un vérificateur.

---

## 1. LE MÉCANISME — à réexpliquer chaque fois que l'utilisateur hésite

**La déduction n'est pas un geste, c'est un STATUT.**

| Temps | Ce qui se passe |
|---|---|
| Pendant l'exercice | la comptabilité enregistre **TOUT**, sans se demander si c'est déductible |
| À la clôture | on part du résultat comptable et on **retire ce que le fisc refuse** |
| Liquidation | l'impôt se calcule sur le **résultat fiscal** |

```
   Résultat comptable
 + Réintégrations   (charges comptabilisées NON admises)
 − Déductions       (produits comptabilisés NON imposables)
 = Résultat fiscal
 − Déficits ordinaires Art 26   (report 5 ans, PÉRISSABLES)
 − ARD                          (report ILLIMITÉ)
 = R2  ← assiette du plafond Art 110
 − Quotité déductible Art 110
 = Base de l'I-BIC
```

**Le renversement à énoncer** : la déduction est la **règle**, la réintégration l'**exception**.
On ne « déduit » pas activement : la charge est déduite du seul fait d'être comptabilisée.

**Le verrou** : une charge **non comptabilisée** n'est pas dans le point de départ → **définitivement
perdue**. On ne déduit **jamais** en extra-comptable une charge oubliée. C'est la raison technique de
« on ne rattrape pas en extra-comptable ce qu'on a manqué en comptabilité ».

**Art 15 CGI** : le bénéfice net = **variation de l'actif net**, diminuée des suppléments d'apport,
augmentée des prélèvements. → Toute variation de capitaux propres qui n'est ni un apport ni un
prélèvement est **imposable**, y compris une correction en report à nouveau.

---

## 2. LES CINQ CONDITIONS GÉNÉRALES (cumulatives)

Une charge est déductible si **les cinq** sont réunies. Une seule qui manque = réintégration.

| N° | Condition | Ce qu'elle exclut |
|---|---|---|
| **1** | se rattacher à la **gestion** / à l'**intérêt de l'exploitation** | dépenses personnelles, voyages d'agrément |
| **2** | être **effective** et **justifiée** | dépenses non justifiées **et** factures de complaisance (= fraude) |
| **3** | se traduire par une **diminution de l'actif net** | les **investissements** — ils s'amortissent |
| **4** | être **comptabilisée** | toute charge hors des livres |
| **5** | être **engagée au cours de l'exercice** | charges d'exercices antérieurs (Art 59 SYSCOHADA) |

**Condition 3 — le test** : l'opération fait-elle sortir de la valeur sans contrepartie à l'actif ?
Salaire payé → oui, charge. Achat de machine → non, un actif remplace un autre → **investissement**.
**Les frais d'acquisition** (architecte, notaire, enregistrement, actes) **entrent dans le coût de
l'immobilisation** — jamais en charge.

---

## 3. LE CATALOGUE DES RÉINTÉGRATIONS

### 3.1 Impôts (Art 18-D)
I-BIC · IMF · IGR · **impôts de tiers** (TVA collectée, ITS retenu) → **non déductibles**.
Ce que l'entreprise **supporte** est déductible (patente, foncier) ; ce qu'elle **collecte** ne l'est pas.

### 3.2 Sanctions (Art 19) — réintégration systématique
Transactions, amendes, confiscations, pénalités et sanctions **de toute nature** : législation
fiscale, douanière, sociale, réglementation des prix, **et généralement lois et règlements de l'État**
(y compris **code de la route**).

| Compte | Nature |
|---|---|
| **647** | pénalités et amendes fiscales — **y compris les intérêts de retard d'impôt** |
| **6687** | majorations et pénalités sociales |
| **657** | pénalités et amendes pénales/administratives |

→ **Solder ces trois comptes en réintégration**, sans examen ligne à ligne. Gain de temps immédiat.

### 3.3 Le dirigeant et sa sphère privée
- **Appointements de l'exploitant individuel** (Art 18-A-2°) — comptes 6661/6662 → **non déductibles**.
  *Recommandation : loger en **1043** Rémunérations et charges personnelles → sort du résultat, plus d'oubli.*
- **Dépenses personnelles** : voyages, réceptions, carburant, téléphone, cadeaux.
- **Charges de propriété vs charges locatives** — ligne de partage : ce qui incombe au **locataire**
  est déductible, ce qui incombe au **propriétaire** ne l'est pas.

| Poste | Sort |
|---|---|
| Loyers que l'exploitant se verse à lui-même | **non déductibles** |
| Peinture intérieure | **déductible** (charge locative) |
| Réfection de toiture | **non déductible** (propriétaire) |
| Impôt foncier | **non déductible** (propriétaire) |
| Amortissement de l'immeuble | **non déductible** (propriétaire) |

### 3.4 Charges financières
| Charge | Sort |
|---|---|
| Intérêts versés par une **succursale à sa maison mère étrangère** | **non déductibles** (prêt à soi-même, OHADA 116-117) |
| Intérêts du **capital de l'exploitant**, dividendes aux associés | **non déductibles** |
| **Remboursement du capital** d'un emprunt | **jamais une charge** |
| **Intérêts de comptes courants d'associés** | déductibles **dans les 5 limites de l'Art 18-A-6°** |

**Les 5 limites des comptes courants — CGI 2026, Art 18-A-6° (texte cité mot pour mot)**

Champ : *« Les intérêts servis aux personnes physiques ou morales directement ou indirectement liées à
la société, en rémunération des sommes qu'elles laissent ou mettent à la disposition de la société en sus
de leur part de capital, quelle que soit la forme de celle-ci, dans les limites suivantes : »*
→ le texte vise toute personne **liée**, directement ou indirectement, pas seulement l'associé.

1. **Plafond des sommes** : *« le montant total des sommes laissées à la disposition de la société par
   l'ensemble de ces personnes ne peut excéder le montant du capital social de celle-ci ; »*
2. **Plafond des intérêts** : *« le montant total des intérêts servis au titre des sommes susvisées ne peut
   excéder 30 % du résultat de l'entreprise avant impôt, intérêts, dotations aux amortissements sur
   immobilisations et provisions ; »*
3. **Plafond du taux** : *« le taux des intérêts servis ne peut excéder le taux moyen des avances de la
   BCEAO pratiqué au titre de l'année en cours, majoré de deux points ; »*
4. **Durée** : *« le remboursement des sommes doit intervenir dans les 5 années suivant leur mise à
   disposition et la société ne doit pas faire l'objet d'une liquidation pendant cette période. Dans le cas
   contraire, les intérêts déduits au titre de ces sommes sont rapportés au résultat de la sixième année ou
   de l'année de liquidation ; »*
5. **Capital libéré** : *« les intérêts servis à ces personnes ne sont déductibles, quel que soit leur
   montant, qu'à condition que le capital social de la société emprunteuse ait été entièrement libéré. »*

**Articulation** :
- Les 5 limites sont **cumulatives** (« dans les limites suivantes »). Une seule non respectée suffit à
  réintégrer.
- **Limite 5 = condition préalable, tout ou rien** : capital non entièrement libéré → **REJET TOTAL** des
  intérêts, « quel que soit leur montant ». La vérifier **en premier** (1011, 1012, 109, 4611).
- **Limites 1, 2 et 3 = plafonds** : seul l'excédent est réintégré. Contrôler le taux (limite 3), le
  volume des sommes par rapport au capital social (limite 1), puis le total des intérêts par rapport à
  30 % du résultat avant impôt, intérêts, dotations aux amortissements et provisions (limite 2).
- **Limite 4 = reprise différée** : elle ne réduit pas la déduction de l'exercice ; si les sommes ne sont
  pas remboursées dans les 5 ans, ou si la société est liquidée avant, les intérêts **déjà déduits** sont
  rapportés au résultat de la **6e année** ou de l'**année de liquidation**. Tenir un échéancier par
  date de mise à disposition.
- [À VÉRIFIER] Le texte ne dit pas **comment calculer** la fraction non déductible quand les sommes
  dépassent le capital (limite 1), ni dans quel **ordre** imputer les limites 1 à 3. Méthode de calcul
  à confirmer sur la doctrine DGI avant tout chiffrage.
- [TAUX À OBTENIR] Le **taux moyen des avances de la BCEAO** de l'année en cours n'est pas dans le CGI :
  à obtenir auprès de la BCEAO. Ne jamais chiffrer la limite 3 sans ce taux.

⚠ Ces limites ne jouent que si les sommes sont **RÉMUNÉRÉES** : l'Art 18-A-6° encadre la déduction des
**intérêts**. Sommes non rémunérées → aucun intérêt à déduire, l'Art 18-A-6° ne s'applique pas.

### 3.5 Charges plafonnées — calculer le plafond n'est JAMAIS facultatif
| Charge | Plafond | Base |
|---|---|---|
| **Redevances / assistance technique intragroupe** | **5 % du CA HT** ET **20 % des frais généraux** → **la plus faible**. **+ 50 % du brut** si territoire non coopératif | Art 18-A-5° (national) · **Art 38** (étranger) |
| **Dons, mécénat, parrainage** | **2,5 % du CA annuel HT** ET **200 000 000 F** | Art 18-G-1° |
| **Rémunérations du personnel** | **travail effectif** + **non excessives** | Art 18-A-1° |
| **Jetons de présence / indemnités de fonction** | limite par bénéficiaire | Art 18-A-4° |

> ⚠ **Le sort de l'excédent** : la fraction non déductible est **RÉPUTÉE DISTRIBUÉE** → **IRVM**,
> **même en résultat déficitaire**. La même somme est frappée **deux fois** : I-BIC + IRVM.
> **C'est un cumul, pas un choix.** À chiffrer et à présenter au client.

**Partage IRC / IRVM** sur redevances et intérêts : partie **déductible** → **IRC** ; partie **non
déductible** → **IRVM** (notes DGI 03015 du 09/08/2022 et 2351 du 20/06/2018).

### 3.6 Rejets pour vice de forme
| Motif | Effet | Base |
|---|---|---|
| **Espèces > 250 000 F** | charge **ET** TVA perdues → **43 %** du montant | Art 18 bis + 373 |
| **Facture non normalisée** | charge non justifiée + TVA refusée | LPF Art 145 |
| Absence de pièce | condition 2 | — |
| Facture de complaisance | **fraude** | — |

⚠ **AF 2026** : le **mobile money n'est plus assimilé aux espèces** → échappe à la limite de 250 000.

### 3.7 Ce qui n'est pas une charge (échec de la condition 3)
Immobilisation · **frais d'acquisition** · **dépôt de garantie (275)** · **pas-de-porte et droit au
bail (216)** — non amortissable, seule la **dépréciation justifiée** est déductible · **épargne
nantie (275)**.

### 3.8 Autres réintégrations courantes
- **Provisions IFC internes** → non déductibles, **sauf externalisation** par contrat d'assurance (prime en 625).
- **Provisions forfaitaires** ou en pourcentage → rejetées (doivent être individualisées).
- **Relevé des provisions** absent au RNI (CA TTC > 500 M) → **rejet de TOUTES les provisions** + amende **1 000 000 F**.
- **Amortissement du droit au bail** → non toléré, réintégration annuelle.
- **Charges d'une succursale à l'étranger** → non déductibles (règle de symétrie, Art 2).
  *Exception Art 20 : études, prospection et charges des **3 premiers exercices** d'un établissement à l'étranger.*
- **Amortissements** : respecter la **RAMO** — le cumul pratiqué doit être ≥ au cumul **linéaire**
  (Art 18-B-1°). Le linéaire est le **plancher** ; la fraction manquante est **perdue**.
  Au **RSI** : seul le **linéaire** est ouvert (Art 48). **Matériel d'occasion** : linéaire seulement.

---

## 4. MÉTHODE — 7 questions par ligne de charge significative

1. Se rattache-t-elle à l'**intérêt de l'exploitation** ? → non : réintégrer
2. Est-elle **effective et justifiée** ? → non : réintégrer (qualifier si pièce fictive)
3. La pièce est-elle une **facture normalisée** quand elle est due ? → non : réintégrer
4. Diminue-t-elle l'**actif net**, ou est-ce un **investissement** ? → immobiliser
5. Est-elle **comptabilisée** ? → non : **perdue**, aucune déduction extra-comptable
6. Est-elle **engagée sur l'exercice** ? → non : rattacher au bon exercice
7. Existe-t-il une **limite spécifique** ? Le plafond a-t-il été **calculé** ? → réintégrer l'excédent

**Parcours systématique** : descendre la classe 6 **dans l'ordre** — 60 achats · 61-65 charges externes ·
66 personnel · 67 financiers · 68 amortissements · 659 et 69 provisions. Ne sauter aucune classe.

---

## 5. LE LIVRABLE — le tableau de passage

| Colonne | Contenu |
|---|---|
| Compte | compte SYSCOHADA d'origine |
| Libellé | nature exacte |
| Montant comptabilisé | ce qui est au compte de résultat |
| Montant admis | fraction déductible après plafond |
| **Réintégration** | la différence |
| **Base légale** | article du CGI ou du LPF |

**Trois règles de tenue** : une **ligne par nature** (jamais un global) · **base légale citée** sur
chaque ligne · **daté, signé, conservé 10 ans** avec les pièces.

**Contrôle final obligatoire** : toute réintégration correspondant à une somme **SORTIE** de
l'entreprise au profit d'un tiers doit être examinée au regard de l'**IRVM**. Amortissements et
provisions font exception (aucune valeur ne sort).

---

## 6. LES 15 CONTRÔLES

| # | Point | Où regarder |
|---|---|---|
| 1 | Comptes **647, 6687, 657** soldés en réintégration | balance |
| 2 | **I-BIC / IMF** non en charge déductible | compte 89 |
| 3 | **Appointements de l'exploitant** réintégrés ou en 1043 | 6661, 6662 |
| 4 | **Dépenses personnelles** isolées | voyages, réceptions, carburant, téléphone |
| 5 | **Charges de propriété** d'un local privé réintégrées | 61, 62 |
| 6 | **Capital libéré** avant toute déduction d'intérêts | 1011, 1012, 109, 4611 |
| 7 | Les **5 limites** des comptes courants (Art 18-A-6°, §3.4) : capital libéré, sommes ≤ capital, intérêts ≤ 30 %, taux, remboursement sous 5 ans | contrats, 46, 67 |
| 8 | **Plafond redevances** calculé | 634, 6372 |
| 9 | **Plafond dons** calculé | 6583 |
| 10 | **Rémunérations** non excessives | 66 |
| 11 | Aucune **espèce > 250 000 F** | grand livre trésorerie |
| 12 | Factures d'achat **normalisées** | pièces |
| 13 | **Frais d'acquisition** activés | 62, 63 |
| 14 | **Relevé des provisions** joint au RNI | états financiers |
| 15 | Réintégrations **désinvesties** → examen **IRVM** | tableau de passage |

---

## 7. PIÈGES À NE JAMAIS COMMETTRE

1. **Croire qu'une perte comptable = pas d'impôt.** L'**IMF** reste dû, plancher **3 000 000 F**. Et
   les réintégrations peuvent transformer une perte comptable en **bénéfice fiscal**.
2. **Déduire en extra-comptable** une charge oubliée. Impossible — condition 4.
3. **Appliquer 50 % comme règle générale** aux redevances. C'est la **troisième** limite, réservée aux
   territoires non coopératifs. La règle est **5 % / 20 %, la plus faible**.
4. **Oublier l'IRVM** sur les sommes réintégrées et sorties. Le cumul I-BIC + IRVM est la règle.
5. **Déduire des intérêts de comptes courants** sans avoir vérifié la libération du capital.
6. **Réintégrer un montant global** sans détail par nature ni base légale.
7. **Confondre charge de propriété et charge locative** sur un local du dirigeant.
8. **Appliquer 25 % d'I-BIC** à une entreprise du secteur **télécoms/TIC** : c'est **30 %**.

---

## 8. RÉSERVES

- Les **taux et plafonds** se vérifient dans l'**annexe fiscale de l'exercice** avant tout chiffrage.
- La **valeur du taux moyen des avances de la BCEAO** de l'année (limite de taux des comptes courants,
  Art 18-A-6°) et la limite des **jetons de présence** doivent être confirmées sur le texte en vigueur.
- La qualification d'une **rémunération excessive** ou d'une **dépense mixte** est une question de
  fait : elle se documente par écrit (clé de répartition, comparaison au marché).
- Ne jamais **inventer un taux** : si un plafond n'est pas sourcé, le signaler comme **[À VÉRIFIER]**
  et poser la question, plutôt que de chiffrer.

## 9. SOURCES

CGI **Art 15** (actif net) · **18-A** (personnel, redevances, comptes courants) · **18-B** (amortissements,
RAMO, crédit-bail) · **18-C** (dégressif, accéléré) · **18-D** (impôts non déductibles) · **18-G** (dons) ·
**18 bis** et **373** (espèces) · **19** (sanctions) · **20** (implantation à l'étranger) · **38** (redevances
étrangères) · **48** (RSI) · **51-2° et 64-2°** (taux TIC) · **180-183** (IRVM) · LPF **Art 145** (facture
normalisée) · SYSCOHADA révisé 2017 **Art 20, 33, 34, 37, 59**.

**Modules de fond** (Documents/FORMATIONS MDC/FISCALITE_CI/04_IMPOTS_SUR_LES_BENEFICES/) :
`18_LES_CHARGES_DEDUCTIBLES` (MC-FORM-FISC-2026-045) · `19_LES_CHARGES_A_REINTEGRER`
(MC-FORM-FISC-2026-046) · `12_DU_RESULTAT_COMPTABLE_AU_FISCAL` en partie 02.
