---
name: documents-sobres-sans-style-ia
description: RÈGLE — les documents produits doivent être formels et ne jamais paraître rédigés par une IA (pas d'encadrés colorés, pas de tirets, pas de détails internes)
metadata:
  type: feedback
---

Les documents destinés aux clients ou à l'administration doivent être **formels, sobres, et ne pas donner l'impression d'avoir été faits par une IA**.

**Why:** le gérant (15/10/2026) a rejeté un sommaire avec encadré jaune, tirets « - » bruts, noms de fichiers en MAJUSCULES_AVEC_TIRETS_BAS et détails internes (_OBSOLETE, emplacements, « rien n'a été envoyé ni signé ») : « ça ne fait rien de formel », « c'est grave dans un document officiel ».

**How to apply:**
- Pas d'encadré coloré ni de bloc « L'essentiel » décoratif ; paragraphes ordinaires, puces « • » discrètes seulement si utiles (convertisseurs corrigés le 15/10 : build_mdc_pdf.py, md2docx_mdc.js).
- Jamais de noms de fichiers ou de dossiers bruts (tirets bas) dans le texte ; les écrire en français lisible.
- Aucun détail interne dans un document client : archives, emplacements, état d'avancement interne, matrices de contrôle, courriers « à valider ».
- Éviter les tournures et tics d'IA : tirets longs en série, listes à rallonge, phrases d'emphase, formules toutes faites, emojis, mentions de génération automatique.
- Ton d'un professionnel : phrases complètes, sobres, précises ; distinguer document interne (Agence) et document client.
- Voir aussi [[explications-simples-actes-exacts]] et [[aucun-montant-documents-collaborateurs]].

**Ajouts du 16/10/2026 :**
- Jamais de champ entre crochets (« [NOM ET QUALITÉ] », « [À COMPLÉTER] ») dans un document officiel : renseigner à partir des parties connues, sinon reformuler sans le champ (« son représentant habilité ») et demander l'information manquante au gérant.
- Les conventions, contrats, actes, décisions, attestations et lettres signées par les parties ne portent JAMAIS le logo ni l'en-tête de l'Agence : les produire par build_versions_a_signer.py (Word simple, papier à en-tête de la partie émettrice), jamais par le pipeline brandé publish_*_mdc. Anciennes versions avec logo archivées dans _OBSOLETE/AVANT_RETRAIT_LOGO_2026-10-15.
- **Format validé par le gérant le 16/10/2026** (« ça c'est bon ») : l'acte A_SIGNER_01 — titre en capitales, « Entre les soussignés », comparution complète de chaque partie (forme, capital, RCCM, NCC, siège, représentant nommé avec sa qualité), « ci-après », Exposé, articles numérotés, tableau sobre, signatures « Pour [rôle], [société], [nom], [qualité] ». Modèle à suivre pour toute convention.
- (16/10/2026) Aucune mention explicative entre parenthèses à côté d'un blanc : pas de « (date de la décision) », « (date de signature) », « (date de la signature réelle, à ne jamais antidater) ». Le gérant n'en voit pas l'utilité et cela trahit un travail fait par IA. Un blanc de date reste nu : « Fait à ____, le ____ », « Par décision du ____ ».

**Précision du 19/10/2026 :** la règle « sans logo » ne vaut que pour les actes entre clients ou tiers (conventions TRACE ↔ AVE MARIA, décisions d'associé, attestations). Les contrats et notes où l'Agence est partie (contrat de prestation, proposition, note d'information) portent TOUJOURS l'en-tête et le pied de page de l'Agence, avec une référence MC-… : pipeline publish_livrable_mdc.py et publish_pdf_mdc.py. Le gérant a reproché un contrat RICHTAZ produit sans son en-tête (« depuis quand tu me génères un document sans mes initiales ? »).

**Précision du 23/10/2026 :** un acte signé où l'Agence est partie (procès-verbal, décharge) se monte sur le papier à en-tête officiel `PAPIER_EN_TETE_2026/PAPIER_EN_TETE_MDC_2026.docx`, sans filigrane « CONFIDENTIEL ». Les signatures vont côte à côte, sur une ligne qui ne se coupe pas entre deux pages, et le document tient en 2 pages. PDF par Word. Modèle : `DOSSIER CLIENTS/ATELIER DES REVES BY BGK/_SOURCES_MD/build_pv_remise.py`. Le pipeline publish_* (filigrane, signatures sur 3 pages) a été refusé (« le rendu ne me plaît pas »).

**RÈGLE ABSOLUE du 26/10/2026 (« de grâce, ne fais plus jamais ça ») :** aucune note d'avertissement ni réserve explicative dans un document produit. Sont visés les paragraphes du type « les déclarations non déposées ne figurent pas dans ces montants… », « … sont à vérifier », « montant à confirmer ». Le document ne contient que les faits et les chiffres. Les limites, réserves et points à vérifier se disent au gérant dans la réponse du chat, jamais dans le fichier.
