---
name: enregistrement-automatique-atelier
description: 18/11 — l'atelier enregistre seul 2,5 s après la frappe, avec témoin et avertissement avant de quitter
metadata:
  type: project
---

Depuis le 18/11/2026, l'atelier n'attend plus qu'on pense à cliquer : toute saisie dans un volet part au serveur 2,5 secondes après la dernière frappe. Un témoin dans la barre dit « enregistré à 16 h 42 » en vert, ou « PAS ENREGISTRÉ » en rouge avec la raison, et la page refuse de se fermer sur du travail non parti. En ouvrant un dossier, la personne lit « vous l'aviez laissé le 17/11 à 21 h 55 », avec qui a enregistré en dernier.

En cas de panne d'internet, ce qui ne part pas est gardé dans le navigateur (localStorage, clés `mdc_atelier_attente_*`), un bandeau le dit, et tout repart seul au retour du réseau — testé par un contrôle node dans tests_atelier.py. Limite à dire au gérant : cela tient à l'ordinateur et au navigateur utilisés.

**Why :** le gérant ne veut pas qu'un collaborateur puisse perdre une journée parce qu'il a oublié un bouton ; voir [[atelier-saisies-ecrasees]].

**How to apply :** le bouton Enregistrer reste pour qui préfère. L'onglet des pièces a son propre enregistrement automatique. En cas de refus du garde-fou, aucune fenêtre ne surgit pendant la frappe : le témoin passe au rouge et la question n'est posée qu'au clic volontaire.
