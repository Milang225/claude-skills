---
name: refondation-mdc-indice
description: "Oct 2026 redesign of MDC from scratch — \"notation\"/AAA dropped for Indice MDC /100 + exposition; design lives in ~/LA CONFORMITE LMDC"
metadata:
  node_type: memory
  type: project
  originSessionId: 3fe2eedf-0d33-4209-be01-08319ab8d0ea
  modified: 2026-10-11T00:45:22.217Z
---

On 2026-10-10 the gérant asked for MDC (La Maison de la Conformité SARL) to be redesigned from A to Z, after a public Facebook comment (Hermann Guehi) pointed out that "notation" is a regulated term (AMF-UMOA rating agencies like Bloomfield).

Decisions recorded in `/Users/bilefilsseverin/LA CONFORMITE LMDC/` (01_PLAN_DIRECTEUR, 02_METHODE_INDICE_MDC, 03_OFFRES_ET_TARIFS, 04_PROCESSUS_ET_DOCUMENTATION, modeles/, outils/indice_mdc.py + referentiel_mdc_v1.json):
- No more "agence de notation", AAA–D, "visa", "certifié conforme", "audit/auditeur". Instead: Indice MDC de conformité /100 (Maîtrisé/Satisfaisant/Fragile/Exposé/Critique) + exposition estimée FCFA; "attestation de diagnostic".
- One method v1.0 (6 domains, 45 fixed controls), frozen until 2027-10-31. Offer ladder: Diagnostic → Mise en conformité → Suivi.
- MDC does not keep accounts for third parties (ordonnance 2009-387 OECCA-CI); partner with an inscribed cabinet.

- Mission (set by the gérant, same day): not just quantify exposure but **win the control** — "Préparer · Assister · Défendre" (06_MISSION_DEFENSE_CONTROLE.md). Each P/NC observation carries a defense position (FORTE/DISCUTABLE/FAIBLE) + strategy (REGULARISER/DOCUMENTER/DEFENDRE); KPI = taux d'abattement. Key lever: LPF art. 24 régularisation spontanée → only intérêts de retard, impossible once an avis de vérification is received. Ivorian penalties use the "seuil du quart" (art. 162), not "bonne foi".

**Why:** the old setup had 3 conflicting notation grids across skills (notateur-conformite, mdc-expert ×2) and risky regulated wording; the gérant felt lost.
**How to apply:** new client work should use the Indice method and vocabulary. On 2026-10-11 the skills were aligned: a "CHARTE MDC 2026" block (prevails over the rest) sits at the top of 16 MDC skills; generator headers read "Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social"; publish_pdf_mdc.py / publish_livrable_mdc.py block technical jargon and old vocabulary; notateur-conformite rewritten around indice_mdc.py (old noter.py → noter_ancien_abroge.py); mdc-expert old sections (mission type 1/2, AAA grids, visa/certification) carry ⛔ ABROGÉ banners; diagnostic-financier uses word levels (Très solide → Critique). Backup: ~/.claude/sauvegarde-skills-avant-charte-2026-10-11.tar.gz. Business PDFs: ~/LA CONFORMITE LMDC/PDF via outils/generer_pdf.py — the gérant objected strongly to file names, commands or code blocks in documents; never put them in anything he or clients read. See [[feedback-decider-sans-questions]].
