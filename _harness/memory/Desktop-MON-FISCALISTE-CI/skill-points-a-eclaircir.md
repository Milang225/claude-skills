---
name: skill-points-a-eclaircir
description: "Skill dédié qui DÉTECTE les points à éclaircir d'un dossier et DRESSE la DEE globale ; règle d'or : soumettre → attente → traiter après réponse, jamais qualifier avant"
metadata: 
  node_type: memory
  type: reference
  originSessionId: c3c001b6-a642-4b04-ae47-9c68316ff5e7
  modified: 2026-08-18T02:23:15.603Z
---

Le skill **`points-a-eclaircir`** (créé août 2026) **cherche les points à éclaircir** d'un dossier (relevé, pièces, base, états, déclarations) et **dresse la DEE** (Demande d'Explication Écrite) globale.

**Déclencheurs :** « cherche/liste les points à éclaircir », « prépare/dresse la DEE », « qu'est-ce qui reste à justifier ? », « fais la demande d'explication ».

**Règle d'or (= mdc-expert §37.10) :** on **soumet, on met en ATTENTE (4711/4712/471/409/5211), on traite APRÈS la réponse — jamais qualifier avant.** Un chèque au gérant sans pièce va en **4712**, PAS en 462 (462 est déjà une qualification). Pour les points sensibles (prélèvement dirigeant), la DEE présente les **scénarios d'exposition** (distribution→IRVM 15 %, rémunération→ITS, remboursement→preuve, prêt→à rembourser) au lieu d'une écriture.

**Livrable :** UN « Document des points à éclaircir » GLOBAL (une seule DEE consolidée, remplace les DEE partielles → archivées OBSOLETE), catalogue de détection D1-D15, produit via le pipeline règle d'or ([[regle-dor-controle-livrables]], `publish_livrable_mdc.py`). Fond = ce skill ; fabrication = [[skill-producteur-livrables]] ; traitement post-réponse = mdc-expert. S'appuie sur [[reconstitution-releve-maitrise-ecarts]] (comptes d'attente §37). Cas de référence : GLOBE (MC-DEE-GCI-2026-004). Voir aussi [[jamais-minorer-exposition-fiscale]], [[posture-auditeur-detecter-irregularites]].
