---
name: Catalogue complet des scripts — MON COMPTABLE CI
description: Tous les scripts backend/scripts/, rôle et usage de chacun
type: reference
originSessionId: 170e232b-c107-45c9-ab32-d67b34a0b362
---
# Catalogue des scripts — `/Users/bilefilsseverin/Desktop/MON-COMPTABLE/backend/scripts/`

---

## ⚡ RÈGLE DE WORKFLOW OBLIGATOIRE (tous dossiers clients)

> **Décision client — à appliquer sur les dossiers : SOM, KSM, MABEK, KRA, KF uniquement.**
> BALOU et TIM7 sont exclus de ce workflow.

### 🔑 PREMIÈRE ACTION : identifier le cas du client

| | CAS 1 | CAS 2 |
|---|---|---|
| **Situation** | A des états financiers + un relevé bancaire | N'a PAS de comptabilité mais exerce |
| **Modèle** | MABEK TRANSPORT | SOM MULTI SERVICE |
| **Mission** | Croiser, auditer, détecter les écarts, reconstituer | Créer la DB from scratch depuis les traces disponibles |
| **Point de départ** | Liasse déclarée + relevé bancaire | Quittances DGI + SMIG + loyer + (relevé optionnel) |

---

### CAS 1 — Entreprise avec états financiers + relevé bancaire (modèle MABEK)

```
ÉTAPE 0 — Parser le relevé bancaire + analyser
  → gen-[client]-analyse-releve.js

ÉTAPE 1 — Croiser liasse ↔ relevé
  → gen-[client]-diagnostic-liasse-releve.js

ÉTAPE 2 — Reconstitution si écart (Art. 16 LPF CI)
  → gen-[client]-reconstitution-comptable.js

ÉTAPE 3 — Propositions régularisation (2 scénarios A+B)
  → gen-[client]-propositions-regularisation.js

ÉTAPE 4 — Notation conformité + État Impôts
  → gen-notation-conformite.js + gen-[client]-etat-impots.js

ÉTAPE 5 — PDFs
  → gen-pdf-[client].js
```

---

### CAS 2 — Entreprise sans comptabilité (modèle SOM)

**Variante 2A (données basiques)** : quittances DGI + SMIG + loyer seulement
**Variante 2B (données réelles)** : quittances + relevé bancaire + factures + contrats

```
ÉTAPE 0 — Inventaire des traces disponibles
  → Lister : quittances DGI, SMIG déclaré, bail, relevé bancaire, factures

ÉTAPE 1 — Créer la DB + saisir les écritures mois par mois
  → gen-[client]-compta.js (from scratch)
  → Ordre SYSCOHADA : D 6xx/C 4xx (constatation) puis D 4xx/C 571 (paiements quittances)

ÉTAPE 2 — Clôturer + AN cascade
  → type_ecriture='CLOTURE' obligatoire, vérifier balance D=C avant clôture

ÉTAPE 3 — AVANT TOUT : État Impôts & Taxes
  → gen-[client]-etat-impots.js EN PREMIER

ÉTAPE 4 — Liasse standard
  → journal, balance, bilan, CR, AN

ÉTAPE 5 — État Général + Excel interactif
  → gen-[client]-etat-general.js + gen-[client]-excel.js

ÉTAPE 6 — Audit + Révision (valider la reconstitution)
  → gen-audit-liasse.js + gen-controle-liasse.js

ÉTAPE 7 — PDFs + livraison
  → gen-pdf-[client].js
  → Copie dans Livres Comptables/ : état impôts + état général + Excel
```

> ⚠️ **Règle CAS 2** : ne jamais inventer un chiffre. Si un montant n'est pas documenté, le signaler et demander au client avant de saisir.
> ⚠️ **Règle absolue tous cas** : l'état des impôts se génère EN PREMIER dans tout dossier ayant une DB.

---

### Livrables obligatoires (communs aux 2 cas, dès qu'une DB existe)
| Document | Script | Description |
|----------|--------|-------------|
| **État Impôts & Taxes** | `gen-[client]-etat-impots.js` | Recap TEE/ITS/FDFP : constaté / payé / dû par exercice, KPIs, paiements |
| **État Général** | `gen-[client]-etat-general.js` | Tous comptes classes 1-9, tous exercices, soldes cumulatifs au 31/12 |
| **Excel interactif** | `gen-[client]-excel.js` | Classeur ExcelJS : formules charges→tiers→571, AN cascade, soldes auto |

---

## 🔧 Modules partagés (utilitaires)

| Script | Rôle |
|--------|------|
| `report-style.js` | Charte graphique unifiée de tous les rapports HTML (couleurs, polices, `RS.fmt()`, `RS.header()`) |
| `preflight.js` | Contrôle préalable universel avant tout document. Signature : `preflight.run(db, {table:'ecritures',cpte:'num_compte'}, exId, annee, exN1)` → `{ok, critiques[], avertissements[], resume, bannerHtml}`. Vérifie : balance D=C, 571 mouvementé, TEE/ITS/FDFP taux de règlement, AN cohérents |
| `gen-balance.js` | Balance générique (utilisée en base par certains clients) |
| `get-balance.js` | Utilitaire lecture soldes (helper interne) |
| `gen-journal-synthese.js` | Journal synthèse tous clients / tous exercices — même format que Journal Général, une ligne par compte |
| `gen-flux-tresorerie.js` | Tableau de Flux de Trésorerie SYSCOHADA méthode indirecte |
| `gen-notation-conformite.js` | Rapport de notation / scoring fiscal et comptable (HTML professionnel) |
| `gen-audit-liasse.js` | Agent auditeur — 18 contrôles sur liasse SMT. Usage : `node gen-audit-liasse.js [client] [annee]` |
| `gen-controle-liasse.js` | Agent réviseur — 3 sections (A: conformité SYSCOHADA, B: logique OHADA 10 contrôles, C: revue analytique 7 ratios). Usage : `node gen-controle-liasse.js [client] [annee]` |
| `gen-pdf-syntheses-journal.js` | Convertit les 16 SYNTHESE_JOURNAL_*.html en PDF dans les sous-dossiers clients |
| `gen-pdf-and-reorganise.js` | PDF + réorganisation dossiers (usage ponctuel) |
| `yepado-data.js` | Données client YEPADO (référentiel externe) |

---

## 👤 SOM MULTI SERVICE (PP/EI — 2019-2026)

### Scripts de saisie comptable
| Script | Couvre | Notes |
|--------|--------|-------|
| `gen-som-compta.js` | v1 initiale | Obsolète |
| `gen-som-compta-v2.js` | v2 | Obsolète |
| `gen-som-compta-v3.js` | v3 | Obsolète |
| `gen-som-compta-v4.js` | **2019–2024** | **Version de référence** — exercices complets avec clôtures, AN |
| `gen-som-2025-2026.js` | **2025–2026** | Rattrapage 2025 + exercice en cours 2026 (DGI : ITSREGUL, TODTEE, pénalités) |
| `gen-som-2023-2024-compta.js` | 2023-2024 | Version intermédiaire (remplacée par v4) |
| `gen-som-2023-compta.js` | 2023 | Version ponctuelle |
| `gen-som-2024-compta.js` | 2024 | Version ponctuelle |
| `gen-som-manuel-saisie.js` | Saisie manuelle | Pour corrections manuelles |
| `gen-som-rattrapage.js` | Rattrapage | Corrections historiques |

### Scripts de rapports (tous paramétriques `node script.js [annee]`)
| Script | Document généré | Fichier sortie |
|--------|----------------|---------------|
| `gen-som-journal.js` | Journal Général | `JOURNAL_SOM_MULTI_SERVICE_[annee].html` |
| `gen-som-balance.js` | Balance des comptes | `BALANCE_SOM_MULTI_SERVICE_[annee].html` |
| `gen-som-bilan.js` | Bilan SYSCOHADA (GZ=HZ vérifié) | `BILAN_SOM_MULTI_SERVICE_[annee].html` |
| `gen-som-cr.js` | Compte de Résultat | `COMPTE_RESULTAT_SOM_MULTI_SERVICE_[annee].html` |
| `gen-som-an.js` | Report à Nouveau | `AN_SOM_MULTI_SERVICE_[annee].html` — disponible 2020+ |
| `gen-som-an-2023.js` | AN 2023 (ponctuel) | Version figée |
| `gen-som-2024-balance.js` | Balance 2024 (ponctuel) | Version figée |
| `gen-som-2024-bilan.js` | Bilan 2024 (ponctuel) | Version figée |
| `gen-som-2024-cr.js` | CR 2024 (ponctuel) | Version figée |

### Scripts d'états récapitulatifs
| Script | Document généré | Fichier sortie |
|--------|----------------|---------------|
| `gen-som-etat-impots.js` | État récapitulatif impôts & taxes (TEE/ITS/FDFP, KPIs, paiements, dettes) | `ETAT_IMPOTS_SOM_MULTI_SERVICE.html` → PDF dans `Livres Comptables/` |
| `gen-som-etat-general.js` | État général tous comptes classes 1-9, tous exercices (style identique à gen-som-etat-impots) | `ETAT_GENERAL_SOM_MULTI_SERVICE.html` → PDF A3 dans `Livres Comptables/` |
| `gen-som-excel.js` | Classeur Excel **interactif** ExcelJS — 3 feuilles : ÉTAT GÉNÉRAL (formules en chaîne), RÉSULTATS, GUIDE DE SAISIE | `ETAT_GENERAL_SOM_MULTI_SERVICE.xlsx` dans `Livres Comptables/` |
| `gen-som-simulation.js` | Simulation pédagogique saisie d'un mois (Mai 2026) — cascade charges→tiers→571 — données Jan-Avr réelles DB | `SIMULATION_SAISIE_MAI2026_SOM.xlsx` dans `Livres Comptables/` |
| `gen-som-simulation-2023-bilan2024.js` | **Feuille 1** : Saisie complète 2023 mois par mois (données DB réelles, 12 mois × comptes) — **Feuille 2** : Bilan SYSCOHADA 2024 complet | `SIMULATION_2023_BILAN_2024_SOM.xlsx` dans `Livres Comptables/` |

### Scripts PDF et correction
| Script | Rôle |
|--------|------|
| `gen-pdf-som.js` | Génère les **48 PDFs** SOM (2019-2026) dans `/Documents/DOSSIER CLIENTS/SOM MULTI SERVICE/`. Comprend Bilan, CR, Balance, Journal, AN par année + Flux Trésorerie + Audit & Révision 2022-2025 |
| `fix_som_db.js` | Correction DB : insert TEE 2022 (ESP23010936787, 100 000 FCFA, 2023) + apport gérant compl. 2026 (161 605 FCFA). **Idempotent** — vérifie doublon avant insert |
| `fix-som-2023-2024.js` | Correction ponctuelle 2023-2024 |
| `fill-som-note7.py` | Remplissage Note 7 (Python) |

### Régénération complète SOM (depuis `/backend/`)
```bash
for yr in 2019 2020 2021 2022 2023 2024 2025 2026; do
  node scripts/gen-som-journal.js $yr
  node scripts/gen-som-balance.js $yr
  node scripts/gen-som-bilan.js $yr
  node scripts/gen-som-cr.js $yr
done
for yr in 2020 2021 2022 2023 2024 2025 2026; do
  node scripts/gen-som-an.js $yr   # AN pas pour 2019 (1er exercice)
done
node scripts/gen-pdf-som.js
```

---

## 🏢 KSM SARL (PM/SARL — 2022-2024)

| Script | Rôle |
|--------|------|
| `gen-ksm-compta.js` | Comptabilité complète 2022-2024 (exercice étendu 16 mois 2022-2023 + 2024) |
| `gen-ksm-journal.js` | Journal Général `[annee]` |
| `gen-ksm-balance.js` | Balance `[annee]` |
| `gen-ksm-bilan.js` | Bilan `[annee]` |
| `gen-ksm-cr.js` | Compte de Résultat `[annee]` |
| `gen-ksm-an.js` | Report à Nouveau `[annee]` |
| `gen-pdf-ksm.js` | PDFs KSM SARL |

---

## 🚛 MABEK TRANSPORT (PM/SARL — 2023-2024)

| Script | Rôle |
|--------|------|
| `gen-mabek-compta.js` | Comptabilité complète 2023-2024 (exercice étendu 14 mois) |
| `gen-mabek-journal.js` | Journal Général `[annee]` |
| `gen-mabek-balance.js` | Balance `[annee]` |
| `gen-mabek-bilan.js` | Bilan `[annee]` |
| `gen-mabek-cr.js` | Compte de Résultat `[annee]` |
| `gen-pdf-mabek.js` | PDFs MABEK |
| `gen-audit-revision-mabek.js` | Rapport audit/révision spécifique MABEK |
| `gen-analyse-releve-mabek.js` | Analyse du relevé bancaire SGBCI (1 285 tx, crédit exact 135 265 442) |
| `gen-mabek-diagnostic-liasse-releve.js` | Diagnostic croisé liasse ↔ relevé |
| `gen-mabek-manuel-analyse.js` | Analyse manuelle (ponctuel) |
| `gen-reconstitution-comptable-mabek.js` | Reconstitution comptable depuis relevé |
| `gen-propositions-regularisation-mabek.js` | Propositions de régularisation |
| `gen-mabek-diagnostic-liasse-releve.js` | Rapport comparatif liasse vs relevé |

> **Statut MABEK** : dossier en **PAUSE** (20/04/2026). Relevé parsé (pdfplumber, `/tmp/parse_mabek3.py`), 1 285 tx, crédit exact, débit à réconcilier (~10M d'écart). Prochain : analyser anomalies.

---

## 👨‍👩‍👧 FAMILLE KRA (PM/SARL — 2023-2024)

| Script | Rôle |
|--------|------|
| `gen-famille-kra-compta.js` | Comptabilité complète NCC 2229049M — Commerce/Épicerie — Régime TEE |
| `gen-famille-kra-journal.js` | Journal `[annee]` |
| `gen-famille-kra-balance.js` | Balance `[annee]` |
| `gen-famille-kra-bilan.js` | Bilan `[annee]` |
| `gen-famille-kra-cr.js` | CR `[annee]` |
| `gen-famille-kra-an.js` | AN `[annee]` |
| `gen-pdf-famille-kra.js` | PDFs Famille KRA |

---

## 🏗️ KF IMMOBILIER CI (PM/SARL — 2024-2025)

| Script | Rôle |
|--------|------|
| `gen-kf-immobilier-compta.js` | Comptabilité NCC 2403558F — Travaux BTP/Immobilier — créée 21/08/2024 |
| `gen-kf-immobilier-journal.js` | Journal `[annee]` |
| `gen-kf-immobilier-balance.js` | Balance `[annee]` |
| `gen-kf-immobilier-bilan.js` | Bilan `[annee]` |
| `gen-kf-immobilier-cr.js` | CR `[annee]` |
| `gen-pdf-kf-immobilier.js` | PDFs KF IMMOBILIER |

---

## 👩 BALOU ADÉLAÏDE (PP/EI — 2024)

| Script | Rôle |
|--------|------|
| `gen-balou-compta.js` | Comptabilité PP — Services/Petit commerce — SMT — AN ouverture : caisse 622 860 FCFA |
| `gen-balou-balance.js` | Balance 2024 |
| `gen-balou-bilan.js` | Bilan 2024 |
| `gen-balou-cr.js` | CR 2024 |
| `gen-balou-flux.js` | Flux de trésorerie |
| `gen-pdf-balou.js` | PDFs BALOU |

---

## 🍽️ TIM 7 MULTISERVICE (PP/EI — 2024)

| Script | Rôle |
|--------|------|
| `gen-tim7-compta.js` | Comptabilité PP — Restauration — NCC 2046563Z — Gérante : DIABY EPSE KONE FATOUMATA — AN : caisse 500 000 FCFA |
| `gen-tim7-balance.js` | Balance 2024 |
| `gen-tim7-bilan.js` | Bilan 2024 |
| `gen-tim7-cr.js` | CR 2024 |
| `gen-tim7-flux.js` | Flux de trésorerie |
| `gen-pdf-tim7.js` | PDFs TIM 7 |

---

## 📊 YEPADO (audit externe)

| Script | Rôle |
|--------|------|
| `gen-yepado-audit-conformite.js` | Rapport audit conformité |
| `gen-yepado-plan-action.js` | Plan d'action |
| `gen-yepado-presentation-executive.js` | Présentation exécutive |
| `gen-yepado-rapport-intermediaire.js` | Rapport intermédiaire |
| `yepado-data.js` | Données de référence YEPADO |

---

## ⚙️ Bonnes pratiques techniques

### gen-pdf-[client].js — pattern Puppeteer correct
```javascript
const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});
for (const f of FICHIERS) {
  const page = await browser.newPage();           // ← nouvelle page par fichier (PAS de réutilisation)
  page.setDefaultNavigationTimeout(60000);
  try {
    await page.goto(`file://${src}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.pdf({ path: dest, format: 'A4', printBackground: true,
      margin: { top: '15mm', bottom: '15mm', left: '10mm', right: '10mm' } });
    ok++;
  } catch(e) { err++; } finally { await page.close().catch(()=>{}); }
}
```
> ⚠️ Ne JAMAIS utiliser `networkidle0` (accroche sur fichiers locaux). Toujours `domcontentloaded`.
> ⚠️ Ne JAMAIS réutiliser la même page — les "detached frame" crashent les suivants.

### fix_[client]_db.js — pattern correction idempotente
```javascript
// 1. Vérifier que num_piece NOT NULL est fourni
const np = db.prepare("SELECT MAX(num_piece) AS mx FROM ecritures WHERE exercice_id=?").get(exId).mx;
// 2. Vérifier doublon avant insert
const dup = db.prepare("SELECT COUNT(*) AS n FROM ecritures WHERE exercice_id=? AND libelle LIKE '%REF%'").get(exId);
if (dup.n === 0) {
  ins.run(np+1, 'OD', 'YYYY-MM-DD', 'COMPTE', 'Libellé', 'REFERENCE', debit, credit, exId, 'NORMAL');
}
// 3. Toujours vérifier balance D=C avant ET après
```

### gen-[client]-bilan.js — exercice non clôturé
```javascript
// Intégrer résultat courant (classes 6/7) pour équilibrer GZ=HZ
// NE PAS filtrer type_ecriture!='CLOTURE' — les CLOTURE s'annulent avec NORMAL dans les exercices clos
const chargesEx  = db.prepare("SELECT COALESCE(SUM(debit)-SUM(credit),0) AS net FROM ecritures WHERE exercice_id=? AND num_compte LIKE '6%'").get(exId).net;
const produitsEx = db.prepare("SELECT COALESCE(SUM(credit)-SUM(debit),0) AS net FROM ecritures WHERE exercice_id=? AND num_compte LIKE '7%'").get(exId).net;
const resultatEx = produitsEx - chargesEx;
const ran103 = solde(exId,'103000').net + Math.max(0, -resultatEx);
const cp = cap104 - ran103 + Math.max(0, resultatEx);
```

### Exécution scripts depuis /backend/
```bash
cd /Users/bilefilsseverin/Desktop/MON-COMPTABLE/backend
node scripts/[script].js [args]
# Toujours lancer depuis /backend/ pour que require('better-sqlite3') se résolve
```
