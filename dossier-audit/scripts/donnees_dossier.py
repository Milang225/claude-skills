# -*- coding: utf-8 -*-
"""Donnees d'un dossier de l'Atelier du diagnostic, pour la production du dossier d'audit.

Lit le dossier la ou il se trouve, dans cet ordre :
  1. le fichier passe en --json
  2. l'Atelier qui tourne sur ce poste : http://localhost:8770/api/dossier?d=<DOSSIER>
  3. le fichier du poste : ~/Documents/DOSSIER CLIENTS/<DOSSIER>/DIAGNOSTIC_COMPLET/donnees_tableau_de_bord.json

Puis il en tire la FICHE DES PIVOTS : les chiffres qui devront etre identiques dans tous
les livrables, et les controles de bouclage qui disent si la matiere est prete.

  python3 donnees_dossier.py LBTECH
  python3 donnees_dossier.py LBTECH --ecrire "<dossier d'audit>"
"""
import json, os, sys, urllib.request

CLIENTS = os.environ.get("MDC_CLIENTS") or os.path.expanduser("~/Documents/DOSSIER CLIENTS")
SOUS, DONNEES = "DIAGNOSTIC_COMPLET", "donnees_tableau_de_bord.json"
API = "http://localhost:8770/api/dossier?d="
NIVEAUX = ((85, "Maîtrisé"), (70, "Satisfaisant"), (55, "Fragile"), (40, "Exposé"), (-1, "Critique"))


def charger(dossier, fichier=None):
    if fichier:
        return json.load(open(fichier, encoding="utf-8")), fichier
    try:
        with urllib.request.urlopen(API + urllib.parse.quote(dossier), timeout=4) as r:
            return json.loads(r.read().decode("utf-8")), "Atelier du diagnostic (localhost:8770)"
    except Exception:
        pass
    p = os.path.join(CLIENTS, dossier, SOUS, DONNEES)
    if not os.path.exists(p):
        raise SystemExit("Dossier introuvable : ni l'Atelier ne repond, ni le fichier %s n'existe.\n"
                         "Ouvrir l'Atelier du diagnostic, ou passer --json <fichier>." % p)
    return json.load(open(p, encoding="utf-8")), p


def niveau(v):
    for seuil, nom in NIVEAUX:
        if v >= seuil:
            return nom
    return "Critique"


def secteur(D):
    """Le code secteur des references MC, tire de la reference du tableau de bord."""
    ref = (D.get("client") or {}).get("reference") or ""
    bouts = ref.split("-")
    return bouts[2] if len(bouts) >= 4 else "GEN"


def pivots(D):
    c, ind, ch = D.get("client", {}), D.get("indice", {}), D.get("chiffres", {})
    lignes = (D.get("l06") or {}).get("lignes") or []
    anos = D.get("anomalies") or []
    doc = D.get("documents") or {}
    som = lambda k: sum(float(l.get(k) or 0) for l in lignes)
    exigible = sum(float(l.get("central") or 0) for l in lignes
                   if "non pay" in (l.get("situation") or "").lower())
    p = {
        "dossier": c.get("dossier", ""), "raison_sociale": c.get("raison_sociale", ""),
        "ncc": c.get("ncc", ""), "exercices": c.get("exercices", ""),
        "dirigeant": c.get("dirigeant", ""), "formule": c.get("formule", "Monsieur le Gerant"),
        "signataire": c.get("signataire", ""), "secteur": secteur(D),
        "date": c.get("date", ""), "version": c.get("version", ""),
        "indice": ind.get("valeur"), "niveau": niveau(float(ind.get("valeur") or 0)),
        "domaines": ind.get("domaines") or [],
        "droits": ch.get("droits"), "bas": ch.get("bas"), "central": ch.get("central"),
        "haut": ch.get("haut"), "risque_a_part": ch.get("risque_a_part"),
        "lignes_exposition": len(lignes),
        "droits_lignes": som("droit"), "central_lignes": som("central"),
        "deja_exigible": exigible,
        "anomalies": sum(int(a.get("critiques") or 0) + int(a.get("majeures") or 0) + int(a.get("mineures") or 0) for a in anos),
        "critiques": sum(int(a.get("critiques") or 0) for a in anos),
        "majeures": sum(int(a.get("majeures") or 0) for a in anos),
        "mineures": sum(int(a.get("mineures") or 0) for a in anos),
        "documents_applicables": doc.get("applicables"), "documents_presents": doc.get("presents"),
    }
    if doc.get("applicables"):
        p["documents_taux"] = round(100.0 * float(doc.get("presents") or 0) / float(doc["applicables"]))
    p["attestation"] = ((p["indice"] or 0) >= 70 and not p["critiques"])
    return p


def controles(p):
    """Ce qui doit boucler avant d'ecrire une seule ligne de livrable."""
    out = []
    def c(nom, ok, dit):
        out.append((("OK  " if ok else "ARRET"), nom, dit))
    ecart = abs(float(p["droits_lignes"]) - float(p["droits"] or 0))
    c("Les droits des lignes font le total du tableau de bord", ecart < 1,
      "lignes %s contre tableau de bord %s, ecart %s" % (f(p["droits_lignes"]), f(p["droits"]), f(ecart)))
    ecart2 = abs(float(p["central_lignes"]) - float(p["central"] or 0))
    c("Le central des lignes fait le central du tableau de bord", ecart2 < 1,
      "lignes %s contre tableau de bord %s, ecart %s" % (f(p["central_lignes"]), f(p["central"]), f(ecart2)))
    c("Le dossier porte des lignes d'exposition", p["lignes_exposition"] > 0,
      "%d lignes" % p["lignes_exposition"])
    c("Le dossier porte des anomalies", p["anomalies"] > 0,
      "%d anomalies dont %d critiques" % (p["anomalies"], p["critiques"]))
    c("L'identite du client est complete", all([p["raison_sociale"], p["ncc"], p["exercices"], p["dirigeant"]]),
      "%s, NCC %s, %s" % (p["raison_sociale"], p["ncc"], p["exercices"]))
    c("Chaque ligne d'exposition cite sa piece", p["lignes_sans_piece"] == 0,
      "%d ligne(s) sans piece" % p["lignes_sans_piece"])
    return out


def f(n):
    try:
        return "{:,.0f}".format(float(n)).replace(",", " ")
    except Exception:
        return str(n)


def main():
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    dossier, fichier, ecrire = a[0], None, None
    for i, x in enumerate(a):
        if x == "--json" and i + 1 < len(a): fichier = a[i + 1]
        if x == "--ecrire" and i + 1 < len(a): ecrire = a[i + 1]
    D, source = charger(dossier, fichier)
    p = pivots(D)
    lignes = (D.get("l06") or {}).get("lignes") or []
    p["lignes_sans_piece"] = sum(1 for l in lignes if not (l.get("piece") or "").strip())

    print("SOURCE : %s\n" % source)
    print("FICHE DES PIVOTS — %s" % p["raison_sociale"])
    print("  Dossier %s, NCC %s, exercices %s, secteur %s" % (p["dossier"], p["ncc"], p["exercices"], p["secteur"]))
    print("  Dirigeant : %s" % p["dirigeant"])
    print("  Indice %s sur 100, niveau %s — %s" % (
        p["indice"], p["niveau"],
        "attestation de diagnostic delivrable" if p["attestation"]
        else "attestation non delivrable : le dossier porte un constat de non-conformite"))
    print("  Droits simples %s | bas %s | central %s | haut %s" % (f(p["droits"]), f(p["bas"]), f(p["central"]), f(p["haut"])))
    print("  Deja exigible (declare non paye) %s" % f(p["deja_exigible"]))
    print("  %d anomalies : %d critiques, %d majeures, %d mineures" % (p["anomalies"], p["critiques"], p["majeures"], p["mineures"]))
    print("  Documents %s sur %s, soit %s %%" % (p["documents_presents"], p["documents_applicables"], p.get("documents_taux")))
    print("  %d lignes d'exposition" % p["lignes_exposition"])
    print("\nCONTROLES DE BOUCLAGE")
    arrets = 0
    for etat, nom, dit in controles(p):
        print("  [%s] %s : %s" % (etat, nom, dit))
        arrets += etat.strip() == "ARRET"
    print("\n%s" % ("Matiere prete." if not arrets else "%d controle(s) en arret : corriger dans l'Atelier avant de produire." % arrets))
    if ecrire:
        os.makedirs(ecrire, exist_ok=True)
        q = os.path.join(ecrire, "donnees_audit.json")
        json.dump({"pivots": p, "dossier": D}, open(q, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\nEcrit : %s" % q)
    return 1 if arrets else 0


if __name__ == "__main__":
    import urllib.parse
    sys.exit(main())
