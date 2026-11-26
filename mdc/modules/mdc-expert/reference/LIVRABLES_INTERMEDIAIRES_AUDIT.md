# LIVRABLES INTERMÉDIAIRES D'AUDIT DE CONFORMITÉ LMDC (13, dont AXE I documentaire)
> Capitalisé juin 2026. Modèles brandés : `Documents/LIVRABLES AUDIT LMDC/02_LIVRABLES_INTERMEDIAIRES/`. Générateur : `scripts/generate_livrable_mdc.py` (papier à en-tête obligatoire). FCFA + droit ivoirien/OHADA. Chaque constat sourcé.

## LA COLLECTION (organisée par bloc)
| Bloc | Code | Livrable | Réf | Méthode skill |
|---|---|---|---|---|
| **0 — Documentaire** | LI-0 | AXE I — Audit documentaire (A1-A24 / B1-B68 / C1-C64) | AXE-I | `FICHE_AUDIT_DOCUMENTAIRE_AXE_I.md` + formulaire XLSX |
| **A — Flux & recettes** | LI-1 | Étude du relevé bancaire (apports gérant / virements clients / sorties par prestataire) | MC-ERB | §2 §16 |
| | LI-5 | Reconstitution du chiffre d'affaires réel (banque+caisse vs déclaré) | MC-RCA | §16 |
| | LI-6 | Étude de la trésorerie & rapprochements (triangles MDLC) | MC-TRP | §12 §16 |
| **B — Comptable** | LI-2 | Étude du dernier état financier (bouclage + reconstitution balance) | MC-EEF | §12 §13 §21 |
| | LI-7 | Étude des immobilisations & amortissements | MC-IMO | §12 §15 |
| | LI-8 | Étude des tiers (clients/fournisseurs, lettrage, anciennetés) | MC-TIE | §12 |
| **C — Fiscal** | LI-4 | Analyse des natures d'impôts (compta+banque) | MC-ANI | §15 §16 §20 |
| | LI-3 | Analyse du dernier redressement vs états | MC-ARD | §19 |
| | LI-12 | Historique des paiements d'impôts (3 ans, e-impôts) | MC-HPI | §1 e-impôts §15 |
| **D — Social & Travail** | LI-9 | Étude sociale / CNPS (théorique/déclaré/payé) | MC-SOC | §1 §17 |
| | LI-10 | Étude Inspection du Travail & Droit du travail | MC-TRA | §7 |
| **E — Juridique** | LI-11 | Étude documentaire & conformité juridique (RBE, AUSCGIE) | MC-DOC | §3 §14 |
| **F — Procédures** | LI-13 | Audit des bonnes pratiques & procédures (contrôle interne comptable & fiscal) | MC-BPP | §4 §16 |
| **G — Dirigeants & capital** | LI-14 | Rémunération des dirigeants/associés & gestion des dividendes (ITS/IRVM, réserve légale, CCA, distributions déguisées) | MC-RDD | §15 §20 + AUSCGIE |

## ENCHAÎNEMENT (ordre flexible, logique recommandée)
```
LI-2 (états qui bouclent) ─┐
LI-1 (relevé) ─► LI-5 (CA réel) ─► LI-6 (trésorerie) ─┤
LI-7 (immo) · LI-8 (tiers) ──────────────────────────┤→ croisements
LI-4 (impôts) · LI-3 (redressement) ─────────────────┤
LI-9 (CNPS) · LI-10 (travail) · LI-11 (juridique) ───┘
        │
        ▼
RECONSTITUTION (balance+CR) ► MATRICE ANOMALIES (P/A/R/T/N/F/S) ► NOTATION A→E + RÉGULARISATIONS + PLAN
```

## POINTS-CLÉS DE LI-1 (enrichi)
- **Entrées ventilées par origine** : apports personnels gérant (104/4611, à isoler du CA), virements clients (411/701), remises chèques, espèces.
- **Sorties par prestataire identifié** : bénéficiaire / nature / compte / montant / récurrence + synthèse top-prestataires (NCC ? facture ?).
- Alertes : apports non documentés (requalification), espèces > 250 000 (Art 18 bis), concentration cash (CRF).

## PROPOSITIONS (dossier séparé `PROPOSITIONS LIVRABLES AUDIT LMDC/`, à valider)
| Code | Livrable | Réf | Zone |
|---|---|---|---|
| LI-15 | Passage Résultat comptable -> fiscal & calcul IS/IMF | MC-PCF | détermination de l'impôt réel |
| LI-16 | Audit croisé inter-pôles (matrice de cohérence) | MC-ACI | détection par recoupement |
| LI-17 | Retenues à la source & engagements hors bilan | MC-RHB | exposition oubliée + passifs latents |
| LI-18 | Optimisation & opportunités d'économie | MC-OPT | dimension VALEUR |
| LI-19 | Audit des exonérations (usage & bon usage) | MC-EXO | exonérations non/mal exploitées |
