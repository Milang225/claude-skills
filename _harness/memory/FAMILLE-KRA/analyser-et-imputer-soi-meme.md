---
name: analyser-et-imputer-soi-meme
description: "Le Gérant veut que je reconstitue moi-même le circuit des fonds et l'imputation comptable et fiscale d'une situation, sans attendre qu'il dicte chaque écriture"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 679f9371-c60d-41eb-a209-b37b7fe4122b
  modified: 2026-11-18T02:23:36.943Z
---

Devant une opération, je dois retracer d'où vient l'argent et par où il passe, puis choisir les comptes et le traitement fiscal. Par exemple : un prêt est reçu en banque puis versé en caisse ; un impôt payé par mobile money suppose d'alimenter d'abord le mobile depuis les fonds disponibles, au montant exact du paiement. Je ne dois pas attendre qu'on me dicte chaque écriture, ni court-circuiter le circuit (pas de caisse contre caisse sans compte de virement, pas de paiement mobile sans alimentation préalable).

**Why:** Le 18/11/2026, sur FAMILLE KRA, le Gérant a dû répéter plusieurs fois la logique de trésorerie (prêts → banque → caisse, alimentation du mobile pour les impôts). Il veut que je sois capable d'analyser la situation, d'imputer et d'attribuer le bon traitement fiscal de moi-même.

**How to apply:** Pour chaque flux, je reconstitue le chemin des fonds avec la pièce (échéancier, quittance MOB, reçu…). Chaque passage d'un compte de trésorerie à un autre se fait par le 585, et un compte de trésorerie ne doit jamais être créditeur. J'applique la règle de [[tresorerie-par-defaut-caisse]] et le régime effectif de [[regime-client-avant-impots]]. Je ne pose une question que lorsqu'un fait manque vraiment, pas quand il s'agit d'imputer.
