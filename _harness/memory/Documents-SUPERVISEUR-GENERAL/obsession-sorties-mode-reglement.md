---
name: obsession-sorties-mode-reglement
description: "Doctrine de l'Agence — les sorties de fonds, leur justification et leur mode de règlement sont la priorité absolue ; vigilance maximale sur les débours des transitaires"
metadata:
  node_type: memory
  type: feedback
  originSessionId: eda557a3-e61f-4bda-b376-a80f79efd4ae
  modified: 2026-09-30T20:55:23.558Z
---

Pour l'Agence (MDC), **les sorties, la manière dont elles sont faites et leur mode de règlement sont une obsession** : chaque analyse de dossier commence par elles, et chaque livrable doit le dire explicitement. Pour les commissionnaires en douane et transitaires, les **débours** exigent une documentation spécifique (mandat / ordre de transit, pièce au nom du client, note de débours distincte de la facture, reddition) pour ne jamais être pris pour du chiffre d'affaires.

**Why:** consigne du gérant (dossier AVE MARIA, 30/09/2026). Les sorties non justifiées sont réintégrées (CGI 18, 18 bis : espèces > 250 000) ou requalifiées en revenus distribués (CGI 180-1 : sommes mises à disposition des associés) ; les débours mal documentés deviennent du CA.

**How to apply:** dans toute mission, classer chaque sortie (nature, pièce, mode de règlement, bénéficiaire, risque) ; imputer les sorties vers associés sur un compte courant créditeur conventionné ; fixer la commission des transitaires au prix de pleine concurrence (CGI 38). Manuel de référence : MC-MAN-BP-2026-001 et manuel de procédures MC-MAN-PROC-AM-2026-001 (dossier AVE MARIA). Voir [[dossier-ave-maria-ecomaf]].

Consigne du gérant du 30/09/2026 : prêter une attention particulière aux sorties et **vérifier les bons de caisse** dans chaque dossier. Si l'entreprise n'a pas de bons de caisse, il faut en créer et instaurer une politique. Pour cela, un kit standard existe dans `SUPERVISEUR GENERAL/GUIDES_COLLABORATEURS/KIT_BONS_DE_CAISSE` :
- la politique MC-POL-CAISSE-2026-001, à faire signer par le gérant du client ;
- un modèle de bon prénuméroté ;
- un registre Excel avec contrôles (numérotation, signatures, pièce, espèces > 250 000, avances à régulariser sous 48 h).

Chaque analyse des sorties précise le mode de règlement et le risque de réintégration et/ou de non-déductibilité (vocabulaire exigé par le gérant).

Le 01/10/2026, l'obsession a été intégrée à l'écosystème de doctrine (`SUPERVISEUR GENERAL/ECOSYSTEME_SYSTEME_COMPTABLE`, copies identiques dans `ECOSYSTEME_SYSTEME_COMPTABLE_1` et dans `BASE DOCUMENTAIRE LMDC/06_PROCEDURES/KIT_SYSTEME_COMPTABLE`) :
- **Référentiel MC-REF-SYSCO-2026-001 :** nouvelle section 2 bis « L'obsession MDC : les sorties et les charges » (règle des cinq questions, six règles, contrôle mensuel de 100 % des sorties).
- **Tableau de bord de contrôle permanent :** lignes S1/S2 dans l'onglet Contrôles et nouvel onglet « Sorties ». Il est généré par `_SOURCES/build_outils.py`.
- **Choix de cohérence :** on garde les « douze contrôles » et les « huit signes » sans renuméroter, car ils sont cités dans tout l'écosystème. Le contrôle des sorties s'y ajoute à part.
