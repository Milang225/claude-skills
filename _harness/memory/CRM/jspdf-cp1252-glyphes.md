---
name: jspdf-cp1252-glyphes
description: "Piège jsPDF (admin MDC) — police Helvetica = CP1252, tout caractère hors CP1252 casse le rendu PDF"
metadata:
  node_type: memory
  type: project
  originSessionId: 44b0d6d5-40e2-42cc-bd26-efb4326bce2b
  modified: 2026-10-05T14:48:03.308Z
---

Les PDF générés **côté navigateur** par l'admin MDC (`/var/www/mdc/admin/index.html`, ex. `payDownloadPDF()` = simulation de paie) utilisent **jsPDF 2.5.1 + autotable** avec la police **Helvetica standard = encodage WinAnsi/CP1252**. Dès qu'une chaîne passée à `doc.text`/`autoTable` contient un caractère **hors CP1252**, jsPDF bascule la chaîne entière en rendu 2 octets → **glyphes cassés + espacement caractère-par-caractère** sur toute la ligne.

Caractères coupables rencontrés (incident 05/10/2026) :
- ` ` (espace fine insécable émise par `toLocaleString('fr-FR')`) → séparateur de milliers rendu « / » (« 1/000/000 »)
- `−` (vrai signe moins) → rendu « " »
- `↪` (flèche ↪, puce de sous-ligne) → rendu « !ª »
- OK en CP1252 (ne cassent pas) : `—` U+2014, `–` U+2013, `•` U+2022, `·` U+00B7

**Correction déterministe** (pas d'IA, pas de police embarquée) : n'émettre que du CP1252.
- `fmt` : `.toLocaleString('fr-FR').replace(/[   ]/g,' ')` avant d'ajouter « FCFA »
- signe moins : `'-'` ASCII (U+002D)
- puce de sous-ligne : `•` (U+2022, présent dans CP1252)

Les générateurs **DOCX** (ex. `generateContratTravailDOCX`) et le **texte brut** des e-mails ne sont PAS concernés : Word et le texte affichent ` `/`−` correctement.

Vérification obligatoire : régénérer le PDF en Node (jspdf installé en scratchpad) + rendu image AVANT de déployer — voir [[prefs-documents-charte]]. index.html est statique → l'utilisateur doit faire `Cmd+Shift+R`. Déploiement : voir [[crm-architecture-deploy]].
