---
name: controles-de-tenue-referentiel
description: "Référentiel MC-REF-CTRL-2026-001 (30/10/2026) — 15 contrôles de tenue tirés de la note de revue KRAMO sur TIM 7, source unique branchée sur classeur, fiches, machine, guide"
metadata:
  node_type: memory
  type: project
  originSessionId: cbb45325-4528-4536-9d4a-ba6f3bec0008
  modified: 2026-10-30T19:59:43.014Z
---

Le 30/10/2026, les leçons de la note de revue de l'expert-comptable KRAMO (refus du visa 2025 de TIM 7, 13/10/2026) sont devenues 15 contrôles de tenue, CT01 à CT15, pour tous les dossiers en suivi. Les trois leçons de tête sont : une ligne de relevé = une écriture à sa date ; à-nouveaux = liasse N-1 visée ; retraits du dirigeant au compte courant (AUSCGIE art. 356).

**Source unique :** `SUPERVISEUR GENERAL/CONTROLES_DE_TENUE/_SOURCES/controles_tenue.py`. On la corrige, puis on relance les scripts qui la lisent :
- `build_suivi_dossiers.py` : onglets « Contrôles de tenue » et « Référentiel des contrôles » ;
- `build_fiches_semaine.py` : une page par dossier ;
- `machine.py` : contrôles mensuels datés dans le « Cycle mensuel », contrôles d'ouverture et annuels dans le plan ; procédure du suivi global republiée ;
- `build_referentiel.py referentiel|guide|passage` : produit le référentiel, le guide collaborateur (édition 2, § 12), et le point par client avec sa grille et les brouillons de demande de pièces.

**Premier passage :** le statut des 22 dossiers est dans `passage_controles_2026-10-30.json`, qui est lu par le dernier fichier `passage_controles_*.json`. Les brouillons sont rangés dans `DOSSIER CLIENTS/<client>/CONTROLES_DE_TENUE/` ; ceux d'ECOMAF sont sous `AVE MARIA TRANSIT/SUIVI_2026-09/2_ECOMAF`. LERO n'a pas de brouillon (fin de contrat le 21/10). Envoi par le Secrétariat le 03/11, après le visa du Superviseur. Pièces attendues pour le 13/11.

**Why :** le gérant veut que ce qui a fait refuser un visa ne se reproduise sur aucun autre dossier.

**How to apply :**
- Pour un nouveau passage, écrire un nouveau `passage_controles_<date>.json`, puis relancer les trois scripts.
- Le suivi des missions (8780, serveur) n'a pas été touché ([[equipe-definit-les-etapes]]).
- « Conforme » exige que la pièce ait été vue. CT04 exige un état signé.

Voir [[superviseur-donne-les-consignes]] et [[aucun-montant-documents-collaborateurs]].
