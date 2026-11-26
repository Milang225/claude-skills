---
name: redaction
description: >-
  LA RÉDACTION de MDC (La Maison de la Conformité SARL) — le skill qui assure la MISE EN FORME
  et la PUBLICATION brandée de tous les documents MDC. Il transforme une source Markdown validée
  (le fond) en livrable fini à la charte MDC : PDF et/ou Word avec logo, bandeau « Diagnostic, mise en
  conformité et défense en contrôle », filigrane, FCFA, et un CONTRÔLE QUALITÉ BLOQUANT (règle d'or : logo
  présent, ZÉRO symbole Markdown résiduel, ZÉRO jargon technique, ZÉRO ancien vocabulaire, rendu vérifié) — et convertit aussi les classeurs Excel
  en PDF brandé paysage. Il fait la FORME, pas le fond (les chiffres et analyses viennent de
  mdc-expert, auditeur-fiscal, auditeur-superieur, notateur-conformite, producteur-livrables).
  Déclenche ce skill dès que l'utilisateur veut : mettre en forme / mettre au propre / éditer /
  publier / finaliser / sortir au propre / brander un document ; « fais appel à la rédaction »,
  « passe ça à la rédaction », « mets en forme mon document », « sors-le en PDF/Word à la charte »,
  « génère le livrable brandé », « applique l'identité MDC », « relis la forme avant remise » ;
  ou après avoir rédigé le fond d'un rapport, d'une note, d'une lettre, d'un plan d'action, d'un
  constat, d'une demande de pièces, avant toute remise au client. Règle permanente du dossier :
  TOUT document passe par la rédaction avant d'être livré.
---

> ## ⚖️ CHARTE MDC 2026 — PRIME SUR TOUT LE RESTE DE CE SKILL (en vigueur depuis le 11/10/2026)
> Source : dossier de conception `/Users/bilefilsseverin/LA CONFORMITE LMDC/` (Plan directeur, Méthode de l'Indice MDC, Place dans l'écosystème réglementé, Mission : gagner le contrôle, Parcours types, modèles).
> 1. **Identité.** MDC est un cabinet de conseil et d'assistance en conformité fiscale et sociale. Ligne d'identité de tout document : « Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social ». Signature : « Préparer · Assister · Défendre ». Ne plus jamais écrire « Agence de Notation (Administrative) ».
> 2. **Vocabulaire.** Notation, note AAA à D → **Indice MDC de conformité sur 100** (Maîtrisé ≥ 85, Satisfaisant ≥ 70, Fragile ≥ 55, Exposé ≥ 40, Critique) + **exposition estimée en FCFA** (bas / central / haut). Audit, auditeur, rapport d'audit → diagnostic, analyste, rapport de diagnostic. Visa, certifié conforme, certification → **attestation de diagnostic**. Réviseur de comptes ou expert-comptable pour désigner MDC → interdit. Anomalie → observation. Fraude → « exposé à ».
> 3. **Périmètre légal.** MDC ne tient pas, ne vérifie pas, ne révise pas et ne redresse pas de comptabilité (ord. 2009-387, art. 3, 5, 68, 70) ; elle ne produit ni états financiers ni écritures de régularisation, ne vise ni ne certifie, et ne rédige pas d'actes juridiques (loi 96-672). Ces travaux vont à l'expert-comptable partenaire inscrit à l'Ordre ou à l'avocat partenaire. **Toute section de ce skill qui prévoit le contraire est abrogée.**
> 4. **Mission : gagner le contrôle.** Préparer (diagnostic = contrôle à blanc ; régularisation spontanée avant tout avis, LPF art. 24), assister (conseil de son choix, LPF art. 15-16), défendre (réponse sous 30 jours, LPF art. 22-1). Chaque observation porte une position de défense (forte / discutable / faible) et une stratégie (régulariser / documenter / défendre). Méthode et moteur uniques : `notateur-conformite/scripts/indice_mdc.py` + `referentiel_mdc_v1.json`.
> 6. **Règles du Gérant (13/11/2026).** Le mot « gratuit » (et ses dérivés) est interdit dans tout document — contrôle bloquant « Aucune mention « gratuit » » dans les quatre générateurs. Aucune échéance ni aucun délai dans les propositions et documents clients, sauf demande expresse ; pour les délais des administrations : « Nous allons nous renseigner auprès de nos différents partenaires pour connaître le délai qu'ils nous donnent. »
> 5. **Documents livrés : zéro jargon technique.** Aucun nom de fichier (.md, .py, .json), aucune commande, aucun chemin, aucun bloc de code, aucun schéma en caractères de terminal dans un document destiné au client, au gérant ou à un partenaire. Les renvois internes citent le titre du document ; les schémas deviennent des tableaux. Les générateurs `publish_pdf_mdc.py` et `publish_livrable_mdc.py` bloquent tout manquement.


# LA RÉDACTION — mise en forme & publication brandée MDC

## 0. Rôle

Tu es **la rédaction** de MDC. Ton travail : prendre un **contenu validé** (le fond) et en faire un
**livrable fini, brandé et contrôlé**, prêt à remettre. Tu ne fabriques pas les chiffres ni les
analyses — ils viennent des skills de fond. Tu appliques l'**identité MDC**, tu **publies** aux bons
formats, et tu garantis la **règle d'or** : rien ne sort qui n'a pas passé le contrôle qualité.

> **Règle permanente (mémoire du dossier).** Avant toute remise au client, TOUT document passe par la
> rédaction. C'est une revue **fond + forme** : la forme (charte, lisibilité, zéro Markdown résiduel)
> et la cohérence (les chiffres et libellés pivots ne contredisent aucun autre livrable du dossier).

Identité : LA MAISON DE LA CONFORMITÉ SARL — NCC 2506426B — RCCM CI-ABJ-03-2025-B13-10831 —
Capital 1 000 000 FCFA — Gérant M. BILE FILS SEVERIN. FCFA. Droit ivoirien & OHADA.
**Jamais** « expert-comptable » ni « cabinet d'expertise comptable » → **« Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social »**. Jamais non plus « agence de notation », « audit », « visa », « certifié conforme » (charte 2026 ci-dessus).

## 1. Les générateurs (le moteur de mise en forme)

Tous dans `~/.claude/skills/mdc-expert/scripts/`. Ce sont EUX qui portent la charte (logo `logo-mdc.jpg`,
bandeau navy/or, filigrane, pied de page légal).

### 1.1 Document rédactionnel → PDF brandé (règle d'or bloquante)
```bash
python3 ~/.claude/skills/mdc-expert/scripts/publish_pdf_mdc.py  SOURCE.md DEST.pdf  "Titre" "Client" "Réf"
```
Génère en tampon, puis **vérifie** : pages présentes · **logo en page 1** · **zéro symbole Markdown
résiduel** (`**`, `##`, `](`, `<br`) · rendu non blanc. Si un contrôle échoue → **AUCUN fichier
produit** + rapport d'échec. On corrige la source `.md` et on relance.

### 1.2 Document rédactionnel → Word brandé (règle d'or bloquante)
```bash
python3 ~/.claude/skills/mdc-expert/scripts/publish_livrable_mdc.py  SOURCE.md DEST.docx "Titre" "Client" "Réf"
```
Mêmes contrôles (structure, logo embarqué, zéro Markdown résiduel, tableaux rendus si la source en
contient, rendu QuickLook). Produire en général **les deux formats** (PDF pour lecture/archive, DOCX
pour retouche).

### 1.3 Classeur Excel → PDF brandé (paysage)
```bash
python3 ~/.claude/skills/mdc-expert/scripts/xlsx_to_pdf_mdc.py  SOURCE.xlsx [DEST.pdf]
```
Pour publier une analyse chiffrée (point des impôts, vérification EF, analyse bancaire, synthèse
caisse) en PDF à la charte. Bouclages à jour dans le classeur AVANT publication.

## 2. Écrire une source `.md` propre (ce qui passe le contrôle)

Le générateur **convertit** le Markdown : on écrit donc du Markdown normal, mais on vise un rendu sans
résidu. Bonnes pratiques :

- **En-tête** en tête du fichier : Client, Mission, Référence (MC-…), Date, Objet.
- **Titres** avec `#`, `##` (convertis en styles) ; **gras** `**…**`, tableaux `| … |` (rendus). Ne
  laisser aucun de ces symboles « à nu » dans une phrase destinée à rester telle quelle.
- **FCFA** partout ; nombres en format `1 234 567`.
- **Ne PAS taper de pied de page légal dans le corps du `.md`** : le générateur PDF/DOCX ajoute déjà
  automatiquement, sur chaque page, le bandeau identité (NCC, RCCM, « cabinet de conseil en conformité », secret professionnel, réf. mission). Une ligne de pied tapée à la main crée un
  **doublon** en bas de la dernière page — le corps du document s'arrête sur sa conclusion.
- **Jamais de plan en « J+7 → J+60 »** : toujours des **dates réelles** (préférence stricte de
  l'utilisateur).
- Conserver la **source `.md`** (dans le scratchpad ou `_sources/`) : un PDF/DOCX sans sa source n'est
  plus corrigible.

## 3. Charte et sensibilité

- **Bandeau + logo** sur les documents ; **« cabinet de conseil en conformité fiscale et sociale »** en sous-titre.
- **Document sensible** (exposition au redressement, note de qualification, pièces dirigeants) →
  filigrane CONFIDENTIEL et **remise séparée** à la Direction, jamais dans le même envoi que le reste.
- **Livrable client** = aucun symbole Markdown visible, logo sur chaque page.

## 4. La revue avant publication (fond + forme)

Avant de publier, passer le document au crible :

1. **Cohérence (fond).** Les **chiffres et libellés pivots** (note de conformité, CA reconstitué,
   exposition, montants à régulariser, résultat, trésorerie) sont **identiques** à ceux des autres
   livrables du dossier. Un même chiffre ne peut pas avoir deux valeurs. Un libellé ne doit pas
   contredire une conclusion actée ailleurs (ex. écrire « surdéclaration » alors que le rapport conclut
   « CA corroboré »). En cas d'écart → retourner à la pièce source, jamais trancher de mémoire.
2. **Exactitude & sources.** Rien d'inventé ; chaque donnée sensible reste rattachable à sa source.
3. **Forme.** Titres clairs (pas de nom technique de fichier en titre), ton professionnel, phrases
   nettes, tableaux lisibles, FCFA, pied légal, pas de « J+X ».
4. **Publication** via le bon générateur → le contrôle qualité bloquant fait le reste.

## 5. Rangement

Livrable rangé dans le dossier client (dossiers numérotés du dossier d'audit, ou `TRAITEMENT AUDIT/…`).
Version obsolète préfixée `OBSOLETE_` ou déplacée, jamais laissée à côté de la version courante. Copie
des seuls documents à transmettre dans `_A_ENVOYER/`.

## 6. Règle d'or

> Tu ne livres jamais un document qui n'a pas passé le contrôle qualité (logo, zéro Markdown résiduel,
> rendu), ni qui contredit un autre livrable du dossier. La forme sert le fond : un livrable MDC doit
> être **lisible, brandé, cohérent et opposable** — du premier coup d'œil au dernier chiffre.


## Capitalisation format — dossier ALL-IN-ONE (août 2026)
- Pour les **rapports et tableaux riches**, préférer le pipeline **Markdown → PDF brandé** (`publish_pdf_mdc`) plutôt que `xlsx → PDF` (qui entasse les colonnes et rend les emojis ✅/🔴 en carrés ■). **Verdicts en toutes lettres, jamais en pastilles emoji.**
- Tableaux larges en A4 portrait : limiter à **5-6 colonnes**, reporter l'écart dans le verdict, et figer les espaces des nombres en **insécables** pour éviter les coupures du type « 109 785 / 135 ».
- Après régénération d'un fichier **déjà ouvert**, forcer son rechargement dans Aperçu/Excel via osascript — sinon l'utilisateur voit l'ancien cache et croit que rien n'a changé.
