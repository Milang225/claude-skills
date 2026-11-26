---
name: profil-conformite-client
description: "Projet « profil de conformité » par client (méthode de CA, comptes, sorties, obligations) servant à dériver le cahier des charges de chaque département"
metadata:
  node_type: memory
  type: project
  originSessionId: dd8fc8e9-ccec-443d-acd4-6dc42e4d84e2
  modified: 2026-10-02T00:54:27.672Z
---

Le gérant a lancé ce projet le 01/10/2026. Chaque client reçoit une fiche profil de conformité en 6 blocs :
1. identité et régime (régime actuel / régime théorique) ;
2. **méthode de calcul du CA**, avec un code M1 à M7 et le triangle CA déclaré / facturé / bancaire ;
3. **cartographie des comptes**, à la fois les comptes de trésorerie (banque, mobile money, caisses) et les comptes comptables SYSCOHADA utilisés ;
4. profil des sorties et du mode de règlement ;
5. obligations déclaratives ;
6. points ouverts.

On en dérive un cahier des charges par département (voir [[departements-mdc]]).

Pilote livré le 02/10/2026 sur 4 dossiers : AVE MARIA (M2), Collège St Exupéry (M5), FABELLASHOP (M1) et SCI 3KAS (M4). Il comprend 4 profils PDF, 5 cahiers des charges PDF et le classeur maître `PROFILS_CONFORMITE_TOUS_DOSSIERS_2026-10-02.xlsx`, le tout dans `SUPERVISEUR GENERAL/PROFILS_CONFORMITE/`. Chaque profil PDF est aussi copié dans le dossier du client.

**Générateur :** `PROFILS_CONFORMITE/_SOURCES/build_profils.py` produit tout depuis `_SOURCES/json/*.json`, selon le schéma `_SOURCES/SCHEMA_PROFIL.md`. Les tâches des départements sont dérivées automatiquement du profil. Les PDF passent par `publish_pdf_mdc.py`.

**Déploiement terminé le 02/10/2026 : 54 profils, une entité juridique = un profil.**

Fusions de dossiers (une seule entité) :
- LBTECH dans LIGHT & BRIGHT ;
- SAPHIR dans BALOU ;
- A PAYER DE LERO dans LERO ;
- MABEK et MABEK 2 ;
- ACCES MATERIEL et ACCES MATERIEL MEDICAL ;
- les deux dossiers MFD.

Scissions (SCI et SARL) : OUATTARA, FOUSSENI, DOUAN. FAMILLE KAMARA est scindée en deux contribuables. DOSSIERS IMMOBILIER renvoie aux biens KAMARA.

Volume produit : 3 343 tâches, 695 points ouverts dont 373 P1, 180 stratégies applicables.

**Commande :** `python3 build_profils.py --ranger` régénère tout et range les PDF dans chaque dossier client. `nom_court` dans le JSON sert de libellé.

**Bloc ajouté le 02/10/2026 à la demande du gérant : `vigilance_optimisation`.** Il porte la qualification revendeur / intermédiaire selon la grille des 12 questions, les signaux à repérer dans les relevés, les points d'attention, les stratégies légales S1 à S7 avec leurs écritures et leur dispositif, et les lignes rouges.
- **Doctrine de référence :** MC-DOC-CA-2026-001, `_SOURCES/md/DOCTRINE_CA_REVENDEURS_INTERMEDIAIRES.md`. Elle s'appuie sur :
  - CGI art. 71 bis, 77 et 342 ;
  - LPF art. 25, 26 et 165 (abus de droit majoré de 150 %, rescrit avec silence de 6 mois).
- **Pourquoi le gérant y tient :** la plupart des clients sont des revendeurs ou des intermédiaires. La TEE et l'impôt des microentreprises frappent le CA, pas la marge, donc les collaborateurs doivent savoir détecter la nature réelle des flux.
- **Retenue sur loyers :** 12 %, portée à 15 % si le propriétaire est une personne morale (CGI art. 168 et 169).
- **Centre de gestion agréé :** l'adhésion réduit la TEE de moitié (CGI art. 80) et ramène l'impôt des microentreprises de 6 % à 4 % (art. 71 bis). Il faut adhérer au plus tard le 31/01, ou dans les 30 jours de la DFE, et rester adhérent 3 ans.

**Why:** que chaque département sache exactement comment le CA est calculé et quels comptes sont utilisés pour chaque client.
**How to apply:** les champs inconnus sont marqués « À collecter » et deviennent des tâches. Ne jamais écrire IFU (voir [[pas-d-ifu-dans-les-livrables]]).
