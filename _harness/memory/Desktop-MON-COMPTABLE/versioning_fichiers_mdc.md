---
name: versioning-fichiers-mdc
description: "Convention de nommage des fichiers MDC avec date de travail — évite l'accumulation de doublons"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 489d2c42-e377-49c0-9928-1f3fbf20f979
---

Tout fichier finalisé lors d'une session doit avoir la date de travail en suffixe du nom.

**Format :** `NOM_FICHIER_AAAAMMJJ.xlsx` (date compacte sans tirets)

**Exemple :**
- `MODELE_SAISIE_SOM_MULTI_SERVICE_INTERACTIF_V2_20260619.xlsx`
- `DEPOUILLEMENT_BMS_TRACE_LOGISTICS_2025_2026_20260619.xlsx`

**Règle :** à chaque session de modification d'un fichier existant, renommer avec la nouvelle date (mv, pas cp) → l'ancienne version datée disparaît, une seule version reste.

**Why:** éviter l'accumulation de copies non datées (fichier sans date = version de travail non tracée).

**How to apply:**
1. À la fin de chaque session de travail sur un fichier, `mv NOM.xlsx NOM_AAAAMMJJ.xlsx`
2. Source canonique = `Documents/DOSSIER CLIENTS/`
3. Copier la version datée vers Desktop + VERSION FINALE (pas le nom sans date)
4. Supprimer les copies sans date sur le Desktop après chaque session

**Extension (validée gérant 01/07/2026) — versionnage V1/V2/… des documents de MÉTHODE :**
Les documents ÉVOLUTIFS d'agence (manuels, formulaires, notes de définition — tout ce qui détaille les procédures) suivent un versionnage incrémental, distinct du suffixe date des livrables clients :
- État au 01/07/2026 = **V1 de référence** (sauf AXE I déjà nommé V2). À chaque avancée de mission qui enrichit une méthode, produire une **version améliorée V2, V3…** (`NOM_V2.docx`) SANS écraser la précédente, et consigner le changement dans `Documents/LIVRABLES AUDIT LMDC/00_MANUELS_PROCEDURES/REGISTRE_VERSIONS.txt`.
- **Instruction permanente** : au fil des missions (FABELLASHOP, ALL-IN-ONE/LBTECH, ST EXUPERY…), mettre à jour spontanément les manuels/procédures concernés par ce qu'on apprend, et rafraîchir les copies du bureau (`Desktop/AUDIT 010726/` ou dossier du jour).
