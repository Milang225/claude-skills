---
name: ecosysteme-systeme-comptable
description: Kit d'implantation d'un système comptable chez les clients (parcours IMPLANTATION) — doctrine 9 briques, 12 contrôles, générateurs de manuel de procédures et de calendrier des obligations.
metadata:
  type: project
---

Créé le 21/09/2026 : l'écosystème qui permet aux collaborateurs d'**installer** un système comptable chez une entreprise cliente, puis d'en **rédiger le manuel de procédures**. C'est le maillon qui manquait entre l'audit (qui constate) et le suivi (qui surveille) — ajouté au [[machine-lmdc-procedure]] comme « parcours 2 bis — IMPLANTATION » (6 phases, 6 semaines, une porte de sortie par phase).

Emplacements : `~/SUPERVISEUR GENERAL/ECOSYSTEME_SYSTEME_COMPTABLE/` (+ archive .zip pour transmission) et copie dans `BASE DOCUMENTAIRE LMDC/06_PROCEDURES/KIT_SYSTEME_COMPTABLE` (règle [[copie-systematique-base-documentaire]]).

**Le principe directeur** : un système comptable est efficace lorsque l'audit n'y découvre rien que l'entreprise ne sache déjà. La doctrine tient en 9 briques, 12 contrôles clés tracés (« un contrôle non tracé est réputé non fait »), 5 conditions de piste d'audit et 8 signes de défaillance.

**Les deux générateurs** (`4_MANUEL_DE_PROCEDURES/`) partagent UN fichier de paramètres JSON par client : `generer_manuel.py` (manuel en 12 chapitres, + `--publish` pour PDF/DOCX brandés) et `generer_calendrier.py` (inventaire déclaratif + échéancier XLSX). Ils déduisent du régime/secteur/service gestionnaire/effectif : les impôts dus, le jour d'échéance (10/15/20), les échéances à dates réelles, le seuil de sortie de régime et l'alerte à 80 %. Les classeurs génériques se régénèrent par `_SOURCES/build_outils.py`.

**Why:** capitaliser une prestation vendable en tant que telle, et faire en sorte que deux collaborateurs différents produisent le même standard.

**How to apply:** pour toute mission d'implantation — diagnostic AVANT le manuel, générateur PUIS personnalisation, passage obligatoire par [[supervision-redaction-avant-livraison]], clôture seulement après un arrêté mensuel fait par le client. Obligatoire pour les missions engagées à compter du 05/10/2026 (note de service MC-NS-2026-006) ; séance de prise en main interne prévue le 24/09/2026.
