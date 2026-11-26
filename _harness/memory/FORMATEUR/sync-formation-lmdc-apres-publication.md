---
name: sync-formation-lmdc-apres-publication
description: "Après chaque publication d'un livrable MDC, synchroniser les deux dossiers FORMATION LMDC, dans Documents et sur le Bureau"
metadata:
  type: feedback
---

**Après chaque publication d'un livrable, exécuter la synchronisation des deux dossiers `FORMATION LMDC`** — celui de `~/Documents` et celui du Bureau. Consigne donnée par le gérant en septembre 2026.

```bash
~/.claude/skills/mdc-expert/scripts/sync_formation_lmdc.sh
```

Le script reconstruit `PDF`, `WORD`, `MD` et `00_TEXTES_OFFICIELS` depuis la bibliothèque de travail `~/Documents/ARCHIVES DOCUMENTS/FORMATIONS MDC`, **préserve le dossier `00_NOUVEAUTES_2026`** et ses copies par format, puis recopie l'ensemble sur le Bureau.

**Why:** le gérant consulte et remet ses supports depuis ces deux dossiers, pas depuis la bibliothèque de travail. Sans synchronisation, ils divergent dès la première publication et il remet une version périmée à un client. Il a déjà perdu du temps à chercher des modules récents absents du Bureau.

**How to apply:** la bibliothèque de travail reste `ARCHIVES DOCUMENTS/FORMATIONS MDC` — c'est là que publient les scripts `publish_livrable_mdc.py` et `publish_pdf_mdc.py`. Les deux `FORMATION LMDC` en sont des **copies rangées par format**, jamais la cible directe d'une publication. Les modules récents sont dupliqués dans `00_NOUVEAUTES_2026` à la racine, parce que l'arborescence thématique les enfouit trop profond pour qu'il les retrouve. Y ajouter chaque nouveau module publié. Voir [[textes-officiels-dgi-locaux]] pour le dossier `00_TEXTES_OFFICIELS`.
