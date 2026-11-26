---
name: limite-pj-mail-gmail
description: Les PDF brandés MDC (~200 Ko à cause du logo) sont trop volumineux pour être encodés en base64 et passés en pièce jointe via create_draft.
metadata:
  type: feedback
---

Les livrables PDF brandés MDC pèsent ~200 Ko (logo JPEG intégré, ~160 Ko), soit ~280 000 caractères en base64 — au-delà de ce qu'un tool result peut restituer et de ce qu'il est raisonnable de réinjecter dans un appel `create_draft`. La compression (Ghostscript, PyMuPDF) ne gagne rien : le JPEG est déjà compressé.

**Why :** tenter l'encodage gaspille le contexte pour rien et échoue à la lecture (sortie tronquée et persistée sur disque).

**How to apply :** pour un mail avec livrable brandé, créer le brouillon Gmail avec le corps rédigé (`body` + `htmlBody`) SANS `attachments`, puis indiquer à l'utilisateur le chemin exact du fichier à glisser lui-même. Le dire franchement plutôt que de le passer sous silence. Voir [[preparation-mails]] et [[supervision-redaction-avant-livraison]].
