---
name: cgi-2026-versions-doublees
description: dans le CGI 2026, chaque article est reproduit deux fois ; seule la version datée est en vigueur
metadata:
  type: reference
---

L'édition 2026 du Code général des Impôts **reproduit de nombreux articles deux fois de suite** : d'abord la version **en vigueur**, signalée par une année accolée au numéro (`Art. 347 2020...`, `Art. 90 2024...`, `Art. 92 2025..`), puis la **version antérieure**, sans millésime. Les deux se suivent dans le fichier texte comme dans le PDF.

Pièges déjà rencontrés :

| Article | Version en vigueur | Version périmée répétée en dessous |
|---|---|---|
| **347** — seuil de facturation de la TVA | **200 000 001 F** (loi 2020-972, AF 2021) | 50 000 000 F |
| **90** — taux BNC et retenue bons de caisse | 25 % | 20 % |

Conséquence tranchée : une entreprise au **régime des microentreprises** (50 000 001 à 200 000 000) **ne peut pas facturer la TVA**, et l'option de l'art. 348 ne lui est pas ouverte — liste fermée. La TVA d'amont lui est un **coût définitif**. Le seuil de l'art. 347 coïncide avec le plancher du réel simplifié (art. 45).

**Why :** j'ai publié un module citant le seuil de 50 000 000 en lisant la mauvaise occurrence ; l'utilisateur avait raison de me reprendre.

**How to apply :** sur tout article du CGI, faire `grep -n` sur **toutes** les occurrences et retenir celle qui porte le millésime et la référence d'annexe fiscale la plus récente. Ne jamais se contenter du premier résultat. Voir [[textes-officiels-dgi-locaux]] et [[analyse-fiscale-quatre-sources]].
