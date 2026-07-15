# PROCÉDURE D'AUDIT GLOBAL — LA MAISON DE LA CONFORMITÉ (MDC)
## Guide méthodologique reproductible

> **Version** : 1.0 — 02 mai 2026
> **Auteur référent** : M. BILE FILS SEVERIN, Gérant MDC
> **Cabinet** : LA MAISON DE LA CONFORMITÉ SARL (RCCM CI-ABJ-03-2025-B13-10831, NCC 2506426B)
> **Ambition** : Permettre à tout opérateur (auditeur, expert-comptable, IA) de reproduire l'audit MDC avec une qualité homogène — du recueil des pièces à la livraison du dossier client.

---

## TABLE DES MATIÈRES

1. [Philosophie de la mission MDC](#1-philosophie-de-la-mission-mdc)
2. [Cadre de référence et compétences requises](#2-cadre-de-référence-et-compétences-requises)
3. [Phase 0 — Onboarding client](#3-phase-0--onboarding-client)
4. [Phase 1 — Collecte des sources](#4-phase-1--collecte-des-sources)
5. [Phase 2 — Extraction technique des données](#5-phase-2--extraction-technique-des-données)
6. [Phase 3 — Audit comptable (Bilan + CR + Notes)](#6-phase-3--audit-comptable-bilan--cr--notes)
7. [Phase 4 — Audit bancaire (Triangles MDLC)](#7-phase-4--audit-bancaire-triangles-mdlc)
8. [Phase 5 — Audit fiscal (e-impots + risques)](#8-phase-5--audit-fiscal-e-impots--risques)
9. [Phase 6 — Détection des anomalies (codification)](#9-phase-6--détection-des-anomalies-codification)
10. [Phase 7 — Reconstitution & scénarios fiscaux](#10-phase-7--reconstitution--scénarios-fiscaux)
11. [Phase 8 — Production des livrables (identité MDC)](#11-phase-8--production-des-livrables-identité-mdc)
12. [Annexes](#12-annexes)

---

## 1. PHILOSOPHIE DE LA MISSION MDC

L'audit MDC repose sur **5 principes fondamentaux** non négociables :

### 1.1 Principe de RIGUEUR DOCUMENTAIRE
- **Aucun chiffre inventé** — toute donnée doit avoir une source identifiable (page de la liasse, ligne du relevé, quittance e-impots).
- Si une donnée n'est pas extractible : mentionner explicitement **"non lu / page X à vérifier"**.
- Toujours indiquer la **référence précise** : nom de fichier + page + ligne (ex : `LIAS3250703533589 p.31 Note 13`).

### 1.2 Principe de CONTRADICTION
- Toute donnée doit être **vérifiée à au moins 2 sources** quand cela est possible :
  - Bilan vs Notes annexes (cohérence verticale)
  - Note 14 vs Note 31 (cohérence multi-tableaux)
  - Liasse vs Relevé bancaire (cohérence inter-documents)
  - Liasse N vs Liasse N-1 (cohérence temporelle)
- Toute incohérence est **documentée** comme une anomalie.

### 1.3 Principe d'OPPOSABILITÉ
- L'auditeur doit toujours se demander : **"Si la DGI me lit, est-ce opposable ?"**
- La hiérarchie de la preuve fiscale ivoirienne : Relevé bancaire (très forte) > Liasse fiscale (forte) > Quittances e-impots (forte) > Notes annexes (moyenne) > Documents internes non datés (faible).

### 1.4 Principe de CHIFFRAGE SYSTÉMATIQUE
- Toute anomalie est **chiffrée** en exposition fiscale potentielle (FCFA).
- Tout risque est traduit en **scénarios** (favorable / médian / haut).
- Le rapport final doit présenter un **passif fiscal de conformité** chiffré et hiérarchisé.

### 1.5 Principe d'ACTIONNABILITÉ
- Tout constat doit déboucher sur une **recommandation actionnable** datée (J+7, J+30, J+60, J+90).
- Les recommandations sont classées : URGENT / PRIORITAIRE / NORMAL / STRATÉGIQUE.
- Le client doit savoir **exactement quoi faire** à la lecture du rapport.

---

## 2. CADRE DE RÉFÉRENCE ET COMPÉTENCES REQUISES

### 2.1 Référentiels techniques mobilisés

| Référentiel | Usage |
|---|---|
| **OHADA / SYSCOHADA Révisé (2017)** | Plan comptable, structure bilan, notes annexes obligatoires, Acte uniforme SOC |
| **AUSCGIE** | Art.34 (AGO), Art.371 (capitaux propres < ½ capital), Art.664 (continuation/dissolution), Art.681 (imputation pertes), Art.142+144 (affectation résultat) |
| **AUPCAP** | Art.25 (cessation des paiements), procédures collectives |
| **CGI Côte d'Ivoire** | Art.18 (déductibilité charges), Art.30-32 (régimes fiscaux), Art.39 (IMF), Art.57+103 (revenus distribués + IRVM 13,5%), Art.115-116 (ITS), Art.355-23 (TVA exonérée enseignement) |
| **LPF Côte d'Ivoire** | Art.16 (reconstitution CA), Art.18 (droit de communication), Art.161 (pénalités), Art.184 (majorations), Art.186 (manœuvres frauduleuses 100%) |
| **Code CNPS Côte d'Ivoire** | Cotisations 16,4% patronales + 6,3% salariales, plafonds, branches |
| **Code Travail Côte d'Ivoire** | DPSMO, contrats, registre du personnel, inspection |
| **Loi 2024-388** | RBE (Registre Bénéficiaires Effectifs) — pénalité 1M FCFA forfaitaire |

### 2.2 Compétences techniques de l'auditeur

L'opérateur doit maîtriser :
1. **Comptabilité OHADA Système Normal** — lecture du bilan SN à 76 pages, identification des notes obligatoires, équilibre Actif=Passif, sens débiteur/créditeur des comptes.
2. **Fiscalité ivoirienne 2024** — régimes RE/RME/RSI/RNI, taxation 6% sur CA pour RME, IRVM, ITS, FDFP, IS, TVA, IMF.
3. **Lecture de relevés bancaires** — soldes, totaux mouvements, codification opérations, rapprochement banque/comptabilité.
4. **Analyse financière** — ratios (VA/CA, EBE/CA, charges personnel/CA, solvabilité), évolution multi-exercices, FdR, BFR.
5. **Détection d'anomalies** — codification systématique, gravité, chiffrage exposition.
6. **Programmation Python** — extraction PDFs (PyPDF2, PyMuPDF), graphiques (matplotlib), tableurs (openpyxl), HTML/CSS pour PDF stylés.
7. **Identité documentaire MDC** — palette navy/or, typographies Playfair/DM Sans, structure rapport.

### 2.3 Outils techniques requis

```bash
# Python packages
pip3 install --user PyPDF2 PyMuPDF pdfplumber pdf2image matplotlib openpyxl

# Outils macOS
sips                    # conversion images
qlmanage                # quick look
mdfind                  # recherche système
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome  # PDF generation

# Tools Claude Code
mcp__Desktop_Commander__write_pdf  # PDF natif
Agent (general-purpose)            # délégation analyse experte
Read / Bash / Edit / Write         # I/O standards
```

---

## 3. PHASE 0 — ONBOARDING CLIENT

### 3.1 Identification minimale du client

Recueillir **dans cet ordre** :
1. **Raison sociale** (ex : COLLEGE SAINT-EXUPERY)
2. **NCC** (terminé par P=Personne Physique ou autre suffixe)
3. **RCCM** (forme : CI-ABJ-XX-AAAA-B-XXXXX)
4. **Forme juridique** (SARL / SA / EI / GIE…)
5. **Activité principale** (avec code NSIC si possible)
6. **Adresse** complète
7. **Effectif** approximatif
8. **Régime fiscal déclaré** (TEE / RME / RSI / RNI)
9. **Banque(s) domiciliée(s)** + numéros de comptes
10. **Cabinet certificateur** des comptes

### 3.2 Création du dossier client

Structure standardisée :
```
/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/<NOM_CLIENT>/
├── Liasses fiscales/
├── RELEVE BANCAIRE/
├── Audit & Révision/
├── RAPPORT AUDIT/      ← LIVRABLES MDC
└── Quittances e-impots/
```

---

## 4. PHASE 1 — COLLECTE DES SOURCES

### 4.1 Documents indispensables (par ordre de priorité)

| Priorité | Document | Source typique | Ce qu'on en tire |
|---|---|---|---|
| **1** | Liasse fiscale N (SN ou SMT) | DGI / e-impots | Bilan, CR, Notes 1-39 |
| **2** | Liasse fiscale N-1 et N-2 | DGI / e-impots | Évolution, comparatif |
| **3** | Historique paiements e-impots | e-impots.gouv.ci | TEE/MICRO/ITS/FDFP/IFON/Pénalités |
| **4** | Relevés bancaires N (12 mois) | Banque | Soldes mensuels, encaissements, décaissements |
| **5** | Relevés bancaires N-1 / N-2 | Banque | Triangle Recettes pluriannuel |
| **6** | Statuts SARL / EI | Notaire / RCCM | Forme, capital, gérance |
| **7** | PV d'AGO | Notaire / interne | Affectation résultats, dividendes |
| **8** | Déclarations CNPS (DISA/DASC) | e-CNPS | Vérification masse sociale |
| **9** | Bulletins de paie | Interne | Audit social |
| **10** | Contrats de travail | Interne | Effectif, masse, vacataires |

### 4.2 Sources secondaires (utiles)

- **CNI gérant**, attestation NCC personnelle, compte courant associé écrit
- **Convention prêt-associé** (CCA)
- **Factures fournisseurs** majeures
- **Inventaire physique caisse** signé
- **RBE déposé CEPICI** (Loi 2024-388)
- **ARF** (Attestation Régularité Fiscale)

---

## 5. PHASE 2 — EXTRACTION TECHNIQUE DES DONNÉES

### 5.1 Cas 1 — Liasses fiscales DGI (PDFs nativement texte)

Les liasses émises par e-impots sont **scannées sur formulaire mais avec texte sélectionnable** dans 90% des cas.

```python
import PyPDF2
with open('liasse_2024.pdf', 'rb') as f:
    r = PyPDF2.PdfReader(f)
    print(f"Pages : {len(r.pages)}")
    for i in range(len(r.pages)):
        text = r.pages[i].extract_text()
        # Pages clés à lire en priorité :
        # p4-5 (FR1/FR2 identité), p7 (Bilan Actif), p8 (Bilan Passif),
        # p9 (Compte de Résultat), p10 (TFT), p13-17 (Notes 3A/3B/3C immo),
        # p21-22 (Note 6/7 stocks/clients), p29 (Note 11 Disponibilités),
        # p31-32 (Notes 13-14 Capital + Réserves), p35-37 (Note 16A/16B Dettes),
        # p38-39 (Notes 17-18 Fournisseurs + Dettes fiscales/sociales),
        # p40 (Note 19 Autres dettes - CCA), p41 (Note 20 Banques),
        # p42-49 (Notes 21-28 produits/charges détaillés),
        # p53 (Note 31 - 5 derniers exercices), p61 (Note 37 IS),
        # p64-68 (Détail charges classes 60-67-68), p73 (SUPPL4 Tableau immo)
```

### 5.2 Cas 2 — Liasses ou relevés scannés (images dans PDF)

Si `extract_text()` retourne du vide : utiliser PyMuPDF + lecture vision Claude.

```python
import fitz  # PyMuPDF
doc = fitz.open(path)
for i in range(len(doc)):
    page = doc[i]
    # Test rotation : générer avec et sans rotation 180°
    mat = fitz.Matrix(2.5, 2.5)              # version normale
    pix = page.get_pixmap(matrix=mat)
    pix.save(f'page_{i+1:03d}.png')

    mat_rot = fitz.Matrix(2.5, 2.5).prerotate(180)  # version rotée
    pix_rot = page.get_pixmap(matrix=mat_rot)
    pix_rot.save(f'page_{i+1:03d}_R.png')
```

Puis utiliser le **Read tool** pour lire les PNG en mode vision. Tester les 2 orientations pour identifier la bonne.

### 5.3 Cas 3 — Optimisation pour gros PDFs (50+ pages)

Pour limiter le coût de lecture vision :
1. **Mosaïques 1×2** (2 pages verticalement par image) → divise par 2 le nombre de lectures
2. **Mosaïques 2×2** (4 pages) → divise par 4 mais lisibilité réduite
3. **Crops ciblés** (uniquement bas de page = totaux mensuels) → 137 petites images au lieu de 137 pleines pages

```python
from PIL import Image
def make_pair(p1, p2, out_path):
    img1 = Image.open(p1)
    img2 = Image.open(p2)
    w = max(img1.size[0], img2.size[0])
    h_total = img1.size[1] + img2.size[1]
    pair = Image.new('RGB', (w, h_total), 'white')
    pair.paste(img1, (0, 0))
    pair.paste(img2, (0, img1.size[1]))
    pair.save(out_path, optimize=True)
```

### 5.4 Liste exhaustive des données à extraire (Liasse SN)

#### A) Identité (Pages 4-6, FR1/FR2/FR3)
- Désignation, NCC, RCCM, IDU, n° caisse sociale
- Forme juridique (Note 36)
- Régime fiscal (code 03101=TEE, 03102=RME/RNI, etc.)
- Date début/fin exercice, durée
- Banque + numéro compte
- Personne ayant établi les EF
- Personne à contacter
- AG approuvée O/N
- Signataire + qualité + date
- Dirigeants : nom, NCC, nationalité, adresse

#### B) Bilan Actif (Page 7) — Lignes AD à BZ
- AE Logiciels (213) — net
- AJ Terrains (223)
- AK Bâtiments (231) — Brut, Amort, Net
- AM Mat. mobilier (244) — Brut, Amort, Net
- AN Mat. transport (245)
- AQ Avances/acomptes (252)
- AR Titres participation (261)
- AS Autres immo financières (275)
- AZ TOTAL ACTIF IMMOBILISÉ NET
- BG Clients (411) — Brut, Dépréc., Net
- BJ Autres créances (4xx)
- BS Banque (521) + Caisse (571)
- BU TOTAL TRÉSORERIE-ACTIF
- BZ TOTAL GÉNÉRAL ACTIF

#### C) Bilan Passif (Page 8) — Lignes CA à DZ
- CA Capital (101)
- CD Réserves indispensibles (111)
- CF Réserves libres (118)
- CG Report à nouveau (121/129) — signe + ou -
- CH Résultat exercice (13)
- CJ TOTAL CAPITAUX PROPRES
- DA Emprunts financières (16x)
- DC Provisions risques/charges (19x)
- DD TOTAL DETTES FINANCIÈRES
- DJ Fournisseurs (401)
- DK Dettes fiscales/sociales (42-43-44)
- DM Autres dettes (462-467)
- DP TOTAL PASSIF CIRCULANT
- DR Trésorerie passif (562/565)
- DZ TOTAL GÉNÉRAL PASSIF

#### D) Compte de Résultat (Page 9)
- TC Travaux/services vendus (706)
- XB CHIFFRE D'AFFAIRES
- RC Achats matières (60x)
- RG Transports (61x)
- RH Services extérieurs (62-63)
- RI Impôts et taxes (64x)
- XC VALEUR AJOUTÉE
- RK Charges personnel (66x)
- XD EBE
- RL Dotations amort. (681)
- XE RÉSULTAT EXPLOITATION
- XF RÉSULTAT FINANCIER
- XG RAO
- XH RÉSULTAT HAO
- RS Impôts sur résultat
- XI RÉSULTAT NET

#### E) Notes annexes prioritaires
| Note | Page | Contenu critique |
|---|---|---|
| 3A | 13 | Mouvements bruts immobilisations |
| 3C | 15 | Amortissements cumulés + dotations exercice |
| 7 | 22 | Clients : brut, dépréc., échéances |
| 11 | 29 | Disponibilités : Banque + Caisse + intérêts |
| 13 | 31 | **Capital** : nb actions, valeur nominale, actionnariat |
| 14 | 32 | **Réserves légales/libres + RAN** |
| 16A | 35 | **Dettes financières** : emprunts crédits, crédit-bail, provisions retraite |
| 18 | 39 | **Dettes fiscales/sociales** : Personnel, CNPS, État |
| 19 | 40 | **Autres dettes** : CCA + créditeurs divers |
| 20 | 41 | Trésorerie passif (découverts) |
| 21 | 42 | CA détaillé (vente marchandises / services) |
| 22 | 43 | Achats détaillés |
| 24 | 45 | Services extérieurs détaillés |
| 25 | 46 | Impôts/taxes : directs / indirects / **PÉNALITÉS** |
| 27A | 48 | **Charges personnel** : décomposition |
| 27B | 49 | **Effectifs** : permanents/saisonniers, M/F |
| 28 | 50 | Dotations détaillées |
| 31 | 53 | **5 derniers exercices** : CA, RAN, résultat, effectif, masse salariale |
| 34 | 56-57 | Indicateurs financiers consolidés |
| 37 | 61 | Détermination IS |
| SUPPL4 | 73 | **Tableau immobilisations détaillé** par bien |

---

## 6. PHASE 3 — AUDIT COMPTABLE (BILAN + CR + NOTES)

### 6.1 Délégation à un agent comptable spécialisé

Pour chaque axe (ACTIF / PASSIF / CR), lancer un **agent general-purpose** avec un prompt précis. Voir [Annexes — Prompts d'agents](#annexe-a-prompts-dagents-comptables).

### 6.2 Tests de cohérence systématiques

```
T1 : Bilan équilibré ?       Total Actif = Total Passif (à 1 FCFA près)
T2 : Résultat cohérent ?     Résultat Bilan (CH) = Résultat CR (XI)
T3 : Capital cohérent ?      Capital = Nb actions × Valeur nominale
T4 : Réserves cohérentes ?   Note 14 vs Bilan p.8 vs Note 31
T5 : RAN cohérent ?          RAN N = RAN N-1 + Résultat N-1 (avec/sans dividendes)
T6 : Trésorerie cohérente ?  Note 11 = ligne BU bilan
T7 : Dettes cohérentes ?     Note 16A + Note 18 + Note 19 = ligne DD+DK+DM
T8 : Variation Tréso ?       TFT ZH ≈ Tréso fin - Tréso début
T9 : VA cohérente ?          VA = CA - Achats - Variations - Services - Impôts
T10 : EBE cohérent ?         EBE = VA - Charges personnel
```

### 6.3 Indicateurs financiers à calculer

| Ratio | Formule | Norme école privée CI |
|---|---|---|
| Taux VA / CA | VA / CA | ≥ 60% |
| Marge EBE / CA | EBE / CA | ≥ 5% |
| Marge nette / CA | Résultat / CA | ≥ 0% |
| Charges personnel / CA | Charges 66x / CA | ≤ 70% (privé) |
| Solvabilité | CP / Total bilan | ≥ 25% |
| Couverture intérêts | EBE / Frais financiers | ≥ 3 |
| Délai recouvrement clients | (Clients/CA) × 365 | ≤ 45j |
| Dettes financières / CP | DF / CP | ≤ 100% |
| Fonds de Roulement | Ressources stables - Immo | ≥ 0 |
| Couverture passif circulant | (Tréso + Clients) / PC | ≥ 100% |

---

## 7. PHASE 4 — AUDIT BANCAIRE (TRIANGLES MDLC)

### 7.1 Identification du compte audité

Premier réflexe : **vérifier que le compte audité = compte déclaré FR1**.

```
FR1 (liasse) : Banque BICICI - 0077082 000 12
Relevé fourni : BICICI MARCORY - 0077082 000 12  → ✅ MATCH
```

Si discordance → **alerte rouge** (compte caché ou compte hors-bilan).

### 7.2 Extraction des soldes mensuels

Pour chaque PDF de relevé (typiquement mensuel) :
1. **En-tête** : période "JJ.MM.AA / JJ.MM.AA" + numéro compte + titulaire
2. **Solde initial** : "SOLDE CREDITEUR AU JJ.MM.AA"
3. **Mouvements** : lignes "DD/MM" + libellé + débit | crédit
4. **Totaux mensuels** : "TOTAL DES MONTANTS DEBIT" / "CREDIT"
5. **Solde final** : "SOLDE CREDITEUR AU JJ.MM.AA" (fin de mois)

### 7.3 Triangle BANCAIRE MDLC

```
SI (Solde Initial)  +  E (Encaissements totaux)  -  D (Décaissements totaux)  =  SF (Solde Final)
```

Si le triangle ne ferme pas (à 1 FCFA près) → erreur de lecture ou opération non comptabilisée.

### 7.4 Triangle RECETTES MDLC

```
CA déclaré liasse  ≈  E (Encaissements bancaires nets des apports CCA et virements internes)
```

Si écart > 10% → présomption de **sous-déclaration de CA** (Art.16 LPF CI).

### 7.5 Triangle CMV MDLC (entreprises avec stocks)

```
Achats N  +  SI (Stock Initial)  -  SF (Stock Final)  =  CMV (Coût Marchandises Vendues)
```

À comparer au CMV déclaré au CR. Pour une école sans stock : non applicable.

### 7.6 Catégorisation des opérations bancaires

#### ENTRÉES (Crédits)
- `CA - Espèces` : versements espèces (parents qui paient cash)
- `CA - Virement reçu` : scolarité par virement
- `CA - Remise chèque` : chèques scolarité
- `CCA - Apport associé` : virement gérant → société
- `Régularisation` : opérations annulées
- `Crédit divers` : à identifier ligne par ligne

#### SORTIES (Débits)
- `Salaires` : virements VIR O/COLLEGE SAL
- `Fournisseurs` : chèques numérotés
- `Impôts` : virements DGI
- `CCA - Retrait associé` : virement société → gérant ⚠️
- `Frais bancaires` : tenue compte, agios, timbres
- `Cash retiré` : RET ESP GUICHET ⚠️
- `Voyages personnels` : si carte gérant ⚠️

### 7.7 Cohérence Banque ↔ Liasse

```
Solde Banque 31/12/N  +  Caisse 31/12/N  =  Trésorerie Note 11 = Ligne BU Bilan
```

L'écart Solde Banque / Note 11 = **Caisse implicite** (à vérifier par PV inventaire).

---

## 8. PHASE 5 — AUDIT FISCAL (E-IMPOTS + RISQUES)

### 8.1 Lecture historique paiements e-impots

Le PDF e-impots historique liste 311 paiements types. Pour chaque ligne :
- Code (TSE / FDFP / MICRO / IFON / AVIB / AVNC / PENALITE / ITS / TVA)
- Période (mois / trimestre / tiers / année)
- Année fiscale
- Référence paiement (VIR / CHB / ESP / PRL)
- Date paiement
- Montant

### 8.2 Synthèse par exercice

Pour chaque année fiscale (ex 2024) :
```python
charges_eimpots_2024 = {
    "MICRO": somme paiements MICRO 2024,    # = 6% × CA si RME
    "ITS": somme paiements ITS 2024,         # retenue salariés
    "IFON": somme paiements IFON 2024,       # impôt foncier
    "FDFP": somme paiements FDFP 2024,       # 1% × salaires
    "PENALITE": somme paiements pénalités 2024,
    "TOTAL_CHARGES": somme tout
}
```

### 8.3 Reconstitution du régime fiscal effectif

Si paiements MICRO mensuels = 990 000 FCFA × 12 = 11 880 000 → **régime RME** (6% × 198M)
Si paiements AVIB → régime RNI (IS sur résultat)
Si paiements TEE → régime Entreprenant (CA ≤ 5M)

**Vérifier cohérence** : Régime déclaré FR1 (code 03102) vs Régime effectif (paiements). Toute discordance = anomalie F-1.

### 8.4 Calcul de l'IMF (Impôt Minimum Forfaitaire) — Art.39 CGI

Pour les sociétés au RNI : IMF = 0,5% × CA (plancher).
Pour le RME : intégré dans la taxe MICRO (pas d'IMF supplémentaire).

### 8.5 Rapprochement Liasse Note 25 vs paiements e-impots

```
Note 25 (charges 2024) :
  - Impôts directs       25 774 937
  - Impôts indirects        153 800
  - Pénalités fiscales   11 537 401
  TOTAL                  37 466 138

e-impots PÉRIODE 2024 :
  - MICRO   12 870 000
  - ITS      9 255 423
  - IFON     1 618 020
  - FDFP     1 160 475
  - DIVERS   2 262 679
  TOTAL     27 166 597

Note : ITS retenue ≠ charge (compte 4472, pas charge)
       Pénalités souvent constatées en N mais payées en N-1 ou N+1
```

### 8.6 Sous-déclaration CNPS — calcul rapide

```python
masse_nationale = note_27A["rem_nat"]  # ex 150 257 316 en 2024
cnps_due_estimée = masse_nationale × 0.227  # ~22,7% (16,4% patronal + 6,3% salarial)
cnps_dette_bilan = note_18["cnps"]     # ex 175 000 en 2024
ecart_cnps = cnps_due_estimée - cnps_dette_bilan
penalite_25 = ecart_cnps × 0.25
exposition_cnps = ecart_cnps + penalite_25
```

---

## 9. PHASE 6 — DÉTECTION DES ANOMALIES (CODIFICATION)

### 9.1 Système de codification MDLC

| Préfixe | Domaine | Exemples |
|---|---|---|
| **P-x** | Passif bilan (comptable) | P-1 Capital désaligné, P-2 RAN sans AGO, P-3 CCA |
| **A-x** | Actif bilan (comptable) | A-1 Avances immo amorties, A-2 Dépréciation clients |
| **R-x** | Résultat (comptable) | R-1 Pénalités en charges, R-2 EBE négatif, R-3 Charges/CA>100% |
| **T-x** | Trésorerie (comptable) | T-1 Variation suspecte, T-2 Caisse non inventoriée |
| **N-x** | Notes annexes | N-1 AG non tenue, N-2 Notes vides |
| **F-x** | Fiscal (CGI CI) | F-1 Régime incorrect, F-2 Pénalités, F-3 ITS arriéré |
| **S-x** | Social (CNPS / Travail) | S-1 CNPS sous-déclarée, S-2 DPSMO absente |
| **X-x** | Audit croisé inter-disciplinaire | X-1 CR vs Notes incohérent |
| **REG-ANO-xx** | Régularisation proposée | CAISSE-PRELEVEMENT, HB-RESULTAT, CCA-INTERETS |

### 9.2 Niveaux de gravité

- 🔴 **CRITIQUE** : Risque fiscal majeur > 20M FCFA OU violation OHADA bloquante OU continuité d'exploitation menacée
- 🟠 **ÉLEVÉ** : Risque fiscal 5-20M OU non-conformité OHADA significative
- 🟡 **MOYEN** : Risque fiscal 1-5M OU défaut formel
- 🔵 **MINEUR** : < 1M ou cosmétique

### 9.3 Niveaux de certitude

- **CERTAIN** : Risque déclenché par fait avéré (ex : pénalités 11,5M déjà comptabilisées)
- **PROBABLE** : Très forte présomption (ex : sous-déclaration CNPS calculée)
- **OBLIGATOIRE** : Coût forfaitaire si non-respect (ex : RBE 1M)
- **CONDITIONNEL** : Dépend d'éléments externes (ex : continuité d'exploitation)

---

## 10. PHASE 7 — RECONSTITUTION & SCÉNARIOS FISCAUX

### 10.1 Reconstitution du CA via les RELEVÉS BANCAIRES (Art.16 LPF)

```
CA reconstitué =  Crédits bancaires totaux annuels
              -  Apports CCA documentés (convention écrite)
              -  Virements internes (entre comptes du contribuable)
              -  Remboursements de prêts antérieurs
              -  Régularisations (annulations)
              =  CA présumé pour la DGI
```

Si écart > 10% avec CA déclaré → **Risque reconstitution**.

### 10.2 Reconstitution du CA via les EFFECTIFS (méthode par cohérence)

Pour une école :
```
Effectif salariés = 131
Ratio enseignant/élève (norme privée) = 1/15 à 1/20
Effectif élèves estimé = 131 × 10 = ~1 300 élèves (mid-range)
Frais inscription + scolarité moyenne = 500 000 FCFA/an/élève
CA reconstitué = 1 300 × 500 000 = 650 000 000 FCFA
```

Comparer à CA déclaré → **écart à investiguer**.

### 10.3 Test du ratio Charges Personnel / CA

```
Si CP/CA > 100%  →  Modèle économique non viable
                    → Indique soit sous-déclaration CA, soit charges fictives
```

### 10.4 Calcul de l'exposition fiscale globale

| Chef de redressement | Calcul | Base légale |
|---|---|---|
| **Reconstitution CA — RNI rétroactif** | (CA reconstitué - CA déclaré) × régime fiscal | Art.16 LPF + Art.30-32 CGI |
| **IRVM dividendes occultes** | (Retraits sans justif) × 13,5% | Art.57 + 103 CGI |
| **Pénalités IRVM** | Droits × (25% bonne foi + 36% intérêts 36 mois) | Art.161 LPF |
| **Pénalités manœuvres frauduleuses** | Droits × 100% | Art.186 LPF |
| **Rappel CNPS** | Écart cotisations × 1 (capital) | Code CNPS |
| **Majoration CNPS** | Écart × 25% | Décret CNPS Art.39 |
| **Réintégration pénalités fiscales** | Pénalités déjà charges | Art.18 CGI (non déductibles) |
| **Régularisation ITS arriérés** | Solde dette + 5%/mois | Art.184 LPF |
| **RBE pénalité** | 1 000 000 forfait | Loi 2024-388 |

### 10.5 Scénarios standardisés

| Scénario | Hypothèse | Impact attendu |
|---|---|---|
| **FAVORABLE** | Tous les justificatifs produits, CCA documenté, AGO régularisées | Exposition résiduelle 5-15M (formel) |
| **MÉDIAN** | Reconstitution CA modérée + IRVM CCA + CNPS rappel | 100-200M FCFA |
| **HAUT** | Reconstitution CA agressive + bascule RNI rétroactif + Réserves libres requalifiées | 400-700M FCFA |

---

## 11. PHASE 8 — PRODUCTION DES LIVRABLES (IDENTITÉ MDC)

### 11.1 Liste des livrables types MDC

Pour un audit global complet, produire **dans cet ordre** :

| # | Livrable | Format | Délai |
|---|---|---|---|
| 1 | **Dossier_Audit** (5 axes) | XLSX | J+5 |
| 2 | **Rapport_Anomalies** (6 onglets, 22 tests) | XLSX | J+7 |
| 3 | **RECONSTITUTION_COMPTABLE** (7 onglets) | XLSX | J+10 |
| 4 | **ETAT_RAPPROCHEMENT_FISCAL** | XLSX | J+12 |
| 5 | **ANALYSE_RELEVES_BANCAIRES** | XLSX | J+15 |
| 6 | **SYNTHESE_COMPARATIVE_3_EXERCICES** | XLSX | J+18 |
| 7 | **Rapport_Audit_Global_MDC.pdf** (avec graphiques) | PDF stylé MDC | J+21 |
| 8 | **Synthese_Comptable_Multi_Exercices.pdf** | PDF stylé MDC | J+22 |
| 9 | **Analyse_Releve_Bancaire.pdf** (style MABEK) | PDF stylé MDC | J+23 |
| 10 | **Rapport_Postes_Significatifs_10M.pdf** | PDF stylé MDC | J+25 |

### 11.2 Identité visuelle MDC (charte officielle)

Source : `/Users/bilefilsseverin/Desktop/SITE/frontend/src/style.css`

```css
/* PALETTE OFFICIELLE MDC */
--navy: #0F2040;         /* Couleur primaire — sérieux, autorité */
--navy-mid: #1A3260;     /* Variante */
--gold: #C8932A;         /* Or — accent, valeur */
--gold-light: #E8B84B;   /* Or clair — survol */
--gold-pale: #F5E6C8;    /* Or pâle — fond cards */
--ivoire: #FAF7F2;       /* Fond doux */

/* SÉMANTIQUE ALERTES */
--red: #C0392B;          /* Critique */
--orange: #D4820A;       /* Élevé */
--green: #1A7A4A;        /* Conforme */
--gray: #7F8C8D;         /* Neutre */

/* TYPOGRAPHIES */
font-family-titres: 'Playfair Display', Georgia, serif;  /* Élégance, gravité */
font-family-corps:  'DM Sans', Helvetica, Arial, sans-serif;  /* Lisibilité */
```

### 11.3 Structure standard d'un rapport PDF MDC

```
PAGE 1 — COUVERTURE
  - Bandeau or supérieur (8px)
  - Logo MDC + slogan "VOTRE PARTENAIRE EN CONFORMITÉ"
  - Type de document (TYPE LET ESPACÉ)
  - Titre principal (Playfair, or, 24pt)
  - Sous-titre client (Playfair, blanc, 16pt)
  - Encadré métadonnées (référence, période, NCC, RCCM, date, rédacteur)
  - Mention CONFIDENTIEL
  - Bandeau or inférieur

PAGE 2 — SYNTHÈSE EXÉCUTIVE
  - 4 cards d'indicateurs clés (red/orange/blue/green)
  - Encadré "VERDICT GLOBAL"

PAGES 3-N — CORPS
  - Sections numérotées (badge or)
  - Tableaux navy/ivoire avec lignes alternées
  - Cards de poste (background ivoire, border-left or)
  - Alertes 4 niveaux (red/orange/blue/green/gold)
  - Graphiques matplotlib en base64 inline

PAGE FINALE — RECOMMANDATIONS
  - Tableau 4 colonnes : URGENT / COURT TERME / MOYEN TERME / CONTINU
  - Encadré signatures (cabinet + client)
  - Bandeau légal MDC complet
```

### 11.4 Génération technique du PDF

**Méthode 1 — Chrome headless (recommandée pour styles complexes)**

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="rapport.pdf" \
  --no-margins \
  "file:///path/to/rapport.html"
```

**Méthode 2 — `mcp__Desktop_Commander__write_pdf`** (rapide pour markdown + HTML simple)

```python
# Utilise Puppeteer en interne, accepte markdown + HTML/CSS embarqué
write_pdf(
    path="rapport.pdf",
    content="""<style>...</style>
<h1>Titre</h1>
<table>...</table>
<div style="page-break-before: always;"></div>
..."""
)
```

### 11.5 Génération des graphiques (matplotlib)

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Palette MDC
NAVY = "#0F2040"
GOLD = "#C8932A"
RED = "#C0392B"
GREEN = "#1A7A4A"

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

fig, ax = plt.subplots(figsize=(11, 6))
# ... tracé ...
ax.set_title('TITRE', fontsize=14, fontweight='bold', color=NAVY)
plt.savefig('graph.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# Encoder en base64 pour intégration HTML
import base64
with open('graph.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
img_html = f'<img src="data:image/png;base64,{b64}"/>'
```

### 11.6 Catalogue des graphiques MDC standards

| Graphique | Type | Usage |
|---|---|---|
| Évolution des CP 2020-2024 | Lignes multi | Capitaux propres / Réserves / RAN / Résultat |
| Structure CP | Bar horiz. | Décomposition Capital / Réserves |
| Résultat 5 ans | Bar | Détérioration / amélioration |
| Trésorerie | Lignes | Évolution mensuelle/annuelle |
| CCA / Créditeurs divers | Bar groupé | Mouvement suspect 2022 |
| CA déclaré vs CA reconstitué | Bar horiz. | Risque Art.16 LPF |
| Ratio CP/CA | Bar + ligne | Déséquilibre structurel |
| Exposition fiscale | Donut | Répartition risques |
| Variations panoramique | Bar horiz. | Top hausses/baisses |
| Composition charges personnel | Bar empilé | Décomposition note 27A |

### 11.7 Stockage et nomenclature

```
/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/<NOM_CLIENT>/RAPPORT AUDIT/
├── Dossier_Audit_<NOM>_<ANNEE>.xlsx
├── Rapport_Anomalies_<NOM>_<ANNEE>.xlsx
├── RECONSTITUTION_COMPTABLE_<NOM>_<ANNEE>.xlsx
├── ETAT_RAPPROCHEMENT_FISCAL_<NOM>_<ANNEE>.xlsx
├── ANALYSE_RELEVES_BANCAIRES_<NOM>.xlsx
├── SYNTHESE_COMPARATIVE_3_EXERCICES_<NOM>.xlsx
├── Rapport_Audit_Global_MDC_<NOM>.pdf
├── Synthese_Comptable_Multi_Exercices_<NOM>.pdf
├── Analyse_Releve_Bancaire_<NOM>.pdf
└── Rapport_Postes_Significatifs_10M_<NOM>.pdf
```

---

## 12. ANNEXES

### Annexe A — Prompts d'agents comptables

Pour mobiliser un agent expert sur un axe spécifique, utiliser ce squelette :

```
Tu es un EXPERT-COMPTABLE OHADA / SYSCOHADA Révisé spécialisé en Côte d'Ivoire.
Mobilise toutes tes compétences pour cette analyse.

**MISSION** : [décrire l'objectif précis]

**FICHIERS À ANALYSER** :
1. /chemin/liasse_2022.pdf
2. /chemin/liasse_2023.pdf
3. /chemin/liasse_2024.pdf

**MÉTHODE** : Utilise PyPDF2 (extract_text) + PyMuPDF si scan + Read en mode vision.
Pages clés à privilégier : [lister]

**LIVRABLES ATTENDUS** :
1. Tableau comparatif sur 3 exercices
2. Variations N/N-1 et N/N-2
3. Anomalies détectées (codification + gravité + référentiel)
4. Calcul d'exposition fiscale
5. Synthèse expert-comptable

**INTERDICTIONS** :
- Ne pas inventer de chiffres
- Si donnée non extractible : indiquer "non lu / page X à vérifier"
- Toujours référencer la source

**FORMAT** : Markdown structuré avec tableaux. Sous 4000 mots.
```

### Annexe B — Codification anomalies — Catalogue type

```
P-1 : Capital social désaligné avec nb actions × VN
P-2 : RAN sans AGO d'affectation
P-3 : Compte courant associé sans documentation
P-4 : Apparition fournisseurs (compte 401) sans antécédent
P-5 : Réserves libres ratio anormal vs capital
A-1 : Avances acomptes immo amorties à tort
A-2 : Dépréciation clients massive non justifiée
A-3 : Compte 239 mutualisé avec 231 (immo en cours / corporelles)
R-1 : Pénalités fiscales comptabilisées en charges
R-2 : EBE négatif (continuité)
R-3 : Charges personnel/CA > 100%
R-4 : Frais financiers anormalement bas vs dettes financières
T-1 : Variation trésorerie > 30%
T-2 : Caisse non inventoriée (PV manquant)
N-1 : AG d'approbation non tenue
N-2 : Notes annexes vides (Note 4 Filiales, Note 7 Clients)
F-1 : Régime fiscal déclaré incohérent avec paiements e-impots
F-2 : Pénalités fiscales > seuil annuel normal
F-3 : ITS retenue source non reversée
F-4 : IMF non calculé (RNI uniquement)
F-5 : Liasse fiscale tardive
F-6 : RBE non déposé (Loi 2024-388)
S-1 : CNPS sous-déclarée (cotisations < 22% masse)
S-2 : DPSMO Inspection Travail absente
S-3 : Vacataires non couverts CNPS
S-4 : Charges personnel/CA déséquilibre
X-1 : Note 14 vs Note 31 incohérent (RAN)
X-2 : CR vs Notes annexes incohérent (services ext.)
X-3 : Banque vs Liasse incohérent (caisse non documentée)
```

### Annexe C — Calculs types Côte d'Ivoire

```
TAXE MICRO (RME) :
  Base : CA HT mensuel
  Taux : 6%
  Plafond CA annuel : 200 000 000 FCFA

ITS (Impôt Traitements Salaires) :
  Barème progressif Art.115 CGI CI
  - Tranche 1 : 0% jusqu'à 75 000/mois
  - Tranches supérieures jusqu'à 32%
  - Réduction RICF (Charges de Famille)

CNPS PATRONALE :
  PF Prestations Familiales : 5,75%
  AT/MP Accidents Travail : 2% (école)
  RE Retraite : 7,7%
  ACR Couverture Maladie : 1%
  TOTAL ≈ 16,4% du brut

CNPS SALARIALE :
  RE Retraite : 6,3% du brut

FDFP :
  TA (Apprentissage) : 0,40% du brut
  TFPC (Formation) : 0,60% du brut
  TOTAL : 1% du brut (charge patronale)

IRVM (Impôt sur Revenus Valeurs Mobilières) :
  Taux : 13,5% sur dividendes occultes (Art.103 CGI)

IS (Impôt Société RNI) :
  Taux : 25% sur résultat fiscal

TVA :
  Taux normal : 18%
  Enseignement : EXONÉRÉ (Art.355-23 CGI)

PATENTE :
  Selon valeur locative annuelle bâtiments

IFON (Impôt Foncier) :
  10% × valeur locative annuelle bâtiments
```

### Annexe D — Checklist finale livraison

Avant de remettre le dossier au client, vérifier :

```
☐ Tous les chiffres sont sourcés (référence page liasse / ligne relevé)
☐ Tous les tableaux sont équilibrés (totaux vérifiés)
☐ Toutes les anomalies sont codifiées (P-x / A-x / etc.)
☐ Toutes les anomalies sont chiffrées (exposition FCFA)
☐ Toutes les anomalies ont une régularisation proposée (REG-ANO-xx)
☐ Tous les livrables Excel sont nommés selon la nomenclature MDC
☐ Tous les PDF respectent l'identité visuelle MDC (navy/or)
☐ La page de garde de chaque PDF est complète
☐ Les recommandations sont datées (J+7/J+30/J+60/J+90)
☐ Le bloc légal MDC figure en pied de chaque PDF
☐ La signature gérant + validateur figure sur le rapport principal
☐ Le dossier client est complet dans /RAPPORT AUDIT/
☐ Les sources extraites sont archivées (PNG, JSON, etc.)
☐ Un visa MDC est apposé (si certification)
```

### Annexe E — Cas particuliers et adaptations

| Cas | Adaptation |
|---|---|
| Personne Physique (NCC suffix P) | Pas de CCA mais "compte exploitant" (104). Pas de capital, pas d'affectation formelle. Résultat sur 103. |
| Système Minimal Travail (SMT) | Liasse 24 pages au lieu de 76. Notes condensées. |
| Régime TEE (CA ≤ 5M) | Pas de bilan ni CR. Juste déclaration mensuelle 5% du CA. |
| Régime RME (5M-200M) | Liasse SMT recommandée. Taxe 6% × CA. Pas d'IS sur résultat. |
| Régime RSI (200M-500M) | Régime intermédiaire. IS 25% sur résultat. |
| Régime RNI (>500M) | Liasse SN obligatoire. IS + IMF. TVA si non exonéré. |
| Société sans relevés | Demander BICICI (ou banque) historique 12 mois minimum |
| Dossier urgent (<7j) | Prioriser : Liasse N + Note 19 (CCA) + Note 25 (Pénalités) + Note 31 (5 ans) |

### Annexe F — Questions à poser systématiquement au client

```
1. Avez-vous un PV d'AGO d'approbation des comptes des 3 derniers exercices ?
2. Avez-vous une convention écrite signée pour le CCA / Compte courant exploitant ?
3. Quelle est l'origine des "Réserves libres" (Note 14) ?
4. Quels sont les bénéficiaires des "Créditeurs divers" (Note 19) ?
5. Avez-vous un livre de caisse coté/paraphé ?
6. Avez-vous déposé le RBE (Loi 2024-388) ?
7. Avez-vous reçu des notifications de redressement DGI sur les 3 dernières années ?
8. Êtes-vous à jour des cotisations CNPS (vérifier DISA mensuelles) ?
9. Avez-vous des contrats de travail formels pour TOUS les salariés (incl. vacataires) ?
10. Quelle est la nature des "Titres de participation" (Note 4) ?
11. Avez-vous des immobilisations en cours non encore mises en service ?
12. Y a-t-il eu des retraits importants au compte courant en N et N-1 ?
13. Avez-vous un commissaire aux comptes nommé ?
14. Avez-vous une convention de prêt entre le gérant/associé et la société ?
15. Êtes-vous propriétaire ou locataire des bâtiments d'exploitation ?
```

---

## CONCLUSION

Cette procédure méthodologique permet de produire un audit global MDC reproductible et de qualité homogène. Elle peut être suivie :
- **Manuellement** par un auditeur expérimenté en 5-10 jours ouvrés selon la complexité
- **Avec assistance IA** (agents experts spécialisés) en 1-2 jours
- **En mode 100% automatisé** (en cours de développement) pour les cas standards

La **rigueur documentaire**, la **contradiction systématique**, et la **chiffrage des risques** sont les trois piliers de la qualité MDC.

> **« Le diable est dans les détails. La vérité, dans les sources. »** — Devise interne MDC

---

**LA MAISON DE LA CONFORMITÉ SARL**
RCCM CI-ABJ-03-2025-B13-10831 · NCC 2506426B · Capital 1 000 000 FCFA
Cel +225 07 19 31 49 04 · monfiscaliste@outlook.fr
www.lamaisondelaconformitesarl.net

*Votre Partenaire en Conformité*
