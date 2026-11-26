# Format du fichier `projet.json`

Exemple complet et validé : `exemples/ep01_projet.json` (épisode 1, 47 s de parole + 6 s de fin).
Le dossier du projet contient `projet.json` ; le moteur crée `work/` (intermédiaires, caches) et `export/`.

| Champ | Rôle |
|---|---|
| `nom` | Préfixe des fichiers exportés (`<nom>_youtube_4k.mp4`, `<nom>_tiktok_facebook.mp4`, `<nom>_sous-titres_fr.srt`) |
| `source` | Chemin absolu du rush de la caméra A (face, avec prompteur) |
| `camera_b` | Optionnel : rush de la 2e caméra (angle ≥ 30°, plus serré). Synchronisée automatiquement par le son ; les regards vers les notes basculent sur B au lieu d'être couverts par une animation, et une coupe sur deux passe en B |
| `son` | Optionnel : enregistrement externe (WAV du DJI Mic, 32 bits flottants). Synchronisé automatiquement et utilisé à la place du son de l'iPhone |
| `decalage_camera_b`, `decalage_son` | Optionnel : forcer le décalage (s, t_B = t_A + décalage) si la synchro automatique échoue (bruit, musique) |
| `cadrage_visage_x`, `cadrage_visage_x_b` | Optionnel : position horizontale du visage (0–1) ; sinon détectée par détourage |
| `chaine`, `chaine_sous_titre`, `monogramme` | « Avec Mon Fiscaliste », « CÔTE D'IVOIRE », « MF » |
| `canal_voix` | Optionnel : `c0`, `c1` ou `0.5*c0+0.5*c1` (sinon détection automatique) |
| `musique` | `true` / `false` |
| `couvrir_regards` | `true` : chaque regard hors objectif est couvert automatiquement |
| `prompt_transcription` | Optionnel : vocabulaire pour guider Whisper (noms propres, sigles) |
| `groupes` | `[[debut, fin], …]` en secondes source : les phrases gardées, dans l'ordre |
| `retraits` | `[[a, b], …]` morceaux retirés à l'intérieur d'un groupe (bafouillages, faux départs) |
| `texte` | Une chaîne par groupe : le texte corrigé, **même nombre de mots** que la transcription du groupe |
| `horodatages` | `[[groupe, "mot tel qu'écrit dans texte", debut, fin], …]` corrections ponctuelles (source) |
| `horodatages_groupe` | `{"0": [[debut, fin], …]}` horodatage complet d'un groupe (un couple par mot) |
| `coupures_sous_titres` | `[[groupe, index_mot], …]` forcer une coupure de sous-titre après ce mot |
| `mots_cles` | Mots mis en or italique dans les sous-titres et les citations |
| `scenes` | Voir `catalogue_scenes.md` |
| `fin` | `{"type": "chapitre", "duree": 6, "transition": "burn", "textes": {…}}` |
| `fond_fin_source` | Instant du rush utilisé (flouté) derrière la carte de fin |
| `cinema` | Optionnel : `{"push": 0.045, "profondeur": true, "flou_fond": 10, "fond": "<filtres ffmpeg du fond>"}` — travelling virtuel et profondeur de champ simulée ; `{"push": 0, "profondeur": false}` pour désactiver |
| `miniature` | `{"t", "recadrage", "haut", "mot", "bas"}` — voir `scripts/miniature.py` |

Astuce « même nombre de mots » : si Whisper a entendu « la démonstration » et que le bon texte est
« l'administration » (2 mots → 1), le moteur s'arrête et affiche les deux versions. Solutions : garder un
découpage équivalent (« l'administration » pour « la démonstration » compte 1 mot contre 2 → ajuster), ou
fournir `horodatages_groupe` pour ce groupe (l'horodatage mot à mot vient de `regions` + `verbatim`).
Une espace insécable (` `) soude deux mots en un seul (« de pression. »).

La cadence (24, 25, 30 i/s…) et la résolution (4K, 1080p) sont lues dans le rush (`work/prep.json`) :
aucun réglage à faire. `preparer` affiche les décalages mesurés ; contrôle-les (un décalage absurde de
plusieurs minutes = mauvais fichier ou synchro ratée → donner `decalage_*` à la main, mesuré au clap).
