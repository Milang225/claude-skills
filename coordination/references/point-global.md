# Point global des dossiers en cours — marche à suivre

Le gérant a demandé à chaque collaborateur le point de chacun de ses dossiers en cours. But : **avoir enfin une vue complète**, savoir ce qui brûle, ce qui va brûler et ce que personne ne suit, puis décider ensemble et confier les suites. Les départs du 5 décembre (Claude, SOGBOU) rendent la réaffectation urgente.

Scripts (Python 3 + openpyxl), dans `scripts/` du skill :
- `grille.py` : les 20 colonnes du point (une ligne par dossier), obligatoires marquées ;
- `modele_point.py` : modèle Excel à envoyer (listes déroulantes, mode d'emploi, exemple) ;
- `consolider.py` : réunit les points, classe et produit le classeur de travail.

## 1. Préparer la demande (si elle n'est pas déjà partie au bon format)

- Un modèle par collaborateur, pré-rempli avec son nom et, si on la connaît, la liste de ses clients :
  `python3 scripts/modele_point.py POINT_<Nom>.xlsx --collaborateur "<Nom>" --clients "ACME;BETA;…"`
- Message type (WhatsApp ou e-mail), à adapter et à faire valider par le gérant :

  > Bonjour <prénom>, pour le point global du cabinet, merci de remplir le fichier joint : une ligne par dossier en cours dont vous êtes responsable (clients mensuels et missions non terminées). Colonnes en rouge obligatoires ; si vous ne savez pas, écrivez « À vérifier ». À me renvoyer avant le <date, heure>. Merci.

- Si le gérant a déjà demandé le point en texte libre, **ne pas le refaire demander** : on transcrit (étape 2).

## 2. Recevoir les points, quelle que soit leur forme

- Modèle Excel rempli : utilisable tel quel.
- Autre Excel, Word, PDF, messages WhatsApp, notes vocales retranscrites : **transcrire** dans un CSV dont l'en-tête est fait des clés de `grille.py` (séparateur « ; »), une ligne par dossier, **un fichier par collaborateur** (`point_<nom>.csv`).
  - Ne jamais inventer ni déduire une date, un mois ou un statut : laisser vide. Le vide sera relancé.
  - Recopier les formulations du collaborateur dans `blocage`, `action_proposee`, `commentaire`.
  - Garder le nom du client tel qu'écrit. La consolidation rapproche les variantes (« ACME » et « ACME SARL ») et signale les doublons.
- Liste de **tous** les clients en cours, pour trouver ceux sans aucun point :
  - export de l'écran Clients du CRM, ou liste fournie par le gérant (un nom par ligne, `clients.txt`) ;
  - si le serveur MCP `mdc-crm` est disponible : `depot_clients` ou `clients_search`.

## 3. Consolider

```
python3 scripts/consolider.py POINT_GLOBAL_<AAAA-MM-JJ>.xlsx point_*.xlsx point_*.csv \
  --date <AAAA-MM-JJ> --sortants "Claude;SOGBOU" --clients clients.txt
```

**Classement :**

| Niveau | Motifs |
|---|---|
| 🔴 Urgent | échéance ou action proposée dépassée ; déclaration fiscale en retard d'un mois ou plus ; comptabilité en retard de 2 mois ou plus ; contrôle fiscal en cours ; paie en retard ; blocage alors que l'échéance approche |
| 🟠 À anticiper | échéance dans 7 jours ; comptabilité en retard d'un mois ; déclarations sociales en retard ; états financiers en cours ou non commencés ; pièces manquantes ; aucune action concrète ; point incomplet (un dossier dont on ignore l'état n'est **jamais** « à jour ») |
| ⚪ Non touché | aucune intervention depuis 7 jours ou plus |

**Mois « attendu » :** le mois M-1 après le 15, sinon M-2. C'est une **convention de lecture** : si le gérant applique d'autres délais à un dossier (régime, calendrier particulier), il prime. **Ne jamais affirmer une date limite fiscale de mémoire : la vérifier ou la demander.**

**Le classeur produit contient cinq feuilles :**
- **Synthèse** : chiffres, et une ligne par collaborateur (dossiers, urgents, à anticiper, non touchés, à compléter, honoraires impayés, sortant) ;
- **Dossiers** : toutes les lignes, avec leurs alertes, en couleur ;
- **À compléter** : ce qu'il faut redemander, collaborateur par collaborateur ;
- **Plan proposé** : action, responsable (« À RÉAFFECTER » pour un sortant), date, besoin du gérant, colonnes « Décision du gérant » et « Statut » ;
- **Sans point** : clients en cours pour lesquels personne n'a répondu.

La sortie JSON du script donne les chiffres et les urgences pour le compte rendu.

## 4. Présenter au gérant (court, dans cet ordre)

1. **Les chiffres** en 3 lignes : dossiers reçus, 🔴 / 🟠 / ⚪, sans point, à compléter.
2. **Ce que personne ne suit** :
   - les clients sans point ;
   - les doublons (deux responsables) ;
   - les dossiers des sortants (Claude, SOGBOU), avec le nombre de dossiers et leurs urgences.
3. **Les urgences**, dossier par dossier, en une ligne chacune : client, collaborateur, motif principal, action proposée. Pas plus de 8 à la fois, puis « on continue ? ».
4. **Ce qu'on attend de lui** : la colonne « Besoin du gérant ».
5. **Ce qu'on redemande** : feuille « À compléter », avec les messages de relance prêts à envoyer.
6. Joindre le classeur `POINT_GLOBAL_….xlsx`.

## 5. Décider ensemble

Pour chaque dossier urgent, puis à anticiper, puis non touché, le gérant choisit l'une de ces options. Le coordinateur reformule chaque décision en une phrase : verbe, dossier, responsable, date.
- **Valider l'action proposée**, éventuellement en la corrigeant.
- **Réaffecter** : le dossier d'un sortant, ou un dossier mal suivi. Proposer un nouveau responsable en équilibrant la charge d'après la Synthèse (nombre de dossiers et d'urgents par collaborateur). Prévoir avec le sortant une **passation** datée avant son départ.
- **Demander un plan d'action** au collaborateur, quand la situation demande réflexion : contrôle fiscal, retard de plusieurs mois, client difficile.
- **Se garder un rappel** : appel au client, décision sur les honoraires impayés.
- **Clore** : dossier terminé, ou client qui n'est plus suivi.

Reporter chaque décision dans la feuille « Plan proposé » :
- colonne « Décision du gérant » ;
- colonne « Statut » à « Validé », « Réaffecté », « Plan demandé » ou « Clos ».

Rendre le classeur mis à jour.

## 6. Transmettre et suivre

**Si le module Coordination du CRM est en service** (outils `coord_*` disponibles) :
- chaque décision devient `coord_action_creer` :
  - nature `action`, `demande_plan` ou `memo` ;
  - dossier (`cid`) et responsable (`staff_id`), retrouvés avec `clients_search` et `coord_collaborateurs` ;
- confirmation du gérant par code ;
- ensuite le CRM prévient, relance et fait le point du soir.

**Sinon :**
- un message par collaborateur, avec SA liste : n°, client, action, date, et la consigne de répondre « FAIT » quand c'est fait ;
- un message pour chaque sortant, demandant sa passation ;
- la liste des rappels du gérant.

Proposer de refaire le point global **chaque semaine** jusqu'à ce qu'il n'y ait plus ni « sans point » ni « non touché », puis chaque mois.

## Messages types

**Relance « à compléter »**
> <prénom>, merci pour ton point. Il manque pour <client> : <champs>. Peux-tu compléter avant <heure> ? Si tu ne sais pas, écris « À vérifier ».

**Client sans point**
> <prénom>, le client <client> n'apparaît dans aucun point. Est-il à toi ? Si oui, ajoute sa ligne ; sinon dis-moi qui le suit.

**Passation (collaborateur sortant)**
> <prénom>, pour préparer ton départ du <date>, merci de me remettre avant le <date> la passation de chacun de tes dossiers :
> - l'état exact ;
> - ce qui est en cours ;
> - les échéances ;
> - les pièces attendues ;
> - les accès et contacts utiles ;
> - ce qu'il reste à faire, étape par étape, avec les dates.

**Réaffectation**
> <prénom>, à partir du <date> tu reprends <client> (suivi jusqu'ici par <nom>). Priorité : <action> pour le <date>. La passation de <nom> te sera transmise.
