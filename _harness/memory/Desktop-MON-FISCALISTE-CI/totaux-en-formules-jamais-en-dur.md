---
name: totaux-en-formules-jamais-en-dur
description: "Dans tout classeur MDC, un total ou un montant net est une FORMULE =SUM vivante, jamais un nombre tapé ; la déduction est stockée en négatif"
metadata:
  type: feedback
---

**Un total ou un montant net dans un classeur MDC est TOUJOURS une formule Excel vivante `=SUM(...)`, jamais un nombre saisi en dur.** La déduction (TVA déductible, remise, acompte) est **stockée en négatif** : `=SUM` fait alors la soustraction toute seule, et il devient **structurellement impossible d'additionner une déduction** au lieu de la soustraire.

**Why:** le gérant a relevé sur LERO le 24/07/2026 une TVA à payer fausse — 8 408 867 = collectée 4 964 086 **+** déductible 3 444 781, au lieu de collectée **−** déductible = 1 519 305 : « depuis quand pour trouver la TVA à reverser on additionne ? ». La cause racine : le total était un littéral tapé indépendamment des lignes. Une formule vivante l'aurait rendu impossible — et elle se recalcule si on modifie une ligne.

**How to apply:**
- Construire les chiffrages avec le helper **`scripts/blocs_mdc.py`** (`Bloc.ligne` puis `Bloc.total` → écrit `=SUM()`; `finaliser(wb)` pose `fullCalcOnLoad=True`).
- Toute **déduction se saisit en négatif**, jamais en positif « à soustraire mentalement ».
- Le convertisseur **`xlsx_to_pdf_mdc.py`** évalue les `=SUM()` et formes mixtes (`=B29+SUM(B30:B39)`) : le PDF affiche la valeur sans ouvrir Excel.
- Filet de sécurité : contrôle **⑤** de `controle_coherence_dossier.py` bloque tout net obtenu par addition d'une déduction.

Triple garantie = formule vivante + assert Python à la construction + contrôle ⑤ détectif. Skill mdc-expert **§35.3bis**. [[controle-coherence-fin-de-travaux]] [[chemin-audit-8-phases]]
