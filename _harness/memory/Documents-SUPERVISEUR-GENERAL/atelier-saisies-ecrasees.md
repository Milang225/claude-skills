---
name: atelier-saisies-ecrasees
description: 17/11 — l'atelier remplaçait le dossier par ce que montrait l'écran ; garde-fou, complétion, états précédents
metadata:
  type: project
---

Le 17/11/2026 à 16 h 49, un enregistrement parti d'une page presque vide a écrasé la saisie de LBTECH : 1 320 valeurs effacées sur 2 466, Indice de 29 à 0. Rien n'était perdu — chaque écriture range l'état précédent dans `atelier_journal` — et le dossier a été rétabli le soir même.

Cause : `lire()` reconstruisait tout le dossier depuis le DOM, et `/api/enregistrer` le remplaçait entièrement. Un volet jamais affiché partait vide.

**Why :** la base enregistre parfaitement ; c'est l'écrasement qui faisait croire que « rien ne s'enregistre ».

L'onglet « Pièces du client » gardait les statuts en mémoire jusqu'au clic sur Enregistrer : changer d'onglet les perdait sans un mot. Depuis le 18/11, chaque statut part de lui-même et le message donne l'heure d'arrivée au serveur.

**How to apply :** trois protections posées — refus serveur d'un enregistrement qui vide (confirmation possible), enregistrement qui complète le dossier chargé (`CHARGE`), et bouton « États précédents » (Direction et Superviseur). Un état se désigne par son numéro de journal, jamais par l'heure : deux enregistrements tombent dans la même seconde. Voir [[fonctions-nees-des-pannes]] et [[audit-lbtech-v1]].
