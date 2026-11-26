---
name: modele-reporting-gestion-mensuel
description: Modèle réutilisable de reporting de gestion mensuel MDC (Excel outil + rapport Word) couvrant comptable/fiscal/social + arriérés.
metadata: 
  node_type: memory
  type: project
  originSessionId: cd403c47-e53d-46ce-81ec-4144cf4dabcc
  modified: 2026-08-03T02:28:54.173Z
---

Modèle STANDARD réutilisable produit le 2026-08-03, à ressortir/adapter à chaque mission de suivi client.

Emplacement : `SUPERVISEUR GENERAL/MODELE REPORTING GESTION MDC/`
- `MODELE_REPORTING_GESTION_MENSUEL_MDC.xlsx` — l'OUTIL, 12 onglets (Paramètres, Tableau de bord, Fiscal-suivi, Social & Paie, Comptable, Banque-cartographie, Caisse-journal, Flux sortants, Registres & obligations, **Arriérés & dettes**, Notation, Anomalies & plan d'action). Listes déroulantes + feux tricolores + formules croisées ; total arriérés en `Arriérés & dettes!G40` repris au tableau de bord.
- `MODELE_RAPPORT_REPORTING_GESTION_MENSUEL_MDC.docx/.pdf` — le LIVRABLE client (12 sections, en-tête MDC) généré depuis `rapport_reporting_gestion.md` via `publish_livrable_mdc.py`.

Cadence mensuelle. Point clé exigé par le superviseur : le modèle doit refléter **les données trouvées à l'analyse**, pas seulement le flux du mois — d'où l'onglet/section **Arriérés** (stock de dettes : principal + pénalités + intérêts 1%/mois, ancienneté, statut de régularisation).

**ÉVOLUTION 2026-08-03 (version retenue) — modèle ANNUEL SIMPLIFIÉ** : `MODELE_REPORTING_GESTION_ANNUEL_MDC.xlsx`. UN SEUL fichier par exercice (pas un par mois), 6 onglets : Paramètres · Tableau de bord · **Suivi mensuel** (matrice obligations × 12 mois, cœur du travail) · Trésorerie & flux · Arriérés & dettes · Anomalies & plan. Note principale = **% de conformité + feu 🟢≥80 / 🟠50-79 / 🔴<50** (obligations ✔ ÷ dues) — le superviseur a jugé la cote AAA→D et les malus trop techniques pour le client. Consolidation annuelle (12 mois + % annuel + feu par volet). Appliqué à GLOBE : `REPORTING_GESTION_2026_GLOBE_CI.xlsx` (avril→juillet remplis, conformité ~26% 🔴). Les versions mensuelles à 12 onglets sont l'itération précédente. Livrables regroupés dans `Documents/METHODOLOGIE LMDC/`.

Règle client complémentaire : le **journal général du kit organisation client** (`FICHIER_DE_SUIVI_OPERATIONS_MDC.xlsx`) doit comporter, en plus de « Réf. pièce / scan », deux cases à cocher par opération — **« Doc. scanné »** et **« Rangé au dossier »** — pour que le client sache s'il a suivi la procédure. Voir [[kit-organisation-client-mdc]].

Rattaché au [[kit-livrables-audit-mdc]] ; respecte [[preferences-livrables]] (pas de délais relatifs J+, échéances en dates fermes) et [[supervision-redaction-avant-livraison]].
