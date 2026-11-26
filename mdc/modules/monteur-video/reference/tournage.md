# Captation cinématographique — méthode de tournage

Synthèse des références qui font autorité (American Society of Cinematographers « Shot Craft : The Talking
Head », CineD, guides Blackmagic Camera / Apple Log) appliquée au studio du gérant et à son matériel
(iPhone Air + app Blackmagic Cam + micro DJI). À donner au gérant AVANT un tournage ; au montage, on ne
fait que simuler ce qui n'a pas été capté.

## 1. Diagnostic du rush de l'épisode 1 (métadonnées + images)
| Constat | Effet | Correction |
|---|---|---|
| Obturateur **1/257 s** à 24 i/s | Mouvements saccadés, rendu « vidéo » | **180°** : 1/50 s à 25 i/s |
| 24 i/s en pays 50 Hz | Risque de scintillement des LED / néons | **25 i/s** (Côte d'Ivoire = 50 Hz) |
| Dos collé au mur blanc, plus lumineux que le visage | Image plate, visage sous-exposé | S'éloigner du mur (2–3 m), fond **1 à 2 diaphragmes plus sombre** que le visage |
| Néon vert derrière | Jure avec l'or de la marque, reflets verts | Néon ambre/or ou éteint ; lampe chaude en fond |
| Lumière plate de face / fenêtre | Pas de modelé | Source douce à 45°, côté « large », au-dessus des yeux + négatif côté ombre |
| Un seul angle | Sauts d'image à chaque coupe, tout doit être couvert par des animations | 2e téléphone à 30–45°, plus serré |
| Regard qui part vers les notes | ~80 % d'animations nécessaires pour couvrir | Prompteur sous l'objectif |
| Voix uniquement sur le canal gauche | Oreille gauche seulement (corrigé au montage) | Enregistrement interne DJI (WAV 32 bits flottants) + vérifier le routage audio |

## 2. Réglages caméra (Blackmagic Cam sur iPhone)
- Résolution **4K**, cadence **25 i/s**, obturateur **angle 180°** (l'app garde 1/50 s automatiquement).
- ISO le plus bas possible ; l'exposition se règle avec la **lumière** (intérieur) ou un **filtre ND** (extérieur),
  jamais en montant l'obturateur.
- Balance des blancs **verrouillée** (même valeur sur les deux téléphones), ex. 5600 K avec des LED « jour ».
- Mise au point **verrouillée sur les yeux**, exposition verrouillée, stabilisation **désactivée** sur trépied.
- Codec : débit maximal. Si l'iPhone propose **Apple Log** (modèles Pro) : Log + ProRes ou HEVC, LUT en aperçu
  seulement ; sinon profil standard (le moteur a un étalonnage neutre prêt). HDR vidéo **désactivé**.
- Objectif : préférer le **cadrage ×2 (≈ 52 mm)** à 1,5–2,5 m plutôt que le 26 mm de près : visage plus
  flatteur, fond compressé et plus flou.
- Contrôle : zébras/fausses couleurs pour que la peau soit correctement exposée (peau foncée : ne pas la
  sous-exposer ; exposer pour le visage, pas pour le mur).

## 3. Lumière (du plus important au bonus)
1. **Clé** : grande source douce (softbox 60–90 cm ou fenêtre diffusée) à ~45° du visage, légèrement au-dessus
   des yeux, côté vers lequel le visage est tourné (« côté large ») ; c'est elle qui fait l'image.
2. **Négatif** : tissu/panneau noir côté opposé pour creuser l'ombre (modelé cinéma) ; si trop contrasté,
   un réflecteur blanc à la place.
3. **Contre-jour** : petite lumière derrière, en hauteur, sur les épaules/cheveux : décolle la silhouette du fond.
4. **Fond** : plus sombre que le visage (1–2 diaphragmes) ; une **lampe d'ambiance chaude** dans le champ
   (« practical ») donne de la profondeur ; fond légèrement plus froid que la peau.
5. Couper les plafonniers (lumière du dessus = cernes).

## 4. Cadrage et décor
- Plan poitrine (medium close-up) ; les **yeux au tiers supérieur** ; caméra **à hauteur des yeux**.
- Pour YouTube (adresse directe), regarder **l'objectif** — un prompteur rend cela naturel.
- Se placer **en biais** par rapport au mur (lignes de fuite) plutôt que face à un mur plat ; décor sobre,
  1–2 éléments de marque (sceau MF, plante, lampe).
- 2e caméra (B-cam) : même côté de l'axe (règle des 180°), décalée d'au moins **30°**, plus serrée ; le
  montage coupe dessus pour les phrases fortes et à la place des sauts d'image.
- Mouvement : un **slider** lent ou un zoom très progressif sur la B-cam ; pas d'épaule sur de longues prises.

## 5. Son
- DJI Mic : enregistrement interne **32 bits flottants** activé, micro 15–20 cm sous le menton, câble et
  bonnette cachés ; pièce la plus sourde possible (rideaux, tapis).
- Clap de synchronisation (frapper des mains) au début de chaque prise si deux caméras ou son séparé.

## 6. Ce que le montage simule quand le tournage ne l'a pas fait (moteur `monteur.py`, bloc « cinema »)
- **Travelling virtuel** : zoom avant très lent sur chaque plan (`push`, 4,5 % par défaut).
- **Profondeur de champ simulée** : détourage Apple Vision, fond flouté, ½ diaphragme plus sombre, un peu plus
  froid ; la peau n'est pas touchée (`profondeur`, `flou_fond`, `fond`).
- Alternance de cadrages (large / moyen / serré ≤ 1,2×) pour masquer les sauts d'image.
- Limite : une vraie profondeur de champ optique, une vraie lumière et un vrai 2e angle restent supérieurs.

## Fiche de tournage (à envoyer au gérant)
Page à cocher sur téléphone, publiée : https://claude.ai/artifact/Cw9zHVxM5WFi2Bxf7x7gnj — la mettre à jour
(republication avec cette URL) quand la méthode change. Source HTML : `exemples/fiche_tournage.html`.

## Sources
- ASC — Shot Craft: The Talking Head — https://theasc.com/article/shot-craft-the-talking-head-shooting-interviews/
- CineD — 8 Easy Rules To Enhance Your Interview Lighting — https://www.cined.com/8-cinematography-tips-making-interview/
- Recherche « short side / negative fill / fond 1–2 diaphragmes plus sombre » (Peerspace, MACCAM, Daniel Grindrod)
- Guides Blackmagic Camera / Apple Log (cinem8, Absoluts, Freewell) — https://cinem8.co/blogs/blog/iphone-camera-settings-for-cinematic-videos-apple-log-guide
- Règle des 30° — https://en.wikipedia.org/wiki/30-degree_rule
