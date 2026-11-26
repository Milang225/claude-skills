# Skills — La Maison de la Conformité SARL (MDC)

Dépôt **privé** de sauvegarde des compétences (skills) Claude Code du comptable-fiscaliste MDC.
Tout en FCFA · droit ivoirien / OHADA · secret professionnel.

## Contenu

### `mdc-expert/` — Expert global MDC
Compétence unifiée : comptabilité SYSCOHADA/OHADA (Côte d'Ivoire / UEMOA), analyse de relevés
bancaires, audit global, révision/certification, **télédéclaration fiscale e-impôts (EDI/EFI)**,
production des documents commerciaux MDC, administration serveur.

- `SKILL.md` — corps de la compétence (30 sections).
- `reference/` — fiches de doctrine sourcées (synoptique DGI, TVA/TOB/TSE, impôts sur les
  bénéfices, SYSCOHADA, **déclarations e-impôts EDI/EFI**, calendrier des obligations, etc.).
- `scripts/` — générateurs de livrables (Word/PDF à en-tête MDC), utilitaires.
- `INDEX.md` (dans `reference/`) — point d'entrée à lire en début de session.

### `monteur-video/` — Monteur vidéo de la chaîne AVEC MON FISCALISTE
Montage automatique d'un rush en vidéo YouTube 4K + Short : coupe des bafouillages, regard hors objectif
couvert (Apple Vision), motion design aux couleurs de la marque (Chrome headless), transitions, texte derrière
le personnage, son et export recommandés YouTube. Piloté par un `projet.json` par vidéo.

- `SKILL.md` — méthode complète · `reference/` — catalogue des scènes, format du projet, charte, audio,
  export, dépannage · `scripts/` — moteur (`monteur.py`, `motion/`, `tools/`) · `exemples/ep01_projet.json`.

## Installer toute la façon de travailler sur un autre PC

Voir **[`_harness/README.md`](_harness/README.md)** : skills, agent, tâche planifiée, mémoires, consignes et
Plateforme MDC, avec les scripts `install.ps1` (Windows) et `install.sh` (Mac).

## Sécurité — ne jamais versionner

Les identifiants serveur (VPS Contabo : IP, mot de passe root, VNC) sont **déportés hors dépôt**
dans `mdc-expert/.private/VPS_CONTABO.md`, exclu par `.gitignore`. `SKILL.md §5` n'en contient
qu'un **renvoi**. Sur un nouveau poste, recréer ce fichier localement à partir des identifiants
détenus par le gérant — ne jamais le committer.

Le `.gitignore` exclut : `**/.private/`, `*.bak`, `*.env`, `*.secret`, caches Python, fichiers OS.

## Restauration sur un nouveau poste

```bash
git clone <url-du-depot-prive> ~/.claude/skills
# puis recréer manuellement ~/.claude/skills/mdc-expert/.private/VPS_CONTABO.md (identifiants serveur)
```

## Organisation actuelle

Un seul skill `mdc/` ; les 19 anciens skills sont des modules dans `mdc/modules/` (MODULE.md au lieu de SKILL.md), liens de compatibilité à la racine. État courant : `mdc/etat/rafraichir.py`.
