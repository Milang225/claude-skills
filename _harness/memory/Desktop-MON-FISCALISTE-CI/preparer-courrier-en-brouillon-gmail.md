---
name: preparer-courrier-en-brouillon-gmail
description: "Quand l'utilisateur dit « prépare le corps du courrier / le mail », créer directement un BROUILLON dans son Gmail"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c3c001b6-a642-4b04-ae47-9c68316ff5e7
  modified: 2026-07-29T17:56:19.975Z
---

**Quand l'utilisateur demande de « préparer le corps du courrier » (ou « prépare le mail »), je crée DIRECTEMENT un brouillon dans son Gmail** (outil `create_draft`), en plus de le montrer à l'écran — je ne me contente pas d'afficher le texte.

**Pourquoi :** demande explicite du gérant (juillet 2026) — il veut le mail prêt dans ses brouillons, pas seulement dans le chat.

**Comment l'appliquer :** rédiger l'objet + le corps, appeler `create_draft` (destinataire = le client concerné ; le gérant complète pièces jointes + envoi). Rappeler que l'outil brouillon ne gère pas les pièces jointes → l'utilisateur les ajoute avant d'envoyer. Ne jamais ENVOYER sans accord explicite — seulement le brouillon.
