# Charte visuelle (validée sur l'épisode 1)

## Marque
- Bannière de la chaîne : fond bleu nuit, sceau doré « MF » (rosace), « Avec Mon Fiscaliste » en écriture
  manuscrite blanche, « CÔTE D'IVOIRE » en capitales espacées entre deux filets or, devise « SOYEZ EN RÈGLE ».
- Le sceau est redessiné en vectoriel dans le moteur (fonction `seal()`), le nom en **Snell Roundhand**.

## Couleurs
| Usage | Valeur |
|---|---|
| Or (dégradé texte) | `#FFF1C9 → #FFD98A → #E8B64A → #B8862A` |
| Or lumineux italique (mots-clés) | `#E9A92C` + halo `rgba(255,190,70,.75)` |
| Fond sombre des scènes | `#04060C` + éclipse dorée (bord `#FFE2A0`, halo `#F0A532`) |
| Bleu nuit (enveloppe, sceau) | `#16213F` / `#1B274A` |
| Fond blanc des scènes claires | dégradé `#FFFFFF → #F7F4EE → #ECE7DC` |
| Rouge (barré, alerte) | `#FF6B5E` |

## Typographies (système macOS, chargées par Chrome)
- Texte courant, titres : **SF Pro** (`-apple-system`) — 300 pour les phrases, 600–900 pour les titres.
- Chiffres : SF Pro 800 (ou DIN Condensed).
- Marque : **Snell Roundhand** ; monogramme : **Didot**.

## Mouvement
- Apparition signature : flou → net + légère montée (0,4–0,5 s, easing « out quint »).
- Étiquettes en verre : profondeur de champ (flou selon la profondeur), dérive lente, parallaxe.
- Sous-titres : mot par mot, minuscules, SF Pro 600, blanc avec ombre douce ; mots-clés en or italique ;
  en bleu nuit sur les scènes blanches.
- Filigrane : sceau + nom manuscrit en haut à gauche, masqué pendant les scènes plein écran.

## Image vidéo
- Étalonnage neutre et clair (`GRADE` dans `monteur.py`), sans vignettage : ne jamais réchauffer (rendu jaune).
- Zooms : large 1,0×, moyen 1,1×, serré 1,2× (au-delà, la 4K s'amollit). Alternance à chaque coupe visible.
- Short : recadrage 9:16 centré sur le visage, mêmes animations mises en page en vertical.

## Références de style d'origine
1. Vidéo « Je crée un business en 20 min avec 4 IA » (intro) : éclipse orange, verre, mots géants, scènes
   blanches, courbe à étapes, carte « Étape 1 ». Transposée : orange → or, noir → bleu nuit/noir.
2. Vidéo « 4 transitions indispensables » : film burn, masque flicker, flash blanc, whip.
3. Capture « INSPECTEUR IMPÔT » : texte derrière le personnage.
