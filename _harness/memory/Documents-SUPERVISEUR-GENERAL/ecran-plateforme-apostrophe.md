---
name: ecran-plateforme-apostrophe
description: "11/11/2026 : une apostrophe mal échappée dans page.html a cassé tout le script de l'unité 1 pendant la journée ; contrôle de syntaxe ajouté aux tests"
metadata:
  type: feedback
---

Le 11/11/2026 à 02 h 59, l'ajout du bouton « Code par courriel » a introduit dans `page.html` une
apostrophe doublement échappée : `Revenir à l\\'application` au lieu de `l\'application`, à
l'intérieur d'un gabarit. Le navigateur refuse alors de lire **tout** le script de la page : l'écran
s'affiche, mais le nom du compte n'apparaît pas, la liste des clients reste vide et aucun bouton ne
répond. Le journal du serveur le montrait sans ambiguïté : la page était servie en 200, puis
**aucun appel `/api/...` ne suivait**, parce que le script n'avait jamais démarré.

**Why:** les contrôles ne lisaient que le Python. Un écran peut être entièrement mort alors que le
serveur, la base et les tests sont tous au vert — et personne ne le voit avant qu'un utilisateur
s'en plaigne.

**How to apply:** `tests_securite.py` extrait maintenant le script de `page.html` et le passe à
`node --check` à chaque passage (bloc « L'écran de la plateforme »). Toute modification de
`page.html`, surtout dans un gabarit avec des apostrophes, doit passer cette vérification avant
d'être mise en ligne. Et quand un utilisateur dit « rien ne marche » alors que le serveur va bien,
regarder d'abord si les appels `/api/` apparaissent dans le journal : leur absence désigne le script.

Voir [[code-connexion-par-courriel]] et [[serveur-sauvegardes-et-disque]].
