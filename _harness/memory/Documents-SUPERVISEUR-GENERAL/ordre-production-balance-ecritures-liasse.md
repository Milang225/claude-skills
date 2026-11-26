---
name: ordre-production-balance-ecritures-liasse
description: "Ordre de production d'un dossier compta/EF — la BALANCE d'abord, validation, PUIS les écritures (Sage) et la liasse"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3ee849da-289c-481f-9216-13abd1e858fa
  modified: 2026-10-30T20:42:26.709Z
---

Sur un dossier comptable / états financiers, le gérant veut cet ordre (règle du 30/10/2026, dossier MABEK) :
1. **Produire la BALANCE d'abord** et la lui montrer — modèle brandé MDC : Compte · Intitulé · Total débit · Total crédit · Solde débiteur · Solde créditeur, avec la ligne TOTAUX et les deux contrôles à zéro (mouvements débit = crédit ; soldes débiteurs = créditeurs).
2. **Dès qu'il valide la balance (« c'est bon »)**, passer aux **ÉCRITURES** (journal au format d'import/saisie Sage) et à la **LIASSE** DGI.

**Why:** la balance est le socle ; les écritures, la liasse et les EF en découlent sans rien inventer. Valider la balance avant de propager évite de tout refaire (leçon MABEK : plusieurs allers-retours avant d'arrêter la balance).

**How to apply:** ne jamais sauter directement à la liasse ou aux EF avant d'avoir montré la balance et obtenu l'accord. Les écritures se livrent au format Sage (Journal · Date · Pièce · Compte · Intitulé · Libellé · Débit · Crédit ; journaux AN / VT / BQ / OD) — c'est ce que les collaborateurs saisissent dans Sage. Générateurs MABEK réutilisables : `build_balance_xlsx.py`, `build_ecritures_sage.py`, `build_liasse_smt_2025.py`. Voir [[elaborer-ef-suivant-la-liasse]] et [[mdc-elabore-ef-ne-vise-pas]].
