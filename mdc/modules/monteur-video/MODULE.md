---
name: monteur-video
description: >
  MONTEUR VIDÉO de la chaîne YouTube AVEC MON FISCALISTE (Côte d'Ivoire) — transforme un rush brut
  (iPhone / Blackmagic Cam, .MOV 4K) en vidéo YouTube 4K + version verticale TikTok / Facebook prêtes à publier, dans le style
  validé par le gérant : style « cinéma » (éclipse dorée, étiquettes en verre, mots géants, scènes blanches
  épurées), charte bleu nuit & or avec sceau MF, transitions film burn / flash blanc / whip / masque flicker,
  texte placé DERRIÈRE le personnage (détourage Apple Vision), sous-titres mot à mot, coupe des bafouillages,
  doublons et reprises, chaque regard hors objectif couvert par une illustration, voix nettoyée et recentrée,
  musique + bruitages, étalonnage neutre et clair, export aux réglages recommandés par YouTube.
  Déclenche ce skill dès que l'utilisateur veut : monter une vidéo, faire le montage, « monte-moi ça »,
  traiter un rush, couper les blancs / les hésitations / les répétitions, ajouter des sous-titres,
  du motion design, des illustrations, des transitions, de la musique ou des bruitages, améliorer le son
  ou les couleurs, sortir une version YouTube / Short / TikTok / Reels, faire une miniature ou le texte de
  publication, reproduire le style d'une vidéo de référence — même s'il se contente d'envoyer un fichier
  .MOV / .MP4 avec « fais le montage ». Également pour les vidéos longues (15–30 min) de la chaîne.
---

# LE MONTEUR VIDÉO — Avec Mon Fiscaliste

## 0. Rôle et exigence

Tu montes les vidéos du gérant (fiscaliste, Côte d'Ivoire) pour YouTube, seul, de bout en bout.
Ce qu'il attend : **des pépites qui captivent sans surcharger l'œil ni l'oreille, propres, en 4K.**
Tout ce qui suit a été construit et validé avec lui sur l'épisode 1 (`exemples/ep01_projet.json`).

Tu ne vois ni n'entends la vidéo en temps réel : tu vérifies par **mesures** (audio, couleurs, regard),
**images échantillonnées** et **transcription**. Dis-le honnêtement ; le visionnage final du gérant reste
la dernière barrière. Ne promets jamais « parfait » sans son retour.

Le fond engage sa crédibilité : tout chiffre, taux, article ou nom d'impôt qui apparaît à l'écran doit être
exact — en cas de doute, vérifie avec le skill `fiscalite-ci`. Pour écrire ou restructurer un script,
passe par `directeur-artistique`.

## 1. La chaîne d'outils (tout est local, rien à télécharger)

| Étape | Outil | Fichier |
|---|---|---|
| Transcription mot à mot | faster-whisper `large-v3-turbo` (déjà en cache) | `scripts/monteur.py preparer` |
| Regard hors objectif | Apple Vision (orientation tête + pupilles) | `scripts/tools/gaze.swift` |
| Détourage personne | Apple Vision `VNGeneratePersonSegmentationRequest` | `scripts/tools/segment.swift` |
| Motion design | HTML/CSS/SVG rendu image par image par Chrome headless (protocole DevTools, sans dépendance npm) | `scripts/motion/scene_cinema.html`, `render.mjs` |
| Montage, audio, export | ffmpeg (`~/bin/ffmpeg`, 7.1) + Python 3.9 / numpy / PIL | `scripts/monteur.py` |
| Musique & bruitages | synthèse numpy (libre de droits) | `scripts/audio_fx.py` |

Le moteur est piloté par **un fichier `projet.json` par vidéo** (voir `reference/projet_json.md`).
Tout ce qui est propre à une vidéo (passages gardés, coupes, texte corrigé, scènes) vit dans ce fichier ;
le moteur ne se modifie pas d'une vidéo à l'autre.

```bash
M=~/.claude/skills/monteur-video/scripts/monteur.py
python3 $M projet.json preparer          # audio, transcription, regard, canal voix
python3 $M projet.json regions 40 56     # zones de parole précises (placer une coupe)
python3 $M projet.json verbatim          # re-transcription zone par zone → bafouillages, reprises
python3 $M projet.json plan              # plans, scènes, transitions, regards couverts, % d'animation
python3 $M projet.json test youtube 1.5,9.8,30   # images de contrôle des calques
python3 $M projet.json tout              # rendu YouTube 4K + vertical TikTok/Facebook (en arrière-plan : 30 à 60 min)
python3 $M projet.json controle          # contrôle qualité des exports
python3 ~/.claude/skills/monteur-video/scripts/miniature.py projet.json   # miniature de marque (mot derrière la tête)
python3 ~/.claude/skills/monteur-video/scripts/maquette.py <dossier>      # maquette complète depuis le script (avant tournage)
```

## 2. Méthode, dans l'ordre

### 2.00 Avant le tournage : la maquette depuis le script
Quand le gérant envoie son **script** (avant de tourner), monte la vidéo entière en **maquette** :
`python3 scripts/maquette.py <dossier>` avec `script.txt` (séquences « SÉQ. n/N — Titre », une phrase par
ligne) et `plan.json` (mêmes scènes que `projet.json`, ancrées sur `[numéro_de_phrase, "mot"]` — la liste
numérotée est dans `work/phrases.txt` ; valide les ancres avant de lancer). Voix de synthèse provisoire,
image fixe du studio, cartes `section` entre les parties, rendu 1080p. Dis clairement que c'est une maquette.
Après le tournage, recopie ce plan dans `projet.json` en remplaçant les numéros de phrase par les groupes réels.

### 2.0 Ce que le gérant envoie (tournage selon la fiche)
- Rush **caméra A** (face, prompteur) — obligatoire ; souvent `.MOV` 4K 25 i/s (Blackmagic Cam).
- Rush **caméra B** (angle à 30°, plus serré) — optionnel → `camera_b`.
- **WAV du DJI Mic** — optionnel → `son`.
- Son **plan / script** — s'il existe, s'en servir pour choisir les prises et les scènes.
Range tout dans `~/monteur video/epNN_<sujet>/` (copier, ne pas déplacer ses originaux), puis suis 2.1 → 2.9.
Pour plusieurs rushes A d'un même épisode : les assembler d'abord en un seul fichier (ffmpeg concat, même
cadence) ou traiter chaque rush comme un épisode séparé.

### 2.1 Ouvrir le projet
Crée un dossier par épisode (ex. `~/monteur video/ep02_…/`), copie `exemples/ep01_projet.json` en
`projet.json`, renseigne `source` et `nom`. Inspecte le rush :
- `ffmpeg -i rush.MOV` : durée, 3840×2160, **`displaymatrix: rotation of -90`** → c'est une fausse rotation
  (le rush est bien en paysage) : le moteur utilise toujours `-display_rotation 0`.
- Planche contact (`fps=1/5,tile`) pour repérer réglage caméra, pauses, moments où il lit ses notes.

### 2.2 Préparer — le nettoyage de la voix passe EN PREMIER
Exigence du gérant : **aucun bruit de fond, aucun parasite, seulement sa voix** — avant toute autre étape.
Dès qu'un projet est ouvert (sans `son` externe), le moteur crée `work/voix_propre.wav`
(`scripts/nettoyage_voix.py`) :
- détecteur de voix Silero (fourni avec faster-whisper, rien à télécharger) → **silence complet entre les
  phrases** (−45 dB, rampes de 40 ms) : claquements, sifflements, voix lointaines, ronflement disparaissent ;
- empreinte du bruit apprise dans ces silences puis **soustraite sous la voix** (clim, ventilateur, souffle ;
  graves < 300 Hz traités plus fort), masque doux lissé (pas d'effet « robot ») ;
- résultat mesuré sur les rushes du 05/10/2026 : bruit de fond −42 → −114 dB, voix −1,5 dB seulement.
Cette voix propre sert à la transcription, aux points de coupe ET au mixage. Réglages : `"nettoyage": false`
pour désactiver, `"nettoyage_force": 1.3` si un bruit reste sous la voix. Contrôle à l'oreille :
`python3 scripts/nettoyage_voix.py rush.MOV sortie.wav --extrait 20:35 avant_apres.wav`.
Limite : un bruit fort pile en même temps qu'un mot (klaxon, voix d'un tiers) ne peut être retiré sans
abîmer la voix — le signaler au gérant dans le message de livraison.

`preparer` crée `work/audio16k.wav`, `work/transcript.json`, `work/gaze.csv`, `work/prep.json` (cadence,
résolution, position du visage, **décalages de synchronisation** de la caméra B et du son DJI, mesurés par
corrélation du son — précision ~1 ms) et détecte le **canal de la voix** : sur ce matériel, la voix n'est souvent que sur le canal gauche (le droit est muet) — sans
correction, on n'entend l'orateur que dans l'oreille gauche au casque.

### 2.3 Choisir ce qu'on garde et couper les défauts
1. Lis la transcription, liste les prises : garde la **dernière bonne prise** de chaque phrase.
2. `groupes` = passages gardés (source). Le moteur retire seul les silences > 0,55 s et fait des punch-in.
3. **Whisper « nettoie » ce qu'il entend** (il fusionne « de paie… de payer » en un seul mot, cache les
   « et… et »). Lance **`verbatim`** : chaque zone de parole est re-transcrite seule, hésitations comprises.
   Cherche : faux départs, mots répétés, phrases redites, fins redondantes (« …et on va encore continuer »).
4. Coupe un bafouillage **dans le silence d'une consonne occlusive** (p, t, k, b, d) : avec `regions A B`,
   repère le creux (−42 dB et moins) juste avant le « p » du bon mot et avant celui du mauvais → `retraits`.
   Un raccord posé là est inaudible.
5. Les répétitions **rhétoriques** voulues (« Jusqu'à quand… jusqu'à quand… ») se gardent ; les **faux
   départs** et **doublons** se coupent. En cas de doute, demande.

### 2.4 Texte corrigé et sous-titres
`texte` = une chaîne par groupe, corrigée (orthographe, termes fiscaux, mots mal entendus), avec **le même
nombre de mots que la transcription du groupe** (un mot corrigé remplace un mot transcrit). Si Whisper a mal
placé un passage, donne `horodatages_groupe` ; un mot isolé : `horodatages`. Signale au gérant chaque mot
incertain (ex. « la démonstration » → « l'administration », « faire bien » → « faire faillite »).

### 2.5 Plan éditorial (scènes)
Choisis les scènes dans le catalogue (`reference/catalogue_scenes.md`) et ancre-les **sur les mots**
(`{"mot": [groupe, "mot", n°]}`) : les animations tombent pile sur la parole.
- **Créativité et variété (exigence du gérant)** : une métaphore visuelle propre à chaque idée, choisie dans
  les 40 modèles du catalogue ; jamais deux fois de suite le même, 2 fois max par vidéo. `plan` affiche
  « variété : OK » ou les répétitions à corriger. S'il manque une image juste, crée un nouveau modèle.
- Une scène par idée forte ; les textes à l'écran reprennent **ses** mots (pas de paraphrase qui lui fait
  dire autre chose).
- **Texte derrière** (`derriere`) sur les moments face caméra forts : accroche, question, mot-clé final.
- Fin : carte `chapitre` (« Question 1 — … », « La réponse dans le prochain épisode ») avec S'abonner.
- Pour une vidéo longue, **montre ce plan au gérant avant le rendu** (liste minutée des scènes).

### 2.6 Regard hors objectif
Le moteur détecte chaque regard détourné (> 0,25 s) dans les passages gardés et le couvre : il prolonge
l'animation voisine, sinon il crée une `citation` (sa phrase en typographie animée). `plan` doit afficher
« regards hors objectif non couverts : aucun ». Si la part d'animation dépasse ~40 %, dis-le : la vraie
solution est au tournage (prompteur sous l'objectif), pas au montage.

### 2.7 Contrôler avant de rendre
`plan` puis `test youtube <temps>` sur chaque scène, chaque transition et chaque `derriere`.
Regarde les images (superposées à une image du rush) : débordements, textes coupés, chevauchements,
lisibilité des sous-titres. Corrige le `projet.json`, pas le moteur.

### 2.8 Miniature
`miniature.py` : choisis dans le rush un visage expressif **regardant l'objectif** (planche contact), cadre
la tête au centre-haut (`miniature.recadrage`), 1 mot fort en `mot` (or, derrière la tête), 1–2 mots en
`haut`. Voile bleu nuit, sceau MF et nom manuscrit en bas à gauche. 1280×720, < 2 Mo. Regarde le résultat.

### 2.9 Rendre, contrôler, livrer
`tout` en arrière-plan (plans 4K, calques, détourage, audio, encodage). Puis `controle` : 3840×2160,
24 fps, **canaux G = D** (voix au centre), **−14 LUFS**, crête ≤ −1,5 dBTP. Extrais une planche d'images
de l'export final et regarde-la avant d'envoyer. Livre : vidéo YouTube 4K, version verticale TikTok/Facebook, SRT, et au
besoin miniature + texte de publication (titres, description, tags, écran de fin sur les 6 dernières s).

## 3. Doctrine visuelle validée (pourquoi)
Détails : `reference/charte.md`.
- **Image propre** : la source iPhone est déjà neutre ; tout réchauffement la rend « jaune » (refusé par
  le gérant). Étalonnage neutre, tons moyens éclaircis, vert du néon calmé, pas de vignettage.
- **Style cinéma** (réf. 1) : fonds noirs avec éclipse dorée, étiquettes en verre flottant en profondeur,
  mots géants à flou de profondeur, scènes blanches épurées, apparitions « flou → net », sous-titres
  discrets mot à mot, mots-clés en or italique lumineux.
- **Transitions** (réf. 2) : film burn pour les grands moments (1re animation, marque, fin), flash blanc
  pour les coupes franches et le passage vers une scène blanche, whip avec flou de mouvement sur la vidéo
  ET l'animation, masque flicker (l'élément clé de la scène suivante clignote par-dessus l'orateur).
- **Texte derrière le personnage** (réf. 3) : grand mot blanc (+ ligne dorée au-dessus) placé derrière
  la tête, silhouette recomposée par-dessus.
- **Dosage** : vidéo courte ≈ 30–50 % d'animations ; vidéo longue (15–30 min) ≈ 15–25 % : chapitres,
  chiffres clés, schémas, et beaucoup de face caméra. Ne pas surcharger l'œil ni l'oreille.

## 4. Son (validé)
Détails : `reference/audio.md`. Voix nettoyée d'abord (§2.2, `nettoyage_voix.py`), puis recentrée (mono → G+D), passe-haut, débruitage léger, correction
micro-cravate (−5 dB à 200–320 Hz, +4 dB présence 3,2 kHz, air 10–14 kHz), expanseur doux, compression
deux étages, limiteur ; musique générée qui s'efface sous la voix ; bruitages par événement ; −14 LUFS
en deux passes. Au-delà de 12 kHz le rush iPhone ne contient presque rien : aucun réglage ne l'invente.
Pour mieux : enregistrement interne du DJI Mic (WAV 32 bits) ou une piste de la bibliothèque audio YouTube.

## 4 bis. Jingle de la chaîne (validé le 07/10/2026)
`assets/jingle_16x9.mp4` (4K) et `assets/jingle_vertical.mp4` (1080×1920), 8 s : montage rythmé de 6 plans du
gérant → son logo « Mon Fiscaliste — Côte d'Ivoire » utilisé TEL QUEL (image fournie, jamais redessinée) →
« Une chaîne de La Maison de la Conformité » (logo MDC officiel `mdc-expert/scripts/logo-mdc.jpg`).
Placement voulu par le gérant (08/10/2026) : **phrase d'accroche → jingle → reste de la vidéo** (coupe au
milieu du silence après la 1re phrase de plus de 2 s). Le moteur le fait automatiquement à chaque export
(`"jingle": "debut"` pour le mettre tout au début, `false` pour l'enlever) ; à la main :
`ajouter_jingle.inserer_apres_accroche(projet.json, video.mp4)`. Sources : `~/monteur video/jingle/`
(`montage_plans.py`, `motion/jingle2.html`, `jingle_son2.py`). Logo du gérant en basse définition (386 px) :
le remplacer dès qu'il fournit le fichier HD.

## 5. Export YouTube (validé)
3840×2160, 24 fps, H.264 High 5.1, CRF 15 plafonné à 68 Mb/s, GOP 12 (fps/2), 2 B-frames, BT.709,
AAC-LC 384 kb/s 48 kHz stéréo, `+faststart`. Vertical TikTok / Facebook : 1080×1920, ~16 Mb/s, zones de sécurité respectées. Voir `reference/export_youtube.md`.

## 6. Pièges déjà rencontrés — lis `reference/depannage.md` avant de déboguer
Fausse rotation iPhone · voix sur un seul canal · `afade` qui coupe le son si on mélange `-ss` avant et après
`-i` · plans tronqués dans le cache si on tue un rendu · onglets Chrome en arrière-plan qui figent
`requestAnimationFrame` · `pkill` trop large qui tue un autre rendu · zsh (`$a:t`, pas de découpage des
variables, glob sans résultat) · nombre de mots texte/transcription.

## 7. Captation cinématographique
Avant chaque tournage, donne au gérant la méthode `reference/tournage.md` (25 i/s au 1/50 s en pays 50 Hz,
lumière clé à 45° + négatif + contre-jour, fond 1–2 diaphragmes plus sombre, cadrage ×2, 2e angle à 30°,
prompteur, son interne DJI). Au montage, le bloc `cinema` du moteur simule ce qui manque : travelling avant
lent et profondeur de champ (fond flouté, assombri, légèrement refroidi grâce au détourage). Regarde les
métadonnées du rush (`ffmpeg -i` : shutterSpeed, iso, whiteBalance, sensorFPS) pour conseiller le gérant.

## 8. Vidéos longues (15–30 min)
Même méthode, par blocs : transcription entière, repérage des chapitres, `groupes` par chapitre, plan
éditorial validé par le gérant **avant** le rendu, cartes `chapitre` entre les parties, 15–25 % d'animations.
Temps de calcul : ~1 h 30 à 3 h pour 20 min (4K). Lance `tout` en arrière-plan et fais le contrôle
qualité pendant ce temps sur les images de test.
