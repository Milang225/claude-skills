# Catalogue détaillé des livrables d'audit — MDC

> Détail de chaque livrable : objet, contenu attendu, dépendances, forme. Complète la table du SKILL.
> Ordre = ordre de production dans une mission. `⟨SECT⟩` = code secteur du client.

## PHASE 0 — CADRAGE & DÉMARRAGE

### Note méthodologique d'audit — MC-NOTE-⟨SECT⟩-⟨AN⟩-NNN
La promesse au client. Contexte sectoriel, 4 objectifs, 5 domaines évalués (CNPS, fiscal, inspection,
comptable, droit du travail), 4 phases, outils, livrables promis, garanties. 4-5 pages. Produite avec la
proposition financière. Fond : mdc-expert §6.4/§11.4.

### Note méthodologique de pilotage — MC-PIL-⟨SECT⟩
Cadrage interne (équipe MDC) : qui fait quoi, séquencement, points de vigilance du dossier. Non destinée
au client. Fond : auditeur-superieur.

### Proposition financière d'audit — MC-PROP-⟨AN⟩-NNN (compteur global)
Périmètre + prix forfaitaire + conditions (paiement intégral avant travaux) + délai. 2 pages. La
référence suit le compteur GLOBAL des propositions, pas le secteur.

### Note de démarrage / de reprise d'audit — MC-NDM / REPRISE
Ouvre (ou reprend) la mission après signature : périmètre, interlocuteurs, calendrier, renvoi à la
demande de pièces. Fond : auditeur-superieur.

### Demande de pièces initiale — MC-DEM-⟨SECT⟩-⟨AN⟩-001
Premier temps : identité minimale + pièces de priorité 1 (états financiers, relevés). Fond :
methodologie-audit (catalogue des pièces).

### Demande de pièces consolidée — MC-DEM-⟨SECT⟩-⟨AN⟩-002
Les 7 domaines de pièces en liste à cocher, avec période attendue et priorité. C'est la version
exhaustive, envoyée après la première prise d'information.

### Manuel des inventaires — MC-INV-⟨SECT⟩
Protocole des inventaires de mission (immobilisations, stocks, personnel, éléments comptables) :
comptage en binôme, fiches signées, valorisation. Fond : methodologie-audit.

## PHASE 1 — DIAGNOSTIC & INTERMÉDIAIRE

### Rapport intermédiaire d'analyse — MC-RAPP-⟨SECT⟩
Premières alertes après collecte + tests de bouclage + liste des pièces manquantes. Analyse financière
et fiscale des exercices disponibles. C'est la première livraison si les états ne bouclent pas.

### État détaillé de la situation — MC-ETAT-⟨SECT⟩
Photographie chiffrée : CA reconstitué, entrées et sorties catégorisées, résultat, écarts déclaré/réel,
décisions à prendre. Fond : mdc-expert + auditeur-superieur.

## PHASE 2 — ANALYSES PAR PÔLE

### Analyse du relevé bancaire — MC-ANABANK
Entrées et sorties catégorisées en partition exhaustive, recoupées aux totaux imprimés de la banque.
Toujours vérification croisée obligatoire (Σ catégories = total banque). Version DOCX/PDF + classeur XLSX
4 onglets. Fond : mdc-expert §2/§16.

### Synthèse visuelle du relevé — MC-VIS-⟨SECT⟩ (une par exercice)
Le relevé « en images » : donut des catégories, barres mensuelles, top bénéficiaires. Générateur reportlab
dédié. Filigrane CONFIDENTIEL. Pour lecture rapide par la Direction.

### Rapport d'analyse des versements d'espèces — MC-APP-⟨SECT⟩
Volumétrie des APPRO, déposants identifiés, poids dans les encaissements, saisonnalité (test du calendrier
d'activité), test de couverture par les retraits. Débouche sur la qualification (recettes vs apport).
Fond : mdc-expert §31.

### Note de qualification (compte courant d'associé) — MC-CCA-⟨SECT⟩
Expose le risque de requalification des versements en compte courant d'associé, pourquoi cette thèse est
défavorable (origine des fonds, disproportion capital, imposition des sorties), et la PROCÉDURE pour
verrouiller la qualification en recettes (grille tarifaire, reçus numérotés, journal de caisse,
écriture via compte de créances, rapprochement). Fond : auditeur-fiscal / superieur.

### Rapport de trésorerie pluriannuel — MC-TRESO-⟨SECT⟩
« Le compte est-il juste ou faux ? » Courbe de trésorerie sur N années, test de sincérité (trésorerie
liasse vs solde bancaire à chaque clôture), comptes multiples (compte à terme). Générateur reportlab.

### Reconstitution comptable
Base → balance → CR → bilan reconstitués depuis les états/relevés. XLSX + PDF paysage. Bouclage
obligatoire. Fond : mdc-expert §13/§21.

### Étude comparative & preuves du CA — MC-CRX
Comparaison bilan/CR N vs N-1, dossier de preuves du CA reconstitué (rapprochement encaissements ↔ CA).
Fond : mdc-expert §37.

## PHASE 3 — CONSOLIDATION & CHIFFRAGE

### Rapport d'observations (matrice d'anomalies) — MC-OBS-⟨SECT⟩
Toutes les observations codées (P/A/R/T/N/F/S), cotées (critique/majeur/moyen), avec cause, base légale
et chiffrage. C'est le support de la notation. Fond : notateur-conformite.

### Rapport d'exposition au redressement — MC-EXPO-⟨SECT⟩
Risque fiscal chiffré : Bloc A (sorties requalifiées — IRVM, retenues), Bloc B (taxation du CA par
tranche, arriérés inclus), scénarios favorable/médian/haut, taxation d'office et majoration 100 %.
Générateur reportlab. **Document sensible → remise séparée.**

### Rapport d'ingénierie des réserves & capitaux propres — MC-ING-⟨SECT⟩
Traitement des réserves : apurement des pertes (gratuit), incorporation au capital (droit 6 %),
distribution (IRVM 15/17 %), réévaluation libre. Risque de requalification en distribution occulte.
Fond : mdc-expert / superieur. **Document sensible.**

## PHASE 4 — NOTATION & CLÔTURE

### Rapport de notation — (réf. notation)
Grille AAA→D par domaine et globale, motivée par les observations. Fond : notateur-conformite. Débouche
sur le visa (si ≥ A) ou le constat (si < A).

### Visa de conformité — MC-VISA-⟨SECT⟩ / Constat de non-conformité — MC-NCF-⟨SECT⟩
Le visa (note ≥ A) atteste la conformité ; le constat (note < A) est délivré en lieu et place, avec les
motifs du refus, la note par domaine et le renvoi au plan de remédiation. Générateurs reportlab dédiés
(certificat A4, médaillon de note, tableau des domaines, cachet). Le visa vierge de démonstration porte
un filigrane SPECIMEN ; un constat nominatif réel n'en porte pas.

### Note de clôture de mission — MC-NOTE-⟨SECT⟩-⟨AN⟩-002
Conclusion générale, stratégie de sortie (changement de régime, apurement), synthèse des chiffres-clés.

### Recommandations finales & feuille de route — MC-RECO-⟨SECT⟩
Les axes d'action priorisés et le calendrier. Fond : auditeur-superieur.

### Sommaire du dossier — SOMMAIRE
Recense tous les livrables, l'ordre de lecture, les 5 chiffres à retenir, la conclusion en une phrase.
Produit par ce skill, en dernier, à la racine du dossier.

## PHASE 5 — SUITE DE MISSION (si accompagnement post-audit)

### Feuille de route vers le visa — MC-FDR-⟨SECT⟩
Chemin chiffré de la note actuelle vers A : mécanique de la note, situation de départ, actions par
domaine avec preuve exigée, jalons datés, conditions du visa. Fond : notateur / superieur.

### Plan d'action — MC-PLA-⟨SECT⟩
Organisation cible (qui fait quoi), procédures à installer, calendrier, décisions que la Direction doit
prendre. Fond : auditeur-superieur.

### Politique prestataires & fournisseurs — MC-BPP-⟨SECT⟩
Règles de collaboration au régime réel : facture normalisée, seuil espèces, retenues à la source,
qualification des partenaires, procédure d'engagement des dépenses. Fond : mdc-expert (retenues).

### Propositions & contrat — MC-PROP-⟨AN⟩-NNN / MC-CONT-⟨SECT⟩
Proposition commerciale de suivi (honoraire mensuel), proposition financière des missions de mise en
place (forfait), contrat de prestation unique liant les deux. Fond : mdc-expert §6.

---

## DÉPENDANCES (ordre imposé)

1. États financiers d'abord (sources) → sans eux, rien ne boucle.
2. Relevé bancaire → CA réel → trésorerie.
3. Reconstitution comptable → observations (anomalies).
4. **Notation → exposition → plan d'action** (jamais l'inverse).
5. Visa/constat en tout dernier, après consolidation.
6. Le Sommaire se génère à la fin, quand le dossier est complet.

## CHIFFRES PIVOTS À TENIR IDENTIQUES DANS TOUT LE DOSSIER

CA déclaré · CA reconstitué · résultat déposé · exposition (principal et taxation d'office) · note de
conformité · trésorerie (pic et clôture) · réserves après apurement. Avant toute remise : `grep` de ces
montants sur l'ensemble du dossier ; un écart = retour à la pièce source, pas d'arbitrage de mémoire.
