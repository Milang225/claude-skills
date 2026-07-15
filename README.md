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
