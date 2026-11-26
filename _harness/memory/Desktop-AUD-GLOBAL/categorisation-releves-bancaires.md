---
name: categorisation-releves-bancaires
description: "Tout relevé bancaire analysé doit être restitué avec la catégorisation des entrées ET des dépenses, jamais avec les seuls totaux"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c8a5d90f-6542-40c6-9ee2-e3d95bcfa503
  modified: 2026-07-21T21:31:30.827Z
---

À chaque analyse de relevé bancaire, produire systématiquement la **ventilation par catégorie des entrées et des sorties** — pas seulement les totaux encaissements / décaissements.

Catégories de référence (skill `mdc-expert` §2) :
- **Entrées** : espèces versées · remises de chèques · virements reçus · autres crédits (intérêts, produits divers)
- **Sorties** : chèques payés · virements émis · retraits d'espèces · frais bancaires (timbre, dossier, cotisation package, agios, taxes, abonnement) · autres débits

**Why :** les totaux seuls ne disent rien. C'est la ventilation qui fait apparaître ce qui compte : la part réelle du chiffre d'affaires, les mouvements de trésorerie internes à écarter du CA, les retraits d'espèces non justifiés, la paie hors banque. Sur le Collège Saint-Exupéry (juillet 2026), la catégorisation a isolé 536 M de virements internes qui, additionnés à l'aveugle, auraient gonflé le CA de plus du double et faussé toute l'analyse de régime.

**How to apply :** partition **stricte et exhaustive** (chaque ligne dans une catégorie et une seule, la somme des catégories doit retomber exactement sur le total du relevé). Toujours vérifier ensuite les totaux catégorisés contre les totaux imprimés par la banque, puis contre le solde de clôture — règle de vérification croisée obligatoire. Isoler explicitement les gros mouvements atypiques plutôt que de les noyer dans une catégorie. Voir [[ecritures-cloture-virement-resultat]] pour la restitution comptable qui en découle.
