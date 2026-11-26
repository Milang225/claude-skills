---
name: auditeur-comptable
description: >
  Auditeur comptable INDÉPENDANT de MDC : relit, après le comptable et avant toute remise, un journal,
  un ordre de saisie Sage, une comptabilité régularisée, des à-nouveaux ou une balance, sur trois axes :
  (A) les écritures sont justes (comptes AUDCIF, schémas, paie, stocks, tiers, dates) ; (B) les principes
  comptables SYSCOHADA révisé sont respectés (intangibilité du bilan d'ouverture, indépendance des exercices,
  non-compensation, prudence, continuité d'exploitation, régularité et sincérité, coût historique, permanence
  des méthodes) ; (C) les mises à jour sont faites (dernière version du dossier, script à jour des notes de
  revue, taux en vigueur, catalogue des notes de revue, listes d'opérations intégrées). Déclenche dès que
  l'utilisateur demande de vérifier, auditer, contrôler, relire, valider des écritures ou une comptabilité,
  « est-ce que les écritures sont bonnes », « les principes sont-ils respectés », « tout est à jour ? »,
  et automatiquement après le module ecritures-sans-faute, avant de produire le PDF, l'Excel ou la liasse.
---

# Auditeur comptable MDC

**Rôle.** Contrôler, pas refaire. L'auditeur part du principe que le travail contient des fautes et cherche
à les trouver : il recalcule, il rapproche, il remonte à la pièce. Il ne corrige rien lui-même ; il rend un
rapport (points bloquants, réserves, vérifié) et le comptable corrige. Un chiffre qu'on ne peut pas
reproduire depuis la pièce est une observation.

**Indépendance.** Pour une relecture réellement indépendante, lancer l'agent `auditeur-comptable`
(`~/.claude/agents/auditeur-comptable.md`) **sans lui donner les conclusions du comptable** : seulement le
fichier, le client, l'exercice, la forme et le régime. Il ne voit pas comment les écritures ont été
construites et n'est donc pas ancré sur elles.

**Place dans la chaîne.** `ecritures-sans-faute` (le comptable se contrôle) → **`auditeur-comptable`**
(un second regard) → `redaction` / `producteur-livrables` (mise en forme) → remise.

---

## 1. Lancer l'auditeur

```bash
A=~/.claude/skills/mdc/modules/auditeur-comptable/scripts/audit_comptable.py
python3 $A tout JOURNAL.xlsx --exercice 2025 --forme SARL --regime RSI --n1 BILAN_2024.xlsx --rapport AUDIT.md
python3 $A ecritures JOURNAL.xlsx --exercice 2025 --forme EI --regime TEE      # axes A et B seulement
python3 $A mises-a-jour                                                        # axe C, skill seul
```
Options : `--feuille` (feuille Excel du journal, détectée sinon), `--n1` (balance ou bilan N-1 visé :
colonnes compte + solde, ou débit / crédit), `--regularisations` (fichier d'écritures correctives seules).
Code retour 1 tant qu'il reste un point bloquant. Le rapport est un document **interne** : il ne part
jamais tel quel au client (vocabulaire de la charte : « observations », « diagnostic »).

## 2. Axe A — les écritures sont-elles bonnes ?

Le script reprend intégralement `controle_ecritures.py` (module ecritures-sans-faute) : comptes du plan
AUDCIF, table des confusions interdites, deux temps, écritures globales au 31/12, tiers nominatifs,
à-nouveaux, caisse créditrice, comptes d'attente, capital, forme juridique, régime (classe 89),
paie mois par mois, stocks.

L'auditeur ajoute **à la main**, par sondage (au moins 10 pièces, dont les 5 plus gros montants et
toutes les OD) :

| N° | Contrôle | Comment |
|---|---|---|
| A1 | Nature réelle | Ouvrir la pièce (facture, relevé, quittance) : le compte correspond-il à ce qui a été acheté, vendu, payé ? |
| A2 | Montant | Montant de l'écriture = montant de la pièce (HT/TTC, TVA déductible seulement sur FNE) |
| A3 | Date | Date de la pièce, pas la date de saisie ni le 31/12 |
| A4 | Tiers | Compte individuel au nom figurant sur la pièce |
| A5 | Paie et impôts | Une ligne par ligne de déclaration e-impôts ; paiement à la date de la quittance |
| A6 | Calcul | Recalculer : TVA 18 %, CN 1,2 %, TA 0,4 %, FPC 1,2 %, dotations au prorata de la mise en service |

## 3. Axe B — les principes comptables sont-ils respectés ?

| N° | Principe (SYSCOHADA révisé, AUDCIF et cadre conceptuel) | Ce que l'auditeur vérifie | Script |
|---|---|---|---|
| B1 | **Intangibilité du bilan d'ouverture** | À-nouveaux équilibrés, classes 1 à 5 seulement, égaux au bilan N-1 visé compte par compte. Seule exception : correction d'une erreur significative par le report à nouveau (ou le 103 en EI), mentionnée en note 2 | oui (avec `--n1`) |
| B2 | **Indépendance des exercices** (rattachement) | Aucune charge ni produit d'un autre exercice ; factures non parvenues (408), charges constatées d'avance (476), produits à recevoir (4181), intérêts courus (1662) passés à la clôture et extournés en N+1 | oui (signal) |
| B3 | **Non-compensation** | Aucun solde de sens contraire laissé dans un compte : fournisseur débiteur → 409, client créditeur → 419, banque créditrice → 565 ; pas de compensation client / fournisseur pour un même tiers ; pas d'actif net d'un passif | oui |
| B4 | **Prudence** | Amortissements passés (obligatoires même en perte) ; clients douteux en 416 et dépréciés en 491 (HT) ; stocks dépréciés si la valeur nette de réalisation est inférieure au coût ; provisions pour risques et litiges (191) ; aucun produit latent comptabilisé | oui (signal) |
| B5 | **Continuité d'exploitation** | Capitaux propres ≥ moitié du capital ; sinon consultation des associés dans les quatre mois de l'approbation des comptes et mention en note 2 ; capitaux propres négatifs = plan de redressement à documenter | oui |
| B6 | **Régularité et sincérité** (image fidèle) | Chaque ligne porte une pièce et un libellé précis (nature, tiers, période) ; pas de numéro de pièce réutilisé ; pas de « divers », « équilibre », « écart » ; la réalité prime sur l'apparence (mandat sans contrat = vente pour son compte) | oui |
| B7 | **Coût historique** | Entrées au coût d'acquisition (frais accessoires inclus, AIRSI exclu) ; réévaluation seulement légale ou documentée (106) | oui (signal) |
| B8 | **Permanence des méthodes** | Mêmes méthodes qu'en N-1 (stocks, amortissements, plan de comptes) ; tout changement justifié et expliqué en note annexe, effet sur le report à nouveau | manuel |
| B9 | **Importance significative** | Seuil de signification documenté avant de qualifier une erreur de « non significative » | manuel |

Les principes sans contrôle automatique se vérifient sur pièces et sur la liasse (notes 1 et 2).

## 4. Axe C — les mises à jour sont-elles faites ?

| N° | Contrôle | Pourquoi |
|---|---|---|
| C1 | Le fichier contrôlé est la **dernière version** de sa série dans le dossier client | Plusieurs révisions coexistent (ex. TIM 7 : REV5 à REV16) ; contrôler une version dépassée ne sert à rien |
| C2 | **Non-régression** : chaque faute déjà relevée par un réviseur est encore détectée par le script | Une faute relevée une fois ne doit jamais repasser ; liste dans `CAS_NON_REGRESSION` du script |
| C3 | Tout compte cité dans le module ecritures-sans-faute et dans les listes d'opérations existe dans le plan AUDCIF | Les fautes de numéros viennent souvent de la documentation elle-même |
| C4 | **Taux** en vigueur : TAUX_ET_SEUILS (CN, TA, FPC…) concorde avec le script ; aucun ancien taux (FDFP 1 %) ne traîne dans les modules | Le contrôle de paie dépend des taux |
| C5 | **Catalogue des notes de revue** à jour : aucune note reçue après sa dernière mise à jour ; observations sans contrôle automatique listées pour la revue manuelle | Chaque note de revue doit devenir une règle |
| C6 | **Listes d'opérations** (`~/SKILL COMPTABLE/LISTE_OPERATIONS_*.md`) : opérations « nouveau » non intégrées, points « à trancher » en attente du gérant | Rien ne doit rester entre deux états |
| C7 | Pas de copies `.bak` dans les références | Éviter de lire une version périmée |
| C8 | Le SKILL.md renvoie à ecritures-sans-faute et à auditeur-comptable | Routage |

**Après chaque nouvelle note de revue :** ajouter la faute au catalogue, la règle au module, la règle au
script, **et un cas dans `CAS_NON_REGRESSION`** ; relancer `mises-a-jour` jusqu'à zéro point bloquant.

## 5. Rapport et suite

Le rapport classe chaque observation en **bloquant** (ne pas remettre), **réserve** (justifier par écrit
dans la grille de rapprochements G1-G12 du module ecritures-sans-faute) ou **vérifié**. Joindre le rapport
au dossier de travail (pas au livrable client). Après correction, relancer l'auditeur : on ne remet que sur
un rapport sans point bloquant et avec chaque réserve justifiée.
