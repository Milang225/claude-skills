---
name: famille-kra-negociant
description: "FAMILLE KRA SARL — négociant en gros et demi-gros (pas de mandat), régime TEE ; décisions du Gérant du 17/11/2026"
metadata:
  node_type: memory
  type: project
  originSessionId: 20cfa9d2-9e09-46bf-9e4b-86068bccb4e0
  modified: 2026-11-17T21:33:04.261Z
---

Le 17/11/2026, le Gérant de MDC a tranché deux points pour FAMILLE KRA SARL (NCC 2229049M).

1. **Activité — position changée, NON TRANCHÉE.** Le matin, le Gérant a dit : achat-revente en gros et demi-gros, sans mandat. L'après-midi, il a affirmé : dépôt-vente, la société ne possède pas la marchandise, et il voulait ne montrer que le 7072. Le journal reconstruit est en négoce (7011 / 6011). Ne bascule en commissions que sur preuve que les **ventes sont faites au nom des fournisseurs**. CGI art. 341-342 : le commissionnaire qui vend en son nom propre pour le compte d'autrui est réputé avoir acquis et livré le bien, donc l'opération est imposée en brut même sans propriété. Les pièces actuelles vont dans le sens de l'achat : factures CODCI « CLIENT COMPTANT » payées en espèces, note MDC du 04/08/2026 « ventes fermes », contrat de dépôt-vente seulement en modèle non signé.
2. **Régime** : la société est à la TEE (avis 2025 émis et payés, 344 000). Les comptes 2025 se tiennent en TEE et en SMT : ni TVA, ni I-BIC, ni IMF. Il ne faut jamais introduire l'impôt sur le bénéfice ou la TVA dans son dossier comme des corrections.

**Why:** DFE et RCCM indiquent la vente en gros et demi-gros. Le Gérant m'a repris quand j'ai appliqué l'I-BIC, l'IMF et la TVA du réel simplifié au seul motif que le CA du négoce (219,8 M) dépasse le plafond TEE de 50 M (CGI art. 73).

**How to apply:**
- Ventes 219 765 002 en 701 et achats 199 664 502 (226 factures) en 601. Les 20 100 500 en 7072 sont en réalité la marge.
- Stock propre : 7 430 100 selon l'inventaire reconstitué, à faire signer.
- Le dépassement du plafond est seulement un **risque fiscal** en cas de contrôle, à signaler à part ; ce n'est pas une écriture.
- À la TEE, l'AIRSI n'est pas imputable : c'est une charge définitive. La TEE remplace la patente (art. 72), et son taux est de 4 % pour le négoce (art. 77).
- La pièce 72 « affectation du financement en stock » (D 311 41 800 413 / C 521 31 584 213 / C 571 10 216 200) **vient de la reconstitution MDC du 04/08/2026** (réf. MC-RECON-COM-2025-002, aujourd'hui en _OBSOLETE). C'est une écriture d'équilibrage vers une trésorerie estimée (banque 271 184 + caisse 2 000 000), sans relevés. Le Sage du client la reprend. Il ne faut pas en déduire un détournement de fonds : la trésorerie réelle est inconnue faute de relevés 2025.
- Script de contrôle : `~/FAMILLE KRA/controle_incoherences_kra.py` (REF « modele » = negociant, « regime_declare » = TEE). Voir aussi [[regime-client-avant-impots]].

**Décision du 26/11/2026 (simulation en commissions)** : les échéances BAOBAB du 15/11 et du 15/12/2025 sont réglées d'après l'échéancier LD2435470324 et le journal du client, sans attendre le relevé, ce qui déroge à R14. Circuit : caisse → 585 → 538001 au montant exact, puis prélèvement D 162001 + D 1662 / C 538001. Le capital restant dû est de 9 585 504.
