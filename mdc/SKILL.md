---
name: mdc
description: >
  SKILL UNIQUE de MDC (La Maison de la Conformité SARL) — regroupe en un seul point d'entrée toute l'expertise du cabinet : comptabilité SYSCOHADA, fiscalité ivoirienne (CGI 2026, TVA, ITS, IMF, I-BIC, patente), réintégrations/déductions, avantages en nature, retenues sur salaire, EBNL, audit global et pilotage de mission, contrôle fiscal, notation de conformité (Indice /100), diagnostic financier, LBC/FT, points à éclaircir et DEE, production et mise en forme des livrables (rédaction brandée, PDF/Word/Excel), préparation des mails clients (brouillons Gmail), cartographie « qui reçoit quoi », vidéo et direction artistique de la chaîne AVEC MON FISCALISTE. Connaît l'état courant des clients et des documents créés. Déclenche dès que l'utilisateur parle d'un client MDC, d'un dossier, d'une mission, d'un document à produire ou vérifier, d'un impôt, d'une écriture, d'un relevé bancaire, d'un audit, d'une note, d'une DEE, d'un mail client, d'un livrable, de la plateforme MDC, ou de la chaîne YouTube.
---

# MDC — skill unique

Ce skill remplace les 19 anciens skills. Chacun est un **module** : son mode d'emploi complet est dans `modules/<nom>/MODULE.md`, avec ses `reference/`, `scripts/` et modèles. Chemin de base : `~/.claude/skills/mdc/`.

## Étape 0 — se mettre à jour (à chaque session MDC)

1. Lancer `python3 ~/.claude/skills/mdc/etat/rafraichir.py`, puis lire `etat/ETAT_COURANT.md` : clients, documents récents, fichiers de suivi, mémoire du Superviseur.
2. Pour la situation exacte : outils `plateforme-mdc` (`synthese`, `lister_documents`, `trouver_fichiers`), puis `SUIVI CLIENTS/SUIVI_DES_DOSSIERS_MDC.xlsx` et `SUPERVISEUR GENERAL/00_REGISTRE_DES_DOCUMENTS_VALIDES.xlsx`.
3. Sur un client précis : lire son dossier dans `~/Documents/DOSSIER CLIENTS/<CLIENT>` avant toute réponse, ne rien supposer.

## Étape 1 — choisir le module

Lire `modules/<nom>/MODULE.md` du ou des modules concernés avant d'agir. Plusieurs peuvent s'enchaîner (fond → vérification → mise en forme → envoi).

| Besoin | Module |
|---|---|
| **Toute écriture, journal, ordre de saisie Sage, balance, à-nouveaux, liasse : contrôle obligatoire avant remise** | `ecritures-sans-faute` |
| **Second regard indépendant avant remise : écritures justes, principes comptables respectés, mises à jour faites (dossier et skill)** | `auditeur-comptable` (agent `auditeur-comptable` pour une relecture indépendante) |
| Comptabilité, écritures, relevés bancaires, télédéclaration e-impôts, documents commerciaux (note méthodo, propale, contrat), serveur | `mdc-expert` |
| Question d'impôt, taux, article, exonération, régime | `fiscalite-ci` |
| Passage résultat comptable → fiscal, déductibilité | `reintegrations-deductions` |
| Avantages en nature (véhicule, logement, carburant…) | `avantages-en-nature` |
| Retenues sur salaire, sanctions, avances | `retenues-salaire-paie` |
| Comptabilité des associations / EBNL (SYCEBNL) | `comptable-ebnl` |
| Piloter une mission d'audit global de bout en bout | `auditeur-superieur` |
| Contrôler le travail fiscal avant livraison | `auditeur-fiscal` |
| Indice MDC de conformité /100, plan d'action, visa | `notateur-conformite` |
| Santé financière, ratios, diagnostic | `diagnostic-financier` |
| Blanchiment, KYC, CENTIF, dispositif LBC/FT | `dispositif-lbc-ft` |
| Détecter les points douteux, rédiger la DEE | `points-a-eclaircir` |
| Fabriquer, contrôler, ranger les livrables d'un dossier | `producteur-livrables` |
| Catalogue complet des livrables d'un audit | `producteur-livrables-audit` |
| **Produire le dossier d'audit d'un client à partir des données de l'Atelier du diagnostic** | skill `dossier-audit` (`~/.claude/skills/dossier-audit/`) |
| Mise en forme brandée PDF/Word, contrôle qualité avant remise | `redaction` |
| Corps de mail client, brouillon Gmail (jamais d'envoi) | `preparation-mails` |
| Relire et corriger la note de démarrage et le contrat d'un nouveau client | `demarrage-client` |
| Quel document part à qui | `qui-recoit-quoi` |
| Récap / révision de tous les dossiers, point sur un client | skill `revision` (`~/.claude/skills/revision/`) |
| Scénario, art oratoire, chaîne YouTube | `directeur-artistique` |
| Montage vidéo du rush | `monteur-video` |

## Règles permanentes (toutes missions)

- Aucune écriture comptable ne sort sans le module `ecritures-sans-faute` : comptes vérifiés dans le plan AUDCIF, script `controle_ecritures.py` à zéro erreur, grille de rapprochements remplie.
- Puis passage par `auditeur-comptable` (`audit_comptable.py tout …`) : aucun point bloquant sur les trois axes (écritures, principes, mises à jour) avant remise.
- **Aucun chiffre inventé ni « diversifié »** pour paraître naturel ; un montant sans pièce reste tel quel, signalé à justifier. **Aucun mouvement bancaire sans relevé** (seul le document du prêteur fonde un prêt), jamais d'écriture d'équilibrage vers une trésorerie estimée, jamais de stock alimenté par la caisse ou la banque. **Aucune écriture CNPS sans instruction du Gérant.** Le régime fiscal effectif (avis émis) gouverne les écritures ; un seuil dépassé est un risque, pas un changement de régime (module `ecritures-sans-faute`, R13 à R20).
- Tout en FCFA, droit ivoirien et OHADA, secret professionnel. Identifiant ivoirien : NCC, jamais « IFU ».
- Tout document passe par `redaction` avant remise ; sobre, formel, sans encadré coloré ni style IA.
- Aucun montant (honoraires, chiffres client) dans un document interne destiné aux collaborateurs.
- Livrables enregistrés dans un dossier suivi (DOSSIER CLIENTS, SUPERVISEUR GENERAL…) pour apparaître sur la plateforme (localhost:8765, à relancer par `open` sur Plateforme MDC.app) ; marquer les livrables avec `marquer_livrable`.
- Tout numérique : pièces scannées, signatures numériques, PDF.
- Mails : brouillons seulement, jamais d'envoi.
- **Jamais « gratuit »** dans un document MDC (ni pour une prestation, ni pour une démarche administrative) : écrire ce qui est dû ou « en cours de vérification ». Contrôle bloquant dans les générateurs.
- **Propositions et documents clients : aucune échéance ni aucun délai** (ni dates de remise, ni délais administratifs, ni durées de validité) sauf demande expresse du Gérant. Pour les délais des administrations, écrire seulement : « Nous allons nous renseigner auprès de nos différents partenaires pour connaître le délai qu'ils nous donnent. »
- Identifiants serveur : `modules/mdc-expert/.private/`, jamais versionnés ni recopiés.

## Maintenance

Les chemins `~/.claude/skills/<ancien-nom>` restent valides (liens vers `mdc/modules/`). Pour ajouter un module : créer `modules/<nom>/MODULE.md` et une ligne dans le tableau ci-dessus.
