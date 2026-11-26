# Export et livraison YouTube

## Réglages (constantes `YT_VIDEO` / `YT_AUDIO` de `monteur.py`)
| Paramètre | Valeur | Pourquoi |
|---|---|---|
| Résolution | 3840×2160 (YouTube) · 1080×1920 (TikTok / Facebook) | La 4K déclenche les codecs VP9/AV1 de YouTube : meilleure qualité même vue en 1080p |
| Cadence | 24 i/s (celle du rush) | Ne jamais convertir la cadence |
| Codec | H.264 High, niveau 5.1, CRF 15, plafond 68 Mb/s | Au-dessus des 35–45 Mb/s recommandés pour la 2160p SDR |
| GOP | 12 images (moitié de la cadence), 2 B-frames, `+faststart` | Recommandation YouTube |
| Couleurs | BT.709, plage TV, yuv420p | SDR standard |
| Audio | AAC-LC 384 kb/s, 48 kHz, stéréo | Recommandation YouTube |

## Livrables
1. `<nom>_youtube_4k.mp4` — version principale.
2. `<nom>_tiktok_facebook.mp4` — TikTok et Facebook (Reels) : 1080×1920, H.264 ~16 Mb/s (constante `VERTICAL_VIDEO`), fin avec bouton « + Suivre » (pas de bouton YouTube).
3. `<nom>_sous-titres_fr.srt` — à charger dans YouTube Studio (référencement).
4. `<nom>_miniature.jpg` (script `miniature.py`) : visage expressif regard caméra, grand mot or derrière la tête,
   cartouche en haut, sceau + nom manuscrit ;
   texte de publication (3 titres, description, hashtags, tags) — faire relire par `directeur-artistique`.
5. Écran de fin : les 6 dernières secondes (carte `chapitre`) servent aux éléments de fin YouTube.

## Contrôle qualité (commande `controle`)
Durée, résolution, 24 i/s, canaux gauche = droite, −14 LUFS, crête ≤ −1,5 dBTP. Puis planche d'images
de l'export final (`ffmpeg -ss T -i export.mp4 -frames:v 1`, 12 à 16 instants) regardée avant l'envoi.

## Version verticale TikTok / Facebook — zones de sécurité
L'interface de ces applis recouvre l'image : garder l'essentiel dans la zone centrale.
- Haut : ~180 px (onglets « Abonnements / Pour toi », LIVE) → filigrane placé à 190 px.
- Bas : ~420 px (pseudo, description, musique) → sous-titres centrés vers 72 % de la hauteur.
- Droite : ~140 px entre 700 et 1500 px (boutons j'aime, commentaires, partage) → pas de texte clé collé au bord droit.
- Pas d'écran de fin YouTube : la carte de fin reste (6 s) mais avec « + Suivre » aux couleurs de la marque.
- Couverture TikTok : choisir une image du plan « derrière » (mot + visage) lors de la publication.
