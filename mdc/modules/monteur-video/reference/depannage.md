# Dépannage — pièges déjà rencontrés

| Symptôme | Cause | Solution |
|---|---|---|
| Image couchée / 2160×3840 | Métadonnée de rotation −90° de Blackmagic Cam, fausse | `-display_rotation 0` en option d'entrée (déjà dans le moteur) ; ne pas utiliser `-noautorotate` (la métadonnée se recopie dans la sortie) |
| Voix dans une seule oreille | Voix sur le canal gauche seulement | `canal_voix` / détection automatique, `pan=mono|c0=c0` |
| Trous de son de 2 s à chaque coupe | `afade=out` calé sur un temps d'entrée quand on combine `-ss` avant et après `-i` | Un seul `-ss` avant `-i` (précis en ré-encodage) |
| Plan de 1,8 s au lieu de 5,7 s dans l'export | Rendu tué pendant l'écriture d'un plan, repris depuis le cache | Écriture en `.tmp` puis renommage (déjà dans le moteur) ; sinon supprimer le plan tronqué |
| Rendu Chrome figé | `requestAnimationFrame` gelé dans les onglets en arrière-plan | `renderAt()` synchrone, la capture force l'image (déjà fait) |
| Un rendu s'arrête tout seul | `pkill -f "amf-chrome-"` a tué le Chrome d'un autre rendu | Tuer par PID (`for p in $(pgrep -f …); do kill $p; done`) |
| `ENOTEMPTY … amf-chrome` | Profil Chrome encore verrouillé à la fermeture | Nettoyage tolérant (déjà fait), sans effet sur le rendu |
| zsh : `Invalid alpha … '0.06=fill'` | `$a:t` est un modificateur zsh | Écrire `${a}:t` |
| zsh : `kill` sans effet | zsh ne découpe pas `$VAR` contenant plusieurs PID | Boucle `for p in $(pgrep …)` |
| zsh : `no matches found: *.png` | Glob sans résultat = erreur | `rm -f` inoffensif ; ou `setopt NULL_GLOB` |
| Filtre ffmpeg `$OLD[b2]` vide | zsh interprète `[b2]` comme indice | `${OLD}[b2]` |
| « groupe N : X mots transcrits vs Y » | Texte corrigé et transcription pas alignés | Voir `projet_json.md` (même nombre de mots, ou `horodatages_groupe`) |
| Mot mal horodaté (sous-titre en avance) | Whisper place mal les mots après un bafouillage | `horodatages` avec les temps lus via `regions` |
| Texte « derrière » coupé | Mot trop long | Le moteur réduit la taille ; sinon `size` plus petit ou mot plus court |
| Couleurs jaunes | Étalonnage réchauffé | Garder `GRADE` neutre (source iPhone déjà neutre) |
| Rendu d'animation figé sur une image (capture qui ne revient jamais) | En 4K, la superposition film burn + éclipse dépasse les textures du compositeur de Chrome (l'image passe en 1080p) | Automatique : 2 essais avec délai, puis l'image est rendue en définition moitié et agrandie (`rescue_frames`) ; relancer : les images faites sont gardées |
| Chrome `--screenshot` ne rend pas la main | Chrome headless ne se ferme pas toujours | Attendre l'image puis tuer le processus (déjà dans `miniature.py`) |
| Vidéo qui saccade, « 21,9 i/s » au lieu de 24, images manquantes | ffmpeg 7 perd des images au hasard quand une séquence PNG entre dans un `overlay` | Calques convertis en ProRes 4444 / masques en FFV1 avant la composition (`to_video`) ; le moteur vérifie le nombre d'images et s'arrête s'il en manque |
| Whip qui montre la vidéo entre deux animations | Glissement pendant un enchaînement plein écran → plein écran | Mode `whipin` (flou sur place), automatique quand les scènes se touchent |
| Parasite / « bulles » dans le fond sur une voix nettoyée | Second débruiteur (`afftdn`, `agate`, `adeclick`) appliqué à une voix déjà silencieuse entre les phrases | `voice_chain(chan, propre=True)` quand `P.nettoye` : ces filtres sont retirés (artefacts ÷ 11 mesurés sur la vidéo du 06/10/2026) |
| Ronflement qui « apparaît et disparaît » avec la voix | Ronflement électrique (≈ 62 Hz) laissé sous la voix alors que les silences sont coupés | `nettoyage_voix.anti_ronflement` : passe-haut 85 Hz + coupe-bandes sur les harmoniques mesurées |
