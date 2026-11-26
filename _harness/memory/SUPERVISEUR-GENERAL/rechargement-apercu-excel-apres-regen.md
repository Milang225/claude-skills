---
name: rechargement-apercu-excel-apres-regen
description: "Après régénération d'un PDF/XLSX déjà ouvert, forcer sa fermeture+réouverture dans Aperçu/Excel — sinon l'utilisateur voit l'ancien cache et croit que rien n'a changé."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9935bb39-b36c-45ab-b5cd-94351ca5fbe2
  modified: 2026-08-16T13:47:52.964Z
---

Quand je régénère un document (PDF via publish/xlsx_to_pdf, ou un .xlsx) qui est **déjà ouvert** dans Aperçu (Preview) ou Excel, l'application **garde l'ancienne version en cache** : le fichier sur le disque est à jour, mais la fenêtre montre l'ancien rendu. L'utilisateur ouvre, ne voit aucun changement, et doit redemander — ce qui l'agace fortement.

**Why :** l'utilisateur a dû répéter plusieurs fois « fais appel à la rédaction / je ne vois rien de nouveau » alors que le fichier était bien corrigé — le problème était le cache d'Aperçu, pas la production. Il déteste se répéter.

**How to apply :** après chaque republication d'un document susceptible d'être ouvert, **forcer le rechargement** via osascript (`mcp__Control_your_Mac__osascript`) : dans Aperçu, `close (documents whose name contains "…") saving no` puis `open` du fichier ; pour Excel, fermer sans enregistrer puis rouvrir. Le faire proactivement, sans attendre que l'utilisateur signale « rien de nouveau ». Voir [[supervision-redaction-avant-livraison]].
