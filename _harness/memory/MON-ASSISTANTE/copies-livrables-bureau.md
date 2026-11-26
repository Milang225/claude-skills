---
name: copies-livrables-bureau
description: "Le gérant veut sur son Bureau un dossier de COPIES de tous les livrables générés, tenu à jour"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d072d1a7-0b11-4fdf-86c5-767581c1ebde
  modified: 2026-09-17T21:39:17.418Z
---

Le gérant veut disposer en permanence, sur son **Bureau**, d'un dossier **`00_COPIES DOCUMENTS GENERES`** (le préfixe « 00_ » le fait remonter en tête de liste) rassemblant une **copie** de tous les livrables que nous produisons — sources `.md` + versions PDF/Word/Excel brandées — **rangés par client**. Exclus : pièces fournies par le client (relevés, quittances, liasses, scans, avis, e-impôts), fichiers `OBSOLETE_*`, et la « BASE DOCUMENTAIRE LMDC » (bibliothèque interne qui duplique). Contient un `MANIFEST.md`.

**Why:** il s'était plaint (17/09/2026) de ne pas retrouver, d'un coup d'œil, l'ensemble de ce qu'on a généré depuis le début.

**How to apply:** après toute production de livrables, régénérer/mettre à jour ce dossier avec `python3 ~/.claude/skills/mdc-expert/scripts/build_copies_bureau.py` (ROOTS = `DOSSIER CLIENTS` + `MON JURISTE` ; repère nos productions par préfixes MDC + présence d'une source `.md`). C'est une COPIE : ne jamais déplacer les originaux. État au 17/09/2026 : 811 fichiers, 44 dossiers clients. Voir [[execution-sans-rework]].
