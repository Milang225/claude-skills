---
name: revision-comptes
description: >
  Chargé de la RÉVISION DES COMPTES de MDC : à partir de la balance, du grand livre ou du journal d'un client
  (SYSCOHADA révisé, Côte d'Ivoire), contrôle la régularité des écritures et la sincérité des états de synthèse,
  justifie chaque solde cycle par cycle (trésorerie, ventes-clients, achats-fournisseurs, personnel, État,
  immobilisations, stocks, capitaux propres et emprunts, débiteurs-créditeurs divers), rédige les écritures de
  régularisation (REG-01…) et produit le rapport de révision des comptes avec sa note de conformité comptable.
  Déclenche dès que l'utilisateur demande de réviser des comptes, faire la révision comptable d'un exercice ou
  d'une situation intermédiaire, justifier les soldes, contrôler une balance, « est-ce que les comptes tiennent »,
  préparer la clôture, ou produire un REVISION_<CLIENT>_<EXERCICE>.
---

# Révision des comptes — MDC

**Rôle.** Dire si les comptes d'un client sont réguliers et sincères, et ce qu'il faut corriger pour qu'ils le
soient. Le réviseur part de la balance, remonte au grand livre puis à la pièce, et justifie chaque solde. Un solde
qu'on ne peut pas justifier par une pièce est une réserve, jamais un chiffre à arranger.

**Différence avec les modules voisins.**
- `revision-comptes` révise **les comptes d'un client** (balance reçue ou tenue par l'agence) : justification des soldes, régularisations, rapport.
- `ecritures-sans-faute` contrôle **les écritures que l'agence produit** avant remise (règles R1 à R20, `controle_ecritures.py`).
- `auditeur-comptable` est **le second regard indépendant** sur ce travail avant remise.
- `auditeur-superieur` pilote une mission d'audit global, dont la révision n'est qu'un volet.
- Le skill `revision` fait le point sur l'état des dossiers. Il ne révise pas de comptes.

**Place dans la chaîne.** collecte des pièces → **`revision-comptes`** → écritures de régularisation contrôlées
par `ecritures-sans-faute` → `auditeur-comptable` → `redaction` / `producteur-livrables` → remise.

**Charte 2026.** L'agence ne certifie rien et n'émet aucun visa (ord. 2009-387, art. 70). Jamais « Visé et
certifié conforme », jamais « Réviseur de comptes » comme titre, jamais de note AAA à D. Le résultat s'écrit
**Validé / Validé avec réserves / Refusé**. Signature : « Révision des comptes — La Maison de la Conformité SARL ».

---

## 1. Avant de commencer

1. Lire le dossier `~/Documents/DOSSIER CLIENTS/<CLIENT>` : statuts, forme, régime effectif (avis d'imposition), exercice, dernière balance, notes de revue passées.
2. Réunir les pièces. Sans elles, la révision s'arrête au constat :

| Pièce | Pour quoi |
|---|---|
| Balance N **à 6 colonnes** (mouvements et soldes) | Base de la révision. Une balance à 4 colonnes (soldes seuls) ne suffit pas : l'exiger avec mouvements |
| Balance ou bilan N-1 | À-nouveaux, intangibilité du bilan d'ouverture |
| Grand livre ou journal | Remonter de la balance à l'écriture |
| Relevés bancaires de toute la période + relevé au dernier jour | Triangle banque, rapprochement |
| Brouillard / PV de caisse | Triangle caisse |
| Inventaire des stocks signé | Stocks et CMV |
| État des immobilisations, factures d'acquisition | Immobilisations et amortissements |
| Déclarations fiscales et quittances (TVA, ITS, patente, IMF/BIC, TEE) | Cycle État |
| Livre de paie, déclarations CNPS | Cycle personnel |
| Contrats d'emprunt, tableaux d'amortissement (document du prêteur) | Emprunts |
| PV d'AGO (affectation du résultat), statuts à jour | Capitaux propres |

3. Lister les pièces manquantes dans un tableau « pièces à réclamer » (module `points-a-eclaircir` pour la DEE). Ne pas compenser une pièce absente par une estimation.

---

## 2. Contrôles mécaniques (toujours en premier, bloquants)

| # | Contrôle | Bloquant si |
|---|---|---|
| M1 | Σ mouvements débit = Σ mouvements crédit de la balance | écart > 0 |
| M2 | Chaque pièce équilibrée (si journal fourni) | une pièce déséquilibrée |
| M3 | À-nouveaux N = bilan de clôture N-1 (intangibilité) | écart non expliqué |
| M4 | Résultat du compte de résultat = résultat du bilan (classe 13) | écart |
| M5 | Actif = passif | écart |
| M6 | Sens normal des soldes (caisse et banque débitrices, fournisseurs créditeurs, charges débitrices, produits créditeurs) | caisse créditrice, compte de passif débiteur non expliqué |
| M7 | Comptes utilisés présents dans le plan SYSCOHADA révisé (AUDCIF) | compte inexistant |
| M8 | Aucune trésorerie (5x) passée directement contre une charge ou un produit (6/7) sans tiers, quand l'agence tient la comptabilité | écriture directe |

Outils :

```bash
E=~/.claude/skills/mdc/modules/ecritures-sans-faute/scripts/controle_ecritures.py
A=~/.claude/skills/mdc/modules/auditeur-comptable/scripts/audit_comptable.py
python3 $A ecritures JOURNAL.xlsx --exercice 2025 --forme SARL --regime RSI --n1 BALANCE_N-1.xlsx --rapport CONTROLE.md
```

Plan comptable : `modules/mdc-expert/reference/PLAN_COMPTABLE_OHADA_COMPLET.md`. Tests T1 à T16 de la balance :
`modules/mdc-expert/MODULE.md` §12.5.

---

## 3. Révision par cycle

Pour chaque cycle : **solde à justifier → pièce qui le justifie → constat → régularisation éventuelle**.

| Cycle | Comptes | Ce qu'on vérifie |
|---|---|---|
| Trésorerie | 52, 53, 57, 58 | Solde banque = relevé au dernier jour (sinon rapprochement bancaire écrit). Triangle banque : SI + encaissements − décaissements = SF. Caisse jamais négative ; triangle caisse. 585/588 soldés au 31/12. Aucun mouvement bancaire sans relevé |
| Ventes – clients | 70, 411, 416, 419, 4431 | CA comptabilisé ≈ encaissements + variation des créances. TVA facturée cohérente avec le CA taxable. Créances anciennes : relance ou dépréciation (416 / 491). Soldes clients créditeurs expliqués |
| Achats – fournisseurs | 60, 61, 62, 63, 401, 408, 4452 | Factures rattachées à l'exercice (408 / 476 si nécessaire). TVA récupérée sur factures conformes. Retenues à la source (AIRSI, PPSSI) passées. Soldes fournisseurs débiteurs expliqués |
| Stocks | 31 à 38, 39, 603 | Stock final = inventaire signé. Triangle CMV : SI + achats − SF ; marge brute plausible pour le secteur. Jamais de stock alimenté par la caisse ou la banque |
| Immobilisations | 2x, 28x, 29x, 681, 81, 82 | Chaque immobilisation a sa facture. Dotation 681 = variation des 28 + amortissements des biens sortis. Pas de dotation sur un bien totalement amorti. Cessions passées en 81/82 |
| Personnel | 66, 42, 43, 4472, 641x | Salaires du livre de paie = 661. Charges patronales et ITS cohérents avec la paie (taux dans `fiscalite-ci`). CNPS : aucune écriture sans instruction du Gérant ; une paie sans CNPS se signale. Congés payés et indemnités de fin de carrière provisionnés |
| État | 44x, 64x, 89x | Chaque impôt : charge à l'émission, paiement à la quittance. Dû comptable = dû déclaré. Patente, TEE ou IMF/BIC selon le régime effectif. Comptes d'État de sens inversé reclassés (4492) |
| Capitaux propres – emprunts | 10, 11, 12, 13, 16, 46 | Capital = statuts ; capital libéré (109, 4611 à 4613 soldés). Résultat N-1 affecté par AGO. Réserve légale dotée. Capitaux propres < 50 % du capital : alerte AUSCGIE. Emprunts = tableau du prêteur ; comptes courants d'associés documentés |
| Débiteurs et créditeurs divers | 47 | 471 et 475 justifiés ou apurés à la clôture (le plan révisé n'a pas de 470). 476 à 479 normaux à la clôture : ne pas les traiter en anomalie |

Schémas d'écriture justes : `modules/ecritures-sans-faute/MODULE.md` §3. Cas déjà traités : GLOBE (§36 de
`mdc-expert`), FAMILLE KRA (stocks), BUILDING NEW AFRICA (§14).

---

## 4. Revue analytique

Comparer N et N-1, et les ratios au secteur : marge brute, charges de personnel / CA, loyers / CA, impôts et
taxes / CA, délais clients et fournisseurs, trésorerie. Toute variation forte sans explication devient une
question au client, pas une conclusion. Détail des ratios : module `diagnostic-financier`.

---

## 5. Régularisations

Format habituel :

```
REG-01 (description courte)
Base : <article AUDCIF / CGI / pièce>
D xxxx  Compte              montant FCFA
   C yyyy  Compte                  montant FCFA
Impact résultat : +/- montant
Impact bilan    : +/- montant
```

Catalogue des régularisations courantes : `modules/mdc-expert/MODULE.md` §14.2, étape 5. Chaque écriture de
régularisation passe ensuite par `ecritures-sans-faute` (script à zéro erreur). Aucun chiffre inventé, aucune
écriture d'équilibrage vers une trésorerie estimée.

---

## 6. Le rapport de révision des comptes

Fichier : `REVISION_<CLIENT>_<EXERCICE>` (Word et PDF), dans
`~/Documents/DOSSIER CLIENTS/<CLIENT>/Audit & Révision/`. Référence : `MC-REVCPT-<SIGLE>-<ANNÉE>-<N°>`.

Plan, repris des révisions déjà faites (GLOBE, MABEK, KF IMMOBILIER, TIM 7, FAMILLE KRA) :

1. **En-tête** : client, NCC, forme, régime, activité, exercice ou période (préciser « situation intermédiaire » le cas échéant), référentiel SYSCOHADA révisé / AUDCIF.
2. **Synthèse** : chiffre d'affaires, charges, résultat, trésorerie, dettes, et le résultat de la révision en une phrase.
3. **Contrôles mécaniques** (§2) : tableau contrôle / résultat chiffré.
4. **Plan comptable** : comptes utilisés, conformité, anomalies d'imputation.
5. **Revue des schémas d'écritures** : un échantillon par nature d'opération, schéma constaté, conformité.
6. **Révision par cycle** (§3) : solde, justification, constat.
7. **Revue analytique** (§4).
8. **Réserves** : numérotées R1, R2… ; chacune dit le fait, la base, l'impact chiffré et ce qui la lèvera. Une réserve levée reste affichée, marquée « levée », avec la pièce qui l'a levée.
9. **Écritures de régularisation** (§5) et leur impact sur le résultat et le bilan.
10. **Note de conformité comptable** : régularité des écritures, sincérité des états, exhaustivité et rattachement → **Validé / Validé avec réserves / Refusé**.
11. **Recommandations** et pièces à fournir.

Règles de rédaction : module `redaction` (sobre, formel, sans encadré coloré ni style IA, « l'agence »). Aucun
délai ni échéance dans le document client sauf demande du Gérant. Jamais « gratuit ». Tout en FCFA.

Refus obligatoire si : balance déséquilibrée, résultat du bilan différent de celui du compte de résultat, ou
à-nouveaux différents du bilan N-1 sans explication.

---

## 7. Avant remise

1. `auditeur-comptable` (agent indépendant, sans lui donner les conclusions) sur les régularisations.
2. Contrôle de cohérence du dossier : `mdc-expert` §34 (`controle_coherence_dossier.py`) — aucun livrable ne doit porter un ancien chiffre.
3. `redaction` puis `producteur-livrables` pour le PDF et le Word brandés ; `marquer_livrable` sur la plateforme.
4. Mail d'accompagnement en brouillon seulement (`preparation-mails`).
