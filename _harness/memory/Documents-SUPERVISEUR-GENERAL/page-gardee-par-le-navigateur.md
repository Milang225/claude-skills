---
name: page-gardee-par-le-navigateur
description: « Ça ne passe pas » après un déploiement réussi venait du cache du navigateur
metadata:
  node_type: memory
  type: project
  originSessionId: 7d1e2fa5-fd41-43ee-b04b-bc1d053b28e5
  modified: 2026-11-24T09:48:17.655Z
---

La page de l'atelier était servie sans aucune consigne de cache : le navigateur gardait l'ancienne, et après une mise en ligne réussie le gérant voyait toujours l'écran d'avant. Corrigé le 24/11/2026 — les deux endroits qui servent une page posent `Cache-Control: no-store, must-revalidate`, et un contrôle refuse toute page servie sans consigne de cache.

**Why:** cela a produit plusieurs « ça ne passe pas » et « je ne vois rien changé » dans la session du 15 au 24/11, alors que le déploiement était bon à chaque fois. On cherchait la panne dans le code au lieu du cache.

**How to apply:** quand il dit que rien n'a changé après une mise en ligne, vérifier d'abord les en-têtes servis (`curl -s -D- -o /dev/null http://localhost:8770/`) avant de soupçonner le code. Pour reproduire un écran hors ligne sans compte : construire la page comme le serveur (remplacer `__NOMS__`, `__SCHEMA__`, `__REGIMES__`, `__DEPARTEMENTS__`, `__PROMESSE__`), charger le script dans node avec un faux `document`, et appeler la fonction de rendu — elle écrit dans la page, elle ne retourne rien. Voir [[ecran-plateforme-apostrophe]], [[traitement-automatique-des-releves]].
