---
name: ecritures-sans-faute
description: >
  Garde-fou OBLIGATOIRE de toute production d'écritures comptables MDC (SYSCOHADA révisé, Côte d'Ivoire).
  Né des notes de revue de visa reçues le 11/11/2026 (FAMILLE KRA, KWAANI, KG CONSULTING) et le 13/10/2026
  (TIM 7) qui relèvent : numéros de comptes faux, écritures globales au 31/12, tiers anonymes, à-nouveaux
  faux, charges différentes des déclarations, caisse créditrice, comptes d'attente non apurés.
  Déclenche AVANT de remettre : une écriture, un journal, un ordre de saisie Sage, une balance, un fichier
  de reconstitution, des à-nouveaux, une liasse SMT/SN. Aucun livrable comptable ne sort sans le passage
  du script de contrôle et de la grille de rapprochements de ce module.
---

# Écritures sans faute — garde-fou comptable MDC

**Pourquoi ce module existe.** Les réviseurs (cabinet de visa) ont rejeté les états financiers de quatre
clients pour les mêmes fautes, et les écritures TRACE LOGISTICS produites en juin 2026 contenaient
elles-mêmes six numéros de comptes faux (6313, 4611, 4616, 624100, 626000, 629000). Le module
`mdc-expert` contenait déjà les bons comptes : l'erreur vient de l'application. Ce module est donc
court, impératif, et adossé à un contrôle automatique.

**Ordre de travail imposé** (aucune étape sautée) :

1. Rassembler les pièces (§6) et lister ce qui manque **avant** d'écrire.
2. Choisir chaque compte dans la table §2, puis le vérifier dans `../mdc-expert/reference/PLAN_COMPTABLE_OHADA_COMPLET.md`
   (AUDCIF p. 223-276). Jamais de numéro « de mémoire ».
3. Passer les écritures selon les schémas §3, **à leur date réelle**, une pièce par opération.
4. Lancer le contrôle automatique (§5). Zéro erreur bloquante exigée.
5. Remplir la grille de rapprochements (§4). Tout écart non expliqué = livrable non remis.
6. Seulement alors : ordre de saisie, balance, liasse.

---

## 1. Les règles tirées des notes de revue (R1 à R20)

| N° | Règle | Faute relevée par le réviseur |
|---|---|---|
| R1 | **Chaque opération à sa date, sur sa pièce.** Interdit : une écriture unique au 31/12 qui résume l'année (ventes, charges, paie, règlements). | KG : « toutes les opérations 2025 passées en écritures globales au 31/12 » ; TIM 7 n° 3, 10, 14 |
| R2 | **Tiers nominatif.** Un compte 401/411 par fournisseur ou client réel (4011xxx/4111xxx), nom dans le libellé. Jamais « CLT », « Fournisseur », « Divers ». | KG : client « CLT » non nommé ; TIM 7 n° 13 : 38 FNP sans nom |
| R3 | **Le bon compte selon la nature, pas selon l'habitude.** Table §2. | KRA 3.6, KWAANI 3.1-3.2, KG Q1, TIM 7 n° 4 |
| R4 | **Deux temps** : constatation (D charge / C tiers) puis règlement (D tiers / C 52x ou 57x). Jamais D charge / C trésorerie dans la même pièce. Seule exception : ce que la banque prélève d'office au relevé (frais 631, agios 6745, échéance 162 + 6712), passé D charge / C 521x. | Méthode MDC (client, juin 2026) |
| R5 | **Charge fiscale = déclaration e-impôts = quittance.** La paie, la TEE, la patente, le foncier se comptabilisent au montant **émis/déclaré**, période par période ; les paiements à leur date réelle de paiement. | KRA 3.4, 3.7 ; KWAANI 3.3 ; KG tableaux 1-2 ; TIM 7 n° 17, 19 |
| R6 | **Rattachement à l'exercice.** Charge de N payée en N+1 → dette au 31/12/N. Charge de N-1 → à-nouveau ou report à nouveau, jamais charge de N. Opération de N+1 → jamais dans N. | KRA 2.5 (AMR non comptabilisé) ; KG (foncier 2024 en 2025) ; TIM 7 n° 24 (cartes 2026 en 2025) |
| R7 | **À-nouveaux = bilan N-1 visé, au franc.** Le journal d'à-nouveaux ne contient que des soldes de classes 1 à 5 au 01/01. Jamais de classe 6, 7 ou 8 ; jamais d'opération courante. | KG : compte 89 en à-nouveau, opérations 2024 dans le journal AN ; KRA 3.8 ; TIM 7 n° 5 ; KWAANI §5 |
| R8 | **Caisse jamais créditrice**, à aucune date. Brouillard de caisse + PV de caisse au 31/12. | TIM 7 n° 27 ; KG trésorerie |
| R9 | **Un compte par banque** (5211xx BMS, 5211xx GESCI…), rapproché du relevé au 31/12. | KRA 3.10 ; TIM 7 n° 24 |
| R10 | **Aucun compte d'attente au 31/12** (471, 472, 462 utilisé pour « équilibrer », 585 non soldé). Un solde inexpliqué = prélèvement de l'associé (4621) ou de l'exploitant (104), à documenter avec lui et sur pièce — jamais pour absorber un écart de trésorerie estimée (R14). | TIM 7 n° 25, 28, 29 ; KG (4478 de 750 non justifié) |
| R11 | **Pas de stock, d'actif ou de produit sans pièce.** Pas de virement de trésorerie en stock « par affectation » ; pas de CA réduit aux commissions sans contrat de mandat. | KRA 2.1, 2.2 |
| R13 | **Régime fiscal respecté.** Le compte 89 (891 impôt sur les bénéfices, 895 IMF) n'existe que pour les entreprises au **régime du réel**. Une entreprise au forfait (TEE ou régime des microentreprises) n'a aucun compte 89 : son impôt (TEE ou impôt des microentreprises) va en 6418, dette 446. Le régime est indiqué au contrôle (`--regime`). **Le régime effectif est celui des avis émis** : un chiffre d'affaires au-delà du plafond est un risque fiscal à chiffrer à part, jamais une raison de passer I-BIC, IMF ou TVA dans les écritures d'un client à la TEE. | KG (89000000 chez une EI à la TEE) ; KRA 2025 (CA négoce 219,8 M, société à la TEE) |
| R14 | **Trésorerie bancaire sur relevé uniquement.** Aucun mouvement en 52x ou 53x sans relevé. Seule exception : le document du prêteur (échéancier, attestation) pour la mise à disposition d'un prêt et la dette. Aucun règlement d'échéance sans relevé : l'intérêt de l'échéance va en charge (D 6712 / C 1662), le capital reste dans la dette. **Jamais de trésorerie de fin d'année fixée par estimation, jamais d'écriture d'équilibrage** : l'écart va dans la liste des pièces à obtenir, pas dans un compte. | KRA 2025 : la pièce « affectation du financement en stock » (41 800 413) est née de la reconstitution MDC du 04/08/2026, qui avait fixé banque 271 184 + caisse 2 000 000 « à confirmer sur relevés » ; supprimée le 17/11/2026 sur décision du Gérant |
| R15 | **Aucun chiffre inventé ni « diversifié ».** Un montant sans pièce reste tel quel et est signalé « à justifier » ; il n'est ni arrondi, ni ventilé, ni modifié pour paraître naturel. Chaque ligne d'une reconstitution porte sa source ; la méthode est écrite en note 2. Montants identiques chaque mois = forfait sans pièce : demander les factures. | KRA §4 (charges forfaitaires) ; demande refusée le 17/11/2026 de « diversifier » des montants ronds |
| R16 | **Monnaie électronique 552** (Wave, Orange Money, MTN, Moov). Paiement e-impôts par mobile (quittance MOB…) : D dette fiscale / C 552 à la date de la quittance. Chargement : D 552 / C 57x ou 52x à sa date. Le 552 n'est **jamais créditeur**. | KRA 2025 (quittances MOB passées en banque sans relevé) |
| R17 | **Microfinance en 538**, un sous-compte par établissement (538001 BAOBAB, 538002 GESCI…), jamais en 521 Banques. | KRA 3.10 |
| R18 | **Négoce en brut.** Une entreprise qui achète et revend pour son propre compte : ventes 7011 et achats 6011, une écriture par facture d'achat. Jamais de « commission » égale à ventes − achats. Une marge identique chaque mois signale des ventes calculées : cahier de ventes ou de caisse à produire. | KRA 2.2 ; KRA 2025 (ventes = achats × 1,100671 les 12 mois) |
| R19 | **Corriger l'écriture d'origine.** Un compte faux (inexistant, racine non ventilée, mauvais compte de dette), une pièce coupée en plusieurs numéros ou une écriture sans objet se corrigent par re-saisie de l'écriture d'origine (ou sa suppression), pas par un reclassement qui ferait apparaître le compte fautif. | KRA 2025 (68112, 166, 4428 ; pièces 13/75/77) |
| R20 | **CNPS : aucune écriture sans instruction expresse du Gérant.** Signaler l'absence de cotisations, ne rien passer. | Instruction du Gérant du 17/11/2026 |
| R12 | **Forme juridique respectée.** Entreprise individuelle (personne physique) : capital **103**, compte de l'exploitant **104** (1041 à 1048) viré au 103 à chaque clôture, résultat 131/139 viré au 103 à l'ouverture ; jamais 101x, 462, 465, 111, 1301/1309, pas d'AG. Société (personne morale) : capital **1011 → 1012 → 1013**, comptes courants 462, résultat 1301/1309 puis affectation par AGO ; jamais 103 ni 104. | KG Q1 (EI présentée en SARL) ; KRA (103 dans une SARL) |

---

## 2. Table des comptes — confusions interdites

Colonne de gauche : ce qu'on a écrit à tort (MDC ou clients). Colonne du milieu : le compte AUDCIF exact.

| Nature de l'opération | Compte EXACT | Faux compte déjà rencontré (et pourquoi c'est faux) |
|---|---|---|
| Taxes patronales sur salaires : contribution nationale 1,2 %, contribution employeur expatrié 9,2 % | **6413** Taxes sur appointements et salaires | 6313 = location de coffres (frais bancaires) |
| Taxe d'apprentissage 0,4 % | **6414** | 6413 (KG) ; « 6414/5 » fusionné avec la FPC (KRA) |
| Formation professionnelle continue 1,2 % | **6415** | 6413 |
| ITS retenu sur le salarié (dette) | **4472** (sous-compte 447202) | 4428, 6413 |
| CN / CE patronales (dette) | **4472** (sous-compte 447201) | 4478 |
| FDFP TA + FPC (dette) | **4478** | 4472 |
| Salaire brut personnel national | **6611** (primes 6612, transport 6634) | 401 (KRA) ; 6631 = indemnités de logement |
| Rémunération du gérant de SARL | **6611** (ou 6618 si statutaire hors contrat de travail) | 6631 (logement) |
| Rémunération de l'exploitant individuel | **6661** — ou prélèvement 104 | 661 |
| Net à payer au salarié | **422** | 401 (KRA), 421 (avances) |
| Charges sociales CNPS patronales | **6641** / dette **431x** (4311 PF, 4312 AT, 4313 retraite) — uniquement sur instruction du Gérant (R20) | 664 sans dette, 4318 |
| Prêt ou compte chez un établissement de microfinance (BAOBAB, GESCI, COFINA, ADVANS…) | **538** Autres organismes financiers, un sous-compte par établissement ; dette **162** par prêt ; intérêts **6712**, courus **1662** | 521 Banques (KRA 3.10) ; 166 non ventilé ; 671 |
| Paiement par mobile money (Wave, Orange Money, MTN, Moov), quittances e-impôts « MOB » | **552** Monnaie électronique - téléphone portable (solde débiteur ou nul) ; frais 6317 | 5211 sans relevé ; 552 créditeur |
| Ventes de marchandises d'un négociant | **7011** ; achats **6011** par facture | 7072 commission = ventes − achats (KRA 2.2) |
| Dotation aux amortissements des immobilisations corporelles | **6813** | 68112, 6811 (inexistants) |
| Loyer de bureau (charge) | **6222** Locations de bâtiments / dette **401** bailleur | 422 (KWAANI 3.1) |
| Électricité | **6052** | 624100 (624 = entretien, réparations) |
| Eau | **6051** | 624200 |
| Carburant | **6053** | 6042 |
| Fournitures de bureau non stockées | **6055** | 604000 (achats stockés) |
| Téléphone, internet, crédit de communication | **6281** / **6288** | 626000 (626 = études, documentation) |
| Commissions, tenue de compte, frais bancaires | **6318** (cartes : 6315 ; mobile money : 6317) | 629000 (n'existe pas), 6313 |
| Agios, intérêts bancaires de découvert | **6745** | 631 |
| Intérêts d'emprunt bancaire | **6712** ; intérêts courus non échus : **1662** | 631, 4486 |
| Primes d'assurance | **625x** (6251, 6252 véhicule…) ; part de N+1 → **476** | 6xx sans étalement |
| Honoraires comptable, avocat, notaire | **6324** ; frais d'actes **6325** | 622, 6328 |
| Services vendus (prestataire) | **706** (7061) | 702 = ventes de produits finis (TIM 7 n° 4) |
| Marchandises vendues | **701** | 706 |
| TEE et impôt des microentreprises (charge) — entreprises au forfait | **6418** ; dette **446** (impôts assis sur le CA) | 891, et **tout compte 89** : la classe 89 « impôts sur le résultat » est réservée au régime du réel (KG : 89000000 chez une entreprise à la TEE) |
| Patente (charge) | **6412** ; dette **4421** | dette 446 (KG : « patente transitant par 446 ») |
| Impôt foncier | **6411** ; dette **4421** | 6418 |
| Pénalités et amendes fiscales, AMR | **647x** (6471 assiette, 6473 recouvrement, 6478 autres) ; dette **4421** | 4486 charges à payer (KWAANI 3.5) |
| Impôt BIC / IMF — **régime du réel uniquement** (réel simplifié RSI, réel normal RNI) | **891** / **895** ; dette **441** | 6418 ; 89 utilisé par une entreprise au forfait (TEE, microentreprises) |
| Capital souscrit (souscription) | D **4612** / C **1011** | 4616 = versements anticipés ; 467 |
| Capital libéré | D 521 / C **4612**, puis D **1011** / C **1013** | 4611 = apports **en nature** |
| Compte courant d'associé (apport, avance, prélèvement) | **4621** Associés, comptes courants — principal ; intérêts **4626** | 4611 (apports en nature), 462100 « Le principal » utilisé comme compte d'attente (TIM 7 n° 6) |
| Prêt bloqué de l'associé (convention de blocage) | **164** Avances reçues et comptes courants bloqués | 4621 si blocage signé |
| Capital de l'entreprise individuelle (personne physique) : apports **définitifs** de l'exploitant | **103** Capital personnel | 101x, 4621 |
| Apports **temporaires** de l'exploitant en cours d'exercice (EI) | **1041** Apports temporaires | 103, 4621 |
| Prélèvements de l'exploitant (EI) : dépenses courantes, rémunération et impôts personnels, autoconsommation, retraits | **1042**, **1043**, **1047**, **1048** | 6xxx (charge), 4621 |
| Clôture de l'EI : solde net du 104 (tous sous-comptes) | viré au **103** au 31/12 (AUDCIF p. 284-286) | 104 laissé ouvert au bilan |
| Résultat de l'exercice | **131** bénéfice / **139** perte ; en instance d'affectation (société) **1301/1309** | **89** (KG : compte de classe 8 en à-nouveau) |
| Report à nouveau | **121** créditeur / **129** débiteur — **uniquement après PV d'AGO** | 121 sans PV (KWAANI 2.4, TIM 7 n° 7) |
| Réserve légale | **111** | 1111 |
| Provision pour litiges | **191** | 196 = pensions/retraite (TIM 7 n° 4) |
| Provision pour pénalités | **1981** | 4486 |
| Dépôt de garantie loyer versé | **2751** | 6222 |
| Facture non parvenue (clôture uniquement) | **408** (4081) ; TVA **4455** ; extournée au 01/01/N+1 | 408 soldé dans le même exercice (TIM 7 n° 13) |
| Charge constatée d'avance | **476** | charge pleine |
| Virement banque ↔ caisse | **585**, soldé le jour même des deux côtés | 585 non soldé, ou virement sans contrepartie au relevé (TIM 7 n° 14) |
| Loyer (charge) | **6222** | 6132 (n'existe pas ; 613 = transports pour le compte de tiers) — revue KRA |
| Carburant | **6053** | 6041 matières consommables — revue KRA |
| Entretien d'un véhicule ou d'un camion | **6242** biens mobiliers | 6241 = biens **immobiliers** — revue KRA |
| Transport et manutention sur achats | **6015** frais sur achats | 6271 = annonces, insertions (publicité) — revue KRA |
| Commissions perçues | **7072** (ou 706 si activité principale) | 7062 = services vendus **hors Région** — revue KRA |
| Mandants (ventes et achats pour compte) | **4731** Mandants | 4671 / 4672 (n'existent pas) — revue KRA |
| Autres charges externes | compte de la **nature réelle** (6381 à 6385) | 6388 (n'existe pas) ; charges forfaitaires sans pièce — revue KRA |
| Dette ITS, CN, FDFP | **447201 / 447202 / 4478** | racine 447 non ventilée — revue KRA 3.7 |
| Capital social d'une société (personne morale) | **1011 → 1012 → 1013** (1014 si amorti) | 103 = capital personnel, réservé à l'entreprise individuelle (personne physique) — revue KRA |
| Stock de marchandises | **311x**, mouvementé **uniquement** contre 6031 | 311 contre 5211/571 « affectation du financement » — revue KRA 2.1 |
| Matériel de transport | **245** ; amortissement **2845** / dotation **6813** à compter de la **mise en service** ; AIRSI **hors** coût d'entrée | dotation dès l'achat, AIRSI immobilisée (KRA 3.1) |
| Épargne nantie, dépôt à terme | **2784** / 275 | dette d'emprunt (KRA 2.3) |
| Emprunt | **162** (capital restant dû réel, attestation du prêteur) | montant nominal au lieu du capital restant dû (KRA 2.3) |

**Comptes à 6 chiffres.** Les sous-comptes Sage (447201, 521100, 4011001) sont admis **s'ils prolongent un compte AUDCIF existant à 4 chiffres** et si l'intitulé Sage reprend l'intitulé AUDCIF. Corriger les intitulés faux du plan Sage du client (KG : « 641 Rémunérations du personnel », « 41100000 Clients, dégrèvement de taxes »).

---

## 3. Schémas complets (aucune ligne raccourcie)

### 3.1 Constitution SARL, libération intégrale en numéraire (3 pièces + CCA à part)
```
CONST-1 date des statuts     D 4612 Apporteurs, apports en numéraire (un sous-compte par associé)   C 1011 Capital souscrit, non appelé
CONST-2 date du versement    D 521x Banque (ou 4732 notaire)                                         C 4612
CONST-3 même date            D 1011                                                                   C 1013 Capital souscrit, appelé, versé, non amorti
Frais de constitution        D 6325 frais d'actes / 6324 notaire / 646 droits d'enregistrement      C 401 ou 4732
Avance de l'associé (CCA)    D 521x                                                                   C 4621 Associé X, compte courant
```
Contrôle : 1013 = capital des statuts ; 1011, 4612, 4613 soldés. Le CCA n'est **jamais** dans la même pièce que le capital ; il faut le reçu ou le relevé et, si rémunéré ou bloqué, la convention.
Bilan SMT : capital en HA, CCA en HC (emprunts et dettes assimilées).

### 3.1 bis Entreprise individuelle (personne physique) — capital et compte de l'exploitant
```
Apport initial ou définitif   D 571 / 521x / 2xxx / 311x   C 103 Capital personnel
Apport temporaire en cours    D 571 / 521x                  C 1041 Apports temporaires
Dépense de l'entreprise payée sur fonds privés   D 6xxx (via 401)   …   D 401   C 1041
Retrait de fonds pour usage personnel            D 1048   C 571 / 521x
Dépense privée payée par l'entreprise            D 1042 ou 1043   C 571 / 521x   (jamais en charge)
Autoconsommation (prélèvement en nature)         D 1047   C 724 Production autoconsommée (au coût, AUDCIF p. 477 et 909)
Clôture 31/12 : chaque sous-compte du 104 (1041, 1042, 1043, 1047, 1048) soldé contre le 103 ; résultat en 131 / 139
Ouverture 01/01/N+1 : D 131 / C 103 ou D 103 / C 139
```
Pas de capital social (101x), pas de compte courant d'associé (462), pas de dividendes (465), pas de réserve légale (111), pas de 1301/1309, pas d'AG.

### 3.2 Paie, ITS et FDFP — une série de pièces par mois, copiée sur la déclaration ITS du mois

**Principe.** La déclaration ITS mensuelle e-impôts porte des lignes distinctes : ITS retenu sur les salariés,
contribution nationale (CN), contribution employeur (CE, expatriés seulement), taxe d'apprentissage (TA),
formation professionnelle continue (FPC). **Chaque ligne de la déclaration devient une ligne d'écriture, au
même montant.** On ne calcule pas un « taux global », on ne regroupe jamais deux taxes sur un même compte.

```
PAIE-1 constatation (fin de mois)
   D 6611  Salaires bruts du mois (un libellé par salarié ou livre de paie joint)
      C 447202  ITS retenu sur salaires (ligne « ITS » de la déclaration ; 0 si brut ≤ 75 000)
      C 4313    CNPS part salariale 6,3 % (si immatriculé)
      C 422xxx  Net à payer, un compte par salarié
PAIE-2 taxes patronales (même date)
   D 6413  Contribution nationale 1,2 %          C 447201
   D 6413  Contribution employeur 9,2 % (expatrié uniquement)   C 447201
   D 6414  Taxe d'apprentissage 0,4 %            C 4478
   D 6415  Formation professionnelle continue    C 4478   (montant de la ligne FPC de la déclaration)
PAIE-3 CNPS patronale   D 6641   C 4311 / 4312 / 4313
PAIE-4 paiement du net  D 422xxx C 521x ou 571   (date du virement ou de la décharge)
PAIE-5 paiement ITS     D 447202 + 447201 + 4478   C 521x   date de la QUITTANCE, référence e-impôts dans le libellé
PAIE-6 paiement CNPS    D 431x   C 521x            date de la quittance CNPS
```

**Exemple FAMILLE KRA** (2 salariés à 75 000, brut 150 000/mois, versement e-impôts 4 200/mois) :

| Compte | Libellé | Débit | Crédit |
|---|---|---|---|
| 6611 | Salaires bruts janvier 2025 — 2 salariés | 150 000 | |
| 447202 | ITS retenu janvier (brut ≤ 75 000 par salarié) | | 0 |
| 422 | Net à payer janvier | | 150 000 |
| 6413 | Contribution nationale 1,2 % janvier | 1 800 | |
| 447201 | CN janvier à payer | | 1 800 |
| 6414 | Taxe d'apprentissage 0,4 % janvier | 600 | |
| 6415 | Formation professionnelle continue 1,2 % janvier | 1 800 | |
| 4478 | FDFP janvier à payer | | 2 400 |

Puis, à la date de chaque quittance : D 447201 1 800 + D 4478 2 400 / C 5211 4 200.

**Les fautes relevées par la réviseuse (KRA 3.6 et 3.7), à ne jamais reproduire :**
- salaires portés en 401, ou en 661 réglés directement en caisse sans 422 ni retenue ;
- « 6414/5 » : deux comptes fusionnés en un, ce qui n'est pas un numéro de compte ;
- FDFP à 1 % (ancien taux) et contribution nationale oubliée ;
- 2,8 % passés entièrement en 6413 sous le libellé « CE et CN » (pas de CE pour le personnel local) ;
- dette laissée sur la racine 447, sans sous-compte ;
- paiements regroupés au 30/12, ou absents, au lieu d'un paiement par quittance : la comptabilité affichait
  29 400 F de dette contre 16 800 F réellement dus.

**Tableau obligatoire (joint à chaque dossier)** : mois / brut / ITS / CN / TA / FPC / total déclaré /
date et référence du paiement / reste dû. Le total « reste dû » est le solde de 447201 + 447202 + 4478 au 31/12.
Le taux de FPC mensuel dépend de la déclaration (1,2 % chez KRA ; 0,6 % par mois + 0,6 % régularisés en
fin d'année dans d'autres dossiers) : **reprendre la déclaration**, et vérifier les taux de la période dans
`../fiscalite-ci/reference/TAUX_ET_SEUILS.md`.
**Concordance** : Σ 6611 = livre de paie = État 301 = assiette des déclarations ITS (TIM 7 n° 17).
**Sans n° CNPS, le visa est refusé** : réclamer l'immatriculation en premier.

### 3.3 Impôts et taxes (charge à l'émission, paiement à la quittance)
```
TEE mensuelle         D 6418   C 446      (montant de l'avis, mois par mois)
Patente               D 6412   C 4421     (avis d'imposition)
Impôt foncier         D 6411   C 4421     (avis de l'année N uniquement)
AMR / pénalités       D 647x   C 4421     (exercice de la période rappelée ou de la notification)
BIC / IMF             D 891 / 895   C 441   (RÉEL uniquement ; au forfait — TEE, microentreprises — aucun compte 89 : impôt en 6418 / 446)
Paiement              D 446 / 4421 / 441   C 521x ou 571   (date et référence de la quittance)
```
Impôt de N-1 payé en N : dette dans les à-nouveaux de N, réglée en N. **Jamais** en charge de N.

**Impôt sur le résultat d'un exercice antérieur (régime du réel uniquement), découvert ou payé en N :**

| Situation | Écriture | Fondement |
|---|---|---|
| Impôt dû à la clôture N-1 mais oublié (erreur), montant **significatif** | D 129 (ou diminution du 121) / C 441, à l'ouverture ou dès la découverte ; **mention en note 2** (correction d'erreur) | AUDCIF art. 20 ; admis par la réviseuse (TIM 7 n° 8 : BIC 2024 de 8 000 000 payé en 2025) |
| Rappel né d'un contrôle, d'un avis ou d'un fait nouveau, ou erreur **non significative** | D 892 Rappel d'impôts sur résultats antérieurs / C 441 | Plan AUDCIF 892 ; cadre conceptuel p. 92 |
| Dégrèvement ou annulation d'un impôt antérieur | D 441 / C 899 | Plan AUDCIF 899 |

Jamais en 891 de l'exercice, qui ne reçoit que l'impôt de l'année. Au forfait (TEE, microentreprises), ni 89 ni 892 : un rappel de TEE va en 6418 (et ses pénalités en 647x), rattaché selon §1 R6 (KRA 2.5).

### 3.4 Achats et ventes
```
Facture fournisseur   D 6xxx (nature exacte) + 4452 TVA si facture normalisée (FNE)   C 4011xxx Fournisseur nommé
Règlement             D 4011xxx                                                      C 521x / 571
Facture client        D 4111xxx Client nommé    C 7061 (services) ou 701 (marchandises) + 4432/4431 TVA
Encaissement          D 521x / 571              C 4111xxx       (un encaissement = un règlement de facture identifiée)
```
Reçu de station, ticket sans NCC : pas de TVA déductible, charge seule. Facture non nominative : charge non déductible à signaler.

### 3.5 Trésorerie
```
Frais bancaires mensuels   D 6318 (6315 cartes)   C 521x       (un par mois, au relevé)
Agios                      D 6745                  C 521x
Retrait banque → caisse    D 585  C 521x   puis   D 571  C 585   (les deux le même jour ; le retrait figure au relevé)
Dépense personnelle du gérant payée par la société   D 4621 Associé   C 521x / 571   (jamais en charge)
Échéance d'emprunt         D 162 (capital) + D 6712 (intérêts)   C 521x
Placement / épargne        D 2784 ou 50x   C 521x
```

### 3.6 Clôture
```
Facture non parvenue       D 6xxx + 4455   C 4081      → extourne au 01/01/N+1
Charge constatée d'avance  D 476            C 6xxx      → extourne au 01/01/N+1
Intérêts courus            D 6712           C 1662
Dotation amortissement     D 6813           C 284x      (prorata depuis la mise en service)
Résultat                   solde des classes 6 et 7 → 131 / 139
EI, compte de l'exploitant apports nets (104 créditeur) : D 1041…1048   C 103
                           retraits nets (104 débiteur) :  D 103   C 1041…1048   (le 104 est soldé, AUDCIF p. 284-286)
```

### 3.7 À-nouveaux et affectation
```
À-nouveaux (journal AN, 01/01/N)   reprise ligne à ligne du bilan N-1 visé (classes 1 à 5 uniquement)
Affectation (société, date du PV d'AGO)   D 1301   C 111 (10 % jusqu'à 20 % du capital) / 121 / 465
                                            perte : D 129   C 1309
EI : au 31/12/N-1                    104 (tous sous-comptes) soldé dans le 103 (§3.6)
EI : au 01/01/N                      D 131   C 103   (bénéfice N-1)   ou   D 103   C 139   (perte N-1)
                                     Les à-nouveaux d'une EI ne contiennent donc jamais de 104 ni, après affectation, de 131/139.
```
Sans PV d'AGO, le résultat N-1 reste en 1301/1309 et la pièce est réclamée.

**Résultat ancien non affecté trouvé à l'ouverture** (revue KG : 1 901 950 F laissés en 89000000) :
- Entreprise individuelle : le reclasser au **103** (D 131 / C 103 ou D 103 / C 139 ; un solde trouvé en 89, 12 ou 13 se reclasse de la même façon au 103). Il n'y a ni AG ni report à nouveau à attendre.
- Société : le porter en **1301 / 1309** jusqu'à l'AGO, puis affecter par PV.
- Dans les deux cas : le montant doit égaler le résultat des EF N-1 visés ; sinon c'est une erreur d'à-nouveau (R7) à corriger et à mentionner en note 2.
- Ne **jamais** le faire disparaître dans la liasse par une « variation de dettes » (ligne VC du SMT) : c'est ce qui a faussé le résultat déclaré de KG (−668 752 au lieu de −2 570 702).

### 3.8 Stocks de marchandises (inventaire intermittent) — cas FAMILLE KRA

**Un stock ne naît que d'achats facturés et ne se constate qu'à l'inventaire.**
```
Achat de marchandises   D 6011 (+ 4452 si FNE)   C 4011xxx Fournisseur nommé   (facture)
Frais sur achats        D 6015 (transport, manutention, transit)   C 4011xxx
Vente de marchandises   D 4111xxx Client nommé    C 7011 (+ 4431)
Clôture, stock initial  D 6031   C 311x     (annule le stock d'ouverture, montant des à-nouveaux)
Clôture, stock final    D 311x   C 6031     (montant du PV d'inventaire valorisé au coût d'achat)
Dépréciation            D 6593   C 391x     (articles abîmés, périmés, invendables)
```
Interdits (revue KRA 2.1 et 2.2) :
- **D 311 / C 5211 / C 571 « affectation du financement en stock »** : la trésorerie ne se transforme pas
  en stock par une écriture. Si l'argent a payé des marchandises, ce sont des achats (601) sur facture ;
  sinon il est ailleurs (prélèvement de l'associé, prêt, dépense non justifiée) et il faut le dire.
- Stock final à 0, ou au montant « qui équilibre », sans PV d'inventaire.
- Stock au bilan sans aucun achat 601 dans l'année.
- Achats et ventes « pour compte de mandants » sans contrat de mandat : si FAMILLE KRA vend en son nom
  (DFE et RCCM : vente en gros et demi-gros), le chiffre d'affaires est la vente totale (701), pas la seule commission.
  Si le mandat est réel et prouvé : comptes 4731 Mandants (4671/4672 n'existent pas), commission en 7072
  (ou 706 si c'est l'activité principale), et les marchandises des mandants ne sont pas dans le stock 31.

Pièces exigées à la clôture : PV d'inventaire au 31/12 signé (date, lieu, inventoriste), fiche par article
(quantité × coût unitaire), factures d'achat justifiant les coûts, et rapprochement :
**stock initial + achats − stock final = coût d'achat des marchandises vendues**, comparé au chiffre d'affaires
(marge cohérente avec l'activité).

---

## 4. Grille de rapprochements à remplir avant toute remise

Chaque ligne : montant comptable, montant de la pièce externe, écart, explication. Écart non expliqué = blocage.

| N° | Rapprochement | Pièce externe |
|---|---|---|
| G1 | À-nouveaux 01/01/N = bilan N-1 visé, compte par compte | Liasse N-1 visée |
| G2 | Solde banque au 31/12 (chaque banque) = relevé ± suspens | Relevé complet (toutes les pages) + état de rapprochement |
| G3 | Solde caisse au 31/12 = PV de caisse ; aucune date à solde créditeur | PV de caisse, brouillard |
| G4 | Paiements à l'État de l'année = historique e-impôts, ligne à ligne | Historique e-impôts |
| G5 | Charge TEE / patente / foncier = avis émis pour N | Avis d'imposition |
| G6 | Taxes sur salaires (6413+6414+6415) = déclarations ITS/FDFP de N | Déclarations ITS, État 301 |
| G7 | Salaires 6611 = livre de paie = État 301 = DISA | Livre de paie, DISA |
| G8 | Cotisations CNPS comptabilisées = déclarations CNPS | Déclarations, quittances CNPS |
| G9 | CA comptabilisé = factures émises = encaissements identifiés | Factures, relevé |
| G10 | Emprunts = capital restant dû attesté par le prêteur | Échéancier, attestation |
| G11 | Capital 1013 = statuts ; CCA 4621 = reçus et relevés | Statuts, relevé |
| G12 | Comptes 47x, 585, 408 de N-1 : soldés | Balance |

Pour TEE + ITS/FDFP, présenter le tableau des réviseurs : impôt / période / date / payé e-impôts / comptabilisé / écart.

---

## 5. Contrôle automatique (obligatoire)

```bash
python3 ~/.claude/skills/mdc/modules/ecritures-sans-faute/scripts/controle_ecritures.py ECRITURES.csv --exercice 2025 --forme SARL --regime TEE
```
Entrée : CSV ou XLSX avec les colonnes `journal, date, piece, compte, libelle, debit, credit` (colonne `tiers` facultative).
Formes : `SARL`, `SA`, `SAS`, `SNC` (sociétés) ou `EI` (entreprise individuelle).
Régimes (`--regime`) : `TEE` et `RME` (forfait), `RSI` (réel simplifié), `RNI` (réel normal). Au forfait (TEE et RME), tout compte 89 est bloqué.
Le script vérifie : équilibre par pièce et global ; existence de chaque compte dans le plan AUDCIF ;
confusions de la table §2 (par mot-clé du libellé) ; deux temps ; écritures globales au 31/12 ;
tiers anonymes ; dates hors exercice ; à-nouveaux (classes 6-8, dates) ; caisse créditrice ;
comptes d'attente non soldés ; 408 soldé dans l'exercice ; capital non libéré ; comptes interdits selon la forme juridique ; **paie mois par mois** (422 crédité, CN, TA et FPC présentes et ventilées, taux global en 6413, paiements ITS/FDFP) ; **stocks** (31 mouvementé hors 6031, stock sans achats, stock initial non soldé, stock final sans inventaire) ; comptes racines non ventilés (447, 442, 661, 681, 166).
Sortie : liste des **ERREURS** (bloquantes) et **ALERTES** (à justifier), code retour 1 s'il reste une erreur.
Option `--regularisations` : pour un fichier ne contenant que des écritures correctives (pas de contrôle d'écritures globales ni de paie mensuelle). Les lignes de contrepartie sans date ni pièce reprennent celles de la ligne précédente.

Les écritures générées par un script Python doivent être exportées en CSV et passées au contrôle **avant** la création du PDF ou du fichier Sage.

Ensuite, second regard obligatoire : module `auditeur-comptable` (`audit_comptable.py tout …`), qui reprend ce contrôle et y ajoute les principes comptables et les mises à jour.

---

## 6. Pièces à réclamer d'emblée (préalables au visa)

Sans elles, le réviseur rejette, quelle que soit la qualité des écritures :
notification d'immatriculation **CNPS** (dès le premier salarié) · extrait **RCCM** · **DFE** · statuts ·
**PV d'AGO** approuvant les comptes N-1 et affectant le résultat · liasse N-1 visée · relevés bancaires
**complets** · PV de caisse au 31/12 · factures d'achat et de vente nominatives · contrats (bail, prêt,
mandat, assurance) · livre de paie, bulletins, État 301, DISA · avis TEE, patente, foncier, AMR ·
historique des paiements e-impôts.

Dans la liasse SMT : fiche R1 (IDU, n° CNPS, date de signature), R2 (forme juridique, première année
d'activité), R3 (qualité du dirigeant) ; Note 2 renseignée (continuité, baisse d'activité, capitaux propres
négatifs, corrections d'erreurs) ; colonne N-1 remplie.

---

## 7. Format de l'ordre de saisie Sage

Colonnes : `Journal | Date | N° pièce | Compte | Compte tiers | Libellé | Débit | Crédit | Pièce justificative`.
Journaux : AN (à-nouveaux), ACH, VTE, BQ1/BQ2 (un par banque), CAIS, PAIE, OD.
Libellé = nature + tiers + période (« Loyer novembre 2025 — SCI X »). Une pièce = une opération justifiée.
Joindre en dernière page le résultat du contrôle automatique et la grille §4.

---

## 8. Répondre à une note de revue et passer les régularisations

1. **Tableau de traitement**, une ligne par point de la note : référence, observation, analyse, traitement
   (pièce à fournir / écriture corrective / justification / désaccord argumenté avec texte à l'appui), qui, bloquant ou non, statut.
2. **Classer chaque point** : préalable au visa (CNPS, RCCM, DFE, PV d'AGO) ; pièce manquante ; correction comptable ;
   point qui dépend d'une pièce (à ne pas passer tant que la pièce n'est pas reçue, ou à passer en « conditionnel »).
3. **Écritures correctives** selon les schémas §3 :
   - erreur de l'exercice en cours : annulation de l'écriture fausse puis enregistrement exact (AUDCIF art. 20) ;
   - erreur significative d'un exercice antérieur : par le report à nouveau (société) ou le 103 (EI), mention en note 2 ;
   - à-nouveaux faux : corriger le journal d'à-nouveaux lui-même (classes 1 à 5), jamais par une écriture d'à-nouveau en 89 ou en classe 6-7.
4. **Contrôle** des seules écritures correctives :
   `controle_ecritures.py REGUL.csv --exercice 2025 --forme EI --regime TEE --regularisations`,
   puis contrôle du **journal complet corrigé** sans l'option.
5. **Résultat corrigé** : recalculer et rapprocher du chiffre indicatif de la réviseuse (ex. KRA ≈ 5 533 276 ; KG −2 525 290) ;
   expliquer tout écart.
6. **Liasse corrigée** : même résultat que la comptabilité, colonne N-1, fiche R1/R2/R3, note 2 (corrections d'erreurs, continuité).

## 9. Référence

- Catalogue détaillé des observations des réviseurs et de leur traduction en règles : `reference/CATALOGUE_NOTES_DE_REVUE.md`.
- Plan AUDCIF complet : `../mdc-expert/reference/PLAN_COMPTABLE_OHADA_COMPLET.md`.
- Taux : `../fiscalite-ci/reference/TAUX_ET_SEUILS.md`.
