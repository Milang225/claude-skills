# -*- coding: utf-8 -*-
"""Controle de coherence du dossier d'audit, avant toute remise.

Reprend les controles qui ont fait echouer la remise du dossier MABEK le 24 novembre 2026 :
un chiffre pivot ne peut pas avoir deux valeurs dans un dossier, et aucun livrable ne porte
de terme interdit par la charte.

  python3 controle_coherence_audit.py LBTECH "<dossier d'audit>"
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from donnees_dossier import charger, pivots, f

INTERDITS = [
    (r"\bIFU\b", "« IFU » : l'identifiant ivoirien est le NCC"),
    (r"\bgratuit", "« gratuit » : écrire ce qui est dû, ou « en cours de vérification »"),
    (r"\bJ\+\s?\d", "un délai en « J+X » : le plan se range par rangs, pas par délais"),
    (r"\b(visa|visé par l'Agence|certifié conforme|certification)\b", "un visa ou une certification : MDC délivre une attestation de diagnostic"),
    (r"\.(md|py|json|xlsx|docx)\b", "un nom de fichier : aucun jargon technique dans un livrable"),
    (r"```", "un bloc de code"),
    (r"À RÉDIGER", "une consigne de rédaction non levée"),
    (r"(notre|le) cabinet d'expertise comptable (de MDC|de l'Agence)", "MDC présentée comme un cabinet d'expertise comptable"),
]


def montants_connus(D):
    """Tous les montants que le dossier de l'Atelier porte deja : montants saisis, bases,
    droits, scenarios ligne a ligne, montants des matrices d'anomalies, et totaux par nature.
    Un nombre qui figure la n'est pas une valeur concurrente d'un pivot : c'est une donnee
    du dossier qui se trouve, par hasard, proche d'un pivot."""
    vus = set()

    def ajouter(v):
        try:
            x = float(v)
        except (TypeError, ValueError):
            return
        if abs(x) >= 1000:
            vus.add(round(abs(x)))

    def parcourir(o):
        if isinstance(o, dict):
            for v in o.values():
                parcourir(v)
        elif isinstance(o, list):
            for v in o:
                parcourir(v)
        elif isinstance(o, (int, float)):
            ajouter(o)
        elif isinstance(o, str):
            for m in re.findall(r"\d[\d  .]{3,}\d", o):
                ajouter(m.replace(" ", "").replace("\u00a0", "").replace("\u202f", "").replace(".", ""))

    parcourir(D)
    # les totaux par nature d'impot, poste par poste : ils sont calcules, jamais saisis
    lignes = (D.get("l06") or {}).get("lignes") or []
    for cle in ("droit", "bas", "central", "haut"):
        par_nature = {}
        for l in lignes:
            par_nature.setdefault(l.get("nature_tdb") or "", 0.0)
            par_nature[l.get("nature_tdb") or ""] += float(l.get(cle) or 0)
        for v in par_nature.values():
            ajouter(v)
        ajouter(sum(float(l.get(cle) or 0) for l in lignes))
    return vus


def lignes_de_tableau(texte):
    """Decoupe les tableaux markdown d'un texte : liste de listes de cellules."""
    tableaux, courant = [], []
    for ligne in texte.split("\n"):
        if ligne.strip().startswith("|"):
            cells = [c.strip() for c in ligne.strip().strip("|").split("|")]
            if not all(set(c) <= set("-: ") for c in cells):
                courant.append(cells)
        else:
            if len(courant) > 1:
                tableaux.append(courant)
            courant = []
    if len(courant) > 1:
        tableaux.append(courant)
    return tableaux


def nombre(cellule):
    """Le montant d'une cellule, ou None : « **1 234 567** » -> 1234567.0"""
    c = cellule.replace("*", "").replace("\u202f", " ").strip()
    if not re.fullmatch(r"-?\d{1,3}(?: \d{3})+(?:,\d+)?|-?\d+(?:,\d+)?", c):
        return None
    return float(c.replace(" ", "").replace(",", "."))


def codes_en_double(textes):
    """Un code d'anomalie ne peut ouvrir qu'une seule ligne de tableau dans un livrable."""
    out = []
    for x, t in textes.items():
        vus = {}
        for tab in lignes_de_tableau(t):
            for l in tab:
                m = re.fullmatch(r"\*{0,2}([FSCTVGPARN]-\d{2})\*{0,2}", l[0].strip())
                if m:
                    vus[m.group(1)] = vus.get(m.group(1), 0) + 1
        for code, n in sorted(vus.items()):
            if n > 1:
                out.append((x, code, n))
    return out


def totaux_faux(textes):
    """Une ligne « Total » doit faire la somme des lignes au-dessus d'elle, colonne par colonne."""
    out = []
    for x, t in textes.items():
        for tab in lignes_de_tableau(t):
            larg = max(len(l) for l in tab)
            debut = 1            # une ligne « Total » ne somme que SA section : depuis le total precedent
            for i, l in enumerate(tab):
                if i == 0 or not re.match(r"\*{0,2}total", l[0].strip(), re.I):
                    continue
                for j in range(1, min(len(l), larg)):
                    annonce = nombre(l[j])
                    if annonce is None:
                        continue
                    vals = [nombre(k[j]) for k in tab[debut:i]
                            if len(k) > j and not re.match(r"\*{0,2}total", k[0].strip(), re.I)]
                    vals = [v for v in vals if v is not None]
                    if len(vals) < 2:
                        continue
                    somme = sum(vals)
                    if abs(somme - annonce) > 0.5:
                        out.append((x, l[0].replace("*", "")[:34], j + 1, annonce, somme))
                debut = i + 1
    return out


def pivots_a_verifier(p):
    """Les montants qui doivent etre identiques partout ou ils apparaissent."""
    return {
        "exposition centrale": p["central"], "scénario favorable": p["bas"],
        "scénario haut": p["haut"], "droits simples": p["droits"],
        "déjà exigible": p["deja_exigible"],
    }


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        raise SystemExit(__doc__)
    dossier, dest = a[0], a[1]
    D, source = charger(dossier, a[a.index("--json") + 1] if "--json" in a else None)
    p = pivots(D); p["lignes_sans_piece"] = 0
    src = os.path.join(dest, "_SOURCES_MD")
    fichiers = sorted(x for x in os.listdir(src) if x.endswith(".md"))
    textes = {x: open(os.path.join(src, x), encoding="utf-8").read() for x in fichiers}

    arrets = []
    print("DOSSIER : %s — %d sources\n" % (p["raison_sociale"], len(fichiers)))

    print("1. LES CHIFFRES PIVOTS")
    for nom, val in pivots_a_verifier(p).items():
        mot = f(val)
        porteurs = [x for x, t in textes.items() if mot in t]
        print("   %-22s %14s — %d livrable(s)" % (nom, mot, len(porteurs)))

    print("\n2. LES VALEURS CONCURRENTES D'UN MEME PIVOT")
    # tout montant de 6 chiffres ou plus, rapproche des pivots connus
    connus = {f(v) for v in pivots_a_verifier(p).values()}
    donnees = montants_connus(D)
    suspects = {}
    for x, t in textes.items():
        for m in re.findall(r"\b\d{1,3}(?: \d{3}){2,}\b", t):
            if m in connus:
                continue
            if round(float(m.replace(" ", ""))) in donnees:
                continue        # montant porte par le dossier de l'Atelier : ce n'est pas un pivot concurrent
            suspects.setdefault(m, set()).add(x)
    proches = []
    for m, oustes in suspects.items():
        v = float(m.replace(" ", ""))
        for nom, val in pivots_a_verifier(p).items():
            if val and 0 < abs(v - float(val)) <= max(1000.0, float(val) * 0.05):
                proches.append((m, nom, f(val), sorted(oustes)))
    if proches:
        for m, nom, val, oustes in sorted(proches)[:15]:
            print("   ATTENTION %s est proche de %s (%s) — %s" % (m, nom, val, ", ".join(oustes)))
            arrets.append("valeur concurrente %s" % m)
    else:
        print("   Aucune valeur étrangère au dossier n'est proche d'un pivot.")

    print("\n3. LES TERMES INTERDITS")
    ko = 0
    for x, t in textes.items():
        for motif, dit in INTERDITS:
            for m in re.finditer(motif, t, re.I):
                avant = t[max(0, m.start() - 60):m.start()].lower()
                if any(x in avant for x in (" ni ", "aucun", "pas de", "sans ", "ne vaut")):
                    continue        # la formule negative est permise : « ne vaut ni visa, ni certification »
                ligne = t[:m.start()].count("\n") + 1
                print("   ARRÊT %s ligne %d : %s" % (x, ligne, dit))
                arrets.append(dit); ko += 1
                break
    if not ko:
        print("   Aucun terme interdit.")

    print("\n4. LA RÉFÉRENCE DE CHAQUE LIVRABLE")
    for x, t in textes.items():
        m = re.search(r"MC-[A-Z]+-[A-Z]+-\d{4}-\d{3}", t)
        print("   %-55s %s" % (x[:55], m.group(0) if m else "ARRÊT : aucune référence"))
        if not m:
            arrets.append("référence absente dans %s" % x)

    print("\n5. LES CODES D'ANOMALIE EN DOUBLE")
    d = codes_en_double(textes)
    if d:
        for x, code, n in d:
            print("   ARRÊT %s : le code %s ouvre %d lignes de tableau" % (x, code, n))
            arrets.append("code %s en double dans %s" % (code, x))
    else:
        print("   Aucun code ne figure deux fois en tête de ligne.")

    print("\n6. LES TOTAUX DES TABLEAUX")
    faux = totaux_faux(textes)
    if faux:
        for x, lib, col, annonce, somme in faux[:15]:
            print("   À VÉRIFIER %s — « %s », colonne %d : %s annoncé, %s par la somme des lignes (écart %s)"
                  % (x, lib, col, f(annonce), f(somme), f(abs(annonce - somme))))
    else:
        print("   Chaque ligne « Total » fait la somme de ses lignes.")

    print("\n7. LES SOURCES ET LES FICHIERS PUBLIÉS")
    publies = sorted(x for x in os.listdir(dest) if x.endswith((".pdf", ".docx", ".xlsx")))
    socles = {x[:-3] for x in fichiers}
    sans_publication = [s for s in sorted(socles) if not any(q.startswith(s) for q in publies)]
    orphelins = [q for q in publies if not any(q.startswith(s) for s in socles)]
    print("   %d source(s), %d fichier(s) publié(s)" % (len(socles), len(publies)))
    for s in sans_publication:
        print("   source non publiée : %s" % s)
    for q in orphelins:
        print("   publié sans source : %s" % q)

    print("\n%s" % ("Dossier cohérent : la remise peut être préparée." if not arrets
                    else "%d point(s) d'arrêt : corriger avant toute remise." % len(arrets)))
    return 1 if arrets else 0


if __name__ == "__main__":
    sys.exit(main())
