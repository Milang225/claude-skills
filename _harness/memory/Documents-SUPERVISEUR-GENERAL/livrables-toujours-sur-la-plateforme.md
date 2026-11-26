---
name: livrables-toujours-sur-la-plateforme
description: RÈGLE — tout document produit pour le gérant doit être enregistré dans un dossier suivi par la plateforme (localhost:8765), jamais seulement dans le scratchpad, le Bureau ou Téléchargements
metadata:
  type: feedback
---
Le gérant veut que **chaque document produit pendant nos échanges arrive directement sur sa plateforme** (demande du 15/10/2026).

La plateforme ([[production-par-jour-et-validation]]) indexe automatiquement, en 15 secondes environ, tout fichier pdf, docx, xlsx, pptx ou html enregistré dans :
- `Documents/DOSSIER CLIENTS/<client>/…` (documents d'un client) ;
- `Documents/SUPERVISEUR GENERAL/…` (méthode MDC, guides, procédures, modèles) ;
- `Documents/FORMATION LMDC/…` (formations) ;
- `Documents/DOCUMENTS_RECUS_PAR_MAIL/…` (pièces reçues).
Les dossiers `_OBSOLETE`, `_SOURCES*`, `TRANSMISSION_*`, `PIECES_RECUES`, `MES_LIVRABLES`, `MES_MODELES` et le scratchpad ne sont PAS indexés.

**Why:** il consulte, valide et range tout depuis la plateforme (Mac et iPhone) ; un document hors de ces dossiers est invisible pour lui.
**How to apply:** publier toujours le livrable final (PDF et/ou Word, Excel) dans le bon dossier client ou dans SUPERVISEUR GENERAL, jamais seulement dans le scratchpad ; un document sans client va dans `SUPERVISEUR GENERAL/<thème>/`. Il apparaît alors dans « 📥 À ranger » ; le dire au gérant en une ligne. Ne pas modifier le code de la plateforme sans demande expresse (consigne du 15/10 : « ne touche plus à rien »).
