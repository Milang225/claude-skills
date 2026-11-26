---
name: fix-xlsx-to-pdf-mdc-wrap
description: Bug corrigé le 23/09/2026 dans xlsx_to_pdf_mdc.py (texte de cellule qui chevauchait la colonne voisine) — script partagé par tous les classeurs Excel MDC convertis en PDF.
metadata:
  node_type: memory
  type: reference
  originSessionId: 82cefd56-2789-4448-990e-31cf0f64703a
  modified: 2026-09-23T17:41:38.216Z
---

`~/.claude/skills/mdc-expert/scripts/xlsx_to_pdf_mdc.py` construisait ses tableaux PDF avec des chaînes Python brutes dans les cellules `reportlab.platypus.Table`. Une chaîne brute ne s'enroule pas dans sa colonne : dès qu'elle est plus large que la largeur calculée, elle déborde visuellement sur la colonne voisine (texte superposé, illisible). Repéré sur `CHECKLIST_AUDIT_MDC_V2.xlsx` (colonnes C/D qui se chevauchaient), signalé par l'utilisateur via une capture d'écran.

**Correctif :** chaque cellule est maintenant un `reportlab.platypus.Paragraph` (style Helvetica/Helvetica-Bold, `textColor=DARK`), qui s'enroule correctement dans la largeur de sa colonne — la table grandit en hauteur au lieu de déborder en largeur. Le gras est injecté via des balises `<b>…</b>` dans le texte échappé (XML) plutôt que via un style `TableStyle(FONTNAME…)` externe, qui ne s'applique pas à un `Paragraph`. La troncature arbitraire à 90 caractères (qui coupait les textes longs avec « … », déjà visible sur l'onglet « Les 5 règles » de la V1) a aussi disparu : le texte s'affiche désormais en entier.

**Why :** le script sert à TOUS les classeurs Excel MDC publiés en PDF (point des impôts, analyses bancaires, checklists…). Le bug était latent depuis toujours mais invisible tant que les cellules restaient courtes ; il est devenu flagrant avec des libellés plus longs.

**How to apply :** le correctif est dans le script partagé, donc actif pour toute nouvelle conversion `xlsx_to_pdf_mdc.py`. Si l'utilisateur signale un PDF Excel MDC antérieur au 23/09/2026 avec du texte tronqué à « … » ou visuellement chevauché, le regénérer avec le script à jour suffit (pas besoin de retoucher le classeur source). Ne pas régénérer en masse tous les PDF existants sans demande explicite — beaucoup sont déjà remis à des clients.
