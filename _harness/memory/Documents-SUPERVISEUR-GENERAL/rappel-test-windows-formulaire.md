---
name: rappel-test-windows-formulaire
description: EN ATTENTE au 22/10/2026 — le gérant fait tester l'installation Windows du formulaire par un collaborateur et doit rapporter ce qu'affiche la vérification
metadata:
  type: project
---

Le 22/10/2026, le gérant a dit : « je fais tester l'installation par un collaborateur sur son poste Windows et je te rapporte ce qu'affiche la vérification ». Les fichiers .bat n'ont jamais tourné sur un vrai Windows ; seule la disposition du paquet a été testée sur le Mac.

**Why:** première vraie validation du paquet FORMULAIRE_PROFIL_WINDOWS ([[formulaire-profil-entreprise]]).

**How to apply:** à la prochaine session, demander le retour s'il n'est pas venu. Points à surveiller : Python ouvert par le Microsoft Store, antivirus sur les .bat, Documents redirigé vers OneDrive, proxy qui bloque pip ou npm. Après tout changement du modèle, refaire le paquet (construire_paquet_windows.py) avant de le remettre.

- 22/10/2026 soir : paquet FORMULAIRE_PROFIL_WINDOWS_2026-10-22.zip (PROFIL_ENTREPRISE_2026/) reconstruit avec tous les classeurs en formulaire, logo, import Excel ; installer_windows.bat installe maintenant openpyxl aussi ; LISEZ-MOI contient la liste des tests a à i à dérouler sur un client d'essai. Paquet vérifié seul sur Mac (copie dézippée, 10 classeurs servis) ; les .bat ne sont toujours pas passés sur un vrai Windows. Le gérant remet le zip aux collaborateurs lui-même.
