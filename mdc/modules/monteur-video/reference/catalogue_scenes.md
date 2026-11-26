# Catalogue des scènes (moteur `scene_cinema.html`)

Chaque scène du `projet.json` : `type`, `debut`, `fin`, `textes` (contenu), `cles` (instants clés ancrés sur
les mots), et au besoin `transition`, `hero` (texte du masque flicker), `masquer_sous_titres`.
Les textes acceptent du HTML simple : `<br>`, `<b>`, `<span class="itgold">…</span>` (or italique lumineux),
`<span class="goldg">…</span>` (dégradé or). Toutes les valeurs par défaut sont celles de l'épisode 1.

Plein écran = couvre l'orateur (sert aussi à masquer un regard hors caméra). « Sur orateur » = l'orateur reste visible.

| Type | Affichage | Textes | Clés | Transition par défaut |
|---|---|---|---|---|
| `mot_geant` | Plein écran sombre : étiquettes en verre flottant en profondeur, un mot en lumière, puis un **mot géant doré** | `pills[]` (≈8), `label`, `big` | `label`, `big` | film burn |
| `frise` | Plein écran sombre : ligne lumineuse à 4 points avec étiquettes, titre + sous-titre or | `title`, `sub`, `labels[4]`, `labels_v[4]` (version verticale, plus courte) | `sub` | masque flicker (`hero` = title) |
| `document` | Plein écran BLANC : un document sort d'une enveloppe bleu nuit, puis se fait gribouiller + mot or | `quote`, `header`, `title`, `amount_label`, `amount` (flouté), `big` | `card` (sortie du document), `big` (gribouillage) | whip |
| `barre` | Plein écran sombre : phrase d'intro + 2 étiquettes barrées en rouge | `header`, `items[2]` | `t0`, `t1` | flash |
| `contraste` | Plein écran sombre : « nous » (orbe terne qui descend) vs « elles » (orbe doré qui monte) + 2 cartes chiffrées | `low`, `high`, `stat1`, `stat2_num`, `stat2_label`, `stat2_plus` | `high`, `stat` | whip |
| `courbe` | Plein écran BLANC : courbe dessinée à la main avec 3 étapes lumineuses dorées | `quote`, `labels[3]`, `conclusion` | `conclusion` | flash |
| `compteur` | Plein écran sombre : grand chiffre qui défile de `from` à `to` + étiquettes, puis une chute | `label`, `from`, `to`, `suffix`, `pills[]`, `after` | `hit` (arrivée), `after` | masque flicker (`hero` à donner, ex. « 0% ») |
| `marque` | Plein écran sombre : sceau MF, « Avec Mon Fiscaliste » manuscrit, 2 lignes de promesse | `line1`, `line2` | `l1`, `l2` | film burn |
| `citation` | Plein écran sombre : la phrase prononcée, mot par mot | — (`phrase`) | — | flash (créée automatiquement pour couvrir un regard) |
| `question` | Sur orateur : grande question au centre, fond assombri | — (`phrase`) | — | — |
| `derriere` | Sur orateur : **grand mot DERRIÈRE la personne** (+ petite ligne or au-dessus) | `top` (optionnel), `main`, `size`, `size_v` | `main` | — |
| `section` | Plein écran sombre : carte de partie / de question en cours de vidéo (lever d'éclipse, sans bouton) — « Partie 2 », « Question 1 », « Engagement 3 », « La règle de base » | `kicker`, `title`, `sub` | — | film burn |
| `chapitre` | Plein écran sombre : lever d'éclipse, « Question 1 », titre, sous-titre, bouton S'abonner | `kicker`, `title`, `sub` | — | film burn (dans `fin`) |

`phrase` (question / citation) : liste `[texte, ancre, "gold"|"white"]`.

## Ancres
- `{"mot": [groupe, "mot"]}` : début du 1er mot égal (sans ponctuation, insensible à la casse) dans le groupe ;
  `{"mot": [g, "mot", 1]}` = 2e occurrence ; `"bord": "fin"` = fin du mot ; `"decalage": -0.2` en secondes.
- Nombre = temps de montage absolu ; `"fin_video"` = fin de la parole (début de la carte de fin).

## Bonnes pratiques
- Plein écran : démarrer ~0,2 s avant le mot déclencheur, finir ~0,4 s après le dernier mot illustré.
- Deux scènes plein écran qui se touchent s'enchaînent sans repasser par l'orateur (le moteur gère le raccord).
- `derriere` : un seul mot court en `main` (le moteur réduit la taille s'il dépasse 92 % de la largeur) ;
  le placer quand l'orateur est face caméra, cadrage serré ou moyen, tête au centre.
- Les chiffres et termes fiscaux affichés doivent être exacts (vérifier avec `fiscalite-ci`).
- Nouveau type de scène : l'ajouter dans `scene_cinema.html` (objet `B.<type>`), dans `FULL_TYPES` /
  `LIGHT_TYPES` / `TRANS_DEFAUT` et `sfx_events` de `monteur.py`, puis documenter ici.


## Scènes créatives — une métaphore par idée (`motion/scenes_creatives.js`)
Plein écran, dessinées sur une scène 1920×1080 (mise à l'échelle automatique en vertical). Textes dans
`textes` (tous optionnels, valeurs par défaut = épisode manifeste) ; instants clés `cles.a` / `cles.b`.

| Type | Métaphore | Idéal pour | Textes principaux |
|---|---|---|---|
| `boussole` | Labyrinthe de tuiles traversé par un chemin doré | naviguer, s'orienter, se repérer | title, tiles[] |
| `balance` | Balance qui penche puis se redresse | payer plus / gagner plus, équilibre | title, left, right, after |
| `boucle` | Boucle fléchée qui tourne sans fin | cercle vicieux, répétition | labels[3], center |
| `ailleurs` | Loupe qui fouille des étiquettes puis part ailleurs | « le problème est ailleurs », fausse piste | title, pills[], big |
| `respire` | Cercles qui respirent, mot barré | étouffer / libérer, pression | line1, strike, after |
| `numero` | Chiffre géant tracé au trait d'or | Question 1, Engagement 2, étape n | n, kicker, title |
| `vague` | Vagues dorées et surfeur sur la crête | surfer, s'adapter, conjoncture | kicker, title |
| `cle` | Clé qui entre dans une serrure et libère la lumière | comprendre, déverrouiller, accès | kicker, title |
| `reseau` | Nœuds reliés qui se ramifient | écosystème, acteurs, filiales, liens | center, nodes[], branches[] |
| `billets` | Liasse FCFA barrée | « ce n'est pas l'argent » | title, after |
| `enveloppe_non` | Enveloppe glissée sur le bureau, tampon interdit | corruption, pots-de-vin, « faut bouger » | title, after |
| `foule` | Des personnes qui forment le bâtiment de l'administration | « elle est à nous », bien commun | title, after |
| `decodage` | Jargon juridique qui se décode en clair | expliquer une loi, traduire | title, label1, label2, jargon, clair |
| `prix` | Étiquette qui défile jusqu'à 0 FCFA | gratuit, coût, prix | title, after |
| `calendrier` | Page de calendrier, date entourée de rouge | échéance, jour J, redressement | mois, title, after, jour |
| `bouclier` | Page de loi qui devient bouclier | protection, sens de la loi | title, after |
| `fondations` | Briques qui s'empilent, maison qui s'élève | bases solides, conformité | title, labels[4] |
| `iceberg` | Partie émergée / immergée | « ce n'est pas que… », face cachée | title, tip, deep[4] |
| `triptyque` | Trois cartes qui pivotent | 3 engagements, 3 piliers, 3 étapes | title, items[[n, titre, sous-titre]] |
| `flux` | Des centaines de points qui virent au rouge au même endroit | milliers de cas, erreurs récurrentes | title, after |
| `semaine` | Calendrier hebdo, la même marque qui revient | récurrence, chaque semaine / mois | title, after |
| `croissance` | Courbe qui monte avec pastilles | ça marche, résultats, financements | title, badges[3] |
| `boite_outils` | Chapeau de magicien barré puis boîte à outils | pas d'astuces / dispositifs légaux | title, after, tools[4] |
| `orage` | Nuage d'orage qui devient ampoule | peur → compréhension | title, after |
| `confidentiel` | Dossier flouté + cadenas | anonymat, secret professionnel | title |
| `associe` | Camembert avec la part de l'État, un œil qui s'ouvre | l'État associé, il regarde les comptes | title, slice, pie, after |
| `parchemin` | Parchemin qui se déroule, sceau | règle d'or, principe, citation forte | kicker, rule |

## Règle anti-répétition (vérifiée par `plan` / `maquette.py` : ligne « variété »)
- Une idée = une image : choisir la métaphore qui colle au sens de la phrase, pas le modèle le plus pratique.
- Jamais deux fois de suite le même modèle ; au plus 2 fois par vidéo (texte `derriere` : 3–4 fois, sur les temps forts).
- Laisser des respirations face caméra entre les animations (le gérant n'aime ni la répétition ni la surcharge).
- Besoin d'une idée que le catalogue ne couvre pas ? Créer un nouveau modèle dans `scenes_creatives.js`
  (fonction `stage()` + `ttl()`), l'ajouter à `CREATIVES` / `LIGHT_TYPES` / `SFX_CREATIVES` et à ce tableau.

## Scènes TikTok — verticales natives (`motion/scenes_tiktok.js`, 05/10/2026)
Dessinées sur une scène 1080×1920. Zone utile y 230 → 1250 (au-dessus des sous-titres à 72 %).
Habillages **sur orateur** : `accroche`, `commentaire`, `rec`. Les autres sont plein écran.

| Type | Image | Idéal pour | Textes / clés |
|---|---|---|---|
| `accroche` | Titre d'accroche des 3 premières s (styles `bande`, `tampon`, `neon` : varier d'une vidéo à l'autre) | hook | l1, l2, style ; `couvre_regard` possible |
| `commentaire` | Vignette « Réponse au commentaire de… » façon TikTok (couvre le regard pendant la lecture) | réponse à un abonné | nom, texte |
| `rec` | Viseur caméra REC + minuteur sur l'orateur | filmer, garder une trace | label |
| `preuves` | 6 cartes de preuves cochées | « tout type de preuve » | title, items[[emoji,label]], after ; a, b |
| `decharge` | Décharge remplie, signée, tamponnée | décharge, reçu | title, lines[], stamp ; a = signature, b = tampon |
| `aiguillage` | Pièces : chiffre d'affaires par défaut, apport si un document | apport, qualification des fonds | title, left, right, doc ; a = document |
| `echeancier` | 4 cartes d'échéance cochées | délais, remboursement | title, items[[n,unité]], after ; b |
| `dividende` | Le sac d'argent qui sort devient « dividende » | requalification | title, from, to, after ; a |
| `statuts` | Livret des statuts qui s'ouvre, articles vides, tampon | rémunération / indemnité du gérant | title, articles[], stamp ; a, b |
| `piece` | Pièce de 5 F qui tombe puis barrée | « même pas 5 F » | value, unit, title, after ; a |
| `porte` | Porte qui s'ouvre, silhouette qui sort | révocation, renvoi | title, sign, after ; a |
| `duel` | Deux colonnes salarié ≠ gérant | comparer deux statuts | left, right, l_items, r_items ; a |
| `guichet` | Dossier tamponné « non concerné » | administration incompétente | sign, file, stamp ; a |
| `valise` | Valise → maison | partir, rentrer | title, after ; b |
| `ticket` | Ticket de pari, tampon de prélèvement | gains, retenue à la source | title, rows, gain, tax, rate, after ; a, b |
| `agrement` | Appli sur téléphone, « agréée ? » ✖ | agrément, conformité d'une plateforme | app, check, after ; a, b |
| `machine` | Machine à laver « SOCIÉTÉ » avec billets | blanchiment | title, label, after ; b |
| `radar` | Radar qui repère un apport, devient suspect | contrôle, soupçon, LBC | title, blip, verdict ; a, b |
| `contrat` | Convention aux clauses cochées une à une | convention, clauses | title, doc, clauses[] ; a |
| `surligne`, `cinetique` | Phrase prononcée (papier surligné / mots cinétiques) | couvrir un regard | automatique, en rotation avec `citation` |

Regards en TikTok face caméra : `"regard_min": 0.8` (s) dans projet.json — les coups d'œil plus courts
restent naturels ; les regards couverts automatiquement tournent entre `cinetique`, `surligne`, `citation`.
`"filtre_source": "delogo=…,"` efface un filigrane du rush (ex. « dji OSMO POCKET 3 » des exports DJI Mimo :
`delogo=x=78:y=486:w=612:h=84,` en 1728×3072). Exemple complet : `~/monteur video/tiktok_0510/specs.py`.
