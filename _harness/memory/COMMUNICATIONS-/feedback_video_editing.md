---
name: Feedback montage vidéo — Bilé Fils Séverin
description: L'utilisateur attend de vrais effets/transitions/légendes sur ses montages YouTube, pas un simple split-screen statique
type: feedback
originSessionId: e01d6bdc-9c51-4d3c-a307-980dd4384902
modified: 2026-10-27T19:36:25.686Z
---
Sur les montages vidéo YouTube/Shorts pour Bilé Fils Séverin, ne JAMAIS livrer un simple split-screen statique sans effets — il considérera ça "boff, rien de spécial".

Ce qu'il attend par défaut sur tout montage :
- **Légendes karaoké** burned-in (style Submagic/Captions.ai), pop mot par mot, blanc + stroke noir épais (style @steph.mormand TikTok validé comme référence le 2026-05-07).
- **B-roll / plans de coupe pertinents** insérés aux moments-clés (illustrer le mot prononcé). À demander à l'utilisateur s'il n'a pas fourni de matériel B-roll.
- **Audio normalisé** broadcast (-16 LUFS via loudnorm).

**❌ À NE PAS faire** (rejetés explicitement) :
- Pas de logo / watermark Mon Fiscaliste sur les vidéos.
- Pas de Ken Burns, pas de fade in/out, pas de flash transitions, pas de vignette.
- Pas de cartons intro/outro pleine page.
- Pas de musique de fond (le style validé n'en a pas).
- Pas de jump cuts agressifs sur les silences (cf. règle critique ci-dessous).

**Why** : il a explicitement rejeté un premier rendu split-screen statique avec "il n'y a pas de transitions, il n'y a pas d'effets, la vidéo est boff". Sa référence stylistique est Macron / Villepin pour le ton, mais visuellement il veut bien la dynamique moderne YouTube/Shorts.

**How to apply** : ne jamais demander "tu veux que j'ajoute des effets ?" — proposer/livrer directement la version riche. La transcription via faster-whisper (modèle `small`, fr) est installée et fonctionne. Pipeline ffmpeg type dans `/tmp/filter.txt` (pendant la dernière session) — réutilisable comme base.

---

**RÈGLE CRITIQUE : NE PAS supprimer les silences de Bilé.** Ses silences font partie de sa communication non-verbale (regards appuyés, gestes qui finissent la phrase, pauses dramatiques type Macron/Villepin). Le style "jump cuts agressifs" sur les silences (à la steph.mormand) ne convient PAS à son ton autoritaire de fiscaliste.

**Why** : il l'a explicitement dit le 2026-05-07 — "les silences dans mes vidéos ont aussi un impact dans ma communication non verbale".

**How to apply** : par défaut, garder TOUS les silences. Si jump cuts nécessaires, demander avant et limiter aux pauses > 2.5-3s vraiment mortes. Le "punch" doit venir des légendes pop synchronisées + recadrage + B-roll pertinent, PAS de la suppression de silences.

---

**Générique d'ouverture : OUI** (demandé le 2026-10-27, « tu as oublié le générique »). Séquence animée de 2,8 s en tête : fond sombre, ligne or, « MON FISCALISTE » dont les lettres se resserrent, « Bilé Fils Séverin · Fiscaliste », reflet sur le titre, coupe franche. Script : `generique.py` (scratchpad de la session du 2026-10-27). C'est la seule exception à la règle « pas de carton ».

Le 2026-10-27, il a aussi rejeté le bandeau-titre fixe en haut et le texte `@monfiscaliste` (« enlève ceux-là »). Il a confirmé : silences gardés, pas de musique, zoom, vignette ni carton de fin.

**Référence visuelle validée** (envoyée 2026-05-07) : le compte TikTok @steph.mormand. Style à reproduire pour le rendu visuel uniquement : vertical 9:16, légendes blanches gras + stroke noir épais centrées vers y=60%, sync mot-à-mot, watermark en bas à droite, **aucun** Ken Burns / vignette / flash / fade / musique / cartons pleine page. Voir `/tmp/ref_frames/` pour exemples de frames analysées.
