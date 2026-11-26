# Projet AUD GLOBAL — LA MAISON DE LA CONFORMITÉ SARL (LMDC)

## ⚠ DISTINCTION CRITIQUE
- **LMDC** = la marque/cabinet (toujours utiliser, pas "MDC")
- **MDLC** = la méthodologie propriétaire (Manuel d'audit Logique des Comptes)

## 📚 RÉFÉRENCE MAÎTRE — À LIRE EN PREMIER
**`/Users/bilefilsseverin/Desktop/MON COMPTABLE1/MEMOIRE_LMDC_COMPLETE.md`**
↑ Document consolidé de TOUTES les compétences acquises. À recharger en début de chaque session.

## Fichiers de compétences techniques
- `/Users/bilefilsseverin/Desktop/MON COMPTABLE1/COMPETENCE_MDLC_REFERENCE.md` (référence détaillée 697 lignes)
- `/Users/bilefilsseverin/Desktop/MON COMPTABLE1/RAPPORT_ANALYSE_FAMILLE_KRA_2024_v2_MDLC.xlsx` (rapport modèle)

## Identité LMDC (rappel rapide)
- SARL · Capital 1 000 000 FCFA · NCC **2506426B** · RCCM **CI-ABJ-03-2025-B13-10831**
- Gérant : M. BILE FILS SEVERIN
- Email : **lamaisondelaconformite@gmail.com** · Tél : +225 07 19 31 49 04
- Site : **www.lamaisondelaconformitesarl.net** (avec "sarl"!)
- Réseaux sociaux : **@Mon Fiscaliste CI** (TikTok, Facebook, YouTube)

## Positionnement
> « LMDC est une **agence de notation en matière de conformité administrative** — comptable, fiscale et sociale. »
> « Nous évaluons la capacité d'une entreprise à **sortir vainqueur d'un contrôle de l'administration**. »

## 4 départements
1. **Secrétariat** — la porte d'entrée
2. **Comptabilité** — le cœur technique
3. **Fiscalité & Droit des affaires** — le bouclier
4. **Communication** — la voix du cabinet *(ajouté 27/04/2026)*

## Mission — 5 piliers
RECONSTRUIRE · ANTICIPER · ÉDUQUER · ORGANISER · DÉFENDRE

## Vision
**« Que Dieu nous aide »** — Devenir LA référence ivoirienne en notation de conformité.

## Marché ivoirien — diagnostic
Souffre de 2 maux : **BRICOLAGE** + **MANQUE D'ÉDUCATION**

## Méthodologie MDLC en 5 étapes
EXPLIQUER → AUDITER → RAPPORTER → RÉGULARISER → ENCADRER & CONTRÔLER

## Skills synchronisés
- `analyse-releve-bancaire` : Catégorisation opérations bancaires
- `rapport-audit-global` : Audit complet 12 pages PDF avec grille notation
- `mdc-expert` : Polyvalent SYSCOHADA / OHADA / fiscalité CI
- `analyse-historique-paiement-impots` (29/04/2026) : Excel interactif FULL-EDITABLE
  - Distinction CHARGE constatée (Cl. 6) vs PAIEMENT effectif (Cl. 4 MvtD)
  - Dette cumulée = Dette N-1 + Charge N − Paiement N
  - Cascade AN(ouv) automatique pour comptes de bilan
  - Format type : 9 onglets (Synthèse, KPIs, État Général, Détail, Observations, Écritures, Plan d'Action, Reports, Guide)

## Conventions Excel interactif
- 🟡 Jaune `FFF2C0` = saisie  ·  🔵 Bleu `DCE7F8` = calcul auto
- 🟣 Violet `E5DAF0` = AN cascade  ·  🟢 Vert `DAEFD9` = solde 31/12
- 🔴 Rouge/Rose = dettes  ·  🏛 Navy `1A1A2E` = headers  ·  ✨ Or `C8A24C` = totaux

## Règle livrables clients
TOUJOURS placer les Excel interactifs dans :
`/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/[NOM CLIENT]/_FICHIERS_INTERACTIFS_LMDC/`

## Infrastructure VPS
- Domaine OFFICIEL : **lamaisondelaconformitesarl.net** (avec "sarl"!)
- IP : 109.199.123.251
- SSH : root + <MOT DE PASSE RETIRÉ>
- Backends PM2 :
  - mdc-backend (3000) — main + secrétaire
  - mdc-creation (3001)
  - mdc-crm (3002)
  - audit-lmdc (3003)
  - mdc-comptable

## Espace Secrétaire (production-grade)
- URL : https://lamaisondelaconformitesarl.net/admin/secretaire.html
- Login : secretaire@lamaisondelaconformite.com / Password : <MOT DE PASSE RETIRÉ>
- Stack : bcrypt + JWT HS256 + sessions révocables + audit log + healthcheck
- DB : /var/www/mdc/backend/secretariat.db

## Présentation équipe LMDC (livrée 27/04/2026)
- Folder : `/Users/bilefilsseverin/Documents/PRESENTATION EQUIPE LMDC 2026-04-27/`
- 22 slides 16:9 · Times New Roman · navy + or sur ivoire

## RÈGLES DE TRAVAIL APPRISES
- ⚠ TOUJOURS respecter la dernière correction utilisateur (ne pas sur-écrire avec données archivées)
- ⚠ JAMAIS dire "IS" ou "IS RME" — utiliser "TEE" / "RME" / "RNI"
- ⚠ JAMAIS confondre LMDC (cabinet) et MDLC (méthodologie)
- ⚠ Présenter explicitement les divergences entre sources avant correction

## RÈGLE OBLIGATOIRE — Git Push automatique
À chaque travail significatif : commit + push sur GitHub (compte **Milang225**, repos privés).
- `~/bin/gh` installé et authentifié
- `.gitignore` toujours présent

## Repos GitHub (Milang225)
| Repo | Projet | Chemin local |
|------|--------|-------------|
| aud-global-lmdc | Plateforme Audit Global | ~/Desktop/AUD GLOBAL |
| competence-mdlc | Référence MDLC + modèles | ~/Desktop/MON COMPTABLE1 |
| site-mdc | Site principal | ~/Desktop/SITE |
| mon-comptable | ComptaPilot 360 SYSCOHADA | ~/Desktop/MON-COMPTABLE |
| mon-fiscaliste | CRM Fiscaliste | ~/Desktop/MON FISCALISTE |
| mdc-vps | Panel admin + backend VPS | ~/Desktop/projets-vps/mdc |
| crm-mdc | CRM clients/dossiers | ~/Desktop/projets-vps/crm |
| creation-mdc | Création entreprise | ~/Desktop/projets-vps/creation |
| mdc-comptable-vps | Module comptabilité | ~/Desktop/projets-vps/mdc-comptable |

## Dossiers clients de référence
- **SOM MULTI SERVICE** (EI/TEE) — Audit 2019-2024 livré 29/04/2026 — Note D
- **NADRELIE** (SARL) — Rapport audit 2024 livré
- **FAMILLE KRA** (SARL) — Modèle de référence MDLC

## Rapport modèle universel
`/Users/bilefilsseverin/Desktop/MON COMPTABLE1/RAPPORT_ANALYSE_FAMILLE_KRA_2024_v2_MDLC.xlsx`
