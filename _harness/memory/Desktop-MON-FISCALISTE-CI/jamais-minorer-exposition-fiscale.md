---
name: jamais-minorer-exposition-fiscale
description: "En exposition fiscale, ne jamais alléger par défaut — afficher le brut, toute minoration est conditionnelle à un justificatif produit"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fe4f2f95-a69c-4364-85d9-367f608bcc60
  modified: 2026-07-23T23:35:53.190Z
---

**En matière d'exposition fiscale, on n'allège JAMAIS par défaut.** On affiche le **montant brut**. Toute minoration — crédit d'impôt, taxe déductible, exonération, prélèvement subi — n'est portée au chiffrage **que sur justificatif effectivement produit**. À défaut, elle est présentée comme une **opportunité à sécuriser**, jamais comme un acquis.

**Why:** le gérant m'a repris sèchement le 23/07/2026 sur le dossier LERO : « ne fais plus cette erreur car tu as voulu fausser le calcul ». Trois de mes choix allaient tous dans le même sens — la baisse : (1) j'avais **déduit** l'AIRSI subi de l'IMF (−1 392 858) alors qu'un prélèvement opéré par un tiers ne se déduit pas d'office ; (2) j'avais retenu **une tranche** des arriérés (5 820 325) au lieu de la liste complète (9 252 217), TO laissées de côté ; (3) j'avais **omis** l'AIRSI 5 % dû sur les ventes (16 714 828). Résultat : exposition sous-évaluée de 128 962 819 à 102 936 286. Un chiffrage minoré ne protège pas le client — il l'expose à une mauvaise surprise au contrôle.

**How to apply:**
- Toute déduction/crédit/exonération ⇒ **exiger la pièce** avant de l'inscrire ; sinon, brut + mention « opportunité, sous réserve de production de … ».
- **Ne jamais déduire d'office** un prélèvement opéré par un tiers ([[reflexe-retenues-source-prestataires]]).
- **Arriérés : prendre la liste e-impôts EN ENTIER**, et ajouter explicitement les taxations d'office.
- **Contrôle d'omission** : dérouler la matrice des natures (skill mdc-expert §33) — l'oubli d'une nature *due* est une minoration déguisée.
- **Test du faisceau** : si tous mes arbitrages penchent du même côté, c'est un biais, pas une coïncidence. Le vérifier avant de livrer.

**Corollaire — neutraliser un double compte ne se fait JAMAIS en rabotant une ligne.** Quand une même imposition figure à deux endroits (ex. LERO : la TVA 1 008 000 de la TO de décembre 2025 présente à la fois dans la liste e-impôts et dans le réel), on laisse **chaque ligne à sa valeur intégrale** et on ouvre une **ligne dédiée « neutralisation du double compte »** en négatif, commentée. Le gérant m'a repris (« mais ça n'a pas été changé ») quand j'avais ramené les arriérés de 9 252 217 à 5 820 325 pour absorber le doublon : à l'écran, cela redonne exactement le chiffre minoré qu'il avait fait corriger. Le montant réclamé en l'état par le centre doit rester **lisible en entier** (LERO : 15 132 030) ; le retraitement se voit à part.

Contrôle formalisé : **C12** de la grille du skill `auditeur-fiscal`. [[regle-dor-controle-livrables]] [[client-lero-forage]] [[regularisation-to-liquidee]]
