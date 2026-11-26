---
name: dossier-ave-maria-ecomaf
description: Suivi AVE MARIA TRANSIT CI (future TRACE LOGISTICS CI) & ECOMAF — état au 30/09/2026, livrables, chiffres de référence, points ouverts
metadata:
  type: project
---
Mission de suivi AVE MARIA TRANSIT CI (NCC 0901858J, TEE, CA déclaré 5 000 001) + ECOMAF (NCC 230566Y, rejeté par la FNE), contrat MC-CONT-SUIVI-2026-001. Dossier commercial dans `DOSSIER CLIENTS/TRACE LOGISTICS/SUIVI CI & ECOMAF/`, travaux dans `DOSSIER CLIENTS/AVE MARIA TRANSIT/SUIVI_2026-09/` (sources et scripts dans `_SOURCES_MD/`).

Livrables du 30/09/2026 : contrôle de la fiche (MC-DT-SUIVI-2026-001), note de traitement (MC-TRT), DEE 23 points (MC-DEE, non envoyée), base comptable reconstituée 2026 + cartographie + état des appros/prêts inter-entités (MC-REC-SUIVI-2026-001), directive débours (MC-DIR-DEB-2026-001), analyse des relevés + états de rapprochement (MC-ARB-SUIVI-2026-001), exposition au redressement + plan de régularisation (MC-EXPO-SUIVI-2026-001 : A 548,4 M / B 330,2 M / C 16,6 M ; ECOMAF 132,7 M).

Chiffres de référence (source = onglet RECAP de la fiche, pas les onglets mensuels) : débours 4711 = 342 260 226 ; fonds TRACE LOGISTICS BF = 575 000 000 ; bilan de situation 30/09 = 494 023 236 après qualification QUAL-01 à 04 et ventilation des comptes courants CC-01 à 03 (515 439 774, tous créditeurs ; 50 M en 466100 ECOMAF ; 40 M en 471300 à justifier) (fonds TRACE BF = provisions 4191, 3 notes de débours mensuelles, excédent 232 739 774 en 462110) ; capitaux propres d'ouverture −1 617 000 (EF 2025 mal classés) ; doublon caisse 18 500 000 (COR-13).

**Deux entités distinctes** (consigne du gérant, 30/09/2026) : une base comptable PAR société, jamais une base commune. Dossier `SUIVI_2026-09/` organisé en `0_DOCUMENTS_COMMUNS`, `1_AVE_MARIA`, `2_ECOMAF`, `3_OPERATIONS_ENTRE_AVE_MARIA_ET_ECOMAF`, `_OBSOLETE`. Fonds TRACE BF = provisions sur débours ; solde non consommé 232 739 774 → convention CONV-04 si non justifié ; conventions CONV-01 à 05 en projet. Chaîne 34 517 419 ECOMAF → caisse AVE MARIA → droit de douane (à confirmer).

Exposition et DEE scindées par entité (MC-EXPO-AM/EC, MC-DEE-AM 27 points / EC 10 points). Kit débours : contrats-cadres MC-CTR-TR/EC-2026-001, modèles ordre de transit / note de débours / facture, registre des 550 débours. Analyse des sorties MC-SORT-AM-2026-001 (749,3 M, 53 % en espèces ; 44,9 M exposés à réintégration) ; commission recommandée coût + 10 % = 44 635 945 (non comptabilisée avant validation de la marge). Manuels MC-MAN-BP-2026-001 et MC-MAN-PROC-AM-2026-001 dans 1_AVE_MARIA/MANUELS. Tableau de bord HTML à la racine de SUIVI_2026-09.

**Why:** la note de conformité T3 dépend des réponses à la DEE et du contrat de transit avec TRACE BF.
**How to apply:** repartir de `build_base.py` (regénère tout) ; vérifier la cohérence avec `controle_coherence_dossier.py` après chaque modification.

Mise à jour 30/09/2026 : la direction a retenu la commission de transit AVE MARIA au **coût majoré de 5 %** = 42 607 039 (coûts 40 578 132 × 1,05 ; 3 FNE FC-TR-2026-07/08/09 au 706100, COM-01/COM-02 imputées sur 462110). Résultat 30/09 +2 028 907 ; CP 411 907 (< ½ capital, Art. 371) ; CC TRACE BF 190 132 735 (CONV-04) ; CC total 472 832 735 ; base AM 2 057 lignes, bilan 494 023 236. Contrat-cadre Art. 7 fixé à coûts + 5 %. Grands livres séparés produits (GRAND_LIVRE_AVE_MARIA_2026 / _ECOMAF_2026, xlsx + PDF paginé, build_gl.py). Réintégration : assiette brute 44 908 380, base réintégrable 23 487 622 (≈5,9 M IBIC au réel).

Mise à jour 30/09/2026 (suite) : **ECOMAF 2S est la filiale à 100 % d'ECOMAF BURKINA** (information de la direction). Les 100 M reçus de la mère le 31/08 sont reclassés en 462100 compte courant de l'associé unique (QUAL-EC-01, convention CONV-06 à signer) ; bilan EC inchangé 193 266 204, 110 lignes. Transferts USD : 83 017 970 financés avant l'arrivée des fonds de la mère (argent TRACE BF + AVE MARIA, FIFO), 88 271 698 par la mère. Exposition EC scénario B ramenée à 36 888 866 (mère + AVE MARIA reconnus). Hypothèse retenue par l'Agence : mandat d'achat pour la mère, commission coûts + 5 % (8 120 381 sur coûts connus). Nouveaux livrables EC : analyse des sorties (MC-SORT-EC-2026-001), contrat de mandat d'achat (MC-CTR-MERE-EC-2026-001), manuel de procédures (MC-MAN-PROC-EC-2026-001), grands livres et balances générales des deux sociétés, rapport explicatif simple (MC-EXPL-2026-001). Lien de capital AVE MARIA ↔ ECOMAF 2S non établi : si absent, prêt 50 M en 2748/1688 et risque de monopole bancaire.

Précision de la direction (30/09/2026) : les 19 bons de caisse CAISOP du 03/07 au 13/07/2026 (19 416 752, « Sur chargement », route, pesage, syndicat) portent la référence « ECOMAF » dans la fiche Sage, mais **ce sont des débours d'AVE MARIA** (refacturés à TRACE BF), pas des opérations d'ECOMAF. Ne pas les réaffecter. La fiche Excel du client ne contient ni ventes ni dépenses d'ECOMAF : ECOMAF n'a que son relevé bancaire.

**Constat du profil de conformité (02/10/2026), vérifié sur les pièces :** ces deux éléments contredisent les livrables du 30/09 et sont à arbitrer.
- **TEE 2025 et 2026 :** elles sont PAYÉES par mobile money le 20/04/2026, d'après l'historique e-impôts (T2.pdf), où toutes les lignes sont « Payé ». La base (446000 à 500 000), l'anomalie F-1, le point R7 et la DEE les donnent pourtant impayées.
- **DFE du 12/05/2026 (changement de gérance) :** elle indique une SARLU au capital de 25 000 000, alors que 1 500 000 est comptabilisé, avec le RCCM CI-ABJ-03-2026-M-19804. L'associée unique est Mme M'BRA AYA ALINE et le signataire COMPAORE HALIDOU, gérant.
- **Conséquence :** les apporteurs inscrits en 462 ne seraient pas associés. Ce serait alors des avances de tiers, avec un risque de monopole bancaire, et les conventions CONV-01 à 04 seraient à revoir.

**Profil ECOMAF 2S (02/10/2026) :** l'hypothèse « mandataire » (M3) ne tient pas en l'état, avec un score de 1/12.
- **Les faits :** les 11 domiciliations d'import sont au nom d'ECOMAF 2S, le mandat est postérieur aux achats, et 83 M ont été payés avant l'arrivée des fonds de la mère.
- **Qualification probable :** commissionnaire (CGI art. 342), avec un CA d'au moins 178,9 M. À arbitrer par le Superviseur avant la signature du mandat.
- **NCC :** 230566Y n'a que 6 chiffres, ce qui explique probablement le rejet par la FNE.

**TRACE LOGISTIC(S) SARL :** c'est une 3e entité, ivoirienne (NCC 2404990E, mission ORD-2026-0022), distincte de TRACE BF et d'AVE MARIA. Elle serait l'émettrice probable des 51,5 M reçus par AVE MARIA le 03/06, ce que contredisent les livrables qui la disent « non constituée ». Deux sociétés du groupe déclarent exactement 5 000 001 à la TEE, d'où un risque de fractionnement.

Le 05/10/2026, l'Agence a revu les conventions préparées par l'équipe (avis MC-AVIS-CONV-AM-2026-001, dans 1_AVE_MARIA/CONVENTIONS_COMPTES_COURANTS/REVUE_EQUIPE_2026-10-05).

**Conventions de l'équipe :** COMPAORE 100 M ; TRACE LOGISTICS CI 101,5 M (gérante TRAORE Aminatou Nafony, RCCM CI-ABJ-03-2024-B12-09555) ; TRACE BF 515 M présentés comme un prêt de trésorerie.

**Avis de l'Agence :** les fonds TRACE BF sont des avances pour les travaux de transit faits en Côte d'Ivoire (provisions 4191, débours, commission), et non un prêt. La convention ne doit porter que sur le solde non consommé.

**Faits relevés :**
- Les vrais virements burkinabè portent la référence « BF148 01029 » : 15 virements, 435 M.
- Le virement de 100 M du 21/05 (« VRT RECU TRACE LOGISTICS ») est de format domestique. Il vient probablement de TRACE CI. S'il est confirmé, le solde dû à TRACE BF passe de 190 132 735 à 90 132 735. L'avis de crédit CORIS est à obtenir.
- Selon les conventions de l'équipe, AMT-CI est une SARLU au capital de 25 M (RCCM CI-ABJ-03-2026-M-19964), avec M. COMPAORE associé unique. La base de l'Agence retient 1,5 M de capital : écart à vérifier sur les statuts.
- Les conventions de l'équipe sont datées du 21/04 et du 03/05/2026, avant les versements qu'elles constatent : elles seraient lues comme antidatées.

**Jeu de conventions corrigées (05/10/2026)**, dans 1_AVE_MARIA/CONVENTIONS_COMPTES_COURANTS (préfixes 00 à 05) et dans la transmission 02_OBJECTIF_2_CONVENTIONS/CONVENTIONS_CORRIGEES_2026-10-05 :
- 00 note à l'équipe MC-NOTE-CONV-AM-2026-002 ;
- 01 contrat-cadre TRACE BF MC-CTR-TR-2026-001-R, avec le relevé de compte : 475 M d'avances certaines + 100 M conditionnels, débours 342 260 226, commission 42 607 039 ;
- 02 CONV-04R solde TRACE BF 190,1 ou 90,1 M, optionnelle, sous condition d'un lien de capital ;
- 03 CONV-01R COMPAORE ;
- 04 CONV-02R TRACE CI, conditionnelle au lien de capital ;
- 05 rapport source corrigé : total dû 391 632 735 dans les deux hypothèses.

L'ancienne CONV-03 (BACI) est retirée. Les anciennes CONV-01 à 04 sont dans _OBSOLETE.

CONV-01R est bloquée tant que les statuts n'ont pas tranché qui est l'associé unique (M. COMPAORE ou Mme M'BRA). Si ce n'est pas M. COMPAORE, il faut une convention de prêt du gérant.

**Pièces annexes et note de traitement (06/10/2026)**, numérotées 06 à 13 dans CONVENTIONS_COMPTES_COURANTS :
- 06 note comptable et fiscale MC-NOTE-TFC-AM-2026-001 ;
- 07 lettre de choix TRACE BF ;
- 08 attestations des remises d'espèces ;
- 09 état de calcul des commissions (au prorata des débours) ;
- 10 décisions de l'associé unique ;
- 11 convention de prêt du gérant ;
- 12 lettre à CORIS ;
- 13 demande de pièces.

La base du 30/09 range encore en 462 TRACE BF (462110), TRACE CI, BACI et le financement 2025. Les reclassements REG-CONV-01 à 04 (372 832 735) sont proposés vers 419110 et 4712, mais **pas encore passés dans la base**. Le compte 471100 garde un solde de 572 300 de débours non refacturés.

**Faits juridiques établis le 06/10/2026** (pièces dans `Downloads/03_AUTRES/reradiationtracelogisticsetchangementdedenomination/`) :
- Mme MBRA a cédé 100 % des parts (2 500 parts, 25 000 000) à M. COMPAORE par acte notarié du 21/05/2026 (Me FOFANA). Les droits de 1 % (250 000) ont été payés le 15/06.
- **M. COMPAORE est donc l'associé unique** depuis le 21/05/2026.
- RCCM : CI-ABJ-01-2008-B13-03552, modifié sous CI-ABJ-03-2026-M-31380 (20/07/2026). Les numéros M-19964 et M-19804 sont faux.
- Passeport selon l'acte : A5009209.

**Points ouverts :**
- Aucune sortie d'AVE MARIA ne correspond au prix de 25 M ni aux frais : il faut le reçu du notaire et un relevé personnel de M. COMPAORE.
- La libération du capital de 25 M (statuts du 26/03/2026) n'est pas prouvée, alors que la base porte 1,5 M.
- L'article 6 des statuts parle à tort d'un « apport » de M. COMPAORE.

**Règles fiscales vérifiées dans le CGI 2026** (texte : `Documents/FORMATION LMDC/00_TEXTES_OFFICIELS/CGI_2026_TEXTE_INTEGRAL.txt`) :
- art. 852-4 : timbre de 1 % sur les sommes mises à disposition par un associé ou une autre société ;
- art. 854 : délai de 30 jours après l'opération ;
- art. 823 : amende égale au droit, soit 100 % ;
- art. 835 : timbre de dimension de 1 000 F par page A4 ;
- art. 554-7 et 703-20 : enregistrement des marchés dans le mois, droit fixe de 25 000.

Chiffrage : AVE MARIA 4 129 000 certains, ECOMAF 3 099 000. La convention de l'équipe à 515 M aurait coûté 10,3 M.

**Livrables du 06/10/2026 :**
- note fiscale du timbre (DET), note sur le rachat ;
- courrier de demande des pièces des débours et son annexe de 550 lignes ;
- historique des approvisionnements (856,5 M d'apports extérieurs) ;
- matrices de contrôle M1 à M10 ;
- versions Word à signer, sans encadrés internes ni en-tête MDC (`build_versions_a_signer.py`).

**Rangement du 06/10/2026, après relecture contradictoire.**

Le dossier `1_AVE_MARIA/CONVENTIONS_COMPTES_COURANTS/` est organisé en quatre parties :
- **1_DEFINITIF**, en six sous-dossiers :
  - 1_LIRE_D_ABORD ;
  - 2_A_SIGNER, avec les Word sans en-tête MDC ;
  - 3_NOTES_ET_CALCULS ;
  - 4_COURRIERS_A_VALIDER ;
  - 5_CONTROLES ;
  - 6_PIECES_JURIDIQUES_RECUES ;
- **2_DOCUMENTS_DE_TRAVAIL**, avec les versions annotées ;
- **REVUE_EQUIPE_2026-10-05** ;
- **_OBSOLETE**.

Le dossier de transmission contient `02_OBJECTIF_2_CONVENTIONS/CONVENTIONS_DEFINITIVES_2026-10-06`. Les scripts build_* écrivent directement dans 1_DEFINITIF.

**Chiffrage révisé du timbre pour AVE MARIA :**
- 2 068 000 de droits certains ;
- 7 900 654 avec les risques probables, identique dans les deux hypothèses : TRACE CI 2 030 000 et solde TRACE BF utilisé depuis juin 3 802 654 ou 1 802 654 ;
- 9 524 654 au maximum.

L'écriture de constatation du timbre (6462 et 6478 au débit, 4428 au crédit, risques probables en provision 19) **n'est pas passée** et attend la validation du Superviseur. Avec les seuls droits certains, le résultat tomberait à +28 907.

**Point clé ouvert :** à qui appartient le dépôt de 170 M du 15/06 (caution d'agrément) ? C'est l'article 10 du contrat-cadre, option (i) ou (ii). La réponse fixe le solde dû à TRACE BF et le timbre correspondant.

**Mise à jour de la base du 06/10/2026, sur instruction du gérant** (`apply_maj_base_2026-10-06.py`).

Trois séries d'écritures :
- COR-TEE : la TEE 2025 et 2026 (500 000), payée le 20/04 par mobile money, est soldée en contrepartie du compte 471250 (payeur à justifier) ;
- TIM-01 : 2 000 000 de timbre et d'amende pour M. COMPAORE, en dette 442800 ;
- PROV-01 : 2 030 000 de provision 191100 pour TRACE CI.

Le solde TRACE BF n'est pas provisionné : il dépend de la propriété du dépôt.

Résultats après mise à jour :
- 2 073 lignes au journal ;
- bilan inchangé à 494 023 236 ;
- résultat : perte de 2 001 093 ;
- capitaux propres : −3 618 093, sous la moitié du capital (AUSCGIE art. 371).

Le rapport à la direction MC-RAP-DIR-AM-2026-001 est dans `1_DEFINITIF/1_LIRE_D_ABORD`.

L'origine du virement de 100 M du 21/05 (TRACE BF ou CI) reste **non confirmée** : le gérant a d'abord dit « TRACE CI », puis s'est rétracté et va demander la confirmation. Les deux hypothèses sont conservées.

**Changement de schéma décidé par la direction le 08/10/2026.**

La direction a tranché :
- les fonds reçus sont des **financements**, et non des avances sur débours ;
- les **débours payés par AVE MARIA sont ceux d'ECOMAF 2S**, importateur en Côte d'Ivoire.

L'étude définitive MC-ETU-DEF-AM-2026-001 et son classeur `build_etude_definitive.py` sont dans `1_DEFINITIF`.

**Montants établis par la banque :**
- financement TRACE BF → AVE MARIA : 475 M, plus 100 M conditionnels pour le virement du 21/05 ;
- financement TRACE CI → AVE MARIA : 101,5 M ;
- compte courant COMPAORE : 100 M ;
- prêt AVE MARIA → ECOMAF 2S : 50 M ;
- **financement TRACE BF → ECOMAF 2S : 50 M** (22/07, références 786394 et 786395) ;
- compte courant ECOMAF BURKINA → ECOMAF 2S : 100 M.

**Débours d'ECOMAF 2S (342 260 226) :**
- 53 934 171 établis : 19 bons marqués ECOMAF pour 19,4 M, plus le droit de douane de 34 517 419 qui correspond au virement d'ECOMAF du 03/08 ;
- 288 326 055 à prouver par les 11 domiciliations (n° 11067 à 11446).

**Conséquences :**
- ECOMAF 2S supporte un coût d'importation de 563,8 M, à couvrir par des ventes ou une refacturation à sa mère ;
- le timbre d'AVE MARIA monte à 15,53 M, soit un complément de 11,5 M à constater ;
- celui d'ECOMAF 2S est de 4 M.

La référence « BF148 01029 » marque tout virement venu du Burkina, y compris ceux d'ECOMAF BURKINA : ce n'est pas un code propre à TRACE BF.

**En attente de validation :** la rédaction des nouvelles conventions et la mise à jour des deux bases. L'ancien contrat-cadre avec TRACE BF et CONV-04R sont devenus sans objet.

**Dossier séparé ouvert le 08/10/2026 :** le détachement des salariés de TRACE BF en Côte d'Ivoire (CIPRES et impôt sur les salaires), confié à un agent. Brouillons dans `scratchpad/detachement`.

**Conventions du schéma « financements », rédigées le 08/10/2026.** Elles sont dans `1_DEFINITIF/2_A_SIGNER`, et leurs versions annotées dans `2_DOCUMENTS_DE_TRAVAIL`. Les sources sont dans `_SOURCES_MD`.

Sept actes :
- CONV-FIN-01 : financement TRACE BF → AVE MARIA, 475 M, plus [100 M] conditionnels ;
- CONV-FIN-02 : financement TRACE CI → AVE MARIA, 101,5 M, plus [100 M] conditionnels ;
- CONV-01R : compte courant COMPAORE, 100 M ;
- contrat de transit AVE MARIA ↔ ECOMAF 2S (MC-CTR-EC-2026-001-R) : débours de 342 260 226, dont 53,9 M établis et 288,3 M à rattacher aux domiciliations, avec une clause de rattachement ; commission de 42,6 M facturée à ECOMAF ;
- CONV-05R : prêt de 50 M ;
- CONV-FIN-03 : financement TRACE BF → ECOMAF 2S, 50 M ;
- CONV-06R : compte courant de la mère, 100 M.

**Chiffres d'ensemble :** total de 1 361 367 265 ; droits d'environ 19,76 M, dont 9 765 000 de timbre et 9 765 000 de pénalités.

Notes associées : présentation MC-NOTE-CONV-FIN-2026-001, détail des opérations MC-DET-OPE-AM-2026-001.

**Archivage :** les documents de l'ancien schéma sont dans `_OBSOLETE/SCHEMA_AVANCES_POUR_TRAVAUX_2026-10-06`. Les matrices de contrôle sont encore établies sur l'ancien schéma.

**Base comptable :** mise à jour le 08/10/2026 (script `_SOURCES_MD/apply_maj_base_2026-10-08.py` : ANN-COM, REG-FIN-01/02, TIM-02, REP-PROV). Résultat −56 108 132, capitaux propres −57 725 132, bilan 836 283 462.

**Commission : AUCUNE.** Décision du 08/10 : AVE MARIA n'a facturé aucun client, la commission n'est pas déterminable. Total des conventions 1 318 760 226 ; somme due par ECOMAF 2S = débours 342 260 226 ; rémunération « [À DÉTERMINER PAR LES PARTIES] ».

**Espèces :** le demandeur a des réserves sur les sorties en espèces ; ne rien requalifier. Politique MC-POL-ESP-AM-2026-001 (CGI art. 18 bis, exception mobile money de la loi 2025-987 ; 107 frais Wave dans les débours).

**Détachement des salariés de TRACE BF :** cinq projets publiés dans `0_DOCUMENTS_COMMUNS/DETACHEMENT_SALARIES_TRACE_BF_2026-10-08`.
- Sécurité sociale : la convention CIPRES prévoit l'affiliation dans le pays de travail (art. 10). Le détachement est limité à 6 mois prévisibles, avec un certificat FCC-01 (art. 11-1°).
- Impôt : règlement UEMOA 08/2008, art. 16-2. L'exception joue pour un séjour de 183 jours au plus dans l'année fiscale, avec un employeur non résident et sans établissement stable en Côte d'Ivoire.
- Ces projets sont à faire valider par l'équipe Juridico-Fiscal.
- 08/10/2026 : rapport détaillé de mission destiné à la direction des deux sociétés (MC-RAP-CLI-AM-2026-001, 19 pages, PROJET à valider par le Superviseur avant remise), dans 1_DEFINITIF/1_LIRE_D_ABORD.
- 08/10/2026 : rapport de diagnostic MC-RAP-DIAG-AM-2026-001 (14 p) + classeur MATRICES_ANOMALIES_EXPOSITION_REDRESSEMENT_2026-10-08.xlsx (script `_SOURCES_MD/build_matrices_anomalies_exposition.py`). Version finale sans commission : 43 anomalies (AMT 29, ECOMAF 14). Exposition 21,23 M / 122,06 M / 753,52 M (plafond). Notes de départ : AMT CCC (5,40), ECOMAF BB (12,00). Seuil cible de la note méthodologique : 30 000 FCFA. Le demandeur a refusé toute mention de la remise gracieuse des pénalités dans le rapport ; retirée le 08/10 du rapport, de la note de présentation et de CONV-06R. Ne plus la proposer.
- 08/10/2026 (suite) : procédure des débours MC-PROC-DEB-AM-2026-001 (4_COURRIERS/19) ; profils des sociétés et de la relation MC-PROF-AM-EC-2026-001 et note TVA import ECOMAF MC-NOTE-TVA-IMP-EC-2026-001 (3_NOTES/20, 21 ; TVA au port estimée ≈ 42 M, fourchette 38-50 M, incluse dans 100 324 032 de liquidations) ; dossier de paiement des droits MC-DOS-ENR-AM-2026-001 (4_COURRIERS/22 : 19 747 000 = AMT 15 658 000 + ECOMAF 4 089 000) ; recueil des actes à signer 2_A_SIGNER/00 (script build_recueil_conventions.py). Indices de transit vers le Burkina dans les débours (RSE douane Burkina, SITARAIL, BTA) et débours « ECOMAF » dès le 03/07, avant l'ouverture du compte d'ECOMAF 2S (21/07) : à faire confirmer.
- 08/10/2026 (version exacte) : 21/05 rattaché à TRACE CI (CONV-FIN-02 = 201 500 000 ; CONV-FIN-01 = 475 000 000 ; REG-FIN-03 en base) ; compte courant COMPAORE 100 000 000 ; remboursements sans date, initiés sur demande, dans la limite de la trésorerie (y compris comptes courants CONV-01R et CONV-06R : préavis et blocage supprimés) ; COMPAORE associé de TRACE CI (% à compléter), gérant mais non associé de TRACE BF → financements TRACE BF déclarés occasionnels ; prêt AMT→ECOMAF = avance à un cocontractant (loi bancaire 34-1), sans intérêt ; clause de rattachement des débours au 31/12/2026 (elle était perdue dans la version à signer, rétablie). Script apply_version_exacte_conventions.py.
- 09/10/2026 : rapport mensuel MC-RAP-MENS-AM-2026-001 (0_DOCUMENTS_COMMUNS/RAPPORTS_MENSUELS), classé COMPTABILITÉ / FISCALITÉ / SOCIAL. Faits du mois apportés par le gérant : accès FNE obtenus par le département informatique (tests par les développeurs de TRACE BF) ; états financiers de TRACE LOGISTICS déposés et ARF obtenue ; publication de la radiation déposée (entité non précisée) ; 11 contrats de travail ; CNPS déposée le 06/10, RDV 20/10. État trimestriel commissionnaire T3 dû le 15/10/2026.
- **Correction du gérant (09/10/2026)** : la base d'AVE MARIA a été **reconstituée à partir des EF 2025** (ouverture) ; la **base 2026 est en cours de stabilisation** (ne pas la dire « achevée »). Pour ECOMAF 2S, l'Agence a **créé la base comptable de l'exercice 2026** (pas une reconstitution à partir d'EF 2025).
- 12/10/2026 : lancement des formalités AVE MARIA à l'Inspection du travail (note MC-NOTE-IT-AM-2026-001, 1_AVE_MARIA/SOCIAL) : déclaration d'entreprise + reprise d'activité (décret 96-209), visa du registre d'employeur (CT art. 92.3) ; ensuite règlement intérieur (décret 96-197, >10 salariés) et élection d'1 délégué + 1 suppléant (11 à 25 salariés). Code du travail 2015 archivé en local : FORMATION LMDC/00_TEXTES_OFFICIELS/CODE_DU_TRAVAIL_2015_TEXTE.txt.
- **Précisions du gérant (09/10/2026)** :
  - « TRACE LOGISTICS CI » **n'existe pas encore** : c'est le futur nom d'AVE MARIA, dont M. COMPAORE détient 100 %. La société d'Abidjan qui a viré 101,5 M (« SOCIETE TRACE LOGIST CI », NCC 2404990E, gérante Mme TRAORE) est une autre entité — ses associés sont inconnus : la clause « COMPAORE associé du Financeur » de CONV-FIN-02 est donc à revoir.
  - ECOMAF 2S : dénomination corrigée sur e-impôts (le nom de TRACE y apparaissait). Changement de régime suspendu à la demande de Mme KABORE ; l'Agence veut rouvrir la discussion (plus de 280 M de frais engagés par AVE MARIA → seuil dépassé ; ~42 M de TVA import récupérables). Ne pas citer le Doyen MAN ZIO dans les livrables (mention de briefing interne).
  - Paie AVE MARIA : bulletins régularisés après réception du numéro CNPS ; Inspection du travail (visites médicales) après l'immatriculation.
  - Comptabilité AVE MARIA : l'équipe établit les matrices d'anomalies sur les données produites par le comptable du client.
  - Rapport mensuel : pas de calendrier (il suivra les directives de la direction).
- 09/10/2026 (fin) : **TRACE LOGISTICS (Abidjan)** (NCC 2404990E, gérante Mme TRAORE Aminatou Nafony) n'a **pas** M. COMPAORE pour associé (confirmé). CONV-FIN-02 : financement occasionnel, convention non réglementée ; le financeur est nommé « TRACE LOGISTICS (Abidjan) » / « TRACE Abidjan » dans tous les livrables (plus jamais « TRACE CI », réservé au futur nom d'AVE MARIA). Base : compte 471220 relabellisé. Fichier à signer : A_SIGNER_02_CONVENTION_FINANCEMENT_TRACE_ABIDJAN_AVE_MARIA.
- 09/10/2026 : dossier de transmission à la direction d'AVE MARIA : SUIVI_2026-09/TRANSMISSION_DIRECTION_AVE_MARIA_2026-10-09/ (+ .zip), 10 sous-dossiers 00 à 09, 69 fichiers, bordereau MC-BORD-AM-2026-001. Exclus : notes internes (profils, TVA import), courrier 13 et matrices de contrôle du 06/10 (ancien schéma), versions annotées. Non envoyé.
- 09/10/2026 : mention « Statut : PROJET… à valider par le Superviseur » retirée des 9 documents transmis à la direction d'AVE MARIA, sur décision du gérant (il valide lui-même). Les deux politiques portent « à adopter par décision du gérant ».
- 09/10/2026 : règlement intérieur (projet) + note de procédure MC-NOTE-RI-DP-AM-2026-001 + 9 modèles (élection du délégué sous supervision de l'inspecteur, décret 96-207 ; RI décret 96-197) dans 1_AVE_MARIA/SOCIAL/REGLEMENT_INTERIEUR_ET_DELEGUE_DU_PERSONNEL. Éligibilité : 12 mois d'ancienneté + nationalité ivoirienne ; électeurs 6 mois → si personne ne remplit, RI soumis à un travailleur désigné par ses pairs (CT 16.1). Rapport mensuel envoyable seul : SUIVI_2026-09/ENVOI_RAPPORT_MENSUEL_2026-10-09 (mention « documents détaillés en cours de traitement »).
- 09/10/2026 : le gérant indique que la rédaction a confirmé le rendu et que le Superviseur a validé les données du rapport mensuel (envoi autorisé par lui ; l'Agence n'envoie rien elle-même).
- 09/10/2026 : brouillon Gmail de transmission du rapport mensuel créé (compte lamaisondelaconformite@gmail.com), sans destinataire ni pièce jointe — à compléter et envoyer par le gérant.
- 09/10/2026 : brouillon Gmail « Transmission des documents détaillés » créé (sans destinataire ni pièce jointe ; joindre TRANSMISSION_DIRECTION_AVE_MARIA_2026-10-09.zip, 17,8 Mo). Le gérant a retiré du dossier les sous-dossiers 05 Comptabilité, 06 Politiques et 07-C AEJ : bordereau aligné.
- 09/10/2026 : rapport mensuel enrichi d'une partie « Les chiffres clés du mois » (A dépouillement : entrées AMT 856,5 M, sorties 714,2 M, débours 342,3 M par nature, flux ECOMAF ; B montant de chaque convention, total 1 318 760 226 ; C droits 19 747 000) + mention « le reste des documents est en cours de finalisation ». 9 pages.
- 09/10/2026 : synthèse d'une page des chiffres clés (Excel une feuille + PDF A4 paysage) dans ENVOI_RAPPORT_MENSUEL_2026-10-09 (script build_synthese_une_page.py) ; brouillon Gmail du rapport mensuel actualisé (chiffres + « le reste est en cours de finalisation » ; objet modifié par le gérant en « SEPTEMBRE 2026 », conservé).
- 09/10/2026 : synthèse d'une page = ACTIONS MENÉES EN SEPTEMBRE 2026 (18 actions : 7 achevées, 4 en cours, 6 en attente, 1 à engager), Excel + PDF, ENVOI_RAPPORT_MENSUEL_2026-10-09 (la synthèse des chiffres est archivée dans _OBSOLETE). Brouillon Gmail actualisé en conséquence. Le gérant parle du rapport comme celui de septembre.
- 09/10/2026 : rapport mensuel retitré « SEPTEMBRE 2026 » (période : septembre 2026, situation au 9 octobre ; fichiers RAPPORT_MENSUEL_ACTIONS_AGENCE_SEPTEMBRE_2026, anciens « OCTOBRE » archivés) ; message à faire passer : l'Agence a beaucoup travaillé en septembre → encadré d'ouverture « 18 actions… 64 mouvements bancaires, 550 débours, 7 conventions, 43 anomalies, 11 contrats, une vingtaine d'actes sociaux » ; mail réécrit dans ce sens.
- **Total des conventions = 976 500 000 (financements seuls)** — décision du gérant (09/10/2026) : les débours du contrat de transit (342 260 226) ne sont PAS comptés dans le total des conventions ; on les mentionne à part. Ne plus écrire 1 318 760 226. Corrigé partout (rapport mensuel, synthèse, note de présentation, détail, étude + classeur, rapport détaillé, sommaire, mail).
- 12/10/2026 : **Indice MDC recalculé** (méthode v1.0, période 2026, évaluation provisoire à valider par le superviseur général). Il remplace les notes CCC et BB du 08/10.
  - **AVE MARIA** : 20,9 sur 100, niveau Critique, Indice définitif (couverture 84,9 %). Six contrôles critiques sont non conformes : V01, F02, S01, S02, S03 et G01.
  - **ECOMAF 2S** : 16,9 sur 100, niveau Critique, Indice provisoire (couverture 64,3 %). Trois contrôles critiques sont non conformes : F01, F02 et G01. Les domaines des ventes et du social ne sont pas vérifiables.
  - **Commissaire aux comptes** : AUSCGIE art. 376, il faut dépasser 2 seuils sur 3 ; AVE MARIA n'en dépasse qu'un (le total du bilan), donc pas d'obligation.
  - **Fichiers** : dossier `0_DOCUMENTS_COMMUNS/INDICE_MDC_2026-10-12/` (évaluations JSON, résultats, classeur des 45 contrôles), produit par le script `_SOURCES_MD/build_indice_mdc_2026-10-12.py`.
- **14/10/2026** :
  - **Contrat de transit AMT–ECOMAF** : ne cite plus AUCUN montant. L'ancien art. 11 (somme due, tableau, rattachement) est remplacé par une clause courte « au cours de la collaboration, AMT gère et paie les débours, refacturés par notes de débours ; opérations passées incluses ». Art. 8 : relevé non signé par ECOMAF, note acceptée par son règlement. Art. 5 : factures fournisseurs au nom d'ECOMAF « aux soins d'AMT », pas d'espèces > 250 000. Art. 7 : AMT à la TEE, pas de TVA. Résultat : timbre 1 % (3 422 602) évité. Règle : ECOMAF ne signe jamais un solde dû.
  - **Acte n° 13** : mise à disposition gratuite d'un bureau AMT → TRACE BF + décision n° 5 (enregistrement CGI art. 552, 34 000). Dossier de paiement des droits : total général 19 781 000.
  - **Notes de débours** : modèle par dossier (KIT_DOCUMENTAIRE_DEBOURS) ; notes ND-EC-2026-07/08/09 générées (build_notes_debours_ecomaf_2026_07_09.py) mais **à NE PAS envoyer**.
  - **Doute majeur sur le schéma** : débours 342 M = 2× marchandises ECOMAF (171 M) ; 58 « chargements » ≈ 3,1 M (179 M) = camions longue distance probables ; dossiers TLNE/TLOD = numérotation TRACE. Hypothèse : AMT = antenne d'exécution à Abidjan du transit de TRACE BF vers le Burkina (retour possible au schéma du 30/09). Livrables : rapport MC-RAP-IMP-EC-2026-001 (3_OPERATIONS), DEE MC-DEE-AM-2026-003 (4_COURRIERS/23, réponse au 24/10), note interne provisoire MC-NOTE-PROV-AM-2026-001 (0_DOCUMENTS_COMMUNS/NOTES_INTERNES_AGENCE). Recommandation : suspendre CONV-FIN-01, CONV-FIN-03, contrat de transit et acte 13 jusqu'aux réponses.
  - Détachement TRACE BF : certificats FCC-01 (A_SIGNER 12), fiche procédure direction + support de réunion (risques, 6 interdits) dans DETACHEMENT_SALARIES_TRACE_BF_MISSION_ABIDJAN_2026-10.

**16/10/2026 — DFE de TRACE LOGISTICS (Côte d'Ivoire) reçue** (classée dans DOSSIER CLIENTS/TRACE LOGISTICS/PIECES_JURIDIQUES_TRACE_LOGISTICS_CI) : SARL, capital 25 M, RCCM CI-ABJ-03-2024-B12-09555, NCC 2404990E, TEE, transit et commissionnaire en douane depuis le 06/01/2025, siège Treichville Av. 4 Rue 18 B lot 142 îlot 44 ; gérante Mme TRAORE Aminatou Nafony ; associés **M. COMPAORE Halidou 60 %**, M. TRAORE Kassoum 40 %. ⇒ CONV-FIN-02 est une convention réglementée (actes 02 et 10 corrigés). Le gérant a aussi confirmé : M. COMPAORE est gérant de TRACE BF ET d'ECOMAF 2S (actes 04, 05, 06 réglementés ; acte 11 = décisions de l'associé unique d'ECOMAF 2S). Le rapport détaillé du 08/10 et le profil disent encore le contraire (à corriger).
