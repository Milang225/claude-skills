---
name: depouillement-releve-auto
description: "Dès qu'un relevé bancaire est fourni, le dépouiller automatiquement dans le gabarit MDC et remplir la SYNTHÈSE CATÉGORIES"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b317e1a9-2048-4ae5-ab82-de71d08bdbe8
---

Dès que l'utilisateur fournit un relevé bancaire (PDF/image, n'importe quelle banque), produire SANS attendre une demande explicite un fichier Excel basé sur le **gabarit de dépouillement MDC** (`GABARIT_DEPOUILLEMENT_RELEVE_MDC.xlsx`), avec :
1. Onglet **DÉPOUILLEMENT** : toutes les opérations saisies (Date | Libellé tel quel | Débit | Crédit | Solde imprimé), classification Débit/Crédit par la **méthode du solde progressif** (Solde recalculé = solde précédent + Crédit − Débit ; écart = 0 partout = saisie certifiée intègre).
2. Colonne **Catégorie** remplie pour chaque ligne selon les catégories MDC : Encaissement CLIENT / Versement espèces gérant / Virement reçu divers / Fournisseur / Salaire / Impôt-CNPS-FDFP / Frais bancaires / Retrait-prélèvement gérant / Mouvement interne-caution / Régularisation banque.
3. Onglet **SYNTHÈSE CATÉGORIES** : total par catégorie, avec **encaissements clients en évidence**.
4. **Bouclage** vérifié : Σ Débits / Σ Crédits / Solde final recalculé = totaux imprimés par la banque (au franc près).

**Why:** L'utilisateur (gérant MDC) a trouvé le gabarit `GABARIT_DEPOUILLEMENT_RELEVE_MDC.xlsx` utile et veut que ce dépouillement-catégorisation soit le livrable systématique à chaque relevé fourni.

**How to apply:** Identifier d'abord (banque, n° compte, titulaire, période, solde initial/final) — le **contenu prime sur le nom du fichier** (un fichier nommé « 2023 » peut contenir du 2022). Encaissement CLIENT = virement nommé OU remise de chèque (REM CHQ / SORT CHEQUES / REM CHEQUE CONFRERE) ; le tireur d'un chèque n'est PAS sur le relevé → renvoyer au grand-livre 411. Exclure des clients : versements espèces du gérant, RTGS de tiers, cautions. Voir [[methodologie_balance_mdc]] et la section 2/16 du skill mdc-expert. Gabarit + livrables dans `Documents/DOSSIER CLIENTS/<CLIENT>/`.
