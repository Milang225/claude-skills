---
name: tresorerie-par-defaut-caisse
description: "Sans compte de trésorerie signalé par le cabinet (banque, chèque, mobile money), tous les flux passent par la caisse 571"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 679f9371-c60d-41eb-a209-b37b7fe4122b
  modified: 2026-11-17T23:23:34.042Z
---

Tant que le cabinet ne m'a pas indiqué qu'un client a un compte bancaire, un compte de chèques ou un compte de mobile money, tous les mouvements de trésorerie vont sur la caisse (5711). Je ne crée pas de compte 52x, 55x ou 5211 « à identifier » sur un simple libellé. Exception mobile money (instruction du 18/11/2026) : quand un règlement est attesté par une pièce de paiement mobile (quittance e-impôts « MOB », reçu Wave/Orange Money…), il passe par le 552, alimenté depuis la caisse le même jour : D 585 / C 5711, puis D 552 / C 585, puis D tiers / C 552.

**Why:** Le 17/11/2026, sur FAMILLE KRA, j'avais créé un compte bancaire 5211 « à identifier » pour les commissions, et le journal passait les paiements d'impôts par un compte 552 de mobile money avec des chargements depuis la caisse. Le Gérant a rappelé la règle : sans information, tout passe par la caisse. Il exige des écritures cohérentes, claires, exactes, conformes à un principe comptable, jamais un schéma sans sens (ex. stock contre trésorerie).

**How to apply:** Un règlement sans compte de trésorerie connu se passe D tiers / C 5711 (ou l'inverse pour un encaissement). Exception, fonds d'emprunt (instruction du Gérant du 18/11/2026, FAMILLE KRA) : le prêt est viré sur le compte bancaire du prêteur puis transféré en caisse. Écritures : D 521xxx / C 162 (mise à disposition), D 585 / C 521xxx (retrait), D 5711 / C 585 (versement en caisse). Jamais de banque directement contre caisse, toujours par le 585. Voir [[famille-kra-negociant]].
