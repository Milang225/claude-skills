---
name: formation-engagement-vs-tresorerie
description: "Module de formation MDC « Comptabilité d'engagement vs trésorerie » (SYSCOHADA + fiscal CI)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0be0e442-5c5e-4112-bc9f-888fda5e835a
  modified: 2026-08-02T12:38:44.007Z
---

Module de formation interne MDC produit le 02/08/2026 : **Comptabilité d'engagement (Système normal) vs Comptabilité de trésorerie (SMT / recettes-dépenses)**, avec implications fiscales Côte d'Ivoire.

Emplacement : `~/Documents/FORMATIONS MDC/COMPTA_ENGAGEMENT_VS_TRESORERIE_2026/`
- `MANUEL_...MDC_20260802.docx`/`.pdf` (7 p.) + `CAHIER_CAS_...MDC_20260802.docx`/`.pdf` (4 p.)
- `_SOURCES_MD/` : sources Markdown (`MANUEL_...md`, `CAHIER_CAS_...md`).
- **Régénéré via le PIPELINE OFFICIEL MDC** (skill mdc-expert §9.0/§22) : `publish_livrable_mdc.py` (docx) + `publish_pdf_mdc.py` (pdf) → en-tête à logo + filigrane CONFIDENTIEL + identité « Agence de Notation Administrative », contrôle qualité bloquant (zéro Markdown résiduel). Réfs MC-FORM-COMPTA-2026-001 (manuel) / -002 (cahier). L'ancien moteur maison reportlab a été retiré.

Pivot pédagogique ancré au Guide SYSCOHADA (p.34 et p.45) : SN = flux juridique « a » + flux financier « b » (2 temps) ; SMT = **contraction**, recettes-dépenses seulement, mais **reconstitution créances/dettes/stocks/immos à la clôture** (hybride).

⚠️ Seuils SMT cités = AUDCIF art.13 (négoce 60M / artisanat 40M / services 30M). Régimes fiscaux CI (entreprenant ≤50M, micro 50-200M, RSI 200-500M, RNI >500M) = architecture réforme 2021 → **à revérifier sur l'Annexe fiscale de l'exercice** (change chaque année). BNC = base encaissements/décaissements (RIBNC).

Réutilise la convention [[formation_organisation_comptable]] (MANUEL+CAHIER .docx→.pdf + _SOURCES) et le [[docs_version_modifiable]] / [[versioning_fichiers_mdc]].
