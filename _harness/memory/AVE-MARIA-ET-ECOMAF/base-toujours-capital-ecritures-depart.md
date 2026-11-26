---
name: base-toujours-capital-ecritures-depart
description: "Toute base comptable reconstituée doit partir du capital et des écritures de départ (CONST-01 à 03), jamais d'une balance sans capital"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b013bc2f-43c1-49d9-9be1-6ee933ade635
  modified: 2026-11-06T14:55:13.839Z
---

Une base comptable / balance reconstituée ne doit jamais sortir sans capital ni écritures de départ. Si le montant n'est pas connu, le demander à l'utilisateur avant de livrer plutôt que de laisser le capital à zéro.

**Why:** le 06/11/2026, l'utilisateur a reproché que la base ECOMAF 2S ait été livrée « sans capital et écritures de départ, comme on l'a fait plusieurs fois ». Il a donné le capital (10 000 000) ; l'ancienne règle « on ne devine jamais le capital » avait laissé le poste à 0.

**How to apply:** schéma MDC §36.3 + §37.2 étape 5 : CONST-01 D 4612 / C 1011 (souscription), CONST-02 D 521 ou D 571 / C 4612 (libération ; caisse si le relevé s'ouvre à 0), CONST-03 D 1011 / C 1013. Des espèces versées à l'ouverture du compte bancaire ont alors la caisse pour contrepartie (D 521 / C 571).
