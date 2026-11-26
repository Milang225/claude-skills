---
name: rapprochements-atelier
description: 23/11 — dix rapprochements nommés qui tranchent la 2e question de l'audit, sous l'étude comparée
metadata:
  type: project
---

`rapprochements.py` répond à la deuxième question de l'audit : ce que l'entreprise déclare correspond-il à la réalité ? Dix rapprochements (R01 à R10), par exercice : déclaré, constaté, écart, état (Concordant sous 5 %, À expliquer, Impossible faute de source) et conclusion.

Les deux chiffres sont lus dans l'étude comparée (`etude_comparee.lignes`) : aucune ressaisie. La conclusion reprend le vocabulaire des relevés (`categorisation.CONCLUSIONS`) et seules « Non justifié après réponse » et « Sans réponse dans le délai » deviennent une exposition retenue. Chaque rapprochement nomme le livrable qu'il bloque ; `a_demander()` ignore les exercices dont les deux sources sont vides.

**Why :** l'atelier collectait tout et ne concluait rien — d'où des dossiers instruits à fond et des livrables de restitution à 0 %.

**How to apply :** l'écran est sous l'onglet Étude comparée, route `/api/rapprochements`. Voir l'aperçu global validé par le gérant (artifact « Le fil de conformité ») : restent à construire la grille des obligations qui se remplit seule, l'Indice en trajectoire et l'avancement par livrable.
