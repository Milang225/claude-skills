---
name: revue-taux-cgi-2026
description: Revue du 20/09/2026 des taux cités dans les cours bilan et compte de résultat — erreurs trouvées et corrigées ; points de vigilance récurrents.
metadata:
  type: reference
---

Passe de vérification au CGI 2026 (20/09/2026) sur `COURS_BILAN_SN_LIGNE_PAR_LIGNE` et `COURS_COMPTE_DE_RESULTAT_SN`. **Sept erreurs de fond corrigées** :
- biens amortissables en frais généraux : **300 000 F** de prix unitaire (art. 18-9°) — les cours disaient 500 000 ;
- comptes courants d'associés : **cinq** conditions cumulatives (art. 18 A 6°), la 5e étant le **remboursement sous 5 ans** (reprise en 6e année) — les cours en listaient 4 ;
- taux de référence : **taux moyen des avances de la BCEAO** + 2 points, et non « taux de prêt marginal » ;
- redevances et assistance : **5 % du CA dans la limite de 20 % des frais généraux** (art. 18 A 5°) ; les 50 % du brut ne visent que les bénéficiaires en **pays non coopératif ou à fiscalité privilégiée** (art. 38-3°) — les cours généralisaient les 50 % à tout l'intragroupe ;
- régime mère-fille : **50 % / 90 % / 95 %** (art. 21 et 22), jamais « 50 à 100 % » ;
- dons : double limite **2,5 % du CA et 200 000 000 par an** ;
- art. 110 : **35 %** région d'Abidjan (Abidjan, Aboisso, Adzopé, Agboville) / **40 %** autres régions, dans la limite de 50 % des bénéfices sur 4 exercices, programme ≥ 100 M HT (25 M pour les PME).

Vérifié et **confirmé exact** : IMF 0,5 % du CA TTC, minimum 3 000 000 (art. 39 ET 53, donc aussi au réel simplifié), maximum 35 000 000 ; 40 % logements du personnel avec plafond de 20 M HT par logement (art. 18 C 3°) ; sursis des plus-values, remploi sous 3 ans (art. 28) ; réserve légale 1/10 jusqu'à 1/5 du capital (AUSCGIE). **Piège à retenir** : « art. 144 » désigne le FDFP dans le CGI et la **facture normalisée dans le LPF** — toujours préciser le code.

**Why :** un taux faux dans un support de formation se propage dans tous les dossiers des collaborateurs.
**How to apply :** à chaque reprise d'un ancien document, refaire cette passe. Voir aussi [[formations-lecture-des-etats]]. Deux outils maison ont été renforcés ce jour : `build_mdc_pdf.py` rend désormais les blocs de code ``` en monospace au lieu de les laisser en clair, `publish_pdf_mdc.py` les détecte dans son contrôle qualité, et `mdutil.unwrap()` ne fusionne plus les blocs de code. Les coefficients de l'amortissement dégressif restent à vérifier : ils relèvent de l'arrêté n° 102/MEF/DGI/CT du 4 février 1985, non archivé.
