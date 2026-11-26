---
name: toujours-joindre-les-fichiers
description: "Consigne permanente : toujours JOINDRE les fichiers à un courriel/livrable, jamais seulement les mentionner"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c3c001b6-a642-4b04-ae47-9c68316ff5e7
  modified: 2026-08-20T18:01:27.284Z
---

**Toujours JOINDRE les fichiers** quand un courriel ou un livrable les mentionne — ne jamais se contenter d'écrire « ci-joint » sans que la pièce y soit réellement.

**Why :** un mail qui annonce une pièce jointe absente fait perdre du temps au client et décrédibilise l'Agence ; la valeur est dans le fichier, pas dans l'annonce. (Consigne gérant, GLOBE, août 2026.)

**How to apply :**
- Préparer un brouillon Gmail → tenter d'**attacher réellement** la pièce (l'outil `create_draft`/`update_draft` accepte des pièces jointes en base64).
- Limite technique honnête : incorporer un binaire volumineux (xlsx/pdf/docx) via l'outil = transcrire son base64 → **risque de corruption silencieuse**. Dans ce cas : **livrer le fichier dans la conversation** (SendUserFile) prêt à glisser, le **signaler explicitement** dans le mail et **rappeler de le joindre** — jamais un mail qui prétend joindre sans joindre.
- Systématiquement livrer le(s) fichier(s) à l'utilisateur en même temps que le brouillon.

Lié à [[preparer-courrier-en-brouillon-gmail]], [[mails-jamais-joindre-exposition]] (ce qu'on NE joint PAS), [[skill-points-a-eclaircir]] §6bis (DEE + tableau de bord xls joint).
