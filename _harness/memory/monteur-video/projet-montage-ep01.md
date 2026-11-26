---
name: projet-montage-ep01
description: "État du projet vidéo : épisode 1 monté, skill monteur-video créé, tournage des « vraies » vidéos prévu le 01/10/2026"
metadata:
  node_type: memory
  type: project
  originSessionId: 67778b14-01b9-4592-bea2-3d777fdb5078
  modified: 2026-10-05T19:32:03.002Z
---

- Épisode 1 (« L'administration, notre ennemi ? ») monté le 29–30/09/2026 dans `~/monteur video/` (projet.json, export/).
  Exemple de référence copié dans `~/.claude/skills/monteur-video/exemples/ep01_projet.json`.
- Skill `~/.claude/skills/monteur-video/` : moteur `scripts/monteur.py` (piloté par projet.json), catalogue de scènes,
  miniature, méthode de tournage `reference/tournage.md`, fiche de tournage publiée
  https://claude.ai/artifact/Cw9zHVxM5WFi2Bxf7x7gnj.
- Le 01/10/2026 le gérant tourne ses « vraies » vidéos selon la fiche (25 i/s, 1/50 s, caméra B à 30°, WAV DJI,
  prompteur) et les enverra : appliquer directement le skill (§2.0 : ranger dans `~/monteur video/epNN_<sujet>/`).
- Multicaméra + son DJI + cadence auto ajoutés le 30/09 et testés sur une simulation (`~/monteur video/test_multicam/`),
  pas encore sur un vrai tournage à deux caméras : vérifier les décalages affichés par `preparer`.
- 30/09 : script complet de l'épisode « manifeste » de la chaîne (6 séquences, 74 phrases) → maquette 6 min livrée
  (`~/monteur video/ep_manifeste/` : script.txt, plan.json ancré par numéro de phrase, export/ep00_manifeste_MAQUETTE.mp4).
  À son tournage, reprendre plan.json → projet.json (numéros de phrase → groupes réels). Points ouverts posés au gérant :
  « d'oppressions » vs « de pression », « nous [nous] décourageons », tutoiement/vouvoiement, dosage d'animations (52 %).
- 05/10/2026 : 8 rushes verticaux (DJI Osmo Pocket 3 + copies iPhone, face caméra, sujets au choix) = 6 sujets
  → 6 vidéos TikTok/Facebook dans `~/monteur video/tiktok_0510/` (specs.py → construire.py → projet.json par vidéo).
  Sur TikTok la marque est « Mon Fiscaliste » (@bile_le_fiscaliste, ~90 K abonnés), pas « Avec Mon Fiscaliste ».
  Doutes de transcription signalés : « tu n'as pas une affaire » (paris), « toi tu n'as pas un enfant » (coupé).
**Why:** il veut que « dès qu'il envoie, on sache quoi faire ».
**How to apply:** à la réception de rushes, invoquer le skill `monteur-video` sans redemander la méthode. Voir [[feedback-montage-video]].

- **Lot du 08/10/2026 (10 rushes ep02) : livré en entier le 09/10/2026** (tiktok_10 → tiktok_19 dans `tiktok_0510/`, specs `_V10`…`_V19`).
  Points appris : vérifier que la transcription « voix nettoyée » n'a pas avalé le début (C132 : 30 s perdues, recollées depuis
  `ep02/work/t_*.json`) ; seuil de parole désormais relatif (rush IMG_1147 enregistré à −43 dB) ; couper les animations
  automatiques de regard (`regard_min: 99`) quand il montre un objet à la caméra ; `couverture.descente` si la tête cache le titre.
  Restent ouverts : nom exact de « M. Benjamin Indri/Ingrid », logo HD.

- **13/10/2026 — format « réponse à un TikTok »** (tiktok_20_gestionnaire) : sa vidéo à elle présentée en écran de téléphone
  (`reaction_gestionnaire/segments_elle.py`), ouverture choc + arrêt sur image, médaillons-rappels, scène `virement` créée ;
  assemblage en 2 étapes (`reaction_gestionnaire/assembler.py`). Rushes DJI Osmo Pocket 3 (costume beige) : filigrane à effacer
  (`filtre_source: delogo=x=85:y=482:w=600:h=78,`), image parfois floue → choisir la miniature par netteté.
  Ne jamais finir une phrase de `corrige` de l'accroche par « … » : le jingle se coupe là. tiktok_21_tchebe = vidéo à part.
