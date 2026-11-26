# Où sont les faits

Tout ce qui suit est **en lecture**. Aucune écriture dans le CRM sans l'accord du Gérant.

## Le serveur de production

`root@109.199.123.251` (Ubuntu), clé `~/.ssh/id_ed25519_contabo`. Il tourne jour et nuit, Mac éteint.

| Quoi | Où |
|---|---|
| Admin du site | `mdc-backend`, port 3000 — `lamaisondelaconformitesarl.net/admin/` |
| CRM équipes | `mdc-crm`, port 3002 — route `/crmequipes`, et `crm.lamaisondelaconformitesarl.net` |
| **Base du CRM** | `/var/www/crm/backend/crm-fiscaliste.db` (SQLite) |
| Documents | `/srv/mdc-production/Documents` — recopiés du Mac toutes les 5 minutes par le relais |
| Rapports produits | `/var/lib/mdc-coordinateur/` |
| Journal du coordinateur | `/var/log/mdc-coordinateur.log` |
| Transcription des notes vocales | `/usr/local/bin/mdc_transcrire.py`, moteur `/opt/whisper.cpp` (modèle `small`) |
| **Boîte WhatsApp du Gérant** | service `mdc-coordinateur` (systemd), `/opt/mdc-coordinateur/`, port 127.0.0.1:3017, page `https://lamaisondelaconformitesarl.net/coordination/` |
| Base de la boîte | `/var/lib/mdc-coordinateur/coordinateur.db` — tables `wa_contacts`, `wa_messages`, `wa_brouillons`, `journal` |
| Pièces jointes et notes vocales reçues | `/var/lib/mdc-coordinateur/media/` |
| Réglages (jetons, clés) | `/etc/mdc-coordinateur.env`, lisible du seul administrateur |
| Canal privé du Gérant | Telegram, module `/opt/mdc-coordinateur/telegram.js` — tables `tg_messages` et `memos` |
| Surveillant des plateformes | `/usr/local/bin/mdc_veilleur.js`, toutes les 10 minutes |

`app.lamaisondelaconformitesarl.net` est un site **Netlify**, pas sur ce serveur ; ses données
viennent de la base ci-dessus. On lit la base, pas l'écran.

Toujours ouvrir la base en lecture seule :
`sqlite3 -readonly /var/www/crm/backend/crm-fiscaliste.db "<requête>"`

## Les tables qui servent

| Table | Ce qu'elle contient | Colonnes utiles |
|---|---|---|
| `clients` | Les clients (73) | `id`, `company`, `contact_referant`, `prestation_suivi_global`, `prestation_suivi_compta`, `prestation_suivi_fiscal`, `tarif_mensuel`, `ncc`, `regime` |
| `teams` | Les six départements | `name`, `key`, `email`, `members` (JSON : nom, rôle, login) |
| `team_tasks` | **Les directives** | `recipient_name`, `title`, `deadline`, `status` (`a_faire`/`en_cours`/`fait`), `seen_at`, `progress`, `client_company` |
| `team_messages` | Messages d'équipe | `from_name`, `to_login`, `body`, `read_at` |
| `ordres_mission` | Les ordres de mission (61) | `numero`, `client_company`, `team_name`, `status` (`envoye_non_signe`/`envoye_signe`), `employee_status` (`nouveau`/`en_cours`/`livre`/`bloque`), `employee_last_update_at` |
| `dispatches` | Envois aux équipes | `status`, `deadline`, `received_at`, `submitted_at`, `validated_at` |
| `missions` | Les missions | `cid`, `title`, `phase`, `deadline`, `status`, `assigned_team` |
| `factures` | La facturation (71) | `statut` (`paye`/`impaye`/`partiel`), `montant`, `montant_paye`, `date_echeance`, `mois` |
| `consultations` | Prospects et rendez-vous | `statut` (`depot_recu`/`rdv_confirme`/`accord`/`termine`), `depot_montant`, `rdv_date`, `suite_prevue` |
| `depot_journal_lignes` | **La saisie comptable** | `cid`, `annee`, `mois`, `libelle`, `entree`, `sortie`, `valide_par`, `montant_ok` |
| `depot_suivi_fiscal` | **Les déclarations du mois** | `cid`, `annee`, `mois`, `data` (JSON par impôt : `statut_code`, `observation`) |
| `depot_paie` | **Les bulletins du mois** | `cid`, `annee`, `mois`, `data` (JSON : `salaries[]`) |
| `depot_personnel` | L'effectif du client | `nom`, `poste`, `declare_cnps`, `date_sortie`, `salaire_base` |
| `depot_entreprise_infos` | La fiche entreprise | `obligations` (JSON : PATENTE, RESULTAT, TVA, ITS, AIRSI, TSE, FONCIER, IRVM, E301…), `rccm`, `ncc`, `centre` |
| `depot_transmissions` | Ce qui a été transmis au client | `numero`, `created_at`, `nb_files`, `pv_path` |
| `email_logs` | Les mails partis | `destinataire`, `objet`, `statut`, `created_at` |
| `depot_requetes` | Les demandes des clients | `objet`, `canal`, `statut`, `date_requete`, `delai_jours` |
| `depot_activity` | Le journal de l'espace collaborateurs | `acteur`, `action`, `detail`, `created_at` |
| `dossiers_creation` | Les créations de sociétés | — |

Les trois tables du cycle (`depot_suivi_fiscal`, `depot_paie`, `depot_obligations`) ont la même
forme : une ligne par `(cid, annee, mois)`, avec le contenu dans `data` en JSON.

**Au 26/11/2026, elles sont presque vides** : 19 clients sont sous suivi mensuel et aucun n'a son
mois complet enregistré. C'est le premier chantier du Coordinateur — faire renseigner, pas refaire.

## Sur le Mac du Gérant

| Quoi | Où |
|---|---|
| Procédures du cabinet | `~/Documents/PROCEDURES LMDC/`, `~/LA CONFORMITE LMDC/` |
| Procédures du Gérant | `~/Documents/SUPERVISEUR GENERAL/PROCEDURES_GERANT/` |
| Checklists et manuels | `~/Documents/BASE DOCUMENTAIRE LMDC/06_PROCEDURES/` |
| Dossiers clients | `~/Documents/DOSSIER CLIENTS/<CLIENT>/` |
| Suivi des dossiers | `~/Documents/SUIVI CLIENTS/SUIVI_DES_DOSSIERS_MDC.xlsx` |
| Registre des documents validés | `~/Documents/SUPERVISEUR GENERAL/00_REGISTRE_DES_DOCUMENTS_VALIDES.xlsx` |
| Plan du Coordinateur | `~/COORDINATION/PLAN_COORDINATEUR.md` |

Et les outils `plateforme-mdc` : `synthese`, `lister_documents`, `trouver_fichiers`, `lire_fichier`,
`preparer_brouillon_gmail` (brouillons seulement, jamais d'envoi).
