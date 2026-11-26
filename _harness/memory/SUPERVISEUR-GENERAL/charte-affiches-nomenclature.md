---
name: charte-affiches-nomenclature
description: Charte visuelle « Nomenclature » des affiches de live MDC + générateurs Python (affiches PNG et PDF brandés) — couleurs, polices et structure exactes.
metadata:
  type: reference
---

**Charte « Nomenclature »** (le mouvement visuel est décrit dans `~/Documents/FORMATION LMDC/MD/COMMUNICATION/PHILOSOPHIE_NOMENCLATURE.md`) : deux teintes seulement, une dominante profonde qui absorbe, une chaude qui découpe et **désigne** ; un élément domine, tout le reste chuchote ; deux familles typographiques — large pour l'énoncé, mécanique étroite pour la mesure ; jamais de paragraphe ; masse lourde en bas.

**Couleurs exactes** (relevées sur les affiches du gérant) : fond `#1A1A2E` (26,26,46) · ocre `#E0A55A` (224,165,90) · blanc cassé `#F0EBE1` · gris mono `#7C7C92` · segment inactif `#2E2E48`.
**Polices** : titres `/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf` · mono `/System/Library/Fonts/Menlo.ttc`.
**Logo** : `~/Desktop/02_MDC INTERNE/projets-vps/crm/backend/logo-mdc.jpg` — déjà sur fond ocre, à normaliser sur l'ocre exact avant collage.

**Structure d'une affiche** : filet ocre → ligne mono (LA MAISON DE LA CONFORMITÉ | référence technique) → titre condensé 2-4 lignes dont **une en ocre** → **schéma de démonstration** (segments · étages · colonnes · noyau) → bloc de données (label ocre / valeur blanche / source grise) → note grise → bandeau ocre (logo + EN DIRECT CE SOIR + date + FACEBOOK - TIKTOK).
**Formats** : Facebook 1080×1350 et TikTok 1080×1920. **Pas d'accent ni d'emoji** dans les textes d'affiche (DIN Condensed les rend mal) — écrire en capitales sans accents.

**Générateurs** dans `CONTENU_MON_FISCALISTE/AFFICHES/_SOURCES/` : `generer_affiches.py` (moteur, 4 types de schémas) · `affiches_saison3.py` à `affiches_saison7.py` (les specs + `DEBUT_SAISON1` à ajuster si le lancement bouge).

**Le moteur se contrôle lui-même** (corrigé le 24/09/2026) : il imprime une alerte `!` quand une valeur ne tient pas dans sa colonne ou quand le bloc de données est resserré contre le schéma. **Une génération propre ne produit AUCUNE alerte** — sinon l'affiche a du texte coupé ou superposé. Trois garde-fous y pourvoient : l'espacement des labels se desserre quand la place manque, la source passe à la ligne (à droite, en gris) plutôt que d'écraser la valeur, et la hauteur des étages se réduit au-delà de 4 lignes. **Ne jamais se fier à l'œil sur une seule affiche : c'est l'absence d'alerte sur l'ensemble qui vaut contrôle.**

**Les PDF ne se fabriquent PAS ici.** Tout document passe par le skill `redaction` → `publish_pdf_mdc.py` (et `publish_livrable_mdc.py` pour le DOCX), qui portent la charte documentaire MDC : logo, bandeau « Agence de Notation Administrative », filigrane CONFIDENTIEL, pied légal NCC/RCCM/capital, contrôle qualité bloquant. **Ne jamais écrire de générateur PDF maison** — c'est la charte des affiches qui est spécifique, pas celle des documents.

**Why :** le gérant annonce chaque live par un post Facebook + une affiche le jour même ; les affiches et les PDF font partie du décorticage de chaque module.
**How to apply :** une affiche par live, générée en même temps que les scripts de la semaine. Voir [[decorticage-systematique-des-modules]] (pièce n°3 des 18) et [[positionnement-architecte-mon-fiscaliste]].
