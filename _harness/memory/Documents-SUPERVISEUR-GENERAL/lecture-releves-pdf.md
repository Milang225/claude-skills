---
name: lecture-releves-pdf
description: 23/11 — les relevés PDF scannés sont lus par OCR, et chaque ligne est vérifiée par la colonne du solde
metadata:
  type: project
---

`releve_pdf.py` lit les relevés bancaires en PDF, y compris les scans : tesseract 5.3.4 avec le français est installé sur le serveur, PyMuPDF rend les pages à 250 dpi.

**La règle qui rend l'OCR acceptable en audit :** rien n'est cru sur parole. Le mouvement de chaque ligne est calculé comme la différence des soldes, le montant lu doit y correspondre, sinon la ligne est signalée et n'est pas importée. Le sens vient du solde (il monte = entrée). Le solde de clôture et les totaux servent de second contrôle. Une ligne douteuse ne contamine pas les suivantes : on se recale sur le solde lu.

Deux pièges résolus : les nombres se lisent par groupes de trois (« NATIONAL 1 50 000 » n'est pas 150 000), et les soldes se cherchent ligne par ligne, jamais dans le texte entier. Les relevés de 2023 disent « Solde début », ceux de 2024-2025 « Solde précédent ».

**Mesure sur les vrais relevés :** 27 relevés ORABANK de LBTECH (2023 à 2025), **27 sûrs sur 27, 204 opérations lues et 204 vérifiées**.

**Why :** le gérant n'a que des scans ; sans cela, les exercices 2023 et 2024 restaient vides et les rapprochements ne pouvaient rien conclure. Voir [[plusieurs-releves-registre]].
