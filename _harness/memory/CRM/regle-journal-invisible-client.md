---
name: regle-journal-invisible-client
description: RÈGLE gérant : le journal (opérations, écritures, comptes) ne doit pas exister côté client ; outil réservé à l'équipe MDC, interdit aussi côté serveur
metadata:
  type: feedback
---

Décision du gérant (08/11/2026) : « le client ne doit pas voir ça chez lui » — ni journal des opérations, ni écritures, ni comptes, n° d'écriture, historique ou écarts.

**Why:** le client ne connaît pas le journal ; c'est un outil de travail de l'équipe.

**How to apply:** côté client, seulement des gestes simples (Point de vente, Factures, Caisse, Mobile Money, Nouvelle recette / dépense) qui écrivent dans la même table. Ne jamais se contenter de masquer : routes client coupées côté serveur. ⚠ La branche locale `integrite-comptable` ajoute encore au portail historique, n°, pastilles et bandeau : à déplacer côté équipe (étape 3 du prompt dans `~/CRM/TRANSMISSIONS_INFORMATIQUE/2026-11-08/TRANSMISSION.md`). Voir [[regle-jamais-cloturer-mois]], [[transmissions-informatique]].
