---
name: preparation-mails
description: >-
  PRÉPARATION DES MAILS CLIENTS de MDC (La Maison de la Conformité SARL). Ce skill rédige le
  CORPS d'un mail client — un texte court, en clair, jamais un document mis en page — annonce les
  pièces jointes déjà publiées (notes, fiches, classeurs brandés produits par mdc-expert /
  redaction), et dépose le tout en BROUILLON dans le Gmail de l'utilisateur. Il ne produit JAMAIS
  le corps du mail en PDF ou en Word : le PDF est l'attachement, le mail est un texte. Il ne
  SEND jamais un message — seulement create_draft ; l'envoi reste un geste volontaire de
  l'utilisateur dans Gmail. Déclenche ce skill dès que l'utilisateur veut : préparer/rédiger un
  mail pour un client, envoyer le mail à un client, mettre un mail en brouillon, mettre ça dans
  mon Gmail, « prépare le mail pour... », « envoie le mail pour la situation X », « fais-moi un
  brouillon Gmail avec la note en pièce jointe ».
---

> ## ⚖️ CHARTE MDC 2026 — PRIME SUR TOUT LE RESTE DE CE SKILL (en vigueur depuis le 11/10/2026)
> Source : dossier de conception `/Users/bilefilsseverin/LA CONFORMITE LMDC/` (Plan directeur, Méthode de l'Indice MDC, Place dans l'écosystème réglementé, Mission : gagner le contrôle, Parcours types, modèles).
> 1. **Identité.** MDC est un cabinet de conseil et d'assistance en conformité fiscale et sociale. Ligne d'identité de tout document : « Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social ». Signature : « Préparer · Assister · Défendre ». Ne plus jamais écrire « Agence de Notation (Administrative) ».
> 2. **Vocabulaire.** Notation, note AAA à D → **Indice MDC de conformité sur 100** (Maîtrisé ≥ 85, Satisfaisant ≥ 70, Fragile ≥ 55, Exposé ≥ 40, Critique) + **exposition estimée en FCFA** (bas / central / haut). Audit, auditeur, rapport d'audit → diagnostic, analyste, rapport de diagnostic. Visa, certifié conforme, certification → **attestation de diagnostic**. Réviseur de comptes ou expert-comptable pour désigner MDC → interdit. Anomalie → observation. Fraude → « exposé à ».
> 3. **Périmètre légal.** MDC ne tient pas, ne vérifie pas, ne révise pas et ne redresse pas de comptabilité (ord. 2009-387, art. 3, 5, 68, 70) ; elle ne produit ni états financiers ni écritures de régularisation, ne vise ni ne certifie, et ne rédige pas d'actes juridiques (loi 96-672). Ces travaux vont à l'expert-comptable partenaire inscrit à l'Ordre ou à l'avocat partenaire. **Toute section de ce skill qui prévoit le contraire est abrogée.**
> 4. **Mission : gagner le contrôle.** Préparer (diagnostic = contrôle à blanc ; régularisation spontanée avant tout avis, LPF art. 24), assister (conseil de son choix, LPF art. 15-16), défendre (réponse sous 30 jours, LPF art. 22-1). Chaque observation porte une position de défense (forte / discutable / faible) et une stratégie (régulariser / documenter / défendre). Méthode et moteur uniques : `notateur-conformite/scripts/indice_mdc.py` + `referentiel_mdc_v1.json`.
> 5. **Documents livrés : zéro jargon technique.** Aucun nom de fichier (.md, .py, .json), aucune commande, aucun chemin, aucun bloc de code, aucun schéma en caractères de terminal dans un document destiné au client, au gérant ou à un partenaire. Les renvois internes citent le titre du document ; les schémas deviennent des tableaux. Les générateurs `publish_pdf_mdc.py` et `publish_livrable_mdc.py` bloquent tout manquement.


# PRÉPARATION DES MAILS — brouillons Gmail brandés MDC

## 0. Rôle et confusion à éviter

Un mail client a **deux parties bien distinctes** :

- **le corps du mail** : un texte court, écrit en clair, directement dans le champ du message —
  jamais mis en page, jamais transformé en PDF ou en Word ;
- **la pièce jointe** : le document déjà publié par `redaction` ou `mdc-expert` (note d'information,
  fiche, classeur), au format PDF/Word/Excel avec logo et charte MDC.

**Ne jamais confondre les deux.** Si l'utilisateur dit « pourquoi tu prépares le mail en PDF ? »,
c'est le signe que le corps du mail a été traité comme un document au lieu d'un texte simple — le
corriger immédiatement : le corps repasse en texte courant, la mise en forme riche (gras, listes)
passe uniquement par le HTML du mail (`<strong>`, `<ul>`), jamais par un fichier.

## 1. Structure attendue du corps

1. **Objet** — court, factuel, sans jargon de référence interne (pas de « MDC/NI/VM-2026 » dans
   l'objet, ça reste dans la note).
2. **Ouverture** — « Madame, Monsieur, » directement, pas de fioriture.
3. **Contexte** — 2 à 4 lignes qui rappellent l'obligation ou la situation, sans reprendre tout le
   contenu de la pièce jointe.
4. **L'essentiel chiffré** — en texte courant ou en liste simple à tirets, jamais un tableau
   Markdown (`|---|---|`) : ça ne se rend pas dans un mail.
5. **Annonce des pièces jointes** — une phrase qui dit ce qu'elles contiennent.
6. **Action attendue** — validation, paiement, retour de document, avec une date si pertinent.
7. **Formule de politesse + signature MDC** :
   ```
   BILE SÉVERIN
   Gérant — LA MAISON DE LA CONFORMITÉ SARL
   Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social
   Tél. +225 07 19 31 49 04 · lamaisondelaconformite@gmail.com
   www.lamaisondelaconformitesarl.net
   ```

**Longueur cible : 150 à 350 mots.** Un mail n'est pas une note — s'il faut tout expliquer en
détail, c'est que ça appartient à la pièce jointe, pas au corps du message.

## 2. Deux versions du corps, jamais une seule

Le tool de brouillon Gmail (`create_draft`) accepte `body` (texte brut) et `htmlBody` (mise en
forme riche). Toujours fournir les deux, à partir de la même source :

- **`body`** : texte brut lisible — retirer tout symbole Markdown résiduel (`**`, `##`, `-`
  décoratif). Les emphases se perdent, c'est normal pour du texte brut.
- **`htmlBody`** : la même chose convertie proprement — `**gras**` → `<strong>gras</strong>`,
  sauts de paragraphe → `<p>...</p>`, listes à tirets → `<ul><li>...</li></ul>`. Pas de CSS
  exotique, pas de tableau complexe : un mail doit s'afficher correctement sur mobile.

Si une source `_sources/Mail-*.txt` ou `.md` existe déjà pour la situation demandée, elle sert de
base : ne pas la réécrire depuis zéro si elle est à jour, seulement la convertir proprement en
`body`/`htmlBody`.

## 3. Pièces jointes

- **Toujours reprendre les fichiers déjà publiés** dans le dossier `_A_ENVOYER/` (ou équivalent) du
  projet en cours — jamais régénérer un PDF pour l'occasion, jamais improviser un contenu.
- Lire chaque fichier, l'encoder en base64, et le passer dans `attachments` avec son `filename`
  d'origine et le bon `mimeType` (`application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  pour un `.docx`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` pour un
  `.xlsx`).
- Vérifier la taille cumulée des pièces jointes (limite 25 Mo côté Gmail) avant d'assembler le
  brouillon.

## 4. Destinataire

- Si l'adresse du client est connue (donnée dans la conversation, ou dans un fichier de contacts
  du projet), la mettre dans `to`.
- **Si elle n'est pas connue, ne jamais l'inventer** : créer le brouillon avec `to` vide et le
  signaler clairement à l'utilisateur — il complètera le destinataire lui-même avant l'envoi.

## 5. Règle d'or — jamais d'envoi direct

Ce skill **ne produit que des brouillons** (`create_draft`). Il n'appelle **jamais**
`send_message`, `reply`, ni aucun outil qui transmet réellement le message à un tiers — l'envoi
reste un geste volontaire que l'utilisateur pose lui-même dans Gmail, après relecture. Toujours
confirmer à l'utilisateur, une fois le brouillon créé :

- l'objet retenu ;
- le ou les destinataires (ou « à compléter ») ;
- la liste des pièces jointes ;
- un rappel qu'il doit relire et cliquer Envoyer lui-même.

## 6. Enchaînement typique

1. Identifier la situation du client (s'appuyer sur un éventuel `Guide-mails-par-situation.txt`
   du projet) et la source de mail correspondante dans `_sources/`.
2. Convertir cette source en `body` (texte brut) et `htmlBody` (HTML propre).
3. Rassembler les pièces jointes depuis `_A_ENVOYER/`, les encoder en base64.
4. Demander le destinataire si absent, sinon le renseigner.
5. Appeler `create_draft` (jamais `send_message`).
6. Restituer à l'utilisateur un résumé court du brouillon créé.
