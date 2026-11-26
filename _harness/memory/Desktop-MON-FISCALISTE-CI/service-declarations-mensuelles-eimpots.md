---
name: service-declarations-mensuelles-eimpots
description: Service récurrent — remplir chaque mois les déclarations e-impôts (réel) à partir des données comptables fournies
metadata: 
  node_type: memory
  type: project
  originSessionId: fe77d19f-b8dd-46ba-867d-c9e660543b65
---

Projet en cours (démarré juillet 2026) : produire chaque mois les **déclarations fiscales remplies, prêtes à saisir sur e-impôts.gouv.ci**, pour des entreprises **au réel (RNI et RSI)**. Le fiscaliste (MDC) fournit les données d'un mois (balance, grand livre, journal, tableau de bord — « tout moyen qui comporte des données ») + une instruction (ex. « fais-moi la TVA de janvier ») ; je renvoie le **formulaire rempli ligne par ligne** + les annexes EDI à joindre, pour que son équipe le saisisse.

**Périmètre & échéances** : piloté par le calendrier du tableau synoptique DGI → [[FICHE_SYNOPTIQUE_CALENDRIER_DGI.md]] (Partie B). Réel non-DGE = **15 du mois suivant** ; DGE/DME = **10/15/20**. Carnet mensuel type (services) : TVA, ITS (+CE+CN+FDFP), TSE (0,1 % CA), retenues fournisseurs (RIBIC/RIBNC/AIRSI/PPSSI le cas échéant). Annuels : patente (15/03), État 301 (30/05-30/06), régul. ITS (février), acompte BIC.

**Structure des formulaires** : [[FICHE_DECLARATIONS_EIMPOTS_EDI_EFI.md]] (62 natures champ par champ) + modèle Excel `Desktop/MON FISCALISTE CI/MODELES_DECLARATIONS_EIMPOTS_CI.xlsx`.

**Règles de calcul faisant foi** (barème ITS/RICF, charges patronales CE local exonérée / total local 2,8 % / expat 12 %, TVA 18/9 %, TSE 0,1 %) : le tableau synoptique DGI prime sur les taux par défaut des templates EDI/EFI (qui sont périmés sur l'ITS). Toujours revérifier vs Annexe Fiscale de la période — cf. [[toujours-verifier-dgi-2026]].

**Dossier témoin observé** : RESEAU IVOIRIEN DE MAINTENANCE (NCC 2300433S) — comptable Fils Séverin BILE — déclare TVA hors DGE, ITS, RIBIC/RIBNC, TSE, patente commerce+transport, État 301 (⇒ profil réel, probablement RNI).
