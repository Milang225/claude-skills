---
name: traitement-automatique-des-releves
description: "Le traitement des opérations bancaires se fait à l'import, sans saisie ligne par ligne"
metadata:
  node_type: memory
  type: project
  originSessionId: 7d1e2fa5-fd41-43ee-b04b-bc1d053b28e5
  modified: 2026-11-24T09:36:32.292Z
---

Depuis le 24/11/2026, l'atelier qualifie les opérations lui-même au moment de l'import du relevé : le libellé de la banque donne la catégorie, la qualité du bénéficiaire et le mode de règlement. Le collaborateur ne saisit plus rien ; il confirme. Le vocabulaire des banques de la place est dans `MOTS` et `MODES_MOTS` de `categorisation.py` (atelier).

**Why:** le gérant a rejeté la version où l'import n'était qu'un import et la qualification restait manuelle — « le traitement, pas l'import ». Mesuré sur les relevés LBTECH : 47 opérations sur 71 qualifiées avant, 71 sur 71 après.

**How to apply:** tout ce que la machine remplit reste marqué « proposé » jusqu'à confirmation, et reste modifiable ligne par ligne ; ce qui n'a pas été qualifié est rendu en clair avec les libellés restants. Le bouton « Reprendre le traitement » ne touche que les champs vides. Pour enrichir le vocabulaire, ajouter un motif dans `MOTS` et un contrôle dans `tests_atelier.py`. Voir [[rapprochements-atelier]], [[lecture-releves-pdf]], [[plusieurs-releves-registre]].
