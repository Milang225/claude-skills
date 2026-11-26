#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detecter_points.py — DÉTECTEUR DE POINTS À ÉCLAIRCIR (skill points-a-eclaircir, MDC).

Scanne une base comptable Excel (feuille Journal) et remonte :
  1) tous les flux logés en comptes d'ATTENTE (4711/4712/471/409/5211) → à soumettre en DEE ;
  2) les écritures qui PRÉJUGENT d'une nature (462 compte courant, 465 dividendes, 411/701 sur un
     flux non justifié…) → À BASCULER EN ATTENTE avant de dresser la DEE (règle §37.10).

Sortie :
  - un rapport lisible à l'écran ;
  - un scaffold JSON (points_detectes.json) pré-rempli, à compléter puis passer à dresser_dee.py.

Usage :
  python3 detecter_points.py "CHEMIN/COMPTA.xlsx" [--journal "2-Journal"] [--json points_detectes.json]

Aucune dépendance hors openpyxl. Ne modifie jamais la base : lecture seule.
"""
import sys, json, argparse, re
from collections import defaultdict

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl requis : pip install openpyxl")

# Comptes d'attente légitimes (à soumettre en DEE)
ATTENTE = {
    '4711': "Encaissements à justifier",
    '4712': "Décaissements à justifier",
    '471':  "Écart de rapprochement / période à justifier",
    '409':  "Fournisseurs, avances versées (facture à obtenir)",
    '5211': "Banque — 2e compte à identifier",
}
# Comptes de QUALIFICATION : leur présence sur un flux non justifié est un signal d'alerte
QUALIF_RISQUE = {
    '462': "Compte courant d'associé — QUALIFICATION (un prélèvement dirigeant sans pièce doit rester en 4712)",
    '465': "Dividendes à payer — QUALIFICATION (une distribution suppose un PV d'AGO)",
}
MOTS_DIRIGEANT = re.compile(r"g[ée]rant|associ[ée]|dirigeant|apporteur", re.I)


def col_index(header_row):
    """Retrouve les colonnes Compte / Libellé / Débit / Crédit / Date depuis une ligne d'en-tête."""
    idx = {}
    for j, v in enumerate(header_row):
        s = str(v).strip().lower() if v is not None else ""
        if s.startswith("compte"): idx['compte'] = j
        elif s.startswith(("intitul", "libell")): idx.setdefault('lib', j)
        elif s.startswith("d") and "bit" in s: idx['debit'] = j
        elif s.startswith("cr") and "dit" in s: idx['credit'] = j
        elif s.startswith("date"): idx['date'] = j
        elif s.startswith(("lib",)) : idx.setdefault('lib', j)
    return idx


def num(v):
    if v in (None, ""): return 0.0
    if isinstance(v, (int, float)): return float(v)
    return float(str(v).replace(" ", "").replace(" ", "").replace("\xa0", "").replace(",", "") or 0)


def racine(c):
    m = re.match(r"(\d+)", str(c)); return m.group(1) if m else str(c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("--journal", default=None, help="nom de la feuille Journal (auto-détecté sinon)")
    ap.add_argument("--json", default="points_detectes.json")
    ap.add_argument("--client", default="[CLIENT]")
    ap.add_argument("--ref", default="MC-DEE-[SECT]-[AN]-NNN")
    a = ap.parse_args()

    wb = openpyxl.load_workbook(a.xlsx, data_only=True)
    jname = a.journal or next((s for s in wb.sheetnames if "journal" in s.lower()), wb.sheetnames[0])
    ws = wb[jname]
    rows = list(ws.iter_rows(values_only=True))
    # trouver l'en-tête
    hrow = next((i for i, r in enumerate(rows) if r and any(str(c).strip().lower().startswith("compte") for c in r if c)), 0)
    idx = col_index(rows[hrow])
    if 'compte' not in idx:
        sys.exit(f"Colonne 'Compte' introuvable dans la feuille {jname}. En-tête lu : {rows[hrow]}")

    attente = defaultdict(list)   # compte -> [(date, lib, montant, sens)]
    alertes = []                  # (compte, date, lib, montant, motif)

    for r in rows[hrow + 1:]:
        if not r or idx['compte'] >= len(r): continue
        cpt = r[idx['compte']]
        if cpt in (None, ""): continue
        cpt = str(cpt).strip()
        d = num(r[idx['debit']]) if 'debit' in idx and idx['debit'] < len(r) else 0
        c = num(r[idx['credit']]) if 'credit' in idx and idx['credit'] < len(r) else 0
        if d == 0 and c == 0: continue
        lib = str(r[idx['lib']]) if 'lib' in idx and idx['lib'] < len(r) and r[idx['lib']] else ""
        dat = str(r[idx['date']]) if 'date' in idx and idx['date'] < len(r) and r[idx['date']] else ""
        rc = racine(cpt)
        # attente
        for code in ATTENTE:
            if cpt == code or rc == code:
                attente[code].append((dat, lib, d - c))
                break
        # alerte qualification
        for code, motif in QUALIF_RISQUE.items():
            if (cpt == code or rc == code):
                flag = "  ⚠ bénéficiaire dirigeant/associé" if MOTS_DIRIGEANT.search(lib) else ""
                alertes.append((cpt, dat, lib, d - c, motif + flag))

    # ---- rapport écran ----
    print(f"\n=== DÉTECTION POINTS À ÉCLAIRCIR — {a.xlsx} (feuille {jname}) ===")
    print(f"\n▸ FLUX EN ATTENTE (à soumettre en DEE) :")
    if not attente:
        print("   (aucun compte d'attente mouvementé)")
    for code, items in sorted(attente.items()):
        tot = sum(m for *_, m in items)
        print(f"  • {code} {ATTENTE[code]} — {len(items)} ligne(s), solde {tot:,.0f}")
        for dat, lib, m in items:
            print(f"      {dat:12} {m:>14,.0f}  {lib[:70]}")
    print(f"\n▸ ALERTES QUALIFICATION (à BASCULER en attente AVANT la DEE — règle §37.10) :")
    if not alertes:
        print("   ✅ aucune écriture qualificative détectée sur un flux sensible")
    for cpt, dat, lib, m, motif in alertes:
        print(f"  ⚠ {cpt} {dat} {m:>14,.0f}  {lib[:55]}\n       → {motif}")

    # ---- scaffold JSON pour dresser_dee.py ----
    LABELS = {'4711': "Encaissements en attente de justification (compte 4711)",
              '4712': "Décaissements en attente de justification (compte 4712)",
              '471':  "Écart de rapprochement / période à justifier (compte 471)",
              '409':  "Achats réglés sans facture — avances fournisseurs (compte 409)",
              '5211': "Paiements depuis un autre compte — relevés à obtenir (compte 5211)"}
    sections = []
    for code, items in sorted(attente.items()):
        tot = sum(m for *_, m in items)
        sections.append({
            "titre": LABELS.get(code, f"Compte {code}"),
            "intro": f"Inscrits en {ATTENTE[code].lower()} — non qualifiés tant que la justification n'est pas produite.",
            "colonnes": ["Date", "Libellé", "Montant (FCFA)", "Explication demandée"],
            "lignes": [[dat, lib, f"{abs(m):,.0f}".replace(",", " "), "[QUESTION À PRÉCISER]"] for dat, lib, m in items],
            "total": ["", f"Total {code}", f"{abs(tot):,.0f}".replace(",", " "), ""],
            "note": ""
        })
    # une section exposition pré-remplie si un flux dirigeant est en attente/alerte
    if alertes or any("gérant" in l.lower() or "associ" in l.lower() for its in attente.values() for _, l, _ in its):
        sections.append({
            "titre": "Prélèvement au profit du dirigeant — nature à établir et exposition",
            "type": "exposition",
            "intro": "Ce flux n'est appuyé par aucune pièce : il reste en attente, NON qualifié. Chaque hypothèse emporte une exposition différente.",
            "colonnes": ["Hypothèse (à confirmer)", "Traitement", "Exposition estimée", "Base légale (CGI)"],
            "scenarios": [
                ["Distribution / prélèvement sur bénéfices", "revenu réputé distribué → IRVM", "15 % du montant (+ pénalités si tardif)", "Art. 180-183"],
                ["Rémunération du dirigeant", "ITS (barème) + bulletin + CN/FDFP", "selon barème", "Art. 115-120"],
                ["Remboursement d'une avance antérieure", "neutre", "néant (sur preuve de l'avance)", "—"],
                ["Prêt / avance au dirigeant", "à rembourser ; requalification possible", "IRVM si requalifié", "Art. 180"],
            ]
        })
    config = {
        "client": a.client,
        "reference": a.ref,
        "remplace": "",
        "destinataire": f"Monsieur le Gérant de {a.client}",
        "objet": "Éléments du dossier comptable nécessitant vos explications avant traitement définitif",
        "echeance": "[JJ/MM/AAAA]",
        "sections": sections
    }
    with open(a.json, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Scaffold écrit : {a.json}")
    print("   → compléter les [QUESTION À PRÉCISER], ajuster, puis :")
    print(f"     python3 dresser_dee.py {a.json} --out DEE.md --publish")


if __name__ == "__main__":
    main()
