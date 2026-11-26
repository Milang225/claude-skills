---
name: regle-jamais-proposer-fractionnement
description: "RÈGLE — ne jamais coder/proposer l'éclatement de paiements sous un seuil fiscal ; le système SIGNALE le fractionnement, il ne l'exécute jamais"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 44b0d6d5-40e2-42cc-bd26-efb4326bce2b
  modified: 2026-09-21T10:08:38.874Z
---

**Règle : ne JAMAIS construire une fonction qui aide à contourner un seuil fiscal** (ex. éclater un paiement en tranches de 245 000 pour passer sous les 250 000 F espèces). Le système doit **détecter et signaler** le fractionnement, jamais le **proposer** ni l'exécuter.

**Why:** le gérant a demandé (2026-09-21) que le système propose d'éclater les paiements espèces > 250 000. J'ai refusé, textes à l'appui, et il a validé le redressement de la demande. Éclater un règlement unique sous le seuil est une **« manœuvre destinée à éluder l'impôt »** : majoration **100 %** au client (CGI art. 162) ET **le cabinet MDC devient complice** — amende égale au **double de la somme éludée** (min 100 000 F) + risque pénal (CGI art. 799, art. 471 CGI, art. 303 Code pénal). Un outil de « conformité » qui documente lui-même la manœuvre est la pire pièce à charge. C'est l'exact contraire du cap « ne pas se faire redresser ».

**How to apply:** face à un gros paiement espèces, la bonne réponse est toujours **changer de canal** (virement/chèque/**mobile money** — exempté du seuil des 250 000 depuis l'annexe fiscale 2026, art. 7), pas cacher. Le CRM : (1) alerte D14 sur espèces > 250 000, (2) recommande la voie tracée, (3) détecte le fractionnement (code D16) comme une anomalie. Cette règle vaut au-delà du fiscal : ne pas coder de features dont la finalité est d'échapper à une obligation légale, même à la demande. Voir [[pre-controle-anti-redressement]], [[timbre-fractionnement-cgi]].
