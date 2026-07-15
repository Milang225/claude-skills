#!/usr/bin/env python3
"""Filtre supplémentaire : éliminer Bordereaux de Livraison (BL) + Devis."""
import json, re, os
from collections import Counter

OCR_DIR = "/tmp/bna_ocr/txt"
docs = json.load(open("/tmp/bna_ocr/factures_tva.json"))

def is_bordereau_or_devis(d):
    """Détecte BL, BdL, devis, expédition — qui ne sont pas des factures."""
    try:
        with open(os.path.join(OCR_DIR, d["file"])) as f:
            text = f.read()
    except:
        text = d.get("raw_excerpt", "")
    low = text.lower()

    # Marqueurs FORTS de BL/Devis
    bl_markers = [
        r"bordereau\s*de\s*livraison",
        r"bon\s*de\s*livraison",
        r"\bbon\s*n[°o]?\s*livraison",
        r"^\s*bl\s*\d{4,}",
        r"avis\s*d.exp[ée]dition",
        r"\bn[°o]?\s*exp[ée]dition\b",
        r"bon\s*de\s*r[ée]ception",
    ]
    devis_markers = [
        r"^\s*devis\s*$",
        r"^\s*devis\s*n[°o]",
        r"\bdevis\s*n[°o]?\s*[\w-]+\s+du\s+\d",
        r"validité\s*du\s*devis",
        r"\bproforma\b",
        r"\bdevis\s*estimatif\b",
    ]
    # Marqueurs FORTS de vraie facture
    facture_markers = [
        r"\bfacture\s*n[°o]",
        r"^\s*FACTURE\s*$",
        r"r[ée][çc]u\s*n[°o]",
        r"^\s*r[ée][çc]u\s*$",
        r"ticket\s*de\s*caisse",
        r"facture\s*normalis[ée]e",
        r"avis\s*de\s*paiement",
    ]

    has_bl = any(re.search(p, low, re.M) for p in bl_markers)
    has_devis = any(re.search(p, low, re.M) for p in devis_markers)
    has_facture = any(re.search(p, low, re.M | re.I) for p in facture_markers)

    # Si c'est un BL ou un devis ET pas de facture associée → exclure
    if (has_bl or has_devis) and not has_facture:
        if has_bl: return ("BL", "Bordereau/Bon de livraison sans facture")
        if has_devis: return ("DEVIS", "Devis / Proforma")
    return (None, None)

kept = []
removed = []
for d in docs:
    typ, motif = is_bordereau_or_devis(d)
    if typ:
        removed.append((typ, motif, d))
    else:
        kept.append(d)

print(f"Total avant filtre BL/Devis : {len(docs)}")
print(f"Retirés : {len(removed)}")
print(f"  par type : {dict(Counter(r[0] for r in removed))}")
print("\nDocs retirés (top 30 par TTC) :")
removed_sorted = sorted(removed, key=lambda r: -(r[2].get("ttc") or 0))
for typ, motif, d in removed_sorted[:30]:
    print(f"  [{typ}] {d['file']:30s} | {d['supplier'][:25]:<25} | {motif} | TTC={d['ttc'] or 0:,}".replace(",", " "))

print(f"\nConservées (vraies factures) : {len(kept)}")
ttc_kept = sum(d['ttc'] or 0 for d in kept)
print(f"Σ TTC conservé : {ttc_kept:,}".replace(",", " "))

# Save
with open("/tmp/bna_ocr/factures_final.json", "w") as f:
    json.dump(kept, f, ensure_ascii=False, indent=2)

# Stats par année après filtre
print("\n=== APRÈS FILTRE BL/DEVIS — par année ===")
by_y = {}
for d in kept:
    y = d.get("year") or "ND"
    by_y.setdefault(y, {"n":0,"ttc":0})
    by_y[y]["n"] += 1
    by_y[y]["ttc"] += d["ttc"] or 0
for y in sorted(by_y, key=lambda x: (x=="ND", x)):
    print(f"  {y}: {by_y[y]['n']:>3} factures / Σ TTC = {by_y[y]['ttc']:>15,}".replace(",", " "))

# Ratio 2022
fact_2022 = [d for d in kept if d.get("year")==2022]
ttc_2022 = sum(d["ttc"] or 0 for d in fact_2022)
ht_2022 = int(ttc_2022/1.18)
print(f"\n📊 2022 NET FACTURES SEULES :")
print(f"   {len(fact_2022)} vraies factures")
print(f"   Σ TTC = {ttc_2022:,} | HT = {ht_2022:,}".replace(",", " "))
print(f"   Charges balance 2022 = 134 169 349 HT")
print(f"   Ratio = {ht_2022/134169349:.2f}")
