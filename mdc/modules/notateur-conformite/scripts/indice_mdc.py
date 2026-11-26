#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Moteur de l'Indice MDC de conformité — La Maison de la Conformité SARL.

Commandes :
  python3 indice_mdc.py modele  sortie.json  [--client NOM] [--reference MDC-AAAA-NNN]
      Crée une feuille d'évaluation vierge listant tous les contrôles du référentiel.
  python3 indice_mdc.py calculer evaluation.json  [--md synthese.md]  [--json resultat.json]
      Valide la feuille, calcule l'indice, le niveau, la couverture et l'exposition.
  python3 indice_mdc.py referentiel  [--md referentiel.md]
      Imprime le référentiel (tableau des contrôles) en Markdown.

Le moteur ne juge pas : il applique les règles. Le statut de chaque contrôle relève
de l'analyste et doit être adossé à une pièce.
"""
import argparse, json, os, sys
from collections import defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
REF_DEFAUT = os.path.join(ICI, "referentiel_mdc_v1.json")


# Position de défense d'une observation si l'administration la relevait :
#   FORTE      : texte, pièce ou doctrine permettent de contester avec de bonnes chances
#   DISCUTABLE : argumentable, issue incertaine
#   FAIBLE     : le rappel serait fondé ; mieux vaut régulariser
DEFENSES = ("FORTE", "DISCUTABLE", "FAIBLE")
# Stratégie retenue avec le client :
#   REGULARISER : corriger spontanément avant tout contrôle
#   DOCUMENTER  : constituer dès maintenant le dossier de preuve
#   DEFENDRE    : maintenir la position et préparer l'argumentaire
STRATEGIES = ("REGULARISER", "DOCUMENTER", "DEFENDRE")


def charger_referentiel(chemin=REF_DEFAUT):
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def referentiel_pour(feuille, chemin=REF_DEFAUT):
    """Le référentiel de la version avec laquelle la feuille a été évaluée : une feuille 1.0 (45 contrôles) se calcule
    toujours avec la méthode 1.0, archivée à côté ; les nouvelles feuilles suivent la version en vigueur."""
    ref = charger_referentiel(chemin)
    v = feuille.get("version_methode")
    if v and v != ref["version"]:
        archive = os.path.join(os.path.dirname(chemin), f"referentiel_mdc_v{v}.json")
        if os.path.exists(archive):
            return charger_referentiel(archive)
    return ref


def fcfa(n):
    return f"{int(round(n)):,}".replace(",", " ") + " FCFA"


# ---------------------------------------------------------------- modèle vierge
def creer_modele(ref, sortie, client, reference):
    feuille = {
        "client": client or "",
        "reference": reference or "MDC-AAAA-NNN",
        "periode": "",
        "date_evaluation": "",
        "analyste": "",
        "relecteur": "",
        "version_methode": ref["version"],
        "evaluations": [
            {"controle": c["id"], "intitule": c["intitule"], "gravite": c["gravite"],
             "statut": "", "constat": "", "piece": "",
             "exposition_fcfa": {"bas": 0, "central": 0, "haut": 0},
             "defense": "", "strategie": ""}
            for c in ref["controles"]
        ],
    }
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(feuille, f, ensure_ascii=False, indent=2)
    print(f"Feuille vierge créée : {sortie} ({len(ref['controles'])} contrôles)")


# ---------------------------------------------------------------- validation
def valider(ref, feuille):
    erreurs = []
    ids = {c["id"] for c in ref["controles"]}
    vus = {}
    for e in feuille["evaluations"]:
        cid = e.get("controle")
        if cid not in ids:
            erreurs.append(f"{cid} : contrôle inconnu du référentiel {ref['version']}")
            continue
        if cid in vus:
            erreurs.append(f"{cid} : évalué deux fois")
        vus[cid] = e
        st = e.get("statut", "")
        if st not in ref["statuts"]:
            erreurs.append(f"{cid} : statut '{st}' invalide (attendu C, P, NC, NV ou NA)")
            continue
        if st in ("P", "NC", "NV") and not e.get("constat", "").strip():
            erreurs.append(f"{cid} : un statut {st} exige un constat")
        if st in ("P", "NC") and not e.get("piece", "").strip():
            erreurs.append(f"{cid} : un statut {st} exige la pièce qui l'établit")
        if st in ("P", "NC", "NV"):
            if e.get("defense", "") not in DEFENSES:
                erreurs.append(f"{cid} : position de défense requise ({', '.join(DEFENSES)})")
            if e.get("strategie", "") not in STRATEGIES:
                erreurs.append(f"{cid} : stratégie requise ({', '.join(STRATEGIES)})")
        if st == "NA" and not e.get("constat", "").strip():
            erreurs.append(f"{cid} : un 'non applicable' doit être motivé dans le constat")
    for cid in sorted(ids - set(vus)):
        erreurs.append(f"{cid} : contrôle non évalué (tous les contrôles sont obligatoires)")
    if feuille.get("version_methode") != ref["version"]:
        erreurs.append(f"Version de méthode {feuille.get('version_methode')} ≠ référentiel {ref['version']}")
    return erreurs, vus


# ---------------------------------------------------------------- calcul
def calculer(ref, feuille):
    erreurs, evals = valider(ref, feuille)
    if erreurs:
        return None, erreurs

    g = ref["gravites"]
    st = ref["statuts"]
    regles = ref["regles"]
    par_dom = defaultdict(list)
    for c in ref["controles"]:
        par_dom[c["domaine"]].append(c)

    domaines, indice = [], 0.0
    poids_applicable_total = poids_couvert_total = 0
    critiques_nc = []
    expo = {"bas": 0, "central": 0, "haut": 0}

    for d in ref["domaines"]:
        num = den = couvert = 0.0
        plafonne = False
        compte = defaultdict(int)
        for c in par_dom[d["code"]]:
            e = evals[c["id"]]
            s = e["statut"]
            compte[s] += 1
            for k in expo:
                expo[k] += (e.get("exposition_fcfa") or {}).get(k, 0) or 0
            if s == "NA":
                continue
            w = g[c["gravite"]]
            den += w
            num += w * st[s]["valeur"]
            if st[s]["couvert"]:
                couvert += w
            if c["gravite"] == "CRITIQUE" and s == "NC":
                plafonne = True
                critiques_nc.append(c["id"])
        score = 100.0 * num / den if den else 100.0
        if plafonne:
            score = min(score, regles["plafond_domaine_si_critique_nc"])
        poids_applicable_total += den
        poids_couvert_total += couvert
        indice += score * d["poids"] / 100.0
        domaines.append({
            "code": d["code"], "libelle": d["libelle"], "poids": d["poids"],
            "score": round(score, 1), "plafonne": plafonne,
            "couverture": round(100.0 * couvert / den, 1) if den else 100.0,
            "C": compte["C"], "P": compte["P"], "NC": compte["NC"],
            "NV": compte["NV"], "NA": compte["NA"],
        })

    indice = round(indice, 1)
    couverture = round(100.0 * poids_couvert_total / poids_applicable_total, 1) if poids_applicable_total else 100.0

    # Niveau brut puis règle du maillon critique
    niveaux = ref["niveaux"]
    rang = {n["code"]: i for i, n in enumerate(niveaux)}  # 0 = meilleur
    brut = next(n for n in niveaux if indice >= n["min"])
    retenu = brut
    motif_plafond = None
    for r in regles["maillon_critique"]:
        if len(critiques_nc) >= r["critiques_nc_min"]:
            plafond = niveaux[rang[r["niveau_max"]]]
            if rang[retenu["code"]] < rang[plafond["code"]]:
                retenu = plafond
                motif_plafond = (f"{len(critiques_nc)} contrôle(s) critique(s) non conforme(s) "
                                 f"({', '.join(critiques_nc)}) : niveau plafonné à « {plafond['libelle']} »")
            break

    if couverture >= regles["couverture_definitive_min"]:
        statut_indice = "DÉFINITIF"
    elif couverture >= regles["couverture_provisoire_min"]:
        statut_indice = "PROVISOIRE"
    else:
        statut_indice = "NON ÉMIS"

    a = regles["attestation"]
    attestation = (statut_indice == "DÉFINITIF" and indice >= a["indice_min"]
                   and couverture >= a["couverture_min"] and len(critiques_nc) <= a["critiques_nc_max"])

    observations = []
    for c in ref["controles"]:
        e = evals[c["id"]]
        if e["statut"] in ("P", "NC", "NV"):
            observations.append({"controle": c["id"], "intitule": c["intitule"], "gravite": c["gravite"],
                                 "statut": e["statut"], "constat": e["constat"], "piece": e.get("piece", ""),
                                 "exposition_central": (e.get("exposition_fcfa") or {}).get("central", 0),
                                 "defense": e.get("defense", ""), "strategie": e.get("strategie", "")})
    ordre = {"CRITIQUE": 0, "MAJEUR": 1, "MINEUR": 2}
    observations.sort(key=lambda o: (ordre[o["gravite"]], -o["exposition_central"]))

    par_defense = {d: 0 for d in DEFENSES}
    for o in observations:
        par_defense[o["defense"]] += o["exposition_central"]

    return {
        "par_defense": par_defense,
        "client": feuille.get("client"), "reference": feuille.get("reference"),
        "periode": feuille.get("periode"), "date_evaluation": feuille.get("date_evaluation"),
        "version_methode": ref["version"],
        "indice": indice, "statut_indice": statut_indice, "couverture": couverture,
        "niveau_brut": brut["libelle"], "niveau": retenu["libelle"], "couleur": retenu["couleur"],
        "lecture": retenu["lecture"], "motif_plafond": motif_plafond,
        "critiques_non_conformes": critiques_nc, "attestation_possible": attestation,
        "exposition_fcfa": expo, "domaines": domaines, "observations": observations,
    }, []


# ---------------------------------------------------------------- restitution
def texte(r):
    L = []
    L.append("INDICE MDC DE CONFORMITÉ — méthode v" + r["version_methode"])
    L.append(f"Client : {r['client']}   Réf. : {r['reference']}   Période : {r['periode']}")
    L.append("-" * 78)
    L.append(f"{'Domaine':<40}{'Poids':>6}{'Score':>8}{'Couv.':>7}  C  P NC NV NA")
    for d in r["domaines"]:
        mark = "*" if d["plafonne"] else " "
        L.append(f"{d['code']} {d['libelle']:<38}{d['poids']:>5}%{d['score']:>7.1f}{mark}{d['couverture']:>6.0f}%"
                 f" {d['C']:>2} {d['P']:>2} {d['NC']:>2} {d['NV']:>2} {d['NA']:>2}")
    L.append("-" * 78)
    L.append(f"INDICE : {r['indice']} / 100   ({r['statut_indice']}, couverture {r['couverture']} %)")
    L.append(f"NIVEAU : {r['niveau']}" + (f"   [brut : {r['niveau_brut']}]" if r["niveau"] != r["niveau_brut"] else ""))
    if r["motif_plafond"]:
        L.append("        " + r["motif_plafond"])
    e = r["exposition_fcfa"]
    L.append(f"EXPOSITION ESTIMÉE : bas {fcfa(e['bas'])} · central {fcfa(e['central'])} · haut {fcfa(e['haut'])}")
    d = r["par_defense"]
    L.append(f"  dont défense forte {fcfa(d['FORTE'])} · discutable {fcfa(d['DISCUTABLE'])} · faible {fcfa(d['FAIBLE'])}")
    L.append("ATTESTATION : " + ("possible" if r["attestation_possible"] else "non délivrable"))
    L.append("* domaine plafonné à 50 (contrôle critique non conforme)")
    L.append(f"Observations : {len(r['observations'])}")
    return "\n".join(L)


def markdown(r):
    L = [f"## Synthèse — Indice MDC de conformité (méthode v{r['version_methode']})", ""]
    L.append(f"**Indice : {r['indice']} / 100 — niveau « {r['niveau']} »** "
             f"({r['statut_indice'].lower()}, couverture {r['couverture']} %)")
    L.append("")
    L.append(f"_{r['lecture']}_")
    if r["motif_plafond"]:
        L += ["", f"Règle du maillon critique : {r['motif_plafond']}."]
    e = r["exposition_fcfa"]
    d = r["par_defense"]
    L += ["", f"**Exposition estimée** : {fcfa(e['central'])} (fourchette {fcfa(e['bas'])} à {fcfa(e['haut'])}).",
          f"Dont position de défense forte : {fcfa(d['FORTE'])} · discutable : {fcfa(d['DISCUTABLE'])} · "
          f"faible (à régulariser) : {fcfa(d['FAIBLE'])}.", ""]
    L.append("| Domaine | Poids | Score /100 | Couverture | Non conformes |")
    L.append("|---|---:|---:|---:|---:|")
    for d in r["domaines"]:
        s = f"{d['score']:.1f}" + (" (plafonné)" if d["plafonne"] else "")
        L.append(f"| {d['libelle']} | {d['poids']} % | {s} | {d['couverture']:.0f} % | {d['NC']} |")
    L += ["", "| Contrôle | Gravité | Statut | Constat | Pièce | Défense | Stratégie |", "|---|---|---|---|---|---|---|"]
    for o in r["observations"]:
        L.append(f"| {o['controle']} {o['intitule']} | {o['gravite'].capitalize()} | {o['statut']} | {o['constat']} "
                 f"| {o['piece']} | {o['defense'].capitalize()} | {o['strategie'].capitalize()} |")
    return "\n".join(L) + "\n"


def referentiel_md(ref):
    L = [f"| Code | Contrôle | Gravité | Question de test | Preuve attendue |", "|---|---|---|---|---|"]
    lib = {d["code"]: d for d in ref["domaines"]}
    cur = None
    for c in ref["controles"]:
        if c["domaine"] != cur:
            cur = c["domaine"]
            d = lib[cur]
            L.append(f"| **{cur}** | **{d['libelle']} — {d['poids']} %** | | | |")
        L.append(f"| {c['id']} | {c['intitule']} | {c['gravite'].capitalize()} | {c['test']} | {c['preuve']} |")
    return "\n".join(L) + "\n"


def main():
    p = argparse.ArgumentParser(description="Indice MDC de conformité")
    sp = p.add_subparsers(dest="cmd", required=True)
    m = sp.add_parser("modele"); m.add_argument("sortie"); m.add_argument("--client"); m.add_argument("--reference")
    c = sp.add_parser("calculer"); c.add_argument("evaluation"); c.add_argument("--md"); c.add_argument("--json")
    r = sp.add_parser("referentiel"); r.add_argument("--md")
    for x in (m, c, r):
        x.add_argument("--ref", default=REF_DEFAUT)
    a = p.parse_args()
    ref = charger_referentiel(a.ref)

    if a.cmd == "modele":
        creer_modele(ref, a.sortie, a.client, a.reference)
    elif a.cmd == "referentiel":
        out = referentiel_md(ref)
        if a.md:
            open(a.md, "w", encoding="utf-8").write(out)
        print(out)
    else:
        feuille = json.load(open(a.evaluation, encoding="utf-8"))
        ref = referentiel_pour(feuille, a.ref)
        res, err = calculer(ref, feuille)
        if err:
            print("FEUILLE REFUSÉE — corriger avant tout calcul :", file=sys.stderr)
            for x in err:
                print("  - " + x, file=sys.stderr)
            sys.exit(1)
        print(texte(res))
        if a.md:
            open(a.md, "w", encoding="utf-8").write(markdown(res))
        if a.json:
            json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
