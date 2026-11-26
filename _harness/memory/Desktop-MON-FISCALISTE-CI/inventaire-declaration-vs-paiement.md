---
name: inventaire-declaration-vs-paiement
description: Inventaire déclaratif — toujours distinguer la DÉCLARATION et le PAIEMENT (2 étapes)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 393e9b07-36b0-4f65-8370-465b88a5ecd9
  modified: 2026-07-28T12:44:44.377Z
---

Dans tout inventaire/grille déclarative, **distinguer les DEUX étapes fiscales** : la **déclaration** (déposée ou non) ET le **paiement** (payé ou non). Chaque case porte les deux.

Codes : **D+** déclaré + payé · **D−** déclaré, NON payé · **D\*** déclaré à zéro/minoré · **N** non déclaré · **TO+ / TO−** taxé d'office payé / non payé · **—** néant · **~** à vérifier.

**Why :** feedback du gérant sur les grilles TIM 7/LBTECH/GLOBE — je ne distinguais pas déclaration et paiement. Une déclaration déposée mais non payée n'est pas à jour ; l'exigible ce sont les paiements manquants (typique au TEE : la DTEE annuelle est déposée mais les fractions mensuelles restent impayées).

**How to apply :** codage à deux dimensions dans le générateur de grille ; en pied de note rappeler « chaque case = déclaration + paiement ». Règle capitalisée dans le skill mdc-expert §30.6-10. Voir [[its-fdfp-imbriques]] et [[reel-declarations-mois-par-mois]].
