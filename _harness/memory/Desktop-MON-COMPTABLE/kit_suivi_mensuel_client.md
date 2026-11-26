---
name: kit_suivi_mensuel_client
description: "Kit opérationnel LMDC pour operationnaliser un suivi mensuel client (guide, emails, plan de classement, script)"
metadata: 
  node_type: memory
  type: project
  originSessionId: bf248b83-bd03-41b1-9fd9-7d5221669470
  modified: 2026-08-06T01:18:56.028Z
---

Kit réutilisable pour passer la méthodologie LMDC à la pratique, dans `Documents/METHODOLOGIE LMDC/KIT_SUIVI_MENSUEL_CLIENT/` (sources `.md` dans `_SOURCES_MD/`, docx générés via `scratchpad/md2docx_lmdc.py`) :
- **GUIDE_COLLABORATION_CLIENT_LMDC** — manuel client bref (démarche, attentes, outils, livrables mensuels). Régime-conscient (TCE/TEE, RME, RSI, RNI — seuils « selon annexe fiscale en vigueur », pas de chiffres inventés). Insiste : outils mis à dispo + **suivre à la lettre nos instructions** + **tenue du journal = priorité n°1**.
- **KIT_EMAILS_SUIVI_MENSUEL_LMDC** — modèle par étape. Onboarding (E1 identité minimale, E2 note démarrage+demande pièces, E3 PV réception) UNE fois ; mensuel (M1 rappel collecte le 1er, M2 montants à télépayer le 10, M3 reporting+note de conformité le 25, M4 relance). Objet normalisé **`LMDC – [CATÉGORIE] – [OBJET]`**.
- **PLAN_DE_CLASSEMENT_LMDC** — disposition **LBTECH** érigée en standard : Domaine→Année→Nature→Tiers, 4 domaines **1.JURIDIQUE 2.FISCAL 3.SOCIAL 4.COMPTABLE**.
- **creer_dossier_client.sh** — génère l'arborescence vide par client : `./creer_dossier_client.sh "CLIENT" "2024 2025 2026"`.
- **MANUEL_COLLABORATION_CLIENT_LMDC** (docx+pdf, réf MC-MANUEL-CLIENT-2026-001) — **doc définitif** fusionnant le guide + le plan de classement en UN manuel client, publié via le pipeline officiel `publish_livrable_mdc.py`/`publish_pdf_mdc.py` (logo+filigrane+contrôle bloquant, cf. mdc-expert §9.0/§22). Mail de transmission = `_SOURCES_MD/MAIL_TRANSMISSION_MANUEL.md` + **brouillon Gmail créé** pour BALIMA (ECOMAF-2S & TRACE LOGISTICS CI), objet `LMDC – AUTRES – …`, cc Direction + N'CHO. ⚠️ create_draft ne joint pas de PJ : attacher le PDF du manuel avant envoi.

**Version finale du manuel (16 sections)** : cadrage préalable (§2 : audit documentaire = collecte + audit des immobilisations) · montée en charge (1er mois pris en charge → passation progressive) · insistance sur les **relevés mensuels** (analyse/anomalies/recommandations) · livrables mensuels détaillés (§8 : reporting intégrant le suivi temps réel des obligations, analyse journal/caisse/relevés/impôts/paiements, base comptable pour Sage, point des impôts payés/à payer, note de conformité) · **PV de transmission** pour chaque document (§9) · **canal secrétariat `lmdcserviceclient@outlook.com`, prise en charge 48 h**, ne pas passer par le Gérant sauf urgence/copie (§12) · plan de classement **supervisé par le chargé de suivi** (§13). ⚠️ **Correction fiscale (instruction gérant) : ITS et FDFP dus chaque mois MÊME sans salarié** ; CNPS seulement si salariés — appliqué au tableau des régimes du manuel ET du guide.

**Mail d'ouverture — MODÈLE UNIQUE VALIDÉ** (`_SOURCES_MD/MAIL_OUVERTURE_SUIVI.md` → `MODELE_MAIL_OUVERTURE_SUIVI.pdf/.docx`, réf MC-MAIL-OUVERTURE-2026-001) : c'est l'AGENCE qui pose le cadre (pas de « merci pour votre proposition »). **2 variantes** (objet + intro seulement) — A. nouveau client / B. client déjà suivi à qui on instaure la nouvelle méthode (GLOBE, LERO, TIM). Corps : transmet le manuel (qui explique brièvement fond + attentes) → annonce les **ordres de mission** (audit documentaire + audit immobilisations + collaborateur désigné pour montrer le classement, **ordre de mission signé/cacheté par le Gérant**) → outils → secrétariat 48 h. PAS la convention d'objet dans le mail (elle vit ailleurs). L'ancien MAIL_TRANSMISSION_MANUEL (flavour BALIMA) est archivé/remplacé. Le brouillon Gmail BALIMA existant est obsolète (à ignorer). Trame 2 du KIT_DEMARRAGE_SUIVI alignée sur ce modèle.

**Dossier `METHODOLOGIE LMDC/VERSIONS FINALES/`** = uniquement les livrables définitifs prêts à diffuser (manuel pdf+docx, fiche inventaire immo pdf+xlsx, modèle mail transmission pdf, + 00_LISEZ-MOI). Callout ITS/FDFP reformulé « la déclaration mensuelle reste due même sans salarié (le cas échéant à zéro / sur la rémunération du dirigeant) ». Manuel 05 (A→G) NON réaligné (laissé en l'état, option ouverte).

Rythme : pièces **avant le 5** → déclarer/payer **avant le 15** (réel) → reporting+note **fin de mois**. Supervision opérationnelle confiée à **N'CHO** (lmdcjuridicofiscal@outlook.com), Gérant en supervision/visa. Cas vivant : BALIMA (comptable ECOMAF-2S / TRACE LOGISTICS CI) attend le circuit — voir [[client_trace_logistics]].

**Audit des immobilisations en Étape 1** : l'audit documentaire ET l'inventaire physique des immobilisations se mènent ENSEMBLE pendant la collecte (noté au PARCOURS). Outils dans `ETAPE_1_CADRER/` (+ copiés dans le package) : `FICHE_INVENTAIRE_IMMOBILISATIONS_MDC.xlsx/.pdf` (fiche vierge terrain, réf MC-INV-IMMO-2026-001, générée via `scratchpad/fiche_immo.py`), `MANUEL_INVENTAIRES_GABARIT_MDC.docx`, `LI-7_IMMOBILISATIONS_AMORTISSEMENTS_MDC.docx`. Comptage en binôme, rapprochement registre/physique, art. 17 AUDCIF.

⚠️ **Divergence à trancher** : Manuel 05 documente un plan **A→G (7 domaines)** « norme unique » mais le réel LBTECH est en **4 domaines numériques**. Standard retenu = LBTECH ; réalignement du Manuel 05 recommandé, non encore fait. Voir [[methodologie_balance_mdc]].
