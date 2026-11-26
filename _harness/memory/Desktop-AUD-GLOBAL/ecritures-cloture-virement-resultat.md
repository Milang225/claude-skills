---
name: ecritures-cloture-virement-resultat
description: Ne pas inclure les écritures RES (virement des comptes 6/7 au résultat) dans les journaux de saisie MDC
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6b19f175-6468-4575-ba37-859025cde7b4
---

Dans les **journaux de saisie** livrés aux comptables (fichiers COMPTABILITE_* / RECONSTITUTION_*), **ne pas inclure les écritures RES-1 / RES-2** (« virement des produits au résultat » D 70x/C 13x-1031-131 ; « virement des charges au résultat » D 13x/C 60-68).

**Why:** ces écritures de détermination du résultat sont **générées automatiquement** par le logiciel comptable (Sage/EBP/Ciel) à la clôture de l'exercice ; le comptable ne les saisit jamais à la main. Les laisser dans le journal a semé la confusion du gérant (« je n'ai jamais passé une écriture de la sorte »).

**How to apply:**
- Journal = uniquement les écritures réellement saisies : à-nouveau, ventes, achats, charges, paie, impôts, trésorerie, **INV** (variation de stocks) et **AMO** (dotations aux amortissements) — ces deux dernières SONT de vraies écritures d'inventaire à garder.
- Retirer RES-1/RES-2, ajuster le total du journal, et porter la mention : « le virement des comptes 6 et 7 au résultat est automatique en logiciel — non saisi ».
- Le résultat reste visible au **Compte de résultat** et au **Bilan** ; la balance est présentée « après clôture » avec la même note.
- Conserver une **page/feuille pédagogique** expliquant le mécanisme (T-compte du 13) pour que le comptable comprenne.

Appliqué (08/07/2026) à NADRELIE (COMPTABILITE_NADRELIE_2025 xlsx+pdf) puis rétroactivement à toutes les bases existantes : KG CONSULTING, SAPHIR TRAVAUX DIVERS, FAMILLE KRA (COMPTABILITE 2025 + RECONSTITUTION 2025 + RECONSTITUTION 2024), RECONSTITUTION_NADRELIE_2025. Sauvegardes `.bak-avant-retrait-RES` créées à côté de chaque fichier. Voir [[reconstitution-kra-nadrelie-2026]].

## Compte technique Sage 890 « Bilan d'ouverture » — ne jamais le montrer dans les écritures
Le **890 « Bilan d'ouverture »** (et **891 « Bilan de clôture »**) sont des **comptes techniques Sage** (à ne pas confondre avec le 89/891 SYSCOHADA « Impôts sur le résultat »). Dans Sage, le report à nouveau reprend les **vrais** comptes ; le 890 n'est qu'un pivot qui doit tomber à zéro. **Décision gérant (08/07/2026) : ne jamais faire figurer le 890 dans les écritures livrées.** Un résidu 890 dans la balance Sage d'un client = **situation nette non affectée** → la reprendre **directement dans le bon compte** de l'à-nouveau (capital 101/103, RAN 12x, c/c associé 462…), sans ligne 890 ni écriture de reclassement (REG). Cas traité : KG CONSULTING — 890 créditeur 1 901 950 repris directement en Capital personnel 103 (2 467 140) dans l'à-nouveau ; REG-01 supprimé ; journal 22 992 890.

**⚠️ Note technique (édition xlsx MDC)** : `openpyxl.delete_rows()` **corrompt les lignes** quand on supprime au MILIEU d'une feuille à cellules fusionnées (des lignes en-dessous perdent leur contenu). Suppressions en fin de feuille = OK. Pour supprimer au milieu : **défusionner tout → delete_rows → refusionner** les lignes pleine largeur (ou régénérer). Toujours re-vérifier ΣD=ΣC ET l'absence de lignes orphelines après édition.

## À-nouveau (AN) hors du journal si le client a déjà sa balance de départ dans son logiciel
**Décision gérant (08/07/2026)** : pour les clients qui **ont déjà leur balance de départ (soldes d'ouverture) dans leur logiciel comptable**, le journal livré ne contient **NI les écritures d'à-nouveau (AN), NI les écritures de clôture** — uniquement les **opérations de l'année (01/01 → 31/12)**. Le logiciel reporte l'ouverture automatiquement ; ressaisir l'AN doublerait les soldes. Note à porter : « la balance de départ est déjà dans votre logiciel — ne pas la ressaisir ». La balance/bilan/CR restent fournis comme états de référence.
- **Concernés (AN retiré) — confirmé** : KG CONSULTING (journal 20 125 000), SAPHIR TRAVAUX DIVERS (journal 27 471 655).
- **NON concernés (AN conservé, = leur balance de départ à établir)** : NADRELIE (reconstituée depuis liasse DGI, pas de logiciel préexistant), FAMILLE KRA.
- Retirer l'AN règle aussi le 890 chez KG (il était dans l'AN).

## ⚠️ Boucle « fenêtre Excel périmée écrasée »
Le gérant ouvre les fichiers dans Excel pour les revoir. S'il **enregistre une fenêtre restée ouverte sur une ancienne version**, il **écrase les corrections faites sur le disque** (arrivé à KG : 890 + clôture revenus). Réflexe : avant d'éditer un fichier, **fermer les classeurs Excel `saving no`** (le disque fait foi), et après édition prévenir de rouvrir la version fraîche sans réenregistrer les fenêtres périmées. Sauvegardes systématiques `.bak-avant-…`.
