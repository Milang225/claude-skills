---
name: Outils installés pour le montage vidéo
description: ffmpeg static + faster-whisper installés localement pour le pipeline de montage YouTube
type: reference
originSessionId: e01d6bdc-9c51-4d3c-a307-980dd4384902
---
Pipeline de montage vidéo installé sur le Mac :

- **ffmpeg 7.1 static (arm64)** : `~/bin/ffmpeg` (téléchargé depuis osxexperts.net). Inclut libass, libfreetype, vignette, drawtext, zoompan, xfade, subtitles, h264_videotoolbox.
- **faster-whisper** : installé via `pip3 install --user faster-whisper`. Utilisé via Python 3.9.6. Modèle `small` (français) téléchargé au premier run, gère bien la transcription word-level avec `word_timestamps=True`.
- **Polices Mac** disponibles pour drawtext / ASS subtitles : `/System/Library/Fonts/Supplemental/Arial Black.ttf`, `Arial Bold.ttf`, etc. Pour libass/subtitles, passer `fontsdir=/System/Library/Fonts/Supplemental`.

**Note importante** : le dossier vidéo de l'utilisateur s'appelle `~/Desktop/Communication ` (avec un **espace à la fin du nom**). Toujours quoter ce chemin. Sortir les rendus directement sur `~/Desktop/` pour éviter qu'il ne les retrouve pas.

**Encodage rapide** : utiliser `-c:v h264_videotoolbox -b:v 8-9M` pour profiter de l'accélération matérielle Apple Silicon.

**Brew n'est pas installé**. Pour tout outil supplémentaire, télécharger un binaire static ou utiliser pip3 --user.
