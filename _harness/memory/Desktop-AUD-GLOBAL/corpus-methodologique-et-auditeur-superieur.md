---
name: corpus-methodologique-et-auditeur-superieur
description: "Corpus méthodologique d'audit (4 manuels + kit) dans methodologie-audit/ et skill maître auditeur-superieur"
metadata: 
  node_type: memory
  type: project
  originSessionId: c8a5d90f-6542-40c6-9ee2-e3d95bcfa503
  modified: 2026-08-15T00:12:46.465Z
---

Capitalisation de la méthode d'audit MDC (créée le 23 juillet 2026, à partir de la mission Saint-Exupéry anonymisée en « Établissement E »).

**Corpus** dans le repo `methodologie-audit/` (sources Markdown maîtresses) :
- `01-manuel-procedure-audit-global.md` — procédure, phases 0-4, 7 pôles, chaîne des livrables, gouvernance qualité.
- `02-catalogue-pieces-obligatoires.md` — 57 pièces sur 7 domaines.
- `03-manuel-analyses-techniques.md` — 10 fiches (OCR, reconstitution, catégorisation bancaire, CA réel, sincérité trésorerie, régimes, exposition, ingénierie réserves, codification, notation).
- `04-kit-demarrage-trames.md` — 8 trames prêtes à remplir.
- `README.md` — index.

Versions brandées Word + PDF (63 pages) dans `~/Documents/MDC - MANUELS & PROCEDURES/`, générées via `publish_pdf_mdc.py` / `publish_livrable_mdc.py` (skill mdc-expert).

**Échelle de notation canonique** = celle de `notation-knowledge/` : AAA/AA/A/BBB/BB/B/CCC/CC/C/D sur /20 (l'ancienne échelle A→E est abandonnée). Grille de référence à 7 domaines (Trésorerie 20, CA 20, Fiscal 20, Paie/social 15, Compta/bilan 15, Séparation patrimoines 5, Documentaire 5).

**Skill maître** `~/.claude/skills/auditeur-superieur/` (SKILL.md + reference/ROUTAGE_COMPETENCES.md) : chef d'orchestre qui réunit fiscal + comptable + social/droit du travail + méthodo + notation, et route vers les bases/skills spécialisés ([[mission-audit-all-in-one-consulting]] et autres missions s'y appuient). IRVM taux de travail retenu 15 % (17 % PP), « à confirmer » selon LF.

**Skill de production** `~/.claude/skills/producteur-livrables-audit/` (SKILL.md + reference/CATALOGUE_LIVRABLES_AUDIT.md), créé le 15 août 2026 : a À SA CHARGE le catalogue complet des ~30 livrables d'une mission d'audit (phases 0 à 5), chacun avec sa réf. `MC-⟨TYPE⟩-⟨SECT⟩-⟨AN⟩-NNN`, son skill de fond, son format, son générateur (`publish_*` pour les rédactionnels ; `build_*.py` reportlab pour exposition/trésorerie/visa/constat/synthèses visuelles) et sa destination. Intervient EN AVAL de auditeur-superieur ; complète le skill générique `producteur-livrables` (lui orienté déclarations/compta courante) en se spécialisant sur l'audit. Gabarit de référence = dossier `COLLEGE ST EXUPERY 2/` (structure 00_PIECES_RECUES → 09_SUIVI_ET_VISA + _A_ENVOYER). Porte la charge de complétude et de cohérence : chiffres pivots identiques partout, écart tranché par retour à la pièce source (jamais de mémoire — leçon retraits 117 564 035 vs 115 567 035), livrables sensibles (exposition, qualification CCA) remis séparément.
