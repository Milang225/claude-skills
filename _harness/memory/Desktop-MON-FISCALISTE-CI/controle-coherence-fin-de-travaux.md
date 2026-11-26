---
name: controle-coherence-fin-de-travaux
description: "Après CHAQUE travaux, lancer le contrôle de cohérence du dossier — aucun livrable ne doit contredire les autres"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fe4f2f95-a69c-4364-85d9-367f608bcc60
  modified: 2026-07-24T00:24:13.466Z
---

**Après chaque travaux — pas seulement en fin de mission — lancer le contrôle de cohérence du dossier client :**

```bash
python3 ~/.claude/skills/mdc-expert/scripts/controle_coherence_dossier.py "DOSSIER CLIENT" \
    --perimes <montants corrigés> --cles <montants définitifs> \
    --maitres "EXERCICE AAAA" --terminaux RAPPORT_,NOTE_ --exempts CONTROLE,AUDIT_FISCAL
```

Quatre contrôles : ① montants périmés survivants (bloquant) · ② propagation des chiffres définitifs dans les livrables terminaux · ③ copies de diffusion plus anciennes que leur maître (bloquant) · ④ livrables sans PDF. Code retour 1 si anomalie bloquante — chaînable avant une remise.

**Why:** le gérant l'a demandé le 24/07/2026 sur LERO (« cette manière de faire là, que tu puisses le faire après chaque travaux »). Le dossier comptait 122 livrables Word et Excel diffusés dans quatre répertoires ; l'exposition avait changé cinq fois (128 962 819 → 119 651 114 → 123 770 683 → 135 209 513 → **145 523 033**) et quatre documents portaient encore un impôt minimum minoré corrigé depuis. Deux documents du même dossier qui affichent deux chiffres différents ruinent la crédibilité de tout le travail, y compris la partie juste.

**How to apply:**
- **Noter les montants périmés au fil de l'eau** pendant la session, jamais de mémoire à la fin.
- **Conserver la source markdown de tout `.docx`** à côté du dossier client : un Word publié sans sa source n'est plus corrigeable, il faut le réécrire entièrement (c'est ce qui est arrivé à quatre livrables LERO).
- Corriger → rafraîchir les copies depuis les maîtres → régénérer les PDF → **relancer jusqu'au vert** → committer.
- **Un contrôle qui allège le dossier doit être vérifié deux fois** : sur LERO il a fait *monter* l'exposition de 10 313 520 (assiette 2026 assise sur le CA facturé au lieu du réel, cotisations sociales omises). C'est le sens normal d'un contrôle honnête. [[jamais-minorer-exposition-fiscale]]

Procédure complète : skill `mdc-expert` **§34**. Maillon final de la chaîne §24 → §14 → skill `auditeur-fiscal` → §34 → remise. [[regle-dor-controle-livrables]] [[client-lero-forage]]
