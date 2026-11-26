# CORPUS LBC/FT/FP ARCHIVÉ EN LOCAL

**Emplacement** : `~/Documents/ARCHIVES DOCUMENTS/FORMATIONS MDC/00_TEXTES_OFFICIELS_DGI/LBC_FT/`
**Constitution** : 4 octobre 2026, depuis le site de la BCEAO et celui de la CENTIF Côte d'Ivoire
**Format** : chaque PDF a son jumeau `.txt`, directement interrogeable par `grep`

---

## LE TEXTE EN VIGUEUR EN CÔTE D'IVOIRE — NON ARCHIVÉ DANS LE CORPUS

| Texte | Où le trouver | Ce qu'il faut savoir |
|---|---|---|
| **Ordonnance n° 2023-875 du 23 novembre 2023** relative à la lutte contre le blanchiment de capitaux, le financement du terrorisme et de la prolifération des armes de destruction massive — **JO n° 16 bis, numéro spécial, du 1er décembre 2023** | centif.ci, rubrique textes juridiques : `https://www.centif.ci/wp-content/uploads/2025/03/ORDONNANCE-N2023-875-DU-23-NOVEMBRE-2023-RELATIVE-A-LA-LUTTE-CONTRE-LES-BLANCHIMENTS-DE-CAPIT.pdf` (JO scanné, 40 p., couche texte OCR exploitable) | transpose la loi uniforme de mars 2023 **avec la même numérotation d'articles** ; son **article 206 abroge la loi n° 2016-992** du 14 novembre 2016. En pratique : chercher dans `LOI_UNIFORME_LBCFTFP_MARS_2023.txt`, citer « ordonnance n° 2023-875, art. X ». Numérotation identique vérifiée le 10/10/2026 sur les art. 2 (points 12 et 26), 3, 6, 12, 15, 16, 23, 48, 49, 51, 60, 63, 71, 72, 73, 89, 90, 91, 100, 122, 184, 197, 198 et 206. Variantes de rédaction possibles (ex. art. 89, al. 1 : l'ordonnance écrit « une organisation », la loi uniforme « une organisation et des procédures internes ») : pour un avis engageant, citer le texte de l'ordonnance |

**Textes d'application ivoiriens de 2024, connus par le rapport annuel 2024 de la CENTIF**
(§ I.3, `https://www.centif.ci/wp-content/uploads/2026/04/Rapport-Annuel-CENTIF-2024-.pdf`) —
**non archivés, à récupérer avant tout avis engageant** :

| Texte | Objet |
|---|---|
| Loi n° 2024-362 du 11 juin 2024 | création du registre des bénéficiaires effectifs des personnes morales et des constructions juridiques |
| Décret n° 2024-583 du 26 juin 2024 | modalités d'accès aux informations de ce registre |
| Décret n° 2024-58 du 14 février 2024 | application de l'ordonnance n° 2022-237 du 30 mars 2022 (sanctions administratives LBC/FT/FP et organisation du contrôle des assujettis) : autorité de supervision de chaque catégorie d'EPNFD ; création de la Commission nationale des sanctions (CNS LBC/FT) |

## LES TEXTES DE BASE

| Fichier | Contenu | Pages | Qualité |
|---|---|---|---|
| `LOI_UNIFORME_LBCFTFP_MARS_2023` | **Loi uniforme UMOA** relative à la LBC/FT et à la prolifération des armes de destruction massive | 85 | texte exact |
| `LOI_LBC_FT_2016-992_CI` *(dossier parent)* | **Loi ivoirienne n° 2016-992 du 14 novembre 2016** — Journal officiel. **ABROGÉE** par l'art. 206 de l'ordonnance n° 2023-875 : historique seulement | 32 | **OCR dégradé** |
| `RECUEIL_CHAPITRE_8_LBC_FT` | **Recueil des textes, chapitre VIII** — LBC/FT | 151 | texte exact |
| `RECUEIL_TEXTES_BANCAIRES_UMOA_VOL1_2018` | Recueil des textes bancaires et financiers UMOA, volume I | 1 047 | texte exact |
| `RECUEIL_INDEX_ALPHABETIQUE` | Index alphabétique du Recueil | 13 | texte exact |
| `GUIDE_DISPOSITIF_LBC_FT_UEMOA` | Guide BCEAO du dispositif LBC/FT dans l'UEMOA | 80 | texte exact |

## LES INSTRUCTIONS BCEAO

| Fichier | Objet | Date | Champ et vigueur |
|---|---|---|---|
| `INSTR_001-03-2025_modalites_IF` | **organisation, contrôle interne et conformité** — l'architecture du dispositif | signée le 18 mars 2025 | **institutions financières seulement** (art. 3) — modèle pour un EPNFD ; en vigueur à sa signature (art. 22) ; abroge l'instruction 007-09-2017 (art. 21) |
| `INSTR_002-03-2025_seuil_transports_intra` | seuil des transports physiques **intracommunautaires** d'espèces | signée le 18 mars 2025 | toute personne ; **en vigueur à sa signature** (art. 3) ; **aucun article d'abrogation** |
| `INSTR_003-03-2025_identification_clientele` | **identification, vérification de l'identité et connaissance de la clientèle** par les institutions financières | **signée le 19 mars 2025** | **institutions financières seulement** (art. 3) — modèle pour un EPNFD ; en vigueur à sa signature (art. 31). Bénéficiaire effectif : art. 2 (définition) et art. 12 |
| `INSTR_009-09-2017_seuil_creance_especes` | seuil de paiement d'une créance en espèces | 25 sept. 2017 | prise sous la loi uniforme antérieure — **maintien sous l'ordonnance n° 2023-875 à confirmer** |
| `INSTR_010-09-2017_seuil_declaration_especes` | seuil de déclaration des transactions en espèces à la CENTIF | 25 sept. 2017 | idem — **maintien à confirmer** |

> **Fichier `INSTR_003-03-2025_identification_clientele` remplacé le 10/10/2026.** La version
> archivée le 4 octobre 2026 n'était pas l'instruction mais une capture de la page d'accueil de la
> BCEAO ; elle est conservée sous `INSTR_003-03-2025_ERRONE_page_accueil_BCEAO` (.pdf et .txt) et
> **ne doit pas être citée**. Le fichier actuel est le **texte officiel signé le 19 mars 2025**
> (14 pages, `.txt` interrogeable), issu de cb-umoa.org (rubrique LBC/FT). Les sites de la BCEAO
> et de la Commission bancaire l'intitulent « du 18 mars 2025 », mais la date portée sous la
> signature est le **19 mars 2025** : citer cette dernière. Interrogation directe :
> `grep -n "Article 3 :" "$D/INSTR_003-03-2025_identification_clientele.txt"` ·
> `grep -n -i "bénéficiaire effectif" "$D/INSTR_003-03-2025_identification_clientele.txt"`.

## LES TEXTES ANTÉRIEURS, CONSERVÉS POUR L'HISTORIQUE

| Fichier | Objet |
|---|---|
| `DIRECTIVE_07-2002_blanchiment` | Directive UEMOA n° 07/2002 — première génération |
| `DIRECTIVE_04-2007_financement_terrorisme` | Directive UEMOA n° 04/2007 — financement du terrorisme |
| `DIRECTIVE_02-2015_LBC_FT` | Directive UEMOA n° 02/2015 |
| `DECISION_26_2015_loi_uniforme` et `ANNEXE_DECISION_26_2015_loi_uniforme` | adoption du projet de loi uniforme de 2015 |
| `INSTR_007-09-2017_modalites_IF` | modalités d'application par les institutions financières — **abrogée et remplacée par 001-03-2025 (art. 21)** |
| `INSTR_01-2007-RB_organismes_financiers` | instruction 2007 aux organismes financiers |
| `INSTR_008-09-2017_seuil_transports` | seuil des transports transfrontaliers — **PDF scanné, texte non extractible**. L'instruction 002-03-2025 **ne l'abroge pas expressément** : son sort reste à établir |

---

## COMMENT INTERROGER LE CORPUS

```bash
D=~/Documents/"ARCHIVES DOCUMENTS"/"FORMATIONS MDC"/00_TEXTES_OFFICIELS_DGI/LBC_FT
grep -n -i "bénéficiaire effectif" "$D/LOI_UNIFORME_LBCFTFP_MARS_2023.txt"
grep -rn -i "personne politiquement exposée" "$D"/*.txt
```

---

## RÉSERVES SUR LE CORPUS

- **La loi ivoirienne de 2016 est un Journal officiel scanné.** Son OCR est abîmé par endroits :
  citer avec prudence, et revérifier sur l'original tout passage destiné à un avis engageant.
- **L'instruction 008-09-2017 n'a aucun texte extractible** — PDF image. L'instruction
  002-03-2025 ne contient aucun article l'abrogeant : ne pas écrire qu'elle est « remplacée »
  sans texte à l'appui.
- **Deux textes n'ont pas pu être récupérés** : la Décision n° 021 du 21 décembre 2023/CM/UMOA
  (montants des seuils pour la mise en œuvre de la loi uniforme) et la Décision n° 003 du
  28 mars 2024/CM/UMOA (seuils complémentaires), toutes deux visées par l'instruction
  003-03-2025. **À chercher avant tout travail sur les seuils.**
- **La transposition est faite** : la loi uniforme de mars 2023 est en vigueur en Côte d'Ivoire
  par l'**ordonnance n° 2023-875 du 23 novembre 2023**, dont l'article 206 abroge la loi
  n° 2016-992. L'ordonnance n'est pas archivée dans le corpus (voir en tête de ce fichier).

---

## AJOUTS DU 10/10/2026 — TEXTES ARCHIVÉS DANS LE CORPUS

| Fichier (dossier LBC_FT) | Contenu | Qualité |
|---|---|---|
| `ORDONNANCE_2023-875_LBCFTFP_CI_JO_16bis_2023-12-01` (.pdf, .txt) | **Ordonnance n° 2023-875 du 23 novembre 2023** relative à la LBC/FT/FP, JO n° 16 bis spécial du 1er décembre 2023, 40 p. Texte en vigueur en Côte d'Ivoire ; art. 206 : abrogation de la loi n° 2016-992 | JO scanné, texte reconnu (OCR) : citer l'original pour un avis engageant |
| `CENTIF_CI_RAPPORT_ANNUEL_2024` (.pdf, .txt) | Rapport annuel 2024 de la CENTIF Côte d'Ivoire, 30 p. (§ I.3 : loi n° 2024-362, décrets n° 2024-583 et 2024-58) | texte exact |

Source : centif.ci. Commande : `grep -n -i "Article 206" "$D/ORDONNANCE_2023-875_LBCFTFP_CI_JO_16bis_2023-12-01.txt"`
