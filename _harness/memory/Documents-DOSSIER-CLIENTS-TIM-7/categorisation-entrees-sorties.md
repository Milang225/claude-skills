---
name: categorisation-entrees-sorties
description: Règle permanente — tout livrable chiffré MDC comporte une catégorisation des entrées et des sorties de trésorerie
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4119d81a-9fa1-493a-9117-65388e7355ec
  modified: 2026-11-04T22:55:17.298Z
---

Le gérant demande que **tout livrable comportant une balance ou un état chiffré porte une catégorisation des entrées et des sorties de trésorerie** : banque (521) et caisse (571) séparément, chaque flux rattaché à sa nature (exploitation, personnel, social, fiscal, dirigeant, financement, à justifier), puis une synthèse consolidée hors virements internes. Demandé le 04/11/2026 sur le livrable balance et régularisations de TIM 7.

**Pourquoi :** une balance donne des soldes, pas l'origine des fonds. En contrôle, l'administration part de la trésorerie et demande d'où vient chaque encaissement et à quoi correspond chaque sortie. Présenter la catégorisation d'emblée montre la part des flux justifiés et isole à l'avance ce qui ne l'est pas, au lieu de le découvrir sous contrôle.

**How to apply :** construire les catégories depuis le journal, par contrepartie de chaque ligne de trésorerie (grouper par pièce, netter les comptes au sein de la pièce — les comptes de passage 4011, 422, 4472 disparaissent et la nature réelle du flux apparaît) — jamais à la main. Poser un contrôle bloquant : chaque pièce de trésorerie doit s'équilibrer, et solde d'ouverture + entrées − sorties doit redonner le solde de clôture au franc. Exclure le journal des à-nouveaux (RAN) des flux : c'est le solde d'ouverture. Neutraliser les virements banque → caisse dans la synthèse et asseoir les pourcentages sur les seuls flux externes. Quand le relevé n'est pas détaillé ligne à ligne, dire que la ventilation mensuelle n'est pas disponible plutôt que de la reconstituer.

**L'exercice antérieur aussi** (demandé le 04/11/2026) : quand il n'y a pas de journal, le lire au relevé bancaire — banque seule, montants annoncés comme des planchers, et la clôture ancrée sur l'à-nouveau de l'exercice suivant, ce qui donne l'ouverture par différence. Voir [[tim7-plancher-cumul-bic]].
