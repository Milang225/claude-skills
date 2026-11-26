---
name: courriers-en-brouillon-gmail
description: "Quand le gérant demande de préparer des courriers/emails, les déposer DIRECTEMENT en brouillon Gmail (create_draft), pas seulement en PDF"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e1fe21d5-7734-4db9-8597-05641de9260d
  modified: 2026-08-10T18:30:38.435Z
---

Quand Bilé demande de « préparer les courriers » (ou un email), les créer **directement en brouillon Gmail** via le connecteur Gmail (`create_draft`), corps rédigé et prêt à relire/envoyer — en plus du PDF à la charte si le courrier est aussi un livrable formel.

**Why :** il relit et envoie depuis Gmail ; il ne veut pas seulement un PDF.

**How to apply :**
- Charger l'outil `mcp__…__create_draft` (connecteur Gmail, id `b9f9afb9-…`) via ToolSearch, puis créer un brouillon par courrier (`subject`, `htmlBody` + `body` texte).
- **Destinataires** : laisser `to` vide pour un modèle (le courrier client se personnalise par client ; pour l'équipe, ajouter les adresses si connues).
- **Pièces jointes NON supportées** par `create_draft` (limite de l'outil) → mentionner « ci-joint le guide/manuel » et joindre le PDF à la main depuis le bureau.
- Le 2026-08-10, le connecteur a renvoyé `net::ERR_FAILED` (injoignable) : dans ce cas, prévenir le gérant que le connecteur Gmail doit être reconnecté (réessayer plus tard / session interactive), et garder les contenus prêts.

Voir [[prefs-documents-charte]] pour la charte des PDF joints.
