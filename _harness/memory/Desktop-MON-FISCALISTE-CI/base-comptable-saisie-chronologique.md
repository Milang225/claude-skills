---
name: base-comptable-saisie-chronologique
description: "Une base comptable se SAISIT datée mois par mois (journal → balance → états) ; jamais tout au 31/12, jamais un compte d'exploitation agrégé en guise de base"
metadata:
  type: feedback
---

**Une base comptable ne se résume JAMAIS à un compte d'exploitation agrégé, et ne se saisit JAMAIS en un bloc au 31/12.** Elle se saisit **chronologiquement** : à-nouveaux au 01/01 → 7 journaux datés (RAN, VTE, ACH, PAIE, OD, BQ, CAIS), chaque opération à sa date, mois par mois → balance → grand livre → états. Le compte d'exploitation est l'**aboutissement**, pas le point de départ.

**Why:** deux reprises du gérant sur LERO (août 2026). D'abord « est-ce comme ça qu'on fait la base comptable ? » quand j'avais présenté un compte d'exploitation agrégé — non, la base c'est le journal. Puis « tu as ramené les écritures en une fois au 31 décembre ? » quand j'avais tout daté du 31/12 — une saisie tout au 31/12 interdit la TVA du mois, le suivi mensuel et une tenue régulière ; c'est un faux.

**How to apply:**
- Seules les écritures d'**inventaire** (dotations, provisions, IRVM sur distributions, régularisations, IMF/TSE/patente annuelles) se datent au **31/12**. Tout le reste est daté à sa période.
- Dates d'achats manquantes → ventiler **au prorata du CA** (flux tendu), solder l'arrondi en **471**, signaler « provisoire, à figer sur relevés ».
- Le **compte d'exploitation se mensualise** aussi (CA réel mensuel, achats prorata, charges fixes 1/12).
- Livrable : `JOURNAL_DE_SAISIE_<CLIENT>_<ANNÉE>.xlsx`. Procédure : skill mdc-expert **§36.1** + `PROCEDURE_SAISIE_BASE_COMPTABLE_MDC`. [[chemin-audit-8-phases]] [[totaux-en-formules-jamais-en-dur]]
