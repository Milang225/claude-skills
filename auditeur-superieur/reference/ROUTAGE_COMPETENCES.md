# Table de routage — Auditeur Supérieur

> Réflexe de pilotage : *quelle demande → quelle base ouvrir → quelle fiche appliquer*.
> Racine repo : `/Users/bilefilsseverin/Desktop/AUD GLOBAL/`. Skills : `~/.claude/skills/`.

## 1. Par nature de question

| La demande porte sur… | Base à ouvrir d'abord | Fiche / skill |
|---|---|---|
| Un taux, un régime, une sanction, une optimisation fiscale | `fiscal-knowledge/` (README puis 0X ciblé) | skill `auditeur-fiscal` |
| Une écriture, un compte, une clôture, un état financier | `comptable-knowledge/` | skill `comptable-ebnl` |
| Reconstituer une base à partir des états | `comptable-knowledge/` + Manuel d'analyses fiche 2 | fiche 2 |
| Catégoriser un relevé bancaire | Manuel d'analyses fiche 3 | fiche 3 (entrées ET sorties) |
| Déterminer le vrai chiffre d'affaires | Manuel d'analyses fiche 4 | fiche 4 |
| Vérifier si la trésorerie / le compte est sincère | Manuel d'analyses fiche 5 | fiche 5 |
| Savoir quel régime s'applique / si bascule due | `fiscal-knowledge/03-regimes.md` + fiche 6 | fiche 6 |
| Chiffrer le risque en cas de contrôle | `fiscal-knowledge/06-sanctions.md` + fiche 7 | fiche 7 |
| Réserves, capitaux propres, distribution, réévaluation | fiche 8 + `fiscal-knowledge/07-optimisation.md` | fiche 8 |
| CNPS, ITS, contrats, bulletins, inspection du travail | `fiscal-knowledge/05-impots-divers.md` (ITS/FDFP) + Manuel procédure (pôles social & inspection) | pôles D & Inspection |
| Coder / coter / noter les anomalies | `notation-knowledge/` + fiches 9-10 | skill `notateur-conformite` |
| Quelles pièces demander au client | `methodologie-audit/02-catalogue-pieces-obligatoires.md` | catalogue |
| Quelle trame / courrier / grille utiliser | `methodologie-audit/04-kit-demarrage-trames.md` | kit |
| Par où commencer / quel livrable ensuite | `methodologie-audit/01-manuel-procedure-audit-global.md` | manuel de procédure |
| Produire un document brandé MDC | skill `mdc-expert/scripts/publish_*` | générateurs |

## 2. Par phase de mission

| Phase | Réflexe | Livrable attendu |
|---|---|---|
| 0 Onboarding | Kit trames 1-4 → mémo client + demande de pièces | MC-NDM, MC-DPJ |
| 1 Diagnostic | Fiche 1 (OCR) + fiche 2 (bouclage) | Rapport intermédiaire + pièces manquantes |
| 2 Audit par pôle | Fiches 2-6 selon le pôle | Base reconstituée + matrice d'anomalies |
| 3 Consolidation | Fiches 7-8 + passage compta→fiscal | Exposition chiffrée + écritures de régularisation |
| 4 Notation & clôture | Fiches 9-10 + moteur de notation | Rapport de notation + plan d'action + visa |

## 3. Réflexes de croisement (là où les compétences se rencontrent)

- **CA reconstitué > seuil de régime** → déclenche à la fois le volet *fiscal* (bascule RME→RSI, natures d'impôts) et *comptable* (retraitement produits 706, PCA/CCA). Traiter les deux.
- **Retraits d'espèces / créditeurs non justifiés** → volet *comptable* (justification, caisse) + *fiscal* (requalification, IRVM, taxation d'office) + *notation* (observation critique domaine A/F).
- **Masse salariale** → *comptable* (compte 66) + *social* (CNPS, ITS) + *fiscal* (déductibilité, ITS). Ne jamais compter deux fois le patronal (piège vérifié).
- **Sorties de fonds vers l'étranger / vers le dirigeant** → *fiscal* (IRVM 15/17 %, retenue à la source) + *notation* (séparation des patrimoines, domaine F).

## 4. Règle de priorité en cas de conflit

1. **Bouclage** avant tout : pas de reconstitution ni de notation sur des états qui ne bouclent pas.
2. **Source** avant affirmation : ouvrir la base, citer ; à défaut « (référence à confirmer) ».
3. **Doctrine DGI / BODGI** avant de finaliser un conseil fiscal ; sinon signaler « position à confirmer ».
4. **Cohérence pipeline** : une correction amont se répercute sur rapport, PDF, notation, plan d'action.
