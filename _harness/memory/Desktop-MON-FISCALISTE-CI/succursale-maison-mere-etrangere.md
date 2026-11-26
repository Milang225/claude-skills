---
name: succursale-maison-mere-etrangere
description: "Succursale en CI d'un siège étranger : délai OHADA de 2 ans, flux avec le siège (intérêts non déductibles, TVA d'importation due), IRVM sur les sommes désinvesties"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9aafd489-0e3a-4736-b910-695ffef31c99
  modified: 2026-08-23T17:48:55.885Z
---

**La clé** : succursale et maison mère sont **une seule personne juridique** (AUSCGIE Art. 116 et 117). Tout en découle.

**Le risque juridique que personne ne surveille** : l'**AUSCGIE Art. 120** impose d'apporter la succursale d'une société étrangère à une **société de droit d'un État partie dans les 2 ans**, sauf dispense par arrêté du ministre du commerce. C'est un **statut de transition**. Premier réflexe sur ce type de dossier : **dater la création et vérifier le délai**.

**Fiscalement** : imposée en CI sur ses bénéfices ivoiriens (art. 2 CGI, établissement autonome — note DGI n° 01209 du 12/04/2022). **Bureau de liaison sans CA → IMF au plancher de 3 000 000 F** (notes 01209 et 03012 du 09/08/2022). **Doit émettre des FNE** : la dispense du LPF art. 145-7e ne vise que les entreprises **sans installation professionnelle en CI**.

**Les flux avec le siège** — « on ne fait pas d'affaires avec soi-même », donc hors TVA, **sauf** :
- **Importations : TVA due** par la volonté expresse de l'**art. 344 CGI**, même entre siège et succursale. Vrai sujet de trésorerie.
- **PSASM** (assistance technique du siège) : imposition **supprimée par l'art. 10 de l'AF 2006**. Un redressement sur ce motif se conteste texte en main.
- **Intérêts versés au siège : NON DÉDUCTIBLES** — prêt à soi-même.
- **Frais de siège** : double limite 5 % CA HT / 20 % frais généraux (art. 38) ; ETII sans seuil.

**IRVM** — le volet le plus sous-estimé, car il ne naît pas d'une écriture mais d'une **réintégration**. L'**art. 180-1** frappe **toute somme désinvestie et réintégrée à l'I-BIC** (hors amortissements et provisions), **même en résultat déficitaire**. Assiette naturelle chez une succursale : intérêts au siège + excédent de frais de siège + compte de liaison injustifié. Taux **15 %** (art. 182), **17,65 %** si la succursale prend l'impôt à sa charge (15/85, non déductible), **+25 %** si territoire non coopératif (art. 183 bis). **La même somme supporte l'I-BIC ET l'IRVM — c'est un cumul, pas un choix.**
→ **Non tranché, à sécuriser par écrit auprès du centre** : le sort de la **remontée du résultat après impôt**, l'art. 180-1 visant les associés/actionnaires/porteurs de parts, catégories qu'une succursale ne connaît pas.

**Comptablement** : comptabilité **autonome** tenue en CI, en français et en FCFA — un reporting au siège n'est pas une comptabilité. Relations avec le siège en **compte de liaison** (jamais client ni fournisseur), justifié flux par flux et rapproché du compte miroir. Jamais de capital social, de compte courant d'associé ni de dividendes dans ses comptes.

Module : `FORMATION_SUCCURSALE_MAISON_MERE_ETRANGERE_CI` (MC-FORM-FISC-2026-037). Voir [[conventions-fiscales-ci]], [[redevances-double-limite-5-20]], [[reflexe-retenues-source-prestataires]].
