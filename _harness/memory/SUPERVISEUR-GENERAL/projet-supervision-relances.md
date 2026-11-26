---
name: projet-supervision-relances
description: Projet en cours — système de supervision et de relances des clients/dossiers de MDC
metadata: 
  node_type: memory
  type: project
  originSessionId: 66ec9d18-20bf-4de1-9326-2a34749e0c38
  modified: 2026-09-18T11:25:27.912Z
---

Objectif : donner à l'utilisateur ([[user-role]]) un **système de suivi** pour ne plus être le goulot d'étranglement. Problème initial (juillet 2026) : il ne suit pas ses dossiers et ne s'en souvient que quand le client le relance. Il a mis en place une **feuille de route** et un **rapport journalier** que l'équipe doit lui envoyer, et veut que je fasse les **supervisions et relances**.

Livrable : classeur Excel **`Suivi_Superviseur_MDC.xlsx`** (déplacé le 18/09/2026 vers `~/Documents/SUIVI CLIENTS/`, dossier dédié créé à la demande de l'utilisateur ; contient aussi `Suivi_Dossiers_Clients_MDC.xlsx`, le classeur plus récent avec un onglet par client), 7 onglets : Suivi Clients (cockpit), Tableau de Bord (compteurs auto), Répertoire Clients (identité/fiscalité), Rapports Journaliers, Relances, Collaborateurs, Guide. Colonnes auto : « Jours sans rapport » et « Écart échéance ». Colonnes jaunes = à remplir par lui.

**Source clients** : PDF `situation_globale_clients_MDC_2026-07-19.pdf` (61 pages) — **57 clients** extraits (tableau récap p.1-3 + une fiche/client p.4-60 + stats p.61). Chaque fiche = Informations (Secteur/Régime/NCC/CDI/Email/Tél/Contact) + Prestations (actives/passagères+tarif) + « Actions à mener » = **feuille de route**. Classeur **déjà pré-rempli** avec les 57 ; les 7 clients ayant des actions en attente sont pré-marqués En cours/À faire + Priorité Haute. Doublon source : TRACE LOGISTICS (#19/#20). #42 = son propre cabinet listé comme client.

**Ordres de mission** : ils sont dans sa **boîte mail (Gmail)** — connecteur Gmail disponible ; proposer de les récupérer/rapprocher (avec son accord). Canal des rapports journaliers de l'équipe : à confirmer.

**Organisation MDC découverte (Gmail, juillet 2026)** — les dossiers sont pilotés par **ordres de mission** numérotés `ORD-2026-XXXX` (≈39 émis), envoyés au client ET au département concerné (fiche OM = mission, client, catégorie, échéance, équipe, **personne en charge**). Deux départements exécutants + un service client :
- **Département Juridico-Fiscal** (Équipe Fiscalité & Droit des Affaires) — resp. **N'CHO OCHO PIERRE** — lmdcjuridicofiscal@outlook.com
- **Département Comptabilité** — resp. **N'GUESSAN YAO CLAUDE** — lmdccomptabilite@outlook.com
- **Service Client** — lmdcserviceclient@outlook.com (resp. à confirmer)
Points en attente déjà repérés : GLOBE CI & KF IMMOBILIER (attendent DFE+RCCM), TIM 7 (contrats de travail ; OM-0033 échéance 10/07 dépassée), COLLEGE ST EXUPERIE (OM-0030 échéance 03/07 dépassée ; client veut parler au gérant), FAMILLE KRA (harmoniser avec Mme Carole).

**Vision cible de l'utilisateur (juillet 2026)** : le livrable n'est PAS Excel mais un **rythme** — chaque soir, les points journaliers rentrent → je produis un **rapport de relance pour le lendemain** → il valide → je prépare les **mails aux départements avec instructions**. Le classeur reste ma base/mémoire en coulisses. Il veut aussi une **note de service** imposant aux équipes une **feuille de route par dossier** (départements intervenants, plan d'action, manœuvres entreprises, dates de dépôt/récupération de documents en administration, appels, relances datées) + normaliser le contenu des points journaliers.

**Livrables produits (juillet 2026)** :
- **Note de service `MC-NS-2026-001`** (feuille de route par dossier + normalisation du point journalier, heure limite 18h00, annexes modèles) → `NOTE_DE_SERVICE_FEUILLE_DE_ROUTE_2026-07-19.docx/.pdf` dans `SUPERVISEUR GENERAL/` (générés via `publish_livrable_mdc.py`/`publish_pdf_mdc.py`, en-tête logo + filigrane, QC OK). Destinataires : les 3 responsables — N'CHO Ocho Pierre (JF), N'GUESSAN Yao Claude (Compta), **AKOCHI Colombe (Service Client)**.
- **Brouillon Gmail** de transmission de la note aux 3 boîtes départements créé (id r-5898695087761055689) — PJ à glisser manuellement (create_draft ne joint pas la PJ ici) ; à envoyer après validation.

**Routine quotidienne** : tâche planifiée **`point-supervision-mdc-18h`** (`/Users/bilefilsseverin/.claude/scheduled-tasks/`), cron `0 18 * * *` (18h00 Abidjan) — lit les mails du jour, met à jour le classeur, produit le rapport de relance du lendemain + brouillons de relance à valider. Tourne quand l'app est ouverte (sinon au prochain lancement). Lui recommander « Run now » une fois pour pré-approuver les outils (Gmail, Python/fichiers).

**Règle de fonctionnement convenue** : je prépare les relances (client ET collaborateur) mais je **n'envoie jamais rien sans sa validation** (uniquement des brouillons).

**État au 17/08/2026** : ordres de mission émis jusqu'à **ORD-2026-0045** (0040 WILLING SERVICES annulé — client de Mme NIAMIEN ; 0041 TRACE LOGISTICS ; 0042 FABELLASHOP ; 0043 ACHAT EXPRESS ; 0044 & 0045 KF IMMOBILIER — SCI & SARL). Quatrième interlocutrice identifiée au Juridico-Fiscal : **NIAMIEN Habenan Murielle, assistante fiscale** (même boîte lmdcjuridicofiscal@outlook.com), qui gère ses propres clients (ex. WILLING SERVICES). Constat récurrent : **les départements n'envoient pas de point journalier** — ils transmettent des pièces (XML e-impôts, PDF) sans corps de message ; le Service Client est **muet depuis plus de 10 jours**. Nouveau prospect ajouté au classeur en n° 58 : **BUSINESS HALL CÔTE D'IVOIRE** (Mme OUATTARA Adja Matenin, direction@businesshall.ci) — proposition d'audit transmise le 16/08.

Environnement : LibreOffice/soffice absent + Python 3.9 → `recalc.py` du skill xlsx ne tourne pas ici ; je mets `fullCalcOnLoad=True` pour que les formules se calculent à l'ouverture dans Excel/Numbers.
