---
name: feedback-tiktok
description: "Retours du gérant sur les vidéos TikTok (05/10/2026) — sous-titres sans fautes, variété entre vidéos, musique discrète, miniatures bouche fermée, style de référence"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 67778b14-01b9-4592-bea2-3d777fdb5078
  modified: 2026-10-05T23:07:42.781Z
---

- **Sous-titres et textes à l'écran sans fautes** : il a reproché « des erreurs de grammaire et de conjugaison ».
  Ne jamais recopier l'oral ivoirien mot à mot : réécrire en français écrit correct (sens et ton gardés).
  Outil : `corrige` dans `specs.py` → alignement automatique (`construire.aligner`).
- **Varier le montage d'une vidéo à l'autre** (« je ne veux pas que tout soit identique ») : style de
  sous-titres (`style_sous_titres` : classique, boite, jaune, serif, pop, karaoke), musique (`style_musique` 0–5),
  accroche, zoom (`cinema.push`), animations — en plus de la règle anti-répétition dans une même vidéo.
- **Musique discrète** : `volume_musique` 0.3 (au lieu de 0.55).
- **Miniatures : bouche fermée**, regard caméra, geste posé. Il a rejeté une couverture bouche ouverte.
  Choisir l'image avec `tools/bouche.swift` (ouverture des lèvres) + regard, puis vérifier à l'œil.
- **Référence TikTok qu'il aime** (« INSPECTEUR IMPÔT », @meokpo) : grand titre rouge + blanc en Impact
  derrière la tête dès la 1re seconde, petits sous-titres, illustrations dessinées plein écran.
  → `derriere` avec `"style": "rouge"` et `couverture.py`.

- **Erreurs manifestes entendues dans ses rushes ou son script** (lapsus, mot faux, chiffre douteux,
  phrase incompréhensible) : les lui signaler dans le message de livraison (« juste en bas »), pas dans la vidéo.
- **Une vidéo à la fois** : rendre et envoyer chaque vidéo dès qu'elle est prête, pas tout en parallèle
  (« tu prends énormément de temps »).

**Why:** retours directs pendant la livraison des 6 vidéos TikTok du 05/10/2026.
**How to apply:** pour toute vidéo TikTok/Facebook, partir de `~/monteur video/tiktok_0510/specs.py` comme modèle.
Voir [[feedback-montage-video]] et [[projet-montage-ep01]].

- **Bruit de fond / parasites : à éliminer entièrement avant tout montage** (demande du 06/10/2026, « ne garder
  que ma voix »). Fait automatiquement par le moteur (`work/voix_propre.wav`, `nettoyage_voix.py`, skill §2.2).

- **Jingle (07–08/10/2026)** : ordre voulu = phrase d'accroche → jingle → reste de la vidéo, avec son logo utilisé « tel qu'il est »
  (jamais redessiné) et La Maison de la Conformité (son entreprise) mise en avant. Fait automatiquement par le moteur.

- **Ne pas couper le fond (08/10/2026)** : il a reproché d'avoir coupé des passages « qui allaient faire qu'on
  comprenne la fin » (exemple, chute). Couper seulement bafouillages, faux départs et répétitions ; un passage
  mal compris mais utile au raisonnement est GARDÉ (sous-titre phonétique entre guillemets) et signalé dans le message.

- **Miniatures : ses photos plutôt que des images du rush (09/10/2026)** : il a demandé de changer les miniatures des vidéos 6 et 7
  faites à partir d'images du rush (lèvres pincées, en pleine phrase). Utiliser en priorité ses photos de séance
  (`ep02/work/photos/`, `couverture.photo`) ; s'il n'en reste plus d'inédites, en réutiliser une et lui proposer d'en envoyer d'autres.

- **Bruitages trop forts (13/10/2026)** : « le bruitage est trop fort, réduis ça ». Volume des effets sonores du moteur passé de
  1.15 à 0.45 (`volume_bruitages` dans projet.json pour ajuster) ; effets ajoutés à la main ≤ 0.25. Garder les bruitages discrets.
