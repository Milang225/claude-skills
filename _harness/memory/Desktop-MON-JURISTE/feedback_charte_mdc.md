---
name: Charte graphique MDC — exigence pro et navy/or
description: L'utilisateur exige des livrables visuellement professionnels (jamais "fades"), avec la charte navy + or MDC unifiée sur tous les supports (Word, Excel, PDF)
type: feedback
originSessionId: bf088578-8311-421f-8897-60f2abc8862e
---
**Règle** : tout livrable produit pour ou via MDC doit appliquer la charte graphique unifiée définie dans la **Section 8 du SKILL.md mdc-expert**.

**Why** : sur la mission TIM 7 (mai 2026), l'utilisateur a explicitement reproché à un Excel d'être « trop fade » et a exigé que les .md soient rendus « comme les autres » (= au format MDC navy/or). Il valorise visiblement une identité visuelle forte et constante : un livrable terne déclasse le cabinet auprès du client final.

**How to apply** :
- **Word (.docx)** : bandeau MDC en en-tête (fond navy `#1A1A2E`, texte or `#E8C547`), pied MDC complet (NCC, RCCM, capital, contact), Times New Roman 11 pt, titres Calibri navy, tableaux header navy + lignes alternées
- **Excel (.xlsx)** : bandeau de marque sur 3 lignes en haut de chaque feuille, headers de tableaux navy/blanc, lignes alternées blanc/`#F4F4F8`, sous-totaux or pâle `#F5E5A5`, totaux navy/blanc, format `#,##0_- "FCFA"` avec négatifs en rouge, volets figés sous les en-têtes, pied MDC en bas
- **PDF** : bandeau navy/or en marge négative, encadrés colorés pour synthèses/alertes (rouge clair `#F8E8E8` / crème `#FFFBE8`), score en grand corps (42 pt), pied MDC sur fond gris perle, page-break HTML
- **Markdown source** : conserver les `.md` à côté des `.docx` pour réédition future

**Outils prêts** : utiliser `~/.claude/skills/mdc-expert/scripts/md_to_docx_mdc.py` pour la conversion Markdown → Word, et le template `redesign_excel_mdc_template.py` pour le redesign Excel. Pour PDF MDC : `mcp__Desktop_Commander__write_pdf` avec markdown HTML/CSS inline.

**Ne jamais** :
- Livrer un Excel par défaut (sans header coloré, sans format FCFA, sans bordures)
- Produire un Word sans bandeau ni pied MDC
- Mélanger plusieurs polices ou palettes
- Oublier la mention « Le Cabinet MDC n'est pas assujetti à la TVA »
