---
name: catalogue-formations-mdc
description: Toutes les formations internes MDC centralisées dans un seul dossier rangé par thème + index unique
metadata: 
  node_type: memory
  type: project
  originSessionId: 0be0e442-5c5e-4112-bc9f-888fda5e835a
  modified: 2026-08-02T17:57:26.110Z
---

**Toutes les formations internes de l'Agence MDC sont centralisées dans `~/Documents/FORMATIONS MDC/`** (décision gérant, 02/08/2026 : « regroupe toutes les formations dans un seul dossier »). Avant, elles étaient éparpillées sur le Bureau (`Desktop/formation fiscale/`, `Desktop/MON FISCALISTE CI/`, etc.) → le gérant ne les « voyait » pas.

Structure (rangée par thème) :
- `00_INDEX_FORMATIONS_MDC.pdf` — index brandé de TOUT le dossier (source `_INDEX_FORMATIONS_MDC.md`, publié via `publish_pdf_mdc.py`). Se met à jour à chaque ajout.
- `FISCALITE_CI/` (20 supports) — curriculum fiscal CI : expert fiscalité/retenues, TVA compte de tiers, IBIC-BA-BNC, études de cas 1/2/3, code investissements, minière, SCI, agricole (coopératives, amortissements), importations, changes UEMOA, crédits d'impôt, plus-values.
- `ETATS_FINANCIERS_ET_MASTERCLASS/` (8) — Cours Bilan SN ligne par ligne, Compte de résultat SN, Due Diligence fiscale, Masterclass statut juridique & obligations.
- `EBNL_SYCEBNL_OBNL/` (11) — Atelier SYCEBNL 8 modules (.md, non encore publiés PDF) + Atelier OBNL.
- `ORGANISATION_COMPTABLE_2026/` — [[formation_organisation_comptable]] (manuel 28p + cahier 9p).
- `COMPTA_ENGAGEMENT_VS_TRESORERIE_2026/` — [[formation_engagement_vs_tresorerie]] (manuel 7p + cahier 4p).

Copies de travail : les **originaux sur le Bureau ont été conservés** (cp, pas mv). Doublons écartés (COURS_EXPERT présent 2×), échantillons de déclarations e-impôts (ITS/TVA/PPSSI…) exclus (ce ne sont pas des formations), parasites `__MACOSX`/`~$`/`.zip_1` ignorés.

**Règle : toute nouvelle formation** se dépose dans le bon sous-dossier de `FORMATIONS MDC/`, puis on met à jour `_INDEX_FORMATIONS_MDC.md` et on republie `00_INDEX_FORMATIONS_MDC.pdf`. Supports encore en `.md` (SYCEBNL, agricole, crédits d'impôt, plus-values) publiables en PDF brandé sur demande.
