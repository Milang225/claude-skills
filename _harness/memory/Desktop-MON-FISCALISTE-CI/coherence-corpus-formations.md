---
name: coherence-corpus-formations
description: "Audit de cohérence du corpus des formations MDC (23/08/2026) : méthode par sondes, 4 incohérences de fond corrigées, défaut des blocs de code résolu dans prep_pub"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9aafd489-0e3a-4736-b910-695ffef31c99
  modified: 2026-08-23T22:43:02.060Z
---

**Le corpus des formations** (`Desktop/MON FISCALISTE CI/*.md`, publié dans `Documents/FORMATIONS MDC/FISCALITE_CI/`) compte une quarantaine de modules. Audité intégralement le **23/08/2026**.

**La méthode qui marche** : extraire par **sondes thématiques** toutes les lignes du corpus mentionnant un même pivot (taux, seuil, délai, article), puis les comparer côte à côte. Outil réutilisable : `scratchpad/coh.py`, fonction `sonde(titre, motif, contexte)`. Sondes passées : I-BIC, IMF, TVA, AIRSI, PPSSI/RIBNC, art. 92, IRVM/IRC, seuils de régime, espèces 250 000, déficits, art. 110, conservation, pénalités, droits d'apport, réévaluation.

**Quatre incohérences de fond trouvées et corrigées** — toutes nées du même mécanisme : **un module écrit pour corriger une erreur du corpus, sans propagation aux modules antérieurs**.
1. **Forclusion du remboursement de TVA** : 3 ans → **2 ans** (CGI Art. 383, AF 2022 art. 8-2). 13 occurrences dans 8 modules. Voir [[prescription-fiscale-3-ans]].
2. **« Pénalités 25 % des droits éludés (LPF Art 161) »** : formule inexistante au barème, réfutée par le module Sanctions mais toujours présente dans Prescriptions, Prix de transfert et Apports. Remplacée par **intérêts 5 % + 0,5 %/mois** (10 % + 1 % pour les impôts de tiers) **+ majoration selon l'infraction** (15/30/100 %, 50/100/200 % en taxation d'office, 150 % en abus de droit).
3. **Redevances plafonnées à 50 %** présentées comme règle générale dans le levier L-32 du module Optimisation, alors que le module Prix de transfert avait établi la **double limite 5 % / 20 %**. Voir [[redevances-double-limite-5-20]].
4. **Écart de réévaluation « imposable »** dans le levier L-42, contredit par le module dédié. Voir [[reevaluation-ecart-exonere]].

**Un défaut de forme systémique** : les blocs de code ```` ``` ```` **ne sont pas rendus** par les générateurs — backticks affichés en clair, lignes éclatées en paragraphes. Présent dans **26 modules**, invisible au contrôle règle d'or. **Résolu à la racine** : `prep_pub.py` (étape 0) convertit désormais tout bloc de code en **tableau à une colonne**, et le contrôle interne signale un backtick résiduel. Sauvegarde `prep_pub.py.bak-fences`.

**Ce qu'il reste à faire** : `FICHE_MODELES_FACTURES_ET_AVIS_DE_REGLEMENT.pdf` porte encore le défaut — **sa source markdown est introuvable**, il faudrait la réécrire. Illustration de la règle : un PDF sans sa source n'est plus corrigeable. Voir [[controle-coherence-fin-de-travaux]], [[regle-dor-controle-livrables]].

**La règle à retenir** : quand un nouveau module corrige une erreur du corpus, **passer immédiatement une sonde sur l'ancienne formulation dans tous les autres modules**. Sans cela, la correction reste locale et le corpus se contredit.
