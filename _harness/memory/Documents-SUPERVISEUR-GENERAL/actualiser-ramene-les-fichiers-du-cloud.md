---
name: actualiser-ramene-les-fichiers-du-cloud
description: "« Actualiser » la plateforme redescend les fichiers du cloud : un document interne déplacé localement revient dans le dossier client"
metadata:
  node_type: memory
  type: project
  originSessionId: a5d13372-4dda-4833-a70d-57482267f855
  modified: 2026-11-25T03:44:31.657Z
---

Constaté le 25/11/2026 sur MABEK. Un document déjà transmis au cloud (R2) sous un chemin du dossier client **revient à cet endroit** dès que la plateforme est actualisée, même si on l'a déplacé localement. Le script de restitution interne, rangé dans `_INTERNE`, est ainsi réapparu deux fois à la racine du dossier d'audit, avec les attributs d'un fichier téléchargé.

**Why:** un document interne (script d'entretien, feuille de contrôle) qui réapparaît à la racine d'un dossier client est coché « bon » (★) et devient transmissible au cloud, donc visible dans l'espace du client. Le déplacer sur le Mac ne suffit pas.

**How to apply:** avant toute remise, (1) décocher ★ avec `marquer_livrable` en passant `actif: false` — l'appel sans `actif` est un coup dans le vide, il renvoie `livrable: true` sans rien changer ; (2) déplacer le fichier dans `_OBSOLETE` ; (3) **ne jamais** se reposer sur la liste des fichiers du dossier pour choisir les pièces jointes : donner à `preparer_brouillon_gmail` la liste explicite des clés. Reste à faire retirer la copie du cloud (aucun outil ne le permet de mon côté).

Autre effet du même mécanisme : le PDF redescendu du cloud est régénéré depuis le Word, donc plus lourd (logo en PNG) et avec des retours à la ligne différents — le contenu est identique, la pagination peut changer. Vérifier la pagination sur le PDF qui part réellement. [[livrables-toujours-sur-la-plateforme]] [[aucun-telechargement-plateforme]]
