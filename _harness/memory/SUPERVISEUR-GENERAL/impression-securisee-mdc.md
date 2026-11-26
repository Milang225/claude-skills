---
name: impression-securisee-mdc
description: Dispositif d'impression traçable des supports internes (20/09/2026) — script secure_print_mdc.py, ce qu'il fait et ce qu'il ne peut pas faire.
metadata:
  type: project
---

Outil : `~/.claude/skills/mdc-expert/scripts/secure_print_mdc.py`. Produit des **exemplaires nominatifs** d'un PDF : fond de sécurité pantographe (hachures fines 0,12 pt qui s'effacent à la copie + points 0,50 pt qui survivent, couverture d'encre égalisée à 10 % pour que le mot reste invisible à l'œil), filigrane nominatif, bandeau de traçabilité, micro-marquage en marge, QR de vérification, registre CSV. Mode `--calibrage` : planche de six réglages à photocopier pour choisir celui qui marche sur le copieur de la maison.

**Ce qui est impossible, et qui a été dit au gérant :** empêcher un scan ou une photocopie, et déclencher une alerte automatique lors d'une copie. Le papier ne communique pas. La protection repose sur l'**imputabilité** (retrouver de quel exemplaire vient une fuite), pas sur l'empêchement. Une alerte n'est possible que si quelqu'un **scanne le QR** : cela suppose une page de vérification en ligne qui journalise — proposée, **pas encore créée** (elle publierait des noms de collaborateurs, décision du gérant).

Mesuré en simulation : à 300 dpi en mode texte, le mot ressort (28,8 % de noir contre 0 % pour le fond) ; à 600 dpi le fond domine et la copie ressort grisée — dans les deux cas la copie diffère visiblement de l'original.

**Why :** le gérant veut protéger la méthode maison que ses collaborateurs emportent sur le terrain.
**How to apply :** un tirage par personne, registre tenu par la coordination, remise contre signature — note de service **MC-NS-2026-005**. Livrables imprimables dans `KIT_DETECTION_TERRAIN/_IMPRESSION/`. Voir [[kit-detection-terrain]].
