---
name: feedback-ecritures-notes-de-revue
description: Toute écriture comptable MDC doit passer par le module skill ecritures-sans-faute (script de contrôle + grille de rapprochements) — exigence née des notes de revue de visa du 11/11/2026.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 93ef899f-773d-4811-9a4e-3b59899a8ccf
  modified: 2026-11-11T12:50:27.773Z
---

Aucune écriture, journal, ordre de saisie Sage, balance ou liasse ne se remet sans : comptes vérifiés dans le plan AUDCIF, `controle_ecritures.py` à zéro erreur, grille de rapprochements (déclarations e-impôts, relevés, PV de caisse, EF N-1) remplie.

**Why:** le 11/11/2026, le gérant a reçu des notes de revue de visa (FAMILLE KRA, KWAANI, KG CONSULTING ; TIM 7 le 13/10/2026) relevant « graves erreurs, écritures hyper mal faites, incohérences, numéros de comptes mal faits ». Le contrôle des écritures TRACE LOGISTICS que j'avais produites en juin 2026 a sorti 12 erreurs bloquantes (6313, 4611, 4616, 629000, 624x, 626000, 604000, 701 pour des services, tout daté du 31/12). Les bons comptes étaient déjà dans mdc-expert : la faute était d'écrire les numéros de mémoire. Le gérant a ensuite précisé que les ITS/FDFP et le stock FAMILLE KRA étaient mal passés : écritures MDC du 02/11/2026 avec « 6414/5 », 2,8 % en 6413, racine 447, paiements ITS regroupés, D 311 / C banque-caisse 41,8 M, stock final 0 sans inventaire, aucun achat 601. Règle : ITS/FDFP = une ligne d'écriture par ligne de la déclaration mensuelle, paiement à la date de chaque quittance ; stock seulement via 601 et 6031 sur PV d'inventaire.

**How to apply:** charger `~/.claude/skills/mdc/modules/ecritures-sans-faute/MODULE.md` avant toute écriture ; exporter les écritures en CSV et lancer le script avant de produire PDF/Excel ; chaque opération à sa date, tiers nominatif, charge = montant déclaré. Même si le client demande « tout au 31 décembre », signaler que les réviseurs le rejettent (R1). Ajouter chaque nouvelle note de revue au catalogue `reference/CATALOGUE_NOTES_DE_REVUE.md`. Voir [[client-trace-logistics]].

Précision du gérant (11/11/2026) : la classe 89 (891 impôt sur les bénéfices, 895 IMF) est réservée aux entreprises au régime du réel (RSI, RNI) ; au forfait (TEE et régime des microentreprises) aucun compte 89, impôt en 6418 / 446. Toujours lancer le contrôle avec `--regime`.

Depuis le 11/11/2026, second regard obligatoire après le contrôle : module `auditeur-comptable` (`audit_comptable.py tout JOURNAL --exercice --forme --regime [--n1 BILAN_N-1]`, trois axes écritures / principes / mises à jour) ou agent `auditeur-comptable` sans lui donner mes conclusions. Chaque nouvelle faute de revue → aussi un cas dans `CAS_NON_REGRESSION` du script de l'auditeur.
