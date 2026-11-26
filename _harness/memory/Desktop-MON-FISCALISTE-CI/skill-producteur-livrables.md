---
name: skill-producteur-livrables
description: "Skill dédié à la PRODUCTION des livrables MDC (en aval des skills de fond) — chef de production : mise en forme, règle d'or, rangement, transmission"
metadata: 
  node_type: memory
  type: reference
  originSessionId: c3c001b6-a642-4b04-ae47-9c68316ff5e7
  modified: 2026-08-15T00:15:44.407Z
---

Le skill **`producteur-livrables`** (créé août 2026) est le **chef de production des livrables MDC**. Il intervient **EN AVAL** des skills de fond ([[chemin-audit-8-phases]] mdc-expert, auditeur-fiscal, auditeur-superieur, notateur-conformite, comptable-ebnl / droit du travail & social, rédaction) : ceux-ci produisent la MATIÈRE (calculs, analyses, droit, textes), lui la transforme en **documents finis, contrôlés, rangés et transmis**.

**Quand il se déclenche :** « produis / sors / génère / mets au propre / finalise les livrables ou le dossier de livraison », « regroupe les fichiers à envoyer », « édite en Word/PDF/Excel ».

**Ce qu'il fait :** chaîne fond → production (pipeline règle d'or : `publish_livrable_mdc.py`, `publish_pdf_mdc.py`, `xlsx_to_pdf_mdc.py`, `blocs_mdc.py`) → contrôle qualité + cohérence dossier ([[controle-coherence-fin-de-travaux]]) → rangement (dossier client + « À ENVOYER », sources `.md` conservées) → transmission (brouillon Gmail, [[preparer-courrier-en-brouillon-gmail]], [[mails-jamais-joindre-exposition]]).

**Catalogue (20+ types)** né du dossier GLOBE : comptabilité, écritures (à supprimer/bonnes écritures), transmission comptable, analyse de relevé, étude comparative factures↔banque, audit des déclarations par période, bordereaux, détail & point des impôts, annexes EDI par nature, reporting de gestion (mensuel/trimestriel/semestriel), DEE, notes de conformité, rapport de mission, manuel de procédure, calendrier des obligations, demandes de pièces/factures, documents commerciaux, outils (suivi collecte + PV), volet social. Liste ouverte. Ne fait PAS le fond ; renvoie au skill compétent si la matière manque. Règle d'or : s'il ne passe pas le contrôle, pas de document. [[regle-dor-controle-livrables]] · [[base-documentaire-lmdc]]

**DEUX skills producteurs (routage par type de mission)** — capital, ne pas confondre :
- **`producteur-livrables`** (générique) = **suivi / déclarations MONO-exercice** (ex. GLOBE) ;
- **`producteur-livrables-audit`** (spécialisé) = mission d'**AUDIT de conformité / reconstitution MULTI-exercices** (ex. **COLLÈGE SAINT-EXUPÉRY**), de la note méthodologique au **visa OU constat de non-conformité** ; porte la structure de dossier normalisée (`00_PIECES_RECUES`→`09_SUIVI_ET_VISA`), la convention `MC-⟨TYPE⟩-⟨SECT⟩-⟨AN⟩-NNN`, et les **générateurs graphiques reportlab** (`build_treso.py`, `build_visa.py`, `build_constat.py`…). Livrables emblématiques : MC-ETAT, MC-TRESO (« compte juste ou faux ? »), MC-VIS (relevé en images), MC-CRX, MC-ING (réserves), MC-VISA / MC-NCF (une seule émise selon la note).

**RÉVISION R1 (août 2026)** du skill générique : §8 devient un **aide-mémoire de routage** (reconnaître les 7 livrables d'audit et **renvoyer** vers `producteur-livrables-audit`, ne PAS dupliquer le catalogue) + §9 packs (A audit → skill audit ; B mono-exercice → ce skill). Cohérence propagée à **mdc-expert §38** et **auditeur-superieur** (les deux routent désormais vers le bon producteur). ⚠️ Visa/constat ne sont PAS des MD→PDF : générateur reportlab dédié.
