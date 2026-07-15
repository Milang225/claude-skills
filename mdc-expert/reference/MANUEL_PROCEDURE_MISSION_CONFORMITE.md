# MANUEL DE PROCÉDURE — MISSION D'AUDIT DE CONFORMITÉ MDC
## De la note méthodologique aux livrables : où arriver, et comment y arriver

**Référence :** MC-PROC-AUDIT-2026-001 — Abidjan, le 17 juin 2026
**Émetteur :** La Maison de la Conformité SARL — Agence de notation en conformité administrative
**Devise :** Franc CFA (XOF) — Droit applicable : ivoirien & OHADA

---

## 0. À quoi sert ce manuel

Tu produis une **note méthodologique** (la promesse au client). Ce manuel répond aux deux questions qui te manquaient : **(1) Où dois-je arriver ?** (l'objectif et le livrable final) et **(2) Que dois-je faire, dans quel ordre, pour y arriver ?** (les étapes et les livrables intermédiaires).

---

## 1. L'OBJECTIF FINAL DE TOUTE MISSION (la destination)

> **Livrer au client une photographie chiffrée et notée de sa conformité sur 5 domaines, assortie d'un plan d'action priorisé qui le sécurise AVANT que l'administration n'intervienne.**

Concrètement, à la fin, le client doit avoir en main :
1. Une **note de conformité A→E** (globale + par domaine).
2. Une **exposition financière chiffrée en FCFA** (ce qu'un contrôle lui coûterait).
3. Un **plan d'action priorisé et chiffré** (quoi régulariser, dans quel ordre, à quel coût).
4. Une **base comptable reconstituée** (balance + compte de résultat) quand la comptabilité était absente ou anormale.

Et MDC doit avoir constitué un **dossier client structuré** + un **visa d'auditeur**.

---

## 2. LA GRILLE DE NOTATION A→E (face client)

| Note | Signification | Exposition / risque |
|---|---|---|
| **A** | Conforme — excellence | Aucun risque significatif |
| **B** | Satisfaisant | Anomalies mineures, régularisation légère |
| **C** | Acceptable / à surveiller | Anomalies majeures, exposition modérée |
| **D** | Critique | Exposition élevée, redressement probable |
| **E** | Défaut | Non-conformité grave, contentieux imminent |

*(Ex. site : entreprise notée C, exposition 8,5 M FCFA, régularisation 2,3 M.)*
**Pondération des 5 domaines** : Comptable 20 % · Fiscal 20 % · CNPS/Social 20 % · Inspection Travail 15 % · Droit du Travail 15 % · (Documentaire 10 %).

---

## 3. LES 4 PHASES → ce que tu FAIS et ce que tu LIVRES

### PHASE 1 — Diagnostic préliminaire
- **Tu fais** : entretien dirigeant, collecte documentaire (statuts, RCCM, NCC, états financiers, déclarations DGI/CNPS, bulletins, contrats), premier tri, repérage des risques apparents.
- **Tu livres** : **L3 — Rapport intermédiaire** (premières alertes + liste des pièces manquantes).

### PHASE 2 — Audit détaillé par domaine
- **Tu fais** : analyse documentaire systématique, vérifications croisées, tests de conformité.
  - *Comptable* : reconstitution de la base + balance + CR (cœur de métier).
  - *Fiscal* : revue des déclarations selon le régime, cohérence CA, FNE, RBE.
  - *CNPS/Travail* : immatriculation, DISA, cotisations, contrats, bulletins.
- **Tu livres** : **L4 Dossier d'audit (5 axes)** + **L5 Reconstitution comptable** + **L6 Matrice d'anomalies**.

### PHASE 3 — Analyse des processus & chiffrage
- **Tu fais** : cartographie des circuits, calcul de l'exposition (sous-déclarations × prescription + pénalités + intérêts), écritures de régularisation.
- **Tu livres** : **L7 Écritures de régularisation** + **L8 Étude fiscale** (exposition chiffrée).

### PHASE 4 — Synthèse, notation & restitution
- **Tu fais** : consolidation, calcul des notes A→E, plan d'action priorisé.
- **Tu livres** : **L9 Rapport d'audit final noté** + **L10 Présentation exécutive** + **L11 Visa**.

---

## 4. LA LISTE DES LIVRABLES STANDARDS (ce que tu dois produire)

| # | Livrable | Contenu | Outil MDC |
|---|---|---|---|
| L1 | **Note méthodologique** | La promesse : 5 domaines, 4 phases, livrables | docgen / modèle SOFT SECURITY |
| L2 | **Proposition financière** | Périmètre + prix forfaitaire + conditions | modèle ST EXUPÉRY |
| L3 | **Rapport intermédiaire** | Premières alertes + pièces manquantes | Word MDC |
| L4 | **Dossier d'audit Excel (5 axes)** | Documentaire, cadrage réglementaire, matrices anomalies, logique financière, passif & plan | `Dossier_Audit_<CLIENT>.xlsx` |
| L5 | **Reconstitution comptable** | Base reconstituée + **balance** + **compte de résultat** | méthode §21 + openpyxl |
| L6 | **Matrice d'anomalies** | Codes P/A/R/T/N/F/S, gravité, base légale, impact | onglet ② Anomalies |
| L7 | **Écritures de régularisation** | REG-01…NN : D/C, base légale, impact résultat/bilan + **explication** | onglet Régularisations |
| L8 | **Étude fiscale** | Passage compta→fiscal, IS/IMF, conformité, **exposition chiffrée FCFA** | `ETUDE_FISCALE_<CLIENT>.xlsx` |
| L9 | **Rapport d'audit final** | Synthèse, **notation A→E**, exposition, plan d'action priorisé | PDF 12 pages MDC |
| L10 | **Présentation exécutive** | Synthèse direction, enjeux, recommandations | slides |
| L11 | **Visa / certification** | Note ≥ A → visa ; sinon rapport de non-conformité | registre_visas |

---

## 5. LE CHEMINEMENT (ordre & dépendances)

```
L1 Note méthodo ─► L2 Proposition financière ─► [SIGNATURE + PAIEMENT]
        │
        ▼
PHASE 1 ─► L3 Rapport intermédiaire (alertes + pièces manquantes)
        │
        ▼
PHASE 2 ─► L4 Dossier 5 axes ─► L5 Reconstitution (balance + CR) ─► L6 Matrice anomalies
        │                                                              │
        ▼                                                              ▼
PHASE 3 ─► L7 Écritures de régularisation ◄──────────────── L8 Étude fiscale (exposition FCFA)
        │
        ▼
PHASE 4 ─► L9 Rapport final NOTÉ (A→E) + plan d'action ─► L10 Présentation ─► L11 Visa
```

---

## 6. CRITÈRES DE « MISSION RÉUSSIE » (savoir qu'on est arrivé)

La mission est aboutie quand :
1. La **base comptable reconstituée boucle** (ΣD = ΣC ; Actif = Passif ; Résultat CR = Bilan).
2. **Chaque anomalie** détectée a une **écriture de régularisation** chiffrée et expliquée.
3. L'**exposition financière** est chiffrée en FCFA, par domaine.
4. Une **note A→E** globale et par domaine est attribuée et motivée.
5. Le **plan d'action** est priorisé (J+7 / J+15 / J+30 / J+45 / J+60), chiffré, avec responsable.
6. Le **dossier client** est archivé et **visé**.

---

## 7. RÈGLES D'OR
- On ne livre jamais une « base propre » par-dessus une liasse qui ne **boucle** pas : la 1ʳᵉ livraison est la liste des anomalies de bouclage.
- Toute anomalie est **sourcée** (article CGI / AUDCIF / AUSCGIE / Code prévoyance).
- Tout est en **FCFA**, droit ivoirien & OHADA.
- Toute écriture de régularisation est **expliquée** (le « pourquoi » avant le « comment »).
- Confidentialité absolue : **secret professionnel**.

---

*M. BILE Fils Séverin — Gérant — La Maison de la Conformité SARL*
