---
name: kit-detection-terrain
description: Kit de détection terrain MDC (créé le 20/09/2026) — référentiel de 139 indices, carnet Excel, fiche réflexe, note de service MC-NS-2026-004 ; obligatoire dès le 28/09/2026.
metadata:
  type: project
---

Outil construit le 20/09/2026 pour répondre à [[outillage-terrain-collaborateurs]]. Vit dans `~/Documents/ARCHIVES DOCUMENTS/MACHINE LMDC/1_OUTILS/AUDIT/KIT_DETECTION_TERRAIN/` (copie dans BASE DOCUMENTAIRE LMDC/06_PROCEDURES).

Cinq pièces : **référentiel** MC-OUT-2026-001 (40 p., 11 familles A→K, **160 indices**, chacun = fait observable / où chercher / ce que ça déclenche avec l'article du CGI / preuve / question à poser) · **carnet de terrain** Excel 16 onglets (dont catégorisation des sorties du relevé qui chiffre le risque par RECHERCHEV, et synthèse automatique) · **fiche réflexe** MC-OUT-2026-002 · **note de service** MC-NS-2026-004 (obligatoire pour toute mission engagée à compter du 28/09/2026) · **module MC-OUT-2026-003 « Qualifier l'activité et l'assiette »** (vente ou commission ; faisceau de 12 questions ; 4 secteurs : commerce, services, mines, transit).

Le carnet contient un onglet **DROITS DE TIMBRE** (calculateur : quittances par tranche, dépôts d'espèces, 1 % sur apports en compte courant et effets, connaissements, timbre de dimension → total dû / déclaré / écart ; testé : 651 200 F sur un cas d'école) et un onglet **QUALIFICATION ACTIVITE** : les 12 questions à verdict automatique + un simulateur qui compare l'assiette « vente » et l'assiette « commission » (régime, TEE 4/5 %, micro 6/4 %, IMF 0,5 % min 3 M max 35 M, patente 0,5 % min 300 000, TVA 18 %). Test de référence : 500 M de volume à 5 % → 5 500 000 contre 1 180 000, soit 4 320 000 d'écart annuel.

**Texte manquant à archiver :** l'AUDCG (Acte uniforme OHADA droit commercial général — intermédiaires de commerce : commissionnaire art. 192-207, courtier 208-215, agent commercial 216-233) n'est PAS dans la base locale ; droit-afrique, acpce.cg et actualitesdroitohada renvoient 403 ou 404 à WebFetch. Tant qu'il n'est pas archivé, ne pas citer son texte entre guillemets dans un livrable. Le Code du travail manque aussi.

La base vit dans `_SOURCES/indices.py` ; `build_carnet.py` et `build_referentiel.py` régénèrent les deux livrables à partir d'elle — **toujours modifier la base, jamais le carnet ou le référentiel à la main**, sinon les deux divergent.

**Why :** transférer aux collaborateurs l'œil du contrôleur, pas le manuel fiscal.
**How to apply :** à déployer aux étapes 3-4 du parcours audit du [[machine-lmdc-procedure]] ; enrichir le référentiel de chaque fait nouveau rencontré en mission. `mdutil.unwrap()` doit être appliqué à toute source .md avant publication (le générateur MDC ne convertit pas un gras coupé en fin de ligne et bloque la règle d'or).
