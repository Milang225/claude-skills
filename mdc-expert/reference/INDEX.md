# INDEX MAÎTRE — Skill mdc-expert (LA MAISON DE LA CONFORMITÉ SARL)
> Point d'entrée. À LIRE en début de session. Tout en FCFA, droit ivoirien/OHADA. Papier à en-tête MDC obligatoire sur tout livrable.

## 1. DOCTRINE SOURCÉE (ouvrages assimilés)
- ⭐ `FICHE_SYNOPTIQUE_CALENDRIER_DGI.md` — **RÉFÉRENCE DE PREMIER RECOURS** : synoptique DGI (taux/base/exonérations/articles, Éd. AF 2025) + calendrier des obligations (délais). **Fait foi** pour la grille des régimes (TCE/TEE/RME/RSI/RNI), le barème ITS/RICF, et les **charges patronales (CE local exonérée, total local 2,8 % / expat 12 %)**.
- `FICHE_TVA_TOB_TSE_AIRSI.md` — taxes sur le CA
- `FICHE_IMPOTS_BENEFICES.md` — IS/IMF, régimes RE/RME/RSI/RNI (doctrine détaillée AF 2024)
- `FICHE_COMPTA_SYSCOHADA.md` — écritures, états, SIG
- `FICHE_SYSCOHADA_IFRS.md` — divergences, retraitements
- `FICHE_FISCALITE_AGRICOLE.md` · `FICHE_GROUPAGE_IMPORT_TRANSITAIRE.md` — fiscalité sectorielle
- `NOTE_CODES_REGIMES_DGI.md` — codes régime fiche R2 (code 3 = ex-synthétique obsolète)
- ⭐ `FICHE_DECLARATIONS_EIMPOTS_EDI_EFI.md` — **TÉLÉDÉCLARATION e-impôts** : 62 natures d'impôt champ par champ (EFI maître + 10 annexes EDI), workflow saisie hors-ligne → XML → injection. Base du **moteur de déclarations mensuelles** (données comptables → formulaire rempli). Modèles : `Desktop/MON FISCALISTE CI/MODELES_DECLARATIONS_EIMPOTS_CI.xlsx` (66 onglets) + reproduction HTML. Calendrier/échéances → `FICHE_SYNOPTIQUE_CALENDRIER_DGI.md` Partie B.

## 2. CŒUR DE MÉTIER
- `METHODE_RECONSTITUTION_BASE_COMPTABLE.md` — états financiers → base → balance + CR (mapping inverse)  [SKILL §21]
- `CAS_FAMILLE_KRA_ex-mon-comptable.md` — cas de référence matrice d'anomalies

## 3. PROCÉDURE D'AUDIT (implémentable A→Z)  [SKILL §24]
- `FICHE_USINE_LIVRABLES_AUDIT.md` — **VUE MAÎTRESSE** : tous les livrables (validés + proposés), emplacements, feuille de route, références MC
- `FICHE_AUDIT_DOCUMENTAIRE_AXE_I.md` — LI-0 (A1-A24 / B1-B68 / C1-C64) + formulaire XLSX
- `LIVRABLES_INTERMEDIAIRES_AUDIT.md` — 12 livrables LI-1..LI-12 + enchaînement  [SKILL §23]
- `MANUEL_PROCEDURE_MISSION_CONFORMITE.md` — objectifs & livrables
- Manuel équipes : `Documents/LIVRABLES AUDIT LMDC/00_MANUELS_PROCEDURES/MANUEL_AUDIT_EQUIPES_MDC.docx`

## 4. RÉDACTION DES LIVRABLES  [SKILL §22]
- `BIBLIOTHEQUE_LIVRABLES_LMDC.md` — structures (Note, Proposition, Notation, Régularisation, Rapport postes)
- Générateur : `scripts/generate_livrable_mdc.py md dest.docx "Titre" "Client" "Réf"` (en-tête logo + pied identité)

## 5. MÉMOIRE & RÈGLES
- `MEMOIRE_FISCALE.md` — cœur de métier, préférences, règles permanentes (FCFA, droit ivoirien, papier à en-tête), notions validées, journal

## CHAÎNE D'AUDIT STANDARD
Cadrage → AXE I (LI-0) → LI-1..LI-12 → Reconstitution (balance+CR) → Matrice anomalies + contradiction → Étude fiscale + exposition → CLÔTURE → Notation A→E (grilles) → Exposition au redressement (coût FCFA) → Plan d'action → Visa.
Quality gates : bouclage (Actif=Passif, CR=Bilan, ΣD=ΣC) · sourcing article par article · contradiction · REG équilibrées.
