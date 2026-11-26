# Barème de la note de conformité financière MDC

Fiche de référence du skill `diagnostic-financier`. Le barème est défini une seule fois, dans
`scripts/moteur_diagnostic.py` (constante `BAREME`), et repris à l'identique dans l'onglet
`Score` du classeur — où il est **modifiable par l'utilisateur** (cellules bleues).

---

## 1. Mécanique

Sept critères. Chacun est noté **100 / 50 / 0** selon deux seuils, puis pondéré.

```
note du critère = 100 si la valeur atteint le seuil « bon »
                   50 si elle atteint le seuil « moyen »
                    0 sinon
score global    = Σ (poids × note du critère)          → 0 à 100
```

Une valeur non calculable (dénominateur nul, EBE négatif) vaut **0**, pas « non noté » : une
entreprise dont l'EBE est négatif n'a pas un ratio « indisponible », elle a un ratio catastrophique.

### Échelle

| Note | Score | Lecture |
|---|---|---|
| **AAA** | ≥ 90 | Structure financière excellente |
| **AA** | ≥ 80 | Très solide |
| **A** | ≥ 70 | Solide |
| **BBB** | ≥ 60 | Correcte |
| **BB** | ≥ 50 | Fragilités identifiées |
| **B** | ≥ 40 | Fragile |
| **CCC** | ≥ 30 | Situation préoccupante |
| **CC** | ≥ 20 | Très préoccupante |
| **C** | ≥ 10 | Critique |
| **D** | < 10 | Situation compromise |

---

## 2. Les sept critères et leur justification

### 2.1 Rentabilité d'exploitation — EBE / CA — poids 20 %
*Bon ≥ 8 % · Moyen ≥ 4 %*

Le premier des tests : l'activité dégage-t-elle une marge avant toute question de financement,
d'amortissement et d'impôt ? Un EBE faible condamne tout le reste — l'entreprise ne pourra ni
rembourser, ni investir, ni encaisser un choc. Poids maximal avec le critère 2.5.

### 2.2 Couverture des frais financiers — RE / frais financiers — poids 20 %
*Bon ≥ 3x · Moyen ≥ 1,5x*

Sous **1x**, l'exploitation ne paie plus la banque : le résultat courant devient structurellement
négatif et la cessation de paiements n'est plus qu'une question de calendrier. C'est le ratio le
plus prédictif à court terme, d'où son poids.

### 2.3 Endettement net / EBE — poids 15 %
*Bon ≤ 2x · Moyen ≤ 3,5x*

Nombre d'années d'EBE nécessaires pour effacer la dette. La norme d'orthodoxie financière retient
**3x maximum**. Au-delà de 4x pour une PME sans actifs mobilisables, le refinancement devient
incertain.

### 2.4 Autonomie financière — capitaux propres / total bilan — poids 15 %
*Bon ≥ 30 % · Moyen ≥ 15 %*

Mesure qui « possède » l'entreprise. Sous 15 %, les créanciers en sont propriétaires de fait et
tout aléa se transforme en insolvabilité. À croiser systématiquement avec le test **art. 371
AUSCGIE** (capitaux propres < moitié du capital social → régularisation obligatoire).

### 2.5 Dettes fiscales et sociales en jours de CA — poids 15 %
*Bon ≤ 20 j · Moyen ≤ 45 j*

**Le critère signature de MDC.** Il figure ici pour deux raisons cumulatives :

1. c'est la mesure directe de l'**exposition** que MDC est chargée de traiter ;
2. c'est un **indicateur avancé de défaillance** — le score de la Banque de France retient
   explicitement les dettes fiscales et sociales parmi ses sept contributions, et observe que les
   entreprises en difficulté se signalent par leur allongement.

Autrement dit, l'arriéré fiscal n'est pas seulement un risque de redressement : c'est un symptôme
de trésorerie. Ce double statut est l'argument central des restitutions MDC.

### 2.6 Délai de règlement fournisseurs — poids 10 %
*Bon ≤ 60 j · Moyen ≤ 90 j*

Quand une entreprise ne peut plus payer, elle commence par étirer ses fournisseurs — avant même
de manquer une échéance bancaire. Un allongement rapide est un signal précoce. Poids modéré car
le ratio est sensible à la politique d'achat et aux pratiques sectorielles.

### 2.7 Part de l'endettement à court terme — découverts / dette brute — poids 5 %
*Bon ≤ 20 % · Moyen ≤ 40 %*

Financer des immobilisations ou un BFR permanent par du découvert, c'est un risque de
transformation : la ressource est révocable à tout moment. Poids faible, mais discriminant en cas
de retournement.

---

## 3. Ce que le barème ne mesure pas

Volontairement absents :

- **La croissance.** Statistiquement neutre en matière de risque de défaillance — une croissance
  rapide mal financée est aussi dangereuse qu'une stagnation.
- **La rentabilité des capitaux propres (ROE).** Trop sensible au levier : une société très
  endettée peut afficher un ROE flatteur juste avant de tomber.
- **La taille.** Elle biaiserait le classement en faveur des grands dossiers.
- **La qualité de la conformité administrative.** C'est l'objet de `notateur-conformite`.

---

## 4. Le score Z'' d'Altman — usage et limites

```
Z'' = 6,56 X1 + 3,26 X2 + 6,72 X3 + 1,05 X4

X1 = fonds de roulement net / total actif      (working capital — PAS le BFR)
X2 = réserves + report à nouveau / total actif
X3 = résultat d'exploitation / total actif
X4 = capitaux propres / dettes totales
```

Seuils d'origine : `< 1,1` défaillance probable · `1,1 à 2,6` zone grise · `> 2,6` saine.

**Trois précautions non négociables.**

1. **X1 est le fonds de roulement net, pas le BFR.** Confondre les deux inverse le signal : un BFR
   qui gonfle ferait *monter* le score alors qu'il traduit une dégradation.
2. **Les seuils sont calibrés sur des échantillons américains.** Aucune validité statistique n'est
   établie sur des PME ivoiriennes. Le score sert de **classement ordinal** du portefeuille ;
   il ne doit jamais être présenté à un client comme une probabilité de faillite.
3. **Une fonction score vieillit.** Elle doit être maintenue à mesure que l'environnement
   économique évolue.

---

## 5. Procédure de recalibrage

Le barème du §2 est fixé **à dire d'expert**. Il devient une véritable référence dès que l'onglet
`Portefeuille` du classeur contient assez de dossiers.

### Quand recalibrer
- Au moins **20 dossiers** au total, et **5 dossiers minimum par secteur** pour publier une
  médiane sectorielle.
- Puis une revue **annuelle**.

### Comment
1. Extraire, pour chaque critère, la distribution observée sur le portefeuille (onglet
   `Portefeuille`, lignes 6 à 40).
2. Poser, par secteur : **seuil « bon » = médiane** du secteur ; **seuil « moyen » = premier
   quartile** (ou troisième quartile pour les critères en sens inverse).
3. Vérifier la **discrimination** : les dossiers ayant connu un incident réel (redressement,
   cessation de paiements, rupture de crédit) doivent se retrouver majoritairement sous 40.
   Si ce n'est pas le cas, le barème ne discrimine pas — revoir les poids avant les seuils.
4. Reporter les nouvelles valeurs dans `BAREME` (`scripts/moteur_diagnostic.py`) **et** dans les
   cellules bleues de l'onglet `Score`. Les deux doivent rester identiques.
5. **Dater et archiver** la version du barème. Une note produite sous barème v1 n'est pas
   comparable à une note produite sous barème v2 : mentionner la version dans le livrable.

### Ce qu'il ne faut pas faire
- Ajuster un seuil pour « arranger » la note d'un client donné.
- Publier une médiane sectorielle calculée sur moins de cinq dossiers.
- Changer de barème en cours de mission.

---

## 6. Réserves à reproduire dans tout livrable

> La note de conformité financière porte sur la **santé financière** de l'entité. Elle est établie
> à partir des documents remis par le client, non audités sauf mention contraire. Elle ne
> constitue ni une certification, ni un audit légal des comptes, ni un conseil en investissement.
> Le score Z'' est utilisé comme instrument de classement et non comme probabilité de défaillance.
> Les pondérations et seuils sont fixés par MDC et révisés périodiquement.
