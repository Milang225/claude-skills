---
name: dossier-audit
description: >
  PRODUCTION DU DOSSIER D'AUDIT DE CONFORMITÉ de MDC (La Maison de la Conformité SARL), à partir des
  données de l'Atelier du diagnostic (application de profil d'entreprise). Prend un dossier de l'Atelier,
  en tire les chiffres pivots, écrit les squelettes pré-remplis des livrables, les fait rédiger, les publie
  en PDF et en Word brandés, contrôle leur cohérence et prépare la remise. Produit le jeu complet : synthèse
  de l'exposition, tableau d'exposition, rapport d'audit de conformité, audit documentaire, note de chiffrage
  des expositions, classeur des matrices d'anomalies, constat de non-conformité et Indice, plan d'action,
  le point et les bons usages, note au comptable, modèles d'actes juridiques, script de restitution, sommaire,
  bordereau de transmission et cartographie des destinataires. Déclenche dès que l'utilisateur veut : produire /
  sortir / générer / fabriquer le dossier d'audit ou les livrables d'un audit de conformité ; « fais-moi les
  documents de l'audit de <client> » ; reprendre les données de l'application de profil ou de l'Atelier pour
  en faire des livrables ; contrôler la cohérence d'un dossier d'audit avant remise.
---

# DOSSIER D'AUDIT DE CONFORMITÉ — de l'Atelier aux livrables

Ce skill fabrique le dossier d'audit d'un client à partir de la matière déjà saisie dans
**l'Atelier du diagnostic**. Il ne refait pas le fond : il le met en forme, le contrôle et le range.
Le gabarit est le dossier **MABEK TRANSPORT du 24 novembre 2026**, et les contrôles sont ceux qui ont
fait échouer sa première remise.

Identité : LA MAISON DE LA CONFORMITE SARL — NCC 2506426B — RCCM CI-ABJ-03-2025-B13-10831 —
Capital 1 000 000 FCFA — Gérant M. BILE FILS SEVERIN. FCFA, droit ivoirien et OHADA.
Jamais « expert-comptable » pour désigner MDC : **cabinet de conseil en conformité fiscale et sociale**.

---

## 1. D'OÙ VIENNENT LES DONNÉES

L'Atelier tient, pour chaque dossier, un fichier unique qui porte tout : identité du client, Indice
et ses six domaines, chiffrage (droits, bas, central, haut), lignes d'exposition avec leur pièce,
matrices d'anomalies, inventaire documentaire, priorités, et la matière des livrables L01 à L23.

Le script le trouve tout seul, dans cet ordre : le fichier passé en `--json`, puis l'Atelier s'il
tourne sur le poste, puis le fichier du poste
`~/Documents/DOSSIER CLIENTS/<DOSSIER>/DIAGNOSTIC_COMPLET/donnees_tableau_de_bord.json`.

**Aucun chiffre ne se saisit à la main.** Tout montant d'un livrable vient de ce fichier ou s'en
déduit. Un chiffre qui n'y est pas n'entre pas dans un livrable : il est réclamé au dossier.

---

## 2. LA CHAÎNE DE PRODUCTION

```
python3 ~/.claude/skills/dossier-audit/scripts/formulaires_de_collecte.py <DOSSIER> "<dossier d'audit>"
   → le classeur des huit formulaires : le remplir, puis
python3 ~/.claude/skills/dossier-audit/scripts/lire_formulaires.py "<dossier d'audit>"
python3 ~/.claude/skills/dossier-audit/scripts/formulaires_de_collecte.py <DOSSIER> --etat
python3 ~/.claude/skills/dossier-audit/scripts/donnees_dossier.py <DOSSIER>
python3 ~/.claude/skills/dossier-audit/scripts/squelettes_audit.py <DOSSIER> "<dossier d'audit>"
   → rédiger chaque .md de _SOURCES_MD : lever toutes les consignes « À RÉDIGER »
python3 ~/.claude/skills/dossier-audit/scripts/controle_coherence_audit.py <DOSSIER> "<dossier d'audit>"
python3 ~/.claude/skills/dossier-audit/scripts/publier_dossier_audit.py "<dossier d'audit>"
python3 ~/.claude/skills/dossier-audit/scripts/documents_de_remise.py <DOSSIER> "<dossier d'audit>"
   → puis publier à nouveau : le sommaire, le bordereau et la cartographie
```

0. **`formulaires_de_collecte.py`** puis **`lire_formulaires.py`** — la boucle d'entrée du skill :
   **vous recevez des formulaires, vous les remplissez, le skill en fait les livrables.** Le premier
   écrit un classeur de neuf feuilles — un sommaire qui dit ce qui manque, puis huit formulaires ayant
   chacun ses colonnes, ses listes de choix et ses lignes vides, pré-remplis de ce que l'Atelier porte
   déjà. Le second relit le classeur rempli et en fait `collecte.json`, que les squelettes reprennent.
   Trois livrables en dépendent entièrement, parce que l'Atelier ne les nourrit pas : « Le point et les
   bons usages » (formulaire F6), les modèles d'actes (F7) et le script de restitution (F8). Tant que le
   formulaire est vide, le livrable le dit et reste un squelette, que le publieur refuse.
   Le détail des besoins est dans `reference/CE_QUE_LE_SKILL_DEMANDE.md`.
   **Un besoin non couvert se réclame, il ne se suppose pas.**
1. **`donnees_dossier.py`** — la fiche des pivots et les contrôles de bouclage. Les droits et le
   central des lignes d'exposition doivent faire, au franc, les totaux du tableau de bord. **Un arrêt
   ici se corrige dans l'Atelier, jamais dans un livrable.**
2. **`squelettes_audit.py`** — écrit dans `_SOURCES_MD/` un squelette par livrable : en-tête, référence
   MC, plan, et **tous les tableaux chiffrés déjà remplis**. Les passages à écrire portent une consigne
   « À RÉDIGER » qui dit quoi dire et sur quelle matière. Le script n'écrase jamais un fichier existant.
3. **La rédaction** — c'est le travail du cabinet, pas du script. Le plan de chaque document et le ton
   attendu sont dans `reference/CATALOGUE_DES_LIVRABLES.md`.
4. **`controle_coherence_audit.py`** — les pivots, les valeurs concurrentes, les termes interdits, la
   référence de chaque livrable. Rien ne part tant qu'il reste un point d'arrêt.
5. **`publier_dossier_audit.py`** — PDF et Word brandés par les générateurs de `mdc-expert`, avec leur
   contrôle qualité bloquant. **Il refuse toute source qui porte encore une consigne « À RÉDIGER ».**
   La version précédente est archivée avant d'être remplacée.
6. **`documents_de_remise.py`** — le sommaire, le bordereau et la cartographie, construits sur
   **l'inventaire réel du dossier** : un document encore en squelette n'y figure pas, et un document
   publié hors catalogue est signalé. Ils se régénèrent à chaque remise, en dernier.

Le contrôle de cohérence vérifie sept choses : les pivots, les valeurs étrangères au dossier proches
d'un pivot, les termes interdits, la référence de chaque livrable, **les codes d'anomalie en double**,
**les totaux de tableau qui ne font pas la somme de leur section**, et la correspondance entre les
sources et les fichiers publiés. Les trois derniers sont nés du test du 24 novembre 2026 : une matrice
dupliquée y était passée sans être vue.

Le **classeur des matrices** a son générateur, `classeur_matrices.py` : il **relit les sources du
dossier** et n'écrit aucun chiffre de sa main. Il refuse un rapport qui porte encore une consigne
« À RÉDIGER », et se relance **après la dernière correction du rapport**, avant les PDF. C'est la règle
apprise sur MABEK, où un classeur produit trop tôt a contredit le dossier de 941 257. L'ancien
générateur du dossier MABEK, lui, est un exemplaire, pas un outil :
c'est la règle apprise sur MABEK, où un classeur produit avant la dernière correction du rapport a
contredit le dossier de 941 257. Modèle à reprendre :
`~/Documents/DOSSIER CLIENTS/MABEK/AUDIT DE CONFORMITE 2026/_SOURCES_MD/build_matrices_xlsx.py`.
Le classeur se régénère **après** la dernière correction du rapport, et avant les PDF.

---

## 3. CE QUE LE DOSSIER CONTIENT

Dix-sept documents, dans l'ordre de lecture. Le détail de chacun — objet, destinataire, plan type,
référence, format, caractère obligatoire — est dans `reference/CATALOGUE_DES_LIVRABLES.md`.

| # | Livrable | Destinataire | Format |
|---|---|---|---|
| 0 | Sommaire du dossier | Client | PDF |
| 0 bis | Bordereau de transmission | Client | PDF |
| 1 | Synthèse de l'exposition | Client | PDF + Word |
| 2 | Tableau d'exposition | Client | PDF + Word |
| 3 | Rapport d'audit de conformité | Client | PDF + Word |
| 3 bis | Grille des déclarations, un bloc par exercice | Client | PDF + Word |
| 3 ter | Audit des procédures internes et externes | Client | PDF + Word |
| 4 | Audit documentaire | Client | PDF + Word |
| 5 | Note de chiffrage des expositions (sensible) | Direction | PDF + Word |
| 6 | Classeur des matrices d'anomalies et des chiffrages | Client | Excel + PDF |
| 7 | Le point et les bons usages | Client | PDF + Word |
| 8 | Plan d'action de mise en conformité | Client | PDF + Word |
| 9 | Constat de non-conformité et Indice | Client | PDF + Word |
| 10 | Note d'instructions au comptable | Comptable, par le Gérant | PDF + Word |
| 11 | Modèles d'actes et instructions juridiques | Avocat ou notaire, par le Gérant | PDF + Word |
| 12 | Note particulière au dossier (facultative) | Client | PDF + Word |
| 13 | Script de restitution | **Interne, jamais remis** | PDF + Word |
| 14 | Cartographie des destinataires | Interne et client | PDF |

**L'attestation de diagnostic ne se délivre qu'à partir de 70 sur 100 et sans manquement critique.**
En dessous, le dossier porte un **constat de non-conformité** : c'est lui qui tient lieu de réponse.
Aucun livrable ne revendique un visa, une certification ou une attestation que l'Indice interdit.

---

## 4. LES RÈGLES QUI NE SE NÉGOCIENT PAS

1. **Un chiffre pivot n'a qu'une valeur dans un dossier.** Une correction amont se propage à tous les
   livrables, au franc, et le contrôle de cohérence le vérifie avant la remise.
2. **Tout constat cite sa pièce.** Les lignes d'exposition de l'Atelier portent leur pièce : elle se
   recopie dans le livrable. Un montant sans pièce reste signalé comme tel, jamais arrondi.
3. **Ce qui s'exclut ne se cumule pas.** Les qualifications alternatives se présentent hors total.
4. **Trois scénarios, toujours** : favorable, central, haut. L'écart entre le favorable et le haut
   mesure ce que vaut la régularisation volontaire : c'est l'argument décisif devant le dirigeant.
5. **Aucune échéance, aucun délai** dans un document client, sauf demande expresse du Gérant. Le plan
   d'action se range par rangs.
6. **Zéro jargon** : aucun nom de fichier, aucun chemin, aucune commande, aucun bloc de code.
7. **Jamais « gratuit »**, jamais « IFU » : l'identifiant ivoirien est le **NCC**.
8. **Aucun montant d'honoraires** dans un livrable d'audit.
9. **Le document sensible se remet séparément** : la note de chiffrage ne part pas dans le même envoi.
10. **Plusieurs exercices, un seul audit** : une seule notation, un seul jeu d'observations
    dédoublonné, chaque observation étiquetée par son exercice. La grille des déclarations, l'audit
    documentaire, la paie et le tableau d'exposition se déclinent par exercice ; le skill les déduit du
    cadrage. Jamais un rapport par exercice.
11. **Chaque livrable garde sa source** dans `_SOURCES_MD/` : un PDF sans sa source n'est plus corrigible.

---

## 5. LE CIRCUIT DE CLÔTURE

Produire ne suffit pas. Avant toute remise, le dossier passe par :

1. le **contrôle de cohérence** de ce skill ;
2. le **Superviseur** (module `auditeur-superieur` du skill `mdc`), qui rend un avis motivé —
   feu vert, feu vert conditionnel, feu orange ou feu rouge — et une liste fermée de conditions
   de sortie. Il contrôle les pivots, les bouclages, la note, la charte, la complétude du pack et
   l'hygiène du dossier ;
3. la **correction des points d'arrêt**, dans les sources, puis une nouvelle publication ;
4. le **mail de remise** préparé en brouillon, jamais envoyé, et aligné sur l'inventaire réel du
   dossier — ni plus de documents annoncés que remis, ni moins.

Ce que le contrôle de MABEK a appris, et que le contrôle de cohérence vérifie désormais :
le classeur régénéré après la dernière correction ; un seul jeu de totaux dans le dossier ; un
document périmé retiré de la remise plutôt que laissé à côté du bon ; la méthode écrite partout où
un montant ne se reconstitue pas de sa propre ligne ; et un mail qui ne recommande rien que le
dossier n'établit.

---

## 6. RANGEMENT

```
~/Documents/DOSSIER CLIENTS/<CLIENT>/AUDIT DE CONFORMITE <ANNÉE>/
├── _SOURCES_MD/              ← les sources, et le générateur du classeur
├── _OBSOLETE/VERSIONS_MODIFIEES/   ← les versions remplacées, jamais à côté des bonnes
└── les livrables en PDF, Word et Excel
```

Les livrables sont enregistrés dans un dossier suivi pour apparaître sur la plateforme, et marqués
comme livrables. Tout est numérique : pièces scannées, signatures numériques, PDF.
