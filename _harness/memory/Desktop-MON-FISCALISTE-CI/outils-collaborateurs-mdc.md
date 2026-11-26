---
name: outils-collaborateurs-mdc
description: Outils MDC réutilisables (suivi collecte des pièces + PV de réception) rangés dans Documents/OUTILS MDC/
metadata: 
  node_type: memory
  type: reference
  originSessionId: c3c001b6-a642-4b04-ae47-9c68316ff5e7
  modified: 2026-08-03T02:58:28.446Z
---

Outils MDC transversaux (tous clients), dossier **`Documents/OUTILS MDC/`** :

- **`INVENTAIRE_COLLECTE_PIECES_MDC.xlsx`** (+ .pdf, générateur `generate_inventaire_collecte.py`) — classeur pour que les collaborateurs suivent si chaque entreprise a fait parvenir les pièces requises. 3 onglets : Mode d'emploi · Suivi collecte (grille : 37 pièces réf. par domaine juridique/fiscal/social/comptable/bancaire/ventes-achats/dirigeant, menu déroulant Statut Reçu·Partiel·Manquant·En attente·N/A + couleurs auto) · Synthèse & Alertes (COUNTIFS par client, complétude, COMPLET/INCOMPLET). Pour un nouveau client : copier le bloc de lignes, changer nom+NCC.
- **`PV_RECEPTION_INFORMATIONS_MDC.docx`** (+ .pdf, source `pv_reception_informations.md`) — modèle de procès-verbal de réception d'informations/pièces (parties, pièces reçues, pièces manquantes, réserves, signatures), à établir à chaque remise de dossier par un client.

Se rattache à l'audit documentaire (mdc-expert §3 / AXE I) et à [[base-documentaire-lmdc]]. Livrables produits via le pipeline règle d'or [[regle-dor-controle-livrables]].
