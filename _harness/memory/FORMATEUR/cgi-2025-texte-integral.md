---
name: cgi-2025-texte-integral
description: "Le texte intégral du CGI ivoirien 2025 est archivé en local et grep-able — à interroger avant toute recherche web sur un article"
metadata:
  type: reference
---

Le **Code général des Impôts ivoirien, édition 2025** (à jour au 3 janvier 2026) est archivé en texte brut dans `Documents/FORMATIONS MDC/FISCALITE_CI/_SOURCES_MD/CGI_2025_TEXTE_INTEGRAL.txt` (~1 Mo, 10 500 lignes). Les articles y sont repérables par `grep -n "Art. NNN –"`.

Source : African Tax Legislation Atlas, `https://a-tla.org/cote-divoire/code-general-des-impots`, qui publie le Code en **.docx** téléchargeable. Extraction : `zipfile` sur `word/document.xml` puis suppression des balises.

**Why:** les recherches web sur un article du CGI ramènent des paraphrases approximatives, parfois fausses (un extrait en ligne donnait 5 % et 400 000 F pour l'IMF, contre 0,5 % et 3 000 000 F dans le texte). Les PDF de la DGI ne sont pas lisibles par WebFetch. Disposer du texte intégral en local supprime cette source d'erreur et permet de vérifier au mot près.

**How to apply:** interroger ce fichier **avant** toute recherche web sur une question de CGI. Attention : l'extraction laisse des césures de la mise en page (`so-ciété`, `bénéfi-ces`), donc chercher des motifs courts ou tolérants. Voir [[questions-germees-avant-reponse]] : la recherche dans le texte intégral est ce qui permet de répondre aux questions germées plutôt que de les laisser ouvertes.
