---
name: checklist-audit-suivi-mdc-v2
description: "Les 4 documents de procédure MDC — checklist audit, checklist suivi, manuel audit, manuel suivi — TOUS séparés par parcours depuis le 23/09/2026. Où ils sont rangés et ce qu'ils couvrent. À utiliser si l'utilisateur les cherche encore ou demande une V3."
metadata:
  node_type: memory
  type: reference
  originSessionId: 82cefd56-2789-4448-990e-31cf0f64703a
  modified: 2026-09-23T18:01:38.305Z
---

**Règle définitive (consigne expresse de l'utilisateur, 23/09/2026) : un document par parcours, jamais un document fusionné audit+suivi.** Appliquée deux fois le même jour : d'abord au manuel (« sépare le manuel en fonction de l'audit ou du suivi »), puis à la checklist (« fais pareil pour la checklist, sépare-la aussi en deux fichiers »). Ne plus jamais recréer une version fusionnée « audit et suivi » d'un même document — même avec des onglets/chapitres distincts à l'intérieur, l'utilisateur veut des FICHIERS séparés.

**Les 4 documents actuels :**
1. **CHECKLIST_AUDIT_MDC_V2.xlsx** (+ .pdf, réf. MC-CHK-AUDIT-2026-002) — 3 onglets : Checklist Audit (49 étapes/9 phases) · Les 5 règles · Points de blocage (9 phases + 1 transversal qualité).
2. **CHECKLIST_SUIVI_MDC.xlsx** (+ .pdf, réf. MC-CHK-SUIVI-2026-001, NOUVEAU fichier) — 2 onglets : Checklist Suivi (21 étapes/7 phases) · Points de blocage (6 étapes, spécifique suivi). Renvoie à l'onglet « Les 5 règles » du fichier Audit pour les principes de fond communs, ne les duplique pas.
3. **MANUEL_PROCEDURE_AUDIT_MDC_V2.docx** (+ .pdf, réf. MC-MAN-AUDIT-2026-003) — audit seul, 8 phases (0 à 8) + table des livrables par phase.
4. **MANUEL_PROCEDURE_SUIVI_MDC.docx** (+ .pdf, réf. MC-MAN-SUIVI-2026-001, NOUVEAU document) — suivi seul, **8 étapes numérotées du début à la fin**, chacune avec Qui / Livrables / Bloquant précisés dans le texte, + table récap « Les livrables, par étape » + table « Points de blocage ». Renvoie au manuel audit pour les 5 règles, ne les duplique pas.

**Exigence de forme sur tout document de procédure MDC (audit ou suivi), retenue pour l'avenir :**
- Un déroulé d'**étapes numérotées du début à la fin** (jamais de simples sections thématiques non numérotées).
- Une **table de synthèse des livrables par étape**.
- Une **table des points de blocage** propre au document (pas seulement des mentions éparses dans le texte).
- Renvoyer vers le document audit pour la doctrine commune (5 règles, principes de fond) plutôt que la dupliquer dans le document suivi.

**Emplacements** (house rule [[copie-systematique-base-documentaire]]) — les 4 documents, mêmes 3 emplacements :
- Source de référence : `~/Documents/ARCHIVES DOCUMENTS/LIVRABLES AUDIT LMDC/00_MANUELS_PROCEDURES/`. Sources markdown des manuels : `_SOURCES_MD/manuel_audit.md` et `_SOURCES_MD/manuel_suivi.md`. Générateur de la checklist : script scratchpad de session (à recréer si besoin, ou éditer le xlsx directement en respectant le style : bandeau 1F3864/or C9A227/crème FFFBE8, lignes bloquantes en rouge C0392B).
- `~/Documents/BASE DOCUMENTAIRE LMDC/06_PROCEDURES/` (les 4).
- `~/Documents/ARCHIVES DOCUMENTS/MACHINE LMDC/0_PROCEDURE/` (les 2 checklists seulement — les manuels ne sont volontairement pas dans le cockpit, qui ne garde que l'essentiel cochable ; `00_LISEZ-MOI.md` y référence les deux checklists).

**Doctrine commune ajoutée par rapport aux V1 d'origine** (identique dans les 4 documents) : triangles de cohérence (CA / masse salariale / trésorerie), demande DFE + export Sage dès le cadrage, contrôle juridique (baux/PV), kit de détection terrain obligatoire à compter du 28/09/2026, confrontation aux pièces avant toute conclusion « non fait » et revue de cohérence inter-livrables (post-incident Saint-Exupéry), passage obligatoire par la rédaction avant remise.

**Contenu de fond ajouté (23/09/2026, retour de l'utilisateur : « ça ne me dit pas bien »)** — le manuel/la checklist audit devaient être plus EXPLICITES sur ce que l'équipe recherche concrètement, pas seulement dérouler des phases procédurales. Ajouté dans les deux (manuel chap. 1 + phases 2-4, checklist items 2.7-2.8/3.5/4.6) :
- Confrontation nommée **état de synthèse du RÉEL ↔ état de synthèse du DÉCLARATIF** (pas juste « comparer »).
- **Droits de timbre** explicitement dans la matrice des natures (absents des relevés bancaires, oubliés sinon).
- **Traçabilité des dépenses** (chaque décaissement → une pièce) et **consignation des pièces** (l'entreprise les conserve-t-elle ?) comme vérifications à part entière, pas sous-entendues.
- **Actes anormaux de gestion** et **réintégrations potentielles** (renvoi au skill [[reintegrations-deductions]] pour le chiffrage) — absent à 100 % de la première version, c'est le manque le plus net signalé par l'utilisateur.
Réflexe à garder : un manuel MDC doit toujours nommer explicitement ces éléments de fond fiscal (déclaratif/réel, timbre, AAG/réintégration, traçabilité, consignation), pas seulement décrire une procédure en phases.

**Même enrichissement appliqué au SUIVI** (demande de suite immédiate de l'utilisateur, même jour) — adapté au rythme MENSUEL plutôt qu'à la reconstruction ponctuelle de l'audit : état de synthèse du réel/déclaratif **du mois**, droits de timbre dans la grille mensuelle, traçabilité des dépenses **du mois**, consignation des pièces **du mois**, actes anormaux de gestion/réintégrations signalés **chaque mois** (pour ne pas laisser le risque s'accumuler sur l'exercice — c'est l'argument de valeur du suivi). Checklist Suivi passée de 21 à 25 étapes. **Règle générale retenue : toute enrichissement de fond appliqué au document Audit doit être répercuté au document Suivi correspondant, reformulé au rythme mensuel — ne pas attendre que l'utilisateur le redemande séparément.**

**Piège corrigé en cours de route** : les tout premiers jets citaient littéralement « J+7 → J+60 » / « J+X » pour ILLUSTRER l'interdiction — repéré en revue et corrigé partout. Voir [[preferences-livrables]] : la règle proscrit la chaîne elle-même, pas seulement son usage comme échéancier réel.

**Référencée dans** : skill `mdc-expert` §35 (point d'entrée de toute mission — les 4 réfs y sont à jour). Voir aussi [[machine-lmdc-procedure]], [[kit-livrables-audit-mdc]], [[standard-qualite-travail-pro]], [[fix-xlsx-to-pdf-mdc-wrap]].

**How to apply :** si l'utilisateur redemande l'un de ces documents, ils sont là — pas besoin de les refaire. Toute nouvelle amélioration de doctrine doit produire une V3 des 4 documents en parallèle (jamais un seul), chacun restant un FICHIER séparé par parcours, sans écraser les versions précédentes, en suivant le même `REGISTRE_VERSIONS.txt`. Régénérer les manuels via `publish_livrable_mdc.py` / `publish_pdf_mdc.py`, les checklists via `xlsx_to_pdf_mdc.py` — jamais en éditant un docx/pdf à la main.
