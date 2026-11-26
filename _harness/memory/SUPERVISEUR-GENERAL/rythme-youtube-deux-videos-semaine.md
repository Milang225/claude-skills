---
name: rythme-youtube-deux-videos-semaine
description: DÉCISION (24/09/2026) — la chaîne YouTube passe à 2 vidéos par semaine, en 1 long le dimanche + 1 court le mercredi ; l'année complète est écrite (52+52).
metadata:
  type: project
---

**Le gérant a arrêté le rythme YouTube le 24/09/2026**, en deux temps : d'abord 1 vidéo par semaine au lieu d'une tous les 15 jours, puis **2 par semaine**. Le format du second rendez-vous a été choisi par lui : **1 long + 1 court** (et non 2 longs, ni 1 long + 1 entretien).

**L'architecture retenue :**
- **Dimanche — le long**, format A chapitré, 10 à 17 min. 52 épisodes + l'épisode de lancement en semaine 0.
- **Mercredi — le court**, 3 à 5 min, **une seule idée**, adossé au long de la MÊME semaine dont il extrait un point et le déplie entièrement. 52 courts.
- **Un seul tournage pour les deux**, le dimanche : le long puis le court dans la foulée, même tenue, même décor. C'est ce qui rend le rythme tenable en plus des 2 sessions TikTok et des 2 lives.

**NOMMAGE — règle posée par le gérant le 25/09/2026, à respecter pour tout nouveau script :**
- **numérotation par séquence** : le numéro d'épisode suit l'ordre de diffusion. L'épisode de la semaine 7 porte le numéro 7. Le court de la même semaine porte le même numéro. Plus aucun décalage entre `Sn` et `EPn`.
- **sans zéro initial** : `S1_EP1_TITRE.md`, pas `S01_EP01_`. Longs dans `04_YOUTUBE/`, courts dans `04_YOUTUBE/COURTS/Sn_CTn_TITRE.md`. Note de format : `04_YOUTUBE/00_FORMAT_COURT.md`.
- **Conséquence à connaître** : le tri alphabétique du Finder devient S1, S10, S11… S2. Les générateurs ont été corrigés pour trier **numériquement** (`_generer_prompteur_html.py`, fonction `rang()`), mais tout nouveau script qui liste ces fichiers doit trier sur le nombre, jamais sur le nom.

**NUMÉROTATION DES SÉQUENCES (25/09/2026)** — chaque section d'un script porte son rang de tournage :
`## SÉQ. 3/9 · 02:40 — LES TROIS ENGAGEMENTS`. Le prompteur l'affiche dans un cadre devant l'horodatage.
**Seules les séquences de tournage sont numérotées** : une section dont le titre n'est pas en CAPITALES (une fois retiré un suffixe `*(toi)*`) est une section de production — *Le titre*, *La miniature*, *À vérifier avant tournage*, *Les extraits TikTok à découper* — et elle ne porte ni horodatage ni numéro, et ne compte pas dans la durée. L'outil `04_YOUTUBE/_recaler_horodatages.py` applique la règle, recalcule les horaires à 140 mots/min, renumérote et corrige la durée annoncée ; il est **idempotent**, à relancer après toute modification d'un script.

**Règle de calibrage apprise le même jour :** les durées annoncées dans les fiches étaient fausses sur toute la série (jusqu'à 20-22 min annoncées pour 6 min de texte réel). **Mesurer le texte réellement dit, recalculer les horodatages section par section à 140 mots/minute, et corriger la durée annoncée** — le script de recalage est dans le scratchpad de session, à refaire à chaque nouveau lot. Voir [[standard-qualite-travail-pro]].

**Why :** le rythme et le format conditionnent toute la production (tournage, montage, matière puisée dans les modules) — et le gérant a tranché lui-même le format après avoir vu le coût de 104 épisodes longs.
**How to apply :** tout nouvel épisode se place à sa semaine, son court s'écrit dans la foulée, et la chaîne d'intégration se relance : `_teleprompteur.py` (longs + courts), `_generer_prompteur_html.py`, `_generer_prompteur_web.py`, `_publier_tout.py`, `00_PILOTAGE/_generer_suivi.py --force`, rsync du miroir, puis republication de l'artifact. Voir [[organisation-dossier-contenu-mon-fiscaliste]] et [[chaine-youtube-administrations]].
