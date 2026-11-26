---
name: elaborer-ef-suivant-la-liasse
description: "« Élaborer des états financiers » = les couler dans la liasse fiscale DGI (SMT ou SN selon le régime), pas seulement un bilan/CR maison"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3ee849da-289c-481f-9216-13abd1e858fa
  modified: 2026-10-30T19:07:32.941Z
---

Quand le gérant demande d'« élaborer les états financiers » d'un client, il veut qu'on les coule dans la LIASSE FISCALE DGI (modèle officiel) — Système Normal (SN) ou Système Minimal de Trésorerie (SMT) selon le régime —, pas seulement produire un bilan / compte de résultat / TFT maison.

**Why:** c'est le format que le cabinet d'expertise comptable valide et que la DGI reçoit ; le bilan/CR « maison » n'est qu'une étape de travail.

**How to apply:** modèles vierges dans `ARCHIVES DOCUMENTS/DOCS DGI/` — `LIASSE FISCALE DGI SN (1).xlsx` (146 onglets) et `LIASSE SMT (2).xlsx` (41 onglets). La liasse est pilotée par l'onglet **BALANCE N** (et **BALANCE N-1**) : on y injecte la balance (colonnes A=compte, B=intitulé, G=S.F. débit, H=S.F. crédit) et l'identité (onglets **ENTITE** et **FICHE R1**) ; le bilan, le compte de résultat, le TFT et les notes se calculent seuls par des `SUMIF` sur les préfixes de comptes (colonnes auxiliaires I–P = `LEFT(compte,n)`). openpyxl n'évalue pas les formules : poser `wb.calculation.fullCalcOnLoad = True` pour que tout se recalcule à l'ouverture dans Excel, et vérifier l'équilibre en rejouant les agrégats en Python. Le régime (donc SMT ou SN) dépend de l'activité, pas seulement du CA : seuils AUDCIF art. 13 = négoce < 60 M, artisanat < 40 M, services < 30 M ; distinct du régime fiscal (microentreprise/entreprenant). MABEK 2025 = SMT (négoce, CA 43 070 000 < 60 M) : `build_liasse_smt_2025.py` (la feuille Balance du modèle SMT est une grille à lignes fixes par code ; mapper chaque compte sur sa ligne, C=débit/D=crédit, avec OVERRIDE vers les feuilles 706101/8121/1981 quand on tombe sur un sous-total). Actif = passif = 55 860 000, résultat 21 379 442. Voir [[mdc-elabore-ef-ne-vise-pas]].

Pièges du modèle SMT (`LIASSE SMT (2).xlsx`) : le sous-total 641 de la feuille Balance (ligne 629) omet la ligne 6418 ; le corriger dans la copie (ajouter +C637 etc.), sinon la TEE sort des impôts. Le BILAN condensé L12 ne prend que le résultat (pas le report à nouveau) : y loger RAN + résultat. LibreOffice n'est pas installé ; pour vérifier les formules, utiliser le module Python `formulas` (ExcelModel().loads(f).finish().calculate()). Exemple complet : `DOSSIER CLIENTS/KWAANI SERVICES/ETATS FINANCIERS 2025/_SOURCES_MD/build_liasse_smt_2025.py`.
