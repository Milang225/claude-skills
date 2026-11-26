---
name: fiscalite-ci
description: >
  SKILL MAÎTRE DE LA FISCALITÉ IVOIRIENNE de MDC (La Maison de la Conformité SARL).
  Point d'entrée unique pour toute question d'impôt en Côte d'Ivoire, adossé aux TEXTES OFFICIELS
  ARCHIVÉS EN LOCAL et interrogeables au mot près : CODE GÉNÉRAL DES IMPÔTS ÉDITION 2026 intégral
  (1 162 articles, texte exact issu du HTML, PDF cherchable de 1 520 pages, annoté des versions 2025
  et 2024), Doctrine fiscale DGI 2026 (338 pages), Bulletin officiel DGI 2026 (analyse de l'annexe
  fiscale 2026, 172 pages), Code minier 2014, AUSCGIE, loi bancaire UMOA 2023, Convention CIPRES de sécurité sociale, Code des investissements et sa note DGI, et le CGI 2025 conservé en archive.
  Déclenche ce skill dès que l'utilisateur pose une question sur : un impôt, un taux, un seuil, une assiette,
  une exonération, une déduction, une déclaration, un régime d'imposition, une pénalité ;
  I-BIC, IMF, TVA, ITS, IRVM, IRC, patente, droits d'enregistrement, impôt foncier, TSE, TOB, AIRSI,
  taxe d'apprentissage, FDFP, CNPS ; TEE, microentreprises, réel simplifié, réel normal ;
  régime mère-fille, holding, GIE, groupe, prix de transfert, plateformes numériques, startups labellisées,
  fiscalité minière, Code des investissements et agréments, monopole bancaire et prêts entre entreprises,
  détachement de personnel et sécurité sociale CIPRES ; annexe fiscale 2026, doctrine DGI, note de service, bulletin officiel ;
  « quel taux », « combien va payer », « est-ce déductible », « est-ce exonéré », « que dit le texte »,
  « quel article », « quelles déclarations », « quel régime ». Couvre aussi la production de modules de
  formation fiscale. Route vers reintegrations-deductions (déductibilité fine), retenues-salaire-paie,
  avantages-en-nature, auditeur-fiscal (contrôle du travail produit) et mdc-expert (comptabilité, livrables).
---

> ## ⚖️ CHARTE MDC 2026 — PRIME SUR TOUT LE RESTE DE CE SKILL (en vigueur depuis le 11/10/2026)
> Source : dossier de conception `/Users/bilefilsseverin/LA CONFORMITE LMDC/` (Plan directeur, Méthode de l'Indice MDC, Place dans l'écosystème réglementé, Mission : gagner le contrôle, Parcours types, modèles).
> 1. **Identité.** MDC est un cabinet de conseil et d'assistance en conformité fiscale et sociale. Ligne d'identité de tout document : « Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social ». Signature : « Préparer · Assister · Défendre ». Ne plus jamais écrire « Agence de Notation (Administrative) ».
> 2. **Vocabulaire.** Notation, note AAA à D → **Indice MDC de conformité sur 100** (Maîtrisé ≥ 85, Satisfaisant ≥ 70, Fragile ≥ 55, Exposé ≥ 40, Critique) + **exposition estimée en FCFA** (bas / central / haut). Audit, auditeur, rapport d'audit → diagnostic, analyste, rapport de diagnostic. Visa, certifié conforme, certification → **attestation de diagnostic**. Réviseur de comptes ou expert-comptable pour désigner MDC → interdit. Anomalie → observation. Fraude → « exposé à ».
> 3. **Périmètre légal.** MDC ne tient pas, ne vérifie pas, ne révise pas et ne redresse pas de comptabilité (ord. 2009-387, art. 3, 5, 68, 70) ; elle ne produit ni états financiers ni écritures de régularisation, ne vise ni ne certifie, et ne rédige pas d'actes juridiques (loi 96-672). Ces travaux vont à l'expert-comptable partenaire inscrit à l'Ordre ou à l'avocat partenaire. **Toute section de ce skill qui prévoit le contraire est abrogée.**
> 4. **Mission : gagner le contrôle.** Préparer (diagnostic = contrôle à blanc ; régularisation spontanée avant tout avis, LPF art. 24), assister (conseil de son choix, LPF art. 15-16), défendre (réponse sous 30 jours, LPF art. 22-1). Chaque observation porte une position de défense (forte / discutable / faible) et une stratégie (régulariser / documenter / défendre). Méthode et moteur uniques : `notateur-conformite/scripts/indice_mdc.py` + `referentiel_mdc_v1.json`.
> 5. **Documents livrés : zéro jargon technique.** Aucun nom de fichier (.md, .py, .json), aucune commande, aucun chemin, aucun bloc de code, aucun schéma en caractères de terminal dans un document destiné au client, au gérant ou à un partenaire. Les renvois internes citent le titre du document ; les schémas deviennent des tableaux. Les générateurs `publish_pdf_mdc.py` et `publish_livrable_mdc.py` bloquent tout manquement.


# FISCALITÉ IVOIRIENNE — SKILL MAÎTRE

## RÈGLE D'OR : LE TEXTE AVANT TOUT

> **Ne jamais répondre de mémoire, ni depuis une recherche web, sur une question de fiscalité ivoirienne.
> Les textes officiels sont archivés en local et interrogeables au mot près. Les consulter D'ABORD.**

**Pourquoi cette règle est absolue.** Les recherches web sur la fiscalité ivoirienne ramènent
des paraphrases souvent fausses. Exemples réellement rencontrés et corrigés :

| Affirmation trouvée en ligne | Ce que dit le texte |
|---|---|
| IMF : 5 % du CA, minimum 400 000 | **0,5 %**, minimum **3 000 000** — CGI art. 39 |
| Succession : abattement 12 000 000, taux 45 % | 100 000 000 et 12 % selon le CGI et un notaire |

**Et ne jamais répondre par déduction quand un texte peut être lu.** Sur huit corrections doctrinales
relevées en septembre 2026, **cinq portaient sur des raisonnements qui paraissaient solides**
et que la lecture directe a démentis.

## OÙ SONT LES TEXTES

Dossier : `~/Documents/ARCHIVES DOCUMENTS/FORMATIONS MDC/00_TEXTES_OFFICIELS_DGI/`

| Fichier | Contenu | Volume |
|---|---|---|
| **`CGI_2026_TEXTE_INTEGRAL.txt`** · **`CGI_2026.pdf`** | **CODE GÉNÉRAL DES IMPÔTS, ÉDITION 2026 — SOURCE DE RÉFÉRENCE.** 1 162 articles, **annoté** des versions 2025 et 2024. PDF cherchable de 1 520 pages | **3 284 835 car.** |
| `DOCTRINE_FISCALE_2026_TEXTE.txt` · `.pdf` | **Doctrine fiscale 2026** — notes de service de portée générale, 338 p. | 737 496 car. |
| `BULLETIN_OFFICIEL_DGI_2026_TEXTE.txt` · `.pdf` | **Bulletin officiel DGI 2026** — note n° 00511 du 27/01/2026, analyse de l'annexe fiscale 2026, 172 p. | 329 270 car. |
| `CODE_MINIER_2014_TEXTE.txt` | **Loi n° 2014-138** du 24 mars 2014 portant Code minier | 106 062 car. |
| `LOI_BANCAIRE_UMOA_2023_TEXTE.txt` · `.pdf` | **Loi bancaire UMOA du 16 juin 2023** — monopole bancaire, opérations permises à toute entreprise, sanctions | 211 Ko |
| `CIPRES_CONVENTION_2006.txt` | **Convention CIPRES** de sécurité sociale — détachement, législation applicable | 240 Ko |
| `CODE_INVESTISSEMENTS_ORD_2024-857_TEXTE.txt` · `.pdf` | **Ordonnance 2024-857** modifiant le Code des investissements. **Le Code de base, ord. 2018-646, n'est pas en local** | 23 Ko |
| `NOTE_DGI_050_2024_CODE_INVESTISSEMENTS_TEXTE.txt` · `.pdf` | **Note DGI n° 050** — avantages en **phase d'exploitation** des entreprises agréées | 19 Ko |
| `AUSCGIE_TEXTE.txt` | Acte uniforme OHADA sociétés commerciales et GIE | 631 Ko |
| `CGI_2025_TEXTE_INTEGRAL_ARCHIVE.txt` | Édition 2025, **conservée pour comparer les versions** | 1 093 005 car. |

> **Toujours interroger l'édition 2026.** L'édition 2025 ne sert plus qu'à retrouver un état
> antérieur du texte. L'édition 2026 porte d'ailleurs, sous chaque article modifié, la mention
> des versions **2025** et **2024**, ce qui permet de dater un changement sans changer de fichier.

**Comment chercher.**

```bash
F="$HOME/Documents/ARCHIVES DOCUMENTS/FORMATIONS MDC/00_TEXTES_OFFICIELS_DGI/CGI_2026_TEXTE_INTEGRAL.txt"
grep -n "^Art. 39 –" "$F"            # atteindre un article précis
sed -n '1697,1740p' "$F"             # lire son contenu
grep -n -i "minimum forfaitaire" "$F"  # chercher une notion
```

> **Deux pièges de recherche.** L'édition **2026** vient d'une source HTML : le texte est propre,
> sans césure, mais les numéros d'articles s'écrivent tantôt `Art. 92` tantôt `Art. 92 ` avec une
> espace finale — **ne jamais ancrer sur un motif trop strict**. L'édition **2025** archivée porte
> en revanche des césures de mise en page : `so-ciété`, `bénéfi-ces`, `microentre-prises`.

Les autres actes uniformes OHADA (AUDCG, AUDCIF) sont dans
`~/Documents/ARCHIVES DOCUMENTS/FORMATIONS MDC/FISCALITE_CI/_SOURCES_MD/`.

**Comment le CGI 2026 a été obtenu** — le site `cgici.com` est une application JavaScript. Les pages
ne sont pas à `cgici.com/page-N.html`, qui renvoie 404, mais à **`cgici.com/V2026/page-N.html`**,
de 0 à 713. Seule l'observation du trafic réseau pendant une navigation réelle le révèle. Le contenu
est du **HTML**, donc du texte exact, sans reconnaissance de caractères.

## MÉTHODE DE RÉPONSE

**1. Faire germer une dizaine de questions dérivées avant de répondre.** La question posée n'est
presque jamais la seule qui compte. Les afficher quand elles éclairent le raisonnement : elles
servent de plan.

**2. Lire le texte.** Citer l'article, verbatim, entre guillemets.

**3. Chiffrer.** Un taux sans un exemple chiffré n'est pas une réponse opérationnelle.

**4. Séparer ce qui est établi de ce qui est déduit.** Tout livrable se termine par une
**réserve méthodologique** en deux parties : ce qui est établi sur le texte, et ce qui relève
du raisonnement. **Nommer les points ouverts plutôt que les taire.**

**5. Router vers le skill spécialisé** quand la question l'appelle — voir la fin de ce document.

## FICHIERS DE RÉFÉRENCE DE CE SKILL

| Fichier | Contenu |
|---|---|
| `reference/TAUX_ET_SEUILS.md` | **Tous les taux et seuils vérifiés sur texte**, avec l'article |
| `reference/REGIMES_D_IMPOSITION.md` | TEE, microentreprises, réel simplifié, réel normal, et le **plancher du minimum de perception** |
| `reference/ANNEXE_FISCALE_2026.md` | **Les 38 mesures** de l'annexe fiscale 2026, avec les changements de fond |
| `reference/POINTS_OUVERTS.md` | Les questions non tranchées, à ne jamais présenter comme réglées |
| **`reference/NORME_REDACTION_MODULES.md`** | **La norme de rédaction des modules — à lire avant d'en produire ou d'en réviser un** |

## LES QUATRE ERREURS LES PLUS COÛTEUSES

**1. Croire qu'une société sans chiffre d'affaires ne paie rien.** Le minimum de perception
impose un **plancher** d'impôts professionnels : 8 000 000 au réel simplifié, 9 600 000 au réel
normal. Voir `reference/REGIMES_D_IMPOSITION.md`.

**2. Confondre exonération du salarié et déduction de l'employeur.** Un plafond d'exonération
à l'ITS ne limite jamais la déductibilité de la charge chez l'entreprise.

**3. Appeler « holding » une société qui exerce une activité.** Le régime de l'article 23
suppose l'**absence de toute activité**. Facturer des prestations au groupe détruit le taux de 12 %.

**4. Payer pour une autre société du groupe sans refacturer.** Réintégration à 25 % **et** IRVM
à 15 % sur la somme désinvestie, cumulés, **même en déficit**. Soit 40 % de la somme.

## ROUTAGE VERS LES AUTRES SKILLS

| Question | Skill |
|---|---|
| Une charge est-elle déductible ? réintégrations, tableau de passage | `reintegrations-deductions` |
| Retenue sur salaire pour faute, absence, dommage, avance | `retenues-salaire-paie` |
| Évaluation d'un avantage en nature | `avantages-en-nature` |
| Vérifier un travail fiscal déjà produit avant livraison | `auditeur-fiscal` |
| Écritures, états financiers, livrables, télédéclaration | `mdc-expert` |
| Mise en forme et publication à la charte | `redaction` |

## PRODUCTION DE MODULES DE FORMATION

Le curriculum vit dans `~/Documents/ARCHIVES DOCUMENTS/FORMATIONS MDC/FISCALITE_CI/`, en 14 blocs numérotés.
**Vérifier systématiquement qu'un module n'existe pas déjà** avant d'en produire un,
et repérer le numéro de leçon libre.

Tout module comporte, dans cet ordre : en-tête avec référence `MC-FORM-FISC-AAAA-NNN`,
**SOMMAIRE** (obligatoire, avant l'avant-propos), avant-propos, sections numérotées avec durées,
grille de contrôle, synthèse en dix règles, **réserve méthodologique**.

Publication :

```bash
NODE_PATH=$(npm root -g) python3 ~/.claude/skills/mdc-expert/scripts/publish_livrable_mdc.py SRC.md DEST.docx "Titre" "Client" "Réf"
python3 ~/.claude/skills/mdc-expert/scripts/publish_pdf_mdc.py SRC.md DEST.pdf "Titre" "Client" "Réf"
```

## ACQUÉRIR UN NOUVEAU TEXTE DE LA DGI

Les publications de la DGI sont des **livres feuilletables sans couche de texte**. Méthode validée :

```bash
B="https://www.dgi.gouv.ci/assets/documents/<NOM_DU_LIVRE>"   # pages : $B/files/mobile/N.jpg
# 1. trouver la dernière page par dichotomie sur le code HTTP
# 2. télécharger chaque page
# 3. sips -Z 2600 page.jpg --out page.png     (agrandir pour la reconnaissance)
# 4. ~/.claude/skills/mdc-expert/scripts/mdc-ocr page.png >> texte.txt
# 5. PDF cherchable : PyMuPDF, réinsérer le texte en calque invisible (render_mode=3)
```

Les notes de service scannées se lisent avec `mdc-ocr` après conversion en images par PyMuPDF.
