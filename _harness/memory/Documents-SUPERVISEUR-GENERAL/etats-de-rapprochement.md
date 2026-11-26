---
name: etats-de-rapprochement
description: 23/11 — sept feuilles de travail produites par le dossier : CA, salaires, impôts, banque, trésorerie, DGI, flux
metadata:
  type: project
---

`etats_rapprochement.py` produit, par exercice, sept feuilles de travail à partir de ce qui est déjà au dossier : ER1 chiffre d'affaires, ER2 salaires et cotisations, ER3 impôts et taxes, ER4 rapprochement bancaire, ER5 trésorerie, ER6 déclaré à la DGI, ER7 évolution des encaissements et décaissements.

Chaque feuille porte objet, sources, tableau du rapprochement, ce que l'état révèle, ce qui manque, conclusion et trois signatures. Référence `MC-ER-<dossier>-<exercice>-<n°>`. Sortie en PDF et Word par les mêmes publieurs que les livrables rédigés ; l'ancienne version va dans `_anciennes_versions`.

**Règles posées :** un état qui manque de sa source n'est pas produit à moitié, il dit ce qui lui manque ; un écart sans conclusion empêche de clore l'état ; une feuille de travail est interne et ne part jamais au client.

**Why :** le rapport de diagnostic et l'avis fiscal attendent ces rapprochements écrits — c'est ce qui bloquait les livrables à 0 %.

**How to apply :** l'écran est sous les rapprochements, onglet Étude comparée ; route `/api/etats_rapprochement`. Voir [[rapprochements-atelier]].
