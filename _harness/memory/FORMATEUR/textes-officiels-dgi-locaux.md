---
name: textes-officiels-dgi-locaux
description: "Les textes fiscaux ivoiriens de référence et le plan de comptes SYSCOHADA sont archivés en local, en PDF cherchable et en texte brut grep-able"
metadata:
  type: reference
---

Le dossier `Documents/FORMATIONS MDC/00_TEXTES_OFFICIELS_DGI/` contient les sources officielles suivantes, chacune en **texte brut interrogeable par grep** :

| Fichier | Contenu | Volume |
|---|---|---|
| `CGI_2025_TEXTE_INTEGRAL.txt` | Code général des Impôts 2025, à jour au 3 janvier 2026 | 1 093 005 car. |
| `DOCTRINE_FISCALE_2026_TEXTE.txt` + `.pdf` | Doctrine fiscale 2026, notes de service de portée générale, 338 pages | 737 496 car. |
| `BULLETIN_OFFICIEL_DGI_2026_TEXTE.txt` + `.pdf` | Bulletin officiel DGI 2026 = note de service n° 00511 du 27 janvier 2026, analyse de l'annexe fiscale 2026, 172 pages | 329 270 car. |
| `CODE_MINIER_2014_TEXTE.txt` | Loi n° 2014-138 du 24 mars 2014 portant Code minier | 106 062 car. |
| `PLAN_DE_COMPTES_SYSCOHADA_TEXTE.txt` | Plan de comptes SYSCOHADA révisé, **981 comptes** avec intitulés, extrait de l'onglet « Balance » de la liasse SMT du portail e-impôts (`Documents/ARCHIVES DOCUMENTS/DOCS DGI/LIASSE SMT (2).xlsx`) | 981 lignes |

**Why:** ces documents ne sont pas diffusés en PDF sur le site de la DGI. Ils sont publiés dans un **livre feuilletable** dont les pages sont de simples images, sans couche de texte. Les reconstituer coûte cher (téléchargement page par page puis reconnaissance optique), et les recherches web sur ces sujets ramènent des paraphrases souvent fausses.

**How to apply:** interroger ces fichiers **avant** toute recherche web sur une question fiscale ivoirienne. Attention aux césures de mise en page dans le CGI (`so-ciété`, `bénéfi-ces`) : chercher des motifs courts. Voir [[cgi-2025-texte-integral]] pour la méthode d'extraction du CGI.

**Le plan de comptes** se grep par numéro en début de ligne (`^601`). Ce n'est pas l'AUDCIF, qui reste non archivé : deux écarts connus sont signalés en tête du fichier (absence du compte 13 Résultat net, et du seul en-tête 62 Services extérieurs A). Les **liasses fiscales officielles en Excel** du dossier `DOCS DGI` — SMT et système normal — portent en outre les maquettes des états et **les formules de report balance vers liasse**, qui font autorité pour les correspondances compte / ligne. Voir [[analyse-fiscale-quatre-sources]].

**Méthode pour un livre feuilletable de la DGI** — les pages sont à `<url_du_livre>/files/mobile/N.jpg`. Trouver la dernière page par dichotomie, télécharger, agrandir à 2600 px avec `sips -Z 2600`, puis passer `mdc-ocr`. Le PDF cherchable se fabrique en réinsérant le texte reconnu en calque invisible avec PyMuPDF (`render_mode=3`).
