---
name: systeme-comptable-dossier
description: la plateforme ignore le système comptable (SN/SMT/entreprenant) ; note MC-NS-2026-010 du 07/11/2026 liste 6 constats et 6 évolutions, non codées
metadata:
  type: project
---
Au 07/11/2026, aucun champ « système comptable » sur le dossier (seuls regime fiscal + mode_tenue). Le générateur contracte les lignes du journal portail sans tiers, le contrôle E3 est codé en dur « ok », la TVA est débitée en 445200 même sur espèces > 250 000 (D14 alerte mais le générateur ne suit pas), une date 0202 a été acceptée.
Note de service MC-NS-2026-010 (SUPERVISEUR GENERAL/NOTES_EVOLUTION_PLATEFORME + copie BASE DOCUMENTAIRE LMDC/NOTES_INTERNES) : règle de détermination (AUDCIF art. 11/13, seuils HT 60/40/30 M strictement inférieur, « sauf option » ; AUDCG 30-32) et évolutions E1-E6.
**Why:** le gérant : « si on rate ça, on se perd » — le système comptable commande écritures, journaux et liasse.
**How to apply:** ne pas coder sans accord (notes seulement demandées) ; point de doctrine ouvert : TFT en SMT (art. 29 vs chapitre SMT). Fiche skill FICHE_COMPTA_SYSCOHADA ligne 13 à corriger (« sauf option »). Voir [[base-comptable-crm]], [[journal-portail-ecritures]], [[pre-controle-anti-redressement]].
Suite 07/11/2026 : l'informaticien intègre via un PROMPT (pas un patch) → NOTES_EVOLUTION_PLATEFORME/PROMPT_INFORMATICIEN_SYSTEME_COMPTABLE(.zip) : règles R1-R36 (R29-R36 = opérations À CRÉDIT, demandées par le gérant : « ne l'oublie pas ») + code de référence 29 tests. Ne pas oublier le crédit dans toute règle d'écriture future.
