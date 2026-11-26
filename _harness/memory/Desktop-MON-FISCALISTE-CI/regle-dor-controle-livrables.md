---
name: regle-dor-controle-livrables
description: "Règle d'or — aucun livrable Word remis sans contrôle qualité automatique bloquant"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c3c001b6-a642-4b04-ae47-9c68316ff5e7
---

**RÈGLE D'OR (décision gérant, juillet 2026) : ne JAMAIS produire un livrable Word qui ne passe pas le contrôle qualité. S'il ne passe pas, on ne produit pas le document.**

Tout Word client MDC passe par le pipeline **`~/.claude/skills/mdc-expert/scripts/publish_livrable_mdc.py`** (générateur soigné `md2docx_mdc.js` en docx-js + contrôle bloquant) :
`NODE_PATH=$(npm root -g) python3 .../publish_livrable_mdc.py SOURCE.md DEST.docx "Titre" "Client" "Réf"`

Le script génère en tampon, vérifie (génération OK, structure, **zéro Markdown résiduel** `**`/`*`/`##`/`](`, tableaux, **logo embarqué**, **rendu QuickLook**) et ne publie QUE si tout passe ; sinon aucun fichier + rapport d'échec → corriger la source et relancer.

**Pourquoi :** le gérant a exigé que la mise en forme soit peaufinée automatiquement et qu'aucun document défectueux ne sorte. **Comment l'appliquer :** capitalisé dans mdc-expert §9.0. Rendu « papier à en-tête cabinet » (logo, navy/or, tableaux, encadrés). Précédent : dossier GLOBE CÔTE D'IVOIRE. Cf. [[client-globe-cote-divoire]].
