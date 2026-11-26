# Harness MDC — la façon de travailler, pour un autre PC

Ce dossier contient tout ce qui, en plus des skills, fait travailler Claude « à la manière MDC ».

| Dossier | Contenu | Où il s'installe |
|---|---|---|
| `../` (racine du dépôt) | Les skills : `mdc` (et ses 23 modules), `coordination`, `dossier-audit`, `revision` | `~/.claude/skills` |
| `agents/` | Agent `auditeur-comptable` (relecture indépendante) | `~/.claude/agents` |
| `scheduled-tasks/` | Tâche `point-supervision-mdc-18h` | `~/.claude/scheduled-tasks` |
| `memory/` | Mémoires de Claude, une par projet (règles du Gérant, décisions, façons de faire) | `~/.claude/projects/<projet>/memory` |
| `claude-md/` | Consignes de projet (CLAUDE.md) du projet AUD-GLOBAL | à copier dans le projet voulu |
| `plateforme-mdc/` | Code de la Plateforme MDC et de son serveur MCP | voir plus bas |

## Installer sur Windows

```powershell
git clone -c core.symlinks=true https://github.com/Milang225/claude-skills.git H:\claudeskill
powershell -ExecutionPolicy Bypass -File H:\claudeskill\_harness\install.ps1 -Base "H:\MDC"
```

- Activez d'abord le **Mode développeur** de Windows (raccourcis des modules).
- `-Base` est le dossier où vous créerez vos projets. Pour retrouver la mémoire d'un projet, ouvrez Claude Code dans
  `H:\MDC\<NOM>`, avec le nom du dossier de `memory/` (ex. `H:\MDC\SUPERVISEUR-GENERAL`, `H:\MDC\CRM`, `H:\MDC\LMDC`).
- Si `%USERPROFILE%\.claude\skills` existe déjà, renommez-le avant de lancer le script.

## Installer sur Mac

```bash
git clone https://github.com/Milang225/claude-skills.git ~/.claude/skills
bash ~/.claude/skills/_harness/install.sh
```

## Ce qui vient tout seul

Les **plugins** (comptabilité, juridique, documents, ventes…) et les connecteurs claude.ai (Gmail, Agenda…) sont
liés au compte Claude : ils réapparaissent en se connectant avec le même compte.

## Étape manuelle : la Plateforme MDC

Le serveur MCP `plateforme-mdc` lit les documents dans `Documents/SUPERVISEUR GENERAL` et `Documents/DOSSIER CLIENTS`,
et ses accès (R2, messagerie) dans un `.env` et le trousseau, qui **ne sont pas** dans ce dépôt.
1. Copier `plateforme-mdc/` dans `Documents/SUPERVISEUR GENERAL/_SOURCES_REGISTRE/`.
2. Adapter les chemins `/Users/bilefilsseverin/...` des scripts au nouveau PC.
3. Recréer le `.env` à la main à partir des accès détenus par le Gérant.
4. Déclarer le serveur : `claude mcp add plateforme-mdc -s user -- python3 "<chemin>/mcp_plateforme_mdc.py"`.

## Ce qui n'est volontairement PAS dans le dépôt

- Identifiants, mots de passe, clés, adresses de serveur : `.private/`, `.env`, trousseau.
- 60 mémoires techniques (serveur, sécurité, accès, déploiement) écartées automatiquement parce qu'elles citent des
  accès ou des adresses. Elles restent sur le Mac d'origine, dans `~/.claude/projects/*/memory`.
- Les sauvegardes `.bak` et les journaux.
