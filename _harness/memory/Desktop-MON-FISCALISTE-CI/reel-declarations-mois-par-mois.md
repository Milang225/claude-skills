---
name: reel-declarations-mois-par-mois
description: "Entreprises au réel (RSI/RNI) — tout travail se détaille mois par mois, pas en agrégat annuel"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 393e9b07-36b0-4f65-8370-465b88a5ecd9
  modified: 2026-07-28T11:32:51.628Z
---

Pour toute **entreprise au réel (RSI/RNI)**, quand le gérant demande un travail (déclarations, estimation, régularisation, exposition, reconstitution), le présenter **mois par mois** — une ligne = un mois. La TVA, l'ITS + CN + FDFP, la TSE et les retenues à la source sont **mensuelles**. Le total annuel n'apparaît qu'en **récapitulatif APRÈS** le détail mensuel, jamais à la place. Seuls l'IMF/BIC et la patente sont annuels.

**Why :** feedback du gérant sur le dossier TIM 7 (juillet 2026) — j'avais livré une estimation TVA/TSE en agrégat annuel alors que les déclarations d'un réel sont mensuelles.

**How to apply :** produire un tableau `Mois | base | impôt` par nature ; le modèle existe déjà (CALC-TVA-TIM7-2026 mois par mois). Règle capitalisée dans le skill mdc-expert §30.6-8 ; cf. §30.3 carnet mensuel. Voir [[service-declarations-mensuelles-eimpots]] et [[declarations-jamais-inventer-donnees]].
