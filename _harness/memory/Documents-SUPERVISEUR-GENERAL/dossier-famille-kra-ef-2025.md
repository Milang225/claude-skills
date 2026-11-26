---
name: dossier-famille-kra-ef-2025
description: "FAMILLE KRA SARL — EF 2025 élaborés le 02/11/2026 (écritures éclatées au mois, liasse SMT, note MC-RC-KRA-2026-001) ; réserves emprunts/camion/trésorerie"
metadata:
  node_type: memory
  type: project
  originSessionId: b5080078-3cc3-4071-811e-fda290375549
  modified: 2026-11-02T11:56:25.085Z
---

Le 02/11/2026, à la demande du gérant : écritures 2025 éclatées mois par mois (format Sage), balance, liasse SMT 2025 et note de revérification MC-RC-KRA-2026-001, dans `DOSSIER CLIENTS/FAMILLE KRA/ETAT FINANCIER 25/` (générateur `_SOURCES_MD/build_kra_2025.py`). Base = comptabilité 2025 retenue du 30/09/2026 (fidèle à DECL 26) : CA 20 100 500, résultat 4 546 600, bilan 5 904 878. Clé mensuelle = achats facturés 2025 (226 factures). Corrections : 7062→7072, 605→6388, TEE 446→442. Le PDF « EF25 » du dossier est en fait la liasse 2024 déposée (LIAS3250520943762), reprise en N-1.

Gérante : Mme KOUAKOU N'DA AMOIN ANNE-CAROLLE (dite Carolle), précisé par le gérant le 02/11/2026 ; la liasse 2024 citait encore KRA KOUAKOU DIEUDONNE. Demande de pièces MC-DP-KRA-2026-002 prête, non envoyée.

Données Direction du 02/11 : loyers réels 240 000 (local 1) + 50 000 (local 2) par mois, 2 salariés déclarés à 75 000. Résultat avec stock final 0 : 3 466 600, bilan 4 824 878. Stock final 2025 : options A (0, recommandée), B (fiche d'inventaire reconstitué signée, plafonné à 3 253 700 du stock 2024), C (3 253 700) — paramètre STOCK_FINAL du générateur ; option B retenue le 02/11 : le générateur lit la fiche d'inventaire (lignes « Société », signée, plafond stock 2024), testée. Position arrêtée le 02/11 (le gérant refuse l'achat-revente en nom propre) : FAMILLE KRA est MANDATAIRE (dépôt-vente), CA = commissions et marges ; stock propre 0 (stock 2024 vendu), marchandises des mandants 7 430 100 HORS BILAN (note 4 pour mémoire, note 2) ; flux encaissés/reversés pour les mandants en comptes de tiers ; résultat 3 466 600, bilan 4 824 878. Réserve clé : contrats de dépôt-vente et redditions de comptes, taux TEE prestataire.

**Why:** le dépôt 2025 est en retard ; les points à arbitrer (modèle commission, emprunts GESCI/Baobab, camion KAMA, trésorerie, stock, CNPS) restent ouverts.

**How to apply:** ne pas déposer avant pièces sur les points 1 à 4 de la note ; à réception, modifier le générateur et régénérer. Voir [[elaborer-ef-suivant-la-liasse]], [[mdc-elabore-ef-ne-vise-pas]].
