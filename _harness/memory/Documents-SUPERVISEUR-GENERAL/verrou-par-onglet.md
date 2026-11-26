---
name: verrou-par-onglet
description: 23/11 — deux personnes travaillent sur le même dossier si elles sont sur deux onglets différents
metadata:
  type: project
---

Règle posée par le gérant le 23/11/2026 : deux collaborateurs doivent pouvoir travailler en même temps sur le même client ; seule la présence de deux personnes sur le **même onglet** est un problème. Le verrou de l'atelier porte donc sur le couple dossier + onglet, plus sur le dossier entier.

Le bandeau du dossier dit qui est sur quel onglet, chaque onglet occupé porte un trait ambre, et quitter le dossier lâche tous ses onglets. `acces.py` : `prendre/detenteur/liberer(..., onglet)` et `occupants(dossier)`.

**Why :** l'ancien verrou par dossier bloquait tout le monde dès qu'une personne l'ouvrait.

**How to apply :** le signalement reste indicatif, il n'empêche pas d'écrire — c'est le garde-fou et l'historique qui protègent les données (voir [[atelier-saisies-ecrasees]] et [[enregistrement-automatique-atelier]]).
