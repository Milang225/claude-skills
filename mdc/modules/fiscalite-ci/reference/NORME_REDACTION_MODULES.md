# NORME DE RÉDACTION DES MODULES — STANDARD MDC

> Norme arrêtée par le gérant en septembre 2026, à partir du module **43, deuxième édition**.
> **Tout module produit ou révisé s'y conforme.**

## LA RÈGLE CARDINALE : L'ASSIETTE AVANT LE TAUX

**Un taux ne s'écrit jamais seul.** Il s'écrit toujours avec ce sur quoi il s'applique.

| Interdit | Obligatoire |
|---|---|
| « Personnes physiques : 9 % » | « Personnes physiques : **9 % de la valeur locative** » |
| « Habitation principale : 3 % » | « Habitation principale non productive : **0,5 % de la valeur marchande** » |

**Tout tableau de taux comporte une colonne « Assiette ».** Sans exception.

> **L'erreur que cette règle prévient.** La première édition du module 43 confondait des **abattements
> d'assiette** avec des **taux d'impôt**. Un lecteur appliquant 13 % à la valeur marchande au lieu de
> la base par appréciation directe surévaluait l'impôt de **dix-huit fois**.

## NE JAMAIS MÉLANGER DEUX IMPÔTS DANS UN MÊME TABLEAU

Un tableau, un impôt. Si deux impôts frappent le même bien, deux tableaux, chacun titré de son impôt.

## CHAQUE RÈGLE SE TERMINE PAR UN EXEMPLE CHIFFRÉ

Un taux sans exemple n'est pas une réponse opérationnelle. L'exemple montre **le calcul en entier**,
ligne par ligne, du montant de départ au montant d'impôt.

**Format de l'exemple :**

```
**Données :** [énoncé en une phrase]

| Étape | Calcul | Montant |
|---|---|---|
| Assiette de départ |  | X |
| Abattement éventuel | X × taux | Y |
| Impôt | Y × taux | **Z** |
```

Quand un calcul comporte **deux temps** — abattement puis taux — les deux temps apparaissent
séparément, jamais fondus en un seul taux effectif. Le taux effectif se donne **en plus**, jamais
à la place.

## LA STRUCTURE OBLIGATOIRE

| Ordre | Élément | Règle |
|---|---|---|
| 1 | En-tête | Public, rattachement, durée, référence `MC-FORM-FISC-AAAA-NNN`, prérequis, **sources** |
| 2 | **SOMMAIRE** | **Obligatoire, avant l'avant-propos**, en tableau avec les durées |
| 3 | Avant-propos | Pose le problème, pas le plan |
| 4 | Sections numérotées | Chacune avec sa durée |
| 5 | Cas chiffrés | Une section entière, plusieurs cas |
| 6 | Grille de contrôle | Tableau : point de contrôle, anomalie si… |
| 7 | Synthèse | Dix règles numérotées en toutes lettres |
| 8 | **Réserve méthodologique** | **Deux parties** : ce qui est établi sur le texte, ce qui reste ouvert |

## LA RÉSERVE MÉTHODOLOGIQUE

Elle se scinde toujours en deux.

**« Ce qui est établi sur le texte »** énumère les articles lus directement, avec leur source.

**« Ce qui reste à vérifier »** nomme les points ouverts. **Les taire est une faute.** Un point ouvert
signalé protège le lecteur ; un point ouvert dissimulé l'expose.

## LES CITATIONS

Tout texte de loi ou de doctrine se cite **verbatim, entre guillemets français, en bloc de citation**,
avec son article. Une paraphrase ne vaut jamais citation.

## QUAND UNE ÉDITION EN REMPLACE UNE AUTRE

L'avant-propos s'ouvre par **un tableau des corrections apportées** : ce que disait l'édition
précédente, ce que dit le texte. La version antérieure est **archivée**, jamais supprimée, dans
`_VERSIONS_ANTERIEURES`, suffixée `_vN_SUPERSEDE`.

## CE QUI EST PROSCRIT

- Un taux sans assiette
- Un tableau de taux sans colonne « Assiette »
- Deux impôts dans un même tableau
- Une règle sans exemple chiffré
- Un module sans sommaire
- Un module sans réserve méthodologique
- Une affirmation de doctrine présentée comme un texte
- Un point ouvert passé sous silence

## CONTRÔLE DE FORME AVANT PUBLICATION — DEUX VÉRIFICATIONS OBLIGATOIRES

Le contrôle qualité du script de publication ne teste que les **doubles** astérisques. Il laisse
passer les **astérisques simples orphelins**, qui s'impriment tels quels dans le PDF livré au client.

**Cas rencontré :** une citation en italique `*« Ce taux est de… »*` dont le texte est coupé par un
retour à la ligne. L'astérisque ouvrant reste seul sur sa ligne et **s'affiche dans le document**.

**Vérifier les deux, sur le fichier source, avant chaque publication :**

```python
def desequilibre(ligne):
    doubles = ligne.count("**") % 2                       # gras coupé
    simples = ligne.replace("**", "\x00").count("*") % 2  # italique coupée
    return doubles or simples
```

**La correction consiste à recoller les lignes**, jamais à supprimer l'astérisque : une citation doit
tenir sur une seule ligne source, si longue soit-elle.

> **Ne jamais utiliser un astérisque comme appel de note** en fin de titre : il est lu comme une
> emphase ouverte. Écrire la mention en toutes lettres.

## JEU DE CARACTÈRES — RÈGLE ABSOLUE

Les PDF sont produits par ReportLab avec les **polices de base du PDF** — Times, Helvetica, Courier — qui sont en **encodage Latin-1**. Tout caractère hors de cette couverture sort en **carré noir** dans le document livré, sans que l'extraction de texte ne permette de le détecter après coup.

**Caractères interdits, et leur remplacement :**

| Interdit | Code | Remplacer par |
|---|---|---|
| ᵉ ʳ (ordinal « 1ᵉʳ ») | U+1D49, U+02B3 | **1er**, **2e**, **XXe** — en lettres ordinaires |
| ⚠ | U+26A0 | rien — le gras suffit |
| ✅ | U+2705 | **✓** (U+2713), qui passe |
| ❌ | U+274C | **✗** (U+2717), qui passe |
| ⭐ | U+2B50 | rien |
| ☐ | U+2610 | **[ ]** |
| sélecteur de variante | U+FE0F | rien |

**Caractères vérifiés comme passant sans problème :** × ÷ − → ↔ ↑ ≤ ≥ ≠ ≈ Σ § ° · ½ œ ’ « » – — … € ✓ ✗

**Le contrôle est armé dans les deux scripts de publication** (`publish_pdf_mdc.py` et `publish_livrable_mdc.py`) : la présence de l'un de ces caractères dans la source **bloque la publication** au titre de la règle d'or, avant même la génération. Code de sortie 4.

**Autre motif de blocage à connaître :** le motif `](` d'un lien Markdown échoue au contrôle « aucun symbole Markdown résiduel ». Les renvois entre modules s'écrivent en texte simple, pas en lien.

> **Ne jamais réparer une bibliothèque entière par un script de remplacement sans garde-fou.** Toute passe globale sur les sources doit vérifier que **le nombre de lignes de chaque fichier est inchangé** avant d'écrire, et le miroir `FORMATION LMDC/MD` sert de sauvegarde de référence pour restaurer en cas de fausse manœuvre.
