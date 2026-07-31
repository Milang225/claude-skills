# FICHE — ÉCRITURES SPÉCIFIQUES EBNL (22 cas d'application corrigés)

> Source : **Guide d'application du SYCEBNL** (22 applications). Numérotation reprise **du guide** ;
> le plan officiel note certaines variantes (7922 pour 7925 ; 96/97 pour 90/91 ; 8411 pour 8421) —
> voir `FICHE_PLAN_COMPTABLE_SYCEBNL.md`. Sigles : EBNL = Entité à But Non Lucratif ; HAO = Hors
> Activités Ordinaires ; VNC = Valeur Nette Comptable ; BAD = Banque Africaine de Développement.

**Principe transversal** : toute ressource dédiée (dotation consomptible, subvention, fonds affecté,
don/legs) est **neutralisée** par une reprise (79x) ou une quote‑part transférée (702/703), au **rythme**
de la consommation ou de l'amortissement.

---

## CHAPITRE 1 — Fonds propres des associations, fondations et assimilés

### Application 1 — Dotation consomptible et non consomptible
- Apports **définitifs** = dotation **non consomptible sans droit de reprise** (101) ; apports pour
  **fonctionnement** = dotation **consomptible** (104) ; apports **provisoires** = dotation non
  consomptible **avec** droit de reprise (102).
- Si statuts prévoient souscription/libération → comptes **45 apporteurs** (4511 nature / 4512 numéraire).
```
Souscription : D 4511/4512 / C 1015, 1041 (ou 1025/1021 pour provisoires)
Libération   : D 2xx immob. / 5xx / C 4511/4512
Clôture      : D 1049 / C 703  (couverture des charges par la dotation consomptible consommée)
```

### Application 2 — Droit d'adhésion et appel de cotisations de nouveaux membres
- Ventilation de l'appel global : **droit d'entrée (103)**, **dépôt restituable (1851)**, **cotisations (701)**.
```
Appel       : D 411 / C 103, 1851, 701
Encaissement: D 52 / C 411
```

### Application 3 — Subventions d'investissement destinées à une association
```
Notification : D 4731 / C 1417 (organismes internationaux)
Réception    : D 5211 / C 4731
Acquisition  : D 2xx / C 4812 ; règlement D 4812 / C 5211
Reprise      : D 1417 / C 799  — terrain (non amortissable) : sur 10 ans sans prorata ;
               bâtiment : au rythme de l'amortissement (ex. 1/20 × prorata)
```

---

## CHAPITRE 2 — Fonds affectés et reportés (associations, fondations)

### Application 4 — Fonds non utilisés en fin d'exercice destinés à un projet spécifique
```
Réception donation (BAD) : D 52 / C 165
Consommation (ex. 1/3)   : D 165 / C 7925  [officiel : 7922]
Solde consommé N+1       : D 165 / C 7925
```

### Application 5 — Fonds provenant des dons et legs (d'immobilisations)
```
Réception legs   : D 2313, 2442, 2441, 2451 / C 4861 (dettes successorales) et C 167
Paiement dettes  : D 4861 / C 52
Provision charges: D 1679 / C 192  (ex. entretien de la tombe 25 ans)
Amortissements   : D 6813 / C 283x, 284x
Reprise fonds    : D 167 / C 7923  (= montant de la dotation aux amortissements)
```

### Application 6 — Legs/donations non reçus d'immobilisations destinées à la vente
```
Constatation     : D 203/204 / C 172
Dépréciation N+1 : D 6952 / C 2902
Cession          : D 818 / C 203,204 (VNC) ; D 485 / C 828 ; D 52 / C 485
Solde du 172     : D 172 / C 7962
Solde dépréc.    : D 2902 / C 7952
```

### Application 7 — Donation temporaire d'usufruit
```
Réception  : D 2011 / C 171
Loyer      : D 412 / C 7082 ; encaissement D 52 / C 412
Amort.     : D 680 / C 280  (sur la durée de la donation)
Reprise    : D 171 / C 7961  (même rythme)
Dépréc.    : par simplification, information en Note 5D (pas d'écriture)
Rétrocession: D 280 / C 2011
```

---

## CHAPITRE 3 — Fonds propres des projets de développement

### Application 8 — Projet de développement (financement Banque Mondiale)
```
Décaissement : D 52 / C 162 (invest. = 80%) et C 462 (fonctionnement = 20%)
Investissements: D 22/23/24 / C 4812 ; règlement D 4812 / C 52  (PAS d'amortissement)
Charges fonct.: D 60-66 / C 40, 42, 43, 44 …
Neutralisation: D 462 / C 702  (au fur et à mesure des charges)
Fonds invest. non consommés (clôture) : D 162 / C 165
Extourne 01/01/N+1 : D 165 / C 162
Ajustement clé bailleur : D 162 / C 462 (réaffectation)
```
> Option **états par bailleur/sous‑projet** : suffixer les comptes d'un identifiant bailleur ; états
> combinés obligatoires.

---

## CHAPITRE 4 — Dons

### Application 9 — Dons en nature à distribuer
```
Réception        : D 654 / C 7542
Non consommé (clôture): D 345 / C 6035  et  D 7542 / C 4713
Réouverture 01/01: D 6035 / C 345  et  D 4713 / C 7542  (contrepassation)
```

### Application 10 — Dons en nature à vendre
- Suivi en **classe 9 (engagements/CVN)** jusqu'à la cession ; frais avant cession en charges,
  neutralisés par **476** si non vendu en fin d'exercice.
```
Réception (engagement) : D 901 / C 910   [officiel : 961/970]
Frais remise en état   : D 8311 / C 52
Clôture si non vendu   : D 476 / C 8311  ; réouverture D 8311 / C 476
Vente HAO              : D 52 / C 8421   [officiel : 8411]
```

### Application 11 — Dons en numéraire, revenus des manifestations et édifices religieux
```
Générosité (église) : D 57, 52 / C 7041 (dons), 7043 (deniers du culte), 7044 (quête), 7045 (dîmes)
Dons notifiés non encaissés : D 475 / C 7041
Manifestation (kermesse) : charges D 6061 (billetterie), 6062 (tombola) / C 401 ; recette D 57 / C 706
Mosquée (zakat, célébration) : D 57,52 / C 7041, 7044 (zakat), 7045 (célébrations)
Construction : D 252 (avance)/C 52 ; D 2327 (édifice religieux, sous escompte 5%) / C 252, 4812
```

### Application 12 — Frais de recherche de fonds
```
D 636 Frais de recherche de fonds / C 40 ; règlement D 40 / C 52
```

---

## CHAPITRE 5 — Cotisations des membres et versements des fondateurs

### Application 13 — Cotisations des membres
```
Appel        : D 411 / C 701
Recouvrement : D 57 / C 411
Douteux      : D 4161 / C 411
Dépréciation : D 6594 / C 4912  (ex. 80% des cotisations dues)
```

### Application 14 — Contribution du fondateur (frais de fonctionnement d'une fondation)
```
D 52 / C 752 Contribution du fondateur (versement)
```

### Application 15 — Subventions et aides financières versées par les EBNL
```
D 652 Subventions versées par l'entité / C 57  (ex. aide à un parti politique)
```

---

## CHAPITRE 6 — Autres opérations spécifiques

### Application 16 — Subvention d'exploitation sur plusieurs exercices
```
Notification : D 4732 / C 711 ; encaissement D 52 / C 4732
Clôture N    : D 711 / C 477  (part des exercices futurs)
Rattachement N+1, N+2 : D 477 / C 711
```

### Application 17 — Abandons de frais engagés par les bénévoles
```
Frais engagés : D 6181, 6384, 6383, 6055 / C 4572 Bénévoles
Abandon       : D 4572 / C 7583 Abandons de frais par les bénévoles
```

### Application 18 — Convention de mécénat
```
Signature : D 4751 Mécènes / C 7046 Mécénats
Versements: D 52 / C 4751
```

### Application 19 — Restitution de subvention non utilisée conformément à la convention
```
Notification (invest.+exploit.) : D 4731, 4732 / C 1417, 713
Réception  : D 52 / C 4731, 4732
Quote-part à reverser : D 1417 / C 4739
Reversement : D 4739 / C 52
```

### Application 20 — Contributions volontaires en nature
```
Dons en nature (fournitures) : D 901 / C 910   [officiel : 961/970]
Personnel bénévole           : D 904 / C 914   [officiel : 964/974]  (heures × SMIG horaire)
→ Information en Note 1 (Ressources / Emplois) ; évaluation à la valeur actuelle / SMIG horaire.
```

---

## CHAPITRE 7 — Tableaux de correspondance (projets de développement)

### Application 21 — Tableau Emplois‑Ressources (TER)
- **Ressources** (mouvement crédit) : 161/162/462 (bailleurs), 163/463 (contrepartie État), 164/464/707/77.
- **Emplois – immobilisations** (mouvement débit classes 21‑25, net des dettes 481).
- **Emplois – charges** (mouvement débit 60‑67, net des variations de dettes fournisseurs/fiscales/personnel).
- **Fonds disponibles début/fin** = soldes débiteurs N‑1 / N des comptes 51, 52, 53, 55, 57.
- Contrôle : **Encaisse disponible (III+IV) = Fonds disponibles fin (VI)**.

### Application 22 — Tableau d'exécution budgétaire
Colonnes : Budget (1) | Décaissement (2) | Engagement (3) | Réalisation (4 = 2+3) | Crédit disponible
(5 = 1−4) | Exécution % (4/1).
- **Décaissement** = mouvements débit N des immobilisations (hors virements internes) + variation des
  dettes fournisseurs d'investissement + mouvements débit des charges (6, 8), net des variations 40/409.
- **Engagement** = solde créditeur N des fournisseurs (40) et fournisseurs d'investissement (481) + bons
  de commande / contrats signés non exécutés.
```

---

## Aide‑mémoire des comptes de reprise / transfert (le cœur de la neutralité EBNL)

| Ressource dédiée | Reprise / transfert |
|------------------|---------------------|
| Dotation consomptible (104/1049) | **703** Quote‑part de dotation consomptible transférée |
| Fonds d'administration projet (462) | **702** Quote‑part de fonds d'administration transférés |
| Fonds affecté à un projet (165) | **7922** (guide : 7925) |
| Fonds affectés aux investissements projet (162) | **7921** |
| Dons et legs d'immobilisations (167) | **7923** |
| Donation temporaire d'usufruit (171) | **7961** |
| Legs d'immob. destinées à la vente (172) | **7962** |
| Dépréc. immob. destinées à la vente (2902) | **7952** (reprise) |
| Subvention d'investissement (14x) | **799** |
