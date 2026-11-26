---
name: equipe-et-plateformes-mdc
description: "MDC's real team (as of Oct 2026) and its platforms (espace client /depot, gestiondocumentaire, crmequipes) — the espace client is \"capital\" for the gérant"
metadata:
  node_type: memory
  type: project
  originSessionId: 3fe2eedf-0d33-4209-be01-08319ab8d0ea
  modified: 2026-10-11T01:42:29.060Z
---

Team per docs/platforms (to be confirmed by the gérant, Oct 2026): BILE FILS Séverin (gérant); SOGBOU Jean-Christian Dominique (superviseur général since 2026-09-07); NIAMIEN Murielle (coordinatrice des dossiers); GNAMIEN Emmanuella (secrétariat); N'CHO Ocho Pierre (fiscalité, chargé de suivi); N'GUESSAN Yao Claude and ACHOURA Timothée (comptabilité — in transition: reserved activity → reconversion or future CGA); AKOCHI Colombe (assistante de direction in Aug docs, status unconfirmed); stagiaires; a "département informatique" exists (names unknown).

Platforms = one Node/Express app on lamaisondelaconformitesarl.net (VPS): client portal /depot/connexion (tabs Documents, Journal général, Caisse, Mobile Money, Paie du mois, Utilisateurs; Importer, Transmettre → sealed PV), admin page /gestiondocumentaire (MDC only), staff space /crmequipes, console /admin. SQLite in prod, PostgreSQL migration on staging. Analysis: `~/LA CONFORMITE LMDC/outils/SYNTHESE_PLATEFORMES.md`; old manuals digest: `outils/SYNTHESE_ANCIENS_MANUELS.md`.

The gérant said the espace client is "capital" and companies must use it, adopted by his own team first. He also requires: before writing any procedure (client or internal), a meeting client + département informatique + dedicated department, then implement and test on the platform, then write the procedure ("cadrage, implémentation, procédure").

**Why:** the A-to-Z design assumed a from-scratch firm; reality is an existing team, clients (Suivi global incl. tenue) and platforms — see `09_PASSAGE_DE_L_EXISTANT.md` (bascule 2026-11-16) and `10_ESPACE_CLIENT.md`.
**How to apply:** tie every procedure/training to real screens; never propose changes to the live platform without the gérant's go (only list them in the "registre des adaptations"); credentials exist in plain text in some files — never copy them. Related: [[refondation-mdc-indice]], [[perimetre-legal-mdc]].
