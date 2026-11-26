---
name: reevaluation-ecart-exonere
description: "Écart de réévaluation libre : exonéré d'impôt BIC, seule la quote-part des biens amortissables est réintégrée au rythme de l'amortissement (CGI Art. 334)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9aafd489-0e3a-4736-b910-695ffef31c99
  modified: 2026-08-23T16:52:11.094Z
---

**La règle exacte** (CGI Art. 330-338, AF 1999 art. 19) :
- L'écart de réévaluation libre est **EXONÉRÉ d'impôt BIC** — il n'est ni un produit, ni une réserve, il n'affecte pas le résultat (compte **1062**, capitaux propres).
- **Contrepartie, Art. 334** : la quote-part afférente aux biens **AMORTISSABLES** est **réintégrée au résultat fiscal au rythme de l'amortissement**, ce qui neutralise le surplus d'amortissement déduit. Effet net sur l'impôt : **zéro**.
- La quote-part des biens **non amortissables (terrains)** est **définitivement exonérée** — c'est là qu'est le seul vrai gain fiscal, avec la réduction des plus-values de cession futures.

**Champ plus étroit que le SYSCOHADA** : l'Art. 330 **exclut les incorporels et les titres de participation**, là où SYSCOHADA Art. 62 les admet. L'Art. 331 impose la **totalité** des immobilisations éligibles — réévaluation partielle interdite. Écart **non distribuable**, ne compense pas les pertes ; incorporation au capital possible au droit d'apport **6 %** (Art. 758).

**Ce que cette fiche corrige** : le corpus `mdc-expert/SKILL.md` §15.2 affirmait « imposable au taux IS, 35 % sur l'écart » — doublement faux (l'écart est exonéré, et le taux de 35 % n'existe plus ; I-BIC à 25 %). Ligne corrigée le 22/08/2026, sauvegarde `SKILL.md.bak-reevaluation`.

La réévaluation **légale** (Art. 322-329, coefficient 1,40, compte **1061**, taxe spéciale 10 %) est un dispositif **clos** de 1994-1995 : un solde 1061 au bilan en est le vestige.

Module de référence : `FORMATION_ECARTS_REEVALUATION_CI` (MC-FORM-CPTA-2026-036). Voir [[plus-values-regime-verifie]], [[prescription-fiscale-3-ans]], [[toujours-verifier-dgi-2026]].
