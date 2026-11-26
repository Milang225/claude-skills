---
name: glyphes-interdits-pdf-mdc
description: Les PDF MDC sont en polices Latin-1 ; certains caractères Unicode sortent en carrés noirs et sont bloqués à la publication
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e00f2fb8-9eee-43d3-bb66-3409ca1aaa5d
  modified: 2026-09-21T00:41:16.964Z
---

Les PDF de la bibliothèque MDC sont produits par ReportLab avec les polices de base du PDF (Times, Helvetica, Courier), **en encodage Latin-1**. Tout caractère hors de cette couverture s'imprime en **carré noir** dans le document livré.

Interdits, avec leur remplacement : **ᵉ ʳ** (l'ordinal « 1ᵉʳ ») → `1er`, `2e` · **⚠** et **⭐** → rien · **✅** → `✓` · **❌** → `✗` · **☐** → `[ ]` · U+FE0F → rien.
Vérifiés comme passant : × ÷ − → ↔ ↑ ≤ ≥ ≠ ≈ Σ § ° · ½ œ ’ « » – — … € ✓ ✗

**Why:** le 21/09/2026, BILE Fils Séverin a signalé un « 1■■ mai 2026 » dans un module publié. Le contrôle qualité ne testait que le Markdown résiduel, et l'extraction de texte d'un PDF ne révèle pas le défaut — seul un rendu à l'image le montre. Sa consigne : « je ne veux pas voir ce genre de choses là dans un document produit par toi ».

**How to apply:** le garde-fou est installé dans `publish_pdf_mdc.py` et `publish_livrable_mdc.py` — la présence d'un de ces caractères dans la source bloque la publication (code 4) au titre de la règle d'or. Détail complet dans `~/.claude/skills/fiscalite-ci/reference/NORME_REDACTION_MODULES.md`. Le motif `](` d'un lien Markdown bloque aussi : les renvois entre modules s'écrivent en texte simple.

Corollaire appris le même jour : **toute passe globale de remplacement sur les sources doit vérifier que le nombre de lignes de chaque fichier est inchangé avant d'écrire**. Une regex expérimentale laissée dans un script a fusionné des lignes dans 116 fichiers ; le miroir `~/Documents/FORMATION LMDC/MD/` a permis la restauration. Voir [[sync-formation-lmdc-apres-publication]].

**Saut de page** (ajoute le 08/10/2026) : une ligne contenant exactement `[SAUT DE PAGE]` dans la source Markdown insere un saut de page reel, en PDF (`build_mdc_pdf.py`) comme en Word (`md2docx_mdc.js`). Le marqueur est consomme, jamais imprime. Il sert aux fiches recto-verso et a tout document dont la coupe doit etre maitrisee. Sauvegardes : `*.bak-pagebreak`. Verifie sans regression de mise en page sur les modules existants.
