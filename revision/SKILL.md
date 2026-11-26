---
name: revision
description: >
  Révision et récapitulatif des dossiers clients MDC (La Maison de la Conformité). Connaît tous les dossiers de
  ~/Documents/DOSSIER CLIENTS et le classeur SUIVI_DES_DOSSIERS_MDC.xlsx (créations, travaux préliminaires,
  diagnostics, contrôles de tenue). Produit un récap global (statut actif / en veille / dormant, dernier
  mouvement, étape de suivi, pièces de cadrage manquantes, points d'attention) ou une fiche détaillée d'un
  dossier. Déclenche dès que l'utilisateur demande un récap, une revue, un point, un état ou une révision des
  dossiers, « où on en est », « fais-moi le point sur <client> », « quels dossiers sont en retard / dormants ».
---

# Révision des dossiers MDC

Skill en **lecture seule** : il ne modifie, ne déplace et ne supprime aucun fichier client. Il complète le
skill `mdc` (qui produit les livrables) ; pour agir sur un dossier après la revue, passer au module `mdc` concerné.

## Sources

| Source | Contenu |
|---|---|
| `~/Documents/DOSSIER CLIENTS/<CLIENT>` | Pièces et livrables de chaque client (les fichiers « OBSOLETE » sont comptés à part) |
| `~/Documents/SUIVI CLIENTS/SUIVI_DES_DOSSIERS_MDC.xlsx` | Onglets Créations, Travaux préliminaires, Diagnostics, Contrôles de tenue (CT01…) |
| `~/Documents/SUPERVISEUR GENERAL/00_REGISTRE_DES_DOCUMENTS_VALIDES.xlsx` | Documents de méthode validés (à lire si la question porte sur la méthode) |
| Outils `plateforme-mdc` (`synthese`, `lister_documents`, `trouver_fichiers`) | État de la plateforme, si le serveur est lancé |

## Récap global (« fais-moi le récap des dossiers »)

1. Lancer :
   ```bash
   python3 ~/.claude/skills/revision/scripts/recap.py
   ```
   Le script écrit `~/REVISION/RECAP_DOSSIERS_<AAAA-MM-JJ>.md` et affiche son chemin.
2. Lire ce fichier, puis répondre à l'utilisateur avec une synthèse courte, en français, structurée ainsi :
   - **Vue d'ensemble** : nombre de dossiers actifs (≤ 30 jours), en veille (31–90 j), dormants (> 90 j).
   - **Ce qui a bougé cette semaine** : dossiers modifiés dans les 7 derniers jours et leur dernier document.
   - **Priorités** : dossiers où le suivi indique une prochaine étape, un Indice MDC critique, beaucoup de
     contrôles de tenue en « Manque », ou des pièces de cadrage absentes (profil, note méthodologique,
     proposition financière, contrat).
   - **À harmoniser** : entreprises inscrites au suivi sans dossier à leur nom, dossiers en veille depuis
     longtemps.
3. Donner le lien vers le fichier complet. Ne pas recopier tout le tableau dans la réponse.

## Fiche d'un dossier (« fais-moi le point sur TIM 7 »)

1. Lancer :
   ```bash
   python3 ~/.claude/skills/revision/scripts/recap.py --client "TIM 7"
   ```
   (correspondance souple : accents, casse, SARL/SCI/SA ignorés).
2. Compléter en **lisant les documents récents clés** (fiche de tâches, profil de conformité, dernier rapport,
   note d'avancement) avant de conclure — ne rien supposer à partir des seuls noms de fichiers.
3. Répondre : situation, ce qui a été fait (dates), ce qui reste à faire (prochaine étape du suivi,
   contrôles en « Manque », pièces manquantes), et qui doit agir.

## Règles

- Tout en FCFA, droit ivoirien / OHADA, secret professionnel. Identifiant : NCC.
- Aucun montant client ni honoraire dans un récap destiné aux collaborateurs.
- Le statut « actif / en veille » reflète la date du dernier fichier, pas l'état contractuel : le signaler
  si la conclusion en dépend.
- Les « pièces de cadrage non trouvées » sont déduites des noms de fichiers ; les vérifier avant de les
  réclamer au client.
- Variantes de noms entre le classeur et les dossiers : compléter `ALIAS` dans `scripts/recap.py`.
- Dossiers ignorés (modèles, essais) : `IGN_DIRS` dans `scripts/recap.py`.
