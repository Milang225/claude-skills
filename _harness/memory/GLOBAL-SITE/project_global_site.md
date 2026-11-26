---
name: Project GLOBAL SITE — module bulletins de paie Global Connectors
description: Refonte du module bulletins-paie de globalconnectorsci.net inspirée du panel admin MDC, dans /Users/bilefilsseverin/GLOBAL SITE/
type: project
originSessionId: eb39c124-4505-4378-8356-3f0e87c90379
---
**Objectif** : dupliquer le module `https://globalconnectorsci.net/espace-client/bulletins-paie` (Global Connectors / Compta 360 GC) en améliorant le front, en s'inspirant de l'admin MDC (`https://lamaisondelaconformitesarl.net/admin`).

**Why:** L'utilisateur trouve le front actuel de Global Connectors "nul". Il veut le même type de portail que le panel admin MDC qu'il a déjà construit, appliqué au cas Global Connectors (espace client salarié pour récupérer ses bulletins de paie).

**How to apply:**
- Travailler dans `/Users/bilefilsseverin/GLOBAL SITE/` (vide au démarrage)
- Réutiliser la stack et le style du panel admin MDC (cf. mémoire `reference_mdc_infra`)
- Cible de déploiement : VPS Contabo, sous-dossier ou sous-domaine de globalconnectorsci.net
- Calculs paie spécifiques Côte d'Ivoire : ITS, CNPS (régime général + accidents travail + retraite), CMU, FDFP, taxes employeur
- Multi-entreprises (Global Connectors a plusieurs clients employeurs)
