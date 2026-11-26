---
name: docs-version-modifiable
description: "Pour tout document livré, toujours fournir une version modifiable (Word) où l'utilisateur peut laisser des observations, avant la version finale"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b317e1a9-2048-4ae5-ab82-de71d08bdbe8
---

À chaque fois qu'un document est produit pour l'utilisateur (rapport, mémo, courrier, note, proposition, etc.), fournir **systématiquement une version modifiable** — en pratique un **.docx éditable** (via `~/.claude/skills/mdc-expert/scripts/md_to_docx_mdc.py`) — permettant à l'utilisateur d'**éditer et de laisser ses observations** (suivi des modifications / commentaires Word, ou zone « Observations »). L'utilisateur relit, annote, renvoie ses retours, puis je **réadapte la version finale** (PDF soigné) en intégrant ses corrections.

**Why:** L'utilisateur (gérant LMDC) travaille en boucle de validation : il veut toujours pouvoir amender un livrable avant sa finalisation, plutôt que recevoir uniquement un PDF figé.

**How to apply:** Workflow standard pour tout livrable = (1) produire le **.docx modifiable** (charte MDC navy/or) ; (2) l'utilisateur annote/observe ; (3) j'intègre et je régénère le **.pdf final** (via `mcp__Desktop_Commander__write_pdf`). Si un PDF est demandé d'emblée, fournir quand même le .docx en parallèle. Voir [[depouillement_releve_auto]] et la charte graphique du skill mdc-expert (§8). Terminologie : « Agence LMDC » (jamais « Cabinet »).
