# Son

## Diagnostic à faire sur chaque rush
```bash
ffmpeg -hide_banner -t 60 -i RUSH -vn -af "astats=measure_perchannel=RMS_level:measure_overall=none" -f null - 2>&1 | grep "RMS level"
```
- Deux valeurs très différentes (ex. −26 dB / −inf) → la voix n'est que sur un canal : le moteur la recentre
  (`pan=mono|c0=cX`). Sans cela, l'orateur n'est audible que dans une oreille au casque.
- Bruit de fond (pause) vers −74 dB : excellent, débruitage léger seulement.
- Spectre typique micro-cravate DJI sur la poitrine : excès 150–500 Hz, peu d'énergie au-dessus de 12 kHz.

## Chaîne voix validée (`voice_chain` dans `monteur.py`)
recentrage mono → passe-haut 75 Hz → anti-clics → débruitage FFT léger (nr 8) → grave −6 dB (shelf 140 Hz),
−5 dB à 200 et 320 Hz, −3 dB à 550 Hz → présence +4 dB à 3,2 kHz, +1 dB à 6 kHz → air +5 dB à 10 kHz,
+4 dB à 14 kHz → dé-esseur léger → expanseur doux (queue de réverbération, respirations) → compresseur 2,5:1
(nivellement) → compresseur 5:1 rapide (crêtes) → limiteur −1 dBFS.
Résultat mesuré : variation de niveau de 6,9 → 5,5 dB, voix au centre.

## Musique et bruitages (`audio_fx.py`)
- Musique générée (nappe, arpège, basse douce, 92 BPM, La mineur) : libre de droits, s'efface sous la voix
  (ducking), remonte sur la carte de fin. Si le gérant veut mieux : piste de la bibliothèque audio YouTube.
- Bruitages : `whoosh`, `swish`, `riser`, `boom`, `impact`, `thud`, `pop`, `coin0-2`, `paper`, `fail`,
  `shimmer`, `tick`, `tock`, `click`, `ding`, `flashhit`, `glitch` — placés automatiquement par type de
  scène et de transition (`sfx_events`).
- Mixage final normalisé à −14 LUFS intégrés, crête −1,5 dBTP (loudnorm deux passes, linéaire).

## Pour aller plus loin (hors moteur)
- Activer l'enregistrement interne du DJI Mic (WAV 32 bits flottants) et fournir ce fichier : meilleure source.
- Tourner avec un prompteur sous l'objectif : moins de regards hors caméra, moins d'animations nécessaires.
