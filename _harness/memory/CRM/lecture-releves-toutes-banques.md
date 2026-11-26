---
name: lecture-releves-toutes-banques
description: "Les relevés déposés se lisent depuis la base documentaire (sans réimport), et le lecteur PDF a été réparé à la racine — quatre causes de « il n'y a rien »"
metadata: 
  node_type: memory
  type: project
  originSessionId: e1fe21d5-7734-4db9-8597-05641de9260d
  modified: 2026-08-26T05:02:08.367Z
---

**26/08/2026 — « je ne veux pas avoir à importer un relevé si j'ai déjà un dossier relevé qui est fourni ; le système doit lire tous les relevés à l'intérieur et les analyser cumulativement ou séparément ».**

La plateforme va chercher les relevés **là où ils sont archivés**. Sélection : un fichier est proposé s'il est rangé dans un dossier dont un segment porte *banque / relevé / bancaire*, ou si son nom le dit — sinon elle proposerait les factures et les pièces de personnel qui vivent dans le même dépôt. Deux modes : **séparé** (chaque mois enregistré avec SON bouclage — le mode qui protège) et **cumulé** (vue d'ensemble, rien enregistré). Un mois refusé n'empêche pas les autres mais est nommé.

**⚠ Le lecteur PDF était cassé de quatre façons, et l'échec était SILENCIEUX (« j'ai importé un relevé, le système dit qu'il n'y a rien »).** Diagnostiqué sur deux relevés réels du dépôt :
1. **`Td` ne s'écrivait qu'en majuscule** dans la regex (`TD?`) : CORIS BANK n'émet que des `BT x y Td (texte) Tj ET` → toutes les abscisses restaient à 0, colonnes inséparables. `BT` doit aussi remettre la matrice de texte à l'identité (norme PDF 32000 §9.4.2).
2. **`/Font 7 0 R`** — un dictionnaire de polices par **référence** n'était pas suivi (seule la forme en ligne `/Font <<…>>` l'était) → aucune table glyphe → caractère → tout le corps du tableau perdu, seuls les en-têtes (écrits en clair) passaient.
3. **Les montants sont cadrés à DROITE avec des espaces** : l'abscisse de départ du fragment tombe à gauche de son en-tête. Une fenêtre fixe rangeait donc les crédits en débits. → **affectation à la colonne dont l'en-tête est la PLUS PROCHE**, jamais une fenêtre. (Même doctrine que pour les balances.)
4. **Formats de banque** : `01-May-2026` n'était pas une date, `Mouvement Debiteur/Crediteur` (UBA) pas un en-tête, `Total des crédits :` / `Solde à l'ouverture :` / `Solde de clôture :` / `Solde au : <date> <montant>` pas des totaux. Un « Solde au … » **avant** la première opération est l'ouverture, **après** c'est la clôture.

Ajouté aussi : repli vers l'OCR quand la couche texte existe mais ne rend **aucune** opération (une couche texte présente ne prouve pas qu'elle soit lisible), et un objet sans flux n'hérite plus du flux de l'objet suivant.

**La CHAÎNE DES SOLDES (27/08/2026).** Un relevé imprime le solde APRÈS chaque opération : deux soldes consécutifs encadrent le mouvement, que la banque écrit donc **deux fois** (en montant, et en variation de solde). C'est le triangle bancaire appliqué ligne à ligne. La plateforme s'en sert pour (a) **contrôler** — un montant lu qui contredit la variation est signalé avec SA ligne, (b) **compléter** — un montant perdu par l'OCR est rendu par la variation, (c) **rectifier** — un montant mal lu est redressé, parce que le solde est corroboré par toute la chaîne alors que le montant n'est écrit qu'une fois. ⚠ Garde-fou : une lecture redressée n'est **jamais** certifiée par sa propre arithmétique — si le relevé ne porte aucun total imprimé permettant de la vérifier, l'import est **refusé**. Et on ne crée jamais une opération sans ligne au relevé : une rupture inattribuable reste une rupture, nommée.

**Un relevé ne tient pas dans le mois de son dossier.** Le fichier de GLOBE est rangé dans « 06 Juin » et couvre du 1er mai au 31 juillet. **C'est la date de l'opération qui décide de son mois**, jamais le nom du dossier — sinon on déclare en juin la TVA de mai. Chaque mois ouvre sur la clôture du précédent (calculée, jamais inventée), et le débordement n'écrase pas un mois déjà servi par son propre fichier.

**Résultat mesuré en production** : CORIS (IVOIRE MINING) 32 opérations lues en 0 s, **bouclage au franc des deux côtés** (débits 55 647 619 · crédits 67 499 500 · clôture 11 851 881). GLOBE (UBA) est un **scan photo** : d'abord 9 opérations et un refus, puis **22 opérations et crédits 36 140 155 = le total imprimé au franc**, grâce à la chaîne des soldes (1 montant rectifié de 50 F, 1 montant complété de 1 221 025 F, tous deux nommés en observation). Non-régression prouvée : **100 PDF du dépôt de production relus, 99 identiques, 1 mieux lu, 0 dégradé**.

Test durable : `tests/test_lecture_banques.js` (fabrique les deux familles de PDF à la main et exige le bouclage) + `tests/test_releves_depot.js`. Voir [[crm-architecture-deploy]] et [[depot-base-documentaire]].
