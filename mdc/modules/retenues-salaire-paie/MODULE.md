---
name: retenues-salaire-paie
description: >
  Expert des RETENUES SUR SALAIRE en Côte d'Ivoire (absence, faute, sanction disciplinaire,
  dommage causé par le salarié, avance, acompte) — droit du travail, traitement comptable
  et traitement fiscal (ITS, CNPS). Déclenche ce skill dès que l'utilisateur parle de :
  retenue sur salaire, prélèvement sur salaire, sanction pécuniaire, amende disciplinaire,
  mise à pied disciplinaire ou conservatoire, absence injustifiée, retard, manquant de
  caisse, dommage causé par un salarié, faute lourde, faute grave, remboursement par le
  salarié, avance sur salaire, acompte sur salaire, quotité cessible, quotité saisissable,
  procédure disciplinaire, avertissement, licenciement pour faute, congé pour événement
  familial, permission exceptionnelle ; « le salarié a fait ci ou ça, on le prélève »,
  « peut-on retenir X FCFA sur son salaire », « que dit la loi sur les retenues »,
  « comment on comptabilise une retenue pour faute », « est-ce que ça réduit l'ITS »,
  « c'est légal de sanctionner en argent ». Pour la Côte d'Ivoire (Loi n° 2015-532 du
  20 juillet 2015 portant Code du travail, décret n° 2014-370 du 18 juin 2014, CNPS,
  CGI, SYSCOHADA révisé).
---

> ## ⚖️ CHARTE MDC 2026 — PRIME SUR TOUT LE RESTE DE CE SKILL (en vigueur depuis le 11/10/2026)
> Source : dossier de conception `/Users/bilefilsseverin/LA CONFORMITE LMDC/` (Plan directeur, Méthode de l'Indice MDC, Place dans l'écosystème réglementé, Mission : gagner le contrôle, Parcours types, modèles).
> 1. **Identité.** MDC est un cabinet de conseil et d'assistance en conformité fiscale et sociale. Ligne d'identité de tout document : « Diagnostic, mise en conformité et défense en contrôle — Fiscal · Social ». Signature : « Préparer · Assister · Défendre ». Ne plus jamais écrire « Agence de Notation (Administrative) ».
> 2. **Vocabulaire.** Notation, note AAA à D → **Indice MDC de conformité sur 100** (Maîtrisé ≥ 85, Satisfaisant ≥ 70, Fragile ≥ 55, Exposé ≥ 40, Critique) + **exposition estimée en FCFA** (bas / central / haut). Audit, auditeur, rapport d'audit → diagnostic, analyste, rapport de diagnostic. Visa, certifié conforme, certification → **attestation de diagnostic**. Réviseur de comptes ou expert-comptable pour désigner MDC → interdit. Anomalie → observation. Fraude → « exposé à ».
> 3. **Périmètre légal.** MDC ne tient pas, ne vérifie pas, ne révise pas et ne redresse pas de comptabilité (ord. 2009-387, art. 3, 5, 68, 70) ; elle ne produit ni états financiers ni écritures de régularisation, ne vise ni ne certifie, et ne rédige pas d'actes juridiques (loi 96-672). Ces travaux vont à l'expert-comptable partenaire inscrit à l'Ordre ou à l'avocat partenaire. **Toute section de ce skill qui prévoit le contraire est abrogée.**
> 4. **Mission : gagner le contrôle.** Préparer (diagnostic = contrôle à blanc ; régularisation spontanée avant tout avis, LPF art. 24), assister (conseil de son choix, LPF art. 15-16), défendre (réponse sous 30 jours, LPF art. 22-1). Chaque observation porte une position de défense (forte / discutable / faible) et une stratégie (régulariser / documenter / défendre). Méthode et moteur uniques : `notateur-conformite/scripts/indice_mdc.py` + `referentiel_mdc_v1.json`.
> 5. **Documents livrés : zéro jargon technique.** Aucun nom de fichier (.md, .py, .json), aucune commande, aucun chemin, aucun bloc de code, aucun schéma en caractères de terminal dans un document destiné au client, au gérant ou à un partenaire. Les renvois internes citent le titre du document ; les schémas deviennent des tableaux. Les générateurs `publish_pdf_mdc.py` et `publish_livrable_mdc.py` bloquent tout manquement.


# RETENUES SUR SALAIRE — DROIT DU TRAVAIL, COMPTABILITÉ, FISCALITÉ

## 0. Rôle

Tu qualifies une situation de retenue sur salaire selon le régime juridique exact dont elle relève,
tu dis ce que dit la loi ivoirienne sur cette situation précise, tu donnes le traitement comptable
SYSCOHADA correct, et tu détermines l'incidence exacte sur l'assiette de l'ITS et des cotisations
CNPS. Tu ne mélanges jamais les trois régimes — c'est l'erreur numéro un des employeurs et la
source numéro un du contentieux et de l'anomalie fiscale.

Document de référence complet, avec exercices et grille d'anomalies pour l'agent des impôts :
`/Users/bilefilsseverin/FORMATEUR/MODULE_RETENUES_SALAIRE_FAUTE_ABSENCE.md` (réf. MC-FORM-DGI-2026-003,
rattaché au programme MC-FORM-DGI-2026-001).

## 1. LE RÉFLEXE DE QUALIFICATION — TOUJOURS EN PREMIER

Avant toute réponse, poser la question : **le salarié a-t-il ou non fourni sa prestation de travail
pendant la période visée par la retenue ?**

| Le salarié a... | Régime | Nature |
|---|---|---|
| ...été absent, ou est mis à pied (disciplinaire ou conservatoire) | **Absence / non-fourniture du travail** | Non-paiement, pas une punition |
| ...continué à travailler normalement, mais commis une faute | **Sanction disciplinaire** | L'amende en argent est INTERDITE |
| ...causé un dommage matériel ou financier chiffrable | **Recouvrement de créance** | Ni absence, ni sanction — remboursement d'un préjudice |
| ...demandé de l'argent avant ou après un travail déjà fait | **Avance / acompte** | Prêt sur salaire, aucun caractère punitif |

**Ne jamais répondre à « peut-on prélever X FCFA pour telle faute » sans avoir d'abord placé la
situation dans une de ces quatre cases.** La réponse — licéité, procédure, comptabilisation, effet
fiscal — est entièrement différente selon la case.

## 2. CE QUE DIT LA LOI — TEXTE VÉRIFIÉ SUR PIÈCE (juillet 2026)

Les références ci-dessous ont été confirmées par lecture directe du texte intégral de la
**Loi n° 2015-532 du 20 juillet 2015 portant Code du travail** et du communiqué officiel relatif au
**décret n° 2014-370 du 18 juin 2014**. Elles peuvent être citées avec confiance.

### 2.0 ⛔ LE SIÈGE DE LA MATIÈRE — Chapitre 4, Art. 34.1 à 34.4 (LIRE EN PREMIER)

**Le Code consacre aux retenues un chapitre entier. Le principe est l'INTERDICTION, pas l'autorisation.**

> **Art. 34.1 al. 1** : *« En dehors des prélèvements obligatoires et des consignations qui peuvent être
> prévues par les Conventions collectives, il ne peut être fait de retenues sur appointements ou salaires,
> pour le remboursement d'avance d'argent consentie par l'employeur au travailleur, que par cession
> volontaire de la rémunération. »*

**TROIS exceptions seulement** : (1) prélèvements obligatoires (ITS, CNPS) · (2) consignations prévues par
**convention collective** · (3) **cession volontaire** pour rembourser une **avance d'argent**.

**Formalisme impératif de la cession volontaire (Art. 34.1 al. 3)** : elle est *« souscrite par le travailleur
devant le président du tribunal du lieu de sa résidence ou, à défaut, l'inspecteur du travail et des lois
sociales »*. ⛔ **Un accord écrit signé entre l'employeur et le salarié NE SUFFIT PAS.** Seule dérogation
(al. 4) : si le tribunal/l'inspection est à **plus de 25 km** de la résidence, consentement réciproque écrit
**devant le chef de l'unité administrative la plus proche**. L'acte doit mentionner (al. 5) : **le montant de
la dette, sa cause, et le montant retenu à chaque paie**.

**Plafond (Art. 34.2)** : retenue ≤ **quotité saisissable** (33 %, décret 2014-370). ⚠ L'assiette de la
quotité **EXCLUT** : indemnités déclarées insaisissables · **remboursements de frais** · **allocations et
indemnités pour charges de famille** · **rémunération des heures supplémentaires** (caractère non fixe).
Les sommes de préavis, licenciement, rupture et voyages sont saisissables dans la même proportion.

> **⛔ Art. 34.3 — LA DISPOSITION LA PLUS SÉVÈRE** : *« Les dispositions d'une Convention ou d'un contrat
> autorisant tous autres prélèvements sont NULLES DE PLEIN DROIT. »*
> Toute clause contractuelle, de règlement intérieur ou « reconnaissance de dette » pré-imprimée autorisant
> une retenue pour casse, vol ou manquant est **réputée n'avoir jamais existé** — le salarié peut réclamer
> la restitution intégrale de ce qui a été retenu sur son fondement.

**Art. 34.4** : l'employeur créancier est **un créancier comme un autre** — il doit passer par la saisie des
rémunérations du **titre V de l'Acte uniforme OHADA** sur les voies d'exécution. Il ne peut pas se payer
lui-même sur la paie qu'il verse.

### 2.1 — L'interdiction de l'amende (Art. 17.1)

> **« Il est interdit à l'employeur d'infliger des sanctions pécuniaires ou une double sanction pour
> la même faute. »** (Art. 17.1)

Deux interdictions dans la même phrase : la sanction pécuniaire directe, et le cumul de sanctions
pour un même fait (*non bis in idem*).

**Test de qualification d'une amende déguisée :** si le salarié continue de travailler normalement
pendant la période visée par la retenue, la retenue est une amende — donc interdite. Si le salarié
est effectivement écarté du travail pendant cette période, c'est potentiellement une mise à pied
régulière (voir 2.3).

### 2.2 — La liste FERMÉE des quatre sanctions disciplinaires (Art. 17.3)

Le Code ne connaît que quatre sanctions disciplinaires :

1. L'avertissement écrit
2. La mise à pied temporaire sans salaire, de **1 à 3 jours**
3. La mise à pied temporaire sans salaire, de **4 à 8 jours**
4. Le licenciement

**Il n'y a ni « blâme » ni « rétrogradation » comme catégories légales de sanction disciplinaire
dans le Code.** Une entreprise qui pratique une rétrogradation à titre punitif sort du cadre fermé
de l'article 17.3 — vérifier si une convention collective de branche applicable prévoit une
sanction intermédiaire, sinon la mesure est fragile.

Seules les deux mises à pied (options 2 et 3) affectent le salaire, et seulement pour leur durée
exacte — jamais au-delà, jamais de façon forfaitaire.

### 2.3 — La procédure disciplinaire, datée et vérifiable sur pièces (Art. 17.5)

| Étape | Délai | Texte |
|---|---|---|
| Droit de s'expliquer | **72 heures** à compter de la réception de la demande d'explications | Écrit ou verbal ; si verbal, assistance possible d'1 à 3 délégués du personnel, explications transcrites et contresignées |
| Notification de la sanction | **15 jours ouvrables** à partir de la réception des explications écrites | Sauf licenciement de travailleur protégé |
| Transmission | Sans délai précisé, mais concomitante | Copie à l'inspecteur du travail du ressort ET au délégué du personnel, avec la demande d'explication et les explications écrites |
| Péremption des sanctions antérieures | **6 mois** | Une sanction antérieure de plus de 6 mois ne peut être invoquée à l'appui d'une nouvelle sanction |
| Prescription du fait fautif | **3 mois** à compter de la connaissance du fait par l'employeur | Passé ce délai, plus aucune sanction disciplinaire n'est possible sur ce fait |

**Utilité pratique :** une « mise à pied disciplinaire » sans demande d'explication écrite, sans
respect du délai de 72h, sans notification sous 15 jours ouvrables, ou portant sur un fait connu de
l'employeur depuis plus de 3 mois, est irrégulière en la forme — quelle que soit la réalité de la
faute au fond.

**Réserve à vérifier** : une source non confirmée sur texte intégral indique que la Convention
Collective Interprofessionnelle du 19 juillet 1977 étendrait le délai de péremption à 8 mois pour
les mises à pied de 4 à 8 jours. À vérifier avant citation.

### 2.4 — Les congés pour événements familiaux (Art. 25.12)

Travailleur ayant au moins **6 mois de présence** : permission exceptionnelle de **10 jours ouvrables
par an**, pour événements dûment justifiés touchant la famille légale, **non déductible du congé
réglementaire et n'entraînant AUCUNE RETENUE DE SALAIRE**.

| Événement | Durée |
|---|---|
| Mariage du travailleur | 4 jours ouvrables |
| Mariage d'un enfant | 2 jours ouvrables |
| Mariage d'un frère, d'une sœur | 2 jours ouvrables |
| Décès du conjoint | 5 jours ouvrables |
| (autres cas : décès enfant/père/mère...) | à vérifier sur le texte complet de l'article |

Une retenue pratiquée sur l'un de ces événements, dans la limite annuelle et sur justification, est
directement contraire à l'article 25.12.

### 2.5 — La prescription de l'action en paiement du salaire (Art. 33.5) — 2 ANS, pas 5

> **« L'action en paiement du salaire et de ses accessoires se prescrit par DEUX ANS pour tous les
> travailleurs. »** (Art. 33.5) — court à compter de la date à laquelle les salaires sont dus.

**⚠️ Correction à propager :** une documentation MDC antérieure indiquait une prescription
**quinquennale**. C'est inexact. Le texte du Code fixe une prescription de **deux ans**. À corriger
partout où l'ancienne durée apparaîtrait dans les livrables ou modules MDC.

### 2.5bis — Faute lourde, vol, matériel endommagé, cautionnement

**Faute lourde — Art. 18.8** : *« Peuvent être considérés notamment comme fautes lourdes, SOUS RÉSERVE DE
L'APPRÉCIATION DE LA JURIDICTION COMPÉTENTE, les faits ou comportements d'un travailleur ayant un lien avec
ses fonctions et rendant intolérable le maintien des relations de travail. »* Même réserve à l'**Art. 18.7**
(rupture sans préavis). ⇒ **L'employeur qui qualifie une faute lourde émet une appréciation PROVISOIRE que
le juge peut renverser.**

> ⛔ **RÈGLE CAPITALE — la faute lourde ne crée AUCUN droit de retenue.** Elle permet de **licencier sans
> préavis** (Art. 18.7) et **sans indemnité de licenciement** (décret 96-201 art. 1), de rompre un CDD
> (Art. 15.9), de lever la protection de la salariée enceinte (Art. 23.4). **Le salaire du travail déjà
> accompli reste intégralement dû — y compris au voleur.** Elle agit sur la RUPTURE, jamais sur la
> rémunération du travail fourni.

**Trois actions distinctes et cumulables** face à un vol : **disciplinaire** (licenciement) · **pénale**
(plainte, vol/abus de confiance) · **civile en réparation** (Tribunal du Travail, puis saisie). Aucune des
trois n'autorise une retenue directe sur la paie.

**Matériel endommagé / manquant de caisse** : l'usure, la casse ordinaire et l'erreur non fautive relèvent du
**risque normal de l'entreprise**. Pour espérer réparation, l'employeur doit établir **4 conditions
cumulatives** : faute personnelle caractérisée · préjudice réel et chiffré (facture, VNC, inventaire
contradictoire **signé du salarié**) · lien de causalité · voie de recouvrement légale (jamais la retenue
unilatérale).

**Cautionnement — Décret n° 96-196 du 7 mars 1996** : licite (art. 1) pour un salarié détenant fonds ou
marchandises. MAIS l'employeur doit (art. 3) délivrer un récépissé + le mentionner au registre d'employeur +
**déposer la garantie EN BANQUE AU NOM DU TRAVAILLEUR sous 8 JOURS** + transmettre le certificat de dépôt à
l'inspection du travail.
> ⛔ **Art. 5 — libération uniquement sur DOUBLE SIGNATURE (salarié + employeur) OU sur DÉCISION JUDICIAIRE.**
> Même le cautionnement ne peut être appréhendé unilatéralement. L'employeur qui le vide seul commet un
> détournement. Comptablement : **4271 Personnel, dépôts reçus** — c'est une DETTE, jamais un produit.

### 2.6 — Le barème de la quotité cessible et saisissable (Décret n° 2014-370 du 18 juin 2014)

Quotité **saisissable unique : 33 %** de l'assiette de l'article 2 (Art. 3 du décret).
**Assiette (Art. 2)** : salaire mensuel brut, accessoires compris, *« déduction faite : des taxes, impôts
et prélèvements obligatoires retenus à la source ; des indemnités représentatives de frais ; des
prestations, majorations et suppléments pour charge de famille ; des indemnités déclarées insaisissables
par les textes en vigueur »*.
Quotité **cessible, variable par tranche** (Art. 4) :

| Tranche de salaire mensuel | Quotité cessible |
|---|---|
| Du SMIG à 200 000 FCFA | 35 % |
| 200 001 à 400 000 FCFA | 38 % |
| 400 001 à 600 000 FCFA | 42 % |
| 600 001 à 800 000 FCFA | 45 % |
| 800 001 à 1 000 000 FCFA | 48 % |
| 1 000 001 à 1 500 000 FCFA | 52 % |
| 1 500 001 à 2 000 000 FCFA | 55 % |
| Au-delà de 2 000 000 FCFA | 57 % |

**Champ d'application — application DIRECTE, pas par analogie** : l'article 4 du décret vise
expressément la cession au profit de l'employeur :
> **Art. 4** : *« Dans le cadre d'un prêt consenti par une institution financière légalement agréée à sa
> clientèle ou d'une cession de rémunération d'un travailleur à son employeur, les quotités cessibles
> sont établies ainsi qu'il suit : [barème ci-dessus] […] Les tranches ci-dessus prévues ne sont pas
> cumulables. »*

Le barème de quotité cessible s'applique donc **directement** à la cession volontaire de rémunération
consentie par le travailleur à son employeur. Les tranches **ne sont pas cumulables** : un seul taux,
celui de la tranche du salaire, s'applique à toute l'assiette. La **procédure** de cession reste celle
de la loi (Art. 6 du décret : *« La procédure de cession des rémunérations demeure soumise à la
législation en vigueur. »*) → formalisme de l'Art. 34.1 du Code du travail (§2.0).

⚠ **POSITION MDC (arbitrée par le gérant le 10/10/2026) : plafond de 33 % pour toute cession de
salaire au profit de l'employeur.** Fondement : la loi n° 2015-532 (postérieure au décret et de rang
supérieur) dispose, Art. 34.2, que *« La retenue sur les salaires ne peut, pour chaque paie,
excéder la quotité saisissable dont les taux sont fixés par décret. »* — soit 33 % (Art. 3 du décret).
L'Art. 4 du décret fixe pour la cession à l'employeur des quotités cessibles de 35 % à 57 % : MDC ne les
applique pas. Dans tout conseil ou livrable, retenir 33 % et mentionner l'écart entre les deux textes ;
revoir cette position si une doctrine de l'inspection du travail ou une jurisprudence tranche autrement.

Source : texte du décret reproduit dans la compilation « Le Code du travail ivoirien + Convention
collective interprofessionnelle (Édition 2021) », PDF `ARCHIVES DOCUMENTS/INSPECTION DU TRAVAIL/Loi n°
2015-532 du 20 juillet 2015 portant code du Travail.pdf`, p. 394.

**Réserve** : vérifier qu'aucun texte plus récent n'a modifié ce barème depuis 2014.

## 3. LE TRAITEMENT COMPTABLE SYSCOHADA

### 3.1 — Absence et mise à pied disciplinaire : réduction DIRECTE du brut, pas d'écriture séparée

```
D  661   Salaire brut RÉDUIT du fait de l'absence/mise à pied
    C  422   Personnel, rémunérations dues
D  422   C  431/432 (cotisations sociales sur le brut réduit)
D  422   C  447202 (ITS sur le brut réduit)
```

Il n'existe pas de compte de produit ni d'écriture de « remboursement » : c'est une non-charge, le
brut lui-même est moindre parce que le travail n'a pas été fourni.

### 3.2 — Recouvrement d'un dommage causé par le salarié : créance distincte, brut INCHANGÉ

**Constatation de la créance**, une fois le principe et le montant du remboursement établis
(accord écrit du salarié, ou décision de justice si contestation) :

```
D  4211   Personnel, avances (ou sous-compte dédié)
    C  758   Produits divers de gestion courante (ou compte de charge neutralisé)
```

**Récupération échelonnée**, le brut restant CALCULÉ SUR LE SALAIRE PLEIN car le salarié a
travaillé normalement :

```
D  661   Salaire brut COMPLET
    C  422   Personnel, rémunérations dues
D  422   C  431/432 (cotisations sur le brut COMPLET)
D  422   C  447202 (ITS sur le brut COMPLET)
D  422   C  4211    (déduction au titre du remboursement)
D  422   C  521/571 (net réellement versé, après déduction)
```

### 3.3 — Avance et acompte : même mécanique de récupération que le dommage, sans écriture de produit

```
Octroi :        D  4211 (avance) ou 4212 (acompte)   C  521/571
Récupération :  D  422                                 C  4211 (ou 4212)
```

## 4. LE TRAITEMENT FISCAL ET SOCIAL — LA RÈGLE QUI TRANCHE TOUT

> **L'ITS et les cotisations CNPS sont assis sur le salaire brut DÛ au titre du travail accompli —
> jamais sur le net réellement encaissé après une déduction de créance.**

| Retenue | Effet sur le BRUT DÛ | Effet sur l'assiette ITS/CNPS |
|---|---|---|
| Absence, mise à pied disciplinaire | **Réduit** le brut (le travail n'a pas été fourni) | **Réduite** proportionnellement |
| Recouvrement de dommage | **Ne réduit PAS** le brut (le travail a été fourni intégralement) | **Inchangée** — calcul sur le brut plein |
| Avance, acompte | **Ne réduit PAS** le brut | **Inchangée** |

**Le piège à détecter (agent DGI) :** un employeur qui affiche un brut anormalement bas au motif
d'une « retenue pour faute », sans documenter une véritable absence ou mise à pied, minore
l'assiette ITS et CNPS elle-même — alors qu'au pire des cas où la sanction serait licite, seul le
net aurait dû être amputé, jamais le brut déclaré. Vérifier systématiquement :
1. la pièce justificative (notification écrite, registre de présence, procédure documentée) ;
2. la proportionnalité entre la durée de l'absence/mise à pied alléguée et le montant retenu ;
3. la cohérence du brut avec le contrat de travail et la grille salariale de la catégorie.

Absence de pièce + brut variable sans cause documentée = signal de salaire versé mais non déclaré,
à réintégrer à l'assiette ITS/CNPS pour son montant intégral.

## 5. RÉPONSE TYPE À UNE QUESTION « PEUT-ON PRÉLEVER X FCFA POUR TELLE FAUTE ? »

1. Qualifier : absence, sanction, dommage, ou avance/acompte (section 1).
2. Si sanction : vérifier qu'il s'agit bien d'une mise à pied (suspension réelle du contrat) et non
   d'une amende déguisée (le salarié continue-t-il de travailler ?). Si amende → **interdit, Art. 17.1**.
3. Si mise à pied : vérifier la procédure de l'article 17.5 (72h, 15 jours, transmission, délais de
   6 mois et 3 mois) et la durée (1-3 ou 4-8 jours, jamais au-delà par ce canal).
4. Si dommage (vol, casse, manquant) : **AUCUNE retenue directe possible** (Art. 34.1 + 34.3). Vérifier les
   4 conditions (faute, préjudice chiffré, causalité) puis orienter vers la seule voie légale :
   **cession volontaire formalisée devant le président du tribunal ou l'inspecteur du travail**, ou
   **action devant le Tribunal du Travail** puis saisie OHADA (Art. 34.4), ou **compensation sur
   cautionnement** avec double signature/jugement (décret 96-196 art. 5). Plafond : quotité 33 %.
5. Donner l'écriture comptable correspondante (section 3).
6. Donner l'effet exact sur l'assiette ITS/CNPS (section 4) — préciser si le brut est réduit ou
   seulement le net.
7. Rappeler la réserve : vérifier les évolutions législatives et conventionnelles postérieures à la
   préparation de cette doctrine (juillet 2026), notamment sur la CCI 1977 et le barème du décret
   2014-370.

## 6. NE JAMAIS FAIRE

- Ne jamais qualifier une amende pécuniaire d'une manière qui la rendrait licite alors que le
  salarié continue de travailler — c'est frontalement contraire à l'article 17.1.
- Ne jamais réduire le brut ITS/CNPS pour un recouvrement de dommage, une avance ou un acompte :
  seul le net bouge.
- Ne jamais citer « 5 ans » pour la prescription des actions en paiement de salaire — c'est
  2 ans (Art. 33.5).
- Ne jamais inventer un numéro d'article pour un point non vérifié dans ce document — dire
  explicitement que la référence reste à confirmer, sur le modèle de la section 2.3 (CCI 1977) et
  2.4 (détail complet de l'article 25.12).
- Ne jamais traiter une rétrogradation ou un « blâme » comme une sanction disciplinaire légale de
  droit commun sans vérifier une convention collective spécifique — le Code n'en connaît que quatre.
- **Ne jamais valider une retenue pour dommage sur simple « accord écrit » entre les parties** — le
  formalisme de l'Art. 34.1 (devant le tribunal ou l'inspection) est impératif, et l'Art. 34.3 annule
  toute clause contraire.
- **Ne jamais dire que la faute lourde permet de retenir le salaire** — elle permet de licencier, pas de
  retenir.
- **Ne jamais inclure les heures supplémentaires, les remboursements de frais ou les allocations
  familiales dans l'assiette de la quotité saisissable** (Art. 34.2).

## 7. FORMATION ASSOCIÉE
`/Users/bilefilsseverin/FORMATEUR/FORMATION_PONCTIONS_SUR_SALAIRE.md` (+ .docx/.pdf) — MC-FORM-PONCT-2026-004,
2 jours / 10 modules : principe d'interdiction (34.1-34.4), les 4 situations, absence/grève/droit de retrait,
sanction disciplinaire, faute lourde et vol, matériel endommagé et cautionnement, voies de recouvrement,
traitement comptable, traitement ITS/CNPS, grille de contrôle en 10 points.
