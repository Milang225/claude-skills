---
name: regime-client-avant-impots
description: "Partir du régime fiscal effectif du client (avis émis) ; un dépassement de seuil est un risque, pas un changement de régime à appliquer"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 20cfa9d2-9e09-46bf-9e4b-86068bccb4e0
  modified: 2026-11-17T13:07:44.724Z
---

Les impôts d'un client se calculent selon le régime sous lequel il est réellement imposé, c'est-à-dire celui des avis émis. Le dépassement d'un seuil de chiffre d'affaires se présente comme un risque fiscal en cas de contrôle, chiffré à part. Il ne faut pas en déduire soi-même un autre régime, avec l'I-BIC, l'IMF ou la TVA, et le traiter en corrections comptables.

**Why:** Sur FAMILLE KRA, qui est à la TEE, j'ai fait intervenir l'I-BIC et la TVA parce que le CA dépassait 50 M. Le Gérant m'a repris le 17/11/2026.

**How to apply:** Avant tout calcul d'impôt, vérifier le régime effectif dans le dossier (avis, DFE, liasse déposée). Signaler les seuils dépassés dans une rubrique « risques » distincte. Voir [[famille-kra-negociant]].
