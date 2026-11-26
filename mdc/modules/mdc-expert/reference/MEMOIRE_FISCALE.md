# MÉMOIRE FISCALE PERSISTANTE — Chatbot fiscal du gérant MDC

> Ce fichier est la mémoire longue du chatbot fiscal. À LIRE au début de toute session
> fiscale/comptable, et à METTRE À JOUR à chaque échange important (préférences, clients,
> questions traitées, décisions). Règle d'or §10 du SKILL.md.

## CŒUR DE MÉTIER MDC (priorité absolue)
- Reconstituer la **base comptable à partir des états financiers** → détecter les **matrices d'anomalies** (comptable/fiscal/social) → faire des **propositions** (régularisations + plan).
- Méthode dédiée : `reference/METHODE_RECONSTITUTION_BASE_COMPTABLE.md` (mapping INVERSE états→comptes).

## PRÉFÉRENCES DU GÉRANT (M. BILE Fils Séverin)
- **RÈGLE PERMANENTE (absolue)** : toujours travailler en **francs CFA (XOF)** et selon le **droit ivoirien** — CGI CI, Annexes Fiscales, LPF, Doctrine fiscale DGI, OHADA/SYSCOHADA révisé. Toujours **citer les sources** fiscales et comptables.
- **RÈGLE PERMANENTE — PAPIER À EN-TÊTE (absolue, toutes sessions)** : TOUT livrable LMDC doit être produit sur le papier à en-tête MDC (en-tête logo + identité récurrents, pied NCC/RCCM/contacts récurrent) via `scripts/generate_livrable_mdc.py` (python-docx). Ne JAMAIS livrer un document MDC sans cet en-tête/pied. Logo : `scripts/logo-mdc.jpg`.
- Veut un **chatbot fiscal permanent, sans perte de mémoire** au fil des échanges.
- Pédagogie : **exemples concrets, chiffres ronds, pas-à-pas, zéro jargon** quand il dit « je ne comprends rien ».
- Apprécie les tableaux récap et la validation explicite de sa compréhension.
- Devise directrice : « La fiscalité ne sert à rien sans comptabilité » → toujours coupler les deux.

## SOURCES ASSIMILÉES (juin 2026)
- 4 ouvrages OCRisés → fiches dans `reference/` (TVA/TOB/TSE/AIRSI ; Impôts bénéfices ; Compta SYSCOHADA ; SYSCOHADA/IFRS).
- Texte OCR brut : `Desktop/MES DOCS FISCALITÉ /_OCR_TEXTE/`.
- **⭐ juillet 2026 — 2 publications officielles DGI ingérées intégralement** (`Desktop/MES DOCS FISCALITÉ /SYNOPTIQUES.pdf` + `IMPOTS ET TAXES.pdf`) : le **Tableau synoptique des impôts et taxes** (Éd. AF 2025 : taux/base/exonérations/articles CGI) et le **Calendrier des obligations fiscales** (délais/service/personnes soumises). → fiche maîtresse `reference/FICHE_SYNOPTIQUE_CALENDRIER_DGI.md` (fait foi pour taux & délais).

## NOTIONS DÉJÀ EXPLIQUÉES (ne pas réexpliquer sauf demande)
- IMF RSI = 0,5 % CA, plancher 3 M, **sans plafond** (RNI plafonné 35 M).
- **Condition b) de l'IMF** (Note DGI 01137 du 06/04/2022) : cumul = (I-BIC OU IMF, le + grand) + Patente ;
  si < **8 M (RSI)** / **9,6 M (RNI)** → payer le complément. Patente exonérée = comptée à sa valeur théorique.
  Exonéré d'IMF lui-même → 0 (aucune régularisation). Compris et validé par le gérant via exemple « Ets KOUASSI ».
- Leviers d'optimisation BTP traités (TVA encaissement, amort. dérogatoires, Art 110, Art 28, crédit emploi).

## CLIENTS / DOSSIERS SUIVIS
- (à compléter au fil des missions)

## JOURNAL DES ÉCHANGES
- 2026-06-08 : Assimilation des 4 ouvrages + capitalisation Section 20. Q/R sur IMF RSI, condition b), exonération patente, optimisation BTP.
- 2026-06-17 : FINALISATION. Chaîne d'audit complète : AXE I documentaire (LI-0) récupéré + 12 livrables intermédiaires brandés + reconstitution + notation A→E + régularisations. Manuel équipes (MC-PROC-AUDIT-2026-002). Générateur papier à en-tête (logo, python-docx). Protocole implémentable §24. INDEX maître posé. EN ATTENTE décision gérant : (1) GitHub (privé/public + données clients), (2) socle Journal→Balance→États du tableau SOM V2, (3) sort de mon-comptable.
- 2026-07-15 : **Ingestion des 2 publications DGI officielles** (Synoptique AF 2025 + Calendrier des obligations). Création de `reference/FICHE_SYNOPTIQUE_CALENDRIER_DGI.md`. Corrections apportées au SKILL.md : (1) grille des régimes AXE II corrigée (TCE ≤5M / TEE 5-50M / RME 50-200M / RSI 200-500M / RNI >500M) ; (2) **charges patronales tranchées** — CE proprement dite **exonérée pour le personnel local** (9,2 % expatrié uniquement), total patronal **local 2,8 %** (CN 1,2 % + TA 0,4 % + TFPC 1,2 %, FDFP local = 1,6 %) / **expat 12 %** ; l'ancienne lecture « 4 % » est écartée (double compte) et la controverse KRA est résolue (inférence masse ÷ 2,8 % confirmée) ; (3) barème ITS mensuel (0/16/21/24/28/32 %) + RICF (0 → 44 000/mois) ajoutés au SKILL §1 et §15.4. Édition = AF 2025 → recouper AF 2026 avant de figer un chiffre.
- 2026-06-18 : USINE À LIVRABLES consolidée. Dossier `Documents/LIVRABLES AUDIT LMDC/` (cadrage->documentaire->14 intermédiaires->clôture notation/exposition/plan) + propositions LI-15..19 (passage fiscal, audit croisé, retenues/hors bilan, optimisation, exonérations) dans dossier séparé. Note de démarrage (MC-NDM) + e-mail + feuille de route (MC-FDR) + manuel équipes. Générateur rendu SOBRE (sans émoji). Fiche maîtresse : reference/FICHE_USINE_LIVRABLES_AUDIT.md.

## IRVM vs IRC — taux officiels vérifiés (source : DGI, « Impôts et taxes en Côte d'Ivoire », pp. 30-33 ; capitalisé juillet 2026)

**IRVM (Art. 180 et s. ; taux Art. 182-183)** — retenue à la source sur les revenus des TITRES (actions, parts sociales, revenus réputés distribués, obligations) :
- Droit commun : **15 %** (porté à **17 %** pour les bénéficiaires personnes physiques) — dividendes ordinaires, lots d'obligations, distributions de bénéfices exonérées de BIC ou n'ayant pas supporté le BIC au taux art. 64.
- **10 %** dividendes régulièrement mis en paiement par les sociétés cotées à la **BRVM** (porté à **12 %** pour les personnes physiques).
- **2 %** produits, lots et primes de remboursement des **obligations émises en CI remboursables en 5 ans au moins** (porté à **3 %** personnes physiques).
- Exonérations (Art. 211-236 bis) : produits d'obligations versés à des PM non établies dans l'UEMOA ou PP domiciliées hors UEMOA (Art. 236) ; augmentations de capital par incorporation de réserves (Art. 226 al. 2-3).

**IRC (Art. 192 et s. ; taux Art. 193)** — retenue à la source sur les revenus des PRÊTS et créances (intérêts/arrérages des créances ayant le caractère juridique d'un prêt, dépôts d'argent, cautionnements en numéraire, comptes courants, emprunts NON obligataires) :
- Droit commun : **18 %**.
- Comptes de dépôts : particulier **1 % à 13,5 %** selon la durée du dépôt ; entreprise **1 % à 16,5 %** selon la durée.
- Comptes courants (dont CCA) : particulier **13,5 %** ; entreprise **16,5 %**.
- Exonérations : intérêts de comptes courants inclus dans les recettes d'une profession industrielle/commerciale/agricole (double condition Art. 216) ; créances commerciales ; prêts des associations à leurs membres ; comptes d'épargne populaire ; zones CNO (8 ans).

**Clé de distinction** : titre négociable (action/part/obligation) → IRVM ; simple créance/prêt/dépôt → IRC. Les obligations relèvent de l'IRVM (jamais de l'IRC) ; le compte courant d'associé relève de l'IRC (13,5 %/16,5 %) côté bénéficiaire ET de l'art. 18-A (4 limites de déductibilité) côté société.

## CODE DES INVESTISSEMENTS 2018 — paramètres exacts (source : Ord. 2018-646 du 01/08/2018, OCR intégral juillet 2026 ; ⚠️ vérifier Ord. 2024-857 modificative avant tout dossier)

- **Exclusions (art. 6)** : commerce ; banques/finance ; bâtiment à usage non industriel ; professions libérales.
- **Catégorie 1 (art. 5)** : agriculture, agro-industrie, santé, hôtellerie (hôtellerie cat. 1 si invest ≥ 5 Mds zone A / ≥ 2 Mds zones B-C ; en dessous → cat. 2). **Catégorie 2** : tout le reste non exclu.
- **Zones** : A = district d'Abidjan ; B = chefs-lieux de région + Bonoua + Grand-Bassam ; C = reste.
- **Régime de DÉCLARATION (art. 10-12)** : créations uniquement, avantages en phase d'exploitation. Cat. 1 : zone A 5 ans à 50 % ; zone B 10 ans (100 % ans 1-5, 50 % ans 6-10) ; zone C 15 ans (100 % ans 1-10, 75 % ans 11-15) — sur BIC+IMF, patente, CE (nationaux, HORS TA/TFPC), IPF (+ IRVM dividendes des actionnaires NATIONAUX en zones B/C). Cat. 2 : crédits d'impôt = % des montants investis — A 25 %, B 35 %, C 50 % — imputables sur BIC+IMF, patente, IPF, TVA, CE emplois locaux, **jusqu'à remboursement complet**. PME en déclaration = avantages de l'art. 18 (agrément-exploitation PME).
- **Régime d'AGRÉMENT (art. 13-18)** : création OU développement. Seuils : GE ≥ 200 M (hors TVA, hors BFR) ; PME ≥ 50 M ; grands centres commerciaux ≥ 10 Mds (A) / 5 Mds (B-C) ; projets structurants : 100/75/50 Mds (A/B/C).
  - **Phase d'implantation (art. 14-15)** : exonération droits de douane (sauf redevance statistique + prélèvements communautaires) + **suspension temporaire de TVA** sur matériels, équipements, 1er lot de pièces de rechange (plafonné à 10 % A / 20 % B / 30 % C de la valeur des équipements), services et travaux — subordonnée au certificat d'agrément (jamais commencer avant).
  - **Phase d'exploitation** : GE cat. 1 = mêmes barèmes que déclaration (5/10/15 ans, 50 / 100-50 / 100-75 %) ; GE cat. 2 = crédits 25/35/50 %. **PME cat. 1** : A 5 ans à **75 %** ; B 10 ans (100 % puis 75 %) ; C **15 ans à 100 %** — TOB en plus dans le champ. **PME cat. 2** : crédits **37,5 % (A) / 52,5 % (B) / 75 % (C)**.
- **Multizone (art. 16)** : pour l'impôt sur les bénéfices, avantage de la zone où l'investissement est le plus élevé.
- **Contenu local (art. 21-22, GE étrangères)** : +2 % de crédit d'impôt par volet — encadrement ivoirien ≥ 80 % ; sous-traitance nationale ≥ 25 % ; ouverture du capital ≥ 15 % à des nationaux (secteurs par décret). Cat. 1 : applicables après la période d'exonération totale.
- **Hôtellerie / centres commerciaux (art. 23)** : montage à deux têtes admis — société d'infrastructure (avantages phase implantation + exo IPF en exploitation) + société d'exploitation (avantages exploitation), chacune devant investir et être agréée.
- **Projets structurants (art. 19-20)** : convention d'État négociée via CEPICI, avantages additionnels sur mesure.
- **Jamais exonérés par le Code** : TA + TFPC (FDFP), redevance statistique, prélèvements communautaires, TSE ; et la **taxe de voirie 2 % de la VL frappe précisément les exonérés d'impôt foncier** (art. 166 CGI).

## FISCALITÉ MINIÈRE CI — paramètres exacts (sources : Loi 2014-138 Code minier ; Ord. 2014-148 ; Décret 2014-632 ; OCR intégral juillet 2026)

- **3 régimes d'exploitation** : artisanale (méthodes traditionnelles, ni chimie ni explosifs — réservée aux PP ivoiriennes) ; **semi-industrielle** (méthodes simples et peu mécanisées) ; industrielle (moderne, mécanisée, = permis d'exploitation, ≤ 20 ans renouvelable 10).
- **Autorisation semi-industrielle (art. 52-56)** : arrêté du Ministre des Mines ; **réservée** aux PP ivoiriennes / coopératives à participation ivoirienne majoritaire / **PME de droit ivoirien à capital majoritairement ivoirien** ; durée **4 ans renouvelable** ; superficie **25 à 100 hectares** ; superficiaire **15 000 F/ha/an** (Ord. 2014-148 art. 8).
- **Taxe ad valorem** (Code art. 151-153 ; Ord. 2014-148 art. 5) — semi-industriel ET permis d'exploitation assujettis (art. 152) ; **assiette = CA − frais de transport (prix FOB) − frais d'affinage** ; payable **trimestriellement**. Barème OR selon cours de l'once USD : **3 %** (≤ 1000), **3,5 %** (1000-1300), **4 %** (1300-1600), **5 %** (1600-2000), **6 %** (> 2000). ⚠️ cours actuel > 2000 → **6 %**. Autres : argent/platine 4 % ; pierres précieuses/fines 3 % ; métaux de base (cuivre, manganèse, bauxite…) 3,5 % ; fer brut 3,5 % / enrichi 2,5 %. Diamant brut : PAS d'ad valorem.
- **Artisanale** : droit forfaitaire annuel **20 000 F/ha/an** (Décret 2014-632 art. 6).
- **⚠️ Exonération IS/IMF de 5 ans (Code art. 169-e) = RÉSERVÉE au titulaire du PERMIS d'exploitation (industriel)**. Le **semi-industriel paie l'IS/BIC de droit commun 25 % + IMF** dès le 1er franc — piège classique.
- **Phase recherche (art. 162-163)** : exonération droits de douane + TVA sur matériels du programme agréé (pièces ≤ 30 % CAF) ; exonération IS, IMF, impôts fonciers, droits d'enregistrement des apports — pour le titulaire **ET ses sous-traitants agréés**.
- **Sous-traitants miniers** : les avantages douaniers (admission temporaire art. 156 ; exo matériels recherche art. 162 ; **exo carburants/lubrifiants/produits chimiques + admission temporaire 3 ans art. 166** ; effets perso expatriés 1 an art. 167) ne profitent qu'aux **sous-traitants AGRÉÉS par l'Administration des Mines**. Non agréé = droit commun total. Le sous-traitant reste dans tous les cas soumis à l'**IS de droit commun sur ses bénéfices** (les faveurs sont douanières, pas sur le résultat). Contrats de sous-traitance à communiquer à l'Administration des Mines.
- **Autres (permis exploitation)** : exo IPF bâti/non bâti (pas IRF ni voirie), exo patente sur extraction/vente (PAS la transformation), exo TSE, **IRC réduit de moitié** sur prêts > 3 ans (art. 170). Réhabilitation : **compte séquestre obligatoire** (art. 144-148), alimentation = charge déductible BIC. Recettes de vente : **rapatriement obligatoire** (changes, art. 172) ; or brut : poinçonnage 80 F/g.
- **Mines = EXCLUES du Code des Investissements 2018 ET de l'art. 110 CGI** (régime autonome, pas de cumul). Carrières, elles, relèvent du Code des Investissements (art. 171).
