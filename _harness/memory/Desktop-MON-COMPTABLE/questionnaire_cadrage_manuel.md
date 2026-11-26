---
name: questionnaire-cadrage-manuel
description: Questionnaire client générique pour rédiger tout manuel de procédures MDC (intake sur mesure)
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4113ea6b-b203-41aa-82c7-f4fc6bd3dd59
  modified: 2026-08-03T01:57:21.526Z
---

**Questionnaire de cadrage — élaboration du manuel de procédures** (MC-QUEST-MAN-2026-001), modèle GÉNÉRIQUE réutilisable pour TOUT client : `Documents/LIVRABLES AUDIT LMDC/00_MANUELS_PROCEDURES/QUESTIONNAIRE_CADRAGE_MANUEL_PROCEDURES_MDC.docx/.pdf/.md`. Le client remplit (colonne Réponse), MDC rédige ensuite son manuel sur mesure.

12 sections : 1 Identification/juridique · 2 Activité/modèle éco · 3 Régime fiscal & taille · 4 Approvisionnement/fournisseurs · 5 Logistique/livraison · 6 Stock · 7 Trésorerie/banque · 8 Personnel & social · 9 Comptabilité & outils · 10 Activité réglementée/ARTCI · 11 Organisation interne & attentes · 12 Pièces à joindre + observations libres + bloc signature.

**Why:** capitalise la méthode qui a produit le manuel FABELLASHOP (issu du mémo 6 points + note de conseil + synthèse réunion). Standardise l'intake pour tous les futurs manuels.
**How to apply:** envoyer le .docx au nouveau client → à réception, rédiger le manuel via le pipeline `publish_livrable_mdc.py`/`publish_pdf_mdc.py`. Gabarit de sortie = [[client-fabellashop]] (manuel éd.2, 11 parties + partie 8 obligations tous domaines).
