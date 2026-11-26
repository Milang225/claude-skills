---
name: chemin-scripts-publication-mdc
description: les scripts de publication MDC ont migré sous skills/mdc/modules/ et md2docx exige NODE_PATH
metadata:
  type: project
---

Les scripts de publication MDC ne sont plus dans `~/.claude/skills/mdc-expert/scripts/` mais dans **`~/.claude/skills/mdc/modules/mdc-expert/scripts/`** (`publish_pdf_mdc.py`, `md2docx_mdc.js`, `sync_formation_lmdc.sh`).

`md2docx_mdc.js` échoue avec `requireStack` si on ne lui passe pas le chemin des modules globaux — le paquet `docx` est installé en global nvm, pas à côté du script :

```
NODE_PATH="$(npm root -g)" node ~/.claude/skills/mdc/modules/mdc-expert/scripts/md2docx_mdc.js SOURCE.md CIBLE.docx
```

**Why :** l'ancien chemin est encore accepté par un lien pour le PDF mais pas par node, et l'échec arrive après la publication du PDF — on croit le livrable complet alors que le DOCX manque.

**How to apply :** toujours utiliser le chemin `skills/mdc/modules/` et préfixer l'appel node par `NODE_PATH="$(npm root -g)"`. Vérifier la présence des deux fichiers avant d'annoncer la publication, puis lancer la synchronisation — voir [[sync-formation-lmdc-apres-publication]] et [[glyphes-interdits-pdf-mdc]].
