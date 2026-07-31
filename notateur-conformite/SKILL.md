---
name: notateur-conformite
description: >
  NOTATEUR DE CONFORMITÉ — cœur de métier de MDC (La Maison de la Conformité SARL) en tant
  qu'AGENCE DE NOTATION ADMINISTRATIVE couvrant les volets comptable, fiscal et social.
  Recense les observations d'un dossier client, les code, les cote, les pondère par domaine
  et produit une NOTE DE CONFORMITÉ motivée (AAA → D) assortie d'un rapport d'observations
  et d'un plan de remédiation. Déclenche ce skill dès que l'utilisateur parle de : noter un
  client, note de conformité, notation, scoring, grille de notation, coter, quelle note on
  lui met, rapport d'observations, observations relevées, évaluer la conformité, niveau de
  conformité, qualité du suivi administratif, diagnostic de conformité, à quel point c'est
  mal tenu, rating client, dégrader ou relever la note, revoir la notation, restituer les
  anomalies au client. S'applique à TOUT dossier — audit global, mission de régularisation,
  revue de comptes — et constitue le livrable terminal de toute mission MDC.
---

# NOTATEUR DE CONFORMITÉ — Procédure de notation MDC

> MDC est une **agence de notation administrative**, pas un cabinet qui tient les comptes.
> Le produit fini d'une mission n'est pas un bilan : c'est une **note adossée à des observations
> sourcées, à une exposition chiffrée et à un plan de remédiation**.

Ce skill est le **livrable terminal** de toute mission. Il s'appuie sur les travaux produits
via `mdc-expert` (reconstitution, analyse bancaire, étude fiscale) et `auditeur-fiscal`
(contrôle adversarial), et les convertit en note.

---

## 1. LES SEPT DOMAINES ET LEUR PONDÉRATION

| Code | Domaine | Poids | Ce qu'il mesure |
|---|---|---|---|
| **A** | Trésorerie et suivi bancaire | 20 % | Exhaustivité des comptes, traçabilité des flux, rapprochements |
| **B** | Chiffre d'affaires et facturation | 20 % | Sincérité du CA, lien facturation-encaissement, créances |
| **C** | Obligations fiscales | 20 % | Régime applicable, déclarations, paiements, natures d'impôts |
| **D** | Paie et obligations sociales | 15 % | Masse salariale réelle, ITS, CNPS, déclarations |
| **E** | Comptabilité et bilan | 15 % | Justification de l'actif et du passif, coupure, amortissements |
| **F** | Séparation des patrimoines | 5 % | Frontière entité / dirigeant, comptes courants, distributions |
| **G** | Organisation documentaire | 5 % | Archivage, classement, disponibilité des pièces |

La pondération privilégie les trois domaines qui portent l'exposition financière (A, B, C = 60 %).
F et G pèsent peu **en note** mais leurs observations sont souvent les plus révélatrices en analyse
de causes (§6).

---

## 2. COTATION DES OBSERVATIONS

Trois niveaux, et trois seulement. Ne pas inventer d'échelon intermédiaire.

| Gravité | Malus | Critère de qualification |
|---|---|---|
| **CRITIQUE** | −5 | Remet en cause la sincérité des comptes, expose à un redressement majeur, ou révèle une perte de contrôle sur un flux financier |
| **MAJEUR** | −3 | Manquement à une obligation légale, ou absence d'un dispositif de contrôle indispensable |
| **MOYEN** | −1 | Défaut de forme, d'organisation ou de documentation sans incidence financière directe |

**Note d'un domaine** = max(0 ; 20 − somme des malus du domaine).
**Note globale** = somme pondérée des notes de domaine.

Le plancher à zéro est assumé : un domaine cumulant plus de quatre observations critiques
est hors de contrôle, et la note doit le dire.

---

## 3. GRILLE DE NOTATION

| Note /20 | Lettre | Qualification |
|---|---|---|
| ≥ 19 | **AAA** | Excellence |
| ≥ 17 | **AA** | Très satisfaisant |
| ≥ 15 | **A** | Satisfaisant |
| ≥ 13 | **BBB** | Acceptable |
| ≥ 9,5 | **BB** | Insuffisant |
| ≥ 7,5 | **B** | Médiocre |
| ≥ 4,5 | **CCC** | Critique |
| ≥ 2,5 | **CC** | Très critique |
| ≥ 0,5 | **C** | Pré-contentieux |
| < 0,5 | **D** | Défaut |

**Visa** : un visa de conformité n'est émis qu'à partir de **A**. En dessous, rapport de
non-conformité et plan de remédiation.

---

## 4. LE MOTEUR

```bash
python3 ~/.claude/skills/notateur-conformite/scripts/noter.py observations.json
```

Format d'entrée — un tableau JSON :

```json
[{"code":"A1","domaine":"A","gravite":"CRITIQUE",
  "constat":"Un seul compte communiqué alors que trois existent",
  "montant":30000000,"piece":"Relevé BICICI p.27","action":"Réclamer tous les relevés"}]
```

Le moteur ne juge pas : **il compte**. La qualification de gravité relève de l'analyste et doit
être défendable devant un contradicteur.

---

## 5. PROCÉDURE EN NEUF ÉTAPES

1. **Cadrer le périmètre** — exercices, pièces reçues, pièces manquantes. Toute limite de périmètre est écrite avant de commencer.
2. **Boucler les données** — aucune observation n'est formulée sur des chiffres qui ne bouclent pas. Relevés rapprochés aux totaux imprimés, Actif = Passif, Résultat CR = Résultat bilan.
3. **Relever les observations** domaine par domaine, en balayant le catalogue `reference/CATALOGUE_OBSERVATIONS.md`.
4. **Adosser chaque observation à une pièce** ou à un calcul reproductible. Une observation sans pièce est une hypothèse : elle se formule comme telle ou ne se formule pas.
5. **Coter** selon §2, en appliquant les critères et non l'impression.
6. **Faire contredire** — déployer `auditeur-fiscal` ou un agent indépendant pour challenger les cotations. Toute observation réfutée est retirée ou déclassée.
7. **Calculer la note** avec le moteur.
8. **Remonter aux causes** (§6) — c'est ce qui distingue un rapport de notation d'une liste d'anomalies.
9. **Produire les livrables** (§7) et, si la note ≥ A, émettre le visa.

---

## 6. L'ANALYSE DE CAUSES — l'étape qui fait la valeur

Une liste de trente anomalies n'apprend rien à un dirigeant. **Le regroupement en causes lui
montre ce qu'il doit changer.** Quatre familles de causes reviennent presque toujours :

1. **Rupture entre le flux et l'écriture** — l'encaissement est suivi quelque part, l'écriture ailleurs, rien ne les relie.
2. **L'espèce comme mode de gestion** — recettes et charges en numéraire, sans traçabilité du passage.
3. **Confusion entité / dirigeant** — flux personnels sur comptes sociaux, prélèvements non formalisés, comptes courants sans convention.
4. **Absence de contrôle externe effectif** — les anomalies relevées n'auraient pas survécu à une révision annuelle sérieuse.

Formuler systématiquement la **conséquence la plus coûteuse** dans une section isolée : c'est
elle que le dirigeant retiendra.

⚠ **Signaler aussi ce qui joue EN FAVEUR du client.** Une omission de produits peut avoir fait
déclarer des pertes fictives : le dire renforce la crédibilité du rapport et l'adhésion du client.

---

## 7. LIVRABLES

| # | Livrable | Référence | Contenu |
|---|---|---|---|
| 1 | **Rapport d'observations** | `MC-OBS-<SECTEUR>-<ANNÉE>-NNN` | Observations codées par domaine, récapitulatif, analyse de causes, mesures correctives |
| 2 | **Grille de notation** | onglet ou annexe | Note par domaine, pondération, note globale, lettre |
| 3 | **Plan de remédiation** | J+7 / J+15 / J+30 / J+60 | Action, responsable, pièce attendue, effet sur la note |
| 4 | **Visa ou rapport de non-conformité** | `MC-VISA-...` | Selon que la note atteint A ou non |

Tous les documents passent par les générateurs contrôlés (`publish_livrable_mdc.py`,
`publish_pdf_mdc.py`) : logo, filigrane confidentiel, zéro symbole Markdown résiduel.

---

## 8. RÈGLES ABSOLUES

1. **Aucune observation sans pièce.** Une intuition non documentée se formule en hypothèse à vérifier, jamais en constat.
2. **Aucune notation sans bouclage préalable.** Noter des comptes qui ne bouclent pas revient à noter du bruit.
3. **Aucune qualification juridique définitive** — l'Agence observe, chiffre et demande ; elle ne requalifie pas à la place de l'administration.
4. **Toujours ouvrir le contradictoire** : le rapport invite la Direction à répondre, et ses explications sont versées au dossier.
5. **Toujours écrire les limites de périmètre** — comptes non communiqués, exercices non couverts, pièces manquantes.
6. **Ne jamais durcir le ton au-delà de ce que les pièces établissent.** La fermeté vient des chiffres, pas des adjectifs.
7. **Réviser la note** dès que des pièces nouvelles arrivent : une note est datée et révisable.

---

## 9. CAS DE RÉFÉRENCE — COLLÈGE SAINT-EXUPÉRY (juillet 2026)

Premier déploiement complet de la procédure. 36 observations, 14 critiques.

| Domaine | Crit. | Maj. | Moy. | Note /20 | Pondéré |
|---|---|---|---|---|---|
| A — Trésorerie | 5 | 3 | 1 | 0 | 0,00 |
| B — Chiffre d'affaires | 2 | 3 | 1 | 0 | 0,00 |
| C — Fiscal | 2 | 2 | 0 | 4 | 0,80 |
| D — Social | 2 | 1 | 0 | 7 | 1,05 |
| E — Comptabilité | 2 | 4 | 1 | 0 | 0,00 |
| F — Patrimoines | 1 | 3 | 0 | 6 | 0,30 |
| G — Documentaire | 0 | 1 | 2 | 15 | 0,75 |
| **GLOBAL** | **14** | **17** | **5** | | **2,90 → CC** |

Enseignements capitalisés :
- Un produit omis (versements de l'État pour élèves affectés) peut inverser la lecture entière d'un dossier : pertes chroniques devenues bénéfices.
- La contrepartie d'une réserve doit être **cherchée à l'actif** avant toute ingénierie sur le passif.
- Une trésorerie figurant au bilan sans relevé bancaire n'est pas un actif vérifié.
- Toujours vérifier qu'un compte bancaire ou un dépôt à terme aperçu dans les relevés figure bien au bilan.

Dossier : `Documents/DOSSIER CLIENTS/COLLEGE ST EXUPERY 2/`.

---

## 10. CAPITALISATION

Chaque mission enrichit `reference/CATALOGUE_OBSERVATIONS.md` : toute observation nouvelle y est
ajoutée avec son code, son domaine, sa gravité type et l'indice qui permet de la détecter.
Le catalogue est la mémoire de l'Agence ; il rend la notation reproductible d'un dossier à l'autre.
