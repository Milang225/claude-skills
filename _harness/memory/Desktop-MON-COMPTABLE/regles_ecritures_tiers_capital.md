---
name: regles-ecritures-tiers-capital
description: "Deux règles absolues de passation d'écritures exigées par le gérant — trésorerie via tiers, ne jamais oublier le capital"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b5d55cce-ca3c-4c9a-910c-fe89dc1c67e6
---

Sur tout travail comptable (reconstitution, journal, régularisation, à-nouveau, liasse, audit), DEUX règles absolues exigées par le gérant (cas FAMILLE KRA, juin 2026, après deux fautes commises) :

1. **JAMAIS de trésorerie (521 Banque / 571 Caisse / 53) directement contre une classe 6 ou 7.** Toujours passer par un compte de tiers en deux temps : engagement (D 60x / C 401 ; D 411 / C 701 ; D 661 / C 422 ; D 64x / C 44x) PUIS règlement (D tiers / C 521-571). Seules exceptions : frais bancaires/agios (6311/671 ↔ 521), virements internes (585).

2. **TOUJOURS constater la charge AVANT le règlement** (constatation préalable). Ordre chronologique non négociable : 1) constatation/engagement (D charge / C tiers) puis 2) paiement (D tiers / C trésorerie). Interdit de payer (débiter un tiers) une charge jamais constatée. Charge constatée non payée = dette normale ; paiement sans charge préalable = anomalie (décaissement occulte). En clôture, charge sans facture → la constater quand même via 408 (FNP).

3. **NE JAMAIS oublier ni forfaitiser le CAPITAL.** Récupérer le capital social réel aux statuts/DSV/RCCM (le demander si absent, jamais le deviner), l'isoler sur une ligne 101 dédiée, ventiler 101/105/111-118/121-129/13. Toute variation = AGE documentée (Art. 360 AUSCGIE SARL).

**Why:** Sans passage par les tiers ni constatation préalable, l'écart charges constatées ↔ paiements (= les dettes au 31/12) est perdu et le bilan est faux. Le capital noyé/inventé masque les anomalies P-1 (CAP-SANS-AGO) et fausse les capitaux propres.

**How to apply:** Check-list de fin avant toute livraison comptable — (1) chaque flux tréso via un tiers ? (2) chaque charge constatée AVANT son règlement ? (3) capital isolé/tracé ? (4) variation stocks = annulation SI + constatation SF ? (5) ΣD=ΣC, Actif=Passif ? Si un « non » → reprendre, ne pas livrer. Détail dans skill mdc-expert §25. Voir [[comptabilite_syscohada]] et [[methodologie_balance_mdc]].
