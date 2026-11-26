---
name: skill-dossier-audit
description: "Le skill /dossier-audit produit le dossier d'audit de conformité à partir des données de l'Atelier du diagnostic"
metadata:
  node_type: memory
  type: project
  originSessionId: 6bf22ac1-dc88-4525-8adb-c4a3165313cf
  modified: 2026-11-24T21:54:24.122Z
---

Créé le 24/11/2026 : `~/.claude/skills/dossier-audit/` produit les livrables d'un audit de conformité à partir du fichier de l'Atelier du diagnostic, `~/Documents/DOSSIER CLIENTS/<DOSSIER>/DIAGNOSTIC_COMPLET/donnees_tableau_de_bord.json` (ou l'API locale de l'Atelier sur le port 8770). Gabarit : le dossier MABEK du 24/11.

Quatre scripts : `donnees_dossier.py` (fiche des pivots et contrôles de bouclage), `squelettes_audit.py` (les .md pré-remplis des tableaux chiffrés), `controle_coherence_audit.py` (pivots, valeurs concurrentes, termes interdits), `publier_dossier_audit.py` (PDF et Word, refuse une source encore en « À RÉDIGER »).

**Pourquoi :** les chiffres ne doivent jamais être saisis deux fois — c'est ce qui a fait échouer la première remise de MABEK.

**Comment l'appliquer :** lire `reference/CATALOGUE_DES_LIVRABLES.md` pour le plan de chaque document, et `reference/CONTROLES_AVANT_REMISE.md` avant toute remise. Voir [[circuit-de-cadrage]] et [[dossier-mabek-transport-ef-2025]].
