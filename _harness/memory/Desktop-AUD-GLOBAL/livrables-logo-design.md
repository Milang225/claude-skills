---
name: livrables-logo-design
description: "Le logo MDC doit figurer sur chaque document produit ; design « papier à en-tête cabinet » exigé (le gérant trouvait l'ancien rendu « trop IA »)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 46899554-5100-4dba-a8f0-764b4aac0f2f
---

Le gérant exige (juillet 2026) que **tout document MDC porte son logo** (`~/.claude/skills/mdc-expert/scripts/logo-mdc.jpg`) et jugeait l'ancien rendu (bandeau navy plein, tableaux à grille) « trop IA ».

**Why:** les livrables partent chez des clients ; ils doivent ressembler à du papier à en-tête de cabinet, pas à un template généré.

**How to apply:** utiliser les générateurs `build_mdc_docx_hf.py` / `build_mdc_pdf.py` / `generate_livrable_mdc.py` (redesignés juillet 2026) qui intègrent nativement : logo à gauche + identité à droite + double filet navy/or sur chaque page, **filigrane « CONFIDENTIEL » en diagonale** (navy ~6-7 % opacité), titres centrés à filet or, tableaux à filets horizontaux fins sans grille verticale, montants alignés à droite, lignes TOTAL sur fond or pâle. Conditions de paiement par défaut des propositions : **paiement intégral avant le démarrage des travaux**. Ne jamais régresser vers le bandeau texte seul. Contrôler visuellement (rendu PyMuPDF) avant livraison. Voir aussi [[livrables-sans-symboles]].
