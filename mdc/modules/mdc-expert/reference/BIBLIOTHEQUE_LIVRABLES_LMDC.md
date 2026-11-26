# BIBLIOTHÈQUE DES LIVRABLES LMDC — Compétence « Chargée de rédaction »
> Capitalisé juin 2026 d'après les modèles clients (SOFT SECURITY, MABEK, COLLEGE ST EXUPÉRY).
> Générateur branché (logo + identité) : `scripts/generate_livrable_mdc.py md dest.docx "Titre" "Client" "Ref"`. Logo : `scripts/logo-mdc.jpg`.
> RÈGLE : rebrander tout livrable à l'identité OFFICIELLE MDC (jamais « MON COMPTABLE »). Toujours FCFA + droit ivoirien/OHADA + secret professionnel.

## CATALOGUE DES LIVRABLES (structure type)

### L1 — Note méthodologique (modèle SOFT SECURITY) — réf MC-NOTE-...
Contexte+Objectifs / 5 domaines (CNPS, Fiscal, Inspection Travail, Comptable, Droit Travail) / 4 phases / Outils / Livrables / Garanties.

### L2 — Proposition financière (modèle ST EXUPÉRY) — MC-PROP-...
Rappel périmètre / Tableau montant forfaitaire FCFA / Conditions paiement / Conditions réalisation / Prochaines étapes. Validité 7 j. MDC non assujetti TVA.

### L7 — Propositions de Régularisation (modèle MABEK) — MC-REG-...
- Tableau « Résultat déclaré → après Prop A / Prop B (min/max) ».
- **PROPOSITION A (immédiate)** et **PROPOSITION B (équilibrée / recommandée)**.
- Par proposition : table écritures `Compte | Libellé | Débit (FCFA) | Crédit (FCFA)` + ligne TOTAUX (équilibre D=C).
- Chaque écriture **expliquée** (constat → base légale → impact résultat/bilan).

### L9 — Rapport de Notation de Conformité (modèle MABEK) — MC-NOT-...
Modèle prêt : `Documents/LIVRABLES AUDIT LMDC/03_NOTATION_RAPPORTS/MODELE_NOTATION_CONFORMITE_MDC.docx`.
1. Synthèse exécutive (note A→E, anomalies par sévérité, exposition FCFA).
2. Score global + détail par domaine (pondérations 20/20/20/15/15/10).
3. Tableau de bord anomalies (Sévérité | Domaine | Anomalie | Base légale | Exposition FCFA) + TOTAL.
4. Analyse détaillée par anomalie (constat / base légale / exposition redressement / 💡 recommandation).
5. Plan d'action priorisé (URGENT/PRIORITAIRE/NORMAL, J+7→J+60, coût, responsable).
6. Conclusion + note + note cible après régularisation.

### Rapport Postes Significatifs > 10M (modèle COLLEGE ST EXUPÉRY) — MC-RPS-...
Bandeau logo MDC / Vue d'ensemble postes > seuil / Tableaux comparatifs N-2/N-1/N (Actif, Passif, Capitaux, Résultat) / Analyse poste par poste / variations significatives.

### L3 Rapport intermédiaire · L4 Dossier audit 5 axes · L5 Reconstitution (balance+CR) · L8 Étude fiscale · L10 Présentation · L11 Visa
→ cf. SKILL §1, §13, §15, §21 + scripts openpyxl.

### Autres : Contrat de prestation (FABELLASHOP) · Courrier officiel (LERO)
Word MDC, en-tête + identité + objet + corps + signature gérant.

## BRANDING (obligatoire sur tout livrable)
- **Bandeau** : logo MDC (navy/or) + « LA MAISON DE LA CONFORMITÉ SARL » + sous-titre « Votre partenaire en conformité ».
- **Bloc titre** navy + barre or : Titre / Client / Réf / « Devise : FCFA · Droit ivoirien & OHADA ».
- **Pied** : NCC 2506426B · RCCM CI-ABJ-03-2025-B13-10831 · Capital 1 000 000 FCFA · Tél 07 19 31 49 04 · mail/site · « Confidentiel — secret professionnel ».
