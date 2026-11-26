---
name: dispositif-lbc-ft
description: >
  SKILL DE LUTTE CONTRE LE BLANCHIMENT DE CAPITAUX, LE FINANCEMENT DU TERRORISME ET DE LA
  PROLIFÉRATION (LBC/FT/FP) de MDC — La Maison de la Conformité SARL. Construit, documente et
  audite le dispositif LBC/FT/FP d'une entité assujettie en Côte d'Ivoire et dans l'UMOA, adossé
  au CORPUS BCEAO ARCHIVÉ EN LOCAL et interrogeable au mot près : Loi uniforme LBC/FT/FP de mars
  2023 (en vigueur en Côte d'Ivoire par l'ordonnance n° 2023-875 du 23 novembre 2023), loi
  ivoirienne n° 2016-992 du 14 novembre 2016 (abrogée, historique), Recueil des textes chapitre VIII (151 p.),
  Recueil des textes bancaires UMOA volume I (1 047 p.), Instructions BCEAO 001, 002 et 003-03-2025,
  Instructions 007 à 010-09-2017, Directives UEMOA 07/2002, 04/2007 et 02/2015, Guide du dispositif
  LBC/FT dans l'UEMOA. Déclenche ce skill dès que l'utilisateur parle de : blanchiment, LBC/FT,
  LBC/FT/FP, CENTIF, déclaration de soupçon, bénéficiaire effectif, KYC, connaissance du client,
  vigilance, vigilance renforcée, personne politiquement exposée, PPE, gel des avoirs, sanctions
  financières ciblées, approche fondée sur les risques, cartographie des risques de blanchiment,
  conformité, compliance officer, responsable anti-blanchiment, manuel LBC, procédures anti-blanchiment,
  assujetti, EPNFD, prestataire de services d'actifs virtuels, seuil espèces, transport physique
  d'espèces, fiducie, trust, construction juridique, love money, origine des fonds, GAFI, GIABA ;
  « suis-je assujetti », « dois-je déclarer », « comment monter le dispositif », « fais-moi le manuel
  LBC », « audite ma conformité anti-blanchiment », « quel seuil pour les espèces », « que faire de
  ce client ». Produit le dispositif complet : politique, cartographie des risques, procédures KYC,
  dispositif de détection, circuit de déclaration, programme de formation, contrôle interne,
  conservation, et le rapport annuel de mise en œuvre. Route vers fiscalite-ci (fiscalité des flux),
  mdc-expert (livrables et comptabilité) et auditeur-superieur (mission d'audit).
---

> ## ⚖️ CHARTE MDC 2026 — PRIME SUR TOUT LE RESTE DE CE SKILL (en vigueur depuis le 11/10/2026)
> Source : dossier de conception `/Users/bilefilsseverin/LA CONFORMITE LMDC/` (Plan directeur, Méthode de l'Indice MDC, Place dans l'écosystème réglementé, Mission : gagner le contrôle, Parcours types, modèles).
> 1. **Identité.** MDC est un cabinet de conseil et d'assistance en conformité fiscale et sociale. Ligne d'identité de tout document : « Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social ». Signature : « Préparer · Assister · Défendre ». Ne plus jamais écrire « Agence de Notation (Administrative) ».
> 2. **Vocabulaire.** Notation, note AAA à D → **Indice MDC de conformité sur 100** (Maîtrisé ≥ 85, Satisfaisant ≥ 70, Fragile ≥ 55, Exposé ≥ 40, Critique) + **exposition estimée en FCFA** (bas / central / haut). Audit, auditeur, rapport d'audit → diagnostic, analyste, rapport de diagnostic. Visa, certifié conforme, certification → **attestation de diagnostic**. Réviseur de comptes ou expert-comptable pour désigner MDC → interdit. Anomalie → observation. Fraude → « exposé à ».
> 3. **Périmètre légal.** MDC ne tient pas, ne vérifie pas, ne révise pas et ne redresse pas de comptabilité (ord. 2009-387, art. 3, 5, 68, 70) ; elle ne produit ni états financiers ni écritures de régularisation, ne vise ni ne certifie, et ne rédige pas d'actes juridiques (loi 96-672). Ces travaux vont à l'expert-comptable partenaire inscrit à l'Ordre ou à l'avocat partenaire. **Toute section de ce skill qui prévoit le contraire est abrogée.**
> 4. **Mission : gagner le contrôle.** Préparer (diagnostic = contrôle à blanc ; régularisation spontanée avant tout avis, LPF art. 24), assister (conseil de son choix, LPF art. 15-16), défendre (réponse sous 30 jours, LPF art. 22-1). Chaque observation porte une position de défense (forte / discutable / faible) et une stratégie (régulariser / documenter / défendre). Méthode et moteur uniques : `notateur-conformite/scripts/indice_mdc.py` + `referentiel_mdc_v1.json`.
> 5. **Documents livrés : zéro jargon technique.** Aucun nom de fichier (.md, .py, .json), aucune commande, aucun chemin, aucun bloc de code, aucun schéma en caractères de terminal dans un document destiné au client, au gérant ou à un partenaire. Les renvois internes citent le titre du document ; les schémas deviennent des tableaux. Les générateurs `publish_pdf_mdc.py` et `publish_livrable_mdc.py` bloquent tout manquement.


# DISPOSITIF LBC/FT/FP — SKILL DE CONFORMITÉ ANTI-BLANCHIMENT

## RÈGLE D'OR : LE TEXTE AVANT TOUT

> **Ne jamais répondre de mémoire sur un seuil, une obligation ou une sanction en matière de
> blanchiment. Le corpus BCEAO et la loi ivoirienne sont archivés en local et interrogeables au
> mot près. Les consulter D'ABORD.**

**Pourquoi la règle est absolue ici plus qu'ailleurs.** Les seuils LBC/FT changent par
**instruction de la BCEAO**, pas par la loi. Une instruction de 2017 peut être remplacée par une
instruction de 2025 sans que le texte de loi bouge. Répondre « le seuil est de X » sans vérifier
quelle instruction est en vigueur, c'est exposer le client à une infraction.

**Le corpus archivé** : `~/Documents/ARCHIVES DOCUMENTS/FORMATIONS MDC/00_TEXTES_OFFICIELS_DGI/LBC_FT/`
— chaque PDF a son jumeau `.txt`, directement grep-able. Détail dans `reference/SOURCES.md`.

**Le texte en vigueur en Côte d'Ivoire** : **ordonnance n° 2023-875 du 23 novembre 2023** (JO
n° 16 bis, numéro spécial, du 1er décembre 2023 ; texte sur centif.ci). Elle reprend la loi
uniforme de mars 2023 avec la **même numérotation d'articles** : le `.txt` de la loi uniforme du
corpus sert donc à chercher, mais l'article se cite comme article de l'ordonnance. Son
**article 206 abroge la loi n° 2016-992** du 14 novembre 2016 : ne plus citer celle-ci comme
droit en vigueur.

---

## 1. LE RÉFLEXE DE QUALIFICATION — TOUJOURS EN PREMIER

Avant toute réponse, poser **trois questions dans cet ordre** :

| # | Question | Pourquoi elle commande la suite |
|---|---|---|
| **1** | **L'entité est-elle assujettie ?** | si non, aucune obligation LBC/FT propre — mais elle reste exposée au risque pénal |
| **2** | **Dans quelle catégorie ?** | institution financière, EPNFD, PSAV — les obligations diffèrent |
| **3** | **Quel niveau de risque ?** | l'approche est **fondée sur les risques** : les moyens se calibrent, ils ne se copient pas |

> **Ne jamais produire un dispositif « type » sans avoir répondu aux trois.** Un manuel LBC/FT
> copié d'une banque pour un cabinet comptable est inutilisable, et son inadéquation est en
> elle-même une faiblesse du dispositif.

**MDC et les cabinets comptables sont assujettis** : ordonnance n° 2023-875, **article 2,
point 26 e)** — « les professions comptables […] et toute personne qui fournit une assistance ou
des conseils en matière fiscale à titre d'activité rémunérée ». L'**article 51** limite leur
**vigilance à l'égard de la clientèle** à quatre familles d'opérations ; cette limite ne joue ni
pour la **déclaration de soupçon** (art. 60) ni pour l'**organisation interne** (art. 12 et 15).
Les **transitaires** ne figurent plus parmi les EPNFD. Voir `reference/ASSUJETTIS.md`.

---

## 2. LES TROIS SEUILS OPÉRATIONNELS

Ce sont les chiffres que l'on cite le plus, et ceux que l'on se trompe le plus souvent.

| Obligation | Seuil | Source |
|---|---|---|
| **Déclaration des transactions en espèces à la CENTIF** | **15 000 000 FCFA** — montant **égal ou supérieur** (ordonnance, art. 72) | Instruction **010-09-2017** |
| **Interdiction de payer une créance en espèces** | **à partir de 5 000 000 FCFA** — montant **égal ou supérieur** | Instruction **009-09-2017** (« le seuil à partir duquel ») ; ordonnance, art. 73 |
| **Déclaration des transports physiques intracommunautaires d'espèces** | **à partir de 10 000 000 FCFA** | Instruction **002-03-2025** (« le seuil à partir duquel »), en vigueur **à la date de sa signature, le 18 mars 2025** |

> **Réserve** : les instructions 009 et 010 de 2017 ont été prises sous la loi uniforme
> antérieure. Leur maintien sous la loi uniforme de 2023 (ordonnance n° 2023-875) **reste à
> confirmer** auprès de la BCEAO ou de la CENTIF.

**Détail, exemptions et réserves de mise à jour** : `reference/SEUILS_ET_OBLIGATIONS.md`.

> **Ces seuils sont fixés par instruction, pas par la loi.** Vérifier systématiquement, avant
> citation dans un livrable, qu'aucune instruction postérieure ne les a modifiés.

---

## 3. L'ARCHITECTURE D'UN DISPOSITIF — LES HUIT PILIERS

L'instruction **001-03-2025** donne le plan, article par article. **Son article 3 la limite aux
institutions financières** : pour un EPNFD (cabinet comptable, MDC), elle est un **modèle**, pas
une obligation ; l'obligation vient de l'ordonnance n° 2023-875 (art. 12, 15, 60, 89, 100). Le
dispositif complet comporte **neuf piliers**, et un dispositif auquel il en manque un n'est pas
conforme.

| # | Pilier | Fondement |
|---|---|---|
| **1** | **Gouvernance** — politiques et procédures approuvées par la haute direction, y compris la **protection des données** | Ordonnance, art. 12 (dont h) ; modèle : Instr. 001-03-2025, art. 4 et 5 |
| **2** | **Structure interne dédiée**, responsable et **correspondant CENTIF** (incompatible avec la fonction de directeur général ou assimilée) | Ordonnance, art. 12 et 100 ; modèle : Instr. 001-03-2025, art. 7 et 8 |
| **3** | **Classification des risques** — approche fondée sur les risques | Ordonnance, art. 6 et 15 |
| **4** | **Vigilance à l'égard de la clientèle** — identification, vérification, bénéficiaire effectif | Ordonnance, art. 16 à 26, applicables aux EPNFD par l'art. 48, dans les limites de l'art. 51 pour les comptables ; modèle : Instr. 003-03-2025 (réservée aux institutions financières, art. 3) |
| **5** | **Détection et déclaration** — opérations atypiques, déclaration de soupçon à la CENTIF | Ordonnance, art. 60 et 72 |
| **6** | **Formation et sensibilisation du personnel** | Ordonnance, art. 12 ; modèle : Instr. 001-03-2025, art. 9 et 10 |
| **7** | **Contrôle et audit internes** | Ordonnance, art. 12 ; modèle : Instr. 001-03-2025, art. 11 |
| **8** | **Conservation** — dix ans | Ordonnance, art. 23 (applicable aux EPNFD par l'art. 48) |
| **9** | **Gel des avoirs** — sanctions financières ciblées | Ordonnance, art. 89 ; omission sanctionnée pénalement, art. 198, al. 2 |

**Et au-dessus des neuf** : le **rapport annuel de mise en œuvre** du dispositif (modèle :
Instr. 001-03-2025, art. 12), qui est la preuve que les neuf vivent.

Le détail de chaque pilier et les livrables correspondants : `reference/ARCHITECTURE_DISPOSITIF.md`.

---

## 4. LA MÉTHODE DE PRODUCTION D'UN DISPOSITIF

| # | Étape | Livrable |
|---|---|---|
| 1 | **Qualifier** l'assujettissement et la catégorie | note de qualification |
| 2 | **Cartographier les risques** — clients, produits, canaux, zones géographiques | matrice de risques |
| 3 | **Écrire la politique** LBC/FT/FP, validée par l'organe délibérant | politique signée |
| 4 | **Désigner** le responsable et décrire ses attributions | lettre de mission |
| 5 | **Écrire les procédures** d'entrée en relation et de vigilance continue | manuel de procédures |
| 6 | **Outiller la détection** — critères d'alerte, seuils, scénarios | grille d'alertes |
| 7 | **Organiser le circuit de déclaration** — qui alerte, qui décide, qui signe | procédure de déclaration |
| 8 | **Bâtir le plan de formation** et le calendrier | plan de formation |
| 9 | **Définir le contrôle interne** — tests, périodicité, reporting | programme de contrôle |
| 10 | **Fixer la conservation** et le classement | procédure d'archivage |
| 11 | **Produire le rapport annuel** de mise en œuvre | rapport |

> **L'ordre n'est pas négociable.** Écrire les procédures avant d'avoir cartographié les risques
> produit un dispositif générique, c'est-à-dire un dispositif non conforme à l'approche fondée
> sur les risques.

---

## 5. CE QU'IL NE FAUT JAMAIS FAIRE

- **Ne jamais citer un seuil sans vérifier l'instruction en vigueur** — ils changent par instruction.
- **Ne jamais produire un dispositif sans cartographie des risques préalable** — l'approche fondée
  sur les risques est le principe directeur de la loi uniforme, article 6.
- **Ne jamais confondre la déclaration de soupçon et la déclaration de transaction en espèces** :
  la première repose sur un soupçon, sans seuil ; la seconde sur un montant, sans soupçon.
- **Ne jamais conseiller d'informer le client** d'une déclaration de soupçon le concernant.
- **Ne jamais désigner le directeur général comme correspondant CENTIF** : l'article 100,
  alinéa 2, déclare la fonction de directeur général « ou toute autre fonction assimilée »
  incompatible avec ce rôle.
- **Ne jamais citer la loi n° 2016-992 comme droit en vigueur** : elle est abrogée par
  l'article 206 de l'ordonnance n° 2023-875.
- **Ne jamais traiter la fiducie, le trust ou toute construction juridique comme un client ordinaire** :
  l'obligation porte sur l'identification du **bénéficiaire effectif**, pas du titulaire apparent.
- **Ne jamais oublier le volet fiscal** : le CGI impose la déclaration des bénéficiaires effectifs
  des personnes morales, et l'article 54 bis celle des fiducies et trusts étrangers, sous
  **30 jours** et sous peine de **2 000 000 F**.
- **Ne jamais produire un livrable LBC/FT sans réserve de mise à jour** — le GAFI, le GIABA et la
  BCEAO font évoluer le cadre par instruments infra-législatifs.

---

## 6. ROUTAGE

| Si la question porte sur… | Aller vers |
|---|---|
| la fiscalité des flux, les droits d'enregistrement, la TVA | **fiscalite-ci** |
| la comptabilisation, les livrables brandés | **mdc-expert** |
| une mission d'audit global | **auditeur-superieur** |
| le contrôle du travail produit | **auditeur-fiscal** |
| les prêts entre entreprises et le monopole bancaire | module **MC-FORM-FISC-2026-044C** |

---

## 7. RÉSERVE PERMANENTE

**À porter dans tout livrable produit avec ce skill :**

> Le cadre LBC/FT/FP évolue par **instruction de la BCEAO** et par **arrêté ministériel**, plus
> rapidement que par la loi. Les seuils, les exemptions sectorielles et les modalités déclaratives
> se vérifient à la date du livrable auprès de la **CENTIF** et dans les instructions en vigueur.
> La **loi uniforme de mars 2023** est en vigueur en Côte d'Ivoire par l'**ordonnance n° 2023-875
> du 23 novembre 2023**, dont l'article 206 abroge la loi n° 2016-992. Le maintien en vigueur des
> instructions BCEAO de 2017 (009 et 010) sous cette ordonnance reste à confirmer.
