---
name: Capitalisation systématique des compétences MDC
description: Toute nouvelle compétence acquise lors d'une mission MDC doit être consignée dans le SKILL.md mdc-expert et les scripts persistés dans son sous-dossier scripts/
type: feedback
originSessionId: bf088578-8311-421f-8897-60f2abc8862e
---
**Règle** : toute méthodologie, référentiel juridique, charte ou script utilitaire qui émerge d'une mission client MDC doit être **immédiatement capitalisé** dans le skill mdc-expert pour réutilisation future.

**Why** : lors de la mission TIM 7 MULTISERVICE (mai 2026), l'utilisateur a demandé explicitement « acquière la compétence qui t'a permis de faire ce travail ». Il considère que le cabinet doit accumuler son savoir-faire et que chaque mission est une occasion d'enrichir le référentiel interne. Sans capitalisation, le travail est à refaire à chaque fois.

**How to apply** :

1. **Si une nouvelle expertise juridique / fiscale / comptable est mobilisée** : ajouter une nouvelle section au `~/.claude/skills/mdc-expert/SKILL.md` (numérotée), avec articles clés, matrice d'anomalies systémiques, livrables types et chiffrage indicatif.

2. **Si une charte graphique est définie** : la consigner dans la Section 8 du SKILL.md (palette, typographie, mise en forme par type de tableau, mentions obligatoires).

3. **Si un script Python utilitaire est produit** : le copier de son emplacement temporaire vers `~/.claude/skills/mdc-expert/scripts/` avec un nom générique (sans nom de client), et le référencer dans la Section 9 du SKILL.md.

4. **Toujours mettre à jour la Section 10** (« Règle d'or ») avec le précédent capitalisé : « Mission [CLIENT] ([date]) → Section X (sujet) ».

**Précédents capitalisés** :
- Mission TIM 7 MULTISERVICE (mai 2026) → Section 7 (Audit contrats de travail droit ivoirien) + Section 8 (Charte graphique unifiée) + Section 9 (Scripts utilitaires md_to_docx_mdc, redesign_excel_mdc_template, build_mdc_propositions_template)
