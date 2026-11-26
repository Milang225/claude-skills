#!/usr/bin/env python3
"""Récap des dossiers clients MDC.
  python3 recap.py                  -> récap global (Markdown) dans ~/REVISION/
  python3 recap.py --client "TIM 7" -> fiche détaillée d'un dossier
Lecture seule : ne modifie aucun dossier client."""
import os, sys, re, datetime, unicodedata, argparse
H = os.path.expanduser("~")
DOC = f"{H}/Documents"
CL = f"{DOC}/DOSSIER CLIENTS"
SUIVI = f"{DOC}/SUIVI CLIENTS/SUIVI_DES_DOSSIERS_MDC.xlsx"
OUTDIR = f"{H}/REVISION"
TODAY = datetime.date.today()
IGN_DIRS = {"_MODELES", "ESSAI", "TESTPROFIL", "Formation", "BALANCES DES COMPTES POUR BASE"}
FORMES = r"\b(SARLU|SARL|SAS|SA|SCI|SUARL|SNC|CI|COTE D'?IVOIRE|ET|&|DE|DU|LA|LE|LES)\b"
# Familles de documents repérées dans les noms de fichiers
FAMILLES = [
    ("Profil / Indice conformité", r"PROFIL|INDICE|NOTATION"),
    ("Note méthodologique", r"NOTE_METHOD"),
    ("Proposition financière", r"PROPOSITION|PROPALE"),
    ("Contrat / lettre de mission", r"CONTRAT|LETTRE_DE_MISSION|ENGAGEMENT"),
    ("DEE / points à éclaircir", r"(?<![A-Z])DEE(?![A-Z])|POINTS?_A_ECLAIRCIR|DEMANDE_D_EXPLICATION"),
    ("Contrôles de tenue", r"CONTROLES?_DE_TENUE"),
    ("Fiche de tâches", r"FICHE_DE_TACHES|TACHES"),
    ("Pièces juridiques (RCCM, DFE, statuts)", r"RCCM|DFE|STATUT|PIECES_JURIDIQUES"),
    ("Relevés bancaires", r"RELEVE|BANQUE|BANK"),
    ("Balance / grand livre / états financiers", r"BALANCE|GRAND_LIVRE|ETATS?_FINANCIERS|LIASSE|BILAN"),
    ("Déclarations fiscales / sociales", r"DECLARATION|(?<![A-Z])(TVA|ITS|CNPS|PATENTE|IMF|BIC)(?![A-Z])"),
    ("Rapport / diagnostic", r"RAPPORT|DIAGNOSTIC|AUDIT"),
    ("Saisie comptable", r"SAISIE|JOURNAL|DEPOUILLEMENT"),
]
# Variantes de noms entre le classeur de suivi et les dossiers (à compléter au besoin)
ALIAS = {"RICHTZA": "RICHTAZ", "SAINT": "ST", "MULTISERVICES": "MULTISERVICE"}
def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    s = re.sub(r"\(.*?\)", " ", s)
    for a, b in ALIAS.items(): s = re.sub(rf"\b{a}\b", b, s)
    s = re.sub(FORMES, " ", s)
    return re.sub(r"[^A-Z0-9]+", "", s)
def same(a, b):
    a, b = norm(a), norm(b)
    return bool(a and b) and (a == b or (min(len(a), len(b)) >= 4 and (a in b or b in a)))
def d(t): return datetime.datetime.fromtimestamp(t).strftime("%d/%m/%Y")

def scan(path):
    files, obs = [], 0
    for dp, dn, fn in os.walk(path):
        dn[:] = [x for x in dn if not x.startswith(".")]
        for f in fn:
            if f.startswith((".", "~$")): continue
            p = os.path.join(dp, f)
            if "OBSOLETE" in p.upper(): obs += 1; continue
            try: files.append((os.path.getmtime(p), os.path.relpath(p, path)))
            except OSError: pass
    files.sort(reverse=True)
    fams = {}
    for t, rel in files:
        u = unicodedata.normalize("NFKD", rel).encode("ascii", "ignore").decode().upper().replace(" ", "_")
        for nom, rx in FAMILLES:
            if re.search(rx, u): fams.setdefault(nom, (t, rel))  # le plus récent
    subs = sorted(x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x)) and not x.startswith("."))
    return files, obs, fams, subs

def lire_suivi():
    """{onglet: [dict ligne]} à partir du classeur de suivi (ligne d'en-tête = celle contenant 'Entreprise')."""
    out = {}
    try:
        import openpyxl
        wb = openpyxl.load_workbook(SUIVI, read_only=True, data_only=True)
    except Exception as e:
        return {"_erreur": str(e)}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        hi = next((i for i, r in enumerate(rows[:8]) if r and "Entreprise" in [str(c).strip() if c else "" for c in r]), None)
        if hi is None: continue
        head = [str(c).strip() if c else f"col{j}" for j, c in enumerate(rows[hi])]
        out[ws.title] = [dict(zip(head, r)) for r in rows[hi+1:] if r and len(r) > 1 and r[1]]
    return out

def suivi_pour(nom, suivi):
    res = []
    for onglet, lignes in suivi.items():
        if onglet.startswith("_"): continue
        for l in lignes:
            if same(l.get("Entreprise"), nom): res.append((onglet, l))
    return res

def resume_suivi(onglet, l):
    if onglet == "Contrôles de tenue":
        vals = [str(v) for k, v in l.items() if re.match(r"CT\d+", k) and v]
        c = {s: vals.count(s) for s in ("Conforme", "Manque", "Non vérifiable", "Sans objet")}
        return f"Contrôles de tenue : {c['Conforme']} conformes, {c['Manque']} manques, {c['Non vérifiable']} non vérifiables"
    keys = ["Étape constatée sur les pièces", "Dernière étape franchie", "Prestation en cours",
            "Prochaine étape", "Dernière action", "Observation", "Avancement"]
    parts = []
    for k in keys:
        v = l.get(k)
        if v in (None, ""): continue
        if isinstance(v, float) and v <= 1: v = f"{v:.0%}"
        if isinstance(v, datetime.datetime): v = v.strftime("%d/%m/%Y")
        parts.append(f"{k} : {v}")
    return f"{onglet} — " + " · ".join(parts) if parts else onglet

def statut(jours):
    return "Actif" if jours <= 30 else "En veille" if jours <= 90 else "Dormant"

def clients():
    return sorted(c for c in os.listdir(CL) if os.path.isdir(os.path.join(CL, c))
                  and not c.startswith(".") and c.strip() not in IGN_DIRS)

def recap_global():
    suivi = lire_suivi()
    rows, vus = [], set()
    for c in clients():
        files, obs, fams, subs = scan(os.path.join(CL, c))
        last = files[0] if files else None
        jours = (TODAY - datetime.date.fromtimestamp(last[0])).days if last else 9999
        s = suivi_pour(c, suivi)
        for o, l in s: vus.add((o, l.get("Entreprise")))
        rows.append(dict(nom=c.strip(), n=len(files), obs=obs, last=last, jours=jours,
                         statut=statut(jours) if last else "Vide", fams=fams, suivi=s))
    L = [f"# Récap des dossiers MDC — {TODAY.strftime('%d/%m/%Y')}", "",
         f"Source : `~/Documents/DOSSIER CLIENTS` ({len(rows)} dossiers) et `SUIVI_DES_DOSSIERS_MDC.xlsx`.", ""]
    cpt = {k: sum(r["statut"] == k for r in rows) for k in ("Actif", "En veille", "Dormant", "Vide")}
    L += ["## Vue d'ensemble", "",
          f"- Actifs (modifiés depuis 30 jours ou moins) : **{cpt['Actif']}**",
          f"- En veille (31 à 90 jours) : **{cpt['En veille']}**",
          f"- Dormants (plus de 90 jours) : **{cpt['Dormant']}**",
          f"- Vides : **{cpt['Vide']}**",
          f"- Inscrits au classeur de suivi : **{sum(bool(r['suivi']) for r in rows)}**", ""]
    L += ["## Tableau des dossiers", "",
          "| Dossier | Statut | Dernier mouvement | Fichiers | Suivi | Dernier document |",
          "|---|---|---|---:|---|---|"]
    for r in sorted(rows, key=lambda r: r["jours"]):
        lm = d(r["last"][0]) if r["last"] else "—"
        ld = os.path.basename(r["last"][1]).replace("|", "/") if r["last"] else "—"
        sv = ", ".join(sorted({o for o, _ in r["suivi"]})) or "—"
        L.append(f"| {r['nom']} | {r['statut']} | {lm} | {r['n']} | {sv} | {ld[:70]} |")
    L += ["", "## Points d'attention", ""]
    for r in sorted(rows, key=lambda r: r["jours"]):
        if r["statut"] != "Actif": continue
        manque = [f for f, _ in FAMILLES[:4] if f not in r["fams"]]
        info = [resume_suivi(o, l) for o, l in r["suivi"]]
        L.append(f"### {r['nom']}")
        for i in info: L.append(f"- {i}")
        if manque: L.append(f"- Pièces de cadrage non trouvées dans le dossier : {', '.join(manque)}")
        if r["obs"]: L.append(f"- {r['obs']} fichier(s) obsolète(s) conservé(s)")
        L.append("")
    orph = [(o, l.get("Entreprise")) for o, ls in suivi.items() if not o.startswith("_")
            for l in ls if (o, l.get("Entreprise")) not in vus]
    if orph:
        L += ["## Inscrits au suivi sans dossier à leur nom (création rattachée à un autre dossier, ou nom à harmoniser)", ""]
        L += [f"- {e} ({o})" for o, e in orph]
        L.append("")
    dorm = [r["nom"] for r in rows if r["statut"] in ("Dormant", "Vide")]
    if dorm: L += ["## Dossiers dormants ou vides", "", ", ".join(dorm), ""]
    if "_erreur" in suivi: L += [f"> Classeur de suivi illisible : {suivi['_erreur']}", ""]
    os.makedirs(OUTDIR, exist_ok=True)
    out = f"{OUTDIR}/RECAP_DOSSIERS_{TODAY.strftime('%Y-%m-%d')}.md"
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(out)

def fiche(nom):
    cands = [c for c in clients() if same(c, nom)] or [c for c in os.listdir(CL) if same(c, nom)]
    if not cands: sys.exit(f"Aucun dossier ne correspond à « {nom} ».")
    for c in cands:
        files, obs, fams, subs = scan(os.path.join(CL, c))
        print(f"# Fiche dossier — {c.strip()}  ({TODAY.strftime('%d/%m/%Y')})\n")
        print(f"Chemin : ~/Documents/DOSSIER CLIENTS/{c}")
        print(f"{len(files)} fichiers actifs, {obs} obsolètes, sous-dossiers : {', '.join(subs) or 'aucun'}\n")
        print("## Suivi"); s = suivi_pour(c, lire_suivi())
        for o, l in s: print("- " + resume_suivi(o, l))
        if not s: print("- Non inscrit au classeur de suivi")
        print("\n## Documents par famille (le plus récent)")
        for f, _ in FAMILLES:
            print(f"- {f} : " + (f"{d(fams[f][0])} · {fams[f][1]}" if f in fams else "non trouvé"))
        print("\n## 15 derniers fichiers")
        for t, rel in files[:15]: print(f"- {d(t)} · {rel}")
        print()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--client")
    a = ap.parse_args()
    fiche(a.client) if a.client else recap_global()
