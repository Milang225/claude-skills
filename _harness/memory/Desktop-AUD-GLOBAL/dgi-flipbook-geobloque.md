---
name: dgi-flipbook-geobloque
description: "Les flipbooks EBOOK de la DGI (doctrine fiscale, BODGI) sont géo-bloqués hors Côte d'Ivoire"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 97d7ebee-e494-4fbb-88fa-c1d8afa9ef17
---

Les publications de la DGI au format **flipbook** (`https://www.dgi.gouv.ci/assets/documents/EBOOK/...` et `.../DOCTRINE_FISCALE_2026/`) ne sont **pas récupérables à distance** depuis l'environnement de l'agent :

- pages composées d'**images sans couche de texte** (pas d'OCR natif) ;
- les fichiers image (`files/mobile/N.jpg`, `large`, `thumb`) **redirigent vers `https://secure.sndi.ci/Interdit.xml`** = accès interdit hors réseau autorisé / Côte d'Ivoire (SNDI = opérateur informatique de l'État) ;
- l'index de recherche `mobile/javascript/search_config.js` ne contient que le **sommaire** (reste vide) ;
- `basic-html/pageN.html` est en **UTF-16** et ne contient que les titres de page, pas le corps.

**How to apply** : ne pas tenter de scraper ces flipbooks pour en extraire le contenu — seul le **sommaire/structure** est obtenable. Pour intégrer le contenu à `fiscal-knowledge/`, demander à l'utilisateur le **PDF source** (export depuis un poste en CI). Les PDF hébergés sur `dgbf.ci` (annexes fiscales), eux, sont en texte natif et téléchargeables — mais l'utilisateur a demandé de ne pas conserver les docs DGBF. Voir [[dgi-flipbook-geobloque]] et le fichier `fiscal-knowledge/11-procedures-actes-dgi.md` § D.
