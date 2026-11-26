---
name: charte-2026
description: Charte MDC 2026 (11/10/2026) — diagnostic et non audit, Indice MDC sur 100 et non AAA-D, pas de visa ni de tenue comptable ; dossier de conception LA CONFORMITE LMDC
metadata:
  type: project
---
La **charte MDC 2026** est en vigueur depuis le 11/10/2026. Sa source est le dossier de conception `/Users/bilefilsseverin/LA CONFORMITE LMDC/`, qui contient : plan directeur, Méthode de l'Indice MDC, manuels M00 à M09, modèles, fiches de poste et formation.

**Identité** : « Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social ».

**Vocabulaire** :
- audit devient diagnostic ;
- la note AAA à D devient l'**Indice MDC sur 100** (45 contrôles, 6 domaines T, V, F, S, C, G), avec une exposition estimée en FCFA ;
- visa et certification deviennent l'attestation de diagnostic ;
- « anomalie » devient « observation ».

**Périmètre** :
- La comptabilité (tenue, révision, écritures, états financiers) relève de l'expert-comptable partenaire.
- Les actes juridiques relèvent de l'avocat partenaire.
- Les générateurs de publication bloquent le jargon technique et l'ancien vocabulaire.

**Diagnostic** : M03 décrit le processus en 13 étapes. Les trois inventaires du profil (documentaire, personnel, immobilisations) se font à l'étape 5 ; leur détail est dans M03 A, `manuels/M03A_INVENTAIRES_DU_PROFIL.md` (11/10/2026).
- L'inventaire des immobilisations est un **constat** : sans valeur nette, sans amortissement, sans compte ; les écarts sont transmis à l'expert-comptable.
- L'inventaire du personnel croise **4 sources** et n'est remis qu'au dirigeant.

**Précautions** : une autre session peut travailler en parallèle dans ce dossier ; ne pas écraser ses fichiers. Pour publier un document de ce dossier, utiliser `outils/generer_pdf.py`.

**Why** : décision du gérant (dossier de conception du 10/10/2026).

**How to apply** :
- Tout nouveau livrable suit la charte.
- Les anciens outils sont réutilisés selon `11_RESSOURCES_REUTILISABLES.md`.
- Le dispositif [[dispositif-declenchement-machine]] est antérieur à la charte et doit être mis à la charte avant tout usage client.

**Papier à en-tête 2026 (12/10/2026)** : `SUPERVISEUR GENERAL/PAPIER_EN_TETE_2026/` (docx, dotx, lettre type, PDF ; générateur `_SOURCES/build_entete.py`) + note de service MC-NS-2026-008. Le contrôle qualité bloque aussi la simple citation de l ancienne mention « Agence de Notation ».

**Procédure du gérant et carte des documents (12/10/2026)** : deux documents dans `SUPERVISEUR GENERAL/PROCEDURES_GERANT/`.
- **MC-PROC-ACC-2026-001, accompagnement d'un nouveau client** : 4 phases (profil, matrices, plan d'action, suivi), 10 jours au plus, tout numérique.
- **MC-PROC-DOC-2026-001, « Les étapes et les documents »** : à chaque étape, le modèle de la charte ou l'outil à utiliser.
- **Documents encore à créer** : inventaire des tiers (créances et dettes, en constat) ; feuille de chiffrage ; fiche d'identification du client et du bénéficiaire effectif ; versions génériques du PV de comptage, du compte rendu et de la demande d'explication écrite ; onglet Indice du classeur de diagnostic d'entrée.

**Documents créés le 12/10/2026** par `PROCEDURES_GERANT/_SOURCES/build_documents_manquants.py`, dans le dossier de conception :
- **Modèles :** inventaire_des_tiers, feuille_de_chiffrage, fiche_identification_client (elle reste au gérant), proces_verbal_comptage_caisse, compte_rendu_reunion, demande_explication_ecrite.
- **Outils :** INVENTAIRE_DES_TIERS_MDC.xlsx et FEUILLE_DE_CHIFFRAGE_MDC.xlsx.
  - Intérêts de retard vérifiés dans le LPF, art. 161-1 : 5 % puis 0,5 % par mois ; 10 % puis 1 % par mois pour les retenues, la TVA et l'ITS.
  - Majorations retenues selon la méthode : 15 ou 30 %, 30 ou 60 %, 100 ou 150 %.
- **Classeur de diagnostic d'entrée :** l'onglet « 9 Indice » porte les 45 contrôles du référentiel. Son résultat est identique à celui du moteur indice_mdc.py (testé).

**Entrée du client :** elle relève du gérant. Elle a été retirée de la carte des documents (consigne du 12/10).

Fiche d'identification du client : retirée à la demande du gérant (12/10), jugée inutile. Ne pas la recréer.

**Profil de l'entreprise, modèle complet (12/10/2026, à la demande du gérant).** Le modèle de la charte ne lui convenait pas. Le nouveau est MC-MOD-PROF-2026-002, dans `SUPERVISEUR GENERAL/PROFIL_ENTREPRISE_2026/` (docx et pdf de 22 pages, source md dans `_SOURCES`).
- **A — L'entreprise.**
- **B — Diagnostics et inventaires :** documentaire, personnel croisé à 4 sources, procédures internes et externes, tiers, créances et dettes, stock, immobilisations, projets et investissements.
- **C — Fiscalité :** régime, grille des natures d'impôts en 2 étapes, situation fiscale.
- **D — Chiffre d'affaires et argent :** méthode M1 à M7, reconstitution en 15 lignes, triangle du CA, revendeur ou intermédiaire, comptes de trésorerie, sorties et modes de règlement, locaux.
- **E — Comptes SYSCOHADA à utiliser,** à valider par l'expert-comptable.
- **F — Difficultés, alertes, points ouverts, synthèse T V F S C G.**

Le fichier `modeles/profil_entreprise.md` de la charte n'a pas été modifié (autre session).
