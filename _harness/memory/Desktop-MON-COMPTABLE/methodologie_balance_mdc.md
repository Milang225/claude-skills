---
name: methodologie-balance-mdc
description: "Méthodologie standard MDC pour traiter toute balance comptable cliente — format 6 colonnes, exhaustivité absolue, audit contradictoire, étude fiscale, liasse SN. Capitalisée sur le cas BUILDING NEW AFRICA 2025."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 489d2c42-e377-49c0-9928-1f3fbf20f979
---

Méthodologie unique MDC pour toute balance reçue, à appliquer **systématiquement et sans demander d'autorisation** (le SKILL `mdc-expert` §12-17 contient le détail).

## Format obligatoire de travail
**Balance 6 colonnes** : `N° compte (8 chiffres EXACTS) | Intitulé EXACT | Mvt Débit | Mvt Crédit | Solde Débit | Solde Crédit`

## Workflow 4 livrables successifs
1. **Liasse SN** (`LIASSE_<CLIENT>_<ANNÉE>.xlsx`) — 9 onglets : 0-Bouclage / 1-Balance / 2-Bilan / 3-CR / 4-Notes / 5-Régul / 6-Synthèse indicateurs / 7-Rapport audit final
2. **Étude fiscale** (`ETUDE_FISCALE_<CLIENT>_<ANNÉE>.xlsx`) — 4 onglets : Passage compta-fiscal / Conformité déclarative / Exposition fiscale / Plan d'action fiscal
3. **Rapport contradictoire** (agent auditeur déployé en parallèle, jamais omettre)
4. **Rapprochement bancaire** si relevé fourni (`RAPPROCHEMENT_<CLIENT>_<MOIS>.xlsx`)

## Règles absolues à ne JAMAIS violer
- **EXHAUSTIVITÉ** : tous les comptes, sans omission, sans raccourci, sans normalisation
- **BOUCLAGE en premier** : si écart > 1 FCFA et version structurée disponible → STOP + demander Excel
- **TRANSPARENCE** : écart résiduel toujours documenté dans onglet `0-Bouclage`
- **EXPORT EXCEL PRIVILÉGIÉ** : PDF Sage = source d'erreurs (lignes compactes, valeurs ambiguës)
- **CONTRADICTION** : déployer un agent auditeur indépendant systématiquement
- **SOURCING** : citer l'article exact (CGI CI, AUSCGIE, AUDCIF, AUPCAP, Code prévoyance)

## Erreurs juridiques à ne plus reproduire
- SARL → art. **371 AUSCGIE** (pas 664 qui est pour SA)
- IMF Côte d'Ivoire → **max(3 000 000 ; 0,5% CA HT)** plafonné 35 M
- CNPS patronale BTP CI → **15-18%** (pas 11,2% présumé)
- Sous-traitance BTP 55-75% du CA = **normal**, pas anomalie
- CCA non rémunérés → **pas de sous-cap fiscale art. 18**
- IS comptabilisé sur perte → probablement **acompte ou IS antérieur**, pas anomalie automatique

## Charte graphique MDC obligatoire pour tous les livrables Excel/Word
- Navy `#1A1A2E` (bandeaux, headers, totaux)
- Or `#E8C547` (accents, bordures, mentions)
- Format FCFA : `#,##0_- "FCFA";[RED]-#,##0_- "FCFA";"—"`
- Pied de page : MDC SARL | NCC 2506426B | RCCM CI-ABJ-03-2025-B13-10831

## Dossier client structuré
`/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/<NOM CLIENT>/EXERCICE_<ANNÉE>/`
- Scripts Python générateurs (`generate_*.py`)
- Livrables Excel (`LIASSE_*.xlsx`, `ETUDE_FISCALE_*.xlsx`)
- Modules d'import (`balance_*.py`)

**Why** : la méthodologie a été co-construite avec le client lors de la session BNA mai 2026, après plusieurs allers-retours où des erreurs initiales (raccourcissement n° comptes, omissions, bases juridiques fausses pour SARL, IMF mal calculé) ont été identifiées et corrigées. La règle d'exhaustivité absolue est non-négociable.

**How to apply** : dès qu'une balance arrive (PDF, Excel, image), déclencher le workflow complet sans demander d'autorisation. Si la source est un PDF avec écart de bouclage > 1 FCFA, exiger l'export Excel avant production de la liasse.

Voir [[skill-mdc-expert]] §§12.7, 13, 14, 15, 16, 17 pour le détail technique complet.
