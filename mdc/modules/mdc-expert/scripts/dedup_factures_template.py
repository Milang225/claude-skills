#!/usr/bin/env python3
"""Dédoublonnage strict des factures dépouillées BNA."""
import json
from collections import defaultdict

docs = json.load(open("/tmp/bna_ocr/factures_clean.json"))

# 1. EXCLURE les pages "Comment lire votre facture" Orange (notices pédagogiques)
def is_notice_orange(d):
    excerpt_low = d.get("raw_excerpt","").lower()
    return ("comment lire" in excerpt_low and "facture internet" in excerpt_low) \
        or "comment lire l'annexe" in excerpt_low

# 2. EXCLURE les BUROTOP fiches client (pas des factures)
def is_fiche_client(d):
    return "FICHE DE CREATION" in d.get("raw_excerpt","").upper() \
        or "modification clients" in d.get("raw_excerpt","").lower()

# 3. EXCLURE les pages sans contenu utile (FOURNISSEUR_INDETERMINE + pas de TTC + pas de date)
def is_empty_page(d):
    return d["supplier"]=="FOURNISSEUR_INDETERMINE" and not d["ttc"] \
           and not d.get("year")

excluded = []
kept = []
for d in docs:
    if is_notice_orange(d):
        excluded.append(("NOTICE_ORANGE", d)); continue
    if is_fiche_client(d):
        excluded.append(("FICHE_CLIENT", d)); continue
    if is_empty_page(d):
        excluded.append(("PAGE_VIDE", d)); continue
    kept.append(d)

print(f"Total brut: {len(docs)}")
print(f"Exclus (non-factures): {len(excluded)}")
from collections import Counter
print("  par motif:", dict(Counter(e[0] for e in excluded)))
print(f"Conservés: {len(kept)}")

# 4. DÉDOUBLONNAGE STRICT : même (fournisseur, jour, mois, année, TTC)
# Pour chaque groupe doublon, conserver UNE seule occurrence
seen_sig = {}
dedup_kept = []
dedup_removed = []
for d in kept:
    sig = (d["supplier"][:30], d.get("day"), d.get("month"), d.get("year"), d["ttc"])
    # Si signature complète (toutes valeurs non None), dédoublonner strict
    if all(v is not None for v in sig):
        if sig in seen_sig:
            dedup_removed.append((sig, d))
            continue
        seen_sig[sig] = d
    dedup_kept.append(d)

print(f"\nDoublons stricts retirés: {len(dedup_removed)}")
for sig, d in dedup_removed:
    print(f"  ⊖ {d['file']} | {sig}")

# 5. DOUBLONS PROBABLES (même fournisseur+date sans TTC ferme) : alerte mais on garde
soft_dupes = defaultdict(list)
for d in dedup_kept:
    if d["year"] and d.get("day") and d.get("month"):
        sig = (d["supplier"][:30], d["day"], d["month"], d["year"])
        soft_dupes[sig].append(d)
warn = {k:v for k,v in soft_dupes.items() if len(v)>1}
print(f"\nDoublons probables (fournisseur+date, TTC ≠) — à vérifier manuellement: {len(warn)}")
for sig, lst in warn.items():
    print(f"  ⚠  {sig}")
    for d in lst:
        print(f"     {d['file']} TTC={d['ttc']}")

# Save
with open("/tmp/bna_ocr/factures_dedup.json", "w") as f:
    json.dump(dedup_kept, f, ensure_ascii=False, indent=2)

# Stats avant/après par année
def stats(arr, lbl):
    by_y = defaultdict(lambda: {"n":0,"ttc":0})
    for d in arr:
        y = d.get("year") or "ND"
        by_y[y]["n"] += 1
        by_y[y]["ttc"] += d["ttc"] or 0
    print(f"\n=== {lbl} ===")
    for y in sorted(by_y, key=lambda x: (x=="ND", x)):
        print(f"  {y}: {by_y[y]['n']:>3} docs / TTC = {by_y[y]['ttc']:>15,}".replace(",", " "))

stats(docs, "AVANT (brut)")
stats(dedup_kept, "APRÈS dédoublonnage + exclusions")

# Spécifique 2022
fact_2022 = [d for d in dedup_kept if d.get("year")==2022]
ttc_2022 = sum(d["ttc"] or 0 for d in fact_2022)
ht_2022 = int(ttc_2022/1.18)
print(f"\n📊 EXERCICE 2022 NET DE DOUBLONS:")
print(f"   {len(fact_2022)} factures uniques")
print(f"   Σ TTC = {ttc_2022:,} FCFA".replace(",", " "))
print(f"   Σ HT  = {ht_2022:,} FCFA".replace(",", " "))
print(f"   Charges déclarées balance 2022 = 134 169 349 HT")
print(f"   Ratio Fact/Charges = {ht_2022/134169349:.2f}")
