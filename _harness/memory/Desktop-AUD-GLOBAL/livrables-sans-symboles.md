---
name: livrables-sans-symboles
description: Aucun symbole Markdown (* > #) ne doit apparaître en clair dans les livrables clients MDC
metadata:
  type: feedback
---

Le gérant ne veut **aucun symbole Markdown visible** (`*`, `**`, `***`, `>`, `#`, `<br>`) dans les documents clients livrés (Word/PDF).

**Why:** plusieurs livrables sortaient avec des astérisques (italique/gras) et des `>` (citations) affichés en clair → non professionnel.

**How to apply:** les générateurs `build_mdc_pdf.py` et `build_mdc_docx_hf.py` ont été corrigés pour rendre `*italique*`, `**gras**`, `***gras+italique***`, `> citation` (encadré crème/or) et `<br>` (saut). La mention TVA s'écrit en `***...***` (gras+italique). Toujours vérifier le rendu (un symbole visible = bug à corriger). Voir [[rangement-dossier-clients]].
