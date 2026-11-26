# LES SOURCES DU SKILL — OÙ ELLES SONT, COMMENT LES INTERROGER

**Dossier unique :** `~/Documents/ARCHIVES DOCUMENTS/FORMATIONS MDC/00_TEXTES_OFFICIELS_DGI/`

| Fichier | Ce que c'est | Format | Fiabilité |
|---|---|---|---|
| **`CGI_2026_TEXTE_INTEGRAL.txt`** | **Code général des Impôts, édition 2026** — 1 162 articles, 712 pages sources, 3 284 835 caractères | texte | **Exacte** — issue de HTML, aucune reconnaissance de caractères |
| **`CGI_2026.pdf`** | Le même, en PDF **cherchable**, 1 520 pages, 11 Mo. En-tête de chaque page : le numéro de page source | PDF | **Exacte** |
| `DOCTRINE_FISCALE_2026_TEXTE.txt` · `.pdf` | Doctrine fiscale 2026, notes de service de portée générale, 338 p. | texte + PDF cherchable 44 Mo | Bonne — reconnaissance de caractères |
| `BULLETIN_OFFICIEL_DGI_2026_TEXTE.txt` · `.pdf` | Bulletin officiel 2026 = note n° 00511 du 27 janvier 2026, analyse de l'annexe fiscale 2026, 172 p. | texte + PDF cherchable 21 Mo | Bonne — reconnaissance de caractères |
| `CODE_MINIER_2014_TEXTE.txt` | Loi n° 2014-138 du 24 mars 2014 | texte | Bonne |
| `AUSCGIE_TEXTE.txt` | Acte uniforme OHADA, sociétés commerciales et GIE | texte | Bonne |
| `CGI_2025_TEXTE_INTEGRAL_ARCHIVE.txt` | Édition 2025, **archive** | texte | Césures de mise en page |
| **`LOI_BANCAIRE_UMOA_2023_TEXTE.txt`** · `.pdf` | **Loi uniforme portant réglementation bancaire dans l'UMOA du 16 juin 2023**, en vigueur depuis janvier 2024, 94 p. Remplace la loi de 2007 | texte + PDF | Exacte |
| **`CIPRES_CONVENTION_2006.txt`** | **Convention multilatérale de sécurité sociale de la CIPRES** et son Arrangement administratif, 43 p. | texte | Exacte |
| **`CODE_INVESTISSEMENTS_ORD_2024-857_TEXTE.txt`** · `.pdf` | **Ordonnance n° 2024-857 du 30 septembre 2024**, qui **modifie** le Code des investissements | texte + PDF | Exacte |
| **`NOTE_DGI_050_2024_CODE_INVESTISSEMENTS_TEXTE.txt`** · `.pdf` | **Note DGI n° 050 de 2024** — modalités de mise en œuvre des avantages accordés **en phase d'exploitation** aux entreprises agréées | texte + PDF | Bonne — OCR |
| `CODE_INVESTISSEMENTS_PRESENTATION_CEPICI.pdf` | Présentation du CEPICI | PDF | Document de communication |

## LA SOURCE DE RÉFÉRENCE EST LE CGI 2026

**Toujours l'interroger en premier.** L'édition 2025 ne sert qu'à retrouver un état antérieur, et
l'édition 2026 rend même cela rarement nécessaire : elle porte, sous chaque article modifié, les
mentions des versions **2025** et **2024**.

## COMMENT CHERCHER

```bash
F="$HOME/Documents/ARCHIVES DOCUMENTS/FORMATIONS MDC/00_TEXTES_OFFICIELS_DGI/CGI_2026_TEXTE_INTEGRAL.txt"

grep -n "Art. 92" "$F"                    # atteindre un article
sed -n '3894,3915p' "$F"                  # lire autour
grep -n -i "minimum forfaitaire" "$F"     # chercher une notion
grep -n "===== PAGE" "$F" | head          # repères de pagination source
```

> **Piège de recherche à connaître.** Les numéros d'articles apparaissent tantôt `Art. 92`, tantôt
> `Art. 92 ` avec une espace finale. **Ne jamais ancrer sur un motif strict** du type `^Art\. 63 –`,
> qui existe dans l'édition 2025 mais pas dans l'édition 2026. Chercher `Art. 63` suffit.

## COMMENT CES SOURCES ONT ÉTÉ OBTENUES

**Le CGI 2026** vient de `cgici.com`, une application JavaScript. Les pages **ne sont pas** à
`cgici.com/page-N.html`, qui renvoie 404, mais à **`cgici.com/V2026/page-N.html`**, de 0 à 713.
Seule l'observation du trafic réseau pendant une navigation réelle le révèle. Le contenu est du
HTML, donc du texte exact.

**La Doctrine et le Bulletin** viennent de livres feuilletables de `dgi.gouv.ci`, dont les pages
sont des **images**. Méthode : trouver la dernière page par dichotomie sur le code HTTP, télécharger
`<url>/files/mobile/N.jpg`, agrandir avec `sips -Z 2600`, puis `mdc-ocr`. Le PDF cherchable se
fabrique en réinsérant le texte reconnu en calque invisible avec PyMuPDF, `render_mode=3`.

**Le CGI 2025 archivé** vient de `a-tla.org`, qui publie le Code en `.docx`.

## LE CODE DES INVESTISSEMENTS — CE QUI EST EN LOCAL ET CE QUI NE L'EST PAS

> **Attention : le Code des investissements lui-même n'est PAS archivé.**

Le Code est l'**ordonnance n° 2018-646 du 1er août 2018**, modifiée par l'**ordonnance n° 2019-1088 du
18 décembre 2019**, puis par l'**ordonnance n° 2024-857 du 30 septembre 2024**.

| Texte | En local ? |
|---|---|
| Ordonnance **2018-646**, le Code lui-même | **Non** |
| Ordonnance **2019-1088**, première modification | **Non** |
| Ordonnance **2024-857**, seconde modification | **Oui**, texte et PDF |
| **Note DGI n° 050 de 2024**, avantages en phase d'exploitation | **Oui**, texte et PDF |

**Conséquence de méthode : pour toute question sur le Code des investissements, l'ordonnance 2024-857
seule ne suffit pas.** Elle ne donne que les articles modifiés, sans le texte d'origine. Il faut se
procurer l'ordonnance 2018-646 consolidée avant de répondre sur les conditions d'agrément, les
régimes, les zones ou les avantages en phase d'investissement.

La **note DGI n° 050** couvre en revanche entièrement les avantages de la **phase d'exploitation**.

**Rappel utile du corpus :** le régime du Code des investissements est en **non-cumul absolu** avec la
réduction pour investissement de l'article 110 du CGI et avec les agréments minier et pétrolier. Un
sous-traitant minier **sans agrément** relève du droit commun.

## LA RÈGLE

> **Ne jamais répondre de mémoire ni depuis une recherche web sur une question de fiscalité
> ivoirienne. Ces fichiers contiennent le texte. Les lire.**

## ACTE UNIFORME OHADA — DROIT COMMERCIAL GÉNÉRAL (2010)

| | |
|---|---|
| **Fichier texte** | `00_TEXTES_OFFICIELS_DGI/AUDCG_DROIT_COMMERCIAL_2010_TEXTE.txt` |
| **PDF** | `00_TEXTES_OFFICIELS_DGI/AUDCG_DROIT_COMMERCIAL_2010.pdf` — 67 pages |
| **Version** | Acte uniforme **révisé**, adopté le 15 décembre 2010 à Lomé, publié au JO OHADA n° 21 du 15 février 2011, en vigueur le 15 mai 2011 |
| **Origine** | téléchargé le 23 septembre 2026 depuis acpce.cg ; texte extrait par PyMuPDF, donc **exact** et non issu d'un OCR |

**Ce qu'il sert à trancher — Livre VI, Intermédiaires de commerce :**

| Article | Contenu |
|---|---|
| **169** | définition de l'intermédiaire de commerce |
| **170** | l'intermédiaire de commerce **est un commerçant** |
| **180 / 181** | **le test décisif** : l'acte lie le représenté si le tiers connaissait sa qualité ; il lie l'intermédiaire dans le cas contraire ou en cas de contrat de commission |
| **182 à 187** | responsabilité, **remboursement des avances et frais** (186), **reddition de comptes** (187) |
| **188 à 191** | cessation du mandat |
| **192 à 204** | **commissionnaire** : agit « en son propre nom mais pour le compte du commettant » (192), prix (200), risques (201), **ducroire** (202), mauvaise foi (203) |
| **208 à 212** | **courtier** : met en rapport (208), indépendance (209), interdiction d'opérer pour son compte (211), rémunération en pourcentage (212) |
| **216 et 217** | **agent commercial** : mandataire agissant « au nom et pour le compte » (216) |

**Module qui l'exploite** : MC-FORM-FISC-2026-013B — Le commissionnaire et le mandataire.
