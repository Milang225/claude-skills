---
name: plusieurs-releves-registre
description: 23/11 — plusieurs relevés par dossier, registre avec retrait ciblé et carte des mois manquants
metadata:
  type: project
---

L'onglet Relevés accepte plusieurs fichiers d'un coup, lus l'un après l'autre. Chaque opération porte le numéro du relevé qui l'a apportée (`o["releve"]`), ce qui permet `CAT.retirer_import(rep, ref)` : seules les opérations de ce relevé partent. `CAT.registre(rep)` donne une ligne par relevé (banque, exercices, période, opérations présentes, entrées, sorties) et `CAT.couverture(rep)` la carte des mois servis, vides ou non échus. Filtre par banque à côté du filtre par exercice.

**Why :** un dossier se traite sur plusieurs exercices et plusieurs banques ; sans registre, on ne savait ni ce qui avait été chargé ni ce qui manquait.

**How to apply :** les opérations importées avant le 23/11 n'ont pas de numéro — elles apparaissent sous « Opérations importées avant le suivi des relevés », non retirables, et leur import d'origine s'affiche à 0 pour ne pas les compter deux fois. **Ne jamais réimporter un même fichier en changeant le nom de la banque** : la clé anti-doublon comprend le compte, les opérations seraient dupliquées. Voir [[rapprochements-atelier]].
