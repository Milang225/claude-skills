---
name: module-droit-des-societes
description: Module FORMATION_DROIT_DES_SOCIETES_CI créé le 24/09/2026 — statuts, associés, litiges ; articles AUSCGIE vérifiés sur le texte officiel archivé, avec la méthode de vérification automatique.
metadata:
  type: project
---

**Le module comblait un trou** : jusqu'au 24/09/2026, MDC n'avait **aucun module de droit des sociétés** — seulement des passages épars dans `FORMATION_APPORTS_DE_FONDS_CI`, `MODULE_44B` et `FORMATION_CESSATION_TRANSMISSION_CI`.

**Fichier :** `FORMATION LMDC/MD/FISCALITE_CI/_SOURCES_MD/FORMATION_DROIT_DES_SOCIETES_CI.md` · PDF dans `FORMATION LMDC/PDF/FISCALITE_CI/01_FONDATIONS/` + copie `BASE DOCUMENTAIRE LMDC/05_NOTES_CONSEIL/`. 15 modules : statuts (Art 10, 13) · **tableau des règles supplétives** (ce qui s'applique quand les statuts se taisent) · cession de parts · gérance · décisions collectives · conventions réglementées · réserve légale · droits du minoritaire · société bloquée · **ce que la comptabilité révèle d'un conflit** · 12 contrôles d'audit juridique · 15 pièges.

**LE TEXTE EST ARCHIVÉ** — `FORMATION LMDC/00_TEXTES_OFFICIELS/AUSCGIE_TEXTE.txt` (Acte uniforme révisé du 30/01/2014, 8 130 lignes). **Méthode de vérification à réutiliser pour tout module juridique :** découper le texte en index `{numéro d'article: contenu}` avec `re.split(r"\nArticle (\S+)\s*\n")`, puis vérifier que **chaque article cité dans le module existe** et que **chaque délai/majorité affirmé figure littéralement** dans l'article invoqué. Les 49 articles cités ont passé ce contrôle.

**Les trois trouvailles à exploiter** : **Art 356** — il est **interdit, à peine de nullité**, aux gérants et associés personnes physiques (et à leurs conjoints, ascendants, descendants, et toute personne interposée) d'emprunter à la société ou de s'y faire consentir un découvert : c'est le **compte courant débiteur**, donc **nul en droit ET revenu distribué en fiscalité** · **Art 319** — refuser l'agrément d'un cessionnaire **oblige à racheter**, à un prix fixé par expert · **Art 325** — le gérant associé **ne vote pas sa propre rémunération** et ses voix ne comptent pas dans la majorité.

**Points laissés en réserve** (section « Points à confirmer ») : le **capital minimum de la SARL en Côte d'Ivoire** — l'Art 311 dit « 1 000 000 F CFA sauf dispositions nationales contraires » et la CI a dérogé : **ne jamais l'affirmer sans revérifier le texte national** · le tarif des droits sur les cessions de droits sociaux · le régime ITS du gérant selon qu'il est majoritaire ou minoritaire.

**Décorticage fait dans la foulée** (règle [[decorticage-systematique-des-modules]]) : `CONTENU_MON_FISCALISTE/01_SCRIPTS_PAR_SEMAINE/S28-S29_SAISON_8_STATUTS_ET_ASSOCIES.md` — 42 scripts, 4 lives, 8 affiches. Et deux épisodes YouTube : `02_YOUTUBE/EP18-19_STATUTS_ET_POSTULATS.md`.

**Why :** c'est le socle juridique qui manquait sous les modules fiscaux — la moitié des anomalies de terrain (capital, comptes courants, rémunération du dirigeant) ont leur source dans le droit des sociétés, pas dans le CGI.
**How to apply :** module frère à créer un jour sur les **groupes de sociétés et la SAS**. Voir [[standard-qualite-travail-pro]] pour la méthode de vérification.
