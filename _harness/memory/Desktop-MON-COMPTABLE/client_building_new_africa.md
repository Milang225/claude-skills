---
name: client-building-new-africa
description: "Client BNA — SARL BTP Côte d'Ivoire — Exercice 2025 — Profil à très haut risque (CP négatifs −100M, cessation paiements imminente). Premier dossier traité avec méthodologie MDC complète."
metadata: 
  node_type: memory
  type: project
  originSessionId: 489d2c42-e377-49c0-9928-1f3fbf20f979
---

**BUILDING NEW AFRICA SARL** (BNA) — Secteur BTP / Construction (matériels : vibreur, bétonnière, transport).

## Profil 31/12/2025
- Capital : **1 000 000 FCFA** (minimum légal SARL — sous-capitalisation manifeste)
- CA 2025 : **115 246 355 FCFA**
- Perte exercice : **−50 112 109 FCFA** (Sage) ou **−50 403 759 FCFA** (mon import — écart 291 650 mineur)
- Capitaux propres : **−100 020 154 FCFA** (NÉGATIFS)
- Trésorerie : **3 301 283 FCFA** (TENDUE — 0,6% du bilan)
- Effectif estimé : ~10-15 salariés
- Comptes courants associés : **86 016 149 FCFA** (NGUESSAN + BALDE + 164)
- Source comptable : Sage 100 i7 8.50, balance impression provisoire

## Verdict MDC : D — REFUS DE CERTIFICATION
- Art. **371 AUSCGIE** déclenché (SARL avec CP < 50% capital)
- Art. **25 AUPCAP** risque cessation paiements imminent (TN < dettes CT)
- Exposition fiscale latente ≈ 33,7 M FCFA (29% du CA)

## Anomalies critiques retenues (5 majeures sur 13)
- A1 — CP négatifs −100M
- A2 — Sous-capitalisation (capital 0,19% du bilan)
- B1 — Matériel transport totalement amorti avec dotation indue 2,2M
- B2 — Soldes débiteurs anormaux 4428 + 44284 (≈2M sens inversé)
- B5 — Cessation paiements imminente (AUPCAP art. 25)

## Livrables produits
Dossier : `/Users/bilefilsseverin/Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/EXERCICE_2025/`
- `balance_bna_exhaustive.py` — import 89 comptes (référence pour clients similaires)
- `generate_livrables_v2.py` — générateur liasse 5 onglets exhaustive
- `LIASSE_BNA_2025_V2_EXHAUSTIVE.xlsx` — liasse SN
- `ETUDE_FISCALE_BUILDING_NEW_AFRICA_2025.xlsx` — étude fiscale 4 onglets
- `parse_releves.py` — parser SGCI + NSIA (texte extrait via PyMuPDF)
- `generate_etat_bancaire.py` — générateur état bancaire 6 onglets
- `ETAT_BANCAIRE_BNA_DETAILLE.xlsx` — état bancaire (535 ops, 6 onglets dont Récap CA §5)
- `operations_parsed.json` — 535 opérations catégorisées brutes

## Résultats analyse bancaire (mai 2026)
Relevés traités : NSIA 2022 (190 ops) + SGCI 2023 (345 ops) — 5 PDFs scannés non traitables (OCR requis)
- **CA banque 2022** : 123 647 000 FCFA (ROMNI TRAVAUX = 45,4M + chèques anonymes 78,2M)
- **CA banque 2023** : 246 075 000 FCFA (100% chèques anonymes SG)
- **CCA entrants 2022** : 16 806 000 FCFA (7 personnes physiques : BALDE AISSATA 5,6M + NGUESSAN NGORA 3,4M + DAKPOGAN 2,7M + …)
- **CCA compta 2025** : 86 016 149 FCFA — couverture bancaire = ~20% (gap = relevés 2024-2025 scannés)
- **Retraits espèces non justifiés** : 39 628 000 FCFA (2022+2023) — ALERTE BCA-01
- **Client concentré** : ROMNI TRAVAUX = 37% CA 2022 — ALERTE BCA-02
- **Paiement fiscal tracé banque** : 11 492 FCFA vs 33,7M exposition — ALERTE BCA-03

## À faire à la prochaine intervention
- **Exiger l'export Sage Excel** pour zéro écart de bouclage (291 650 FCFA à résoudre)
- **Exiger relevés 2024-2025 en PDF natif ou CSV** pour compléter l'analyse bancaire (5 PDFs scannés)
- **Exiger bordereaux de remise de chèques SG 2023** pour identifier les clients anonymes
- Convocation AGE art. 371 AUSCGIE sous 6 mois post-approbation des comptes
- Audit DISA CNPS 12 mois pour quantifier sous-déclaration rétroactive
- Clarifier IS 11M (acompte vs IMF dû 3M)
- Justifier les retraits espèces 39,6M (BCA-01) : pointer dans comptes 57x ou 4621
- Vérifier lien ROMNI TRAVAUX avec associés (BCA-02)

## Dossier RECOURS REDRESSEMENT DGI 2022-2023 (juin 2026)
Notification définitive **NRD12739430** (DVFN-SDVS-BCP). Droits 14 115 395 + amendes 10 000 000 (RBE). Balances 2022 (bénéfice +27 567 383) et 2023 (perte −26 610 523) **équilibrées**.
- **Clients NOMMÉS enfin identifiés** (via rapport MDC déc. 2025) : **CCECC-CI, PORTEO BTP, OMNI-TRAVAUX**. Les « chèques anonymes » SG 2023 = CCECC (fact. 0000020, 25 000 000, encaissé 10/01/2023) + PORTEO (fact. 0000019, 18 233 648, encaissé 26/01/2023). Leur somme **43 233 648 = créances 411 au 31/12/2022** (décalage facturation 2022 / encaissement 2023).
- **Position retenue** : (1) TVA reconstitution encaissements = INFONDÉE — encaissements réels HT = HT déclaré au franc près (411 + relevés) ; reconstitution DGI surévaluée de 29 112 612 (TVA comptée 2×) → décharge 5 446 916 ; (2) IRVM = contesté EN TOTALITÉ (position 2 : non-déductibilité ≠ distribution, art. 180) → décharge 5 133 102 ; (3) écart CA 2023 (14 492 289) = abandon (recoupements DERAR non communiqués) ; (4) charges sans factures 2023 (22 595 291) = **CONCÉDÉES** (réintégrées, sans impôt car résultat fiscal reste déficitaire −4 015 232). **Décharge totale visée : 10 580 018.**
- Argument réserve NON utilisé (à vérifier avant emploi) : art. 12 + art. 58 sexies CGI (entreprise nouvelle, exonération BIC 24 mois → renforcerait IRVM=0). Art. 12 risqué (mauvaise foi).
- Régularisation comptable 2025 demandée (mémo) : annuler les charges 22 595 291 + ramener BIC 2025 de 11M à 8M.

**Livrables recours** dans `Documents/DOSSIER CLIENTS/BUILDING NEW AFRICA/` (racine, hors EXERCICE_2025) : COURRIER_DEMANDE_REEXAMEN_DGI_BNA.docx, PJ3_ETAT_DEPOUILLEMENT_RECONSTITUTION_ENCAISSEMENTS_BNA.docx, BORDEREAU_TRANSMISSION_PIECES_BNA.docx, RAPPORT_ANALYSE_REDRESSEMENT_BNA.docx, ANALYSE_ANOMALIES_vs_REDRESSEMENT_BNA.xlsx, MEMO_COMPTABILITE_REGULARISATION_2025_BNA.docx, DEPOUILLEMENT_{SGCI_2022,NSIA_2022,SGCI_2023}_BNA.xlsx, POINT_ENCAISSEMENTS_CLIENTS_BNA.xlsx, GABARIT_DEPOUILLEMENT_RELEVE_MDC.xlsx. Courrier à compléter : date réclamation initiale.

**Why** : ce client est le **cas pédagogique de référence** de la méthodologie MDC. Profil multi-anomalies représentatif de PME ivoiriennes en difficulté financière. Apport méthodologique majeur : la session a permis de finaliser le workflow standard MDC (§§12-17 du SKILL).

**How to apply** : à la prochaine sollicitation sur BNA, vérifier d'abord si l'utilisateur a fourni l'export Sage Excel pour rebouclage à 0 FCFA. Sinon repartir des livrables V2 existants.

Voir [[methodologie-balance-mdc]] pour la procédure standard, et [[skill-mdc-expert]] §17.4 pour les chiffres clés capitalisés.
