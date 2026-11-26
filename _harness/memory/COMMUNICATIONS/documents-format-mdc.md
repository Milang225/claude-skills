---
name: documents-format-mdc
description: "Tout document produit (PDF, Word) doit passer par le format de rédaction MDC, jamais un format maison"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1fdbe2c5-4839-460c-8278-5183ff40b936
  modified: 2026-11-20T01:21:10.684Z
---

Ne jamais produire un document (PDF, Word, fiche, tableau) avec une mise en forme improvisée. Toujours charger le skill `mdc`, module `redaction`, et publier via ses générateurs brandés (logo, bandeau, pied légal, contrôle qualité bloquant). Pour un usage interne, le client est « Usage interne » ; la source Markdown se garde dans `_sources/`.

**Why:** le 20/11/2026, j'ai sorti une fiche « prise de parole » en PDF reportlab fait main ; l'utilisateur l'a rejetée : « tu ne produis jamais un document sans mon format ou mon skill rédaction ».

**How to apply:** dès qu'un fichier livrable est demandé, même une fiche personnelle d'une page, passer par `mdc` → `redaction` avant tout rendu. Version remplacée préfixée `OBSOLETE_`.
