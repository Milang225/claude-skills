---
name: dossier-kwaani-services-ef-2025
description: "KWAANI SERVICES (NCC 2300527J) — ouverture, balance 2025 validées ; liasse SMT 2025 du 03/11 (résultat -1 842 572, bilan 816 667)"
metadata:
  node_type: memory
  type: project
  originSessionId: 2ad5cf0f-c8c3-421b-bfc2-92104d5efbd4
  modified: 2026-11-03T13:00:44.599Z
---

KWAANI SERVICES (NCC 2300527J, commerce général, gérante KOUASSI Paule Noëlle Emmanuella, SMT, capital 1 000 000, aucune recette en 2024). Dossier : `DOSSIER CLIENTS/KWAANI SERVICES` (FISCAL = point fiscal MC-PSF-KWA-2026-001 du 26/10 ; ETATS FINANCIERS 2025 ; CONTROLES_DE_TENUE = brouillon de demande de pièces du 03/11).

Le 03/11/2026, l'utilisateur a déposé la DSF 2024 (EF24.pdf) par erreur dans `MABEK/ETATS FINANCIERS 2025/KWAANI ` : ce n'est PAS un document MABEK. Copie rangée dans KWAANI SERVICES/ETATS FINANCIERS 2025/_SOURCES_EF ; le sous-dossier MABEK/.../KWAANI a été mis à la Corbeille le 03/11 à la demande du gérant.

**Balance d'ouverture au 01/01/2025 VALIDÉE par le gérant le 03/11/2026** (« C'est bon ») : BALANCE_OUVERTURE_2025_KWAANI_SERVICES_2026-11-03.xlsx (script _SOURCES_MD/build_balance_ouverture_2025.py ; onglets Balance, Écritures AN format Sage AN-001, Passage DSF, Points d'attention). Total 3 177 806 : 101 capital 1 000 000 C ; 129 RAN débiteur 183 333 D ; 139 perte 2024 2 177 806 D ; 401 bailleur loyers 720 000 C ; 422 salaires dus 900 000 C ; 4421 taxes sur salaires 4 706 C ; 4428 TEE 2024 250 000 C ; 4486 pénalités 303 100 C ; 571 caisse 816 667 D.

Points : bilan 2024 déposé déséquilibré (actif 816 667 / passif 896 667, HB saisi -2 281 139 au lieu de -2 361 139) ; hypothèse que toutes les charges 2024 sont impayées (note 5 vide), corroborée pour le fiscal par le point fiscal du 26/10 ; salaires 900 000 sans CNPS ; capitaux propres -1 361 139 (art. 371 AUSCGIE) ; le point fiscal relève aussi des régularisations ITS 2023 et 2024 (18 150 chacune) absentes de la DSF.

**Base 2025 du 03/11/2026** : _SOURCES_MD/build_base_2025.py produit BASE_COMPTABLE_2025, BALANCE_GENERALE_2025 et ECRITURES_COMPTABLES_2025_SAGE (87 lignes, ΣD=ΣC=7 198 184, comptes sur 6 chiffres). DÉCISIONS DU GÉRANT du 03/11 : loyer 720 000 et salaires 900 000 repris de 2024 ; charges fiscales ALIGNÉES sur le point fiscal (TEE 200 000 par mois, ITS + taxes de formation janvier 19 800 en 641300, pénalités 2 772 en janvier) ; aucune recette ni aucun règlement en 2025 (confirmé). Perte 2024 affectée en 129 au 30/06/2025 (date supposée). Résultat 2025 -1 842 572 ; bilan 816 667 (caisse) ; dettes 4 020 378 ; capitaux propres -3 203 711. **Balance 2025 VALIDÉE le 03/11/2026.** LIASSE SMT 2025 élaborée le 03/11 (LIASSE_SMT_2025_KWAANI_SERVICES_2026-11-03.xlsx, script _SOURCES_MD/build_liasse_smt_2025.py, N et N-1 placés dans la grille Balance, BILAN/RESULTAT condensés fixés en base de trésorerie : actif = passif = 816 667, HB -4 203 711, HD 4 020 378, KZC -1 842 572 ; N-1 recalculé -2 361 139 / -2 177 806). Formules vérifiées avec le module Python `formulas`. Fiche R1 : personne ayant établi = BILE FILS SEVERIN (comme la DSF 2024), expert attestant laissé vide. Reste : visa du cabinet. Quittances DGI reçues par mail le 26/10 (DOCUMENTS_RECUS_PAR_MAIL) : 29/08/2023 TEE 2023 (60 000 + 20 000) et 21/06/2024 103 333 = solde TEE 2023 (confirme que le seul paiement 2024 soldait la dette 2023) ; aucune quittance 2025. Ouverture, base, balance et écritures VALIDÉES sur la plateforme le 03/11 ; liasse SMT 2025 VALIDÉE par le gérant le 03/11 et marquée livrable ★. [[ordre-production-balance-ecritures-liasse]] [[elaborer-ef-suivant-la-liasse]]
