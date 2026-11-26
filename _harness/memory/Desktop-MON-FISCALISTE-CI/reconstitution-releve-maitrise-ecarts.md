---
name: reconstitution-releve-maitrise-ecarts
description: "Reconstituer la compta à partir du relevé bancaire + pièces, en PROUVANT la maîtrise des écarts (bouclage banque nul, reste isolé en attente + DEE)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c3c001b6-a642-4b04-ae47-9c68316ff5e7
  modified: 2026-08-14T22:09:01.191Z
---

**Dès qu'un dossier fournit un RELEVÉ BANCAIRE et des PIÈCES, la mission est de reconstituer la comptabilité et de PROUVER que les écarts sont maîtrisés.** Méthode complète : mdc-expert **§37** (renvoyée aussi dans auditeur-superieur).

**Pourquoi :** exigence du gérant (août 2026, dossier GLOBE) — « à partir du relevé et des pièces, tu dois reconstituer et vérifier que les écarts sont maîtrisés voire nuls… je veux un travail de pro ». C'est la définition même du travail de reconstitution.

**Comment l'appliquer (les points durs) :**
- Le **relevé est la colonne vertébrale** : compte **521 reconstitué = solde de clôture AU FRANC** (écart de bouclage banque **strictement nul**, sinon une ligne a été omise).
- Chaque flux **qualifié par sa pièce** : adossé → compte définitif ; **non adossé → ATTENTE** (4711 encaissements / 4712 décaissements à justifier), **jamais en CA ni en charge**.
- **Un compte de trésorerie par moyen** : 521 banque · 571 caisse · **53 Mobile Money** · **5211 « 2e compte à identifier »**.
- **Origine de la caisse = le capital** non versé en banque (solde d'ouverture bancaire < capital → le reliquat est en caisse). La caisse finance les espèces ; le Mobile Money s'alimente depuis la caisse.
- **Chèque/virement absent du relevé = 2e compte bancaire** (réflexe [[client-lero-forage]] §31 : le compte fourni n'est jamais le seul) → 5211, solde créditeur = signal du relevé manquant. **Chèque transmis mais non encaissé = dette maintenue** (fournisseur non payé).
- **« Écart maîtrisé » ≠ écart nul** : un écart est maîtrisé quand il est chiffré, logé en compte d'attente nommé, mis en **DEE** et suivi. Seul le bouclage banque est nul. Zéro flux perdu, zéro flux inventé. [[posture-auditeur-detecter-irregularites]] · [[jamais-minorer-exposition-fiscale]]
- Toujours **croiser factures ↔ banque** (« est-ce que ça colle ? ») : encaissements vs factures de vente, décaissements vs factures d'achat → l'écart révèle **CA dissimulé** et **charges sans pièce**.

**Cas MIROIR — quand on N'A PAS les relevés (fréquent), mdc-expert §37.7 :** le contrôle « bouclage banque nul » n'existe pas → la trésorerie est **RECONSTITUÉE, non réconciliée** (à estampiller « à confirmer sur relevé »). On l'ancre sur les pièces (mode de paiement), les déclarations/quittances (§27), le capital. La maîtrise se prouve alors par les **triangles MDLC** (recettes ≈ encaissements, CMV, caisse ≥ 0), la cohérence pièces↔déclarations et le rétro-calcul des assiettes. **Jamais de solde bancaire inventé** pour équilibrer ; tout non-documenté → attente 471 + relevés réclamés en pièce n°1. Base **provisoire** jusqu'à réception des relevés, puis bascule en §37 et réconciliation au franc. Résultat « définitif » seulement une fois la trésorerie réconciliée sur relevé.

Cas de référence : GLOBE CÔTE D'IVOIRE (relevé UBA + pièces) — 521=7 189 997 au franc, caisse issue du capital, Mobile Money 53, 2e compte confirmé (GUIHON), ATLANTIC 29,4 M et KOFFI 14 M en attente + DEE. [[client-globe-cote-divoire]] · [[controle-coherence-fin-de-travaux]] · [[service-declarations-mensuelles-eimpots]]
