---
name: qui-recoit-quoi
description: >
  CARTOGRAPHIE DE DIFFUSION des documents MDC — répond à deux questions : « quel document part à qui ? » et « ce document est-il encore vrai ? ». Inventorie les documents d'un dossier, d'un client ou d'une session, dit pour chacun QUI le reçoit, QUAND et dans QUEL ORDRE, distingue ce qui ne sort jamais de l'agence, puis débusque les documents devenus faux — personne qui a quitté l'agence, régime ou identité modifiés, chiffre divergent entre deux livrables, exposition périmée — en signalant lesquels sont DÉJÀ CHEZ LES CLIENTS et doivent y être corrigés. Produit un bordereau de diffusion. Déclenche-le quand l'utilisateur dit : « je suis perdu dans les documents », « quel document sera envoyé à qui », « qui reçoit quoi », « fais le point des documents », « est-ce encore à jour » ; ou dès qu'un changement survient — « X ne fait plus partie de l'équipe », « le régime a changé » — car il faut mesurer quels écrits deviennent faux. Utilise-le aussi de toi-même quand une session a produit plus de trois documents.
---

> ## ⚖️ CHARTE MDC 2026 — PRIME SUR TOUT LE RESTE DE CE SKILL (en vigueur depuis le 11/10/2026)
> Source : dossier de conception `/Users/bilefilsseverin/LA CONFORMITE LMDC/` (Plan directeur, Méthode de l'Indice MDC, Place dans l'écosystème réglementé, Mission : gagner le contrôle, Parcours types, modèles).
> 1. **Identité.** MDC est un cabinet de conseil et d'assistance en conformité fiscale et sociale. Ligne d'identité de tout document : « Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social ». Signature : « Préparer · Assister · Défendre ». Ne plus jamais écrire « Agence de Notation (Administrative) ».
> 2. **Vocabulaire.** Notation, note AAA à D → **Indice MDC de conformité sur 100** (Maîtrisé ≥ 85, Satisfaisant ≥ 70, Fragile ≥ 55, Exposé ≥ 40, Critique) + **exposition estimée en FCFA** (bas / central / haut). Audit, auditeur, rapport d'audit → diagnostic, analyste, rapport de diagnostic. Visa, certifié conforme, certification → **attestation de diagnostic**. Réviseur de comptes ou expert-comptable pour désigner MDC → interdit. Anomalie → observation. Fraude → « exposé à ».
> 3. **Périmètre légal.** MDC ne tient pas, ne vérifie pas, ne révise pas et ne redresse pas de comptabilité (ord. 2009-387, art. 3, 5, 68, 70) ; elle ne produit ni états financiers ni écritures de régularisation, ne vise ni ne certifie, et ne rédige pas d'actes juridiques (loi 96-672). Ces travaux vont à l'expert-comptable partenaire inscrit à l'Ordre ou à l'avocat partenaire. **Toute section de ce skill qui prévoit le contraire est abrogée.**
> 4. **Mission : gagner le contrôle.** Préparer (diagnostic = contrôle à blanc ; régularisation spontanée avant tout avis, LPF art. 24), assister (conseil de son choix, LPF art. 15-16), défendre (réponse sous 30 jours, LPF art. 22-1). Chaque observation porte une position de défense (forte / discutable / faible) et une stratégie (régulariser / documenter / défendre). Méthode et moteur uniques : `notateur-conformite/scripts/indice_mdc.py` + `referentiel_mdc_v1.json`.
> 5. **Documents livrés : zéro jargon technique.** Aucun nom de fichier (.md, .py, .json), aucune commande, aucun chemin, aucun bloc de code, aucun schéma en caractères de terminal dans un document destiné au client, au gérant ou à un partenaire. Les renvois internes citent le titre du document ; les schémas deviennent des tableaux. Les générateurs `publish_pdf_mdc.py` et `publish_livrable_mdc.py` bloquent tout manquement.


# QUI REÇOIT QUOI — cartographie de diffusion

## 0. À quoi sert ce skill

L'utilisateur est le Gérant d'une agence qui produit beaucoup d'écrits : notes de service, fiches de
poste, manuels, rapports, courriers, contrats, livrables clients. **Il s'y perd — et c'est normal :
la production est rapide, la diffusion ne l'est pas.**

Ce skill répond à deux questions, toujours les deux ensemble :

1. **Qui reçoit quoi ?** — pour que rien ne parte au mauvais destinataire, et que rien ne reste
   au tiroir par oubli.
2. **Qu'est-ce qui est devenu faux ?** — parce qu'un document juste le jour où il est écrit peut
   être faux trois semaines plus tard, sans que personne le rouvre.

> **La règle qui gouverne tout le reste : un document n'est pas un fichier, c'est un engagement
> envers quelqu'un.** Tant qu'on le regarde comme un fichier, on le classe. Quand on le regarde
> comme un engagement, on voit tout de suite qui il engage, et ce qui se casse quand il devient faux.

## 1. Étape 1 — Inventorier

Recenser les documents concernés. Le périmètre dépend de la demande : une session de travail, un
dossier client, un dossier RH, ou tout l'espace.

Le script `scripts/inventaire.py` fait le gros du travail — il liste les documents d'un dossier avec
leur référence MDC, leur date et leurs formats disponibles :

```bash
python3 ~/.claude/skills/qui-recoit-quoi/scripts/inventaire.py <dossier>
```

**Regrouper les formats d'un même document.** Un livrable existe souvent en `.md` (la source),
`.pdf` (la remise) et `.docx` (la retouche). **C'est un seul document, pas trois.** Ne jamais
présenter à l'utilisateur une liste de fichiers : présenter une liste de documents.

**Repérer la référence MDC** (`MC-FP-2026-001`, `MC-NS-2026-002`, `MC-CP-2026-001`…). C'est elle qui
identifie le document, pas son nom de fichier. Un document sans référence est probablement un
brouillon ou une source — le signaler.

## 2. Étape 2 — Classer par cercle de diffusion

Cinq cercles, du plus fermé au plus ouvert. **La règle : un document ne franchit jamais un cercle
sans décision explicite du Gérant.**

| Cercle | Qui | Exemples typiques |
|---|---|---|
| **0 · Direction seule** | Le Gérant | Notes de pilotage interne, grilles de correction, rapports RH, chiffrages non arbitrés |
| **1 · Un collaborateur nommé** | Une personne précise | Fiche de poste, briefing de prise de fonction, commande de travail, lettre d'observation |
| **2 · L'équipe** | Les départements | Notes de service, manuels de procédure, doctrines, calendriers |
| **3 · Le client** | Un client identifié | Rapports, notes de conformité, DEE, courriers, propositions, contrats |
| **4 · L'administration** | DGI, CNPS, Inspection | Déclarations, réponses, dossiers de régularisation |

**Le piège classique, à vérifier systématiquement.** Un document du cercle 0 qui contient la grille
de correction, la stratégie de négociation ou l'appréciation d'un collaborateur **ne doit jamais
passer en cercle 2 ou 3**. Quand un doute existe, poser la question au Gérant plutôt que d'arbitrer.

**Le cas inverse est aussi fréquent** : un document utile qui reste au cercle 0 par oubli, alors que
l'équipe en a besoin pour travailler. Le signaler aussi — un manuel que personne n'a reçu ne
s'applique pas.

## 3. Étape 3 — Débusquer ce qui est devenu faux

**C'est le cœur du skill, et la partie que personne ne fait spontanément.** Un document est vérifié
le jour de sa rédaction, jamais après. Six causes le rendent faux ; les chercher toutes.

### 3.1 Une personne nommée a changé

Un départ, une arrivée, un changement de fonction. Chercher **le nom** dans tous les documents, y
compris ceux déjà remis.

**Et surtout : chercher ce que le document PROMET à propos de cette personne, pas seulement le fait
qu'il la nomme.** Une signature de courtoisie se corrige à la prochaine édition. Mais si le document
dit que cette personne **signe les ordres de mission**, **valide les livrables**, ou **sert de point
de vérification d'identité au client**, alors son départ ouvre un **trou d'authentification** : le
contrôle promis au client ne fonctionne plus, ni pour valider ce qui est légitime, ni pour écarter ce
qui ne l'est pas. **Ce n'est plus une coquille de nom, c'est un risque.** Le dire avec ces mots.

### 3.2 Une donnée d'identité a changé

Régime fiscal, NCC, RCCM, centre des impôts, dirigeant, capital, adresse. **Le régime est le plus
dangereux** : il conditionne tous les calculs, donc tous les chiffres produits pendant qu'il était
faux sont faux.

### 3.3 Un chiffre a été recalculé ailleurs

Deux documents du même dossier portent deux valeurs pour la même grandeur. **L'un des deux est faux,
et c'est presque toujours le plus favorable qui circule.** Vérifier les chiffres pivots : chiffre
d'affaires, résultat, trésorerie, impôts dus, masse salariale, exposition, note de conformité.

### 3.4 Une analyse a dépassé sa durée de validité

Chez MDC, un chiffrage d'exposition est **réputé périmé au-delà de trois mois**. Un document qui
porte un tel chiffrage sans horodatage, ou daté de plus de trois mois, ne se remet pas en l'état.

### 3.5 Une décision contredit l'écrit

Le Gérant a tranché un périmètre, une position, une stratégie — et un document antérieur dit le
contraire. Le document n'est pas seulement obsolète : **il donne une instruction fausse à qui le lit.**

### 3.6 Une version postérieure existe

Deux versions coexistent sans que l'ancienne soit retirée. Préfixer l'ancienne `OBSOLETE_` ou la
déplacer, jamais la laisser à côté de la version courante.

### Comment chercher

Le script `scripts/chercher.py` cherche un terme dans les `.md`, `.pdf`, `.docx` et `.xlsx` d'une
arborescence, et dit dans quel document il apparaît et dans quel contexte :

```bash
python3 ~/.claude/skills/qui-recoit-quoi/scripts/chercher.py "AKOCHI" ~/Desktop
```

Chercher large puis trier : mieux vaut vingt résultats à écarter qu'un document oublié chez un client.

## 4. Étape 4 — Mesurer la gravité

Un document faux ne se traite pas de la même façon selon l'endroit où il est déjà parti.

| Où il est | Gravité | Traitement |
|---|---|---|
| **Pas encore diffusé** | Nulle | On corrige et on republie. Rien à signaler à personne |
| **Chez un collaborateur** | Faible | On rediffuse la version corrigée en disant ce qui change |
| **Chez un client, note ou rapport** | **Réelle** | **Note de correction signée du Gérant.** Le client a agi sur une information fausse |
| **Chez un client, clause d'un contrat** | **Élevée** | Avenant ou notification écrite — **c'est au juriste de trancher**, pas à nous |
| **Déposé à une administration** | **Maximale** | Ne rien faire sans arbitrage du Gérant. Une correction spontanée est une décision fiscale |

**Deux réflexes qui font gagner du temps.** Quand une mission **n'est pas encore déclenchée**, il
suffit de rééditer le document avant lancement — rien à signaler au client. Et quand plusieurs
corrections sont dues au même client, **les regrouper en un seul courrier** : trois notes de
correction en trois semaines inquiètent plus qu'elles ne rassurent.

## 5. Étape 5 — Produire le bordereau de diffusion

C'est le livrable du skill. Le donner **dans la conversation** — c'est une réponse, pas un document
à publier, sauf si l'utilisateur demande une version à garder sous la main.

Structure, dans cet ordre :

**1. Une phrase de cadrage** qui donne tout de suite le rapport : combien de documents, combien
sortent, combien restent. *« Neuf documents. Cinq ne sortent pas de l'agence, quatre s'envoient. »*
C'est cette phrase qui dissipe la sensation d'être perdu — la donner en premier.

**2. Ce qui s'envoie** — un tableau : destinataire · document ou corps de message · pièces jointes.

**3. Ce qui ne s'envoie pas** — un tableau : document · **pourquoi il reste au tiroir**. Toujours
donner la raison : sans elle, l'utilisateur croira à un oubli et l'enverra quand même.

**4. Dans quel ordre** — une chronologie datée, pas une liste. L'ordre compte souvent plus que le
contenu : certaines choses doivent être réglées avant qu'une autre ne parte.

**5. Ce qui est devenu faux** — s'il y a lieu : document · ce qui a changé · où il se trouve déjà ·
traitement proposé.

**6. Les décisions qui restent au Gérant** — courtes, numérotées, chacune appelant une réponse par
oui ou par non quand c'est possible.

## 6. Règles MDC à ne jamais enfreindre

- **Rien ne s'envoie sans le feu vert du Gérant.** Ce skill prépare et ordonne ; il n'expédie pas.
- **Un courrier ou un mail se rédige en texte**, jamais en Word ni en PDF. Le PDF est la pièce
  jointe ; le mail est un message.
- **Tout document destiné à sortir passe par la rédaction** (skill `redaction`) : charte, logo,
  zéro symbole Markdown résiduel.
- **Ne jamais inventer un destinataire ni une adresse.** Si l'adresse manque, écrire
  `[adresse à compléter]` et le signaler.
- **Ne jamais présumer qu'un document a été envoyé.** Tant qu'on n'en a pas la preuve — un accusé,
  un mail parti, une mention au journal —, il est réputé non transmis, et c'est ce qu'il faut dire.

## 7. Le ton juste

L'utilisateur demande ce skill parce qu'il est **perdu**, souvent en fin de session, souvent pressé.

- **Commencer par le chiffre qui rassure**, pas par la liste. On dit d'abord combien il y en a et
  combien sortent ; on détaille ensuite.
- **Des tableaux, pas des paragraphes.** Il doit pouvoir décider en balayant l'écran.
- **Ne jamais rendre une liste de fichiers.** Une liste de fichiers, il l'a déjà — c'est justement
  ce qui le perd.
- **Dire ce qui est risqué avec des mots simples et fermes**, sans dramatiser : *« ce n'est pas une
  coquille de nom, c'est un trou d'authentification »* vaut mieux qu'un paragraphe de précautions.
- **Terminer par les décisions qui lui reviennent**, clairement séparées du reste. C'est ce qu'il
  cherchait en posant la question.
