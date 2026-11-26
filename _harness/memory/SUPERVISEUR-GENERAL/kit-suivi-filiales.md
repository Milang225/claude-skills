---
name: kit-suivi-filiales
description: Kit de pilotage d'un groupe de sociétés (cockpit Excel 6 registres + note de procédure brandée), rangé dans la base documentaire.
metadata:
  type: project
---

Kit réutilisable produit le 23/09/2026 pour le suivi des FILIALES d'un groupe, rangé dans
`~/Documents/BASE DOCUMENTAIRE LMDC/06_PROCEDURES/KIT_SUIVI_FILIALES` :
- `COCKPIT_SUIVI_FILIALES_MDC.xlsx` (réf. MC-OUTIL-FILIALES-2026-001) — 10 onglets : mode d'emploi,
  paramètres, R0 périmètre, R1 calendrier, R2 vie sociale, R3 flux intragroupe, R4 conventions
  réglementées, R5 comptes réciproques, R6 exposition, tableau de bord. Formules vivantes :
  échéances calculées sur l'exercice, statut EN RETARD, timbre 1 % et son butoir à 30 jours,
  écart de bouclage des réciproques, exposition 25 % + 15 %.
- `NOTE_PROCEDURE_SUIVI_FILIALES_MDC.pdf/.docx` (réf. MC-PROC-FILIALES-2026-001).
- Générateur : `_SOURCES_MD/gen_cockpit_filiales.py` — régénérer par là, jamais éditer le .xlsx à la main.

**Why :** le suivi d'un groupe ne se fait pas filiale par filiale isolément ; le risque est dans les
flux croisés. Doctrine du kit : pas d'intégration fiscale en Côte d'Ivoire, chaque filiale est un
contribuable autonome, et payer pour une société sœur sans refacturer coûte 40 % (réintégration 25 %
+ IRVM 15 %, cumulés même en déficit).

**How to apply :** proposer ce kit dès qu'un client détient une participation dans une autre société.
Premier acte : qualifier l'entité (filiale art. 179 AUSCGIE / succursale art. 116-120 / établissement
secondaire) avant d'ouvrir le dossier. Voir [[kit-organisation-client-mdc]], [[copie-systematique-base-documentaire]].
