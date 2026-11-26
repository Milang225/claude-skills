---
name: registre-documents-valides
description: Où sont rangés les documents de méthode validés — registre SUPERVISEUR GENERAL/00_REGISTRE_DES_DOCUMENTS_VALIDES.xlsx, à mettre à jour à chaque nouveau document
metadata:
  type: project
---
Le gérant a demandé (12/10/2026) où sont enregistrés tous les documents qu'il valide.

**Règle :**
- Tout document de méthode est rangé dans `Documents/SUPERVISEUR GENERAL/<DOSSIER_THÉMATIQUE>/`, avec sa source modifiable dans `_SOURCES`.
- Le registre est `SUPERVISEUR GENERAL/00_REGISTRE_DES_DOCUMENTS_VALIDES.xlsx` : famille, document, référence, date, statut (Validé, En cours de validation, Remplacé), dossier, fichiers.
- Il est produit par `SUPERVISEUR GENERAL/_SOURCES_REGISTRE/build_registre.py` ; ajouter une ligne à DOCS à chaque nouveau document, et passer le statut à « Validé » quand le gérant valide.
- Les documents propres à un client restent dans `DOSSIER CLIENTS/<client>/`.

**How to apply :** à chaque création ou validation d'un document de méthode, mettre le registre à jour et le dire au gérant.

**Décisions du 12/10/2026 pour le suivi complet :**
- L'Agence tient la comptabilité du client : saisie du 5 au 10, arrêté le 10, clôture et états financiers établis par l'Agence, avec la signature d'un expert-comptable inscrit si la loi l'exige.
- Les DEE ont leur propre section dans la procédure : 12 situations types, envoi le 12, réponse sous 48 h, et un onglet DEE dans le classeur.
- Les attentes de l'Agence vis-à-vis du client figurent dans le Guide de collaboration MC-GUIDE-CLIENT-2026-002, mise à jour de l'ancien guide d'août conservé dans les archives (kit de suivi mensuel).
