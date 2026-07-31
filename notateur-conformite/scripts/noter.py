#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Moteur de notation de conformite MDC — Agence de Notation Administrative.
Usage : python3 noter.py observations.json
Format attendu : [{"code":"A1","domaine":"A","gravite":"CRITIQUE","constat":"...","montant":0}, ...]
"""
import json, sys, collections

DOMAINES = {
 "A": ("Tresorerie et suivi bancaire", 0.20),
 "B": ("Chiffre d'affaires et facturation", 0.20),
 "C": ("Obligations fiscales", 0.20),
 "D": ("Paie et obligations sociales", 0.15),
 "E": ("Comptabilite et bilan", 0.15),
 "F": ("Separation des patrimoines", 0.05),
 "G": ("Organisation documentaire", 0.05),
}
MALUS = {"CRITIQUE": 5, "MAJEUR": 3, "MOYEN": 1}
BASE = 20
# Grille de notation MDC (note /20 -> lettre)
GRILLE = [(19.0,"AAA","Excellence"),(17.0,"AA","Tres satisfaisant"),(15.0,"A","Satisfaisant"),
          (13.0,"BBB","Acceptable"),(9.5,"BB","Insuffisant"),(7.5,"B","Mediocre"),
          (4.5,"CCC","Critique"),(2.5,"CC","Tres critique"),(0.5,"C","Pre-contentieux"),
          (0.0,"D","Defaut")]

def noter(observations):
    par_dom = collections.defaultdict(list)
    for o in observations:
        par_dom[o["domaine"]].append(o)
    lignes = []; note_globale = 0.0
    for d,(lib,poids) in DOMAINES.items():
        obs = par_dom.get(d, [])
        malus = sum(MALUS[o["gravite"]] for o in obs)
        note = max(0, BASE - malus)
        note_globale += note * poids
        c = collections.Counter(o["gravite"] for o in obs)
        lignes.append({"domaine":d,"libelle":lib,"poids":poids,"critiques":c["CRITIQUE"],
                       "majeures":c["MAJEUR"],"moyennes":c["MOYEN"],"malus":malus,"note":note,
                       "pondere":round(note*poids,2)})
    lettre, qualif = next((l,q) for s,l,q in GRILLE if note_globale >= s)
    return lignes, round(note_globale,2), lettre, qualif

def rapport(observations):
    lignes, ng, lettre, qualif = noter(observations)
    out = []
    out.append("GRILLE DE NOTATION DE CONFORMITE — MDC AGENCE DE NOTATION ADMINISTRATIVE\n")
    out.append(f"{'Dom':<5}{'Domaine':<38}{'Poids':>7}{'Crit':>6}{'Maj':>5}{'Moy':>5}{'Note/20':>9}{'Pondere':>9}")
    out.append("-"*84)
    for l in lignes:
        out.append(f"{l['domaine']:<5}{l['libelle']:<38}{l['poids']:>6.0%}{l['critiques']:>6}"
                   f"{l['majeures']:>5}{l['moyennes']:>5}{l['note']:>9}{l['pondere']:>9.2f}")
    out.append("-"*84)
    tot = collections.Counter()
    for o in observations: tot[o["gravite"]] += 1
    out.append(f"{'':<43}{'TOTAL':>7}{tot['CRITIQUE']:>6}{tot['MAJEUR']:>5}{tot['MOYEN']:>5}{'':>9}{ng:>9.2f}")
    out.append(f"\nNOTE GLOBALE : {ng} / 20   ->   {lettre}  ({qualif})")
    out.append(f"Observations recensees : {len(observations)}")
    return "\n".join(out), ng, lettre, qualif

if __name__ == "__main__":
    obs = json.load(open(sys.argv[1], encoding="utf-8"))
    txt, ng, lettre, qualif = rapport(obs)
    print(txt)
