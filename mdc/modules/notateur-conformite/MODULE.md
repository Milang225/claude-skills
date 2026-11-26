---
name: notateur-conformite
description: >
  INDICE MDC DE CONFORMITÉ — cœur de métier de MDC (La Maison de la Conformité SARL), cabinet de
  conseil en conformité fiscale et sociale. Évalue les 45 contrôles fixes de la méthode publiée,
  calcule l'INDICE MDC SUR 100 (Maîtrisé, Satisfaisant, Fragile, Exposé, Critique), l'EXPOSITION
  ESTIMÉE en FCFA (bas / central / haut, avec position de défense) et décide de l'ATTESTATION DE
  DIAGNOSTIC ; produit la synthèse du rapport de diagnostic et le plan de remédiation. Déclenche ce
  skill dès que l'utilisateur parle de : Indice MDC, diagnostic de conformité, contrôle à blanc,
  noter un client, note de conformité, notation, scoring, grille, coter, quelle note on lui met,
  rapport d'observations, observations relevées, évaluer la conformité, niveau de conformité,
  exposition, position de défense, régulariser ou défendre, attestation de diagnostic, revoir ou
  recalculer l'Indice, re-diagnostic. Le vocabulaire « notation / AAA à D / visa » est abrogé :
  le skill répond toujours en Indice, niveau et attestation. S'applique à tout Diagnostic,
  re-diagnostic de clôture, Suivi (Indice actualisé) et préparation d'une Défense contrôle.
---

# INDICE MDC DE CONFORMITÉ — procédure d'évaluation

> **Source de vérité unique :** la Méthode de l'Indice MDC, version 1.0, en vigueur du 1er novembre 2026 au 31 octobre 2027.
> - Document : `/Users/bilefilsseverin/LA CONFORMITE LMDC/02_METHODE_INDICE_MDC.md`
> - Référentiel : `scripts/referentiel_mdc_v1.json`
> - Moteur : `scripts/indice_mdc.py`
>
> En cas de doute, le référentiel fait foi. L'ancienne grille AAA à D sur 7 domaines (A à G), `noter_ancien_abroge.py` et `SKILL.md.ancien-abroge-2026-10-11` sont **abrogés**.

## 1. Ce que l'Indice mesure

L'Indice mesure le respect des **obligations** fiscales, sociales et comptables d'une entreprise, sur une période donnée, à partir de **45 contrôles fixes**, chacun adossé à une pièce.

Il ne constitue **pas** :
- une notation financière (AMF-UMOA) ;
- un audit ou une certification des comptes ;
- une vérification ou une appréciation de la comptabilité (réservée à l'expert-comptable inscrit) ;
- une consultation juridique.

## 2. Six domaines

| Code | Domaine | Poids |
|---|---|---:|
| T | Trésorerie et flux | 20 % |
| V | Chiffre d'affaires et facturation | 15 % |
| F | Obligations fiscales | 25 % |
| S | Obligations sociales et paie | 20 % |
| C | Obligations comptables et légales (faits seulement : existence, arrêté, visa ou certification, approbation, dépôt, CAC) | 15 % |
| G | Gouvernance et documentation | 5 % |

## 3. Évaluer, puis calculer

1. **Statut de chaque contrôle :**
   - C = 1 ;
   - P = 0,5 ;
   - NC = 0 ;
   - NV (pièce non produite) = 0, et le contrôle sort de la couverture ;
   - NA (motivé) = exclu.
2. **Gravité, fixée par le référentiel :** critique 5, majeur 3, mineur 1.
3. **Score d'un domaine** = 100 × Σ(gravité × valeur) ÷ Σ(gravité applicable). Il est plafonné à 50 si un contrôle critique du domaine est NC.
4. **Indice** = Σ(score × poids).
5. **Couverture :**
   - 80 % ou plus : Indice définitif ;
   - de 50 à 80 % : Indice provisoire ;
   - moins de 50 % : aucun Indice émis.
6. **Niveaux :** Maîtrisé ≥ 85 · Satisfaisant ≥ 70 · Fragile ≥ 55 · Exposé ≥ 40 · Critique.
7. **Règle du maillon critique :**
   - 1 ou 2 contrôles critiques NC : niveau plafonné à Fragile ;
   - 3 ou plus : niveau plafonné à Exposé.
8. **Pour chaque contrôle P, NC ou NV :**
   - un constat et une pièce ;
   - une exposition chiffrée en trois scénarios. Bas = droits + intérêts : c'est le coût d'une régularisation spontanée (LPF art. 24). Central = avec majoration au taux du seuil du quart (art. 162). Haut = avec majoration maximale (art. 162 et 163) ;
   - une **position de défense** (FORTE / DISCUTABLE / FAIBLE) et une **stratégie** (REGULARISER / DOCUMENTER / DEFENDRE).
9. **Attestation de diagnostic** : seulement si l'Indice est définitif, ≥ 70, et sans aucun contrôle critique NC. Elle est valable 12 mois.

```bash
python3 ~/.claude/skills/notateur-conformite/scripts/indice_mdc.py modele CLIENT/evaluation.json --client "NOM" --reference MDC-AAAA-NNN
```

```bash
python3 ~/.claude/skills/notateur-conformite/scripts/indice_mdc.py calculer CLIENT/evaluation.json --md CLIENT/synthese.md
```

Le moteur **refuse** une feuille dans les cas suivants : un contrôle manquant, un P ou NC sans pièce, une position de défense ou une stratégie absente, une version de méthode différente.

## 4. Règles absolues

1. **Aucun statut P ou NC sans pièce.** Une intuition se formule en question dans la demande d'explication, jamais en constat.
2. **Cohérence des sources avant évaluation**, mais **jamais de retraitement de la comptabilité du client**. Une incohérence comptable est orientée vers l'expert-comptable.
3. **Double regard sur tout NC critique** avant le projet de rapport.
4. **Contradictoire** : le client a 8 jours ouvrés pour répondre ; l'Indice est recalculé si besoin.
5. **Toujours écrire les limites de périmètre** (pièces non produites, exercices non couverts).
6. **Mentionner ce qui joue en faveur du client.**
7. **Plusieurs exercices = un seul Indice.** Pour chaque contrôle, on retient la situation la plus défavorable, et l'exercice concerné est étiqueté dans le constat.
8. **Le rapport parle comme un document d'entreprise.** Aucun nom de fichier, aucune commande, aucun schéma de terminal (charte 2026, règle 5).

## 5. Livrables

| Livrable | Contenu |
|---|---|
| Rapport de diagnostic | Page 1 : Indice, niveau, exposition en trois parts, 3 priorités, éléments favorables. Puis : limites, méthode, résultats par domaine, observations, causes, réponses de la direction |
| Plan de remédiation | Action, contrôle visé, échéance (J+7 / J+30 / J+60 / J+90), responsable (MDC, client, expert-comptable ou avocat partenaire), pièce attendue, gain de points |
| Attestation de diagnostic | Si les trois conditions sont remplies |

Modèles : `/Users/bilefilsseverin/LA CONFORMITE LMDC/modeles/`. Mise en forme : skill `redaction`, avec contrôle qualité bloquant.

## 6. Analyse des causes (toujours conservée)

Regrouper les observations en causes, c'est ce qui rend le rapport utile au dirigeant :
1. rupture entre le flux et l'écriture ;
2. l'espèce comme mode de gestion ;
3. confusion entre l'entité et le dirigeant ;
4. absence de contrôle externe effectif.

Isoler **la conséquence la plus coûteuse** dans un encadré.

## 7. Historique

Les missions antérieures au 1er novembre 2026 ont été notées avec l'ancienne grille AAA à D (par exemple Collège Saint-Exupéry : CC 2,90/20 ; LERO consolidé : CCC 5,80/20). Ces notes ne se comparent pas à l'Indice : il faut recalculer selon la méthode v1.0 lors d'un re-diagnostic. Le catalogue `reference/CATALOGUE_OBSERVATIONS.md` reste une aide au repérage des indices de détection ; les codes officiels sont désormais ceux du référentiel (T01 à G05).
