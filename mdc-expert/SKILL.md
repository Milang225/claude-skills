---
name: mdc-expert
description: >
  Expert global MDC (La Maison de la Conformité SARL) — comptabilité SYSCOHADA/OHADA
  pour la Côte d'Ivoire et zone UEMOA, analyse de relevés bancaires, audit global,
  révision/certification de comptes, gestion du VPS Contabo, ET PRODUCTION DE TOUS
  LES DOCUMENTS COMMERCIAUX MDC (note méthodologique, proposition financière, proposition
  commerciale, contrat de prestation). Déclenche ce skill dès que l'utilisateur parle de :
  comptabilité, écritures, journal, balance, grand livre, bilan, compte de résultat,
  liasse fiscale, clôture, report à nouveau, affectation, SYSCOHADA, OHADA, SMT, SMN,
  personne physique/morale, PP/PM/EI, SARL/SA/SAS/SCI, TEE, Impôt Synthétique, ITS,
  FDFP, Patente, TVA, IBIC, pénalités fiscales, e-impots ; relevé bancaire, extrait de
  compte, mouvements bancaires, crédits/débits, chiffre d'affaires, catégoriser les
  opérations ; audit global, rapport d'audit, grille de notation, rapport final, auditer ;
  visa, certification, contrôle qualité, revue des comptes, vérifier les écritures,
  valider le rapport, contrôle interne, révision comptable ; serveur, VPS, déployer,
  SSH, Contabo ; note méthodologique, note methodo, proposition financière, proposition
  commerciale, contrat de prestation, faire une propale, rédiger une note, faire le doc
  pour un client, préparer un dossier client, fais-moi une note pour, fais-moi une
  proposition pour, quel est le tarif, prix pour l'audit, montant mission ;
  télédéclaration e-impôts, EDI, EFI, remplir une déclaration, déclaration mensuelle,
  fais-moi la déclaration TVA/ITS/TSE/RIBIC/RIBNC/AIRSI/patente de tel mois, formulaire
  e-impôts rempli, bordereau de déclaration, calendrier fiscal, échéance de déclaration,
  annexe détaillée, État 301/302, générer le XML de déclaration, moteur de déclarations.
---

# MDC Expert — Compétence Globale La Maison de la Conformité SARL

Expert unifié regroupant 5 domaines : comptabilité SYSCOHADA, analyse bancaire,
audit global, révision/certification, et administration serveur.

---

## SOMMAIRE

1. [Comptabilité SYSCOHADA / OHADA](#1-comptabilité-syscohada--ohada)
2. [Analyse de Relevés Bancaires](#2-analyse-de-relevés-bancaires)
3. [Audit Global (Rapport Final)](#3-audit-global-rapport-final)
4. [Auditeur & Contrôleur de Comptes](#4-auditeur--contrôleur-de-comptes)
5. [SSH VPS Contabo](#5-ssh-vps-contabo)
6. [Production de Documents Commerciaux MDC](#6-production-de-documents-commerciaux-mdc)

---

## IDENTITÉ MDC (toujours inclure dans les rapports officiels)

> **⚠️ RÈGLE TERMINOLOGIQUE ABSOLUE — Décision client juin 2026**
> Dans TOUS les documents MDC produits (notes, propositions, contrats, rapports, mémoires, e-mails),
> remplacer systématiquement le mot **« Cabinet »** par **« Agence »**.
> Exemples : « Agence MDC », « notre Agence », « l'Agence d'Audit », « Agence de Conformité ».
> Aucune exception. À appliquer rétroactivement à tous les modèles et templates.

> **⚠️ RÈGLE D'IDENTITÉ ABSOLUE — Décision gérant juillet 2026**
> MDC est une **AGENCE DE NOTATION ADMINISTRATIVE couvrant les volets comptable, fiscal et social**.
> MDC ne fait PAS d'expertise comptable et ne doit JAMAIS se présenter comme « cabinet/agence d'expertise comptable »,
> « expert-comptable » ou toute formulation évoquant la profession réglementée d'expertise comptable (risque d'exercice illégal).
> Sous-titre officiel de l'en-tête de TOUS les livrables : **« Agence de Notation Administrative — Comptable · Fiscal · Social »**
> (déjà intégré aux générateurs build_mdc_pdf.py, build_mdc_docx_hf.py, generate_livrable_mdc.py, md_to_docx_mdc.py — correctif juillet 2026).
> Vérifier aussi docgen.js (CRM VPS) et tout template avant réutilisation. Toute mention contraire dans un document existant doit être corrigée avant envoi.

- **LA MAISON DE LA CONFORMITE SARL**
- NCC : 2506426B
- RCCM : CI-ABJ-03-2025-B13-10831
- Capital : 1 000 000 FCFA
- Gérant : M. BILE FILS SEVERIN
- Email : lamaisondelaconformitesarl@outlook.com
- Gmail : lamaisondelaconformite@gmail.com
- Tél : +225 07 19 31 49 04
- Site : www.lamaisondelaconformitesarl.net

---

# 1. COMPTABILITÉ SYSCOHADA / OHADA

Expert-comptable SYSCOHADA/OHADA pour la Côte d'Ivoire et la zone UEMOA.

## RÈGLE CRITIQUE : Équilibre de toute écriture
**JAMAIS** valider une écriture comptable déséquilibrée :
- Somme des débits = Somme des crédits (tolérance 0,01)
- Toute balance d'un exercice doit être équilibrée avant clôture

## Différences PP vs PM

### Personne Physique (PP / EI / Entreprise Individuelle)
- **PAS de capital social** (ni 101xxx)
- **Apport du gérant** : D 571000 (Caisse) / C **104000** (Compte de l'exploitant)
- **Retrait du gérant** : D 104000 / C 571000
- **Résultat** : compte **103000** uniquement (PAS 130100/130900)
  - Perte → 103000 débiteur
  - Bénéfice → 103000 créditeur
- **PAS d'AG, PAS d'affectation formelle**

### Personne Morale (PM / Société)
- **Capital social** : 101000
- **Résultat en instance d'affectation** : 130100 (bénéfice) / 130900 (perte)
- **Après AG** : 111100 (réserve légale) / 111800 (autres réserves) / 465000 (dividendes) / 121000 (RAN+) / 129000 (RAN-)

## Plan comptable SYSCOHADA — Comptes essentiels

### Classe 1 — Capitaux
| Compte | Libellé | Notes |
|--------|---------|-------|
| 101000 | Capital social | PM |
| 102000 | Capital personnel | PP déclaré |
| 103000 | Résultat exercice (exploitant) | **PP** |
| 104000 | Compte de l'exploitant | PP — apports/retraits |
| 111100 / 111800 | Réserves | PM |
| 121000 / 129000 | RAN+ / RAN- | PM |
| 130100 / 130900 | Résultat bénéfice / perte | **PM** |
| 162000 | Emprunts bancaires | |

### Classe 2 — Immobilisations : 201100, 211000, 231000, 241000, 245000, 281xxx

### Classe 4 — Tiers
| Compte | Libellé |
|--------|---------|
| 401000 | Fournisseurs |
| 411000 | Clients |
| 421000 | Personnel - Avances |
| 422000 | Personnel - Rémunérations dues (net à payer) |
| 431000 | CNPS |
| 447100 | État - IBIC |
| **447201** | **État - Contribution Employeur (CE + CN) patronale** |
| **447202** | **État - ITS retenu sur salaire (part salariale)** |
| 4478 | État - Autres impôts et taxes (FDFP, TEE, Patente, pénalités) |
| 465000 | Associés - Dividendes |

### Classe 5 — Trésorerie : 521000 (Banque), 571000 (Caisse)

### Classe 6 — Charges
| Compte | Libellé |
|--------|---------|
| 601000 | Achats marchandises |
| 622000 | Locations |
| **6313** | **Impôts sur salaires - Charges patronales (CE + CN)** |
| **6418** | **Autres impôts et taxes directs — TEE** |
| **6414** | **FDFP - Taxe d'Apprentissage (0,40%)** |
| **6415** | **FDFP - Taxe Formation Professionnelle Continue (0,60%)** |
| 647xxx | Pénalités fiscales |
| 661000 | Rémunérations personnel (salaire brut) |

### Classe 7 — Produits : 701000, 706000, 707000

## Schémas d'écritures types

### Apport initial du gérant (PP)
```
D 571000 / C 104000
```

### Salaire mensuel complet (Côte d'Ivoire — confirmé DGI ITS)

**Pièce 1 — Rémunération + retenue salariale (ITS salarié) :**
```
D 661000  Salaire brut                        60 000
  C 422000  Salaire net à payer à l'employé    (60 000 − ITS salarié)
  C 447202  ITS retenu sur salaire              X (barème progressif − RICF)
```

**Pièce 2 — Charges patronales CN (+ CE si expatrié) :**
```
D 6413    Taxes sur appointements et salaires          CN 1,2% × brut (+ CE 9,2% si expatrié)
  C 447201  Contribution Nationale (+ Contribution Employeur) à payer
```
> **⚠️ GRILLE DES CHARGES PATRONALES — DGI 2025 (fait foi ; cf. `reference/FICHE_SYNOPTIQUE_CALENDRIER_DGI.md`) :**
> | Contribution | **Local** | **Expatrié** | Réf. |
> |---|---|---|---|
> | **CE** (Contribution Employeur proprement dite) | **exonéré (0 %)** | **9,2 %** | Art. 134-135, 146 |
> | **CN** (Contribution Nationale) | **1,2 %** | 1,2 % | Art. 146 |
> | **TA** (apprentissage, FDFP) | **0,4 %** | 0,4 % | Art. 143, 146 |
> | **TFPC** (formation continue, FDFP) | **1,2 %** | 1,2 % | Art. 146 |
> | **TOTAL patronal** | **2,8 %** | **12 %** | |

> **✅ CONTROVERSE KRA TRANCHÉE (Synoptique DGI, Édition AF 2025, pp. 19-22)** : pour le **personnel local**, la **CE proprement dite est EXONÉRÉE** ; seul l'expatrié la supporte à **9,2 %**. Le total patronal local = **2,8 %** = CN 1,2 % + TA 0,4 % + TFPC 1,2 % (donc **FDFP local = 1,6 %**, pas 1 %). ⇒ L'ancienne lecture « CE local 2,8 % + CN 1,2 % = **4 %** » était **fausse** (double compte). La **CN est bien une charge patronale** de 1,2 % (non un impôt salarial). ⇒ L'inférence masse salariale = versement ITS ÷ **2,8 %** est **confirmée** (cas KRA : 4 200 ÷ 2,8 % = 150 000 = 2 × SMIG). Cf. §27.3. Compte de charge : **6413 « Taxes sur appointements et salaires »** (SYSCOHADA strict) ; contrepartie 447201.

**Pièce 3 — FDFP (1,6 % du brut, charge patronale) :**
```
D 6414    FDFP - Taxe d'Apprentissage (TA)             0,40% × brut
D 6415    FDFP - Formation Professionnelle (TFPC)      1,20% × brut
  C 4478   État - FDFP à payer                          1,60% × brut
```
- **TA** : **0,4 %** du brut (Art. 143, 146) → compte 6414.
- **TFPC** : **1,2 %** du brut (Art. 146 ; Décret 92-529) → compte 6415. *En pratique, avance mensuelle + régularisation en fin d'exercice ; la DGI publie le taux statutaire 1,2 %.*

**Pièce 4 — Charges CNPS patronale + retenue salariale (si applicable) :**
```
D 664xxx  Charges CNPS patronales
  C 422000  (diminution du net — retenue CNPS salariale ~6,3%)
  C 431xxx  CNPS à payer (patronale + salariale)
```

### Barème ITS salarié (Art. 115-120 CGI) — **retenue à la source par l'employeur**
**ITS = IB (barème progressif) − RICF.** Barème **mensuel** (Art. 116) :
| Tranche mensuelle (F) | Taux |
|---|---|
| 0 – 75 000 | **0 %** |
| 75 001 – 240 000 | 16 % |
| 240 001 – 800 000 | 21 % |
| 800 001 – 2 400 000 | 24 % |
| 2 400 001 – 8 000 000 | 28 % |
| > 8 000 000 | 32 % |

**RICF (Art. 119 bis)** — réduction mensuelle selon les parts : 1 → 0 · 1,5 → 5 500 · 2 → 11 000 · 2,5 → 16 500 · 3 → 22 000 · 3,5 → 27 500 · 4 → 33 000 · 4,5 → 38 500 · 5 → 44 000.
- **Salarié ≤ 75 000/mois → ITS salarial = 0** (mais CN + FDFP patronaux, soit 2,8 % local, restent dus).
- Retraités > 70 ans : abattement **75 %** après RICF (Art. 120). Dockers/dockers-transit : **1,5 %** (Art. 120).
- Exonération totale : salariés agricoles agro-industriels des catégories Art. 147-148 CGI.
> Détail complet (tranches, RICF, exonérations, délais de déclaration) : `reference/FICHE_SYNOPTIQUE_CALENDRIER_DGI.md`.

### Loyer mensuel (non payé)
```
D 622000 / C 401000
```

### TEE / Impôt Synthétique (format Sage)
```
D 6418 - Autres impôts et taxes directs
  C 446  - État, Autres taxes sur le chiffre d'affaires
```

### Paiement d'un impôt (sortie caisse)
```
D 447x00 / C 571000 (ou 521000)
```

### Constitution PM (SARL/SA) — 3 pièces
1. Souscription : D 467xxx / C 101000
2. Libération : D 521000/571000 / C 467xxx
3. Frais : D 201100 + D 445600 / C 401000/521000

### Constitution PP/EI — 1 pièce
```
D 571000 / C 104000
```

## Processus de clôture

1. **Vérifier équilibre** : ∑D = ∑C à 0,01 près
2. **Solder classes 6 et 7** vers 103000 (PP) ou 130100/130900 (PM)
3. **Calculer résultat** = Σ(7xxx) - Σ(6xxx)
4. **Marquer exercice CLOTURÉ**
5. **Générer AN (à-nouveaux)** dans N+1 pour classes 1-5 au 01/01/N+1
6. **Affectation du résultat (PM uniquement)** après AG

## Fiscalité ivoirienne

| Nature | Libellé | Périodicité | Charge | Dette |
|--------|---------|-------------|--------|-------|
| TEE | Taxe État Entreprenant (ex-Impôt Synthétique) | Mensuelle | 6418 | 446 |
| ITS | Impôts Traitements et Salaires | Mensuelle | retenue | 447200 |
| FDFP | Formation Professionnelle | Mensuelle | 6414/6415 | 447400 |
| PATENTE | Contribution Patentes | Annuelle | 6412 | 446 |
| TVA | Taxe Valeur Ajoutée | Mensuelle | — | 447500 |
| IBIC | Impôt sur Bénéfices | Annuelle | 891000 | 447100 |
| PÉNALITÉ | Amendes fiscales | Ponctuelle | 647xxx | 446 |

## Analyse e-impots.gouv.ci

**Principe fondamental : 1 ligne = 1 mois d'impôt individuel**
- Format : `NATURE | Mois Année | Montant | Date paiement | Référence`
- Exemple : `TEE | Juillet 2019 | 25 025 | 23/05/2022 | ESP2205231570`
- **Séparation charge/paiement** : charge dans l'année de constatation, paiement dans l'année de sortie effective d'argent. **NE JAMAIS** inclure dans l'exercice N un paiement de N+1.

## Validation finale d'un dossier comptable
1. ✅ Tous exercices équilibrés (D=C à 0,01)
2. ✅ Classes 6/7 soldées dans exercices clôturés
3. ✅ AN correctement portés en N+1
4. ✅ Paiements dans le bon exercice
5. ✅ Bilan équilibré (Actif = Passif)
6. ✅ Résultat CR = Résultat exercice
7. ✅ PP : pas de 130xxx
8. ✅ PM : classe 130 fermée après affectation

## PROCÉDURE MDC OFFICIELLE — 2 TYPES DE MISSIONS

### MISSION TYPE 1 — Création d'une comptabilité from scratch
**Contexte** : Client sans aucune comptabilité tenue. On part de zéro : collecte des opérations, création du plan comptable, passation des écritures, production des états et liasse.

**Déroulé** :
1. Collecte documentaire (pièces, relevés bancaires, factures, bulletins)
2. Création du plan comptable SYSCOHADA adapté au secteur
3. Saisie chronologique dans les journaux auxiliaires :
   - **RAN** (Report à nouveau) — reprise bilan
   - **CAIS** (Caisse) — opérations cash
   - **BQ** (Banque) — opérations bancaires
   - **ACH** (Achats) — factures fournisseurs
   - **VTE** (Ventes) — factures clients
   - **OD** (Opérations Diverses) — régularisations, charges, impôts
4. Production Balance → Grand Livre → Journal général
5. Établissement Bilan + Compte de Résultat + Liasse DGI (SMT ou SN)
6. Calcul du **Report à Nouveau** par exercice avec clôture séquentielle

### MISSION TYPE 2 — Audit + Reconstitution + Régularisations
**Contexte** : Client avec liasse fiscale existante mais anormale/incomplète. On détecte les anomalies, on reconstitue la comptabilité, on propose les régularisations, puis on certifie.

**3 livrables standardisés MDC** :

#### Livrable A : `Dossier_Audit_<CLIENT>_<ANNEE>.xlsx` — 5 AXES

1. **AXE I — Audit Documentaire** (Partie A Infos préliminaires A1-A20, Partie B Inventaire B1-B52, Partie C Questionnaire dirigeant C1-C45)
2. **AXE II — Cadrage Réglementaire** :
   - 2.1 Grille régimes fiscaux CI (par CA TTC — **grille officielle DGI/AF 2025**, cf. `reference/FICHE_SYNOPTIQUE_CALENDRIER_DGI.md`) : **TCE** ≤5M (2%/2,5%), **TEE** ]5M–50M] (4% commerce/5% autres), **RME/IME** ]50M–200M] (6%, 4% si CGA), **RSI** ]200M–500M] (I-BIC 25%+IMF), **RNI** >500M (I-BIC 25%+IMF). Seuil assujettissement TVA de plein droit = 200M.
   - 2.2 Obligations fiscales selon régime
   - 2.3 Calcul cotisations CNPS CI 2024 (8 branches, plafonds)
3. **AXE III — Matrices Anomalies** (4 matrices) :
   - 3.1 Anomalies comptables SYSCOHADA (codes P-x Passif, A-x Actif, R-x Résultat, T-x Trésorerie, N-x Notes)
   - 3.2 Anomalies fiscales (codes F-x)
   - 3.3 Anomalies sociales (codes S-x)
   - 3.4 Audit croisé inter-disciplinaire
4. **AXE IV — Logique Financière** :
   - 4.0 Données clés N vs N-1
   - 4.1 Analyse cohérence (10 indicateurs : équilibre bilan, marge brute, ratios)
   - 4.2 Diagnostic continuité AUPCAP art. 25 (cessation paiements si ratio < seuil)
5. **AXE V — Passif & Plan d'Action** :
   - 5.1 Chiffrage consolidé passif conformité
   - 5.2 Grille scores (6 domaines /10)
   - 5.3 Plan 15 actions (URGENT/PRIORITAIRE/NORMAL)

#### Livrable B : `Rapport_Anomalies_<CLIENT>_<ANNEE>.xlsx` — 6 onglets

1. **RAPPORT** — Synthèse exécutive : infos mission, tableau de bord passif (critiques/majeures/mineures), score /10, navigation
2. **① SAISIE** — Feuille de saisie liasse SMT/SN (codes AI/GA/AC/AZ/BK/BS/BZ/CA/CJ/DZ/TA/RA/XA/XC/XD/XE/XI/KZC avec formules `=IFERROR(...)`)
3. **② ANOMALIES** — **Moteur 22 tests** (7 familles) :
   - Équilibre : T1 Actif=Passif, T2 Résultat bilan=CR
   - Capital/tréso : T3 Banque>Capital+CA, T4 Reconstitution banque, T5 tréso négative
   - Fournisseurs : T6 Dettes>CA, T7 délai 30-90j, T8 **Triangle CMV**
   - Stocks : T9 Variation stocks, T10 stock>6 mois
   - Clients : T11 Créances>CA, T12 délai recouvrement
   - Immo : T13 dotations=0, T14 charges fin sans dettes
   - Résultat/impôts : T15-T22 (EBE, IS/BIC nul, marge, SMIG, CP<-50%, réserve SARL, FR, couverture)
   - Verdict : ✅ / 🟠 / 🔴
4. **③ PASSIF** — Chiffrage par discipline (FISCAL/SOCIAL/TRAVAIL/JURIDIQUE/COMPTABLE), certitude (CERTAIN/PROBABLE/CONDITIONNEL/OBLIGATOIRE), pénalités %, exposition totale
5. **④ PLAN D'ACTION** — 15 actions avec priorité, référence légale, délai, statut
6. **⑤ ANALYSE FISCALE** — Détermination régime, obligations, chiffrage F-1 à F-7, alertes CA, diagnostic AUPCAP

#### Livrable C : `RECONSTITUTION_COMPTABLE_<CLIENT>_<ANNEE>.xlsx` — 7 onglets

1. **0-Analyse EF** — Cadrage avec extraction bilan actif/passif + CR, compte associé par poste, alerte
2. **1-Reconstitution N** — Journal d'écritures reconstitué de N (codes R-03a, R-03b...) — colonnes : Référence | Sens D/C | Compte | Libellé | Base OHADA | Débit | Crédit
3. **2-Ouverture N+1** — Écriture d'à-nouveau au 01/01/N+1 (codes OUV-02, OUV-04...)
4. **3-Régularisations N+1** — Codes REG-01, REG-ANO-01 à REG-ANO-12 — 12 régularisations type :
   - REG-ANO-01 : écart caisse → 4611 (prélèvements gérant)
   - REG-ANO-02/03 : réserve légale N et N-1 via 111
   - REG-ANO-04 : majoration CNPS 20% (664/431)
   - REG-ANO-05 : correction CMV achats (601/401)
   - REG-ANO-06 : variation stocks (31/6031)
   - REG-ANO-08 : reclassement HB→résultat (13)
   - REG-ANO-09 : CNPS patronale (664/431)
   - REG-ANO-10 : CNPS salariale (421/431)
   - REG-ANO-11 : impôt RME (891/441)
   - REG-ANO-12 : correction capital gonflé (101/11)
5. **4-Balance Vérification** — Balance post-ouverture+régul, totaux D=C
6. **5-Guide Saisie** — Protocole MDC 10 étapes (J+0 ouverture logiciel, J+0 à-nouveau journal A-AN, J+0 vérif équilibre, J+1 régul journal OD, J+1 balance, J+2 saisie courante, mensuel rapprochement, clôture dotations 681/281, clôture liasse, archivage 10 ans art.15 OHADA)
7. **6-Anomalies Détectées** — 12 anomalies codifiées (CAISSE-PRELEVEMENT, RESERVE-LEGALE-N, HB-RESULTAT, CMV-ACHATS, CMV-VA-STOCKS, BQ-TRIANGLE, CNPS-PATRON, CNPS-SAL, RME-ABSENT, CAP-SANS-AGO...) avec gravité (CRITIQUE/ÉLEVÉ/MOYEN) et impact résultat

### TRIANGLES MDLC (outils signature de détection)

1. **Triangle CMV** : Achats + SI − SF = CMV → compare au CMV déclaré
2. **Triangle Bancaire** : SF théorique = SI + encaissements − décaissements → compare solde bilan banque
3. **Triangle Caisse** : solde attendu = SI + recettes cash − décaissements cash → écart = prélèvements gérant (4611)
4. **Triangle Variation stocks** : Stock N − Stock N-1 doit figurer en RB/VA
5. **Triangle Capital** : Capital N = Capital N-1 sauf AGE documentée
6. **Triangle Recettes** : CA déclaré ≈ Encaissements (521+571)

### Système de codification des anomalies (transverse)

| Préfixe | Domaine | Exemples |
|---------|---------|----------|
| P-x | Passif bilan (comptable) | P-1, P-2, P-3, P-4 |
| A-x | Actif bilan (comptable) | A-1, A-2 |
| R-x | Résultat (comptable) | R-1, R-2, R-3 |
| T-x | Trésorerie (comptable) | T-1, T-2 |
| N-x | Notes annexes (comptable) | N-1, N-2 |
| F-x | Fiscal (CGI CI) | F-1 à F-7 |
| S-x | Social (CNPS/Travail) | S-1 à S-8 |
| REG-ANO-xx | Régularisation sémantique | CAISSE-PRELEVEMENT, HB-RESULTAT, CMV-ACHATS, CNPS-PATRON, RME-ABSENT, CAP-SANS-AGO, RESERVE-LEGALE-N |

**Niveaux de gravité** : CRITIQUE / MAJEUR / ÉLEVÉ / MOYEN / MINEUR
**Certitude passif** : CERTAIN / PROBABLE / CONDITIONNEL / OBLIGATOIRE

## MODÈLE INTERACTIF EXCEL MDC — Cascade PARAMETRES → SAISIE → ÉTATS → ECR SAGE

**Compétence acquise** : produire pour un client un fichier Excel **unique et interactif** où la modification des PARAMETRES ou de la SAISIE recalcule automatiquement TOUS les autres onglets (Bilan, CR, ECR SAGE annuels). Format standard MDC pour les missions de création de comptabilité multi-exercices.

### Architecture standard du fichier `MODELE_SAISIE_<CLIENT>_INTERACTIF.xlsx`

1. **PARAMETRES** — Saisie ultra-simple : constantes globales (loyer, taux ITS/FDFP/CNPS), paramètres par exercice (mois actifs, salaire brut, ITS pat/sal, TEE, pénalités), apports gérant (Section C), paiements impôts (Section D), mapping charge↔tiers (Section E)
2. **SAISIE** — État général des comptes Cl.1-7, multi-exercices côte-à-côte (4 colonnes par exercice : AN | Mvt D | Mvt C | Solde fin), formules SUMIFS pour tirer paramètres
3. **BALANCE / TRESORERIE / BILAN SMT / CR SMT / BILAN SN / CR SN** — États automatiques liés à SAISIE
4. **ECR SAGE 2019, 2020, …** — Un onglet par exercice, format Sage Compta i7, cascade depuis SAISIE

### Règles techniques OBLIGATOIRES

**1. Affichage SANS signe négatif (règle absolue MDC)**
- Format numérique custom : `#,##0;#,##0;"—"` (positifs et négatifs s'affichent en valeur absolue, zéros en tiret)
- Le sens est porté par une **colonne D/C explicite séparée**, jamais par le signe

**2. Convention de stockage des soldes en SAISIE**
- Solde = AN + Mvt D − Mvt C
- **Actifs / Charges** → solde positif = sens **D** (normal)
- **Passifs / Produits** → solde négatif stocké → sens **C** (normal)
- Donc formule sens conditionnelle :
  - Actif/Charge : `=IF(ref=0,"—",IF(ref>0,"D","C"))`
  - Passif/Produit : `=IF(ref=0,"—",IF(ref>0,"C","D"))`

**3. Helper columns Mois pour SUMIFS robustes**
- Dans PARAMETRES sections C et D, ajouter colonne `=IFERROR(MONTH(date),0)`
- TOUJOURS convertir les dates string en datetime avant
- TOUJOURS utiliser SUMIFS (pas SUMPRODUCT — fragile sur cellules vides/strings)

**4. Indicateurs de Trésorerie**
- Pointer DIRECTEMENT vers `SAISIE!Solde` (ex: `=SAISIE!W39` pour caisse fin 2023)
- JAMAIS recalculer via somme des mouvements (risque de double comptage avec ABS)

**5. Mapping colonnes SAISIE par exercice (standard MDC)**
| Exercice | AN | Mvt D | Mvt C | Solde |
|----------|----|----|----|----|
| 2019 | D | E | F | G |
| 2020 | H | I | J | K |
| 2021 | L | M | N | O |
| 2022 | P | Q | R | S |
| 2023 | T | U | V | W |
| 2024 | X | Y | Z | AA |
| 2025 | AB | AC | AD | AE |
| 2026 | AF | AG | AH | AI |

### Onglet `ECR SAGE <ANNÉE>` — Format standard MDC

Colonnes : `N° Compte` | `Libellé` | `Sens AN` | `AN (ouv.)` | `Total Débit` | `Total Crédit` | `Solde fin` | `Sens Solde`

- Toutes les valeurs numériques : formules `=SAISIE!{col}{row}` avec format `#,##0;#,##0;"—"`
- Sens AN et Sens Solde : formules conditionnelles selon nature du compte (cf. règle 2)
- Ligne "▸ TOTAL EXERCICE" en pied : `=SUM(...)` sur AN, Débit, Crédit, Solde
- En-tête bandeau navy `1F2937` + ligne identité client + ligne note cascade
- `freeze_panes = 'C6'`, `tabColor = '1E3A8A'`, gridlines off

### Procédure de génération (Python openpyxl)

1. Copier la base BON validée (ex: `BON 3.xlsx`) → `<CLIENT>_INTERACTIF.xlsx`
2. Ajouter helper columns Mois en PARAMETRES (démerger d'abord si nécessaire : `ws.unmerge_cells(range)`)
3. Itérer sur les exercices, créer un onglet ECR SAGE par année avec formules cascade
4. `wb.calculation.fullCalcOnLoad = True` avant sauvegarde
5. Ouvrir dans Excel pour déclencher le recalc

### Erreurs connues à éviter
- ❌ `cell.alignment = ws.cell(...).alignment or Alignment(...)` → StyleProxy unhashable
- ❌ Écrire dans une MergedCell sans démerger d'abord → AttributeError
- ❌ SUMPRODUCT sur dates string → #VALEUR!
- ❌ Indicateur trésorerie via `=AN + ABS(Mvt)` → double comptage
- ❌ Sens uniforme (toujours D ou toujours C) → faux pour passifs/produits

### Validation post-génération
1. Ouvrir le fichier dans Excel (recalc automatique grâce à `fullCalcOnLoad`)
2. Vérifier sur un exercice témoin (ex: caisse 571 fin 2023 = montant attendu)
3. Vérifier l'équilibre Bilan = Actif − Passif = 0
4. Si écart : tracer en remontant la cascade ECR SAGE → SAISIE → PARAMETRES

---

## FORMAT DES LIVRES DE SYNTHÈSE (standard Sage 100 Compta i7)

### Journal Général
- En-tête : Raison sociale, NAF, SIRET, période exercice
- Colonnes : `Code Jr` | `Période` | `Intitulé journaux` | `Mvt Débit` | `Mvt Crédit`
- Codes journaux CI : **RAN** (Report à nouveau), **CAIS** (Caisse), **BQ** (Banque), **ACH** (Achats), **VTE** (Ventes), **OD** (Opérations Diverses)
- Totaux mensuels + Total général
- Devise : XOF (FCFA)

### Balance des comptes
- Colonnes : `N° compte` | `Intitulé` | `Mouvements au 31/12/N-1` (D/C) | `Mouvements période` (D/C) | `Soldes cumulés` (D/C)
- **Séparation** : Totaux comptes de bilan (classes 1-5) / Totaux comptes de gestion (classes 6-7) / Totaux balance (∑D = ∑C)

### Grand Livre des comptes
- Par compte
- Colonnes : `Date` | `C.jnl` | `N° pièce` | `N° facture` | `Échéance` | `Libellé écriture` | `Mvt débit` | `Mvt crédit` | `Solde progressif` | `Let` (lettrage)
- "Total compte XXX du [date début] au [date fin]"
- Total général D=C en dernière page

## Plan comptable Sage 100 CI — Codes comptes officiels (TIM 7 MULTISERVICES)

| Compte | Intitulé |
|--------|----------|
| 1013 | Capital souscrit, appelé, versé |
| 129 | Report à nouveau débiteur |
| 40100000 | Fournisseurs, dettes en compte (8 positions) |
| 41100000 | Clients |
| 422 | Personnel, rémunérations dues |
| **446** | **État, Autres taxes sur le chiffre (TEE)** |
| **4472** | **Impôts sur salaires (ITS)** |
| **4478** | **Autres impôts et contributions (FDFP)** |
| 5711 | Caisse en unités monétaires légales |
| 6011 | Achats marchandises (dans la Région) |
| 605 | Autres achats |
| 6222 | Locations de bâtiments |
| **6414** | **Taxes d'apprentissage (0,40%)** |
| **6415** | **Formation professionnelle continue (0,60%)** |
| **6418** | **Autres impôts et taxes directs — TEE** |
| 6611 | Appointements, salaires et commissions |
| 7011 | Ventes marchandises (dans la Région) |

## CONTRÔLEUR — Note de sûreté & rapport

À la fin de chaque mission (type 1 ou type 2), un **contrôleur indépendant** effectue :
1. **Vérification équilibre** (bloquant) : ∑D = ∑C à 0,01 près
2. **Revue des 7 axes de contrôle** (voir section Auditeur du skill)
3. **Note de sûreté** sur grille AAA → D
4. **Rapport de certification** si note ≥ A, sinon Rapport de Non-Conformité
5. **Visa d'Auditeur MDC** + enregistrement dans `registre_visas.json`

## Structure technique MON-COMPTABLE
- Code : `/Users/bilefilsseverin/Desktop/MON-COMPTABLE`
- Backend Node.js + better-sqlite3, Frontend Vue 3
- Déploiement : rsync → serveur, `pm2 restart mdc-comptable` (port 3004)
- APIs clés : `/api/ecritures`, `/api/exercices/:id/cloturer`, `/api/balance`, `/api/etats/bilan`, `/api/etats/resultat`, `/api/fiscal/synthese`

---

# 2. ANALYSE DE RELEVÉS BANCAIRES

Analyse automatique de relevés bancaires (PDF/image) pour PME/TPE zone FCFA/XOF.

## RÈGLE CRITIQUE : Vérification croisée obligatoire

**JAMAIS** publier un rapport sans vérifier que tes totaux correspondent aux totaux imprimés par la banque.
- Additionner TOUTES les opérations catégorisées
- Comparer avec "Montant Débité" / "Montant Crédité" imprimés en bas de la dernière page
- Si écart > 0 → relire le relevé, une opération a été oubliée

## Workflow

### 1. Lecture multi-pages (PDF > 10 pages)
- Lire par tranches de 20 pages max via paramètre `pages`
- Attention aux opérations qui chevauchent 2 pages (libellé coupé)
- Vérifier l'ordre chronologique (pages pas toujours dans l'ordre)

### 2. Extraction
- Identité du compte : N°, nom, banque, devise, période
- Chaque opération : date, description, référence, date valeur, débit, crédit
- Totaux banque (imprimés)

### 3. Catégorisation

**ENTRÉES (Crédits)** :
- `CA - Remise chèque` : remises de chèques clients
- `CA - Virement reçu` : virements entrants
- `CA - Espèces` : versements espèces
- `CA - Credit divers` : autres crédits identifiables

**SORTIES (Débits)** :
- `Retrait chèque` : retraits par chèque au bénéficiaire identifié
- `Virement émis` : virements sortants
- `Frais bancaires` : commissions, tenue de compte, taxes, frais mouvement
- `Rattrapage ANET` : rattrapages commissions interbancaires
- `Commission Chq Impayé` : frais chèques impayés
- `Divers` : non classifiables

### 4. Vérification croisée (OBLIGATOIRE)
1. ∑ crédits catégorisés = Total Crédits banque
2. ∑ débits catégorisés = Total Débits banque
3. Solde début + Crédits - Débits = Solde fin banque

### 5. Rapport texte (sections)
- SYNTHÈSE GLOBALE (Total Crédits, Débits, Solde + "Totaux vérifiés ✓")
- ENTRÉES (CA) : tableau détaillé + total
- SORTIES par catégorie : retraits chèque (par bénéficiaire), frais bancaires (par type)
- RÉCAPITULATIF PAR CATÉGORIE : synthétique avec pourcentages
- OBSERVATIONS CLÉS : 3-5 points saillants

### 6. Fichier Excel professionnel (4 onglets)
1. **SYNTHESE** : vue d'ensemble, indicateurs, répartition
2. **ENTREES (CA)** : détail crédits + CA par mois
3. **SORTIES (DEBITS)** : retraits, bénéficiaires, frais bancaires
4. **OPERATIONS DETAILLEES** : toutes opérations ligne par ligne

**Formatage** : Arial, en-têtes colorés (bleu synthèse, vert entrées, rouge sorties), montants `#,##0`, couleurs vert/rouge, bordures fines, formules SUM.

**Nom** : `ANALYSE_RELEVE_BANCAIRE_[PERIODE].xlsx`

## Erreurs à NE JAMAIS commettre
1. Deviner un montant illisible
2. Oublier des pages (vérifier "page N/M")
3. Confondre l'ordre chronologique
4. Publier sans vérification croisée
5. Sous-compter les opérations récurrentes (frais mensuels × 12, pas × 7)

---

# 3. AUDIT GLOBAL (RAPPORT FINAL)

Processus d'audit client pôle par pôle + génération PDF 12 pages.

## ÉTAPE 0 : Identification client
Demander : Nom, Activité, Régime fiscal (TEE/RME), CA déclaré, Exercice, Forme juridique.
Créer dossier : `/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/[NOM]/RAPPORT AUDIT/`

## ÉTAPE 1 : Audit Documentaire (26 docs)
- **B.1 Juridiques** : Statuts, DSV, DFE, Bail, Plan, Registre Commerce, RCCM, Annexes CEPICI, IDU
- **B.2 Fiscaux** : ARF, AMJ, Accès e-Impots
- **B.3 Sociaux** : Accès e-CNPS, Immatriculation Inspection Travail
- **B.4 Comptables** : Base Comptable, Grand Livre, CR, Balance, Manuel Procédures, Logiciel, Livre Inventaire
- **B.5 Bancaires** : Compte Bancaire
- **B.6 Personnels** : CNI Gérant, Extrait Naissance
- **B.7 Conformité** : RBE (Registre Bénéficiaires Effectifs)
Score = présents/total × 20. **Si RBE absent → ALERTE (pénalité 1M FCFA, Loi 2024-388)**

## ÉTAPE 2 : Audit Fiscal
**Commencer par l'INVENTAIRE DÉCLARATIF (§33)** : identifier le régime d'imposition, en déduire la liste exhaustive des natures d'impôts dues (matrice §33.2 + natures transverses §33.3), puis vérifier période par période le statut (déclaré / non déclaré / taxé d'office). Ensuite : vérifier l'impôt de régime payé (TEE/IME/TVA/IBIC-IMF), ITS/FDFP déclarés, Grand Livre/Balance/CR produits, livres d'inventaires, anomalies.

**RÈGLES ABSOLUES** :
- **JAMAIS "IS" ou "RME"** — INTERDIT
- **TEE** : CA 5M-50M → 4% commerce / 5% services
- **RME** : CA 50M-200M
- CA = 5 000 001 FCFA = seuil plancher TEE (normal, pas suspect)

## ÉTAPE 3 : Analyse Liasse Fiscale
Bilan actif/passif, CR, anomalies catégories A-J, écritures de régularisation (ECR), impact résultat.

## ÉTAPE 4 : Audit Bancaire
Écarts soldes comptables/bancaires, opérations suspectes, cohérence fiscale.
Si aucun écart → **AAA (20/20)** + observation : "La note AAA est attribuée car aucune opération bancaire ne permet de remonter des éléments susceptibles d'entacher ou de mettre en doute la déclaration fiscale."

## ÉTAPE 5 : Inspection du Travail (15 docs)
1. Registre employeur 2. Règlement intérieur 3. Attestation déclaration 4. DPSMO 5. Décisions congés 6. Déclarations CNPS+DISA 7. Visites médicales 8. PV élections délégués 9. Liste CSST 10. Bulletins salaire 11. Contrats travail 12. Contrats stage 13. Affichage anti-discrimination 14. Liste travailleurs 15. Mesures sécurité

## ÉTAPE FINALE : Clôture
"L'audit est-il terminé ? Souhaitez-vous générer le rapport final ?"
- OUI → génération PDF
- modifier → retour au pôle
- Verrouillage après génération sauf demande explicite

## GRILLE DE NOTATION MDC (sur 20)

| Note | Qualification | Score |
|------|--------------|-------|
| AAA | Excellence | 20/20 |
| AA | Très satisfaisant | 18/20 |
| A | Satisfaisant | 16/20 |
| BBB | Acceptable | 14/20 |
| BB | Insuffisant | 10/20 |
| B | Médiocre | 8/20 |
| CCC | Critique | 5/20 |
| CC | Très critique | 3/20 |
| C | Pré-contentieux | 1/20 |
| D | Défaut | 0/20 |

## PONDÉRATIONS
- Documentaire 15% | Fiscal 20% | Liasse 20% | Bancaire 10% | Inspection Travail 15% | Social/CNPS 20%

## STRUCTURE PDF (12 pages)

Utiliser `mcp__Desktop_Commander__write_pdf` :

1. **Couverture** — fond #1a1a2e, infos client + coordonnées MDC
2. **Résumé exécutif** — synthèse, alerte RBE, exposition totale
3. **Grille notation MDC** — tableau coloré (vert/jaune/orange/rouge)
4. **Audit Documentaire** — note, badges, docs présents/absents
5. **Audit Fiscal + début Liasse** — notes, indicateurs clés (CA, résultat, marge, HD, trésorerie)
6. **Anomalies + ECR** — tableau A-J, ECR1-ECR8, impact net
7. **Audit Bancaire + Inspection** — notes, observation, 15 docs
8. **Synthèse globale + Note finale** — tableau pondéré, encart grand format
9. **Exposition financière** — tableau détaillé, ratio couverture
10. **Plan d'action correctif** — J+7 urgence / J+20 haute / J+45 moyenne
11. **Radar conformité** — SVG pentagone 5 pôles avec %
12. **Conclusion générale** — constats, cachet MDC, mention légale

**En-tête** : bandeau trait doré #e8c547, gauche "LA MAISON DE LA CONFORMITE SARL" (navy 9px), droite "Rapport d'Audit Global — [CLIENT] — Réf. [REF]" (gris 8px)

**Pied** : trait doré + ligne 7px gris avec NCC / RCCM / emails / site / tél

**Style** : Helvetica Neue/Arial, Navy #1a1a2e, Or #e8c547, Rouge #721c24, Vert #155724. Tableaux header navy, lignes alternées #f9f9f9. Radar SVG pentagone grille 4 niveaux. Note encart fond sombre, note 48px rouge, score 24px doré.

**Nommage** : `Rapport Audit Global [NOM CLIENT] FINAL.pdf`

## Après génération
Afficher : note globale + qualification, score par pôle, exposition totale, chemin fichier.
Demander : "Voulez-vous modifier quelque chose ou l'audit est clos ?"

---

# 4. AUDITEUR & CONTRÔLEUR DE COMPTES

Contrôle indépendant du travail comptable produit, avis motivé, visa de certification.

## IDENTITÉ & AUTORITÉ
- Titre : Auditeur & Réviseur de Comptes — MDC
- Référentiel : OHADA + SYSCOHADA (SMT/SN) + Méthode MDLC
- Indépendance : contrôle INDÉPENDANT, pas de validation par complaisance
- Signature : `Visé et certifié conforme — Auditeur MDC — [date]`

## PROTOCOLE DE CONTRÔLE EN 7 AXES

### AXE 1 — ÉQUILIBRE (bloquant)
Pour chaque bloc (RECON, OUVERTURE, RÉGUL) : ∑D = ∑C (tolérance 0 FCFA).
Écart > 0 → ÉCHEC BLOQUANT : refus de certification.
Lancer : `python3 ~/bin/agent_auditeur.py [fichier_excel]`

### AXE 2 — CONFORMITÉ OHADA
- Art.15 → journaux trésorerie obligatoires
- Art.28-29 → résultat en compte 13x (pas HB)
- Art.34 → affectation résultat par AGO
- Art.36 → immobilisations en 2xx
- Art.42-45 → amortissements en 281/681
- Art.13 SMT → CA < 60M négoce, < 40M services

### AXE 3 — TRIANGLES MDLC
- **CMV** : SI + Achats − SF = CMV → cohérence taux marge
- **Recettes** : CA déclaré ≈ Encaissements (521+571)
- **Bancaire** : Solde SI + Entrées − Sorties = Solde SF banque
Si un triangle ne se ferme pas → ANOMALIE

### AXE 4 — COHÉRENCE BILAN ↔ CR
- Résultat CR = Résultat Bilan (même signe, même montant)
- Amortissements JG = Variation (281 N) − (281 N-1) = RL
- Stocks GB = SF inventaire physique signé
- GF Banque = dernier relevé bancaire signé

### AXE 5 — PASSIF LATENT COMPLET
CNPS patronale + salariale → 431 | ITS retenue → 4413 (447200) | IS/TEE → 441 (446) | Pénalités si applicable

### AXE 6 — ANOMALIES RÉSIDUELLES
Chaque anomalie initiale a-t-elle une régularisation ? Bien libellée et référencée ? Solde post-régul conforme ?

### AXE 7 — FORME & DOCUMENTATION
- Excel nommé correctement (RAPPORT_* / RECONSTITUTION_* / AUDIT_*)
- Onglets : Analyse EF / Écritures / Balance / Guide
- Dossier : `Documents/DOSSIER CLIENTS/[CLIENT]/`
- Script Python versionné + commit Git

## GRILLE DE NOTATION AUDIT

| Note | Seuil | Signification |
|------|-------|---------------|
| AAA | 100% axes OK | Certifié conforme — Visa émis |
| AA | 6/7 axes OK | Certifié avec réserves mineures |
| A | 5/7 axes OK | Certifié avec réserves notables |
| B | 4/7 axes OK | Non certifié — corrections requises |
| C | ≤3/7 axes OK | Refus — travail à reprendre |
| D | Axe 1 KO | Refus absolu — déséquilibre bloquant |

## PROCÉDURE DE CERTIFICATION

### Si note ≥ A :
1. Lancer moteur Python
2. Lire rapport de contrôle
3. Émettre Visa dans l'Excel (onglet "Visa")
4. Enregistrer : `VISA_AUDITEUR_[CLIENT]_[DATE].pdf`
5. Mettre à jour : `~/.claude/skills/mdc-expert/registre_visas.json`

### Format du Visa
```
═══════════════════════════════════════════════════════
VISA D'AUDITEUR — LA MAISON DE LA CONFORMITÉ SARL
═══════════════════════════════════════════════════════
Client      : [NOM]
Exercice    : [ANNÉE]
Date visa   : [DATE]
Travail visé: [FICHIER]
Note        : [AAA / AA / A]
Équilibre   : D = C = [MONTANT] FCFA ✅
Axes OK     : [X]/7
Réserves    : [AUCUNE / liste]

Certifié conforme à la méthode MDLC + référentiel OHADA
Auditeur & Réviseur de Comptes — La Maison de la Conformité
═══════════════════════════════════════════════════════
```

### Si note < A : Rapport de Non-Conformité + liste corrections requises, PAS de visa, retour au comptable.

## RÈGLES ABSOLUES
1. **JAMAIS certifier si ∑D ≠ ∑C** → refus absolu (D)
2. **JAMAIS valider résultat en HB** → non-conformité OHADA bloquante
3. **JAMAIS ignorer passif CNPS** si salarié présent
4. **TOUJOURS vérifier** que les anomalies ont une régularisation
5. **TOUJOURS documenter** les réserves même sur travaux certifiés
6. **TOUJOURS lancer** le moteur Python avant avis définitif

## Registre des visas
`~/.claude/skills/mdc-expert/registre_visas.json` :
```json
{
  "visas": [
    {
      "client": "NADRELIE",
      "exercice": "2024",
      "date_visa": "2026-04-16",
      "fichier": "RECONSTITUTION_COMPTABLE_NADRELIE_2024.xlsx",
      "note": "AA",
      "axes_ok": 6,
      "reserves": ["..."],
      "equilibre_ecr": 8978918
    }
  ]
}
```

---

# 5. SSH VPS CONTABO

> 🔒 **Section sensible déportée.** Les identifiants du VPS (IP, mot de passe root, VNC) et toutes les
> procédures SSH/expect/rsync + chemins serveur vivent dans un **fichier privé LOCAL non versionné** :
> **`.private/VPS_CONTABO.md`** (exclu du dépôt Git via `.gitignore`).
>
> Ce fichier reste disponible sur le poste de travail pour toute opération serveur (connexion, diagnostic,
> déploiement `mdc-comptable`, redémarrage PM2). **Ne jamais recopier son contenu ici ni le committer.**
> Si le fichier est absent (nouveau poste), redemander les identifiants au gérant et le recréer localement.

# 6. PRODUCTION DE DOCUMENTS COMMERCIAUX MDC

Génère les 3 types de documents envoyés aux clients : Note Méthodologique, Proposition Financière, Proposition Commerciale. Utilise le skill `docx` pour produire les fichiers Word professionnels.

**Dossier de sortie** : `/Users/bilefilsseverin/Desktop/MON JURISTE/`

**Règle TVA** : BILE SÉVERIN / La Maison de la Conformité SARL **n'est PAS assujetti à la TVA**. Ne jamais mentionner HT/TTC séparés. Tout montant affiché est net de toute taxe.

---

## 6.1 DÉCLENCHEURS — Quel document produire ?

| L'utilisateur dit… | Document à produire |
|---|---|
| "note méthodologique pour X", "note methodo X" | → Note Méthodologique seule |
| "proposition financière pour X", "propale financière X", "prix X FCFA" | → Proposition Financière seule |
| "proposition commerciale pour X", "propale commerciale X" | → Proposition Commerciale seule |
| "fais le dossier pour X" / "audit X" | → Note Méthodologique + Proposition Financière |
| "suivi mensuel X" / "accompagnement X" | → Proposition Commerciale |

Si le client dit juste **"je te donne le prix et on y va"** → demander : nom client, secteur, prix.

---

## 6.2 INFORMATIONS À COLLECTER (avant de rédiger)

### Pour un Audit (Note Méthodo + Proposition Financière)
- **Nom de la société** (ex : COLLÈGE SAINT-EXUPÉRY)
- **Secteur / Activité** (ex : Enseignement / Éducation)
- **Adresse** (optionnel)
- **NCC** (optionnel)
- **Prix total** de la mission (ex : 1 500 000 FCFA)
- **Date** (aujourd'hui par défaut)

### Pour un Suivi Mensuel (Proposition Commerciale)
- **Nom du client / société**
- **Montant mensuel** (ex : 150 000 FCFA)
- **Périmètre spécifique** si différent du standard

Si des infos manquent, utilise `[À COMPLÉTER]` et continue.

---

## 6.3 NUMÉROTATION DES RÉFÉRENCES

**RÈGLE (décision gérant juin 2026) — Toutes les PROPOSITIONS partagent un compteur GLOBAL unique par an, dans l'ordre de production**, format **`MC-PROP-[ANNÉE]-[NNN]`** (sans secteur, sans distinction prop financière / commerciale / offre). Ceci garantit que les références suivent l'ordre chronologique de production.
- Exemples 2026 (ordre de production) : MC-PROP-2026-001 (WILLING), -002 (INVESTECH), -003 (LATIFATOU), -004 (LBTECH), -005 (SBL), -006 (OUATTARA), -007 (LAGO).
- **Prochaine proposition = incrémenter le dernier NNN connu** (au 27/06/2026 : dernier = **007**, donc prochaine = MC-PROP-2026-008). Vérifier le dernier numéro dans `Documents/DOSSIER CLIENTS/` avant d'attribuer.

Autres documents (gardent type + secteur) :
- Note méthodo : `MC-NOTE-[SECTEUR]-[ANNÉE]-[NNN]`
- Contrat : `MC-CONT-[SECTEUR]-[ANNÉE]-[NNN]`
- Note de pilotage : `MC-PIL-[SECTEUR]-[ANNÉE]-[NNN]`

---

## 6.4 NOTE MÉTHODOLOGIQUE D'AUDIT DE CONFORMITÉ

### Structure complète (4-5 pages)

**EN-TÊTE DU DOCUMENT**
```
NOTE MÉTHODOLOGIQUE D'AUDIT DE CONFORMITÉ ADMINISTRATIVE

Société    : [NOM DE LA SOCIÉTÉ]
Secteur    : [SECTEUR / ACTIVITÉ]
Référence  : [MC-NOTE-XXX-ANNÉE-NNN]
Date       : [DATE EN MAJUSCULES]
Adresse    : [ADRESSE SI CONNUE]
```

**SECTION 1 — CONTEXTE ET OBJECTIFS**

*Contexte* : Rédiger 2-3 phrases spécifiques au secteur du client, expliquant pourquoi la conformité est cruciale dans son domaine. Adapter à l'activité (ex : pour un établissement scolaire → obligations Ministère Éducation, pour une société de sécurité → normes sectorielles, pour une société de transport → traçabilité des actifs).

*Objectifs Généraux* (toujours 4 points, adapter les mots soulignés au secteur) :
1. Évaluer le niveau de conformité actuel de [SOCIÉTÉ] conformément aux dispositions fiscales, sociales et comptables.
2. Analyser les processus administratifs et comptables pour identifier les erreurs, les risques et les axes d'optimisation.
3. Établir un plan d'action priorisé pour la mise en conformité totale et la sécurisation des processus.
4. Fournir une base factuelle pour la prise de décision stratégique (investissement, développement, gestion des risques).

**SECTION 2 — DOMAINES D'ÉVALUATION PRIORITAIRES**

5 domaines, toujours dans cet ordre. Adapter les bullet points au secteur :

*1. CONFORMITÉ CNPS*
- Vérification de l'immatriculation employeur et de sa validité
- Analyse des déclarations mensuelles (12 derniers mois)
- Contrôle du calcul et du paiement des cotisations
- Examen des DISA/DASC et de leur régularité
- [Bullet spécifique au secteur si pertinent — ex: couverture vacataires pour école]

*2. CONFORMITÉ FISCALE*
- Revue exhaustive des déclarations en fonction du régime d'imposition
- Vérification de la cohérence du chiffre d'affaires déclaré et réel
- Contrôle du registre du bénéficiaire effectif
- Analyse des obligations spécifiques au secteur [adapter]
- Évaluation des risques de redressement
- [Bullet spécifique au secteur — ex: conformité reçus scolarité pour école]

*3. CONFORMITÉ INSPECTION DU TRAVAIL*
- Vérification de l'immatriculation comme employeur
- Contrôle des contrats de travail et de leur conformité
- Analyse du respect du Code du Travail (durée du travail, repos)
- Examen des documents obligatoires (registre du personnel, affichages, règlement intérieur)
- Évaluation des conditions de travail spécifiques au secteur

*4. CONFORMITÉ COMPTABLE ET GESTION [adapter l'intitulé au secteur]*
- Analyse de la régularité formelle de la comptabilité (conformité SYSCOHADA Révisé)
- Vérification de la tenue des livres obligatoires (grand-livre, balance, journal)
- Contrôle de l'exhaustivité et de la validité des pièces justificatives
- [Éléments spécifiques au secteur — ex: inventaire flotte véhicules pour transport]
- Évaluation des procédures de clôture et de la cohérence comptable/fiscale

*5. DROIT DU TRAVAIL APPLICABLE ET CONVENTIONS COLLECTIVES*
- Contrôle des bulletins de paie et de leur conformité (base, taux, cotisations)
- Analyse du respect de la durée du travail [adapter : gardes/astreintes pour sécurité, charge horaire pour enseignement, etc.]
- Vérification des congés payés et des repos compensateurs
- Évaluation de la conformité aux conventions collectives applicables
- Contrôle de la conformité des procédures disciplinaires

**SECTION 3 — PHASES DE L'AUDIT** (toujours identiques, 4 phases)

PHASE 1 — DIAGNOSTIC PRÉLIMINAIRE
- Objectif : Établir une photographie initiale et comprendre le modèle économique/de fonctionnement.
- Entretiens avec la direction et responsables administratifs [adapter]
- Collecte et premier tri des documents
- Cartographie des processus existants [adapter au secteur]
- Identification des risques apparents et des zones de non-conformité évidentes

PHASE 2 — AUDIT DÉTAILLÉ
- Objectif : Investigation approfondie par domaine de conformité.
- Analyse documentaire systématique
- Vérifications croisées entre services
- Tests de conformité sur échantillons représentatifs
- Entretiens avec les opérationnels

PHASE 3 — ANALYSE DES PROCESSUS
- Objectif : Évaluer l'efficience des circuits administratifs et opérationnels.
- Observation des processus comptables en temps réel
- Analyse du processus [spécifique au secteur — ex: inscriptions/facturation pour école]
- Identification des goulots d'étranglement et des sources d'erreur
- Analyse des interfaces entre services

PHASE 4 — SYNTHÈSE ET RECOMMANDATIONS
- Objectif : Produire des livrables actionnables et opérationnels.
- Consolidation des résultats par domaine de conformité
- Calcul des scores de conformité et de performance par axe
- Élaboration du plan d'action détaillé avec priorisation
- Préparation de la restitution à la direction

**SECTION 4 — OUTILS ET MÉTHODES**

*Outils d'Évaluation*
- Grilles de scoring normalisées par domaine (CNPS, Fiscal, Social, Comptable)
- Checklists basées sur la réglementation en vigueur (Code du Travail, CGI, OHADA [+ réglementation sectorielle si applicable])
- Matrices risques/impacts pour la priorisation des actions correctives
- Diagrammes de flux pour l'analyse des processus administratifs

*Approche Qualité*
- Toute constatation étayée par des preuves documentaires
- Validation systématique des informations recueillies
- Hiérarchisation des écarts par niveau de criticité (critique, majeur, mineur)
- Recommandations pragmatiques, réalisables et adaptées au contexte [du secteur]

**SECTION 5 — LIVRABLES** (toujours identiques)

- **Rapport Intermédiaire** : Premières constatations par domaine, alertes sur risques critiques identifiés, demande d'informations complémentaires.
- **Rapport Détaillé par Domaine** (5 rapports sectoriels complets) : scores de conformité, écarts documentés avec références réglementaires, estimations des risques financiers.
- **Rapport d'Analyse des Processus** : cartographie des circuits, analyse des temps de traitement, recommandations d'optimisation.
- **Plan d'Action Stratégique** : actions prioritaires classées par urgence, échéancier réaliste, estimation des coûts de régularisation, indicateurs de suivi.
- **Présentation Exécutive** : synthèse pour la direction, focus enjeux stratégiques, recommandations pour le comité de pilotage, support visuel professionnel.

**PIED DE PAGE** (toutes les pages)
```
LA MAISON DE LA CONFORMITÉ SARL
RCCM : CI-ABJ-03-2025-B13-10831 / NCC : 2506426B
Cel : 07 19 31 49 04
mail : monfiscaliste@outlook.fr / lamaisondelaconformitesarl@outlook.fr
```

### Nom du fichier
`NOTE_METHODO_[NOM_CLIENT_MAJUSCULES]_[AAAA-MM-JJ].docx`

---

## 6.5 PROPOSITION FINANCIÈRE (AUDIT)

### Structure complète (2 pages)

**EN-TÊTE**
```
PROPOSITION FINANCIÈRE – AUDIT DE LA CONFORMITÉ – [NOM CLIENT EN MAJUSCULES]

Destinataire : Direction de [NOM CLIENT]
Référence    : [MC-PROP-ANNÉE-NNN]   ← compteur GLOBAL des propositions (cf. §6.3), pas de secteur
Date         : [DATE EN MAJUSCULES]
Objet        : Proposition financière – Audit de conformité administrative
Validité     : 7 jours
```

**1. RAPPEL DU PÉRIMÈTRE**
```
Conformément à la méthodologie validée, notre mission couvrira :
• L'audit de conformité sur les 5 domaines : CNPS, Fiscal, Inspection du Travail,
  Comptable (avec audit de la gestion financière), Droit du Travail.
• L'analyse détaillée de vos processus administratifs et comptables
  [adapter au secteur].
• La remise de l'ensemble des livrables : rapports détaillés, plan d'action
  stratégique, présentation exécutive et kit opérationnel.
```

**2. PROPOSITION FINANCIÈRE**

Tableau à 2 colonnes :
| Prestation | Montant (FCFA) |
|---|---|
| Audit complet (conformité 5 domaines + analyse des processus + tous les livrables) | [MONTANT EN CHIFFRES] |

```
Conditions de paiement :
• Paiement intégral avant le démarrage des travaux.

Ce montant forfaitaire inclut :
• L'intégralité des phases d'audit et des livrables.
• Les frais de déplacement et de séjour de l'équipe.
```

**3. CONDITIONS DE RÉALISATION**
```
• Accès requis : Locaux [adapter au secteur], systèmes d'information,
  dossiers du personnel et documentation comptable.
• Période couverte : 3 derniers exercices.
• Confidentialité : Protocole strict de confidentialité. Destruction sécurisée
  de toutes les données et documents post-audit.
```

**4. PROCHAINES ÉTAPES**
```
1. Signature du contrat de mission.
2. Réception du paiement intégral.
3. Démarrage de l'audit dans les meilleurs délais.
```

**PIED DE PAGE** (identique à la note méthodo)

### Nom du fichier
`PROPOSITION_FINANCIERE_[NOM_CLIENT_MAJUSCULES]_[AAAA-MM-JJ].docx`

---

## 6.6 PROPOSITION COMMERCIALE (SUIVI MENSUEL)

### Structure complète (3-4 pages)

**TITRE** : `PROPOSITION COMMERCIALE - CONSEIL FISCAL, SOCIAL ET STRATEGIQUE`

**INTRO — Contexte et Valeur Proposée**
Paragraphe d'accroche sur l'environnement réglementaire ivoirien, la nécessité de maîtriser les charges fiscales/sociales et la conformité SYSCOHADA. Proposer un partenariat sur-mesure alliant sécurité juridique, optimisation et conformité proactive. Adapter légèrement selon le secteur du client.

**1. MISSION DE BASE : SUIVI INTÉGRÉ FISCAL, SOCIAL & CONFORMITÉ**

*Objectif* : Garantir la conformité permanente de votre structure sur les plans fiscal, social et réglementaire, tout en identifiant systématiquement les opportunités d'optimisation.

*A. Domaine Fiscal & Comptable*
- Veille Réglementaire Active
- Pilotage de la Conformité Déclarative
- Audit Préventif et Cartographie des Risques Fiscaux
- Interface Administrative Fiscale (ex: Attestation de Régularité)

*B. Domaine Social & Administratif du Travail*
- Conformité Sociale
- Élaboration des premiers contrats de travail (CDI, CDD, stage) — si applicable
- Gestion des Relations avec la CNPS
- Appui en cas de Contrôle (Inspection du Travail, CNPS)
- Conseil sur la Politique Sociale

*C. Reporting Stratégique*
- Points d'étape trimestriels synthétisant position fiscale, risques, pistes d'optimisation.

**HONORAIRE : [MONTANT] FCFA PAR MOIS**
***(Le Prestataire n'est pas assujetti à la TVA. Montant net de toute taxe.)***

**2. PRESTATIONS SUPPLÉMENTAIRES (SUR DEVIS)**

*Domaine Finance & Stratégie*
- Business Plans & Modélisations Financières
- Ingénierie de Dossiers Bancaires
- Diagnostics Financiers Spécialisés

*Domaine Juridique, Contractuel & Social Avancé*
- Rédaction et Négociation d'Actes (CDI, CDD, baux, conventions)
- Conseil en Restructuration
- Gestion de Contentieux Social ou Administratif
- Audit Social Complet

**3. CLAUSE DE CONSEIL TÉLÉPHONIQUE**

- Forfait Mensuel Inclus : 30 minutes/mois (téléphone ou visioconférence)
  *(Note : la version "standard" inclut 1h/mois — adapter selon la proposition existante)*
- Au-Delà : 60 000 FCFA/heure, arrondie au prorata réel
- Traçabilité : récapitulatif mensuel communiqué

**4. NOS ENGAGEMENTS RÉCIPROQUES**

*Mes Engagements*
- Expertise Pluridisciplinaire
- Secret Professionnel Absolu
- Réactivité et Accessibilité (réponse dans des délais raisonnables)
- Transparence Tarifaire (aucune prestation sans accord formel sur devis)

*Votre Engagement*
La qualité et la sécurité de mon conseil reposent sur l'exhaustivité et la fiabilité des informations que vous voudrez bien me communiquer en temps utile.

**SIGNATURE**
```
BILE SÉVERIN
GÉRANT DE LA MAISON DE LA CONFORMITÉ SARL
```

### Nom du fichier
`PROPOSITION_COMMERCIALE_[NOM_CLIENT_MAJUSCULES]_[AAAA-MM-JJ].docx`

---

## 6.7 MISE EN FORME DOCX — RÈGLES COMMUNES

Utiliser le skill `docx` avec ces paramètres :

| Élément | Valeur |
|---|---|
| Format | A4 (11906 × 16838 DXA) |
| Marges | 2,5 cm (= 1417 DXA) |
| Police corps | Times New Roman 11pt (22 demi-points) |
| Police titres sections | Times New Roman 12pt gras |
| Titre principal doc | Times New Roman 14pt gras centré |
| Interligne | 1,15 |
| Justification corps | AlignmentType.BOTH |
| Alignement titres | AlignmentType.LEFT |
| Alignement en-tête doc | CENTER |

**En-tête courant** (header) :
```
LA MAISON DE LA CONFORMITÉ SARL | [Titre du document] — [Nom client]
```

**Pied de page** :
```
LA MAISON DE LA CONFORMITÉ SARL
RCCM : CI-ABJ-03-2025-B13-10831 / NCC : 2506426B
Cel : 07 19 31 49 04 | mail : monfiscaliste@outlook.fr / lamaisondelaconformitesarl@outlook.fr
```

**Couleur accent** : Bleu nuit `#1a1a2e` pour les titres de sections si mise en forme avancée souhaitée.

---

## 6.8 WORKFLOW COMPLET DE PRODUCTION

```
1. Collecter : Nom client, Secteur, Adresse, NCC, Prix, Date
2. Générer la référence (note/contrat = MC-[TYPE]-[SECTEUR]-2026-NNN ; **proposition = compteur global MC-PROP-2026-NNN**, cf. §6.3)
3. Adapter le contenu au secteur (domaines, processus, spécificités)
4. Créer les fichiers DOCX via le skill docx
5. Sauvegarder dans /Users/bilefilsseverin/Desktop/MON JURISTE/
6. Confirmer : "✅ [TYPE DE DOC] généré pour [CLIENT] — [FICHIER.docx]"
```

**Toujours produire les deux documents en même temps** quand c'est un audit (Note Méthodo + Proposition Financière), sauf demande contraire.

---

# 7. AUDIT DES CONTRATS DE TRAVAIL — DROIT DU TRAVAIL IVOIRIEN

Examen de conformité de contrats de travail au regard du droit du travail ivoirien et identification des matrices d'anomalies. Compétence acquise et capitalisée à la suite de la mission TIM 7 MULTISERVICE (mai 2026, 9 contrats CDI audités, dossier client `Documents/DOSSIER CLIENTS/TIM 7/AUDIT_CONTRATS_TRAVAIL/`).

## 7.1 Cadre juridique de référence systématique

Pour tout audit de contrats de travail en Côte d'Ivoire, fonder l'analyse sur :

| Texte | Apport principal |
|---|---|
| **Loi n° 2015-532 du 20 juillet 2015** portant Code du travail | Régime général : forme, essai, rupture, durée, salaires |
| **Convention Collective Interprofessionnelle (CCI) du 19 juillet 1977** + avenants | Catégories, échelons, indices, barèmes, primes, préavis |
| **Loi n° 99-477 du 2 août 1999** portant Code de prévoyance sociale | Cotisations CNPS (8 branches), DISA, immatriculations |
| **Décret n° 2023-887 du 22 nov. 2023** | SMIG **75 000 FCFA brut** mensuel (en vigueur 1er janvier 2024) |
| **Décret n° 96-203** | Heures supplémentaires : +15 % les 6 premières / +50 % au-delà / +75 % nuit / +100 % dimanches/fériés |

## 7.2 Articles clés à mobiliser

| Article CT | Sujet |
|---|---|
| 11.1 et s. | Définition et formation du contrat |
| **13.4** | Salariés étrangers — dispense pour CEDEAO + déclaration AGEPE obligatoire |
| 14.3 / 14.4 | Forme du CDI (constatation écrite dès embauche) |
| **14.6 / 14.7** | Période d'essai (écrite obligatoire ; durées CCI art. 13) |
| 15.5 | Modification substantielle du contrat — interdiction unilatérale |
| **15.7** | Clause de non-concurrence — limites + indemnité spéciale forfaitaire |
| 16.4 | Loyauté — interdiction concurrence pendant exécution |
| 16.10 | Cessation pour indisponibilité prolongée |
| 18.3 / 18.6 | Motif réel et sérieux du licenciement |
| **21.2 / 21.3** | Durée légale 40h + heures supplémentaires |
| 23.1 / 23.6 | Registre employeur, immatriculation CNPS, travail dissimulé |
| **25.1 / 25.6** | Congés payés (2,2 j/mois) + allocation 1/12 |
| 31.4 / 31.8 | Mentions obligatoires rémunération + bulletin de paie |
| **33.6** | Prescription quinquennale des actions en paiement |
| 43.1 | Visite médicale d'embauche obligatoire |
| 71 et s. | Préavis et indemnité de licenciement |
| 81.1 et s. | Tribunal du Travail |

| Article CCI 1977 | Sujet |
|---|---|
| **13** | Période d'essai : 8 j (1ère cat.) / 1 mois (employés) / 3 mois (cadres) — renouvelable 1× |
| 15.7 | Non-concurrence avec contrepartie pécuniaire obligatoire |
| **22** | Préavis : 8 j (1ère) / 1 mois (employés) / 2 mois (maîtrise) / 3 mois (cadres) |
| 39 | Indemnité de licenciement : 30 % (≤5 ans), 35 % (6-10), 40 % (>10) |
| 54 | Structure rémunération (base catégoriel + sursalaire + primes + indemnités) |
| **Annexe IV** | Grille des salaires minima par catégorie |

## 7.3 Matrice d'anomalies systémiques (à vérifier sur tout contrat ivoirien)

11 critères de conformité standards :

1. **Salaire ventilé** (base catégoriel + sursalaire + primes individualisés) — sinon viole art. 31.4/54
2. **Sursalaire cohérent** (≤ rémunération totale et > 0 si déclaré)
3. **Durée 40 h respectée** (vérifier que les horaires énoncés totalisent bien 40 h)
4. **Période d'essai stipulée par écrit** (sinon non opposable)
5. **Non-concurrence avec contrepartie financière** (sinon nulle)
6. **Mobilité raisonnable** (limite géographique + proportionnalité au poste)
7. **Préavis chiffré** (par catégorie selon art. 22 CCI)
8. **N° d'immatriculation CNPS employeur** affiché
9. **Catégorie professionnelle précisée** (numéro + échelon + indice CCI)
10. **Date de signature ≥ date d'effet** (sinon antidatage = exécution sans contrat écrit)
11. **Visite médicale d'embauche** stipulée et non tronquée

Anomalies systémiques fréquemment constatées (cas TIM 7) :
- Salaire net uniforme à 75 000 FCFA pour toutes catégories (du commis au chef cuisinier)
- Sursalaire arithmétiquement incohérent (supérieur au total ou égal au total = base nulle)
- 44h annoncées comme 40h (samedi matin oublié dans le décompte)
- Clause d'objectifs potestative (« reconsidérer la poursuite » = contournement licenciement légitime)
- Visite médicale tronquée : « examen médical d'embauche **avant.** » (phrase interrompue)
- Lieu de travail contradictoire entre l'article 4 et la fiche de poste

## 7.4 Livrables types pour une mission « audit + régularisation contrats »

Architecture standard du dossier `AUDIT_CONTRATS_TRAVAIL/` du client :

| # | Livrable | Format | Référence MDC |
|---|---|---|---|
| 01 | **Rapport d'audit détaillé** (11 sections, fiche par contrat, matrice consolidée, plan d'action) | DOCX | MC-AUD-DT-AAAA-NNN |
| 02 | **Modèle de contrat type CDI conforme** (18 articles, période d'essai par catégorie, salaire ventilé, mobilité bornée, non-concurrence indemnisée) | DOCX | MC-MOD-CDI-AAAA-NNN |
| 03 | **Avenant de régularisation** (préambule motivé, modifications ciblées, renonciation réciproque sauf CNPS/DGI) | DOCX | MC-AVN-DT-AAAA-NNN |
| 04 | **Courrier d'accompagnement DG** (synthèse + tableau risques + plan d'action + proposition mission) | DOCX | MDC/AAAA/AUD-CLIENT/NNN |
| 05 | **Proposition Financière** mission de mise en conformité (3 axes) | DOCX | MC-PROP-AAAA-NNN (compteur global §6.3) |
| 06 | **Proposition Commerciale** suivi mensuel post-mission | DOCX | MC-PROP-AAAA-NNN (compteur global §6.3) |

Chiffrage type des trois axes (PME 9-15 salariés, secteur restauration / services) :
- Axe 1 — Régularisation contractuelle : 1 000 000 FCFA
- Axe 2 — Paie conforme + paramétrage + 3 mois : 1 200 000 FCFA
- Axe 3 — Sécurisation CNPS / AGEPE / Inspection : 800 000 FCFA
- Total brut **3 000 000 FCFA**, remise globale 500 000 FCFA, **net 2 500 000 FCFA**
- Suivi mensuel post-mission : **150 000 FCFA / mois**

## 7.5 Méthodologie d'analyse rapide (PDF volumineux)

Pour un dossier de plusieurs contrats consolidés en un seul gros PDF (cas TIM 7 : 64 pages, 8 contrats de 8 pages) :

1. `mcp__PDF_Tools_..._get_pdf_info` pour connaître nb de pages
2. `mcp__PDF_Tools_..._split_pdf` avec `page_ranges="every N"` (N = pages par contrat)
3. Lancer **N agents `general-purpose` en parallèle**, un par contrat, avec un prompt structuré exigeant :
   - Identification (nom, naissance, nationalité, pièce, situation)
   - Poste et catégorie
   - Rémunération chiffrée + ventilation + cohérence
   - Durée du travail
   - Clauses sensibles (essai, non-concurrence, mobilité, préavis)
   - Anomalies au regard du Code du travail + CCI
4. Consolider en matrice et synthèse exécutive

---

# 8. CHARTE GRAPHIQUE UNIFIÉE DES LIVRABLES MDC

Tous les livrables MDC (Word, Excel, PDF) doivent partager une identité visuelle cohérente : sobre, professionnelle, navy + or.

## 8.1 Palette de couleurs

| Rôle | Hex | Usage |
|---|---|---|
| Primaire (Navy MDC) | `#1A1A2E` | Bandeaux, headers de tableaux, titres principaux, totaux |
| Accent (Or MDC) | `#E8C547` | Bordures or, soulignement titres, mentions de valeur |
| Or pâle | `#F5E5A5` | Sous-totaux, encadrés crème |
| Crème | `#FFFBE8` | Citations, encadrés synthèse positive |
| Gris perle | `#F4F4F8` / `#F5F5FA` | Lignes paires des tableaux, fond pieds de page |
| Rouge alerte | `#C0392B` | Notes négatives, anomalies critiques, montants débit signalés |
| Rouge clair | `#F8E8E8` | Encadré « réserves » / « non délivré » |
| Vert validation | `#27AE60` | OK, ✅, conformité |
| Bleu nuit Débit | `#0F3D5C` | Colonne Débit dans journaux comptables |
| Bordeaux Crédit | `#6B0F3D` | Colonne Crédit dans journaux comptables |

## 8.2 Typographie

- **Corps de texte** : Times New Roman 11 pt (rapports, propositions, contrats)
- **Titres et tableaux** : Calibri (sans serif) — H1 18 pt, H2 14 pt, H3 12 pt
- **Tableaux Excel** : Calibri 10 pt, header 11 pt gras blanc
- **Pied de page** : Calibri 8-9 pt italique gris
- **Interligne** : 1,15 ; **justification** corps en justify

## 8.3 Bandeau d'en-tête MDC (à apposer en haut de chaque livrable)

```
┌──────────────────────────────────────────────────────────┐
│  Fond #1A1A2E  •  Texte or #E8C547                       │
│      LA MAISON DE LA CONFORMITÉ SARL                     │
│  Agence de Notation Administrative — Comptable ·        │
│  Fiscal · Social —                                       │
│              Côte d'Ivoire (sous-titre blanc italique)   │
│  ─────── Bordure inférieure 4-5 px or #E8C547 ───────    │
└──────────────────────────────────────────────────────────┘
```

## 8.4 Pied de page MDC standard

```
─── Bordure supérieure 2-3 px navy #1A1A2E ───
LA MAISON DE LA CONFORMITÉ SARL  |  NCC : 2506426B  |
RCCM : CI-ABJ-03-2025-B13-10831  |  Capital : 1 000 000 FCFA
Tél : 07 19 31 49 04  |  lamaisondelaconformitesarl@outlook.com
www.lamaisondelaconformitesarl.net
(fond #F5F5FA, texte gris #444 italique 8.5 pt centré)
```

## 8.5 Règles de mise en forme par type de tableau

| Type | Header | Lignes paires | Lignes impaires | Total |
|---|---|---|---|---|
| Tableau de données | Fond navy / texte blanc gras | Fond `#F4F4F8` | Fond blanc | Fond navy / texte blanc gras |
| Sous-total (Excel) | — | — | — | Fond or pâle `#F5E5A5` / texte navy gras |
| Tableau key-value | Première colonne navy gras / valeurs gris foncé | — | — | — |
| Synthèse exécutive | Fond crème ou gris perle, barre or à gauche | — | — | — |

## 8.6 Format monétaire FCFA (Excel)

Toujours utiliser : `#,##0_- "FCFA";[RED]-#,##0_- "FCFA";"-"`
- Séparateur de milliers : espace
- Devise : « FCFA » à droite (UEMOA standard)
- Négatifs en rouge
- Tirets pour les valeurs nulles

## 8.7 Mentions obligatoires dans tout livrable

- Référence MDC normalisée : `MC-[TYPE]-[SECTEUR]-[ANNÉE]-[NNN]`
- Date d'émission en français long (ex : « Abidjan, le 1er mai 2026 »)
- TVA : « Le Agence MDC n'est pas assujetti à la TVA. Tout montant net de toute taxe. »
- Confidentialité : « Document confidentiel — destiné exclusivement à [CLIENT] »
- Signature MDC : « M. BILE Fils Séverin — Gérant »

---

# 9. SCRIPTS UTILITAIRES PERSISTANTS

Les scripts suivants sont sauvegardés dans `~/.claude/skills/mdc-expert/scripts/` et sont à réutiliser pour tout livrable client futur :

## 9.0 GÉNÉRATEURS STANDARD MDC (en-tête/pied + emphases) — À UTILISER PAR DÉFAUT

> **⚠️ RÈGLE ABSOLUE — Décision gérant juillet 2026 : LOGO MDC sur CHAQUE document produit + FILIGRANE « CONFIDENTIEL ».** Tout livrable client (Word, PDF, Excel) porte le logo `scripts/logo-mdc.jpg` dans l'en-tête de chaque page ET un filigrane « CONFIDENTIEL » en diagonale (navy ~6-7 % d'opacité, sous le contenu). Les trois générateurs (`build_mdc_docx_hf.py`, `build_mdc_pdf.py`, `generate_livrable_mdc.py`) l'intègrent nativement depuis le redesign de juillet 2026 — ne jamais revenir au bandeau texte seul.
>
> **Conditions de paiement par défaut des propositions : paiement intégral avant le démarrage des travaux** (décision gérant, confirmée sur GLOBAL PRESTIGE juillet 2026) — pas d'acompte fractionné sauf instruction contraire.

> **⛔ RÈGLE D'OR — Décision gérant juillet 2026 (GLOBE CÔTE D'IVOIRE) : AUCUN livrable Word n'est remis sans avoir passé le contrôle qualité automatique. S'il ne passe pas, on ne produit PAS le document.** Tout Word client passe désormais par le pipeline **`publish_livrable_mdc.py`** (générateur soigné **`md2docx_mdc.js`** en docx-js + contrôle bloquant) :
> ```bash
> NODE_PATH=$(npm root -g) python3 ~/.claude/skills/mdc-expert/scripts/publish_livrable_mdc.py SOURCE.md DEST.docx "Titre" "Client" "Réf"
> ```
> Le script génère en **fichier tampon**, exécute 6 contrôles — (1) génération docx-js sans erreur, (2) structure lisible, (3) **zéro symbole Markdown résiduel** (`**`, `*`, `##`, `](`), (4) tableaux rendus si la source en contient, (5) **logo embarqué**, (6) **rendu QuickLook OK** (`qlmanage -t`) — et **ne copie vers la destination QUE si TOUT passe**. Au moindre échec : **aucun fichier produit** + rapport d'échec, on corrige la source puis on relance. **Volet PDF** : même règle d'or via **`publish_pdf_mdc.py`** (générateur `build_mdc_pdf.py` reportlab, logo + **filigrane CONFIDENTIEL** + tables navy/or ; contrôle : pages, logo, zéro Markdown résiduel, rendu PyMuPDF) — `python3 ~/.claude/skills/mdc-expert/scripts/publish_pdf_mdc.py SOURCE.md DEST.pdf "Titre" "Client" "Réf"`. Le générateur `md2docx_mdc.js` produit le rendu « papier à en-tête cabinet » (en-tête à logo + double filet navy/or, bandeau-titre navy/or, titres à filet or, tableaux navy à lignes alternées, montants à droite, lignes TOTAL sur or pâle, encadrés crème `>`, pied légal + pagination) et gère `**gras**`, `*italique*`, `***gras+italique***`, `> callout`, tableaux, puces, `<br>`. **Prérequis** : Node + module `docx` global (`npm root -g`) ; macOS `qlmanage` pour le rendu. Précédent : dossier GLOBE CÔTE D'IVOIRE (rapport + 2 notes + bordereaux + manuel, tous passés au contrôle).

Deux générateurs produisent les livrables clients (contrats, propositions, notes) avec **tête de lettre à LOGO répétée sur CHAQUE page** (logo à gauche, identité Agence à droite, double filet navy/or), pied de page légal, et des **blocs signature + cachet**. Design « papier à en-tête cabinet » (redesign juillet 2026, validé sur GLOBAL PRESTIGE) : titres centrés à filet or, sous-titres soulignés or, tableaux SANS grille verticale (filets horizontaux fins, en-tête navy, montants alignés à droite, lignes TOTAL détectées automatiquement sur fond or pâle `F5E5A5`) :

```bash
python3 ~/.claude/skills/mdc-expert/scripts/build_mdc_docx_hf.py SOURCE.md DEST.docx   # Word (vrais header/footer)
python3 ~/.claude/skills/mdc-expert/scripts/build_mdc_pdf.py  SOURCE.md DEST.pdf        # PDF (reportlab, header/footer par page)
```

**Markdown supporté (rendu propre, AUCUN symbole apparent dans le livrable)** :
- `*italique*` → italique
- `**gras**` → gras
- `***gras + italique***` → gras + italique
- `> citation` → **encadré crème/or** (callout), le `>` n'apparaît jamais
- `<br>` → saut/espace (utile pour les zones de signature)

**RÈGLE ABSOLUE — aucun symbole Markdown visible dans les livrables** (`*`, `>`, `#`, etc.). Si un symbole apparaît en clair dans un PDF/Word généré, c'est un bug du générateur à corriger, pas à laisser passer.

**Convention mention TVA** : toujours écrire la mention en **gras + italique**, soit `***Le Prestataire n'est pas assujetti à la TVA. ...***` (et non `*...*`).

**Espace de signature** : insérer des lignes `<br>` (gérées comme sauts) pour créer la zone « Signature et cachet : » suivie d'une ligne `______`.

**Rangement** : après génération dans `Desktop/MON JURISTE/`, copier dans `Documents/DOSSIER CLIENTS/<CLIENT>/` (cf. règle de rangement).

## 9.1 `md_to_docx_mdc.py` — Conversion Markdown → Word format MDC

Convertit n'importe quel fichier `.md` en `.docx` avec :
- Bandeau MDC navy/or en haut
- Pied MDC complet en bas
- Titres H1 soulignés double or, H2 avec barre verticale or
- Tables avec header navy + lignes alternées
- Citations sur fond crème + barre or à gauche

Usage :
```bash
python3 ~/.claude/skills/mdc-expert/scripts/md_to_docx_mdc.py SOURCE.md DEST.docx
```

Pré-requis : `pip install markdown` + `textutil` (macOS, déjà installé)

## 9.2 `redesign_excel_mdc_template.py` — Template de redesign Excel

Patron pour appliquer la charte MDC à un fichier Excel existant. À adapter au cas par cas :
- Bandeau de marque sur 3 lignes (MDC + titre + sous-titre)
- Headers de tableaux navy/blanc
- Lignes alternées blanc / `#F4F4F8`
- Sous-totaux or pâle, totaux navy
- Format FCFA `#,##0_- "FCFA"` partout
- Volets figés sous les en-têtes
- Contrôle d'équilibre Σ Débit = Σ Crédit dans journaux comptables
- Pied MDC en bas de chaque feuille

## 9.3 `build_mdc_propositions_template.py` — Word natifs format MDC

Génération directe via `python-docx` (sans textutil) pour propositions financière et commerciale :
- A4, marges 2,5 cm, Times New Roman 11 pt
- Header courant : `LA MAISON DE LA CONFORMITÉ SARL | <titre>`
- Pied courant complet (NCC, RCCM, contact)
- Tableaux montants : header navy, lignes alternées, total navy
- Helpers : `setup_document()`, `add_title()`, `add_section_title()`, `add_body()`, `add_bullet()`, `add_kv_table()`, `add_amount_table()`

## 9.4 PDF design via `mcp__Desktop_Commander__write_pdf`

Pour les rapports d'audit / révision en PDF, utiliser le tool `write_pdf` avec markdown étendu HTML/CSS inline. Inclure :
- Bandeau navy/or en marge négative `margin:-30px -30px 24px -30px`
- Encadrés colorés (synthèse, alerte) avec barre verticale
- Score visible en grand corps (42 pt)
- Pied MDC sur fond gris perle bordure navy
- Page break : `<div style="page-break-before:always;"></div>`

## 9.5 ⭐ `xlsx_to_pdf_mdc.py` — Conversion Excel → PDF aux couleurs MDC

```bash
python3 ~/.claude/skills/mdc-expert/scripts/xlsx_to_pdf_mdc.py SOURCE.xlsx [DEST.pdf]
```

**Pourquoi** : LibreOffice est absent du poste et **Microsoft Excel refuse l'export PDF par AppleScript** (erreur de paramètre −50). Ce convertisseur maison (openpyxl + reportlab) est donc la voie fiable pour livrer un classeur en PDF.

**Ce qu'il fait** : un onglet = une page ; bandeau MDC navy en tête ; nom du classeur et de l'onglet ; valeurs formatées (séparateur de milliers, négatifs entre parenthèses) ; gras conservé ; lignes alternées ; largeurs de colonnes proportionnelles au contenu ; **paysage A4, bascule automatique en A3 au-delà de 12 colonnes** (indispensable pour les grilles déclaratives larges) ; pied de page MDC.

**Batch** : boucler sur `glob.glob(dossier+"/**/*.xlsx", recursive=True)` en excluant les fichiers de verrouillage `~$`. Livrer systématiquement le PDF **à côté** de son classeur.

---

# 10. RÈGLE D'OR : TOUTE NOUVELLE COMPÉTENCE EST CAPITALISÉE ICI

Quand une mission révèle une expertise réutilisable (méthodologie, référentiel juridique, charte de livrable, script utilitaire), elle doit être **immédiatement consignée dans le présent SKILL.md** et les scripts associés sauvegardés dans `~/.claude/skills/mdc-expert/scripts/`.

Précédent capitalisé : Mission TIM 7 MULTISERVICE (mai 2026) → Section 7 (Audit contrats de travail) + Section 8 (Charte graphique unifiée) + Section 9 (Scripts utilitaires).

Précédent capitalisé : Refonte génération documentaire CRM (mai 2026) → Section 11.

---

# 11. GÉNÉRATION DOCUMENTAIRE AUTOMATISÉE — PLATEFORME CRM (`docgen.js`)

Compétence capitalisée à la suite de la refonte des documents commerciaux d'audit dans le CRM (validée par le client : « le rendu est impeccable »). La plateforme `lamaisondelaconformitesarl.net/admin` génère désormais les documents au niveau des modèles de référence (NOTE MÉTHODOLOGIQUE SOFT SECURITY, PROPOSITION FINANCIÈRE ST EXUPÉRY).

## 11.1 Emplacements techniques

| Élément | Chemin |
|---|---|
| Générateur Word | `/var/www/crm/backend/docgen.js` (repo `CRM-mdc`) |
| Endpoint | `POST /api/documents/generate` (server.js) — `{cid, type, fields}` |
| Front (formulaire) | `/var/www/mdc/admin/index.html` → modal « Protocole Documents » |
| Types | `note_methodologique`, `proposition_financiere`, `contrat`, `proposition_commerciale` |

## 11.2 RÈGLE CRITIQUE — Prix audit ≠ tarif mensuel

Le bug historique : la Proposition Financière utilisait `tarif_mensuel` (prix consultation/suivi) au lieu du prix d'audit. **Corrigé** :
- Champ frontend dédié **« 💰 Prix de l'AUDIT (FCFA) »** → `fields.montant_audit`
- Ordre de priorité backend : `fields.montant_audit` → 1er `prestation_passagere.tarif` → `prestation_passagere_tarif`. **JAMAIS `tarif_mensuel`** pour un audit.
- Champ frontend **« ⏱ Délai / Durée de la mission »** (sélecteur, ex-« Durée (mois) ») → `fields.delai_audit` : valeurs texte « une (1) semaine », « deux (2) semaines », « trois (3) semaines », « un (1) mois », « une (1) à quatre (4) semaines », « 3 mois », « 6 mois », « 12 mois ». Audit = 1 semaine→1 mois ; suivi/contrat = 3→12 mois.

## 11.3 Profils sectoriels — `sectorProfile(sector)` dans docgen.js

Adapte automatiquement contexte, bullets fiscal/travail, processus, accès, confidentialité. 7 profils (regex sur le secteur client) :

| Code | Déclencheurs regex | Secteur |
|---|---|---|
| SEC | `s[ée]curit\|gardiennage\|surveillance` | Sécurité privée |
| EDUC | `enseign\|[ée]cole\|coll[èe]ge\|lyc[ée]e\|universit\|[ée]ducat\|scolaire\|institut` | Enseignement |
| TRANSP | `transport\|logistiq\|fret\|v[ée]hicul\|taxi\|livraison` | Transport/logistique |
| BTP | `b[âa]timent\|btp\|construction\|travaux\|g[ée]nie civil\|immobili` | BTP |
| SANTE | `sant\|clinique\|pharmac\|m[ée]dic\|h[ôo]pital\|laboratoire` | Santé |
| HORECA | `restaur\|h[ôo]tel\|tourism\|bar\|caf[ée]\|traiteur` | Hôtellerie-restauration |
| GEN | (défaut) | Générique |

Chaque profil expose : `code`, `contexte` (phrase), `fiscalBullet`, `travailBullet`, `processus`, `acces`, `confidentialite`. Référence doc : `MC-NOTE-[code]-[année]-NNN` / `MC-PROP-[code]-[année]-NNN`.

## 11.4 Structure NOTE MÉTHODOLOGIQUE générée (modèle SOFT SECURITY)

1. Titre or `C9A227` : « NOTE MÉTHODOLOGIQUE D'AUDIT DE CONFORMITÉ ADMINISTRATIVE » + « LA CONFORMITÉ [CLIENT] »
2. En-tête : Société / Secteur / Référence / Date / Délai de réalisation
3. **CONTEXTE ET OBJECTIFS** : Contexte (sectoriel) + 4 Objectifs Généraux
4. **DOMAINES D'ÉVALUATION PRIORITAIRES** : 5 domaines × 5 puces (CNPS, Fiscale [bullet sectoriel], Inspection du Travail, Comptable, Droit du Travail [bullet sectoriel])
5. **PHASES DE L'AUDIT** : 4 phases (Diagnostic / Audit détaillé / Analyse processus / Synthèse) — Objectif + puces
6. **OUTILS ET MÉTHODES** : Outils d'Évaluation / Méthodes de Vérification / Approche Qualité
7. **LIVRABLES** : Rapport Intermédiaire / Détaillé par Domaine / Analyse Processus / Plan d'Action Stratégique / Présentation Exécutive
8. **GARANTIES MÉTHODOLOGIQUES** : Objectivité / Confidentialité / Professionnalisme / Valeur Ajoutée

## 11.5 Structure PROPOSITION FINANCIÈRE générée (modèle ST EXUPÉRY)

1. Titre or : « PROPOSITION FINANCIÈRE – AUDIT DE LA CONFORMITÉ – [CLIENT] »
2. En-tête : Destinataire (Direction de…) / Référence MC-PROP / Date (FR long majuscules) / Objet / **Validité : 7 jours**
3. **1. RAPPEL DU PÉRIMÈTRE** : 3 puces (5 domaines + processus sectoriels + livrables)
4. **2. PROPOSITION FINANCIÈRE** : vrai tableau docx (header navy `1A1A2E`, 2 col Prestation|Montant) — montant = `montantAudit` formaté `fmtMontantDot` (points : `6.000.000`) + Conditions de paiement + Ce montant forfaitaire inclut + mention TVA
5. **3. CONDITIONS DE RÉALISATION** : Accès (sectoriel) / Période 3 exercices / Délai de réalisation / Confidentialité (sectorielle)
6. **4. PROCHAINES ÉTAPES** : 3 étapes numérotées (étape 3 inclut le délai)

## 11.6 Helpers docgen.js réutilisables

- `fmtMontantDot(n)` : format milliers avec points (`6.000.000`) — standard propositions
- `sectorProfile(sector)` : profil sectoriel complet
- `sectionBullets(title, items)` : titre gras 24 + puces « ·  » indentées
- Tableau docx : `new Table` + `TableCell` shading navy header `1A1A2E`, texte blanc, % widths

## 11.7 Procédure de déploiement docgen

```bash
node -c docgen.js                       # check syntaxe (docx absent en local = normal)
rsync docgen.js → /var/www/crm/backend/
ssh VPS: cd /var/www/crm/backend && node -e "require('./docgen.js').generatePropositionFinanciere({...}).then(b=>console.log(b.length))"   # smoke test (module docx présent sur VPS)
pm2 restart mdc-crm
git: CRM-mdc (docgen.js) + site-mdc (admin/index.html), branche vps-baseline
```

---

# 12. ANALYSE D'OPÉRATIONS COMPTABLES À PARTIR D'UNE BALANCE

Compétence renforcée à partir du **Guide d'application du SYSCOHADA** (édition révisée, 437 pages) et de **« Les nouveautés du plan comptable révisé de l'OHADA »** (Loé-Mié & Tari, L'Harmattan 2018, 635 pages). Sources consultables localement :
- `/Users/bilefilsseverin/Downloads/Guide-d-application-du-SYSCOHADA.pdf`
- `/Users/bilefilsseverin/Desktop/Compta OHADA/Nouveautés du plan comptable révisé OHADA.pdf`

Objectif : à partir d'une balance comptable client, produire pour **chaque ligne** une explication structurée (nature, opération économique, contrepartie probable, lecture du solde, alertes).

## 12.1 Méthodologie en 7 étapes — Lecture analytique d'une balance

1. **Identifier la nature du compte** (classe SYSCOHADA + position dans le PCGE)
2. **Vérifier le sens normal du solde** (D pour Actifs/Charges, C pour Passifs/Produits)
3. **Déduire l'opération économique** sous-jacente (achat, vente, paie, paiement…)
4. **Reconstituer la contrepartie probable** (cf. table de correspondance §12.4)
5. **Mesurer la matérialité** (poids relatif vs CA, vs Total Bilan)
6. **Détecter les anomalies** (sens inversé, soldes incohérents, triangles MDLC qui ne ferment pas)
7. **Formuler la recommandation** (régularisation, lettrage, justification à demander)

## 12.2 Grille de lecture systémique par classe SYSCOHADA

### Classe 1 — Ressources durables (sens normal : Créditeur)

| Compte | Intitulé | Sens normal | Opération économique typique | Contrepartie typique | Lecture du solde / alertes |
|---|---|---|---|---|---|
| **101** | Capital social (1011 non appelé / 1012 appelé non versé / 1013 appelé versé non amorti / 1014 amorti) | C | Constitution, augmentation/réduction, amortissement de capital | 4611/4612 (apports), 109, 4619 | Doit correspondre aux statuts (PV AGE) — variation sans AGE = anomalie CRITIQUE |
| 1031 | Résultat exercice (PP/EI) | D ou C | Solde des classes 6/7 en clôture | 6xxx / 7xxx | PP uniquement, jamais en PM |
| 104 | Compte de l'exploitant (PP) | C (normalement) | Apports/retraits gérant | 521/571 | Solde D = retraits > apports (risque qualification distribution) |
| 105 | Primes liées au capital (1051 émission / 1052 fusion / 1053 apport) | C | Augmentation de capital à prix > nominal | 4615, 4611 | Doit suivre une augmentation de capital |
| 111 | Réserve légale (PM : 10% bénéfice tant que < 20% capital — art. SCSA 346) | C | Affectation du résultat | 1301 (bénéfice) | SARL avec bénéfice et 111=0 ⇒ anomalie RESERVE-LEGALE-N |
| 112 | Réserves statutaires | C | Affectation selon statuts | 1301 | |
| 118 | Réserves diverses / facultatives | C | Affectation libre AGO | 1301 | |
| 121 / 129 | Report à nouveau créditeur / débiteur | C / D | Reliquat non affecté | 1301/1309 | RAN- persistant ⇒ surveiller continuité (AUPCAP art. 25) |
| 1301 / 1309 | Résultat en instance d'affectation : Bénéfice / Perte (PM) | C / D | Clôture, en attente de décision AGO | 6xxx / 7xxx puis 111/118/465/121 | Doit être soldé après AGO (max 6 mois après clôture) |
| **14** | Subventions d'investissement (1411 Etat, 1412 Région…) | C | Octroi subvention liée à actif | 4494/4495 | Reprise 799 sur durée d'amortissement |
| **151** | Amortissements dérogatoires | C | Différence amort. fiscal > économique | 851 (dot) / 861 (reprise) | Provision règlementée HAO |
| 16 | Emprunts (162 banques, 163 obligataires, 164 sur location-acquisition…) | C | Encaissement emprunt, remboursement principal | 521 | Variation = (nouveaux − remboursements capital). Cohérence avec 671 |
| 17 | Dettes de location-acquisition | C | Activation contrat de location (révision OHADA) | 2xx | Nouveau au SYSCOHADA révisé — IFRS 16 like |
| 19 | Provisions pour risques et charges (>1 an) | C | Dotation provision long terme | 6911 / 691 / 851 | Doit reposer sur un événement passé documenté |

### Classe 2 — Actif immobilisé (sens normal : Débiteur, sauf amort/dépréciations 28/29 créditeurs)

| Compte | Intitulé | Sens | Opération typique | Contrepartie | Alertes |
|---|---|---|---|---|---|
| 211 | Frais de recherche/développement (capitalisables) | D | Activation projet R&D conforme art. 46 AU | 404/521 | Justifier critères de capitalisation |
| 212-218 | Brevets, licences, marques, logiciels, sites internet, fonds commercial | D | Acquisition / production interne | 404/481 | Logiciels : amort 1-5 ans / Fonds commercial : non amorti, test dépréciation |
| 222 | Terrains nus | D | Acquisition foncière | 481/4812 | Non amortissable |
| 231 | Bâtiments industriels, agricoles, commerciaux | D | Construction / acquisition | 481/4812 | Amort. 10-50 ans (approche par composants §SYSCOHADA Chap.4) |
| 234 | Mobilier | D | Acquisition | 401/481 | Amort. 5-10 ans |
| 2441 | Matériel informatique | D | Acquisition | 401/481 | Amort. 3-5 ans |
| 245 | Matériel de transport | D | Acquisition véhicule | 481 | Amort. 4-5 ans linéaire ou dégressif fiscal |
| 26 / 27 | Titres de participation / Autres immo. financières (prêts, dépôts) | D | Souscription, prêt accordé | 521, 4726 | 26 ≥ 10% capital filiale ; sinon 271 |
| **28** | Amortissements (281-284) | **C** | Constatation usure annuelle | 681 (ou 852 HAO) | Variation N − N-1 = dotation de l'exercice. Égalité avec 681 = test bilan/CR |
| **29** | Dépréciations actif immobilisé | **C** | Perte de valeur (test impairment) | 691/697/853 | Réversible — reprise 791/797/863 |

### Classe 3 — Stocks (sens normal : Débiteur)

| Compte | Intitulé | Variation enregistrée en |
|---|---|---|
| 31 | Marchandises | 6031 (variation) |
| 32 | Matières premières et fournitures liées | 6032 |
| 33 | Autres approvisionnements | 6033 |
| 34 | Produits en cours | 734 |
| 35 | Services en cours | 735 |
| 36 | Produits finis | 736 |
| 37 | Produits intermédiaires et résiduels | 737 |
| 38 | Stocks en cours de route, en consignation, en dépôt | — |
| 39 | Dépréciations des stocks | **C** — contrepartie 6593 (charges) / 7593 (reprise) |

**Triangle Variation stocks** : SF − SI = variation. Cohérence avec compte 603 (entrée en RB) ou 73 (entrée en VA).

### Classe 4 — Tiers (sens variable selon nature actif/passif)

| Compte | Intitulé | Sens normal | Opération typique | Contrepartie | Alertes |
|---|---|---|---|---|---|
| 401 | Fournisseurs d'exploitation | C | Facture reçue ; règlement annule | 60x à 63x ; 521/571 | Solde D anormal (avoir non régularisé) |
| 4011 | Fournisseurs dettes en compte | C | Idem ventilé | 60x | |
| 404 | Fournisseurs, acquisitions courantes d'immobilisations | C | Acquisition immo réglée à court terme | 21-24 | |
| 408 | Fournisseurs, factures non parvenues | C | FNP fin exercice | 60x | Régularisation à extourner J+1 |
| 409 | Fournisseurs débiteurs (avances versées, RRR à obtenir) | D | Avances, avoirs en attente | 521, 601-9 | |
| 411 | Clients | D | Facture émise ; encaissement annule | 70x ; 521/571 | Solde C = avance client (compte 419) |
| 416 | Clients douteux ou litigieux | D | Reclassement après défaut | 411 | À déprécier en 491 |
| 418 | Clients, produits non encore facturés | D | PNF fin exercice | 70x | Régularisation à extourner J+1 |
| **419** | Clients, avances et acomptes reçus | C | Avance reçue avant livraison | 521 | Apparait en passif courant |
| 4211 | Personnel, avances | D | Avance avant prestation | 521/571 | À récupérer sur paie suivante |
| 4212 | Personnel, acomptes | D | Acompte après prestation, avant bulletin | 521/571 | Imputé sur net à payer (422) |
| **422** | Personnel, rémunérations dues (NET À PAYER) | C | Bulletin de paie | 661/662/663 | Solde = net à payer en fin de période |
| 423 | Personnel, oppositions, saisies-arrêts | C | Retenue saisie sur paie | 422 | À reverser au tiers saisissant |
| 425 | Représentants du personnel | C | Cotisations syndicales retenues | 422 | |
| 4271 | Personnel, dépôts reçus | C | Cautions logement de fonction etc. | 521 | |
| **431** | Sécurité sociale (CNPS) | C | Patronale + salariale | 422 (sal) + 664 (patron) | Cohérence : 431 ≈ 6,3% (sal) + 16,4% (pat) × brut |
| 432 | Caisses de retraite complémentaire | C | Mutuelle/IPRES | 664/422 | |
| 433 | Autres organismes sociaux (médecine du travail…) | C | | 664 | |
| **4426** | État, droits de douane | C | Importation : droits d'entrée | 23/24/60 | Composante du coût d'achat |
| 4431 | État, TVA facturée sur ventes | C | Vente B2B | 411 | Centralisée en 4441 |
| 4432 | État, TVA facturée sur prestations de services | C | Facturation services | 411 | |
| 4451 | État, TVA récupérable sur immobilisations | D | Achat immo | 481 | |
| 4452 | État, TVA récupérable sur achats | D | Achat consommables | 401 | |
| 4453 | État, TVA récupérable sur transport | D | Facture transport | 401 | |
| **4441** | État, TVA due | C | Fin de période : 443 − 445 | 443/445 | À régler au mois M+1 |
| **4449** | État, crédit de TVA à reporter | D | TVA récup. > TVA collectée | 4441 | Reportable sur exercice suivant |
| **441** | État, impôt sur les bénéfices | C ou D | Acomptes (D), liquidation IS (C) | 521 ; 891 | Solde C = solde IS à payer ; D = crédit IS |
| **442** | État, autres impôts directs | C | Patente, impôt foncier | 64x | |
| **446** | État, autres taxes sur le CA (TEE, Impôt Synthétique) | C | Taxe État Entreprenant | 6418 | CI : TEE ≤ 50M négoce/services |
| 4471 | État, impôts retenus à la source (IRSA, BNC, BIC retenu) | C | Retenue tiers | 401 (sur paiement fournisseur) | |
| **4472** | État, impôts sur salaires (ITS) | C | Retenue salariale ITS | 422 | CI : compte 447202 |
| 4473 | État, IS retenu | C | | | |
| **4478** | État, autres impôts et taxes (FDFP CI : TA + TFPC) | C | FDFP CI 1% du brut | 6414/6415 | |
| 4486 | État, obligations cautionnées (douanes en délai) | C | Crédit d'enlèvement douanier | 4426 | |
| 449 | État — créances pour subventions/remboursements (4494/4495/4496) | D | Subvention notifiée | 14xx, 711-718, 881 | |
| 45 | Organismes internationaux | C ou D | Cotisations / subventions | 64 / 71/88 | |
| 461 | Apporteurs / Associés (4611-4615, 4619) | D ou C | Apports, augmentation, remboursement capital | 101x, 521 | |
| 465 | Associés — Dividendes à payer | C | Affectation résultat AGO | 1301 | Mise en paiement = D 465 / C 521 |
| 471-478 | Comptes d'attente, transitoires, suspens | D ou C | Opérations en attente d'imputation | divers | **DOIT être soldé à clôture** sinon ALERTE |
| 476 | Charges constatées d'avance (CCA) | D | Régul. fin exercice : charge ≠ exercice | 60-63 | |
| 477 | Produits constatés d'avance (PCA) | C | Idem côté produits | 70-77 | |
| 481 | Fournisseurs d'investissements (>1 an) | C | Achat immo crédit long terme | 21-24 | |
| 485 | Créances sur cessions d'immobilisations | D | Cession en attente d'encaissement | 822 | |
| 49 | Dépréciations de tiers | C | Créance douteuse | 6594 / 7594 | 491 clients, 497 débiteurs divers |

### Classe 5 — Trésorerie (sens normal : Débiteur, sauf concours bancaires courants 561 créditeur)

| Compte | Intitulé | Sens | Opération | Contrepartie | Alerte |
|---|---|---|---|---|---|
| 50 | Titres de placement (52 VMP rév.) | D | Achat actions/OPCVM | 521 | Dépréciation en 590 |
| 521 | Banques (locales en monnaie nationale) | D | Tous flux bancaires | 401, 411, 422, 44, 16, 571… | Doit = dernier relevé bancaire signé |
| 524 | Banques (établissements étrangers / devises) | D | Idem en devises | + 676 écarts conv. | |
| 531 | Chèques postaux | D | | | |
| 53 | Instruments de monnaie électronique (Wave, Orange Money, MoMo) — révision OHADA | D | Encaissements/décaissements mobile money | 411, 401 | Subdivisé par opérateur |
| 56 | Banques, crédits de trésorerie et d'escompte (561 escompte, 564 découvert) | C | Découvert, billets escomptés | 521 | Charges d'intérêts en 671 |
| 571 | Caisse en monnaie nationale | D | Mouvements espèces | 411, 401, 422, 422 | Solde D obligatoire (caisse négative = anomalie CRITIQUE) ; cohérence triangle MDLC |
| 581 | Virements internes | D ou C | Transferts banque ↔ caisse | 521/571 | DOIT être soldé en clôture |
| 59 | Dépréciation titres de placement | C | | 6795 / 7795 | |

### Classe 6 — Charges (sens normal : Débiteur)

| Compte | Intitulé | Opération typique | Contrepartie typique |
|---|---|---|---|
| 601 | Achats marchandises (1=négoce zone, 2=hors zone) | Achat pour revente en l'état | 401 |
| 602 | Achats matières premières et fournitures liées | Achat MP destinée transformation | 401 |
| 604 | Achats matières et fournitures consommables (stockées) | Petit outillage, fournitures | 401 |
| 605 | Autres achats (non stockés : eau, électricité, fourn. bureau) | Consommation immédiate | 401 |
| 6051 | Fournitures non stockables (eau, électricité, gaz) | Factures SODECI, CIE | 401 |
| 6055 | Fournitures de bureau non stockables | | 401 |
| 608 | Achats d'emballages | | 401 |
| 6019, 6029…9 | RRR obtenus sur achats (terminaison 9) | Avoir reçu fournisseur | 401 |
| **603** | Variations de stocks (6031 m'ses, 6032 MP, 6033 autres) | Inventaire fin exercice (signe selon variation) | 31, 32, 33 |
| 61 | Transports (614 personnel, 611 sur achats, 612 sur ventes) | Transporteur tiers | 401 |
| 62 | Services extérieurs A (621-625 liés aux immo : locations, entretien, primes assurance, études, documentation) | Services rattachés aux immo | 401 |
| **622** | Locations et charges locatives | Loyer immeubles | 401 |
| 6241 | Entretien et réparations | | 401 |
| 625 | Primes d'assurances | | 401 |
| 626 | Études, recherches, documentation | | 401 |
| 627 | Publicité, publications, relations publiques | | 401 |
| 628 | Frais de télécommunications | | 401 |
| 63 | Services extérieurs B (631-637) — frais d'exploitation tertiaires | | 401 |
| 6311 | Frais bancaires (commissions de tenue de compte, agios) | Prélèvement banque | 521 |
| **6313 / 6413** | Impôts sur salaires — charges patronales (CN 1,2 % local + CE 9,2 % expat ; FDFP TA/TFPC → 6414/6415→4478). *6413 = SYSCOHADA strict ; 6313 = usage Sage-CI* | Déclaration paie | 447201 |
| 6321 | Honoraires (avocats, experts comptables, consultants) | Facture honoraires | 401 + 4471 retenue |
| 6322 | Frais d'actes et de contentieux | | 401 |
| 6324 | Honoraires des professions règlementées (notaires…) | | 401 |
| 637 | Rémunérations de personnel extérieur (intérim) | Facture agence intérim | 401, transféré en 667 |
| 64 | Impôts et taxes (autres que sur salaires et IS) | | 442/446 |
| **6414** | FDFP — Taxe d'apprentissage (0,40% brut effectif en CI) | Déclaration mensuelle | 4478 |
| **6415** | FDFP — Formation Professionnelle Continue (0,60% mensuel) | Déclaration mensuelle | 4478 |
| **6418** | Autres impôts et taxes directs (TEE en CI) | Déclaration TEE/IS mensuelle | 446 |
| 645 | Impôts et taxes indirects | TVA non récupérable | 4452 |
| 646 | Droits d'enregistrement | | 442 |
| **647** | Pénalités, amendes fiscales | Notification redressement | 446/441 |
| 65 | Autres charges (651 pertes sur créances, 654 dons, 659 charges pour dépréciations) | | divers |
| **6591/6593/6594** | Charges pour dépréciations (clients/stocks/créances) | Inventaire fin exercice | 391, 491 |
| 66 | Charges de personnel | | 422, 431, 432 |
| **6611** | Appointements et salaires personnel national | Bulletin de paie | 422 |
| 6612 | Primes et gratifications | | 422 |
| 6617 | Avantages en nature (régul fin exercice) | OD clôture | 781 |
| 6618 | Indemnité de logement, transport… | | 422 |
| 663 | Indemnités forfaitaires versées au personnel | | 422 |
| **6641** | Charges sociales sur rémunération personnel national (patronale CNPS) | Déclaration mensuelle | 431, 432 |
| 6642 | Charges sociales sur rémunération personnel non national | | 431 |
| 6661 | Rémunération du travail de l'exploitant (PP) | Salaire fictif EI | 422 ou 104 |
| 6662 | Charges sociales de l'exploitant individuel | | 431 |
| 667 | Rémunération transférée de personnel extérieur | Régul fin exercice | 637 (crédit) |
| 67 | Frais financiers et charges assimilées | | 521, 16, 56 |
| **671** | Intérêts des emprunts (banques) | Échéance emprunt (part intérêts) | 521 |
| 672 | Intérêts dans loyers de crédit-bail / location-acquisition | | 521 |
| 674 | Autres intérêts (sur découvert, escompte) | | 56 |
| 676 | Pertes de change | Règlement créance/dette en devises | 401/411 |
| 679 | Charges pour dépréciations financières | | 590 |
| 68 | Dotations aux amortissements | | 28, 29 |
| **6812** | Dotations aux amortissements des immo incorporelles | Inventaire | 281 |
| **6813** | Dotations aux amortissements des immo corporelles | Inventaire | 283, 284 |
| 69 | Dotations aux provisions et dépréciations | | 19, 29 |
| **6911** | Dotations aux provisions pour risques et charges | | 19 |
| **6913/6914** | Dotations aux dépréciations d'exploitation des immo (incorp/corp) | Test impairment | 291, 294 |
| 6972 | Dotations aux dépréciations financières (titres de participation) | | 296 |

### Classe 7 — Produits (sens normal : Créditeur)

| Compte | Intitulé | Opération typique | Contrepartie |
|---|---|---|---|
| **701** | Ventes de marchandises | Vente en l'état | 411 |
| **702** | Ventes de produits finis | Vente production | 411 |
| 703 | Ventes de produits intermédiaires | | 411 |
| 704 | Ventes de produits résiduels | Déchets vendus | 411 |
| 705 | Travaux facturés (BTP) | | 411 |
| **706** | Services vendus | Prestations | 411 |
| 707 | Produits accessoires (7071 emballages, 7073 locations…) | | 411 |
| 708 | Produits des activités annexes | | 411 |
| 7019…7089 | RRR accordés sur ventes (rare en SYSCOHADA, on contre-passe les 70 directement) | Avoir client | 411 |
| **71** | Subventions d'exploitation (711-718) | Notification subvention courante | 4495, 4582 |
| 73 | Variations de stocks de produits (734-737) | Inventaire fin exercice | 34-37 |
| 75 | Autres produits (751 redevances brevets, 754 indemnités, 758 produits divers de gestion) | | divers |
| **758** | Produits divers de gestion courante (recettes inhabituelles) | | divers |
| 759 | Reprises de charges pour dépréciations d'exploitation | Inventaire (annulation/diminution dépréc.) | 391, 491 |
| 77 | Revenus financiers (771 intérêts prêts, 772 dividendes filiales, 776 gains de change, 779 reprises) | | 521 |
| 781 | Transferts de charges d'exploitation | Régul fin ex. (avantages nature, etc.) | 6617, etc. |
| 791 | Reprises de dépréciations d'exploitation des immo | | 291, 294 |
| **799** | Reprises de subventions d'investissement | Inventaire (étalement subv. sur durée amort.) | 14xx |

### Classe 8 — Autres charges et produits (HAO / HAS) — sens variable

| Compte | Intitulé | Sens | Opération |
|---|---|---|---|
| 81 | Valeurs comptables des cessions courantes (812 immo corp, 814 incorp) | D | Cession immo : VCN sortie |
| 82 | Produits des cessions courantes (822) | C | Prix de cession immo |
| 83 | Charges hors activités ordinaires (831 valeur cession HAO, 835 dons, 839 charges pour dépréc HAO) | D | Sinistres, restructurations |
| 84 | Produits hors activités ordinaires (845 dommages-intérêts reçus, 849 reprises HAO) | C | |
| 85 | Dotations HAO (851 prov. règlem. = amort. dérog., 852 amort. HAO, 853 dépréc. HAO) | D | |
| 86 | Reprises HAO (861 prov. règlem., 863 dépréc. HAO) | C | |
| 87 | Participation des travailleurs au bénéfice | D | |
| **88** | Subventions d'équilibre | C | Subvention couvrant pertes |
| **891** | Impôts sur les bénéfices de l'exercice (IS, BIC) | D | Liquidation IS fin exercice |

## 12.3 Patterns d'écritures-types — Mémo des opérations courantes

### Achats / Ventes (Guide SYSCOHADA Chap.2)
```
Achat marchandises B2B :   D 601 + D 4452       C 401
Vente marchandises B2B :   D 411                C 701 + C 4431
Retour sur achat :         D 401                C 601
Retour sur vente :         D 701                C 411
Acquisition immo :         D 2xx + D 4451       C 481 (ou 404)
Importation droits doua :  D 2xx/60x (intégré)  C 4426
```

### Trésorerie & règlements (Chap.4)
```
Règlement fournisseur :    D 401                C 521 (ou 571)
Encaissement client :      D 521                C 411
Virement Banque→Caisse :   D 581→571            puis D 571 C 581 (solder 581 en clôture)
Émission effet à payer :   D 401                C 402 (effets à payer)
Remise à l'escompte :      D 521 + D 6311 + D 6745   C 565 (remises à l'escompte)
Chèque impayé :            D 411 (renvoi)       C 521
Mobile money (Wave/MoMo) : D 53x                C 411 (ou inverse)
```

### TVA (Chap.3 §2.2) — Centralisation mensuelle
```
Fin de mois :
D 4431 + 4432 + 4433/4 (collectée)
  C 4451 + 4452 + 4453 (déductible)
  C 4441 (TVA à décaisser)  ← si position créditrice
  ou
  D 4449 (crédit TVA à reporter) ← si position débitrice
```

### Charges de personnel (Chap.3 §4 — Application 10)
```
Pièce 1 — Comptabilisation du bulletin (brut → net) :
D 6611 + 6612 (brut)                    C 422 (rémunérations dues)
D 422                                    C 431 + 432 (retenues sociales)
D 422                                    C 4212 + 423 + 447 (acompte, saisie, ITS)
                                         → solde 422 = NET À PAYER

Pièce 2 — Charges patronales :
D 6641 (sociales sur rém. perso. national)   C 431 + 432

Pièce 3 — Avantages en nature (régul fin exercice) :
D 6617                                       C 781 (transferts de charges)

Pièce 4 — Personnel extérieur (régul fin exercice) :
D 667                                        C 637
```

### Impôt sur les bénéfices (Chap.3 §2.3 — Application 8)
```
Acompte trimestriel :     D 441.n              C 521
Liquidation fin ex. :     D 891.n              C 441.n
Solde IS restant :        Solde C de 441 = à payer
```

### Subventions (Chap.17 — Applications 66-69)
```
Notification subv. invest. :  D 4494/4495      C 1411 (subv. Etat) ou 1412 (Région)
Encaissement :                D 521            C 4494
Reprise annuelle (étalement sur durée amort.) :
                              D 14xx           C 799 (reprise quote-part)
Subv. exploitation :          D 4495           C 711-718
Subv. équilibre (perte) :     D 4496           C 881
```

### Régularisations d'inventaire (Chap.6)
```
Variation stocks (intermittent) :
  Annulation SI :   D 6031 (m'ses) / 736 (PF)   C 31 / 36
  Constatation SF : D 31 / 36                   C 6031 / 736
  Ou en une écriture (variation seule)

Charges constatées d'avance (CCA) :  D 476     C 60-63
Charges à payer (CAP/FNP) :          D 60-63   C 408 (fournisseurs FNP)
Produits constatés d'avance (PCA) :  D 70-77   C 477
Produits à recevoir (PNF) :          D 418     C 70

Amortissements :     D 681 (ou 852 HAO)         C 281/283/284
Dépréciations immo : D 6913/6914                C 291/294
Dépréciations stk :  D 6593                     C 391
Dépréciations cli :  D 6594                     C 491
Provisions R&C :     D 6911                     C 191
Amort. dérogatoires: D 851                      C 151
Reprises :           Sens inversé → 791/759/863/861
```

### Capitaux propres (Chap.16 — Applications 58-65)
```
Constitution (libération intégrale) :
  D 4611 + 4612         C 1011 (promesses)
  D 4613                C 4611 + 4612 (appel)
  D 1011                C 1012 (appel capital)
  D 2xx + 411 - 162     C 4613 (réalisation apports nature)
  D 4732 (notaire)      C 4613 (réalisation numéraire)
  D 521 + 6324 + 6322   C 4732 (versement notaire net frais)
  D 1012                C 1013 (reclassement capital versé)

Augmentation en numéraire avec prime :
  D 4732                C 4615
  D 4615                C 1013 + 1051 (prime émission)

Augmentation par incorporation de réserves :
  D 118x                C 1013

Réduction par imputation des pertes :
  D 1013                C 1291

Réduction par remboursement :
  D 1013                C 4619 puis D 4619 C 521

Amortissement de capital :
  D 1013                C 1014 puis D 118x C 4619, D 4619 C 521

Affectation du résultat (AGO) :
  D 1301                C 111 + 112 + 118 + 465 + 121
  Mise en paiement div : D 465  C 521
```

### Cessions d'immobilisations (Chap.5 §4)
```
Sortie VCN :          D 81 (812 corp / 814 incorp)  C 2xx
                      D 28x (amort. cumulé)
Prix de cession :     D 485 (créance) ou 521        C 82
Subv. liée résiduelle: D 14xx                       C 799 (solde)
```

## 12.4 Reconstitution de la contrepartie probable depuis une ligne de balance

Lecture par questionnement systématique :

1. **Quel est le compte ?** → identifier la classe et la nature (cf. §12.2)
2. **Quel est le mouvement de la période ?** (D et C distincts ou nets)
3. **Quelle opération économique génère ce mouvement ?** (cf. §12.3)
4. **Quels comptes sont SYSTÉMATIQUEMENT en contrepartie ?** :

| Si compte mouvementé… | Contreparties candidates (par ordre de fréquence) |
|---|---|
| 6xx (charge) | 401 (achat à crédit) → 521/571 (achat cash) → 408 (FNP) → 4xx (régul) |
| 7xx (produit) | 411 (vente à crédit) → 521/571 (vente cash) → 418 (PNF) |
| 21-24 (immo) | 481/404 (acquisition) → 4451 (TVA) ; sortie : 81 + 28x |
| 28x (amort.) | 681 (exploitation) ou 852 (HAO) |
| 29x (dépréc.) | 691/697 (dot. immo) ou 853 (dot. HAO) |
| 31-37 (stock) | 603 ou 73 selon nature (annulation/constatation) |
| 39 (dép. stk) | 659/759 |
| 401 (frn) | 60x (constatation) — 521/571 (règlement) |
| 411 (cli) | 70x (constatation) — 521/571 (règlement) — 416/491 (sinistre) |
| 422 (perso) | 661/662 (constatation) — 431/432 (retenues) — 521/571 (paiement net) |
| 431 (CNPS) | 422 (salariale) + 664 (patronale) — 521 (paiement) |
| 443 (TVA coll.) | 411 — centralisée vers 4441 |
| 445 (TVA déd.) | 401 / 481 — centralisée vers 4441 |
| 4441 (TVA due) | 521 (paiement) |
| 441 (IS) | 521 (acompte) — 891 (liquidation) |
| 446 (autres taxes) | 6418 (TEE) — 521 (paiement) |
| 4471 (retenue source) | 401 (fournisseur) — 521 (reversement) |
| 4472 (ITS) | 422 — 521 (reversement) |
| 4478 (FDFP) | 6414/6415 — 521 (reversement) |
| 521 (banque) | TOUS les comptes 4xx + 6xx/7xx cash |
| 571 (caisse) | 411/401 (cash) + 422 (paie cash) + 521 (alim.) |
| 16x (emprunt) | 521 (déblocage / remboursement principal) + 671 (intérêts) |
| 14xx (subv. invest.) | 4494/5 (création) — 799 (reprise annuelle) |
| 1301 (résultat) | Solde de toutes les classes 6 et 7 — affectation vers 111/465/121/118 |
| 891 (IS) | 441.n |

## 12.5 Détection d'anomalies depuis la balance (méthode MDLC)

À vérifier systématiquement avant tout commentaire :

| # | Test | Anomalie si… | Code |
|---|---|---|---|
| T1 | Total Débit = Total Crédit | Écart > 0,01 | DESEQ-BLOQUANT |
| T2 | Sens des soldes conforme | Caisse 571 créditrice / Banque 521 créditrice non documentée | T-1 |
| T3 | Capital 101 cohérent avec statuts | Variation sans PV AGE | CAP-SANS-AGO |
| T4 | Réserve légale 111 ≥ 10% bénéfice antérieur (PM) | 111 = 0 alors que bénéfices ≥ 5 ans | RESERVE-LEGALE-N |
| T5 | 1301/1309 soldé au bout de 6 mois | Solde persistant > 6 mois après clôture | AFFECT-NON-FAITE |
| T6 | 47x (suspens) soldé à clôture | Solde 471/472/478 ≠ 0 au 31/12 | SUSPENS-NON-LETTRE |
| T7 | 581 (virements internes) soldé | ≠ 0 au 31/12 | VIRINT-NON-SOLDE |
| T8 | Triangle CMV : 601 + SI − SF = CMV cohérent | Marge brute aberrante | CMV-INCO |
| T9 | Triangle Caisse : SI + entrées − sorties = SF | Écart = prélèvements gérant non comptabilisés | CAISSE-PRELEVEMENT |
| T10 | Triangle Banque : SI + encaissements − décaissements = SF | Écart ≠ rapprochement bancaire | BQ-NON-RAPPROCHE |
| T11 | 681 (dotations) cohérent avec ΔN-N-1 sur 28x | ΔAmort ≠ Dotation enregistrée | AMORT-INCO |
| T12 | 6611 (salaires) compatible avec effectif déclaré CNPS | Salaires sans CNPS = dissimulation | CNPS-ABSENT |
| T13 | 6313/6414/6415 enregistrés si paie | Paie sans charges patronales = anomalie | CHARGES-PATRON-ABSENT |
| T14 | 471-478 (comptes d'attente) | Solde > 0 → demander pièces | SUSPENS |
| T15 | 109 / 4611 soldés après libération capital | Solde persistant = capital non libéré | CAP-NON-LIBERE |
| T16 | 416 (clients douteux) déprécié (491) | 416 > 0 sans 491 = sous-évaluation | DEPRECIATION-MANQUE |

## 12.6 Modèle de restitution — Une ligne de balance commentée

Format standard MDC à utiliser systématiquement :

```
COMPTE 601 — Achats de marchandises
─────────────────────────────────────
• Sens balance       : Débit 12.500.000 FCFA
• Nature             : Charge d'exploitation (classe 6) — achat de biens destinés à être revendus en l'état
• Opération économique : Acquisition de marchandises auprès de fournisseurs ; charges du « circuit » entité
• Contrepartie probable : Crédit 401 « Fournisseurs d'exploitation » (achat à crédit) ou 521/571 (cash)
• TVA associée       : 4452 (TVA récupérable sur achats) si entité assujettie
• Régularisations    : Vérifier variation stock 6031 (SF − SI) cohérente avec inventaire physique
• Triangle CMV       : SI + 601 − SF doit ≈ CMV ; rapporter au CA 701 pour taux de marge brute
• Alertes            : (i) 601 anormalement bas vs 701 = marges aberrantes / minoration achats
                       (ii) 601 sans 4452 = TVA non récupérée
                       (iii) Forte hausse N/N-1 sans Δ CA = surstockage ou détournement
• Recommandation     : Lettrer les 401 fournisseurs / réconcilier le grand livre 601 avec factures
```

À appliquer ligne par ligne pour chaque compte significatif (matérialité > 1% du total bilan ou > 2% du CA).

## 12.7 Workflow d'analyse d'une balance client

### FORMAT STANDARD MDC — BALANCE À 6 COLONNES (obligatoire)

Toute balance traitée par le agence MDC doit être normalisée au format **6 colonnes** suivant :

| Col 1 | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 |
|---|---|---|---|---|---|
| **N° de compte** | **Intitulé du compte** | **Mouvement Débit** (période) | **Mouvement Crédit** (période) | **Solde Débit** (cumulé) | **Solde Crédit** (cumulé) |

Si le client fournit une balance à 8 colonnes (avec mouvements N-1 séparés), **les agréger en 6 colonnes** : les mouvements N-1 sont implicitement intégrés dans les Soldes (col 5-6) ; seuls les mouvements de la période N restent en col 3-4.

Si le client fournit une balance à 4 colonnes (sans mouvements), **demander la balance avec mouvements** : sans Mvt D et Mvt C, impossible de mener les triangles MDLC et la détection d'anomalies.

**Tests immédiats sur balance 6 colonnes** :
1. **Σ Mvt D (col 3) = Σ Mvt C (col 4)** — équilibre des mouvements de la période (test T1 bloquant)
2. **Σ Solde D (col 5) − Σ Solde C (col 6) = Résultat de l'exercice** (à affecter)
3. **Pour chaque compte** : Sens normal du Solde cohérent avec la nature (Actif/Charge → col 5 ; Passif/Produit → col 6)

### TEST DE BOUCLAGE D'IMPORT — règle ABSOLUE (bloquant)

Quand la balance arrive en **PDF** (ou image / format non structuré), la ré-saisie manuelle dans Python ou Excel est une **source d'erreurs récurrente** (lignes tronquées, comptes oubliés, chiffres mal lus dans les colonnes compactes Sage). Pour éviter de produire une liasse à partir d'une balance mal importée :

**Procédure obligatoire avant toute production de liasse** :
1. **Préférer toujours un format structuré** (Excel `.xlsx`, CSV, fichier d'export comptable) à un PDF
2. Si seul un PDF est disponible :
   a. Extraire toutes les lignes par OCR/parsing
   b. **Comparer les totaux imprimés Sage en pied de balance** (ex : `Totaux balance D 698 294 678 / C 698 294 678`) aux totaux recalculés sur l'import
   c. **Comparer le nombre de comptes recensés** au nombre attendu (compter les lignes Sage)
   d. Vérifier l'**équilibre Mvt D = Mvt C** sur les totaux importés
3. **Si écart > 1 FCFA OU comptes manquants → STOP** :
   - Ne pas produire la liasse
   - Ne pas lancer l'audit contradictoire
   - **Demander au client la balance au format Excel/CSV exporté directement depuis Sage**
4. Documenter le test de bouclage dans un onglet `0-Bouclage` du fichier Excel produit, avec totaux import vs totaux source.

**Format préféré pour l'import** : Export Sage `Fichier → Exporter → Excel (.xlsx)` ou tableau Excel/CSV envoyé directement par le client. Ne JAMAIS partir d'un PDF si une version structurée est disponible.

### RÈGLE ABSOLUE D'EXHAUSTIVITÉ — Aucune omission, aucune modification

Quand une balance est fournie, l'expert-comptable MDC s'engage à :

1. **REPRENDRE TOUS LES COMPTES** sans exception, même s'ils paraissent peu significatifs (un compte à 1 FCFA doit y être)
2. **CONSERVER LES N° DE COMPTE EXACTS** tels que dans la source (ex : `43131000` et NON `43131` raccourci)
3. **CONSERVER LES LIBELLÉS EXACTS** tels qu'imprimés par le logiciel (ex : `CNPS A PAYER` en majuscules, sans normalisation orthographique)
4. **CONSERVER TOUS LES MOUVEMENTS** : Mvt D période + Mvt C période + Solde D final + Solde C final — aucune agrégation, aucun arrondi
5. **NE PAS DÉCIDER D'OMETTRE** un compte sous prétexte qu'il « semble erroné » ou « peu utile » — c'est au client de décider après audit
6. **NE PAS REGROUPER** des sous-comptes (ex : ne pas additionner 24110001 + 24110003 dans une seule ligne 2411)
7. **CONSERVER L'ORDRE D'ORIGINE** de la balance source
8. **DOCUMENTER LE NOMBRE DE LIGNES IMPORTÉES** et le comparer au nombre attendu

**Sanction interne** : toute production de liasse à partir d'une balance amputée, modifiée ou normalisée sans accord explicite du client = **refus de visa Auditeur MDC** + reprise complète du dossier.

**Bouclage formel à imprimer dans l'onglet `0-Bouclage`** :
```
Source : Sage 100 i7 — fichier <nom> — exporté le <date>
Lignes attendues : N (compte des lignes dans la source)
Lignes importées : M
Σ Mvt D import : X    vs    Σ Mvt D source : X    Écart : 0
Σ Mvt C import : Y    vs    Σ Mvt C source : Y    Écart : 0
Σ Solde D import : Z  vs    Σ Solde D source : Z  Écart : 0
Σ Solde C import : W  vs    Σ Solde C source : W  Écart : 0
Résultat exercice (Σ SD − Σ SC) : R FCFA
✅ Bouclage OK — Import certifié intègre
```
Si une seule de ces vérifications échoue → STOP, ne pas générer la liasse.

Quand l'utilisateur fournit une balance (PDF, Excel, image) :

1. **Charger la balance** (Read PDF + parse en table au format 6 colonnes ci-dessus)
2. **Vérifier l'équilibre** Σ Mvt D = Σ Mvt C (test T1 bloquant) ; Σ Solde D − Σ Solde C = Résultat
3. **Calculer les indicateurs clés** : Total bilan, CA (∑70), Charges (∑60-67), Résultat (7−6), EBE, Marge brute
4. **Lancer les 16 tests d'anomalies** (§12.5)
5. **Produire le tableau commenté** : une ligne par compte significatif au format §12.6
6. **Sortir 3 livrables** :
   - **Note de synthèse** (1 page : équilibre, indicateurs, top 5 alertes)
   - **Tableau détaillé Excel** (1 ligne = 1 compte avec colonnes Nature/Opération/Contrepartie/Alerte/Recommandation)
   - **Plan de régularisations** (codes REG-ANO-xx ; cf. §1 procédure MDC Mission Type 2)

## 12.8 Nouveautés clés du SYSCOHADA révisé à intégrer (entrée en vigueur 2018)

Référence : Loé-Mié & Tari, *Les nouveautés du plan comptable révisé de l'OHADA*, L'Harmattan 2018.

- **Approche par composants** (Chap.4 Guide) : décomposer un actif en éléments amortis séparément (ex : bâtiment = gros œuvre 50 ans + toiture 25 ans + installations 15 ans)
- **Coût de démantèlement** (Chap.6) : capitalisé à l'origine en contrepartie d'une provision 19
- **Contrats de location** : distinction location simple / **location-acquisition** (≈ IFRS 16) → activation en 23x + dette 17x
- **Réserve de propriété** (Chap.9) : comptabilisation chez acheteur (immo dès l'origine) et vendeur (créance privilégiée)
- **Immeubles de placement** (Chap.10) → compte 22 dédié
- **Dépréciation par UGT** (groupe d'actifs) : tests d'impairment annuels obligatoires
- **Engagements de retraite** (Chap.21) : provision IAS 19 like en 19
- **Opérations en devises** (Chap.22) : 476/477 écarts de conversion + 676/776 gains/pertes change réalisés
- **Tableau de flux de trésorerie** obligatoire pour SN (Système Normal) — d'où la recommandation systématique d'utiliser 481/404 pour les immo (Guide §1.1 Remarque)
- **Distinction provisions / dépréciations** stricte (art. 46 vs 48 AU) : provision = passif externe (19), dépréciation = perte de valeur d'actif (29/39/49/59)
- **Instruments de monnaie électronique** : nouveau compte 53 — utile pour la CI (Wave, Orange Money, MTN MoMo, Moov Money)

## 12.9 Règle d'or de l'analyste comptable MDC

> « Toute ligne d'une balance raconte au moins une opération économique.
> S'il y a un débit ou un crédit, il y a eu un événement, donc une pièce, donc une contrepartie.
> L'analyste ne se contente pas de **constater** un solde : il **reconstitue le récit** et **vérifie sa cohérence** avec les autres lignes de la balance, le bilan, le CR et la réalité du métier du client. »

Quand un solde est inexplicable depuis la balance seule, demander : (1) le grand livre du compte, (2) les pièces justificatives, (3) une explication écrite du dirigeant.

---

# 13. WORKFLOW « BALANCE → ÉTATS FINANCIERS COMPLETS SYSCOHADA SN »

Compétence ultime du comptable MDC capitalisée à partir de l'exemple complet pédagogique du **Guide d'application SYSCOHADA pp. 343-394** (entité fictive "SYSTÈME COMPTABLE OHADA SARL", fabricant de meubles, exercice clos 31/12/N).

À partir d'une **balance comptable N (avec rappel N-1)**, l'expert produit la **liasse complète Système Normal (SN)** : Page de garde + 4 fiches d'identification + Bilan + Compte de Résultat + Tableau de Flux de Trésorerie + Notes annexes 1 à 36 + Fiche de synthèse des indicateurs financiers.

## 13.1 Composition de la liasse SN (séquence pédagogique du Guide)

| # | Document | Source des données | Page Guide réf. |
|---|---|---|---|
| 1 | **PAGE DE GARDE** | Identité entité, documents déposés | p.351 |
| 2 | **FICHE R1** — Identification fiscale | Statuts, RCCM, NCC, expert-comptable, banques | p.352 |
| 3 | **FICHE R2** — Contrôle entité + activités | Statuts, CA par branche | p.353 |
| 4 | **FICHE R3** — Dirigeants + CA | PV nominations | p.354 |
| 5 | **FICHE R4** — Liste des notes applicables (A/NA) | Tri logique sur 36 notes | p.355 |
| 6 | **BILAN ACTIF/PASSIF** (lignes AD à BZ / CA à DZ) | Balance soldes au 31/12/N + N-1 | p.356 |
| 7 | **COMPTE DE RÉSULTAT** (TA à RS, SIG XA à XI) | Balance mouvements N + comparatif N-1 | p.357 |
| 8 | **TABLEAU DE FLUX DE TRÉSORERIE (TFT)** | CAFG + variations BFR + flux invest. + flux financement | pp.358-360 |
| 9 | **NOTES ANNEXES 1 à 36** | Détail de chaque rubrique du bilan/CR | pp.361-389 |
| 10 | **NOTE 31** — 5 derniers exercices | Historique CA/Résultat/Dividende | p.390 |
| 11 | **NOTES 32-33** — Production & Achats destinés production | Statistiques d'exploitation | pp.391-392 |
| 12 | **FICHE DE SYNTHÈSE INDICATEURS** | SIG + CAF + Rentabilité + Structure financière + Flux | pp.393-394 |

## 13.2 Mapping BALANCE → BILAN (codes ref SYSCOHADA SN)

### Actif (lignes AD à BZ)

| REF | Libellé Bilan | Comptes balance à agréger | Présenté en |
|---|---|---|---|
| AD | Immobilisations incorporelles | 21x sauf 219 | Brut, Amort 28x (incorp), Net |
| AF | Brevets, licences, logiciels et droits similaires | 211 à 214 | Brut/Amort/Net |
| AG | Fonds commercial et droit au bail | 215, 216 | Brut/Amort/Net |
| AI | Immobilisations corporelles | 22x à 24x | Brut, Amort 28x (corp), Net |
| AJ | Terrains (dont placement séparé) | 22 (221-228) | Non amortissable |
| AK | Bâtiments (dont placement) | 231-237 | Brut/Amort 283/Net |
| AL | Aménagements, agencements, installations | 235, 238 | Brut/Amort 2835, 2838/Net |
| AM | Matériel, mobilier et actifs biologiques | 241, 244, 246, 247 | Brut/Amort 2841, 2844/Net |
| AN | Matériel de transport | 245 | Brut/Amort 2845/Net |
| AP | Avances et acomptes versés sur immobilisations | 252 | |
| AQ | Immobilisations financières | 26, 27 | Brut/Dépréc. 296,297/Net |
| AS | Autres immobilisations financières | 272, 275, 276 | |
| **AZ** | **TOTAL ACTIF IMMOBILISÉ** | Σ AD+AI+AP+AQ | |
| BA | Actif circulant HAO | 4851 + 488 | |
| BB | Stocks et en-cours | 31, 32, 33, 34, 35, 36, 37, 38 − 39 | |
| BG | Créances et emplois assimilés | 409 + 41x + 4xx tiers actif | |
| BH | Fournisseurs avances versées | 409 | |
| BI | Clients | 411 + 416 − 491 | |
| BJ | Autres créances | 421+422D+44x.D+462D+465D+47xD+476 | |
| **BK** | **TOTAL ACTIF CIRCULANT** | Σ BA+BB+BG | |
| BS | Banques, chèques postaux, caisse | 50, 521 à 538, 571, 581 | − 59 (dépréc.) |
| BT | TOTAL TRÉSORERIE ACTIF | Σ | |
| BU | Écart de conversion-Actif | 478 (D) | |
| **BZ** | **TOTAL GÉNÉRAL ACTIF** | Σ AZ+BK+BT+BU | |

### Passif (lignes CA à DZ)

| REF | Libellé Bilan | Comptes balance à agréger |
|---|---|---|
| CA | Capital | 1011+1012+1013+1014 (capital appelé) ou nominal total |
| CB | Apporteurs capital non appelé (−) | 109 en négatif |
| CD | Écarts de réévaluation | 106 |
| CE | Réserves indisponibles | 111, 112 |
| CF | Report à nouveau (+/−) | 121 (C) ou 129 (D) |
| CG | Résultat net de l'exercice | Résultat du CR (XI) — substitue 1301/1309 |
| CH | Subventions d'investissement | 14 |
| CJ | Provisions réglementées | 15 (dont 151 amort. dérog., 154 prov. réval.) |
| **CP** | **TOTAL CAPITAUX PROPRES ET RESSOURCES ASSIMILÉES** | Σ CA…CJ |
| DA | Emprunts et dettes financières diverses | 16 (162, 163, 164, 165, 166, 168) − part < 1 an séparée si SMT |
| DC | Provisions pour risques et charges | 19 |
| **DD** | **TOTAL DETTES FINANCIÈRES** | Σ DA+DC |
| **DF** | **TOTAL RESSOURCES STABLES** | CP + DD |
| DH | Dettes circulantes HAO | 481, 482, 484 |
| DI | Clients, avances reçues | 419 |
| DJ | Fournisseurs d'exploitation | 401 (C) + 408 |
| DK | Dettes fiscales et sociales | 42 (C) + 43 + 44 (C, hors 441 IS si reclassé) |
| DM | Autres dettes | 462 (C) + 465 + 47x (C) + 477 |
| DN | Provisions pour risques à court terme | 499 si applicable |
| **DP** | **TOTAL PASSIF CIRCULANT** | Σ DH…DN |
| DR | Banques, établissements financiers et crédits de trésorerie | 561, 564, 565 |
| **DT** | **TOTAL TRÉSORERIE PASSIF** | DR |
| DV | Écart de conversion-Passif | 479 (C) |
| **DZ** | **TOTAL GÉNÉRAL PASSIF** | Σ DF+DP+DT+DV — DOIT = BZ |

### Test bloquant : **BZ = DZ** (Actif Total = Passif Total) à 1 FCFA près

## 13.3 Mapping BALANCE → COMPTE DE RÉSULTAT (codes ref SYSCOHADA SN)

| REF | Libellé CR | Comptes balance (mouvements ou soldes nets) | Signe |
|---|---|---|---|
| TA | Ventes de marchandises | 701 net (− retours 7019) | + |
| RA | Achats de marchandises | 601 net (− RRR 6019) | − |
| RB | Variation de stocks de marchandises | 6031 (signé : SF−SI) | −/+ |
| **XA** | **MARGE COMMERCIALE** | TA + RA + RB | = |
| TB | Ventes de produits fabriqués | 702 (− 7029 remises) − 7026 retours | + |
| TC | Travaux, services vendus | 705 + 706 | + |
| TD | Produits accessoires | 707 + 708 | + |
| **XB** | **CHIFFRE D'AFFAIRES** | TA + TB + TC + TD | = |
| TF | Production immobilisée | 72 | + |
| TG | Subventions d'exploitation | 71 | + |
| TH | Autres produits | 75, 781 partiel | + |
| TI | Transferts de charges d'exploitation | 781 | + |
| RC | Achats de matières premières et fournitures liées | 602 | − |
| RD | Variation stocks matières premières | 6032 (SF−SI) | −/+ |
| RE | Autres achats | 604, 605, 608 | − |
| RF | Variation stocks autres approvisionnements | 6033 | −/+ |
| RG | Transports | 61 | − |
| RH | Services extérieurs | 62 + 63 (hors 631 services bancaires) | − |
| RI | Impôts et taxes | 64 (sauf 647) | − |
| RJ | Autres charges | 65 (sauf 659) | − |
| **XC** | **VALEUR AJOUTÉE** | XB + RA + RB + (TF à RJ) | = |
| RK | Charges de personnel | 66 (sauf 667 transferts) | − |
| **XD** | **EXCÉDENT BRUT D'EXPLOITATION (EBE)** | XC + RK | = |
| TJ | Reprises de provisions, amortissements | 791, 798, 759 | + |
| RL | Dotations aux amortissements, provisions, dépréciations | 681, 691, 659 (D&P expl.) | − |
| **XE** | **RÉSULTAT D'EXPLOITATION** | XD + TJ + RL | = |
| TK | Revenus financiers et assimilés | 77 | + |
| RM | Frais financiers et charges assimilés | 67 (sauf 679) | − |
| RN | Reprises/Dotations financières | 797 / 697 + 679 | +/− |
| **XF** | **RÉSULTAT FINANCIER** | TK + RM + RN | = |
| **XG** | **RÉSULTAT DES ACTIVITÉS ORDINAIRES (RAO)** | XE + XF | = |
| TN | Produits des cessions d'immobilisations | 82 | + |
| TO | Autres produits HAO | 84, 88 | + |
| RO | Valeurs comptables des cessions d'immo | 81 | − |
| RP | Autres charges HAO | 83, 85 | − |
| **XH** | **RÉSULTAT HORS ACTIVITÉS ORDINAIRES (RHAO)** | TN + TO + RO + RP | = |
| RQ | Participation des travailleurs | 87 | − |
| RS | Impôts sur le résultat | 891 | − |
| **XI** | **RÉSULTAT NET** (= CG du Bilan) | XG + XH + RQ + RS | = |

### Test bloquant : **XI (CR) = CG (Bilan) = 1301 net (ou 1309)**

## 13.4 Tableau de Flux de Trésorerie (TFT) — méthode SYSCOHADA

Architecture en 4 sections + variation nette :

```
ZA  Trésorerie nette à l'ouverture (BT N-1 − DT N-1)

FA  CAFG (Capacité d'AutoFinancement Globale)
    = EBE + revenus financiers + produits HAO encaissables
      − frais financiers − impôts − dotations non décaissables
FB  − Variation BFR exploitation (stocks + créances − dettes circulantes)
FC  Variation BFR HAO
ZB  FLUX OPÉRATIONNELS = FA + FB + FC

FD  − Décaissements d'investissements (Δ immo brutes)
FE  + Encaissements de cessions (TN + Δ 4851)
FF  + Subventions reçues (Δ 14)
ZC  FLUX D'INVESTISSEMENT

FG  + Augmentations de capital (Δ 101)
FH  + Nouveaux emprunts (mouvement 16 nouveau)
FI  − Remboursements d'emprunts (mouvement 16 sortie)
FJ  − Dividendes versés (mouvement 465 paiement)
ZD  FLUX DE FINANCEMENT

ZE  VARIATION TRÉSORERIE NETTE = ZB + ZC + ZD
ZF  Trésorerie à la clôture (BT N − DT N)

CONTRÔLE : ZE = ZF − ZA
```

Exemple chiffré SYSTÈME COMPTABLE OHADA (p.393) :
- Flux opérationnels : **+170 235** k FCFA
- Flux investissement : **−328 722** (acquisitions massives bâtiments)
- Flux financement : **+207 000** (emprunt 100M + capital 200M − dividendes)
- Variation : **+48 513** ⇒ Trésorerie passe de 74 584 à 123 097

## 13.5 Tableau de génération des 36 Notes annexes

| Note | Intitulé | Source balance | Forme attendue |
|---|---|---|---|
| 1 | Information générale | Statuts | Texte |
| 2 | Règles et méthodes comptables | Manuel procédures | Texte |
| **3A** | **Immobilisation brute** | 2xx mouvements N (SI + acquisitions + virements + réévaluation − cessions = SF) | Tableau A B C D=A+B−C |
| 3B | Biens pris en location-acquisition | 17 + 23x activé | Tableau |
| **3C** | **Immobilisations : amortissements** | 28x mouvements N (SI + dotations − amort. sortis = SF) | Tableau A B C D |
| **3D** | **Plus-values et moins-values de cession** | 81 (VCN) vs 82 (prix) | Tableau Brut, Amort, VCN, Prix, ±Value |
| 3E | Réévaluations effectuées | 106 + 154 + commentaires | Texte + tableau |
| 3F | Étalement charges immobilisées | 201, 202 | Tableau |
| **4** | **Immobilisations financières** | 26, 27 | Tableau N/N-1 + ventilation maturité |
| **5** | **Actif circulant et dettes circulantes HAO** | 4851, 488 / 481, 482, 484 | Tableau N/N-1 |
| **6** | **Stocks et en-cours** | 31-37 + 39 (dépréc.) | Tableau N/N-1 + variation |
| **7** | **Clients** | 411 + 416 − 491 | Tableau + ventilation maturité |
| **8** | **Autres créances** | 42 (D) + 462 (D) + 47 (D) + 476 | Tableau N/N-1 + maturité |
| 9 | Titres de placement | 50 − 590 | Tableau |
| 10 | Valeurs à encaisser | 51 | Tableau |
| **11** | **Disponibilités** | 521-538, 571 | Tableau N/N-1 |
| **12** | **Écarts de conversion et transferts de charges** | 478, 479 / 781 | Tableau ventilé devises + commentaire |
| **13** | **Capital — valeur nominale actions** | 101 + tableau associés | Tableau nominatif |
| **14** | **Primes et réserves** | 105, 111, 112, 118, 121, 129 | Tableau |
| **15A** | **Subventions et provisions réglementées** | 14, 15 | Tableau + commentaires |
| 15B | Autres fonds propres | 16 (compte courant > 5 ans) | Tableau |
| **16A** | **Dettes financières et ressources assimilées** | 16 + 19 | Tableau + ventilation maturité |
| 16B | Engagements de retraite (méthode actuarielle) | 196 + hors bilan | Texte + tableau actuariel |
| 16C | Dettes garanties par sûretés réelles | Annexe juridique | Tableau |
| **17** | **Fournisseurs d'exploitation** | 401 (C) + 408 + 409 (D) | Tableau N/N-1 |
| **18** | **Dettes fiscales et sociales** | 42 (C) + 43 + 44 (C) | Tableau N/N-1 |
| **19** | **Autres dettes et provisions risques CT** | 462 (C) + 465 + 47x (C) + 499 | Tableau |
| 20 | Banques crédit escompte trésorerie | 561, 564, 565 | Tableau |
| **21** | **Chiffre d'affaires et autres produits** | 70 ventilé + 75 + 77 | Tableau ventilé région/hors région |
| **22** | **Achats** | 601, 602, 604, 605, 608 | Tableau ventilé |
| **23** | **Transports** | 61 | Tableau ventilé par destination |
| **24** | **Services extérieurs** | 62 + 631-638 | Tableau ventilé par nature |
| **25** | **Impôts et taxes** | 64 | Tableau |
| **26** | **Autres charges** | 65 (sauf 659) | Tableau |
| **27A** | **Charges de personnel** | 66 ventilé | Tableau N/N-1 |
| **27B** | **Effectifs, masse salariale, personnel extérieur** | Données paie | Tableau qualification × sexe × nationalité |
| **28** | **Provisions et dépréciations inscrites au bilan** | 19, 29, 39, 49, 59 — mouvements | Tableau A B C D mouvements |
| **29** | **Charges et revenus financiers** | 67 / 77 | Tableau |
| **30** | **Autres produits et charges HAO** | 83, 84, 85, 88 | Tableau |
| **31** | **Répartition résultat 5 derniers exercices** | Historique CA + Résultat + Dividende | Tableau N à N−4 |
| **32** | **Production de l'exercice** | Données quantité × valeur (par produit) | Tableau matière/unité |
| **33** | **Achats destinés à la production** | 602 ventilé matière | Tableau matière/unité |
| 34 | Actifs et passifs éventuels | Annexe juridique | Texte |
| 35 | Liste informations sociales/environnementales/sociétales | RSE | Texte |
| 36 | Table des codes | Référentiel | Texte |

## 13.6 Fiche de synthèse — Indicateurs financiers (p.393)

À calculer SYSTÉMATIQUEMENT après production du Bilan + CR :

```
SOLDES INTERMÉDIAIRES DE GESTION (SIG) :
- Chiffre d'affaires (XB)
- Marge commerciale (XA)
- Valeur ajoutée (XC)
- Excédent brut d'exploitation (XD)
- Résultat d'exploitation (XE)
- Résultat financier (XF)
- Résultat des activités ordinaires (XG)
- Résultat hors activités ordinaires (XH)
- Résultat net (XI)

CAPACITÉ D'AUTOFINANCEMENT (CAFG) :
EBE + revenus financiers + produits HAO − frais financiers − impôts
Autofinancement = CAFG − dividendes distribués

RENTABILITÉ :
- Rentabilité économique = Résultat d'exploitation (a) / (Capitaux propres + Dettes financières)
- Rentabilité financière = Résultat net / Capitaux propres

STRUCTURE FINANCIÈRE :
- Ressources stables = CP + Dettes financières
- Fonds de roulement (FR) = Ressources stables − Actif immobilisé
- BFR Exploitation = Actif circulant exploitation − Passif circulant exploitation
- BFR HAO = Actif circulant HAO − Passif circulant HAO
- BFR Global = BFR Expl + BFR HAO
- Trésorerie Nette = FR − BFR (contrôle : TN = Trésorerie Actif − Trésorerie Passif)

VARIATION TRÉSORERIE :
- Flux opérationnels + Flux investissement + Flux financement = Δ TN

ENDETTEMENT FINANCIER NET :
- Endettement brut (16 + 561) − Trésorerie active = Endettement net
- Si négatif → entité sur-liquide
```

## 13.7 Procédure type MDC pour produire une liasse SN complète

À chaque mission, suivre cet ordre invariable :

1. **Importer la balance N (et N-1)** au format `N° compte | Intitulé | SI D | SI C | Mvt D | Mvt C | Solde D | Solde C`
2. **Vérifier équilibre balance** (test bloquant T1)
3. **Calculer 16 tests d'anomalies** (§12.5) AVANT production des états
4. **Préparer le mapping balance → Bilan** (§13.2) — pivoter par classe de compte
5. **Préparer le mapping balance → CR** (§13.3) — par nature de charge/produit
6. **Identifier les notes applicables** (Fiche R4) — cocher A/NA selon présence des comptes
7. **Générer le squelette Excel** : un onglet par livrable (Page de garde, R1, R2, R3, R4, Bilan, CR, TFT, Note 3A…Note 33, Synthèse)
8. **Remplir les notes une par une** dans l'ordre du Guide (3A → 3F → 4 → 5 → … → 33)
9. **Calculer le TFT** (§13.4) à partir des mouvements N et de la variation Bilan
10. **Produire la fiche synthèse** (§13.6) avec tous les indicateurs N et N-1
11. **Tests bloquants finaux** :
    - BZ Actif = DZ Passif (à 1 FCFA)
    - XI Résultat CR = CG Résultat Bilan
    - ZE TFT = ZF − ZA (variation trésorerie cohérente)
    - Σ Notes = totaux Bilan/CR
12. **Pagination, en-têtes "Désignation entité / NIF / Exercice / Durée"** sur chaque feuille
13. **Visa Auditeur MDC** (cf. §4) avant remise client

## 13.8 Format normalisé des en-têtes de chaque page de la liasse

Toutes les pages des États Financiers Normalisés portent en haut :

```
Désignation entité : <RAISON SOCIALE>           Exercice clos le <JJ-MM-AAAA>
Numéro d'identification : <NCC/NIF>             Durée (en mois) <12>
```

Avec sous-titre du document : `NOTE <X> : <INTITULÉ EN MAJUSCULES>` ou `BILAN AU 31 DÉCEMBRE N` ou `COMPTE DE RÉSULTAT` ou `FICHE R<x>`.

Chaque tableau de note se termine par un encart **`Commentaire :`** en italique justifiant les variations significatives (≥ 10% N/N-1) ou les opérations atypiques.

## 13.9 Méthodologie de génération automatisée Excel (Python openpyxl)

Pour industrialiser la production :

1. Charger la balance dans un DataFrame pandas (`compte`, `intitule`, `solde_n_d`, `solde_n_c`, `mvt_n_d`, `mvt_n_c`, `solde_nm1_d`, `solde_nm1_c`)
2. Créer un dict de mapping `bilan_mapping = {"AD": ["211","212","213","214"], "AF": [...], ...}`
3. Pour chaque ligne du bilan : `valeur = df[df.compte.str.startswith(prefix)].solde_n_net.sum()`
4. Idem pour le CR (sommation des mouvements N pour les comptes 6/7)
5. Notes : un onglet par note, avec formules `=Balance!XX` pour cascade automatique
6. Format MDC navy/or (cf. §8) + format FCFA `#,##0;[RED]-#,##0;"—"`
7. Volets figés sous les en-têtes, gridlines off, tabColor par section
8. `wb.calculation.fullCalcOnLoad = True` pour recalc à l'ouverture

## 13.10 Cas pédagogique — SYSTÈME COMPTABLE OHADA SARL (Guide pp.343-394)

**Profil entité** : SARL fabrication de meubles en bois, Code activité C 3100, capital 400 M FCFA (libération partielle), 31 salariés, exercice 12 mois.

**Chiffres clés exercice N produits par la liasse complète** :
- CA : 2 041 947 k FCFA (+9% vs N-1)
- Marge commerciale : 40 000 k (nouvelle activité commerciale)
- Valeur ajoutée : 485 093 k (+27%)
- EBE : 266 876 k (+54%)
- Résultat net : 215 390 k (+82%)
- Total bilan : 1 054 424 k FCFA
- Capitaux propres : 656 960 k
- Fonds de roulement : 95 953 k
- Trésorerie nette : 123 097 k
- CAFG : 242 150 k

**Opérations significatives de N** :
- Augmentation de capital 300 M (200 M libérés, 100 M restant)
- Réévaluation libre tous biens corporels (écart 3 500 k + provision réglementée 40 000 k)
- Acquisition bâtiment industriel 430 M + matériels 21 M
- Emprunt London City 100 M (£) sur 7 ans
- Cession motopompe + mise au rebut matériels totalement amortis
- Provision pension retraite 62 116 k
- IS 31 102 k, dividendes 90 000 k

**Cette liasse complète est la référence pédagogique** : à reproduire mécaniquement pour tout client MDC moyennant adaptation des comptes.

---

# 14. MÉTHODOLOGIE STANDARD MDC — « Audit contradictoire systémique d'une balance »

**Compétence-pivot du agence MDC**, déclenchée AUTOMATIQUEMENT à chaque fois que l'utilisateur fournit une balance comptable client (PDF, Excel, image, photo). Capitalisée à partir du cas réel **BUILDING NEW AFRICA SARL** (BTP, exercice 2025) traité en mai 2026.

## 14.1 Principe fondateur

> Un comptable seul produit des erreurs. **Deux comptables qui se contredisent produisent une vérité.**

Toute analyse de balance MDC doit suivre une **procédure contradictoire en double regard** : un comptable « junior » fait une première analyse → un « auditeur indépendant » la challenge avec esprit critique → une **position définitive consolidée** émerge → les régularisations sont rédigées → la liasse SN est produite → le rapport d'audit final est édité.

## 14.2 Workflow en 8 étapes — déclenchement systématique

À chaque fois qu'une balance arrive :

### Étape 1 — Lecture et structuration de la balance
- Identifier l'entité (raison sociale, secteur, logiciel, exercice, devise)
- **FORMAT OBLIGATOIRE — BALANCE 6 COLONNES** : `N° compte | Intitulé | Mouvement Débit | Mouvement Crédit | Solde Débit | Solde Crédit`
  - Si client envoie une balance 8 colonnes (avec N-1 séparé) → agréger en 6 colonnes (mouvements N-1 implicites dans soldes)
  - Si client envoie une balance 4 colonnes (soldes seuls) → **EXIGER** la balance avec mouvements (sans Mvt D/C, pas de triangles MDLC possibles)
- **Test T1 bloquant** : Σ Mouvement Débit (col 3) = Σ Mouvement Crédit (col 4)
- Calculer le **résultat provisoire** = Σ Solde Débit (col 5) − Σ Solde Crédit (col 6) [écart bilan = résultat à affecter]
- Vérifier le **sens normal** de chaque solde (Actif/Charge col 5 ; Passif/Produit col 6)

### Étape 2 — Première analyse "comptable junior" (compétence §12)
- Appliquer la grille de lecture systémique §12.2 (toutes classes 1 à 8)
- Identifier les anomalies par les 16 tests §12.5
- Produire le **rapport d'anomalies initial** avec gravité, base légale, impact

### Étape 3 — Audit contradictoire indépendant
**Déployer un agent `general-purpose` distinct** avec mission de **CONTRADICTION CRITIQUE**. Le prompt de l'agent contient :
1. La balance complète (tous comptes significatifs avec mouvements)
2. Le rapport du « comptable junior » (anomalies A1-Ax)
3. Le **référentiel juridique de vérification** : SYSCOHADA, AUDCIF, AUSCGIE, AUPCAP, CGI CI, Code prévoyance CI
4. La **mission en 4 parties** : (1) Contradiction point par point ✅⚠️❌, (2) Anomalies oubliées par junior, (3) Écritures de régularisation, (4) Verdict définitif noté

**Points de vigilance que l'auditeur doit OBLIGATOIREMENT vérifier** :
- ✓ Calcul exact du résultat (différencier résultat avant IS et après IS)
- ✓ **Distinction SA vs SARL** pour les références AUSCGIE (art. 664 SA / art. 371 SARL pour la perte des capitaux propres < 50% capital)
- ✓ **IMF Côte d'Ivoire** : plancher 3 000 000 FCFA, plafond 35 000 000 (art. 39 et s. CGI CI) — JAMAIS dire « IMF = 0,5% × CA » sans rappeler le plancher
- ✓ **Taux CNPS CI 2025** : Prestations familiales 5,75% + AT 2-5% + Retraite 7,7% patronal = **15-18% selon secteur** (BTP plutôt haut de fourchette)
- ✓ **Lecture compte de tiers** : le solde fin d'un compte 43x N'EST PAS le cumul des cotisations N (c'est uniquement le reliquat à payer). Cumul = mouvements crédit de l'exercice
- ✓ **Sous-traitance BTP** : ratio 55-75% du CA est NORMAL (compte 6058 « achats travaux/matériels/équipements ») — ne pas le qualifier en anomalie
- ✓ **Conventions réglementées CCA** : AUSCGIE art. 350 (SARL) ou 438 (SA)
- ✓ **Sous-capitalisation fiscale** (CGI art. 18) ne s'applique QUE si les CCA sont rémunérés
- ✓ **Cessation paiements** (AUPCAP art. 25) : actif disponible < passif exigible → déclaration tribunal 30 jours

### Étape 4 — Synthèse contradictoire et position définitive
Consolider en tableau :
| Code | Anomalie | Statut | Junior | Auditeur | Position définitive |
|---|---|---|---|---|---|
| A1 | … | ✅⚠️❌ | dit X | dit Y | Z |

Faire émerger **les anomalies OUBLIÉES par le junior** (codes B1, B2, B3…) qui sont souvent les plus graves :
- **B-type** : Immobilisations totalement amorties avec dotations indues
- **B-type** : Comptes de tiers passif avec soldes débiteurs anormaux (4428, 4470 D = erreur)
- **B-type** : Dotations de rattrapage non documentées (toute la dotation cumulée passée sur l'exercice)
- **B-type** : Absence provision IFC (engagements retraite — art. 33 AUDCIF)
- **B-type** : Critères AUPCAP art. 25 cessation paiements

### Étape 5 — Rédaction des écritures de régularisation (REG-01 à REG-NN)
Format standardisé MDC :
```
REG-XX (Description courte)
Base légale : <article exact>
D xxxx Compte source          xxx FCFA
  C yyyy Compte cible              xxx FCFA
Impact Résultat : +/- xxx
Impact Bilan : +/- xxx
```

**Catalogue type des régularisations courantes** :
- **REG-Suspens** : `D 6588 / C 47xx` (apurement comptes d'attente non justifiés)
- **REG-Ouverture** : `D 1291 ou cpt destination / C 4700` (solde du compte d'ouverture)
- **REG-AmortIndu** : `D 28xx / C 6813` (extourne dotation sur bien totalement amorti)
- **REG-IFC** : `D 6911 / C 1971` (provision pensions retraite estimée actuariellement)
- **REG-SensInversé** : `D 4495 / C 4428` (reclasser solde D anormal d'un compte passif en créance)
- **REG-RecapCCA** : `D 164 + 462x / C 1013` (incorporation comptes courants au capital sur décision AGE)
- **REG-IS-IMF** : reclassement IS comptabilisé en acompte (D 4495) + constatation IMF dû (D 891 / C 4411)
- **REG-CNPS** : provision passif latent `D 6641 / C 431` après recalcul DISA
- **REG-Patente** : `D 6412 / C 446` complément patente non comptabilisée
- **REG-TVA** : centralisation mensuelle propre (D 4431 / C 4441 + 4451 + 4452)

### Étape 6 — Production de la liasse SN complète (cf. §13)
Générer un fichier Excel `LIASSE_<CLIENT>_<ANNEE>.xlsx` avec **9 onglets standardisés** :

| # | Onglet | Contenu | Charte couleur tab |
|---|---|---|---|
| 0 | Page de garde | Identité, documents déposés, références | NAVY |
| 1 | Fiche R1 | Identification fiscale complète | NAVY |
| 2 | Balance | Balance source intégrale + tests équilibre | gris |
| 3 | Bilan | Actif/Passif au format SN avec REF lignes AD-DZ | NAVY |
| 4 | Compte de Résultat | CR avec SIG XA-XI | NAVY |
| 5 | Notes annexes | Notes 3A, 6, 7, 8, 11, 13, 14, 16A, 17, 18, 21, 22, 27A, 28 | gris |
| 6 | Régularisations | Écritures REG-01 à REG-NN + synthèse impact | ROUGE |
| 7 | Synthèse Indicateurs | SIG + CAF + Rentabilité + Structure + Alertes juridiques | OR |
| 8 | Rapport Audit Final | Position contradictoire + verdict noté + plan d'action | ROUGE |

**Script de génération Python disponible** : `/Users/bilefilsseverin/.claude/skills/mdc-expert/scripts/generate_liasse_template.py` (à dupliquer et adapter par client).

Template de référence : voir `/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/EXERCICE_2025/generate_liasse_bna.py`.

### Étape 7 — Visa Auditeur ou Refus de Certification
Appliquer la grille §4 :
- Note ≥ A → Visa émis + enregistrement dans `registre_visas.json`
- Note B → Visa avec réserves
- Note C ou D → **Refus + Rapport de Non-Conformité**

### Étape 8 — Plan d'action client priorisé
Format standardisé MDC J+7 / J+15 / J+30 / J+45 / J+60 avec responsabilité (Comptable / Fiscaliste / RH / Juriste).

## 14.3 Bibliothèque des erreurs typiques d'un comptable junior

À chasser systématiquement lors de l'audit contradictoire :

| Erreur fréquente | Réalité technique correcte |
|---|---|
| « Art. 664 AUSCGIE pour SARL » | **Art. 371** pour SARL ; 664 ne s'applique qu'aux SA |
| « IMF = 0,5% × CA » | Plancher **3 M FCFA** plafond **35 M** en CI |
| « Solde 431 = cotisations N » | Solde 431 = **reliquat à payer** ; cumul N = mouvements C |
| « Sous-traitance 60% = anomalie » | Normal en BTP (sectoriel 55-75%) |
| « CCA non rémunérés = sous-cap. fiscale » | Sous-cap. fiscale ne s'applique QUE si intérêts servis |
| « Aucun stock = anomalie » | Pas une anomalie si pas de chantiers en cours documentés |
| « IS sur perte = anomalie » | C'est probablement un acompte ou IMF — à clarifier avant accuser |
| « Compte 60580000 = anomalie d'imputation » | Compte normal SYSCOHADA pour achats travaux BTP |

## 14.4 Cas pratique de référence — BUILDING NEW AFRICA (mai 2026)

Premier déploiement complet de cette méthodologie. Apports :
- **3 anomalies réfutées** sur 10 du junior (A3 CNPS motivation fausse, A4 IS argumentation fausse, A7 sous-traitance ratio sectoriel)
- **5 anomalies majeures ajoutées** par l'auditeur (B1 amort indu, B2 sens inversé 4428, B3 dot rattrapage, B4 IFC absent, B5 cessation paiements)
- **7 régularisations REG-01 à REG-07** finalisées avec bases légales corrigées
- Verdict : **D refus de certification** confirmé, mais sur fondements DIFFÉRENTS de l'analyse junior

Livrables produits :
- `/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/EXERCICE_2025/LIASSE_BUILDING_NEW_AFRICA_2025.xlsx` (9 onglets)
- Script générateur réutilisable

## 14.5 RÈGLE D'OR — Application systématique

> **Dès qu'une balance est fournie par l'utilisateur, déclencher SANS ATTENDRE l'autorisation explicite la procédure complète des 8 étapes** : lecture → junior → auditeur contradictoire → synthèse → régularisations → liasse Excel → visa → plan d'action.
>
> Ne JAMAIS livrer une seule analyse sans contradiction.
> Ne JAMAIS livrer des régularisations sans la liasse SN complète.
> Ne JAMAIS livrer la liasse sans le verdict d'auditeur noté.

---

# 15. ÉTUDE FISCALE — Analyse des incidences fiscales des opérations comptables

Compétence capitalisée depuis le livre **« Les nouveautés du plan comptable révisé de l'OHADA »** (Loé-Mié & Tari, L'Harmattan 2018) — particulièrement les sections « Traitement fiscal » présentes pour chaque thème comptable (pp. 47, 54, 76, 92, 101-104, 111, 158-159, 168).

## 15.1 Principe directeur

> **Comptabilité ≠ Fiscalité.** Le résultat fiscal n'est presque jamais égal au résultat comptable. L'expert comptable doit toujours produire un **tableau de passage** identifiant les **divergences** entre les 2 référentiels et les **retraitements extra-comptables** nécessaires (réintégrations / déductions) pour calculer l'impôt réellement dû.

## 15.2 Catégories de divergences comptabilité/fiscalité (SYSCOHADA révisé)

| Domaine | Divergence possible | Retraitement type |
|---|---|---|
| **Amortissements** | Durée comptable (utilité réelle) vs durée fiscale (barème CGI) | Amortissement dérogatoire (851/151 ↔ 861) |
| **Amortissements** | Méthode UO comptable / linéaire ou dégressif fiscal | Réintégration excédent |
| **Amortissements** | Valeur résiduelle prise en compte en compta, pas en fiscal | Réintégration différence base |
| **Amortissements** | Composants comptables, mais structure unique en fiscal | Réintégration excédent composant |
| **Dépréciations** | Provisions actif déductibles ou non selon CGI Etat-partie | Réintégration si non déductible |
| **Provisions R&C** | IFC, litiges, garanties — généralement NON déductibles en CI | Réintégration totale |
| **Charges immobilisées** | Anciennes charges au compte 475 — non déductibles si solde transféré en RAN | Écriture d'ordre fiscale via 781 |
| **Coûts d'emprunts** | Activés en compta sur actifs éligibles, déductibles en fiscal | Réintégration quote-part activée |
| **Location-acquisition** | Activation en compta (23x + 17x) non reconnue par tous les CGI | Retraitements extra : réintégration dot. amort./intérêts financiers + déduction loyers |
| **Plus-values cession** | Imposition normale OU sursis si réinvestissement 3 ans | Suivi extra-comptable jusqu'à terme |
| **Réévaluation libre** | Écart en capitaux propres mais imposable au taux IS | Imposition à 35% (CI) sur l'écart |
| **Pénalités fiscales** | Comptabilisées en 647, non déductibles | Réintégration totale |
| **Indemnités personnel** | Plafonds exonérés (transport, logement) | Réintégration excédent |
| **CCA non rémunérés** | Pas de sous-cap fiscale (art. 18 CGI CI ne s'applique que si intérêts servis) | — |
| **CCA rémunérés** | Limitation déductibilité : taux BCEAO (prêt marginal) + 2 pts, plafond = capital social (sous-cap.) + 30% BAIIA | Réintégration intérêts excédentaires |

## 15.3 Tableau de passage standard Résultat Comptable → Résultat Fiscal

Format obligatoire pour la DSF (Déclaration Statistique et Fiscale) :

```
RÉSULTAT COMPTABLE AVANT IMPÔT                        XXX
+ RÉINTÉGRATIONS (charges non déductibles)
  R-01 Amortissements indus / excédent fiscal           XXX
  R-02 Dotations rattrapage non documentées             XXX
  R-03 Charges sans pièces justificatives                XXX
  R-04 Pénalités et amendes (647)                        XXX
  R-05 Indemnités personnel excédant plafonds            XXX
  R-06 Provisions non déductibles (IFC, litiges)         XXX
  R-07 Intérêts CCA excédant limites (art. 18 CGI)       XXX
  R-08 Charges sur biens hors exploitation               XXX
  R-09 IS comptabilisé en charges (891 non déductible)   XXX
- DÉDUCTIONS (produits non imposables ou charges déductibles non comptabilisées)
  D-01 Plus-values exonérées (réinvestissement 3 ans)    XXX
  D-02 Reprises de provisions antérieurement réintégrées  XXX
  D-03 Dividendes intragroupe (régime mère-filles)        XXX
  D-04 Crédits d'impôt étrangers à imputer                XXX
  D-05 Amortissements fiscaux > amortissements comptables XXX
= RÉSULTAT FISCAL                                       XXX

IS THÉORIQUE = max(0 ; Résultat fiscal × Taux IS)      XXX
IMF = max(plancher ; min(plafond ; Taux × CA HT))      XXX
IS DÛ = max(IS théorique ; IMF)                        XXX

− Acomptes IS versés                                   XXX
− Crédits d'impôt imputables                           XXX
= SOLDE IS À PAYER (ou RESTITUTION)                    XXX
```

## 15.4 Fiscalité Côte d'Ivoire 2025 — Référentiel chiffré

| Impôt / Taxe | Taux | Base | Plancher | Plafond | Article CGI |
|---|---|---|---|---|---|
| **IS** | 25% | Résultat fiscal | — | — | Art. 51 |
| **IMF** (Impôt Minimum Forfaitaire) | 0,5% | CA HT | **3 000 000** | **35 000 000** | Art. 39 et s. |
| **TVA standard** | 18% | Prix HT | — | — | Art. 339 |
| **TVA réduite (loyers commerciaux)** | 9% | Prix HT | — | — | Art. 340 |
| **ITS** (Impôts sur Traitements et Salaires) | Barème progressif mensuel 0/16/21/24/28/32% | Salaire brut imposable | — | — | Art. 115-116 |
| **Réduction Charges Famille (RICF)** | selon parts (0 → 44 000/mois) | — | — | — | Art. 119 bis |
| **CN** (Contribution Nationale) patronale | 1,2% (local & expatrié) | Salaire brut | — | — | Art. 146 |
| **CE** (Contribution Employeur) — local | **exonéré (0%)** | Salaire brut | — | — | Art. 134-135, 146 |
| **CE** — expatrié | 9,2% | Salaire brut | — | — | Art. 146 |
| **FDFP — Taxe d'Apprentissage (TA)** | 0,4% | Salaire brut | — | — | Art. 143, 146 |
| **FDFP — Formation Continue (TFPC)** | 1,2% | Salaire brut | — | — | Art. 146 |
| **TOTAL charges patronales** | **2,8% local / 12% expatrié** | Salaire brut | — | — | Synoptique DGI AF 2025 |
| **CNPS — Prestations Familiales (PF)** | 5,75% patronal | Salaire brut plafonné 70 000/mois | — | — | Code prévoyance 1999 |
| **CNPS — Accident du Travail (AT)** | 2 à 5% patronal (BTP haut) | Salaire brut plafonné | — | — | Code prévoyance |
| **CNPS — Retraite** | 7,7% patronal + 6,3% salarial | Salaire brut plafonné 2 700 000/mois | — | — | Code prévoyance |
| **Patente — Droit CA** | 0,5% (BTP) | CA HT | — | — | Art. 264 |
| **Patente — Droit Valeur Locative** | 18,5% | VL locaux pro | — | — | Art. 264 |
| **Droits d'enregistrement augmentation capital par incorporation créances** | 0,3% | Montant incorporé | — | — | Art. 754 |
| **Pénalités fiscales** | 25% des droits éludés | — | — | — | Art. 161 |
| **Intérêts de retard** | 1% par mois | Droits dus | — | — | Art. 161 |
| **Prescription droits fiscaux** | 4 à 5 ans | — | — | — | Art. 96 LPF |
| **Prescription CNPS** | 5 ans | — | — | — | Code prévoyance |

## 15.5 Livrable standard MDC — « Étude Fiscale » (4 onglets)

À produire systématiquement APRÈS la liasse SN (Section 14) pour chaque client :

| # | Onglet | Contenu |
|---|---|---|
| 1 | **Passage Compta-Fiscal** | Tableau de retraitements R-01..R-NN / D-01..D-NN + calcul résultat fiscal + IS dû (IS théorique vs IMF) |
| 2 | **Conformité déclarative** | Audit TVA + ITS + FDFP + CNPS + Patente : théorique vs constaté + écart + statut ✅⚠️🔴 |
| 3 | **Exposition fiscale** | Passif latent par catégorie + pénalité 25% + intérêts retard 10%/an + recommandation + priorité |
| 4 | **Plan d'action fiscal** | 15 actions priorisées J+7→J+90, modalité, responsable, coût, gain, ROI |

Nom de fichier : `ETUDE_FISCALE_<CLIENT>_<ANNEE>.xlsx`
Référence : `MC-FISC-<SECTEUR>-<ANNEE>-NNN`
Template : `/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/EXERCICE_2025/generate_etude_fiscale_bna.py`

## 15.6 Workflow MDC pour l'étude fiscale post-balance

À déclencher **automatiquement après production de la liasse SN** :

1. Reprendre le résultat comptable avant IS depuis le CR (XG + XH = avant IS)
2. Lister toutes les opérations comptables ayant un **traitement fiscal divergent** (cf. §15.2)
3. Chiffrer chaque retraitement (R ou D) avec base + montant
4. Calculer le **résultat fiscal** = résultat comptable + Σ Réintégrations − Σ Déductions
5. Calculer **IS théorique** (25% × Résultat fiscal si > 0) et **IMF** (max plancher ; min plafond ; 0,5% × CA HT)
6. Retenir **IS DÛ = max(IS théo ; IMF)**
7. Vérifier la **conformité déclarative** (TVA centralisée, ITS retenu/reversé, FDFP, CNPS, Patente)
8. Quantifier l'**exposition fiscale latente** (sous-déclarations × prescription + pénalités + intérêts)
9. Émettre un **plan d'action fiscal** avec échéances J+7 à J+90, coût/gain, ROI

## 15.7 Règle d'or de l'analyse fiscale

> Une perte comptable ne signifie pas « pas d'impôt ». L'IMF reste dû (plancher 3 M en CI). Et les **réintégrations fiscales peuvent transformer une perte comptable en bénéfice fiscal imposable** — c'est précisément ce qui s'est passé pour BUILDING NEW AFRICA (perte comptable −50 M + réintégrations 9,2 M = résultat fiscal −41 M → IMF 3 M dû).

---

# 16. CONTRÔLE BANQUE ↔ COMPTABILITÉ — Croisement relevé bancaire / écritures comptables

Compétence en cours de construction — sera complétée et démontrée dès le premier relevé bancaire fourni par l'utilisateur. Capitalisation préalable de la méthodologie.

## 16.1 Objectif

Croiser **chaque ligne du relevé bancaire** avec **les écritures comptables** (compte 521 + comptes de tiers contrepartie) pour mesurer :
- Le **taux de couverture / règlement** des factures émises (clients) et reçues (fournisseurs)
- L'**exhaustivité** de la saisie bancaire (toute ligne du relevé doit être en compta)
- La **régularité** (pas d'écriture comptable sans flux bancaire correspondant)
- La **détection d'opérations occultes** (flux bancaires non comptabilisés ou inverse)

## 16.2 Indicateurs à calculer systématiquement

### A. Côté CLIENTS (compte 411 ↔ encaissements 521 D)

| Indicateur | Formule | Norme MDC |
|---|---|---|
| **Taux de recouvrement** | Encaissements clients (mvt D 521 / nature client) ÷ Factures émises N (mvt C 411 N) | > 90% sain ; 70-90% acceptable ; < 70% critique |
| **Taux de couverture** | Encaissements bancaires identifiés ÷ CA TTC N | Idem |
| **Délai moyen recouvrement (DMR)** | (Solde 411 fin N × 360) ÷ CA TTC | < 30j excellent ; 30-60j normal ; > 90j critique |
| **Encaissements non rattachés** | Flux 521 D non liés à un client identifié | Doit être 0 ; sinon enquête |
| **Avoirs reçus non comptabilisés** | Lignes relevé de remboursement non en 411 C | 0 attendu |
| **Chèques impayés** | Lignes "RET impayé" ÷ remises | < 2% attendu |

### B. Côté FOURNISSEURS (compte 401 ↔ décaissements 521 C)

| Indicateur | Formule | Norme MDC |
|---|---|---|
| **Taux de paiement** | Décaissements fournisseurs (mvt C 521 / nature fournisseur) ÷ Factures reçues N (mvt C 401 N) | > 85% sain |
| **Délai moyen paiement (DMP)** | (Solde 401 fin N × 360) ÷ Achats TTC | 30-60j normal |
| **Paiements non identifiés** | Flux 521 C non liés à un fournisseur | Doit être 0 |
| **Paiements urgents en espèces** | Mvt 401 ↔ 571 | À limiter (preuve faible) |

### C. Côté ÉTAT / IMPÔTS / SOCIAL

| Test | Vérification |
|---|---|
| **TVA payée** | Mvt 4441 D = lignes virement DGI sur relevé |
| **IS / IMF payés** | Mvt 441 D = lignes virement DGI |
| **ITS reversé** | Mvt 4470 D = lignes virement DGI |
| **CNPS payée** | Mvt 431 D = lignes virement CNPS |
| **FDFP payée** | Mvt 4478 D = lignes virement FDFP |

### D. Côté PERSONNEL

| Test | Vérification |
|---|---|
| **Salaires payés** | Mvt 422 D = lignes virement salaires mensuels (regroupés ou individuels) |
| **Acomptes** | Mvt 421 D = lignes "ACOMPTE" sur relevé |

### E. Tests de COHÉRENCE GLOBALE (bouclage)

1. **Identité bancaire** : Σ Mvt 521 D + Σ Mvt 521 C = Σ encaissements + Σ décaissements du relevé sur toute la période (à 0 FCFA près)
2. **Solde final** : Solde final relevé bancaire = Solde fin balance compte 521 (rapprochement bancaire)
3. **Écart non rapproché** : tracé et justifié (chèque émis non encore présenté, virement émis non débité…)
4. **Frais bancaires** : Σ lignes frais relevé = Solde mvt 6311
5. **Agios / intérêts** : Σ lignes agios = Solde 671 ou 674

## 16.3 Méthodologie de croisement automatisé

### Étape 1 — Importer le relevé bancaire
Format : PDF, Excel ou CSV. Extraction par ligne :
`Date | Libellé | Référence | Date valeur | Débit | Crédit | Solde progressif`

### Étape 2 — Catégoriser chaque ligne (cf. §2 du SKILL — Analyse de relevés)
Tagger : `Client | Fournisseur | Salaire | Impôt | CNPS | FDFP | Frais bancaire | Cash | Virement interne | Autre`

### Étape 3 — Charger la comptabilité (mouvements 521 D et C par contrepartie)
Pour chaque écriture impliquant 521, identifier le compte de contrepartie.

### Étape 4 — Apparier (matching) ligne par ligne
Critères de matching :
1. **Montant exact** (premier critère)
2. **Date** (à ± 3 jours pour tenir compte de la date valeur)
3. **Libellé / Référence** (mots-clés)

Trois cas :
- ✅ **Apparié** : ligne relevé ↔ écriture compta avec montant et date cohérents
- ⚠️ **Apparié partiel** : montant OK mais date décalée > 5 jours (à investiguer)
- 🔴 **Non apparié** : ligne relevé sans écriture compta ou écriture compta sans ligne relevé

### Étape 5 — Calculer les indicateurs (cf. §16.2)

### Étape 6 — Produire le livrable Excel `RAPPROCHEMENT_BANCAIRE_<CLIENT>_<MOIS>.xlsx`

**Onglets standards** :
1. **Relevé brut** — toutes les lignes du relevé importées
2. **Compta 521** — toutes les écritures du compte 521 sur la période
3. **Matching** — appariement ligne par ligne (vert/orange/rouge)
4. **Indicateurs** — taux de recouvrement, DMR, DMP, % non identifiés
5. **Anomalies** — lignes non appariées avec recommandation
6. **Synthèse exécutive** — verdict + score qualité du suivi bancaire

## 16.4 Catalogue des anomalies typiques détectables

| Code | Anomalie | Diagnostic |
|---|---|---|
| **BCA-01** | Encaissement bancaire sans écriture compta | Vente non comptabilisée (CA dissimulé) ou apport occulte |
| **BCA-02** | Écriture compta de vente sans encaissement | Vente fictive, créance fictive, ou retard saisie banque |
| **BCA-03** | Paiement fournisseur sans facture reçue | Charge dissimulée, paiement personnel, prélèvement gérant |
| **BCA-04** | Frais bancaires non comptabilisés | Sous-évaluation charges 6311 |
| **BCA-05** | Virement interne banque-caisse non équilibré | Compte 581 non soldé |
| **BCA-06** | Salaires payés > salaires comptabilisés | Salaire non déclaré (CNPS/ITS) |
| **BCA-07** | Impôt payé > impôt comptabilisé | Pénalité non comptabilisée |
| **BCA-08** | Encaissement client > facture émise | Avance reçue non saisie en 419 |
| **BCA-09** | Délai recouvrement client > 90 jours | Risque dépréciation 491 |
| **BCA-10** | Concentration encaissements en cash | Risque déclaration CRF (lutte blanchiment) |

## 16.5 Cas d'usage type — Quand l'utilisateur fournit un relevé

**Procédure de déclenchement automatique** :

1. Demander : « Pour quel client / quel mois / quelle banque ? »
2. Lire le relevé via `mcp__PDF_Tools_..._read_pdf_pages`
3. Importer les écritures comptables du compte 521 sur la même période (depuis la balance déjà fournie)
4. Lancer le matching (algorithme §16.3 étape 4)
5. Calculer les 6 indicateurs principaux (Taux recouvrement, DMR, DMP, % non identifiés, frais bancaires, équilibre bouclage)
6. Lister les anomalies BCA-01 à BCA-10
7. Produire le fichier Excel rapprochement
8. Émettre un verdict de **qualité du suivi bancaire** (note AAA → D)

## 16.6 Norme attendue pour un suivi bancaire de qualité (note AAA MDC)

- ≥ 95% des lignes du relevé appariées à des écritures comptables
- 0 anomalie de type BCA-01, BCA-02, BCA-03 (anomalies critiques)
- DMR < 45 jours et DMP > 30 jours (bon équilibre BFR)
- Rapprochement bancaire mensuel formalisé et signé
- Solde théorique compta = Solde relevé bancaire à 0 FCFA près après rapprochement
- Aucun virement interne 581 résiduel en clôture

## 16.7 Statut actuel de la compétence

✅ **Méthodologie capitalisée** (§16.1 à §16.6)
⏳ **Démonstration en attente** : sera produite dès que l'utilisateur fournit son premier relevé bancaire avec la balance associée
📁 **Script Python type** à créer : `generate_rapprochement_bancaire.py` (sera produit lors du premier cas réel)

---

# 17. MÉMO OPÉRATIONNEL — Erreurs commises à ne plus jamais reproduire

Capitalisation des leçons concrètes de la session BUILDING NEW AFRICA (mai 2026), pour devenir un comptable MDC fiable.

## 17.1 ❌ Erreurs à ne JAMAIS reproduire

### Sur l'import des balances

| ❌ Erreur | ✅ Règle absolue |
|---|---|
| Raccourcir `10130000` en `1013` | **Conserver les n° à 8 chiffres EXACTS** tels que dans Sage |
| Normaliser `CAPITAL SOUSCRIT APPELE ET VER` en `Capital souscrit` | **Conserver les libellés EXACTS** (majuscules, fautes, abréviations Sage) |
| Ré-écrire la balance à la main en regardant le PDF | **Préférer l'export Excel/CSV** ; PDF en dernier recours |
| Produire la liasse sans bouclage préalable | **Onglet `0-Bouclage` obligatoire en premier** ; si écart → STOP |
| Omettre un compte « peu significatif » (compte à 1 FCFA) | **Tous les comptes y sont, sans exception** |
| Agréger sous-comptes (`24110001`+`24110003` en `2411`) | **Conserver l'arborescence Sage** |
| Cacher l'écart de bouclage | **Documenter l'écart de manière transparente** dans l'onglet 0 |

### Sur l'analyse d'anomalies

| ❌ Erreur | ✅ Règle absolue |
|---|---|
| Citer art. **664 AUSCGIE** pour une **SARL** | Art. **371 AUSCGIE** pour SARL ; 664 est pour SA |
| Dire « IMF = 0,5% × CA » sans plancher | **IMF CI = max(3 000 000 ; 0,5% × CA HT)** plafonné à 35 M |
| Confondre solde compte tiers (43x) et cumul cotisations | Solde = reliquat ; cumul cotisations = **Mvts C de l'exercice** |
| Qualifier la sous-traitance BTP en anomalie | **Ratio sectoriel 55-75% normal en BTP** |
| Conclure « pas d'IS = anomalie » sur perte | Anomalie seulement si **< IMF plancher 3M** ; sinon perte → IMF dû |
| Présumer sous-cap fiscale (art. 18 CGI) sur CCA non rémunérés | Art. 18 ne s'applique **QUE si intérêts servis** sur CCA |
| Dire « pas de stock = anomalie » | Anomalie SI **chantiers en cours** au 31/12 non valorisés |

### Sur le rapport

| ❌ Erreur | ✅ Règle absolue |
|---|---|
| Livrer une analyse sans contradiction | **TOUJOURS déployer agent auditeur indépendant** |
| Verdict sans note MDC AAA→D | **Toujours une notation motivée** (cf. §4) |
| Plan d'action sans échéances ni responsables | **J+7/J+15/J+30/J+45/J+60** + responsable |
| Tableau d'anomalies sans base légale | **Article exact CGI/AUSCGIE/AUDCIF/AUPCAP** cité |

## 17.2 Checklist standardisée — production d'une liasse depuis une balance

À cocher mentalement à chaque mission :

```
□ 1. Balance reçue : format ? (Excel privilégié, PDF accepté avec test bouclage)
□ 2. Identification entité : raison sociale, forme juridique (SA/SARL/EI), secteur, exercice
□ 3. Import EXHAUSTIF : 100% des lignes, n° 8 chiffres, libellés exacts
□ 4. Onglet 0-Bouclage : Σ Mvt D=C ? Σ Soldes cohérent ? Lignes importées = source ?
□ 5. Si écart > 1 FCFA et version structurée disponible → STOP + demander
□ 6. Si écart résiduel toléré (cas PDF) : DOCUMENTER l'écart transparemment
□ 7. Tests d'anomalies §12.5 (T1 à T16)
□ 8. Production liasse SN 9 onglets (Page garde → Rapport Audit Final)
□ 9. Production Étude fiscale 4 onglets (Passage compta-fiscal → Plan d'action)
□ 10. Déploiement agent auditeur contradictoire (general-purpose)
□ 11. Synthèse contradictoire + position définitive
□ 12. Écritures de régularisation REG-01 à REG-NN
□ 13. Verdict MDC noté AAA→D + plan d'action priorisé
□ 14. Si AAA/AA → Visa émis + registre_visas.json
       Si B/C/D → Refus + Rapport de Non-Conformité
□ 15. Référence dossier MC-LIASSE-<SECTEUR>-<ANNÉE>-NNN
□ 16. Sauvegarde dans /Users/bilefilsseverin/Documents/DOSSIER CLIENTS/<CLIENT>/EXERCICE_<ANNÉE>/
```

## 17.3 Format de réponse type à l'utilisateur après livraison

Toujours structurer une livraison comme :

```
✅ Livrable [Type] généré : [chemin complet]

## Bouclage [✅/⚠️/❌]
[Tests de cohérence + écart résiduel s'il y en a, documenté]

## Synthèse chiffrée
[3-5 indicateurs clés : résultat, CA, anomalies, exposition latente, etc.]

## Verdict MDC
Note : [AAA → D] — [motif principal]

## Pour aller plus loin
[Ce que je peux faire d'autre si l'utilisateur veut]
```

Pas de blabla. Pas de répétition des données déjà visibles dans le fichier produit.

## 17.4 Cas pédagogique de référence — BUILDING NEW AFRICA 2025

Premier client traité avec la méthodologie complète. Apports capitalisés :
- **89 comptes** dans la balance Sage (volumineux ≠ complexe)
- **Capitaux propres négatifs −100M** → art. 371 AUSCGIE (SARL)
- **Risque cessation paiements** AUPCAP art. 25 (TN 3,3M vs dettes CT 25M)
- **Sous-déclaration CNPS** estimée 1-2M/an (pas 5,6M comme dit initialement)
- **IS 11M sur perte = acompte/IS antérieur**, pas anomalie automatique
- **Sous-traitance BTP 61% = normal sectoriel**, pas anomalie
- **Exposition fiscale globale ≈ 33,7 M FCFA** (29% du CA)

Livrables produits (référence à dupliquer) :
- `/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/EXERCICE_2025/`
  - `balance_bna_exhaustive.py` — module Python d'import balance
  - `generate_livrables_v2.py` — générateur liasse complète V2 exhaustive
  - `generate_etude_fiscale_bna.py` — générateur étude fiscale
  - `LIASSE_BNA_2025_V2_EXHAUSTIVE.xlsx` — liasse SN 5 onglets
  - `ETUDE_FISCALE_BUILDING_NEW_AFRICA_2025.xlsx` — étude fiscale 4 onglets

## 17.5 Posture professionnelle MDC

> Un comptable MDC est **honnête sur ses limites** : il dit clairement « je ne peux pas garantir 100% si la source est un PDF Sage compact », il propose la solution (export Excel), il ne masque jamais un écart de bouclage.
>
> Un comptable MDC est **contradictoire avec lui-même** : il déploie systématiquement un auditeur indépendant pour challenger ses propres conclusions ; il accepte de se voir contredire.
>
> Un comptable MDC est **sourcé** : chaque anomalie citée renvoie à un article précis du CGI, de l'AUSCGIE, de l'AUDCIF, du Code prévoyance, etc. ; pas de « il me semble que… »
>
> Un comptable MDC **livre des fichiers, pas des promesses** : chaque mission donne un Excel/Word concret dans un dossier client structuré.

---

# 18. DÉPOUILLEMENT MASSIF DE FACTURES PDF SCANNÉES (pipeline OCR macOS Vision)

Compétence capitalisée sur le dossier BUILDING NEW AFRICA — mai 2026 (144 pages OCR en ~5 min sans installation tierce).

## 18.1 Pipeline complet — Aucune dépendance externe

Quand un client fournit des liasses de factures en PDF (souvent scannés depuis e-Impots, e-Banque ou téléphone) :

| Étape | Outil | Commande type |
|---|---|---|
| 1. Inventaire | PyMuPDF | `fitz.open(pdf); len(doc); doc[0].get_text()` détecte natif vs scanné |
| 2. Conversion PDF→PNG | PyMuPDF | `page.get_pixmap(dpi=220).save("page.png")` |
| 3. OCR FR | **Swift + macOS Vision Framework** (natif, gratuit, précis) | Voir script §18.2 |
| 4. Parser | Python regex | extraction fournisseur, date, TTC, HT, TVA |
| 5. Catégorisation | Mots-clés SYSCOHADA | mapping vers comptes 6xx (cf. §18.3) |
| 6. Livrable Excel | openpyxl + charte MDC (§8) | 4-5 onglets standards |

## 18.2 Script Swift OCR Vision (réutilisable tous clients)

À sauvegarder dans `~/.claude/skills/mdc-expert/scripts/ocr_vision.swift` puis :
```bash
swiftc ocr_vision.swift -o /usr/local/bin/mdc-ocr
mdc-ocr image.png > image.txt
```

Le script Swift complet (35 lignes) est dans `/tmp/bna_ocr/ocr.swift` (copie dans dossier client BNA aussi). Caractéristiques :
- `VNRecognizeTextRequest` avec `.accurate` + langues `["fr-FR", "en-US"]`
- `usesLanguageCorrection = true` (corrige les erreurs OCR par dictionnaire)
- Sortie stdout : 1 bloc texte par ligne reconnue

## 18.3 Catégories SYSCOHADA pré-mappées (BTP + tertiaire)

Référentiel de catégorisation à 17 codes, chacun avec compte SYSCOHADA + mots-clés regex :

| Code | Compte | Mots-clés indicatifs |
|---|---|---|
| MATERIAUX_BTP | 60110000 | béton, BPE, ciment, fer à béton, F500, HLE, agrégat, sable |
| SOUS_TRAITANCE_COFFRAGE | 60580000 | coffrage, panneau HSA, étai, PERI, DMD |
| CARBURANT | 62810000 | Total Energies, Shell, Petroci, Oryx, ZMPX (code pompiste) |
| TELECOM_INTERNET | 62820000 | Orange, MTN, Moov, ADSL, fibre |
| PEAGE_TRANSPORTS | 62480000 | SOCOPRIM, BIP PASS, Pont d'Abidjan |
| EAU_ELECTRICITE | 60510000 | CIE, SODECI, kWh, m3 |
| HONORAIRES_CONSEIL | 63210000 | PwC, Deloitte, KPMG, EY, honoraires |
| IMPRIMERIE_PUB | 62700000 | Netfox, imprimerie, flyers, kakemono |
| MISSIONS_DEPLACEMENT | 62560000 | hôtel, restaurant, billet avion |
| ASSURANCES | 62500000 | NSIA assurance, Allianz, Saham, Sunu |
| FRAIS_BANCAIRES | 63110000 | frais bancaire, commission, agios |
| PATENTE | 64120000 | patente |
| IMPOTS_TAXES | 64180000 | vignette, droits de timbre |

## 18.4 Patterns regex d'extraction (calibrés sur factures CI 2018-2026)

```python
# Net à payer / TTC explicite (priorité)
PAT_TTC = r"(?:net\s*[àa]?\s*payer|montant\s*ttc|total\s*ttc|total\s*[àa]\s*payer)\s*[:.]?\s*(\d[\d\s.,]{2,15})"

# Filtre des faux montants (NCC, téléphone, date, ref facture)
PAT_SUSPECT_LINE = r"(?:ncc|n[°o]\s*cc|t[ée]l|fax|cc\s*[°:]|facture\s*n|bl\s*\d|ref|code|client|bp|cedex)"

# Date : multi-format JJ/MM/YYYY ou JJ mois YYYY
PAT_DATE = r"(\d{1,2})[/\-\.\s](\d{1,2}|janvier|...)[/\-\.\s](20\d{2})"

# Année dans le document (vote majoritaire si pas de date explicite)
PAT_YEAR = r"\b(20[12]\d)\b"
```

## 18.5 Règle de groupement des pages (FACTURE + BL annexés)

Détection page de continuation : présence `BORDEREAU/BON DE LIVRAISON` ET absence `FACTURE/REÇU/DEVIS` → la page est attachée au document précédent (texte concaténé pour la catégorisation).

Cela évite de compter 2 fois la même opération (facture + son BL = 1 doc, pas 2).

## 18.6 Livrables MDC standardisés pour mission « dépouillement factures »

| Fichier | Onglets | Référence MDC |
|---|---|---|
| `DEPOUILLEMENT_FACTURES_<CLIENT>.xlsx` | 1-Récap par charge / 2-Journal écritures SYSCOHADA / 3-Détail pièces / 4-Alertes fiscales | MC-DEP-<SECTEUR>-<ANNÉE>-NNN |
| `CROISEMENT_FACTURES_BALANCE_<CLIENT>.xlsx` | 0-Synthèse exécutive / 1-Matrice par année / 2-Couverture par compte / 3-Détail factures exercice / 4-Argument défense | MC-CRX-<SECTEUR>-<ANNÉE>-NNN |

## 18.7 Alertes fiscales générées automatiquement

4 codes d'alerte standards à émettre sur chaque pièce :

| Code | Critère | Référence | Impact |
|---|---|---|---|
| **ART-373** | Espèces > 250 000 FCFA détecté | Art. 373 CGI CI | TVA non récupérable ≈ 18%/1.18 du TTC |
| **NCC-ABS** | Pas de NCC fournisseur lisible | Art. 144 CGI CI | Charge potentiellement non déductible IS |
| **TEE-FRN** | Fournisseur en régime TEE (non assujetti TVA) | Art. 348 CGI CI | Aucune TVA récupérable (normal) |
| **EX-ANT** | Pièce d'exercice antérieur (< exercice courant -1) | Spécialisation des exercices | À rattacher à l'exercice d'origine |

---

# 19. RÉPONSE À UNE ACCUSATION DGI « CHARGES SANS FACTURE » — Méthodologie défensive

Compétence capitalisée sur dossier BNA exercice 2022 — chef E1 TVA NRD12739430 (mai 2026).

## 19.1 Diagnostic en 4 mesures clés

Quand la DGI accuse le client d'avoir comptabilisé des charges sans pièces justificatives :

| Indicateur | Calcul | Interprétation |
|---|---|---|
| **Charges déclarées HT** | Σ Mvt D classes 6 de la balance, hors dotations 68 | Le montant que la DGI dit non justifié |
| **Σ Factures HT** | Dépouillement OCR ÷ 1,18 (toutes catégories) | Le montant dont le client a la preuve |
| **Ratio Factures / Charges** | Σ Factures HT ÷ Charges déclarées HT | > 1 = défense gagnée / < 1 = compléments requis |
| **Écart absolu** | Σ Factures HT − Charges déclarées HT | > 0 = factures non comptabilisées (sous-déclaration favorable) |

## 19.2 Argumentaire-type (à reproduire en mémoire en décharge)

Si **Ratio > 1** (cas BNA 2022 — ratio 2,25) :
> « Le Agence MDC a dépouillé exhaustivement les factures fournisseurs de l'exercice N, totalisant Σ FCFA HT,
> soit X fois le montant des charges figurant dans la balance Sage (Σ FCFA HT).
> Loin d'avoir comptabilisé des charges fictives, le contribuable a au contraire **sous-comptabilisé**
> ses charges réelles. L'accusation de charges sans pièces est donc factuellement inversée :
> ce sont des **factures sans écritures comptables** qu'il faudrait régulariser, avec un impact
> résultat fiscal FAVORABLE au contribuable (réduction du bénéfice imposable). »

Si **Ratio < 1** : demander au client les factures manquantes avant de répondre. Ne jamais admettre la position DGI.

## 19.3 Pièces probantes à joindre obligatoirement

1. **Liasse Sage** complète (balance 4 ans, GL des comptes 6xx, journal achats)
2. **Recueil des factures** numérotées et indexées (PDF assemblé)
3. **Fichier Excel `DEPOUILLEMENT_FACTURES_<CLIENT>.xlsx`** (preuve du travail MDC)
4. **Fichier Excel `CROISEMENT_FACTURES_BALANCE_<CLIENT>.xlsx`** avec verdict chiffré
5. **Tableau de passage compta-fiscal** montrant que même après réintégrations fiscales, le résultat reste cohérent

## 19.4 Anti-pattern à ne pas commettre

| ❌ | ✅ |
|---|---|
| Reconnaître implicitement la position DGI en transmettant les factures sans démonstration chiffrée | Toujours produire le ratio Σ Factures HT / Σ Charges déclarées AVANT envoi DGI |
| Confondre TTC et HT dans les comparaisons | Toujours convertir TTC → HT (÷ 1,18) avant comparaison aux comptes 6xx (HT) |
| Comparer factures d'une année aux charges d'une autre | Strict respect de la spécialisation : factures N ↔ balance N |
| Ignorer les factures non datées | Soit les rattacher par contexte (papier en-tête, fournisseur récurrent), soit les déclarer hors périmètre |
| Surestimer le TTC quand le montant n'est pas explicite | Filtrer les NCC, téléphones, dates, références ; préférer ligne contenant « total/net/montant » |

## 19.5 Cas pratique de référence — BNA 2022

| Donnée | Valeur |
|---|---|
| CA 706 HT déclaré 2022 | 161 736 732 FCFA |
| Résultat net 2022 | +27 567 383 FCFA |
| Charges totales 2022 (CA − Résultat) | 134 169 349 FCFA |
| Factures 2022 dépouillées (77 pièces) | 356 262 360 FCFA TTC = 301 917 230 FCFA HT |
| **Ratio Factures / Charges** | **2,25** ✅ |
| Comptes 60110000 / 60580000 dans balance | 0 FCFA (anomalie comptable BNA — sous-comptabilisation matériaux et sous-traitance BTP) |
| Verdict défense DGI | INVALIDATION FACTUELLE de l'accusation « charges sans facture » |

Livrable de référence : `Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/EXERCICE_2025/CROISEMENT_FACTURES_BALANCE_BNA.xlsx`

---

# 20. BIBLIOTHÈQUE FISCALE & COMPTABLE IVOIRIENNE — DOCTRINE SOURCÉE (4 ouvrages assimilés)

Compétence capitalisée (juin 2026) après assimilation intégrale par OCR de 4 ouvrages de référence (~2 876 pages scannées) fournis par le gérant. **Le savoir détaillé, sourcé article par article (CGI, Annexes Fiscales 2023/2024/2025, directives UEMOA, SYSCOHADA révisé), vit dans 4 fiches de doctrine** rangées dans `~/.claude/skills/mdc-expert/reference/`. Texte OCR brut conservé chez le client : `Desktop/MES DOCS FISCALITÉ /_OCR_TEXTE/` (un `.txt` consolidé + dossiers page-par-page pour recherche fine). Pipeline OCR : Vision macOS (`scripts/mdc-ocr`, cf. §18) + `scripts/ocr_orchestrator.py`.

## 20.0 Index des fiches — QUAND LES OUVRIR

| Fiche (`reference/…`) | Source | Ouvrir pour… |
|---|---|---|
| **FICHE_IMPOTS_BENEFICES.md** | Niamba/AI-FISC 2024 | IS/I-BIC, IMF, régimes RE/RME/RSI/RNI, amortissements & provisions fiscaux, déficits/ARD, plus-values Art 28, Art 110, crédits d'impôt, BNC, passage compta→fiscal |
| **FICHE_TVA_TOB_TSE_AIRSI.md** | Niamba/AI-FISC 2025 | TVA (champ, exigibilité, déduction, prorata, butoir, remboursement), TOB, TSE, AIRSI, Retenue 2 %, FNE, obligations & sanctions |
| **FICHE_COMPTA_SYSCOHADA.md** | Doumbia Diakariya | Écritures-types SYSCOHADA, immobilisations/amortissements, stocks, personnel, états financiers, SIG, 15 opérations spécifiques |
| **FICHE_SYSCOHADA_IFRS.md** | Kadouamai/L'Harmattan | Divergences SYSCOHADA↔IFRS, crédit-bail (IAS 17), IFC (IAS 19), impôts différés (IAS 12), retraitements |

> **Réflexe** : avant toute mission fiscale/comptable CI, **lire la fiche concernée** (Read). Pour un point précis (un article, un cas), `grep` le `.txt` consolidé puis ouvrir la page exacte dans `_pages/pXXXX.txt`.

## 20.1 ⚠️ CORRECTIONS aux sections antérieures du skill (priment désormais)

1. **Architecture des régimes par CA TTC** — la grille exacte (réforme PME, AF 2021 art. 33) est :

| CA TTC annuel | Catégorie | Régime / Impôt | TVA |
|---|---|---|---|
| 0 – 5 M | Entreprenant (TPE) | **TCE** Taxe Communale Entreprenant : **2 %** commerce / **2,5 %** autres | Non |
| ] 5 M – 50 M ] | Entreprenant (TPE) | **TEE** Taxe d'État Entreprenant : **4 %** commerce / **5 %** autres | Non |
| ] 50 M – 200 M ] | Microentreprise | **IME/RME** : **6 %** (4 % si CGA ou expert-comptable conventionné) | Non (sauf option) |
| ] 200 M – 500 M ] | Petite Entreprise | **RSI** réel simplifié : I-BIC 25 % + IMF | Oui (de droit) |
| > 500 M | Moyenne/Grande Ent. | **RNI** réel normal : I-BIC 25 % + IMF | Oui (de droit) |

   → **Corrige** §3 (audit) qui disait « TEE ≤ 5M » et « RME 5-200M » : c'est **TCE** 0-5M, **TEE** 5-50M, **IME/RME** 50-200M. Le seuil d'assujettissement TVA de plein droit est **200 M** (ex-50 M).
   → La règle « JAMAIS dire IS/RME » de §3 valait pour un contexte d'audit où le client était entreprenant ; en doctrine générale, **IS = I-BIC** et **RME = régime microentreprise (IME)** sont des termes parfaitement valides. Adapter au contexte.

2. **Établissements multiples** (TCE/TEE/IME, CGI Art 78-2°) : chaque établissement est un foyer d'imposition séparé **tant que le CA cumulé ne fait pas changer de régime**. Levier d'optimisation (cf. fiche).

3. **Intérêts comptes courants d'associés** : **4 limites CUMULATIVES** (cf. §15.2 enrichi) — (1) capital intégralement libéré sinon rejet **total** ; (2) montant ≤ capital social ; (3) taux ≤ **BCEAO prêt marginal + 2 pts** (et non +3) ; (4) total intérêts ≤ **30 % du BAIIA** ; + remboursement sous 5 ans. (CGI Art 18-A.)

## 20.2 Mémo-flash des taux & seuils (Côte d'Ivoire, à jour AF 2025)

| Impôt/Taxe | Taux | Base | Plancher/Plafond | Réf. |
|---|---|---|---|---|
| **I-BIC (IS)** | **25 %** droit commun ; **30 %** télécoms/TIC ; **12 %** plus-values holding (titres ≥ 2 ans) | Résultat fiscal | — | CGI Art 51, 64, 23 |
| **IMF** | **0,5 %** (0,10 % pétrole/eau/élec/gaz ; 0,15 % banques/assur.) | CA TTC | **3 M** plancher ; **35 M** plafond (RNI) ; **RSI sans plafond** | CGI Art 39-41, 53 |
| **TVA** | **18 %** normal ; **9 %** réduit ; 0 % export | Prix HT | seuil assujetti **200 M** | CGI Art 359 |
| **TOB** | **10 %** ; **5 %** (PME, CA < 1 Md) | HT | — | CGI Art 401 |
| **TSE** | **0,1 %** | CA total HT (réel uniquement) | ni imputable ni remboursable, mais **déductible au bénéfice** | CGI Art 1084 |
| **AIRSI** | **5 %** ; 1,5 % / 2 % / 0,2 % (listes produits) | TTC (vente taxable) / HT / CAF+DD+TVA (import) | acompte IGR **inopérant** (IGR suspendu) → acquis Trésor | Loi 90-434 |
| **Retenue 2 %** | **2 %** | paiements prestataires informels (par les réels) | non si retenue BIC/BNC 7,5 % déjà faite | CGI Art 84 bis |
| **Prélèvement 5 % Trésor** | 5 % | paiements aux TCE/TEE/IME | **SUSPENDU** (AF 2025 Art 13) | CGI Art 259 bis |
| **Charges espèces > 250 000** | **non déductibles** IS + TVA non récupérable | — | payer par voie bancaire | CGI Art 18 bis, 373 |
| **Calendrier paiement** | 3 fractions : **10**/**15**/**20** avril-juin-sept (industriel/commercial/prestataire) | — | déclaration résultats 30 mai (ou 30 juin si CAC) | Ord. 2015-797 |

## 20.3 Réflexes d'optimisation (ingénierie fiscale légale — le cœur de la demande gérant)

> « La fiscalité ne sert à rien sans comptabilité » — chaque levier ci-dessous suppose une **compta régulière et complète** (condition de l'Art 110, des provisions, du crédit de TVA…). Détail + chiffrage dans les fiches §10 (bénéfices) et §5 (TVA).

1. **Choix/arbitrage de régime** : rester sous un seuil (forfait simple, pas de TVA < 200 M) **vs** opter pour le réel si charges réelles élevées (le forfait taxe le **CA brut**, le réel le **bénéfice net**). Option microentreprise→RSI désormais **sans plancher** (LF 2024) mais **irrévocable 3 ans**.
2. **CGA / expert-comptable conventionné** : **−50 %** sur TEE (4 %→effectif) et IME (6 %→4 %). Quasi-systématique. Piège : renonciation < 3 ans = remise en cause rétroactive.
3. **Amortissements dérogatoires** (accéléré, dégressif coeff. 1,5/2/2,5, **40 % logements personnel**) → anticiper la charge déductible, différer l'impôt ; écart géré en extra-comptable.
4. **ARD (report illimité)** > déficit ordinaire Art 26 (5 ans) : en période déficitaire, **maximiser la part ARD**. Imputer les déficits Art 26 en priorité car périssables.
5. **Plus-values en sursis (Art 28)** : engagement de réinvestissement sous 3 ans (montant = PV + Vo) → impôt différé, trésorerie préservée.
6. **Holding (Art 23)** : PV titres ≥ 2 ans à **12 %**, **exonération totale** si portefeuille ≥ 60 % UEMOA ; régime mère-fille (Art 22) : dividendes exonérés 50-100 %.
7. **Art 110** : déduction **35 %/40 %** des réinvestissements agréés, étalée 4 ans (plafond 50 % du bénéfice fiscal/an, reliquat reportable). Bénéfices effectifs uniquement (pas l'emprunt).
8. **Crédits d'impôt emploi** : 500 000 / 1 000 000 / 1 500 000 par emploi national CDI. Piège : non imputé l'année d'obtention = **perdu**.
9. **TVA** : délai de rattrapage **12 mois** depuis l'exigibilité (AF 2023) ; option **régime des débits** ; **crédit de départ** au passage forfait→réel ; **secteurs distincts** pour échapper au prorata pénalisant ; **remboursement** (export accéléré 15 j sans caution, investissements > 40 M, taux 9 %) ; **débours** (mandat + reddition) hors assiette.
10. **Véhicules déductibles** : utilitaires / tourisme ≤ 12 CV / 2-3 roues ≤ 3 M HT, ou statut transport public au réel (carburant 100 %).

## 20.4 Pièges sanctionnés (à blinder en audit/conseil)
- Charges/achats **> 250 000 F en espèces** → non déductibles IS + TVA non récupérable (Art 18 bis, 373).
- **Facturer la TVA** sous 200 M ou en forfait → redressement. **Déduire une TVA illégalement facturée / facture non normalisée (FNE)** → rejet.
- Intérêts C/C associés hors des 4 limites → réintégration ; capital non libéré → rejet total.
- I-BIC, IMF, amendes/pénalités, appointements de l'exploitant individuel → **non déductibles**.
- Provision **générale/forfaitaire/éventuelle** → rejetée (objet précis + probabilité + relevé des provisions obligatoires).
- Prix de transfert : ETII + master/local file dès **CA > 500 M** en groupe multinational ; amende 5 M/déclaration.
- **FNE** (facture normalisée électronique) obligatoire par paliers 2025 (RNI 01/06, RSI 01/07, RME 01/08, Entreprenant 01/09) ; déconnexion frauduleuse = responsabilité **pénale** (Art 171 bis LPF).
- **Avertissement DGI** : le SYSCOHADA ≠ fiscalité ; **retraitements extra-comptables obligatoires** avant déclaration (Note DGI 01218 du 12/04/2022).

## 20.5 Règle d'or — entretien de cette bibliothèque
À chaque mission qui mobilise un de ces ouvrages, vérifier que la fiche correspondante est à jour de la **dernière Annexe Fiscale** (les AF sortent chaque janvier). Si une nouvelle AF modifie un taux/seuil, mettre à jour la fiche `reference/…` ET le mémo-flash §20.2. Si un nouvel ouvrage est fourni : OCR via `scripts/ocr_orchestrator.py` → fiche de doctrine → nouvelle entrée §20.0.

---

# 21. ⭐ CŒUR DE MÉTIER MDC — RECONSTITUTION BASE COMPTABLE → ANOMALIES → PROPOSITIONS

> **C'est l'activité PRINCIPALE du gérant.** Dès qu'une liasse / des états financiers sont fournis (PDF DGI, bilan, CR, notes), déclencher ce workflow.

**Sens INVERSE de §13** : on part des **états financiers publiés** pour **remonter** à la base comptable, puis on détecte les anomalies, puis on propose.

**Méthode détaillée + mapping INVERSE (états → comptes)** : `reference/METHODE_RECONSTITUTION_BASE_COMPTABLE.md`

**Les 7 étapes (résumé) :**
1. **Inventaire** des états dispo (manque = 1ʳᵉ anomalie).
2. **Tests de bouclage** (Actif=Passif, Résultat CR=Bilan, Σnotes=totaux) — bloquant.
3. **Reconstituer la BALANCE** par dé-mapping états→comptes (soldes N et N-1).
4. **Reconstituer les écritures** (Mvt net = Solde N − Solde N-1 ; appui Notes 3A/3C/28/14 + TFT + écritures-types).
5. **Matrice d'anomalies** (§12.5, codes P/A/R/T/N/F/S).
6. **Propositions** : écritures REG-xx (§14.5) + plan d'action.
7. **Audit contradictoire** (§14.3) + verdict AAA→D + visa/refus.

**Articulation skill** : cette méthode s'appuie sur §1 (Mission Type 2), §12 (lecture balance + 16 tests), §13 (mapping direct, à inverser), §14 (audit contradictoire), §15 (étude fiscale), §16 (rapprochement bancaire), §17 (mémo erreurs), **§27 (élaboration d'une base comptable annuelle sur pièces déclaratives TEE/SMT — cas sans balance ni relevés)**, et les fiches `reference/` (doctrine sourcée).

**Règle d'or** : on ne livre jamais une « base propre » fabriquée par-dessus une liasse qui ne boucle pas — la 1ʳᵉ livraison est alors la **liste des anomalies de bouclage**.

---

# 22. CHARGÉE DE RÉDACTION DES LIVRABLES LMDC

Compétence de production des livrables clients, à l'identité officielle MDC (logo + charte).
**Bibliothèque + structures** : `reference/BIBLIOTHEQUE_LIVRABLES_LMDC.md`.
**Générateur branché** : `scripts/generate_livrable_mdc.py md dest.docx "Titre" "Client" "Réf"` — **aligné juillet 2026 sur le rendu « papier à en-tête cabinet » de §9.0** : tête de lettre à LOGO (logo gauche / identité droite, double filet navy-or), **filigrane CONFIDENTIEL en diagonale sur chaque page**, titres centrés à filet or, tableaux à filets horizontaux fins (en-tête navy à liseré or, montants à droite, lignes TOTAL détectées sur fond or pâle), pied légal à filet or. Ne jamais régresser vers le bandeau texte ou les tableaux à grille.
**Modèles prêts** : `Documents/LIVRABLES AUDIT LMDC/03_NOTATION_RAPPORTS/MODELE_NOTATION_CONFORMITE_MDC.docx`, `MANUEL_PROCEDURE_AUDIT_CONFORMITE_MDC.docx`.
Règles : toujours FCFA + droit ivoirien/OHADA ; rebrander à l'identité MDC (jamais « MON COMPTABLE ») ; chaque écriture/anomalie sourcée et expliquée ; secret professionnel.

---

---

# 23. LIVRABLES INTERMÉDIAIRES D'AUDIT (11 livrables, LI-1 à LI-11)

Collection complète qui alimente la Notation et les Régularisations. **Détail + enchaînement** : `reference/LIVRABLES_INTERMEDIAIRES_AUDIT.md`. **Modèles brandés** : `Documents/LIVRABLES AUDIT LMDC/02_LIVRABLES_INTERMEDIAIRES/`.
- Bloc A (flux) : LI-1 relevé bancaire (apports/clients/prestataires) · LI-5 CA réel · LI-6 trésorerie.
- Bloc B (compta) : LI-2 état financier · LI-7 immo/amort · LI-8 tiers.
- Bloc C (fiscal) : LI-4 natures d'impôts · LI-3 redressement.
- Bloc D (social/travail) : LI-9 CNPS · LI-10 Inspection du travail.
- Bloc E (juridique) : LI-11 documentaire & juridique.
- Bloc F (procédures) : LI-13 audit des bonnes pratiques & contrôle interne (...).
- Bloc G (dirigeants & capital) : LI-14 rémunération des gérants/associés & dividendes — déductibilité/ITS, part excessive -> IRVM 15% (Art 182), comptes courants (Art 18), réserve légale 10% (AUSCGIE 346), distributions déguisées (traitement/scan/conservation des pièces, délais & sincérité déclaratives, gestion des contrats, séparation des tâches, archivage 10 ans).
Enchaînement : LI-2 base → LI-1/5/6 flux → LI-7/8 compta → LI-4/3 fiscal → LI-9/10/11 social-juridique → reconstitution → matrice → Notation A→E + régularisations.
RÈGLE PERMANENTE : papier à en-tête MDC (`scripts/generate_livrable_mdc.py`), FCFA, droit ivoirien/OHADA.

---

# 24. PROTOCOLE D'AUDIT MDC IMPLÉMENTABLE (A→Z) — capstone

Orchestration complète, à dérouler à CHAQUE mission. **VUE MAÎTRESSE de tous les livrables (validés + proposés), emplacements, feuille de route, références MC** : `reference/FICHE_USINE_LIVRABLES_AUDIT.md`. **Manuel équipes** : `Documents/LIVRABLES AUDIT LMDC/00_MANUELS_PROCEDURES/MANUEL_AUDIT_EQUIPES_MDC.docx`.

**Chaîne de compétences (et sections sources) :**
1. Cadrage : Note méthodo + Proposition (§6, §11) → contrat signé.
2. **Audit documentaire AXE I / LI-0** (`reference/FICHE_AUDIT_DOCUMENTAIRE_AXE_I.md`, formulaire XLSX) → score /20, RBE.
3. **12 livrables intermédiaires LI-1..LI-12** (§23, `reference/LIVRABLES_INTERMEDIAIRES_AUDIT.md`).
4. **Reconstitution** base→balance→CR (§21, mapping inverse).
4bis. **Audit des éléments du plan comptable — contrôle des comptes par 8 cycles** (capitaux, ressources durables, immobilisations, stocks, clients/ventes, fournisseurs/achats, personnel/social, État/trésorerie) : 5 assertions (existence, exhaustivité, valorisation, coupure, droits et obligations) × diligences × feuille maîtresse par cycle et par exercice, puis triangles MDLC transverses. Précédé des **inventaires de mission** (immobilisations, stocks, personnel, éléments comptables — comptage en binôme, fiches signées, art. 17 AUDCIF). Manuels : `Documents/LIVRABLES AUDIT LMDC/00_MANUELS_PROCEDURES/MANUEL_AUDIT_ELEMENTS_PLAN_COMPTABLE_MDC.docx` (MC-MAN-CYCLES-2026-001) + gabarit client `MANUEL_INVENTAIRES` (1er cas : Collège Saint-Exupéry, MC-INV-EDUC-2026-001, juillet 2026).
5. **Matrice d'anomalies** (§12.5 : 16 tests, codes P/A/R/T/N/F/S) + **audit contradictoire** (§14).
6. **Étude fiscale** (§15) + exposition (§19, §20).
7. **Notation A→E** + **régularisations REG** expliquées + **rapport final** + **visa** (§3, §4).

**Quality gates bloquants** : bouclage (Actif=Passif, CR=Bilan, ΣD=ΣC) · sourcing article par article · contradiction · équilibre REG.
**Règles permanentes** : papier à en-tête MDC (`scripts/generate_livrable_mdc.py`) · FCFA · droit ivoirien/OHADA · jamais de base sur liasse qui ne boucle pas · secret professionnel.
**Sortie standard** : note A→E + exposition FCFA + base reconstituée + régularisations + plan J+7→J+60, dans le dossier client visé.

---

# 25. ⛔ RÈGLES ABSOLUES DE PASSATION D'ÉCRITURES (capitalisé — cas FAMILLE KRA SARL, juin 2026)

Deux fautes de débutant ont été commises sur la reconstitution FAMILLE KRA et **ne doivent PLUS JAMAIS se reproduire**, sur AUCUN travail comptable (reconstitution, journal, régularisation, à-nouveau, liasse, audit).

## 25.1 ⛔ JAMAIS de trésorerie directement contre une classe 6 ou 7 — toujours via un TIERS

**INTERDIT ABSOLU** : solder un compte de trésorerie (**521 Banque, 571 Caisse, 53 mobile money**) directement contre un compte de **produits (classe 7)** ou de **charges (classe 6)**.

Toute opération s'articule **EN DEUX TEMPS** via un compte de **tiers (classe 4)** :

| Opération | 1. Engagement (constatation) | 2. Règlement (trésorerie) |
|---|---|---|
| **Vente** | D 411 Clients / C 701 (+ C 443 si TVA) | D 521/571 / C 411 |
| **Achat** | D 60x (+ D 445 si TVA) / C 401 Fournisseurs | D 401 / C 521/571 |
| **Service / loyer** | D 62x-63x / C 401 | D 401 / C 521/571 |
| **Salaire** | D 661 / C 422 Personnel | D 422 / C 521/571 |
| **Impôt / taxe** | D 64x / C 44x État | D 44x / C 521/571 |
| **CNPS** | D 664 / C 431 | D 431 / C 521/571 |
| **Emprunt** | D 521 / C 16x (déblocage) ; D 16x + D 671 / C 521 (échéance) | — |

❌ FAUX : `D 571 / C 701` (vente espèces) — `D 601 / C 521` (achat réglé banque) — `D 661 / C 521` (salaire payé) — `D 641 / C 521`.
✅ JUSTE : passer d'abord par 411 / 401 / 422 / 44x, puis solder le tiers par la trésorerie.

**Seules exceptions tolérées** (flux sans tiers identifiable, à justifier) : frais bancaires `D 6311 / C 521`, agios `D 671/674 / C 521`, virements internes banque↔caisse `D 585 / C 521` puis `D 571 / C 585`. Hors ces cas, **un flux de trésorerie a TOUJOURS une contrepartie de tiers**.

**Bénéfice méthodologique** : c'est précisément l'écart entre **charges constatées (engagées via 401/44/422)** et **paiements (décaissés via 521/571)** qui **reconstitue les dettes** au 31/12 (solde créditeur des tiers). Sans passage par les tiers, on perd cette information et on fabrique un bilan faux (cf. §21, articulation charges→paiements→dettes).

### 25.1.bis ⛔ TOUJOURS constater la charge AVANT le règlement (principe de constatation préalable)

L'ordre est **non négociable** et chronologique :
1. **Constatation (engagement)** : la charge naît à la réception de la facture / du fait générateur → `D 60x-66x / C 401-422-44x`. **C'est ici que la charge entre en comptabilité.**
2. **Règlement (paiement)** : seulement ensuite → `D 401-422-44x / C 521-571`.

**INTERDIT** : débiter un tiers (401/422/44) qui n'a jamais été crédité par une constatation préalable — c'est-à-dire **payer une charge qui n'a pas été enregistrée**. Tout règlement présuppose une charge déjà constatée.
- Une charge peut être constatée et **non encore payée** → elle reste en dette (solde créditeur du tiers) : **NORMAL**.
- Un paiement **sans charge constatée au préalable** → **ANOMALIE** (décaissement injustifié, prélèvement occulte, charge dissimulée) : à investiguer, jamais à passer en direct contre la trésorerie.

En clôture (FNP/charges à payer) : si la charge de l'exercice n'a pas encore de facture, la **constater quand même** au 31/12 via `D 60x / C 408` (fournisseurs, factures non parvenues) — la charge précède toujours le décaissement, jamais l'inverse.

## 25.2 ⛔ NE JAMAIS oublier ni forfaitiser le CAPITAL

Le **capital social** doit TOUJOURS être identifié, ventilé et tracé sur sa propre ligne — **jamais noyé** dans un bloc « capitaux propres » ni inventé au forfait.

1. **Récupérer le capital social réel** aux **statuts / DSV (Déclaration de Souscription et de Versement) / RCCM / liasse antérieure** AVANT toute reconstitution. Si indisponible → le **demander explicitement au client**, ne jamais le deviner.
2. **Ventiler systématiquement** les capitaux propres :
   - **101** Capital social (montant statutaire exact)
   - **104** Compte de l'exploitant (PP) / **105** Primes liées au capital
   - **111-118** Réserves (dont réserve légale 10 % du bénéfice jusqu'à 20 % du capital — Art. 346 AUSCGIE)
   - **121** RAN créditeur / **129** RAN débiteur
   - **13** Résultat de l'exercice (130 bénéfice / 139 perte)
3. **Toute variation du capital exige une AGE documentée** : Art. **360 et s. AUSCGIE** (SARL), Art. 388 et s. (SA). Un capital qui « gonfle » du résultat N-1 sans AGE = **anomalie P-1 (CAP-SANS-AGO)**.
4. Dans toute **balance, bilan, à-nouveau ou reconstitution**, le capital social figure sur une **ligne dédiée 101**, jamais agrégé avec le RAN ou le résultat.
5. À l'**à-nouveau (ouverture N+1)** : reprendre 101 Capital social distinctement, 12x RAN distinctement, et **affecter le résultat N (AGO)** avant ouverture (bénéfice → 111/118/121/465 ; perte → 129).

**Réflexe permanent — check-list de fin de travail comptable (AVANT de livrer)** :
1. ✅ Chaque flux de trésorerie passe par un tiers (jamais 521/571 ↔ classe 6/7) ?
2. ✅ Chaque charge est **constatée AVANT son règlement** (engagement d'abord, paiement ensuite) — aucun décaissement sans charge préalable ?
3. ✅ Le capital social est identifié, isolé sur sa ligne 101, et tracé (statuts/DSV) ?
4. ✅ Variation de stocks = annulation SI **ET** constatation SF (deux écritures, variation = SI−SF) ?
5. ✅ ΣD = ΣC sur chaque bloc ; Actif = Passif ; Résultat CR = Résultat Bilan ?
6. ✅ **Toute dette fiscale CONNUE au 31/12 (AMR, avis, rappel d'exercice antérieur) figure au passif d'ouverture reconstitué** — jamais en charge de l'exercice suivant (spécialisation, AUDCIF Art 59 ; capitalisé audit KRA 2025 : rappel ITS 2024 = dette d'ouverture 447, perte 2024 rectifiée) ?
7. ✅ **La ventilation banque (521) / caisse (571) respecte les pièces** : toute quittance « Espèces » sort de la caisse, tout « Mobile/virement » de la banque — jamais de répartition arbitraire contredite par une quittance (capitalisé audit KRA 2025 : patente payée en espèces → caisse) ?
8. ✅ **La clôture vire le résultat au 131 (bénéfice) / 139 (perte)** — le 130 « en instance d'affectation » n'intervient qu'après décision d'AGO ; patente en **6412**, taxes patronales sur salaires en **6413** ?
9. ✅ **RETENUES À LA SOURCE sur les paiements aux FOURNISSEURS/PRESTATAIRES — opérées ?** Dès qu'un redevable **au réel (RSI/RNI)** paie une **prestation de services** à un fournisseur du **secteur informel (TEE / microentreprise / TCE)**, il DOIT opérer la retenue **PPSSI 2 % (CGI Art. 84 bis)** : `D 401[frn] / C 4471`, le prestataire n'encaisse que le net. Vérifier AUSSI, selon la nature : **RIBIC** (loyers, Art. 56 s.), **RIBNC 7,5 %** (honoraires de professions non commerciales au réel, Art. 92), **AIRSI** (uniquement quand le réel *vend* à l'informel — jamais sur un achat de prestations). ⚠️ Piège capitalisé (GLOBE CÔTE D'IVOIRE, juillet 2026) : honoraires de conseil comptabilisés en charge SANS la retenue → chaque facture de prestataire TEE/RME doit générer sa retenue. La **PPSSI est définitive et non imputable** par le prestataire (le caractère d'acompte a été supprimé).

Si une seule réponse est « non » → **reprendre, ne pas livrer**.

Cas de référence : reconstitution FAMILLE KRA SARL 2024 — `Documents/DOSSIER CLIENTS/FAMILLE KRA/ETAT FINANCIER 25/RECONSTITUTION_FAMILLE_KRA_2024_APPROFONDIE.xlsx` ; oubli de retenue à la source PPSSI → GLOBE CÔTE D'IVOIRE SARL 2026 (`Documents/DOSSIER CLIENTS/GLOBE COTE D'IVOIRE/COMPTABILITE_2026/`).

---

# 26. ⭐ DOCTRINE D'AUDIT MDC — AGENCE DE NOTATION : POSTURE, PROMESSE, NOTATION (capitalisé — mission ALL-IN-ONE CONSULTING, juin 2026)

> MDC est une **agence de notation en matière de conformité**, pas un cabinet qui tient les comptes. Le produit fini d'un audit n'est pas un bilan : c'est une **note adossée à une exposition chiffrée et à des références juridiques**. Lire ce cadre avant toute mission d'audit.

**Manuel de référence (source de vérité, à jour) :** `Documents/LIVRABLES AUDIT LMDC/00_MANUELS_PROCEDURES/`
- `CADRE_METHODOLOGIQUE_AUDIT_CONFORMITE_MDC.docx/.md` — document maître (11 sections)
- `PROCEDURE_P03_DETECTION_ANOMALIES_MDC.docx/.md` — détection opérationnelle + DEE
- `CADRE_METHODOLOGIQUE_NOTATION_CONFORMITE_MDC.docx/.md` — moteur réel vs déclaré

## 26.1 La règle de posture (version définitive — ce que nous cherchons)
> Nous ne refaisons pas la comptabilité du client — **nous l'évaluons**. Nous mesurons trois choses : la solidité de ses **procédures**, le **respect de ses obligations**, et la sincérité de sa **dernière liasse fiscale déposée**, dans laquelle nous détectons les **anomalies comptables, fiscales et sociales**. En confrontant **ce qu'il déclare à la réalité de ses opérations**, nous mesurons l'écart — et nous en déduisons son **niveau d'exposition au redressement** (puis la **note de conformité**).

## 26.2 La promesse = miroir de la posture ; les livrables = miroir des composantes
La posture est la *méthode*, la promesse en est la *restitution au client*, la note adossée à l'exposition en est le *produit fini*. **Chaque livrable répond à une composante de la posture** :
1. Rapport de diagnostic & évaluation du dispositif (procédures + audit documentaire) ;
2. Rapport de conformité des obligations, **par administration** (observation obligation par obligation) ;
3. Matrices d'anomalies (comptable/fiscale/sociale) de la liasse + reconstitution réelle ;
4. Étude d'exposition au redressement (rappels + pénalités + intérêts) + régularisations ;
5. **Note de conformité A→E** (par domaine + globale) ;
6. Plan d'action priorisé (J+7→J+60) ; 7. Présentation exécutive ; (+ Rapport intermédiaire en cours).

## 26.3 Le moteur : réel vs déclaré (3 données reines)
- **Le réel** = relevé bancaire (flux encaissés/payés) + archives/pièces (recevabilité des dépenses).
- **Le déclaré** = états financiers + déclarations fiscales & sociales.
- Confrontation **poste par poste** (CA, charges, masse salariale, impôts, résultat) → écart non justifié = **exposition** (majorée pénalités 25 % art. 161 + intérêts 1 %/mois).
- **Recevabilité d'une dépense** (4 critères cumulatifs, sinon réintégration) : pièce probante/FNE + NCC (art. 18, 144) ; intérêt de l'exploitation (art. 18) ; payée par banque si > 250 000 F (art. 18 bis, 373) ; bon exercice.

## 26.4 Le modèle : l'entreprise au centre + 4 administrations
L'entreprise est reliée à **4 administrations**, chacune portant des **obligations** (déclaration, paiement, procédure) à contrôler. C'est la **carte de navigation** ET l'**interface de restitution** (le client clique une administration → voit nos observations obligation par obligation) :
- **Comptabilité** (SYSCOHADA/AUDCIF) · **Fiscalité** (CGI) · **Droit social/CNPS** (Code prévoyance) · **Inspection du travail** (Loi 2015-532 + CCI 1977).

## 26.5 Démarche en 5 phases
P1 Diagnostic & analyse du dispositif (phare : audit documentaire) → P2 Reconstitution réelle & **cartographie des processus** → P3 Détection des anomalies (3 matrices) → P4 Analyse des processus → P5 Synthèse, exposition & notation.

## 26.6 Cartographie des processus — gabarit unique (1 par cycle)
Cycles : **Dépenses/Achats · Facturation · Encaissement/Trésorerie · Paie/Personnel**. Grille à 6 champs par étape : **Acteur · Déclencheur · Document · Écriture attendue · Point de contrôle · Risque/anomalie**. Incarne la doctrine §25 (constatation avant règlement, toujours via un tiers).

## 26.7 Détection (P-03) — 3 contrôles + DEE
Contrôles d'**existence**, de **régularité de fond**, de **respect des délais** (date de dépôt réelle vs échéance légale — calendrier sourcé : TVA/ITS le 15 du M+1, DGE/DME 10/15/20 ; DSF 30 mai / 30 juin si CAC ; IS/IMF 3 fractions ; CNPS/DISA/DASC à confirmer e-CNPS). Toute anomalie non justifiable → **Demande d'Explication Écrite (DEE)** numérotée, envoyée par l'Assistante de Direction, réponse écrite du client archivée comme preuve, statut justifiée/non justifiée.

## 26.8 Notation A→E + pondération (à valider en comité)
A conforme → E défaut. Pondération indicative : Comptabilité 20 % · Fiscalité 25 % · Social/CNPS 20 % · Inspection travail 15 % · Documentaire 20 %.

## 26.9 Correctif outil capitalisé
`scripts/generate_livrable_mdc.py` : le rendu des **blocs de citation `> `** interprète désormais le **gras `**`** (correctif juin 2026 — avant, les `**` s'affichaient en clair). Éviter l'emphase simple `*…*` dans les `.md` (non interprétée) ; utiliser `**` pour le gras.

Cas de référence : mission ALL-IN-ONE CONSULTING SARL (ex-LIGHT & BRIGHT TECHNOLOGIES) — `Documents/DOSSIER CLIENTS/LIGHT & BRIGHT TECHNOLOGIES/`.

---

# 27. ⭐ ÉLABORATION D'UNE BASE COMPTABLE ANNUELLE SUR PIÈCES DÉCLARATIVES (TEE/SMT) — capitalisé missions FAMILLE KRA 2025 / NADRELIE / LERO, juillet 2026

> Compétence : construire la **comptabilité complète d'un exercice** (journal par codes → balance 6 colonnes → CR → bilan → à-nouveau N+1) pour un client au régime de l'**Entreprenant (TEE) en SMT**, quand on ne dispose QUE des déclarations fiscales et des quittances e-impôts (pas de relevés bancaires, pas de facturier). Livrable de référence : `Documents/DOSSIER CLIENTS/FAMILLE KRA/Comptabilite 2025/COMPTABILITE_FAMILLE_KRA_2025.xlsx` (8 onglets).

## 27.1 Hiérarchie des sources (de la plus probante à la moins probante)

1. **Liasse fiscale déposée N-1** (visée DGI) → ancrage du bilan d'ouverture. Si elle contient des erreurs compensées, ouvrir sur la version RECONSTITUÉE (KRA) ; si elle boucle, la reprendre À L'IDENTIQUE pour rester réconciliable DGI (NADRELIE) — ne JAMAIS surcorriger sans pièce.
2. **Quittances e-impôts** (historique des paiements) → charges fiscales **CERTAINES** avec dates réelles de décaissement. Principe : 1 ligne = 1 mois d'impôt ; séparation stricte charge (période) / paiement (date de sortie d'argent).
3. **Déclarations TEE** → ⚠️ PIÈGE DE MILLÉSIME : la déclaration « période N » (déposée en janvier N) porte les **éléments de N-1** ; le **CA réalisé de l'exercice N est dans la déclaration « période N+1 »** (éléments au 31/12/N). Cas KRA : le CA 2025 (20 100 500) était dans la DECL 2026, pas dans la DEC 2025 (qui portait les éléments 2024).
4. **Estimations** → uniquement en dernier recours, TOUJOURS signalées, résultat présenté en fourchette.

## 27.2 Rétro-calcul des assiettes depuis les avis TEE (outil signature MDC)

**Base implicite d'un avis TEE = Total avis ÷ taux ÷ abattement CGA.**
- Validation KRA : avis 2025 (164 000 + 180 000 = 344 000) ÷ 4 % ÷ 50 % = **17 200 000 = CA de la liasse 2024 au franc près** → la DGI assoit l'avis N sur le CA déclaré en liasse N-1 (avec abattement CGA 50 %), en ÉCARTANT au besoin la déclaration TEE du CGA si elle est plus basse. La DGI **croise donc liasse et déclaration TEE**.
- Usage en DÉTECTEUR : rétro-calculer la base de l'avis N+1 révèle le **CA que la DGI voit** pour N. Cas KRA : avis 2026 (464 036) ÷ 2 % = **23 201 800** vs CA déclaré 20 100 500 → +3,1 M ≈ le stock écoulé → anomalie CRITIQUE à investiguer avant rapport final.
- Deux avis TEE distincts pour un même NCC = deux foyers présumés MAIS le CA TEE est en principe consolidé (CGI Art 72 s.) → exiger la justification DGI (établissement secondaire non déclaré = amende 100 000, LPF Art 146-5).

## 27.3 Ancrage de la masse salariale par les quittances ITS

Le versement ITS mensuel récurrent permet d'inférer la masse salariale : **masse = versement ÷ taux patronal**. Taux patronal local **tranché à 2,8 %** par la grille DGI 2025 (CE local exonérée ; CN 1,2 % + TA 0,4 % + TFPC 1,2 % ; cf. §1 et `reference/FICHE_SYNOPTIQUE_CALENDRIER_DGI.md`) — l'ancienne lecture ÷ 4 % est écartée. Cas KRA : 4 200 ÷ 2,8 % = 150 000 = **2 salariés au SMIG exact** (corroboré par « salaires 900 000 = 12 × 75 000 » en DEC 25 et « 2 employés » en DECL 26) → l'anomalie SMIG se dissout. ITS salarial nul ≤ 75 000/mois. En scénario « ventilation interne » (27.4), le choix N'A AUCUN impact sur le résultat — seule la ligne 661/605 bouge.

## 27.4 Ventilation « déclaration-fidèle » des charges déclarées

La déclaration TEE donne des agrégats (loyers, « autres charges liées à l'activité »). Règle MDC :
1. Les charges **documentées par quittances** (salaires inférés, TEE, patente, ITS patronal) sont ventilées **À L'INTÉRIEUR** de l'agrégat déclaré ; le **résiduel** va en 605 « Autres achats et services ».
2. Le total des charges reste = total déclaré (aucune charge fabriquée au-delà de la déclaration) ; sous TEE le résultat n'a AUCUNE incidence fiscale (impôt assis sur le CA) → la lecture minimisant les montants non documentés prime.
3. **Présenter le résultat en fourchette** [lecture additive ; lecture interne] tant que le client n'a pas produit le détail de l'agrégat (anomalie bloquante pour figer le résultat définitif).

## 27.5 Modèle « CA = commissions/marges » (gros & demi-gros intermédiaires)

- Produits au compte **7062 « Commissions et courtages perçus »** (PAS 7061 qui n'existe pas ; PAS 701 sauf part de revente identifiée).
- ⚠️ EXPOSITION TAUX : les commissions sont des **prestations → TEE 5 %**, pas 4 % commerce ; activité mixte (négoce + commissions) **sans comptabilité séparée → 5 % sur la totalité**. Sécurisation : contrats de mandat/commission écrits + comptabilité séparée négoce (701 + 6031, assiette brute, 4 %) / commissions (7062, 5 %).
- Stock propre écoulé avec CA déclaré « net » : le produit de cession est-il DANS le CA déclaré ? Hypothèse à confronter au rétro-calcul TEE N+1 (27.2) et à faire trancher PAR ÉCRIT par le gérant (vendu ? prix ? détruit ? rendu fournisseur ?).
- **TEE libératoire de la patente** (CGI Art 280-19) : une « patente » payée par un contribuable TEE = paiement INDU (restitution à réclamer) OU patente transporteur d'une activité annexe (indice d'activité mixte).

## 27.6 Comptes à utiliser (corrections capitalisées de l'audit OHADA)

| Poste | ✅ Compte correct | ❌ Erreur à ne plus faire |
|---|---|---|
| Taxes patronales sur salaires (versées via « ITS » e-impôts) | **6413** Taxes sur appointements et salaires | 6313 (classe 63 = services extérieurs ; 631 = frais bancaires) |
| Patente / patente transport | **6412** | 6411 |
| TEE | **6418** (avec note justificative) | — |
| Rappel d'impôt d'exercice antérieur CONNU (AMR) | **Dette d'ouverture 447/442** + perte N-1 rectifiée | 658/647 en charge N (violation AUDCIF Art 59) |
| Résultat à la clôture | **131** bénéfice / **139** perte | 130 (réservé à l'instance d'affectation post-AGO) |
| Contrepartie taxes patronales | 447201 (acceptable) | — |

## 27.7 Trésorerie : la ventilation 521/571 suit les PIÈCES

Chaque quittance porte son mode de paiement : **« Espèces » → C 571 (caisse) ; « Mobile »/virement → C 521 (banque)**. Une répartition banque/caisse contredite par UNE seule quittance espèces est une anomalie (cas KRA : patente 24 000 en espèces → caisse 229 700, pas 253 700). À défaut de relevés, retenir la **ventilation minimale prouvée** et la signaler.

## 27.8 Réconciliation obligatoire entre versions successives

Quand une nouvelle version d'une comptabilité remplace une estimation antérieure : **réconcilier les deux au franc près** (résultat, trésorerie, à-nouveau) dans un bloc dédié de l'onglet Cadrage, archiver l'ancienne version (préfixe OBSOLETE ou note), ne JAMAIS laisser coexister deux versions sans piste d'audit. Cas KRA : ancien résultat 3 742 580 + 804 020 (TEE estimée remplacée par TEE réelle 344 000 logée dans l'enveloppe déclarée) = 4 546 600 exactement.

## 27.9 Audit contradictoire multi-lentilles AVANT livraison (généralisation §14)

Toute base comptable construite sur pièces déclaratives passe par **4 auditeurs indépendants** avant livraison :
1. **Arithmétique** — recalcul intégral au franc près (totaux par avis, par date, ventilations, trésorerie, équilibres) ;
2. **Fiscal CGI** — taux, assiettes, abattements CGA, expositions de requalification, calendriers ;
3. **OHADA/SYSCOHADA** — doctrine §25, numéros de comptes, écritures de clôture, spécialisation des exercices ;
4. **Fidélité aux pièces** — chaque montant tracé à sa pièce OU signalé comme hypothèse ; recherche des paiements manquants ; cohérence avec les livrables antérieurs.
Chaque réfutation fondée est APPLIQUÉE (pas seulement notée) ; les findings non tranchables deviennent des anomalies chiffrées avec pièces à réclamer. Cas de référence : audit contradictoire KRA 2025 (4 agents) — a produit 8 corrections appliquées dont la rectification de la grille ITS, le reclassement 6413/6412/131, la caisse sur pièces et la fourchette de résultat.

## 27.10 Pièces à réclamer systématiquement pour FIGER une base déclarative

1. Historique e-impôts COMPLET (toutes les pages — les pages manquantes cachent souvent des pénalités) ; 2. Relevés bancaires 12 mois (ventilation 521/571 + créances clients réelles) ; 3. Bulletins de paie / état 301 (trancher la masse salariale) ; 4. Détail de l'agrégat « autres charges » (lever la fourchette de résultat) ; 5. Avis d'imposition TEE N+1 complet (rétro-contrôle du CA vu par la DGI) ; 6. Inventaire physique signé au 31/12 (PV néant si stock 0) ; 7. Déclaration écrite du gérant sur le sort du stock ; 8. Attestation CGA (sécuriser l'abattement 50 %).

---

# 28. ÉLABORATION & LIVRAISON DES ÉTATS FINANCIERS — ENTREPRENANTS (TEE) & MICROENTREPRISES (RME/IME) EN SMT — capitalisé sessions NADRELIE / KG CONSULTING / SAPHIR (juillet 2026)

Complète §12-§17 (production des états) et §27 (base sur pièces). Fixe la **FORME du livrable remis au comptable pour la saisie** et les règles propres aux petites entités SMT en régime TEE ou RME.

## 28.1 Régime & incidence sur les états
- **TEE (Entreprenant, CA ]5M–50M])** : taxe sur le CA — **4 % commerce / 5 % services** — comptabilisée **D 6418 / C 446**, JAMAIS en 891. Pas d'impôt sur le bénéfice → **aucun compte 891**, et le **résultat n'a aucune incidence fiscale directe** (impôt assis sur le CA).
- **RME/IME (CA ]50M–200M])** : **6 % (4 % si CGA/expert-comptable conventionné)** sur le CA — même logique, D 6418/64x / C 446, pas de 891.
- **TCE (0–5M)** : 2 % commerce / 2,5 % autres.
- Conséquence méthodo : sous TEE/RME on peut annuler/étaler un amortissement, ajuster des charges ou traiter un surplus de caisse en prélèvements **sans impact sur l'impôt** → on optimise la PRÉSENTATION (situation nette, trésorerie réaliste), pas l'impôt.

## 28.2 Le journal de saisie = UNIQUEMENT ce que le comptable saisit (01/01 → 31/12)
Règle absolue (décision gérant, juillet 2026) :
1. **PAS d'écritures de clôture / virement au résultat (RES).** Le virement des comptes 6/7 au résultat (13/1031/131) est **généré automatiquement par le logiciel** à la clôture — ne jamais le mettre dans le journal (sinon confusion classique : « je n'ai jamais passé une écriture pareille »). Mémoire : `ecritures-cloture-virement-resultat`.
2. **PAS d'écritures d'à-nouveau (AN) SI le client a déjà sa balance de départ dans son logiciel** (le report à nouveau y est automatique ; ressaisir l'AN doublerait les soldes) → journal = opérations de l'année seulement ; la balance de départ est fournie à part comme état de référence (« déjà dans votre logiciel — ne pas ressaisir »). AN CONSERVÉ seulement pour une **mise en place from scratch** (pas de logiciel préexistant, ex. entité reconstituée depuis une liasse DGI).
3. **PAS de compte technique Sage 890 « Bilan d'ouverture » / 891 « Bilan de clôture »** dans les écritures. Un résidu 890 dans la balance Sage du client = situation nette non affectée → la reprendre **directement dans le bon compte** (capital 101/103, RAN 12x, c/c 462), sans ligne 890 ni écriture de reclassement. (Ne pas confondre avec le 89/891 SYSCOHADA « impôts sur le résultat », inutilisé en TEE.)
4. On GARDE les vraies écritures d'inventaire à saisir : **AMO** (dotations D 6813/C 2841), **INV** (variation stocks 6031/311), **prélèvements** (D 104/103 / C 571), **paie** (661/422/447/643x).
5. Aucun habillage « CLÔTURE » : sections neutres et datées (VENTES, ACHATS, CHARGES, PAIE, FISCAL, DOTATIONS), du 01/01 au 31/12.

## 28.3 Personne physique / EI (cas dominant TEE)
- Résultat au **1031** (jamais 130/131). Bénéfice créditeur, perte débitrice.
- Capitaux propres : **101/102** capital, **103** capital personnel / résultat exploitant, **104** compte de l'exploitant (apports/retraits). Pas de réserve légale ni d'AGO.
- Ouverture N+1 : résultat N (1031) **viré au capital personnel 103** directement.
- **Caisse trop élevée** (l'exploitant a pris l'argent) → deux traitements, sans impact fiscal TEE, à présenter au gérant :
  - **Prélèvements** `D 104 (ou 103) / C 571` — orthodoxe EI, le résultat reste inchangé (recommandé) ;
  - **Charges au réel** — augmenter les charges effectivement engagées, réduit le résultat (peut créer une perte). À n'utiliser que si ce sont de vraies charges. (Cas KG : option charges retenue par le gérant → caisse ramenée à 800 100, résultat −2 392 790.)

## 28.4 Ventilation des charges « logiques »
Ne jamais laisser un bloc opaque « autres charges ». Ventiler selon l'activité : électricité **6052** (CIE), eau **6051** (SODECI), télécom & internet **628**, loyer **622**, carburant **6053**, emballages/fournitures **608/605**, entretien **624**, publicité **627**, honoraires/sous-traitance **6324/605**, charges diverses **658**. Montants estimés signalés « estimé » tant que les factures ne sont pas fournies.

## 28.5 Amortissement sous TEE/RME
Incidence fiscale nulle → au choix documenté du gérant : dotation normale (si tableau d'immobilisations fiable), **amortissement intégral** pour solder un bien (D 6813/C 2841 = VNC, plus aucune dotation ensuite), ou suspension faute de tableau cohérent. Toujours réclamer le **tableau des immobilisations**.

## 28.6 Structure du classeur livré (petite entité SMT)
`COMPTABILITE_<CLIENT>_<ANNÉE>.xlsx` : 0-Cadrage · 1-Balance de départ (source, réf.) · 2-Journal (opérations à saisir) · 3-Balance · 4-Compte de résultat SMT · 5-Bilan · 6-À-nouveau N+1 · 7-Justificatifs fiscaux / Anomalies · (8-Paie). PDF paysage à en-tête MDC (logo + filigrane) pour transmission. Toujours : format FCFA, bouclage ΣD=ΣC, Actif=Passif, Résultat CR=Bilan, et livrable final épuré (« juste les écritures, sans plus »).

## 28.7 Précautions techniques d'édition (durement acquises)
- **openpyxl `delete_rows`/`insert_rows` CORROMPT** les feuilles à cellules fusionnées lors d'une intervention au MILIEU (les lignes en dessous perdent leur contenu). → privilégier les **modifications de VALEURS** (zéro risque) ; si suppression au milieu nécessaire : **défusionner tout → delete_rows → refusionner** les lignes pleine largeur, puis re-vérifier ΣD=ΣC ET l'absence de lignes orphelines (ligne à date seule).
- **Boucle « fenêtre Excel périmée écrasée »** : le gérant ouvre les fichiers pour les revoir ; s'il enregistre une fenêtre restée sur une ancienne version, il écrase les corrections faites sur le disque (arrivé à KG). → avant toute édition, **fermer les classeurs `saving no`** (`osascript ... close ... saving no`) ; après édition, rouvrir la version fraîche ; **sauvegarde `.bak-…` systématique** avant modification.

Cas de référence : NADRELIE (COMPTABILITE_NADRELIE_2025 xlsx+pdf), KG CONSULTING & SAPHIR (journaux ramenés aux opérations seules, AN + clôture retirés), juillet 2026.

---

# 29. CESSATION, DISSOLUTION & RADIATION D'UNE ENTITÉ — PROCÉDURE ET CHIFFRAGE (capitalisé — cas KF IMMOBILIER, juillet 2026)

> Fermer une entité en Côte d'Ivoire = **DEUX volets distincts et cumulatifs** : (1) la **cessation FISCALE** auprès de la DGI, et (2) la **dissolution + radiation JURIDIQUE** au greffe du tribunal de commerce (RCCM). La déclaration de cessation fiscale **ne vaut PAS** radiation au registre du commerce — les deux sont obligatoires. Erreur fréquente : oublier le volet juridique (tribunal de commerce). Livrable de référence : `Documents/DOSSIER CLIENTS/KF IMMOBILIER/CESSATION & CREATION SCI-SARL/`.

## 29.1 Check-list de fermeture (ordre impératif)

**Étape 1 — Régularisation préalable (bloquant pour l'ARF)**
Aucune ARF ni radiation propre n'est possible tant que subsistent des arriérés. Régulariser : TEE/impôts échus, **ITS + FDFP** non déclarés (cf. §1, §15, §27), **CNPS** (immatriculation + cotisations si un salarié est déclaré — obligation parallèle souvent oubliée), pénalités éventuelles.

**Étape 2 — Arrêté des comptes**
États financiers du dernier exercice clos **+ états financiers de cessation** arrêtés à la date d'arrêt effectif de l'activité (2 jeux d'états).

**Étape 3 — Cessation FISCALE (DGI)**
Déclaration de cessation d'activité (DFE de cessation) auprès de la recette compétente ; **dégrèvement** des avis (TEE/autres) postérieurs à la date de cessation — ne jamais régler les mois postérieurs ; puis **Attestation de Régularité Fiscale (ARF)** une fois tout apuré.

**Étape 4 — Dissolution + radiation JURIDIQUE (greffe du tribunal de commerce)**
PV d'AGE de dissolution + désignation du liquidateur → annonce légale (dissolution) → dépôt RCCM → rapport du liquidateur → annonce légale (clôture de liquidation) → **certificat de radiation**.

**Étape 5 — Clôture des engagements**
Résiliation du bail + apurement de la dette de loyer ; clôture du compte bancaire ; notification du CGA de rattachement.

## 29.2 Grille de chiffrage — Dissolution & radiation au tribunal de commerce (barème constaté juillet 2026)

**Frais et débours (reversés à l'État / journal d'annonces légales) — à refacturer au client à l'euro près, ce ne sont PAS des honoraires :**

| Poste | Montant (FCFA) |
|---|---|
| Enregistrement du PV d'AGE (dissolution et radiation) | 62 000 |
| RCCM — dissolution et radiation | 70 000 |
| Annonce légale (FRAT MAT) — dissolution et radiation | 30 000 |
| Certificat de radiation | 10 000 |
| Enregistrement du rapport du liquidateur | 31 000 |
| **Sous-total frais et débours radiation** | **203 000** |

**Honoraire MDC (prestation) :** **140 000** (cas KF IMMOBILIER — un partenaire prestataire externe peut coter sa propre prestation à ~250 000 ; le prix client MDC reste fixé par le gérant, ici 140 000).
→ **Total volet radiation = 203 000 + 140 000 = 343 000 FCFA.**

## 29.3 Enregistrement d'un CONTRAT DE BAIL — calcul des droits et timbres (règle réutilisable)

Coût d'enregistrement d'un bail = **droits fixes d'enregistrement 25 000 FCFA + timbres fiscaux**.
**Timbres = 1 000 FCFA × nombre de pages × nombre d'exemplaires.**
Exemple KF (bail 2 pages, 3 exemplaires) : 25 000 + (1 000 × 2 × 3) = **31 000 FCFA**. Ce sont des **débours** (reversés à l'État), pas un honoraire. Le loyer du bail SCI→SARL est fixé séparément (KF : 60 000 FCFA/mois, cohérent avec le loyer déclaré à la TEE).

## 29.4 Trame de la PROPOSITION FINANCIÈRE de cessation (2 blocs)

Toujours **séparer visiblement** dans la cotation :
- **Bloc A — Honoraires MDC** : plan de localisation, états financiers (clôture + cessation), ARF, DFE de cessation, prestation radiation.
- **Bloc B — Frais et débours** (État / annonces légales / timbres) : enregistrement bail, PV d'AGE, RCCM, annonce légale, certificat de radiation, rapport du liquidateur.
- **+ Section distincte « Point des impôts à régulariser »** (à verser à la DGI, hors honoraires) : arriérés + ITS/FDFP + CNPS.
Barème KF appliqué : Bloc A 1 050 000 + Bloc B 234 000 = **TOTAL 1 284 000 FCFA** (hors impôts à régulariser ≈ 343 700 et hors dette de loyer 850 000).

## 29.5 Séquencement quand la fermeture accompagne une création (restructuration)

Créer et immatriculer les nouvelles structures (ex. **SCI patrimoniale + SARL d'exploitation**, cf. précédents FOUSSENI / KONE IBRAHIM) **AVANT** de cesser l'entité fermée, pour transférer sans rupture activité, contrats et bail. Un **contrat de bail SCI→SARL** sécurise l'occupation (risque de requalification / acte anormal de gestion à prévenir — cf. proposition de suivi intégré SCI+SARL, honoraire type 350 000/mois).

Cas de référence : KF IMMOBILIER (M. KONE Ibrahim) — cessation/dissolution + création SCI+SARL, juillet 2026 ; procédure radiation communiquée par le partenaire E. Diarra.

---

# 30. ⭐ MOTEUR DE DÉCLARATIONS FISCALES PÉRIODIQUES e-impôts (EDI/EFI) — compétence comptable & fiscaliste (capitalisé juillet 2026)

> **Compétence permanente du comptable ET du fiscaliste MDC.** Dès que l'utilisateur dit « **fais-moi la déclaration [TVA / ITS / TSE / …] de [mois]** » (ou fournit un plan comptable / balance / grand livre / tableau de bord en demandant les déclarations), **dérouler ce protocole** et livrer le **formulaire rempli ligne par ligne, prêt à saisir sur e-impôts.gouv.ci**. L'objectif : le fiscaliste n'a plus qu'à transmettre les instructions à son équipe.

**Références (à ouvrir) :**
- `reference/FICHE_DECLARATIONS_EIMPOTS_EDI_EFI.md` — **les 62 natures d'impôt champ par champ** (indices, sections, type saisie[S]/calcul[C], taux, obligatoire) + mécanique EDI/EFI.
- `reference/FICHE_SYNOPTIQUE_CALENDRIER_DGI.md` — **échéances (Partie B) + taux/barèmes faisant foi (Partie A)**.
- `Desktop/MON FISCALISTE CI/MODELES_DECLARATIONS_EIMPOTS_CI.xlsx` (66 onglets, 1 par impôt) · reproduction HTML des formulaires · générateurs Python dans le scratchpad de la session d'origine.

## 30.1 Mécanique EDI / EFI (rappel)
La DGI fournit des fichiers Excel à macros pour préparer une déclaration **hors-ligne** → **« Génération du XML »** → injection sur le portail. **EFI** (`efi-declaration.xlsm`) = formulaire **maître** (choisir le code impôt parmi 62, saisir NCC + période, remplir) → XML injecté **étape 2**. **EDI** (10 fichiers `edi-*.xlsm`) = **annexes détaillées** nominatives (salariés État 301, retenues RIBIC/RIBNC, véhicules patente, déductions TVA…) → XML injecté **étape 3** (« Transmission des annexes détaillées par EDI »). NCC au format `1234567A`. Le code impôt du fichier doit être identique à celui de la déclaration en ligne.

## 30.2 Protocole en 7 temps (LA « manière de faire »)
1. **Identifier** : nature(s) d'impôt + période (mois/exercice) + **service gestionnaire** → échéance. Centre des Impôts = **15 du mois suivant** ; DGE/DME = **10** (industrie/pétrole/mines) / **15** (commerce) / **20** (prestataires). Défaut = Centre, 15.
2. **Collecter la donnée** — tout support qui porte la donnée (balance 6 colonnes, grand livre, journal, tableau de bord, export Sage `.xlsx/.csv`). Ne jamais exiger un format ; extraire ce qui est fourni.
3. **Mapper** compte SYSCOHADA → ligne du formulaire (§30.4).
4. **Calculer** les champs [C] avec les **taux/barèmes de `FICHE_SYNOPTIQUE_CALENDRIER_DGI.md` (qui PRIMENT sur les taux par défaut des templates EDI/EFI — périmés notamment sur l'ITS)**.
5. **Produire le bordereau rempli** : `Section §x · indice · libellé · MONTANT` reproduisant l'écran e-impôts + **liste des annexes EDI** à générer + **contrôles de cohérence** (bases qui bouclent avec la compta).
6. **Poser les questions ciblées** dès qu'une donnée manque ou est ambiguë (ne JAMAIS inventer un chiffre — cf. §17 posture ; règle §25 constatation).
7. **Vérifier vs Annexe Fiscale de la période** (mémoire `toujours-verifier-dgi-2026`) et livrer.

## 30.3 Carnet mensuel type (entreprise au réel — RNI ou RSI) — le régime ne change pas la date, il change les acomptes BIC
| Chaque mois | Code | Échéance (centre) | Prépare si… |
|---|---|---|---|
| **TVA** | `TVA` (DGE/CME → `TVA_S`) | 15 M+1 | assujetti (réel de droit) |
| **ITS + CE + CN + FDFP** | `ITS` | 15 M+1 | salariés présents |
| **TSE** (0,1 % CA HT) | `TSE` | 15 M+1 | entreprise au réel |
| **RIBIC / RIBNC** | `RIBIC` / `RIBNC` | 15 M+1 | retenue opérée sur fournisseurs BIC/BNC |
| **AIRSI / prélèv. 2 %** | `AIRSI` / `PPSSI` | 15 M+1 | achats/prestations secteur informel |

Non mensuel : Patente (décl. 15/03 ; paiement 15/03 + 15/07) · **acompte BIC 3 tiers** 15/04-15/06-15/09 (réel non-DGE ; DGE/DME 10 ou 20) · État 301 (30/05 ; 30/06 si CAC) · **régularisation annuelle ITS** (15/02 centre ; 10/15/20 fév. DGE/DME) · DSF BIC/BNC (30/05 ou 30/06) · IRVM (15 du mois suivant la distribution).

## 30.4 Contrat « données → formulaire » par nature (mapping + calcul)

**TVA** (`TVA`) — lit `70x`, `4431/4432`, `4451/4452/4453`, `4449`, `4441`.
- Saisie : 1.1 CA total HT (Σ70x) ; 1.2 exportations ; 1.3 exo légales ; 1.4 exo conventionnelles ; 1.5 autres non taxables ; 1.8 livraisons à soi-même ; 2.1/2.2/2.3 CA taxable par taux (**18 % / 9 % / 21,31 %**) ; 3.1 régul. TVA à reverser ; 5.1 TVA déductible du mois (4451+4452+4453) ; 5.2 crédit reporté M-1 (solde 4449).
- Calcul : **1.9 = 1.1 − (1.2+1.3+1.4+1.5) + 1.8** ; 2.4 = 2.1×18 % ; 2.5 = 2.2×9 % ; 2.6 = 2.3×21,31 % ; **4.1 = 2.4+2.5+2.6+3.1** ; 5.3 = 5.1+5.2 ; **6.1 TVA nette = max(0 ; 4.1−5.3)** ; **6.2 crédit à reporter = max(0 ; 5.3−4.1)**. Annexe EDI : état des déductions (détail factures d'achat) + détails export/exo/non taxables.

**ITS** (`ITS`) — lit `661/662`, `6413/6414/6415`, `447x`. Idéal : liste des salariés (brut, parts/enfants, local/expatrié) ; sinon masse brute + effectif + ventilation local/expat + avantages en nature + revenus non imposables.
- **Barème IS mensuel (par salarié)** : 0 % ≤ 75 000 · 16 % ]75 000–240 000] · 21 % ]240 000–800 000] · 24 % ]800 000–2 400 000] · 28 % ]2 400 000–8 000 000] · 32 % > 8 000 000. **ITS salarié = IB(barème) − RICF** (RICF selon parts : 1,5→5 500 · 2→11 000 · 2,5→16 500 · 3→22 000 · 3,5→27 500 · 4→33 000 · 4,5→38 500 · 5→44 000 F/mois). Salarié ≤ 75 000/mois → ITS = 0.
- **Charges patronales (grille DGI 2025 faisant foi)** : **CE local = 0 % (exonéré)** · CE expatrié **9,2 %** · **CN 1,2 %** (local + expat) · **FDFP : TA 0,4 % + TFPC 1,2 %**. Total patronal **local = 2,8 %**, **expatrié = 12 %**. ⚠️ Ne PAS utiliser les taux du template (CE 11,5 %/CN 1,5 % = périmés).
- Total ITS à payer = Σ IS salariés + CE + CN + TA + TFPC. Annexe : État 301 (annuelle).

**TSE** (`TSE`) — lit `70x`. Base = CA HT du mois − exos (produits pétroliers) − livraisons à soi-même ; **taxe = base × 0,1 %**.

**Retenues fournisseurs** — annexe EDI nominative (nom, NCC, activité, montant facture, nature, date) :
- `RIBIC` : 7,5 % / 1,5 % / 2,5 % / 5 % / 10 % / 7 % selon la nature (Art. 56 et s.).
- `RIBNC` : **7,5 %** des sommes brutes (Art. 92).
- `AIRSI` : **5 %** (0,2 % / 1,5 % / 2 % pour produits de grande consommation) ; exonéré si vente à un redevable du réel.
- `PPSSI` (prélèvement 2 % prestataires informels, Art. 84 bis) : **2 %** des sommes versées aux TCE/TEE/RME.

## 30.5 Format du livrable remis (par déclaration)
```
DÉCLARATION [CODE] — [Libellé] — [Contribuable / NCC] — Période [MM/AAAA]
Service : [Centre/DGE/DME]   Échéance : [JJ/MM/AAAA]
────────────────────────────────────────────────
§1 · [Section]
  1.1  [Libellé].................  [MONTANT]  (source : compte 70x)
  ...
  6.1  TVA nette à payer........  [MONTANT]   ← à télépayer
────────────────────────────────────────────────
Annexes EDI à générer : [état des déductions / État 301 / …]
Contrôles : [TVA collectée 4431/4432 = base×taux ✓ ; CA = Σ70x ✓ ; …]
Données manquantes / hypothèses : [questions ciblées]
```
Toujours : montants **FCFA**, distinction [S] saisi / [C] calculé, rappel de l'échéance, et **une question par donnée manquante** plutôt qu'une estimation silencieuse.

## 30.6 Règles absolues
1. **Taux & barèmes** : `FICHE_SYNOPTIQUE_CALENDRIER_DGI.md` prime sur les templates ; revérifier vs **Annexe Fiscale de la période**.
2. **Jamais inventer NI INFÉRER une donnée absente ou non confirmée** → laisser le champ **vide avec placeholder `[À FOURNIR]`** et poser une **question ciblée** ; ne JAMAIS le remplir d'une valeur devinée/déduite, **même signalée « à confirmer »**. Ne transcrire QUE ce qui figure **explicitement dans les pièces**. Pièges capitalisés (cas **TIM 7 MULTISERVICE**, restauration RSI, juillet 2026 — feedback gérant « n'invente aucune donnée ») : **(a)** la charge « loyers » du **compte de résultat n'est PAS la valeur locative de la patente** → exiger le **bail** (loyer CR 3 000 000 alors que le loyer réel = **720 000** → DVL, patente et complément condition b) tous faux, à refaire) ; **(b)** ne jamais inférer la **date de début d'activité / dates d'exercice** (depuis le RCCM), le **poste comptable / centre**, l'**adresse**, la **licence** (vente d'alcool ?) — les **demander**. Une seule donnée fausse fait basculer tout le calcul en aval (posture §17, constatation §25, règle §30.6-3 bouclage).
3. **Boucler avec la compta** : chaque base du formulaire doit se retrouver dans les comptes (70x, 44x, 66x…) ; signaler tout écart.
4. **Spécialisation des exercices/mois** : ne déclarer sur le mois M que les opérations de M (piège de millésime §27.1).
5. **Annexes obligatoires** rappelées à chaque fois (ITS→**État 301/ITSREGUL** ; **honoraires & rémunérations versés à des tiers NON-salariés→État 302/BNCREGUL** — dès qu'un prestataire est payé, penser État 302, distinct du PPSSIREGUL qui récapitule les retenues ; TVA→état des déductions + détail exonérations/exports ; retenues (PPSSI/RIBIC/RIBNC/AIRSI/RIRL)→états nominatifs `edi-annexe-retenue` ; patente transport→liste véhicules). Capitalisé GLOBE CÔTE D'IVOIRE 2026 : oubli initial de l'État 302 sur l'honoraire de conseil.
6. Sert **le comptable** (produire) **et le fiscaliste** (contrôler l'exposition, cf. §15, §19, §26).
7. **RÉFLEXE RETENUES À LA SOURCE côté PAYEUR (ne plus jamais oublier)** — pour tout client **au réel (RSI/RNI)**, balayer les **achats/charges de prestations** et déclencher la retenue due AVANT de livrer compta ou déclarations :
   - **PPSSI 2 %** (Art. 84 bis) — prestations de services payées à un fournisseur du **secteur informel (TEE / microentreprise / TCE)**. Code e-impôts **`PPSSI`** ; état récap. annuel **`PPSSIREGUL`** au 30/04 ; reversement 15 M+1. **Définitive, non imputable** par le prestataire. Écriture : `D 401[frn] / C 4471`.
   - **RIBNC 7,5 %** (Art. 92) — honoraires versés à une **personne exerçant une profession non commerciale AU RÉEL** (avocat, notaire, expert-comptable, consultant PP). Ne PAS confondre avec la PPSSI (prestataire TEE/RME) : SARL au régime TEE → **PPSSI 2 %**, PP libérale au réel → **RIBNC 7,5 %**.
   - **RIBIC** (Art. 56 s.) — loyers commerciaux (retenue sur le bailleur), etc.
   - **AIRSI** — JAMAIS sur un achat de prestations : ne joue que quand le réel **VEND** des biens à l'informel (exclut expressément les prestations de services).
   ⚠️ Le piège classique : comptabiliser l'honoraire en **charge 62x/63x** et **oublier la retenue** → le fournisseur est payé brut, l'État lésé, exposition à l'amende (retenue non opérée + intérêt 1 %/mois). Chaque facture de prestataire doit être passée au filtre « quelle retenue à la source ? ».

8. **ENTREPRISES AU RÉEL (RSI/RNI) — TOUJOURS LE DÉTAIL MOIS PAR MOIS.** Tout travail demandé pour un réel (déclarations, estimation, régularisation, exposition, reconstitution) se présente **période par période, mois par mois** — jamais en agrégat annuel seul : TVA, ITS + CN + FDFP, TSE et retenues à la source sont **mensuelles** (1 ligne = 1 mois). Le total annuel n'apparaît qu'en **récapitulatif APRÈS le détail mensuel**. Seuls l'IMF/BIC et la patente sont annuels. (Feedback gérant — dossier TIM 7, juillet 2026 ; cf. §30.3 carnet mensuel et §1 « 1 ligne = 1 mois ».)

9. **ITS ET FDFP IMBRIQUÉS — UNE SEULE DÉCLARATION.** Sur la fiche e-impôts, la déclaration **ITS ENGLOBE le FDFP (TA + TFPC) et la CN** depuis l'ord. n° 2023-719 : un seul montant, une seule déclaration mensuelle (code `ITS`). Ne JAMAIS présenter le FDFP comme une déclaration/ligne distincte, ni le compter « non déclaré » quand l'ITS est déposé — le FDFP y est inclus (le montant ITS déclaré contient les deux). (Feedback gérant — dossiers TIM 7 / LBTECH, juillet 2026.)

10. **INVENTAIRE DÉCLARATIF — DISTINGUER DÉCLARATION ET PAIEMENT (2 étapes).** Chaque case d'une grille/inventaire porte les DEUX statuts : (a) la déclaration est-elle DÉPOSÉE ? (b) le montant est-il PAYÉ ? Codes : **D+** (déclaré + payé) · **D−** (déclaré, NON payé) · **D\*** (déclaré à zéro/minoré) · **N** (non déclaré) · **TO+ / TO−** (taxé d'office payé/non payé) · **—** (néant) · **~** (à vérifier). Une déclaration déposée mais **non payée** n'est PAS à jour (cas fréquent au TEE : la DTEE annuelle est déposée mais les fractions mensuelles restent impayées ; l'exigible = les paiements manquants). (Feedback gérant — grilles TIM 7/LBTECH/GLOBE, juillet 2026.)

Cas d'amorçage : dossier RESEAU IVOIRIEN DE MAINTENANCE (NCC 2300433S, comptable Fils Séverin BILE) — profil réel (TVA hors DGE + TSE + RIBIC/RIBNC + patente commerce/transport + État 301). Mémoire projet : `service-declarations-mensuelles-eimpots`. Précédent PPSSI oubliée puis régularisée : **GLOBE CÔTE D'IVOIRE SARL** (juillet 2026) — honoraires de conseil TEE 500 000 → PPSSI 2 % = 10 000 (`Documents/DOSSIER CLIENTS/GLOBE COTE D'IVOIRE/COMPTABILITE_2026/`).

---

# 31. ⭐ MISSION-TYPE — RECONSTITUTION MULTI-COMPTES & RÉGULARISATION D'UN CA DISSIMULÉ (capitalisé — cas LERO SARL, juillet 2026)

> Déclenchée quand un client au réel a **plusieurs comptes bancaires**, encaisse **beaucoup d'espèces**, et déclare un CA très inférieur au réel. Cas de référence : **LERO SARL** (négoce de nitrate d'ammonium/explosifs + forage pour carrières, flux tendu sans stock, RSI). Dossier complet : `Documents/DOSSIER CLIENTS/LERO/EXERCICE 2025/` (20 livrables) + versé en **BASE DOCUMENTAIRE LMDC** (`Documents/BASE DOCUMENTAIRE LMDC/`, catalogue MC-BASE-DOC-2026-001).

## 31.1 Le réflexe « le compte fourni n'est pas le bon »
Le client donne souvent un compte **secondaire** (ici BNI, flux minimes). Toujours **chercher les autres comptes** : les gros flux et les achats de marchandises transitent ailleurs (ici 2 comptes BDU-CI, dont un dédié « NITRATES »). Indices d'un compte caché : le CA déclaré ≫ les flux du compte fourni ; des chèques émis sans provision sur ce compte ; des bénéficiaires récurrents (intermédiaires) qu'on ne retrouve pas en face d'un compte d'achat. → **Réclamer les relevés de TOUS les comptes** (pièce n°1).

## 31.2 La preuve du CA dissimulé par les ACHATS (négoce à flux tendu)
Argument imparable, à réutiliser : **achats de marchandises constatés + activité sans stock ⇒ tout a été revendu ⇒ les encaissements sont du CA**, même sans factures de vente. Sur LERO : compte « NITRATES » montrant ~75M d'achats + flux tendu → le CA ne peut PAS être celui déclaré (95M) ; le réel cumulé (3 comptes) = **321M TTC / 272M HT** contre 95M déclarés → **~177M HT dissimulés**. Cette preuve tue les montages d'évitement (cf. §31.5).

## 31.3 Cumul du CA réel sur plusieurs comptes (méthode)
1. Extraire chaque relevé (les BDU-CI sont **texte, séparateur `!`**, totaux imprimés « Total general mouvement » à recouper au franc — parser vérifié).
2. Par compte et par mois, **encaissements clients = versements espèces (APPRO) + remises de chèques + virements reçus**, hors intérêts créditeurs (I.R.C.D) et rejets de chèques.
3. **Cumuler les 3 comptes** ; écarter le double compte (retraits d'un compte re-déposés sur un autre — borner par le total des retraits).
4. Le **cash « APPRO COMPTE »** déposé par les associés = du CA quand il n'est PAS couvert par des retraits (retraits ≪ dépôts ⇒ cash externe = paiements clients). Faire **confirmer par le gérant** le circuit (« les clients paient en espèces, on dépose pour régler les fournisseurs »).

## 31.4 Analyse fiscale des SORTIES (au-delà de la TVA/BIC)
Le fiscaliste tire de l'exposition supplémentaire des DÉBITS :
- **Retraits d'espèces au profit des associés = revenus réputés distribués → IRVM** (Art. 180-183) : **15 %** (droit commun) / **17 %** si bénéficiaires personnes physiques. Écriture `D 465/103 / C 4424`.
- **Virements à des prestataires = base de RIBNC non opérée** (Art. 92, **7,5 %**). Écriture `D 401 / C 4471`.
- ⚠ **Cohérence exclusive** : IRVM sur retraits (= distributions) SUPPOSE que les entrées sont du CA ; si on les traitait en compte courant d'associé, les retraits seraient un remboursement (pas d'IRVM). Les deux lectures s'excluent — trancher avec le traitement des entrées.
- Catégoriser aussi : salaires (virements → recoupe l'ITS), loyer (→ 622 + RIBIC bailleur), frais bancaires (631).

## 31.5 Montages d'évitement à réfuter (et pourquoi)
- **« Déficitaire → seul l'IMF »** : indéfendable si la banque montre des entrées massives.
- **« Versements espèces = compte courant d'associé (462), on ne déclare que les virements de sociétés »** : **indéfendable** — (a) contredit le gérant (les clients paient cash) ; (b) un compte courant disproportionné (ici 198M pour un capital de 1M) appelle la **preuve de l'origine des fonds** ; (c) les **achats de marchandises revendus** prouvent le CA (§31.2). À ne fournir qu'en **Rapport N°2 « à titre d'option, sous la responsabilité du client »**, accompagné d'une **note de décision à faire signer** par le gérant (traçabilité, protège l'Agence). Position recommandée = **le réel**.

## 31.6 Points de droit capitalisés
- **IMF au réel = plancher 8 000 000** (condition b réforme PME : « un réel ne paie pas moins qu'une microentreprise » ; RSI = 200M×4% ; RNI = ×1,2 = 9,6M). Prime sur l'IMF de droit commun 3M. Cf. §20, `FICHE_IMPOTS_BENEFICES.md` §5.
- **TVA — assujetti qui achète sans TVA** : un assujetti (RSI) **facture la TVA sur ses ventes taxables indépendamment de l'amont** ; acheter auprès de non-assujettis/exonérés n'exonère pas de collecter. Preuve pratique de régularité : les **clients ont déduit la TVA et la DGI a accepté** (statut « Acceptée » sur e-impôts « factures déclarées comme fournisseur »). NUANCE : si le PRODUIT lui-même est exonéré (Art. 355), l'aval l'est aussi → facturer serait « TVA facturée à tort » (due mais non déductible par le client). Distinguer exonération **produit** vs **usage** (nitrate engrais exonéré vs nitrate explosif taxable). **Ne jamais présumer** le statut TVA des fournisseurs (de marchandises) sans avoir vu leurs factures → les réclamer : s'ils facturent la TVA, il y a une **TVA déductible** qui réduit l'exposition (chiffrer d'abord SANS déductible = hypothèse maximale prudente, puis réviser).

## 31.7 Levier d'optimisation n°1 du négociant : la TVA amont
Pour un négociant taxé sur des ventes mais achetant sans TVA, **sourcer auprès de fournisseurs assujettis à la TVA** transforme une TVA amont invisible en **TVA déductible** (ici ~36M/an sur ~200M d'achats) → effondre la TVA nette due. Autres leviers (cf. `LEVIERS_OPTIMISATION_FISCALE`) : statut **commissionnaire** (base = commission, pas le prix total, si intermédiation réelle + mandat écrit + compta séparée) ; **régime réel = tout déduire** (marge mince → IMF plancher domine) ; amortissements ; formalisation paie + crédit d'impôt emploi ; régularisation **volontaire** (remise de pénalités).

## 31.8 Jeu de livrables standard de la mission (gabarits en base documentaire)
Bancaire (analyse relevé, **CA réel reconstitué**, catégorisation des sorties) → Compta (reconstitution, journal des dépenses) → Fiscal (synthèse exposition, dette par nature, **point des impôts à payer** dédoublonné, note d'exposition, **notes de redressement** avec écritures sourcées, exposition IRVM/RIBNC) → Déclarations prêtes à saisir → Conseil (**demande de pièces**, **note de synthèse exécutive** en page de garde, leviers d'optimisation, note de décision) → **manuel de procédures**. Chaque `.docx` passe par `publish_livrable_mdc.py` (contrôle bloquant, logo + filigrane).

## 31.9 Alimentation de la BASE DOCUMENTAIRE LMDC
`Documents/BASE DOCUMENTAIRE LMDC/` : 6 domaines (01_ANALYSE_BANCAIRE, 02_COMPTABILITE, 03_FISCAL_EXPOSITION, 04_DECLARATIONS, 05_NOTES_CONSEIL, 06_PROCEDURES) + `07_DOSSIERS_TRAITES/<CLIENT>_<ANNÉE>/` (copie intégrale). **Règle** : à chaque mission, copier le dossier complet dans 07 et verser les modèles réutilisables dans le domaine correspondant, puis mettre à jour le catalogue `00_CATALOGUE_BASE_DOCUMENTAIRE_LMDC.docx`.

## 31.10 Règle ITS — prime de transport exonérée (capitalisé LERO, juillet 2026)
**La prime de transport est exonérée d'ITS jusqu'à 30 000 FCFA/mois par salarié ; le surplus est réintégré dans l'assiette imposable.** L'ITS ne se calcule donc PAS sur le brut mais sur la **base imposable = brut − prime de transport exonérée (plafond 30 000)**. Réflexe : dans toute reconstitution ou déclaration ITS, isoler la prime de transport avant d'appliquer le barème (Art. 115-120) puis la RICF. Ex. LERO : brut 300 000 → base 270 000 → ITS 21 700 (au lieu de 28 000 sur le brut) ; masse 700 000 → base imposable 550 000 → ITS 36 100/mois (au lieu de 52 000). D'autres primes ont aussi des plafonds d'exonération (à vérifier dans `FICHE_SYNOPTIQUE_CALENDRIER_DGI.md` : indemnités de logement, de fonction, etc.).

---

# 32. ⭐ PROCÉDURE STANDARD DE RÉGULARISATION FISCALE (capitalisé — dossier LERO, juillet 2026)

> À dérouler pour tout client au réel (RSI/RNI) en retard de déclarations, **avec ou sans taxations d'office déjà émises**. Document générique : `Documents/BASE DOCUMENTAIRE LMDC/06_PROCEDURES/PROCEDURE_REGULARISATION_FISCALE_MDC.docx` (MC-PROC-REGUL-2026-001). Exemple appliqué : `STRATEGIE_REGULARISATION_TAXATIONS_OFFICE_LERO.docx`.

## 32.1 Le principe fondateur — trier chaque période AVANT d'agir (3 statuts)
- **Période NON encore taxée d'office → DÉCLARATION SPONTANÉE en retard** (voie normale, en libre-service e-impôts) : droits réels + pénalités de retard (légères). Déposer AVANT que l'office ne tombe = bonne foi + évite la **majoration d'office 100 %** (200 % si défaut DFE, art. 27/171 bis LPF). **Seule voie propre en ligne — d'où l'urgence de déclarer vite.**
- **Période taxée d'office mais PAS encore liquidée / mise en ligne** → **réclamation contentieuse** encore pleinement utile pour substituer le réel à l'estimation (compta + vraie déclaration jointes).
- ⚠ **Période taxée d'office ET LIQUIDÉE / mise en ligne = EXIGIBLE** (retour terrain gérant, juillet 2026) → **on ne re-déclare PLUS en ligne** (la période est « fermée » par la TO) et la réclamation, bien que recevable **jusqu'au 31/12 de l'année suivant la mise en recouvrement** (LPF), **ne suspend PAS le recouvrement** (le montant reste dû sauf **sursis de paiement accordé avec garanties**). La régularisation passe alors par le **guichet du Chef de centre (CDI)**, selon le sens de l'écart :
  - Office **surestime** (réel < office — ex. TVA à crédit déductible) → **demande de DÉGRÈVEMENT** (déclaration réelle + justificatifs à l'appui) ; l'administration corrige à la baisse.
  - Office **sous-estime** (réel > office — cas d'un CA dissimulé) → **on ne conteste pas** : **déclaration du COMPLÉMENT** (payer plus, l'administration ne refuse pas) + **transaction** sur les pénalités.
- **Paiement de l'exigible, dans tous les cas** : **moratoire/échéancier** + **remise gracieuse** des pénalités/intérêts ; **sursis** uniquement si réclamation déposée + garanties.

## 32.2 Les 7 étapes
1. **Inventaire déclaratif** (établi via la matrice régime × natures d'impôts **§33**) : tableau nature × période à 3 statuts (déclaré / non déclaré / taxé d'office), depuis l'historique e-impôts + avis reçus.
2. **Reconstitution du réel** (compta + banque) → montant réel par période à opposer à l'office.
3. **Classement** de chaque période (matrice §32.1).
4. **Règles de procédure** : charge de la preuve INVERSÉE sur l'office (au contribuable de prouver l'exagération) ; **délai de réclamation** avant le 31/12 de l'année suivant la mise en recouvrement — **mais la réclamation ne suspend pas le recouvrement d'une TO liquidée** (§32.1), d'où la voie guichet (dégrèvement / transaction) ; **sursis de paiement** à demander expressément (garanties si gros montant) ; majoration 100 %/200 %.
5. **Démarche négociée GLOBALE** (recommandée si plusieurs périodes/impôts) : un dossier unique au Chef du CDI = toutes les vraies déclarations + reconstitution + **prise en compte des déclarations réelles** + **dégrèvement des TO excédentaires (liquidées)** + **établissement des compléments** + **transaction sur les pénalités** + **moratoire** + **remise gracieuse** + **sursis avec garanties**.
6. **Plan séquencé** : (a) déposer d'abord les périodes non taxées (arrête l'hémorragie) ; (b) dossier de régularisation au CDI + sursis ; (c) **dégrèvement** là où l'office surestime une TO **liquidée** (réclamation contentieuse si TO **pas encore liquidée**) ; (d) DSF réelle + IMF ; (e) déclarations mensuelles à l'échéance.
7. **Pérennisation** : installer et respecter le calendrier déclaratif (prolonge le manuel de procédures §26.6/§30).

## 32.3 Livrables
Tableau d'inventaire déclaratif (à 3 statuts : déclaré / non déclaré / taxé d'office — en distinguant TO **liquidée** vs **non liquidée**) · déclarations réelles prêtes à saisir (§30) · **courrier de régularisation au CDI** · **demande de dégrèvement** (TO liquidée surestimée) · **modèle de réclamation contentieuse** (TO non encore liquidée) · demande de transaction / remise gracieuse · échéancier de paiement · note de suivi. Réserve permanente : délais/taux/sursis à confirmer vs Annexe Fiscale en vigueur et instructions du CDI de rattachement.

---

# 33. ⭐ INVENTAIRE DÉCLARATIF FISCAL — MATRICE « RÉGIME D'IMPOSITION × NATURES D'IMPÔTS » (volet fiscal de l'audit)

> Étape systématique du volet fiscal de tout audit (§3 ÉTAPE 2, §14) et point de départ de toute régularisation (§32.2 étape 1). Objectif : établir la liste EXHAUSTIVE des obligations déclaratives d'un client à partir de son régime, puis vérifier période par période ce qui a été déclaré / non déclaré / taxé d'office. Cas de référence : LERO — `POINT_DECLARATIONS_PAR_PERIODE_LERO.xlsx` (MC-INVDECL-FORAGE-2026-014).

## 33.1 Principe : les obligations découlent du RÉGIME + des SITUATIONS
Les déclarations dues ne se devinent pas, elles se DÉDUISENT. Deux déterminants :
- **Le régime d'imposition** fixe les impôts « de régime » (impôt sur CA/bénéfice, TVA, patente, TSE).
- **Les situations de l'entreprise** déclenchent les natures transverses (salariés → ITS ; distributions → IRVM ; prestations payées → retenues à la source ; propriété → foncier).
Ne jamais auditer « au fil de l'eau » : d'abord la carte complète des obligations, ensuite la conformité période par période.

## 33.2 Matrice de référence — RÉGIME → natures d'impôts (Côte d'Ivoire)
Sigles : TCE = Taxe Communale de l'Entreprenant ; TEE = Taxe d'État de l'Entreprenant ; RME = Régime des Microentreprises ; IME = Impôt des Microentreprises ; RSI = Réel Simplifié d'Imposition ; RNI = Réel Normal d'Imposition ; IBIC = Impôt sur les Bénéfices Industriels et Commerciaux ; IMF = Impôt Minimum Forfaitaire ; TSE = Taxe Spéciale d'Équipement ; ITS = Impôt sur les Traitements et Salaires ; CN = Contribution Nationale ; FDFP = Fonds de Développement de la Formation Professionnelle ; IRVM = Impôt sur le Revenu des Valeurs Mobilières ; RIBNC = Retenue à la source sur les Bénéfices Non Commerciaux ; AIRSI = Acompte d'Impôt sur le Revenu du Secteur Informel.

| Régime (seuil CA indicatif*) | Impôt CA / bénéfice | TVA | Patente | TSE | Retenues salaires | Autres natures |
|---|---|---|---|---|---|---|
| **TCE** (micro, CA ≤ 5 M*) | TCE forfaitaire (barème communal) | Non | incluse | Non | ITS+CN+FDFP si salariés | — |
| **TEE** (5–50 M*) | TEE, taux sur CA (libératoire) | Non | incluse | Non | ITS+CN+FDFP si salariés | retenues subies (AIRSI…) |
| **RME** (50–200 M*) | IME 6 % du CA (4 % si CGA), acomptes mensuels + solde annuel | Non (sauf option) | due* | à vérifier* | ITS+CN+FDFP si salariés | DSF allégée |
| **RSI** (200–500 M*) | IBIC/IS (acomptes + solde) OU **IMF si supérieur** (plancher cond. b = 8 M) | **Oui 18 % (mensuelle)** | Oui (annuelle) | **Oui 0,1 % (annuelle)** | ITS+CN+FDFP (mensuel) | IRVM, retenues à la source, foncier, DSF, FNE |
| **RNI** (> 500 M*) | IS/IBIC réel (**IMF ×1,2**) | Oui 18 % (mensuelle) | Oui | Oui 0,1 % | ITS+CN+FDFP (mensuel) | idem RSI + obligations renforcées |

*Seuils, taux et périodicités INDICATIFS — À CONFIRMER vs Annexe Fiscale en vigueur (2026). Le régime peut aussi résulter d'une **OPTION** ou être imposé par la **nature réglementée de l'activité** (ex. négoce d'explosifs → réel) indépendamment du CA.

## 33.3 Natures TRANSVERSES (déclenchées par une situation — surtout aux régimes réels)
- **ITS + CN + FDFP** (mensuel) : dès qu'il y a des salariés. Base ITS = brut − prime de transport exonérée 30 000/mois (§31.10) ; FDFP = TA 0,4 % + TFPC 1,2 %.
- **Retenues à la source à OPÉRER** (client redevable en tant que payeur, déclaration au fil des paiements) : **RIBNC 7,5 %** (prestations BNC / honoraires), **retenue sur loyers**, **PPSSI / prélèvement 2 %** (prestations, fournisseurs non-immatriculés), retenue BIC des non-résidents.
- ⭐ **RÈGLE DES PRÉLÈVEMENTS (AIRSI 5 %, PPSSI 2 %) — TOUT DÉPEND DE QUI OPÈRE LE PRÉLÈVEMENT.** Avant de porter un prélèvement au tableau des impôts du client, se demander **qui prélève** :
  - **CAS A — le CLIENT opère le prélèvement** (il paie un fournisseur non immatriculé, ou vend à des revendeurs) ⇒ **il en est redevable, il doit le reverser** ⇒ **la ligne FIGURE au tableau**. Il n'y échappe que s'il produit une **attestation d'exonération** ; à défaut, il est taxé dessus.
  - **CAS B — un FOURNISSEUR prélève SUR le client** (ex. AIRSI 5 % retenu par le grossiste sur les achats) ⇒ ce n'est **PAS une nature due par le client** ⇒ **la ligne NE FIGURE PAS au tableau**. Elle se mentionne seulement en note, et n'est récupérable en crédit sur l'IBIC/IMF que **sur présentation des justificatifs**.
  - **Ne jamais déduire d'office un prélèvement subi** de l'impôt du client : l'impôt reste affiché brut, le crédit se fait valoir séparément.
  - Cas LERO : **AIRSI = cas B** (ETG a prélevé 5 % sur les achats de nitrate → hors tableau) · **PPSSI 2 % = cas A** (LERO paie des prestataires → il doit l'opérer et le reverser → au tableau). [[reflexe-retenues-source-prestataires]]
- **IRVM/IRC** : distributions de bénéfices, revenus réputés distribués (retraits d'espèces, comptes courants débiteurs d'associés) — 15 % (17 % si personnes physiques).
- **Impôt foncier** : propriété d'immeubles.
- ⭐ **DROITS D'ENREGISTREMENT & TIMBRE — à CHIFFRER, jamais laisser « à vérifier »** :
  - **Apports / sommes déposées par la direction → droit d'apport 1 %.** L'administration requalifie en **apports d'associés** les sommes versées sur les comptes par la direction ; droit de **1 %** sur la base. À chiffrer dès qu'apparaissent un compte courant d'associé, des versements d'espèces d'origine non justifiée, ou une **recapitalisation** (cas des capitaux propres négatifs). ⚠ **Qualification ALTERNATIVE au chiffre d'affaires** : si les dépôts sont du CA (TVA 18 %), ils ne sont pas des apports — **ne jamais cumuler** les deux ; présenter le droit d'apport en *risque alternatif hors total*.
  - **Bail commercial → 2,5 % du loyer annuel, avec DROIT FIXE MINIMUM de 25 000 FCFA.** Le bail doit être **enregistré CHAQUE ANNÉE** (ou selon la périodicité du contrat). **À défaut de bail communiqué, retenir le droit fixe de 25 000 par exercice.** Ex. loyer 70 000/mois → 840 000/an → 2,5 % = 21 000 < 25 000 ⇒ **25 000**.
  - Autres actes : cessions, marchés clients, statuts, procès-verbaux.
- ⭐ **ÉTATS ANNUELS RÉCAPITULATIFS (à VÉRIFIER dans TOUT audit déclaratif)** : **État 301** = déclaration annuelle récapitulative des traitements et salaires (ITS) ; **État 302** = déclaration annuelle des sommes versées à des tiers (honoraires, commissions, courtages, loyers). Distincts des déclarations mensuelles ; leur absence est une anomalie fréquente et sanctionnée.

## 33.4 Méthode — construire l'inventaire déclaratif (7 pas)
1. **Identifier le régime réel** (attestation de régime fiscal / e-impôts / seuil de CA / option / activité). ⚠ Vérifier la cohérence **régime ↔ CA réel** : un franchissement de seuil non déclaré (RME resté en TEE, réel dépassant son plafond) est une anomalie majeure — cœur du cas LERO (TEE→RSI mais CA réel ≫ plafond).
2. **Dériver la liste exhaustive** des natures = impôts de régime (§33.2) + natures transverses (§33.3, **y compris les États 301/302 et les retenues à la source RIBNC/PPSSI/AIRSI**) selon les situations constatées. Ne rien omettre : au réel, l'oubli type porte sur FDFP, TSE, patente, IRVM, RIBNC/PPSSI et les États 301/302.
3. **Fixer périodicité + échéance** de chaque nature (mensuelle / trimestrielle / annuelle).
4. **Construire la matrice nature × période** sur l'exercice audité, à **3 statuts** : déclaré / non déclaré / taxé d'office (source : e-impôts « déclarations » + « montants à payer » + avis d'imposition d'office reçus).
5. **Opposer le RÉEL** (reconstitué : compta, relevés bancaires, paie) à chaque période.
6. **Qualifier et traiter** (renvoi §32.1) : non taxé → déclaration spontanée ; TO ≤ réel → payer la TO ; TO > réel → dégrèvement ; sur TOUTE TO → remise gracieuse de la majoration ; résultat → DSF réelle. **On ne « régularise » pas une TO** (elle est déjà l'impôt de la période).
7. **Livrable** : la « carte des déclarations » (onglet nature × période + récap par action + priorités).

## 33.6 ⭐ LES PALIERS FRANCHIS — quand le CA réel fait sauter plusieurs régimes

**La règle (doctrine gérant, cas collège puis LERO) :** quand la reconstitution révèle un CA réel qui **franchit plusieurs seuils de régime**, l'entreprise ne doit pas seulement l'impôt du régime d'arrivée — elle doit **l'impôt de CHAQUE palier franchi, jusqu'à arriver au réel**. La taxation du CA se reconstruit **par tranche**, jamais d'un bloc au taux final.

**Les seuils et les taux** (à confirmer vs Annexe Fiscale en vigueur) :

| Régime | Seuil de CA | Taux |
|---|---|---|
| **TEE** — Taxe d'État de l'Entreprenant | 5 M → 50 M | **4 % commerce · 5 % services** — si l'entreprise exerce **les deux, on retient le taux le plus élevé (5 %)** |
| **RME** — Régime des Microentreprises | 50 M → 200 M | **6 %** du CA (4 % si adhérent d'un centre de gestion agréé) |
| **RSI** — Réel Simplifié | 200 M → 500 M | régime réel : TVA 18 % + IBIC/IMF |
| **RNI** — Réel Normal | > 500 M | réel, IMF × 1,2 |

**Méthode de chiffrage :**
1. Comparer **CA déclaré** et **CA réel reconstitué** — l'écart révèle les paliers franchis.
2. **Découper le CA réel par tranche** et appliquer à chacune le taux de son régime.
3. Porter le résultat en **bloc B du rapport d'exposition au redressement**.

**Exemple LERO 2025** (CA réel 272 238 292, entreprise à la fois négoce et prestations) :
- tranche TEE 0 → 50 000 000 × **5 %** = 2 500 000
- tranche RME 50 → 200 000 000 (150 000 000) × **6 %** = 9 000 000
- tranche RSI 200 → 272 238 292 : régime réel (TVA + IMF, chiffrés à part)
- ⇒ **impôt des paliers franchis = 11 500 000**

## 33.5 Livrable & réserve
Livrable type : `POINT_DECLARATIONS_PAR_PERIODE_<CLIENT>.xlsx` (onglet « Carte des déclarations » + « Récap par action »). Alimente directement §32 (régularisation) et le rapport d'audit §3. **Réserve permanente** : seuils de régime, taux, périodicités et natures exactes à confirmer vs Annexe Fiscale en vigueur et la situation e-impôts du client. Voir `reference/FICHE_DECLARATIONS_EIMPOTS_EDI_EFI.md` (les 62 natures champ par champ) et [[toujours-verifier-dgi-2026]].

---

# 34. ⭐ CONTRÔLE DE CLÔTURE D'UN DOSSIER — À LANCER APRÈS CHAQUE TRAVAUX (capitalisé — dossier LERO, juillet 2026)

> **Un dossier n'est pas fini quand le dernier fichier est produit. Il est fini quand AUCUN livrable ne contredit les autres.**
> Décision du gérant (24/07/2026) : ce contrôle devient **systématique après chaque travaux**, pas seulement en fin de mission.

## 34.1 Le problème qu'il résout

Une mission produit des dizaines de livrables, diffusés dans plusieurs dossiers (dossier de travail, dossier d'analyse, pack réunion, base documentaire). Chaque correction d'un chiffre doit être répercutée **partout**. En pratique elle ne l'est jamais spontanément : les copies numérotées, les documents anciens dont la source markdown a été perdue, les onglets Excel secondaires continuent de porter l'ancien montant.

**Le risque est direct** : le client ou l'administration ouvre deux documents du même dossier et y lit deux chiffres différents. Tout le travail perd sa crédibilité, y compris la partie juste.

Cas LERO : à la clôture, quatre livrables portaient encore un impôt minimum minoré (6 607 142) corrigé depuis, et l'exposition avait changé cinq fois (128 962 819 → 119 651 114 → 123 770 683 → 135 209 513 → 145 523 033) sans que toutes les copies suivent.

## 34.2 L'outil

```bash
python3 ~/.claude/skills/mdc-expert/scripts/controle_coherence_dossier.py "DOSSIER CLIENT" \
    --perimes  128962819,119651114,6607142 \
    --cles     145523033,106252880,29274358 \
    --maitres  "EXERCICE 2025" \
    --terminaux RAPPORT_,NOTE_DE_CONFORMITE \
    --exempts  CONTROLE,AUDIT_FISCAL
```

Il lit tous les `.docx` et `.xlsx` du dossier (extraction XML directe, aucune dépendance) et exécute **quatre contrôles** :

| # | Contrôle | Ce qu'il cherche | Bloquant |
| --- | --- | --- | --- |
| ① | **Montants périmés** | un chiffre corrigé qui survit quelque part | oui |
| ② | **Propagation** | un chiffre définitif absent des livrables terminaux | informatif |
| ③ | **Fraîcheur** | une copie de diffusion plus ancienne que son maître | oui |
| ④ | **Complétude PDF** | un livrable sans son PDF à côté | informatif |

Il apparie automatiquement les copies numérotées à leur maître (`08b_RAPPORT_X.docx` → `RAPPORT_X.docx`) et neutralise toutes les variantes d'espaces (fine, insécable) qui font échouer une simple recherche de chaîne.

`--exempts` exclut les **rapports de contrôle**, qui citent légitimement les montants corrigés (« porté de X à Y »). Sans cette option, ils remonteraient comme faux positifs.

**Code retour 1** si une anomalie bloquante subsiste : le contrôle peut donc être chaîné avant une remise (`python3 controle_coherence_dossier.py … && envoyer`).

## 34.3 La procédure — six pas après chaque travaux

1. **Lister les montants périmés** de la session : tout chiffre qui a changé, même une fois. Les noter au fur et à mesure, pas de mémoire à la fin.
2. **Lancer le contrôle** avec `--perimes` et `--cles`.
3. **Corriger les fichiers signalés** — par édition de valeur pour les `.xlsx`, par republication depuis la source markdown pour les `.docx`.
4. **Rafraîchir les copies** de diffusion depuis les maîtres (le contrôle ③ donne la liste exacte).
5. **Régénérer les PDF** des fichiers touchés (`xlsx_to_pdf_mdc.py` / `publish_pdf_mdc.py`).
6. **Relancer le contrôle jusqu'au vert**, puis versionner (`git commit` + `push`).

## 34.4 Trois règles de fond, apprises à la dure

**Conserver la source markdown de tout livrable Word.** Un `.docx` publié sans sa source n'est plus corrigeable : il faut le réécrire entièrement. Ranger les `.md` à côté du dossier client, jamais uniquement dans un répertoire temporaire de session.

**Ne jamais neutraliser une incohérence en rabotant une ligne.** Quand deux montants se recoupent, laisser chaque ligne à sa valeur intégrale et ouvrir une ligne dédiée en négatif, commentée. Sinon le lecteur voit réapparaître un chiffre qu'il avait fait corriger. Voir [[jamais-minorer-exposition-fiscale]].

**Le contrôle ne doit jamais alléger le dossier.** S'il fait baisser un total, vérifier deux fois : sur LERO, le contrôle final a fait **monter** l'exposition de 10 313 520 (assiette 2026 assise sur le facturé au lieu du réel, cotisations sociales omises). C'est le sens normal d'un contrôle honnête.

## 34.5 Articulation

Ce contrôle est le **dernier maillon** de la chaîne : §24 (protocole d'audit) → §14 (audit contradictoire) → skill `auditeur-fiscal` (grille C1→C12) → **§34 (cohérence documentaire du dossier)** → remise.

Il ne remplace aucun contrôle de fond : il vérifie que les conclusions du fond sont **effectivement présentes et identiques partout**.

---

# 35. ⭐⭐ LE CHEMIN DE L'AUDIT — SECTION D'ENTRÉE (consolidation juillet 2026)

> **C'est ici qu'on commence toute mission d'audit.** Les sections §3, §12 à §16, §21, §23, §24, §26 et §31 à §34 restent la doctrine de détail ; §35 est le **chemin linéaire** qui les enchaîne. Si les deux divergent, §35 prime.
>
> **Manuel** : `Documents/LIVRABLES AUDIT LMDC/00_MANUELS_PROCEDURES/MANUEL_PROCEDURE_AUDIT_MDC.docx` (MC-MAN-AUDIT-2026-002)
> **Checklist opérationnelle** : `CHECKLIST_AUDIT_MDC.xlsx` — 44 étapes cochables, 3 onglets (checklist · les 5 règles · les 9 points de blocage)

## 35.1 Ce qu'on produit

Le produit fini d'un audit n'est **pas un bilan** : c'est une **note de conformité adossée à une exposition chiffrée**, appuyée sur des références juridiques et sur des pièces.

Trois questions, toujours dans cet ordre : **que fait réellement l'entreprise** (par ses flux, pas ses déclarations) · **qu'a-t-elle déclaré** · **que vaut l'écart**.

## 35.2 Les cinq règles qui rendent un audit clair

Chacune a été établie après une erreur réelle. Elles priment sur toute considération de présentation.

| # | Règle | Ce qu'elle interdit |
| --- | --- | --- |
| **1** | **Toutes les assiettes sur le RÉEL** | chiffrer un exercice sur le CA réel et un autre sur le facturé ou le déclaré — deux méthodes dans un dossier, c'est une de trop (cas LERO 2026 : −10 313 520) |
| **2** | **Jamais de minoration par défaut** | porter une déduction au chiffrage sans justificatif produit. *Test du faisceau : si tous les arbitrages penchent du même côté, c'est un biais* |
| **3** | **Aucune compensation avec la TO** | imputer une taxation d'office liquidée sur l'impôt réel — les deux se **cumulent**, même sur le même mois |
| **4** | **Les qualifications exclusives ne se cumulent jamais** | additionner CA et apport, ou PPSSI 2 % et RIBNC 7,5 % — une position retenue, l'autre entre parenthèses **hors total** |
| **5** | **Aucun livrable ne contredit les autres** | corriger un chiffre sans le propager. Corollaire : **conserver la source markdown de tout Word**, sinon le document devient incorrigible |

## 35.3 Les huit phases

| Phase | Ce qu'on fait | Livrables | ⛔ Bloquant |
| --- | --- | --- | --- |
| **0 · Cadrage** | forme, activité, régime déclaré, périmètre (**plusieurs exercices = UN audit, UNE exposition, UNE notation**) | lettre de mission | régime inconnu |
| **1 · Collecte** | 5 sources ; **le compte fourni n'est jamais le seul** | demande de pièces | relevés incomplets |
| **2 · Le réel** | dépouillement opération par opération, chaîne des soldes, **anti-double compte**, TTC ÷ 1,18 | état des relevés · CA réel · catégorisation des sorties | double compte non écarté par écrit |
| **3 · Le déclaré** | matrice **natures × périodes** déduite du régime, 3 statuts (déclaré / non déclaré / taxé d'office, en distinguant **liquidée**) ; **États 301 et 302** | grille déclarative | une case vide |
| **4 · L'écart** | réel vs déclaré par nature ; **paliers franchis** par tranche ; **redevable** de chaque prélèvement ; deux montants distincts (« ce que le centre réclame » ≠ « ce que le client doit ») | montants par nature · point des impôts · rapport d'exposition | une colonne qui ne se recompose pas |
| **5 · Comptabilité** | journal sur le **CA réel** ; **doctrine du tiers** ; **constatation avant règlement** ; à-nouveaux chaînés ; états financiers **système normal** | journal · base comptable · états financiers | journal ou bilan déséquilibré |
| **6 · Les deux contrôles** | fiscal **C1→C12** (recalcul depuis la donnée brute) et comptable **7 axes**, menés **séparément** ; *un contrôle qui allège doit être vérifié deux fois* | rapport d'audit fiscal · rapport de contrôle | anomalie bloquante ou majeure |
| **7 · Notation** | 7 domaines pondérés, malus par gravité, échelle AAA→D ; **visa seulement à partir de A (≥ 15/20)** | note de conformité | observation non sourcée |
| **8 · Clôture** | **`controle_coherence_dossier.py`** (§34) · PDF complets · **`_SOURCES_MD`** · dossier **À TRANSMETTRE** classé A→F · **bordereau** · **courriel de transmission** (⛔ ne JAMAIS y joindre le rapport d'exposition ni le rapport de contrôle : le premier part **séparément**, le second reste interne ; annoncer la part **exigible**, pas l'exposition consolidée. ⛔ **N'ENGAGER AUCUNE ACTION** : aucun délai imposé, documents opérationnels « prêts à être activés », une seule demande — les disponibilités du client pour la **séance de travail** où le plan sera arrêté. ⛔ **COURRIEL COURT** : une douzaine de lignes, **aucun chiffre dans le corps** — annoncer la fin des travaux, ce qui a été fait en une phrase, remettre le dossier, demander les disponibilités. Le détail est dans les pièces) | audit global · rapport client · plan d'action · bordereau | contrôle au rouge |

**Aucun blocage ne se contourne.** Un dossier livré avec un blocage non levé engage la responsabilité de l'Agence.

## 35.4 Ce qu'on ne fait jamais

**On n'invente aucune donnée** — champ absent = vide + `[À FOURNIR]` + question ciblée ; jamais une valeur devinée, **même signalée « à confirmer »**.
**On ne présume pas le statut fiscal d'un tiers** — régime d'un fournisseur, exonération d'un client : cela se prouve par une pièce.
**On ne livre pas une analyse sans contradiction** — un auditeur seul produit des erreurs, deux qui se contredisent produisent une vérité.
**On ne neutralise pas une incohérence en rabotant une ligne** — chaque ligne garde sa valeur, le retraitement se voit à part.
**On ne remet aucun document qui n'a pas passé le contrôle qualité automatique** — s'il ne passe pas, on ne produit pas le document.

## 35.5 La boîte à outils

| Besoin | Script |
| --- | --- |
| Publier un Word (contrôle bloquant) | `publish_livrable_mdc.py SRC.md DEST.docx "Titre" "Client" "Réf"` |
| Publier un PDF (contrôle bloquant) | `publish_pdf_mdc.py SRC.md DEST.pdf …` |
| Classeur Excel → PDF | `xlsx_to_pdf_mdc.py SRC.xlsx` |
| Word → PDF (Word refuse l'AppleScript) | `docx_to_pdf_mdc.py SRC.docx` · `--lot DOSSIER` |
| Cohérence du dossier (après **chaque** travaux) | `controle_coherence_dossier.py DOSSIER --perimes … --cles … --maitres …` |
| Notation | `notateur-conformite/scripts/noter.py observations.json` |

Skills mobilisés : **`auditeur-fiscal`** (grille C1→C12) · **`auditeur-superieur`** (livrables terminaux) · **`notateur-conformite`** (moteur de note).
