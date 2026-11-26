---
name: corpus-lpf-dans-le-fichier-cgi
description: Le Livre de procédures fiscales est à la SUITE du CGI dans CGI_2026_TEXTE_INTEGRAL.txt ; chercher un article par son seul numéro renvoie l'article du CGI, jamais celui du LPF.
metadata:
  type: reference
---

`~/Documents/FORMATION LMDC/00_TEXTES_OFFICIELS/CGI_2026_TEXTE_INTEGRAL.txt` contient **deux codes** :
le Code général des impôts, puis le **Livre de procédures fiscales** à partir d'environ la ligne 25 000.
Le Code minier 2014, la Doctrine fiscale 2026 et le Bulletin officiel DGI 2026 sont dans le même dossier.

**Pourquoi :** les deux codes ont des articles qui portent les mêmes numéros. Une recherche sur
« Art. 161 » renvoie l'article du CGI (valeur marchande des immeubles urbains) alors que l'article
cherché est souvent celui du LPF (intérêts de retard). Une recherche qui s'arrête au premier résultat
conclut donc à tort que le LPF n'est pas archivé, ou qu'un article n'existe pas.

**Comment l'appliquer :** pour un article du LPF, chercher à partir de la ligne 25 000
(`python3`, parcours des lignes avec un index de départ), ou se repérer aux intitulés voisins.
Vérifié le 05/11/2026 : LPF art. 161 = intérêt 5 % + 0,5 %/mois, porté à 10 % + 1 % pour les retenues,
la TVA et les taxes indirectes, **sans aucune majoration de 25 %** ; art. 162 = 15/30/100 %, porté à
30/60/150 % ; art. 163 = taxation d'office, jusqu'à 100 % ; art. 2 bis = vérification générale **sans
pénalités** sous 200 M de CA, sans condition d'ancienneté ; art. 170 quinquies = 5 000 000 par registre
non tenu, majoré de 500 000 par mois sur requête de l'Administration.
Plusieurs livrables TIM 7 citaient « l'article 161 du CGI » pour une majoration de 25 % qui n'existe
dans aucun des deux codes. Même nature de manque à combler que [[corpus-lbcft-a-archiver]].
