---
name: reflexe-retenues-source-prestataires
description: "Réflexe obligatoire — retenues à la source (PPSSI 2%, RIBNC, RIBIC) sur paiements aux prestataires, côté payeur au réel"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c3c001b6-a642-4b04-ae47-9c68316ff5e7
---

Ne plus JAMAIS livrer une compta ou des déclarations d'un client **au réel (RSI/RNI)** sans avoir balayé ses **achats de prestations** pour opérer la retenue à la source due.

- **PPSSI 2 %** (CGI Art. 84 bis) — prestation payée à un fournisseur du **secteur informel (TEE / microentreprise / TCE)**. Écriture `D 401 / C 4471` ; code e-impôts `PPSSI` (récap `PPSSIREGUL` au 30/04). **Définitive, non imputable** par le prestataire.
- **RIBNC 7,5 %** (Art. 92) — honoraires d'une **profession non commerciale au réel** (PP libérale). SARL au régime TEE → PPSSI 2 %, pas RIBNC.
- **AIRSI** — jamais sur un achat de prestations (uniquement quand le réel *vend* des biens à l'informel).

**Pourquoi :** oubli capitalisé sur GLOBE CÔTE D'IVOIRE (juillet 2026) — honoraires de conseil TEE 500 000 comptabilisés en charge SANS retenue → exposition à l'amende. Le gérant a demandé que l'erreur ne repasse plus.

**Comment l'appliquer :** capitalisé dans mdc-expert §25.2 (check-list point 9) et §30.6 (règle 7). Chaque facture de prestataire passe au filtre « quelle retenue à la source ? » avant livraison. Cf. [[client-globe-cote-divoire]] et [[service-declarations-mensuelles-eimpots]].

**RÈGLE DES PRÉLÈVEMENTS — QUI OPÈRE ? (23/07/2026).** Avant de porter un prélèvement au tableau des impôts du client :
- **Cas A — le client prélève** (paiement à un fournisseur non immatriculé, vente à revendeurs) ⇒ il est redevable, doit reverser ⇒ **la ligne figure au tableau** ; il n'y échappe qu'avec une **attestation d'exonération**, sinon il est taxé.
- **Cas B — un fournisseur prélève sur le client** (ex. **AIRSI 5 %** retenu par le grossiste) ⇒ **pas une nature due par le client** ⇒ **hors tableau** ; simple mention en note, crédit sur l'IBIC/IMF uniquement sur justificatifs. **Ne jamais déduire d'office** un prélèvement subi de l'impôt : l'impôt reste brut.
- **Taux : AIRSI 5 % · PPSSI 2 %.**
- Cas LERO : AIRSI = cas B (ETG a prélevé sur les achats de nitrate → sorti du tableau, IMF remis à 8 000 000 brut) ; PPSSI = cas A (LERO paie des prestataires → reste au tableau).
