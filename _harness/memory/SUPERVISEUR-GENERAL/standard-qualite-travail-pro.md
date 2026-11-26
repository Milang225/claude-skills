---
name: standard-qualite-travail-pro
description: "Exigence permanente du gérant — travail d'audit de niveau professionnel, plus jamais de dossier bâclé (réf. Collège Saint-Exupéry jugé bâclé)."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9935bb39-b36c-45ab-b5cd-94351ca5fbe2
  modified: 2026-08-28T03:00:38.318Z
---

Le gérant exige un **travail de niveau professionnel sur chaque dossier**, sans exception. Il considère que la mission **Collège Saint-Exupéry** a été **bâclée** (rigueur analytique insuffisante) — à ne pas reproduire.

**Why:** MDC vend de la conformité opposable ; un dossier superficiel expose le client ET décrédibilise le cabinet. La forme (kit de livrables, charte) était bonne sur Saint-Exupéry, mais le FOND doit monter d'un cran.

**How to apply :** dérouler INTÉGRALEMENT la démarche en 9 maillons [[demarche-audit-colonne-vertebrale-et-suivi]] sur chaque dossier — ne pas se contenter des EF, aller jusqu'à la base (réclamer l'export Sage), l'adossement des flux aux pièces, les erreurs d'écritures, la déductibilité charge par charge. Avant toute remise : (1) contrôle indépendant (auditeur-fiscal C1→C12 + auditeur-superieur bouclage) ; (2) revue de cohérence inter-livrables (chiffres pivots identiques partout, grep) ; (3) confrontation aux PIÈCES (ne jamais écrire « non enregistré/non fait » sans avoir vérifié les pièces — cas cession/baux LBTECH corrigé) ; (4) aucun jargon interne ni empreinte de production dans les livrables client ; (5) tout document passe par [[supervision-redaction-avant-livraison]]. Le gabarit de format reste Saint-Exupéry (kit), mais la rigueur de fond suit la démarche en 9 maillons.

**Piège de publication PDF (24/09/2026)** : un **gras qui englobe un italique** produit `***` et **casse le parseur de `publish_pdf_mdc.py`** — le contrôle qualité bloque et aucun fichier n'est produit. Écrire `**Le métier répond à une question :** *« … »*` et jamais `**… : *« … »***`. Le publieur `_publier_tout.py` du dossier CONTENU_MON_FISCALISTE signale désormais les `***` avant de tenter la génération.
