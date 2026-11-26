---
name: pre-controle-anti-redressement
description: "Cap du CRM Équipes = machine anti-redressement (calculs justes + détection d'anomalies déterministe, sans IA au runtime) ; règles fiscales déjà codées"
metadata: 
  node_type: memory
  type: project
  originSessionId: 44b0d6d5-40e2-42cc-bd26-efb4326bce2b
  modified: 2026-09-21T10:24:42.184Z
---

**Cap donné par le gérant (2026-09-21)** : finaliser le CRM Équipes comme une **machine anti-redressement**. Pour chaque client/mois : (1) calculer juste (SYSCOHADA), (2) confronter relevé ↔ compta ↔ FNE ↔ déclarations, (3) détecter toute anomalie qu'un contrôleur DGI exploiterait, classée par gravité, **avec l'article du CGI et l'action corrective**.

**Why:** MDC est une agence de conformité ; sa valeur = « qu'un contrôleur ne puisse pas nous redresser ». **How to apply:** toute nouvelle brique doit être **déterministe (aucune IA au runtime — exigence explicite du gérant)** ; l'IA ne sert qu'à *écrire* les règles en lisant le CGI. Chaque alerte cite son article.

**Audit du moteur de calcul (2026-09-21) : il est SAIN et s'auto-contrôle.** Sur Globe (2026, source mixte) : balance équilibrée (écart 0), contrôles internes qui PASSENT — T1-T5 (balance), R1/R2 (compte de résultat), B1 (Actif=Passif), B2 (résultat CR=bilan=4 813 494), B3. Seul B4 (comptes non rattachés) échoue, et il révèle de vraies anomalies : **caisse/momo créditeurs (531/571 = recettes non déclarées, MAJEUR), comptes d'attente 471, tiers au sens anormal (401 débit, 411 crédit)**. Les calculs n'ont jamais été le problème — le manque, c'est la **visibilité unifiée** (un écran de « Pré-contrôle » qui agrège tous ces signaux). Fonctions clés : `eqBalanceGenerale`, `eqCompteResultat`, `eqBilan`, `eqComputeSuiviFiscal`, `eqPointsAEclaircir` (codes D1-D16), `eqComputeReleve`, `eqRapprochements`.

**Briques anti-redressement livrées EN PRODUCTION (2026-09-21), validées sur Globe :**
- **ERB — État de Rapprochement Bancaire** en tableau 2 colonnes (relevé ↔ compta 521) + PDF SYSCOHADA, dans « Analyse relevé ». Champs backend `solde_compta_521` + `releve_totaux` (au niveau RACINE du retour de `eqRapprochements`, PAS niché dans `banque`). Globe mai 2026 : réconcilié, écart 0.
- **Droit de timbre de quittance (v1)** — `eqTimbreBareme` + `eqComputeTimbre` (sorties espèces du mois, retourne aussi `parTranche` = décompte par tranche du formulaire officiel) + nature `TIMBRE` dans le Suivi fiscal (« Dû auto », échéance **16 du mois +1**, date e-Impôts ; art. 879 CGI dit 10). Endpoint **`/declaration-timbre/:annee/:mois`** = Section 1 « Droits progressifs » du formulaire **DTIMBRE** pré-remplie (nb + total par tranche), prête à saisir sur e-Impôts. Globe juillet 2026 = **8 100 F** (1×100 + 6×500 + 1×5000). v2 : mode réel confirmé par le rapprochement ; reste possible : génération de l'annexe EDI `edi_annexe_dtimbre.xlsm` → XML pour injection directe.
- **D14 renforcé** — sur paiement espèces > 250 000 : recommande la **voie tracée** (virement/chèque/mobile money, momo exempté du seuil depuis AF 2026), art. 18 bis/373.
- **D16 fractionnement** — détecte les règlements espèces répétés au même bénéficiaire (chacun ≤ 250 000, cumul > 250 000) → soupçon de contournement, cite art. 162/799. Globe juillet : « enrouleur electrique — 2 × 171 414 = 342 828 F ».

**Reste à faire (priorités du gérant) :** rapprochement **exhaustif & nature-aware** (chaque ligne du relevé → rapprochée / à examiner / anomalie, couverture 100 %, détection structurelle des rejets par paires +X/−X, pas par mots-clés) ; statut d'**attestation** par compte de tiers (401/411 « attestable » seulement si le flux le confirme) ; recettes (encaissements banque vs CA déclaré, marge négative) ; FNE manquante ; IMF non provisionné ; l'écran **Pré-contrôle** unifié.

Voir [[timbre-fractionnement-cgi]], [[regle-jamais-proposer-fractionnement]], [[crm-architecture-deploy]].
