---
name: livrable-a-envoyer-sur-bureau
description: "Quand un livrable est validé pour envoi, le poser directement sur le Bureau avec un nom simple et dire où il est en clair"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4f12d7c3-daf9-49e4-81bb-82b5adf6c282
  modified: 2026-10-01T23:20:33.629Z
---

Le gérant ne retrouve pas les fichiers validés : les chemins du type `Documents/DOSSIER CLIENTS/<client>/MC-…pdf` ne lui parlent pas, et `open -R` ne suffit pas (la fenêtre Finder peut rester derrière). Plainte du 01/10/2026 (lettre d'excuses AMOC) : « quand on valide un fichier, je ne sais pas où le trouver ».

**Why:** il doit souvent joindre lui-même le PDF dans Gmail (le brouillon via l'outil Gmail ne peut pas joindre un fichier de façon fiable, et Claude in Chrome n'est pas toujours connecté). S'il ne trouve pas le fichier, l'envoi est bloqué.

**How to apply:** dès qu'un livrable est validé pour envoi, en plus de l'original rangé et de la copie [[copies-livrables-bureau]], copier le PDF **directement sur le Bureau** avec un nom court et lisible (ex. `LETTRE_EXCUSES_AMOC.pdf`), puis afficher le Finder au premier plan (`osascript` : activate + reveal). Dans la réponse, indiquer l'emplacement en mots simples (« sur votre Bureau, fichier X »), pas seulement un chemin technique. Pour Gmail : Trombone → Bureau → fichier. Voir [[preparation-mails]], [[gmail-drafts-sans-signature]].
