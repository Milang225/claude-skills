"""Consolide les points des collaborateurs en un POINT GLOBAL DES DOSSIERS classé par priorité.

    python3 consolider.py SORTIE.xlsx POINT1.xlsx [POINT2.csv …] [--date 2026-11-26] [--seuil 7] [--horizon 7]
        [--sortants "Claude;SOGBOU"] [--clients liste_clients.txt]

Entrées : fichiers du modèle (modele_point.py, feuille « Point des dossiers ») ou CSV dont l'en-tête reprend
les clés ou les titres de grille.py (Claude transcrit dans ce CSV les points reçus en texte libre).
--clients : liste de TOUS les clients en cours (un par ligne, ou CSV avec une colonne client) : ceux qui
n'ont aucun point sont signalés — c'est le premier risque d'oubli.
--sortants : collaborateurs qui quittent le cabinet : leurs dossiers sont marqués « à réaffecter ».

Règles (dates relatives à --date, par défaut aujourd'hui) :
  • mois attendu : M-1 après le 15 du mois, M-2 avant (comptabilité et déclarations mensuelles) ;
  • URGENT : échéance ou action proposée dépassée ; déclaration fiscale en retard d'un mois ou plus ;
    comptabilité en retard de 2 mois ou plus ; contrôle fiscal en cours ; paie en retard ;
    blocage avec une échéance dans l'horizon ;
  • À ANTICIPER : échéance dans l'horizon ; comptabilité en retard d'un mois ; déclaration sociale en
    retard ; états financiers « en cours » ou « non commencés » ; pièces manquantes ;
  • OUBLIÉ : dernière intervention plus ancienne que le seuil (ou inconnue) ;
  • À COMPLÉTER : colonne obligatoire vide ou valeur illisible (relance du collaborateur) ; une telle ligne,
    comme une ligne sans action concrète, n'est jamais « à jour » (au moins « à anticiper »).
Écrit SORTIE.xlsx (Synthèse, Dossiers, À compléter, Plan proposé, Sans point) et un résumé JSON sur la sortie.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grille import CLES, COLONNES, OBLIGATOIRES, TITRES  # noqa: E402

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

NIVEAUX = ["urgent", "anticiper", "oublie", "ok"]
LIB = {"urgent": "🔴 Urgent", "anticiper": "🟠 À anticiper", "oublie": "⚪ Non touché", "ok": "✅ À jour"}
COULEUR = {"urgent": "FBE6E3", "anticiper": "FAF0D4", "oublie": "EEF0F3", "ok": "E6F3EC"}


def cle_nom(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\b(sarl|sa|sas|sasu|suarl|ets|etablissements?|ste|societe|eurl|gie)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def en_date(v):
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v).strip()
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%Y/%m/%d"):
        try:
            return dt.datetime.strptime(s[:10], f).date()
        except ValueError:
            pass
    return "illisible"


def en_mois(v):
    """Retourne (annee, mois) ou None ou 'illisible'."""
    if v is None or v == "":
        return None
    if isinstance(v, (dt.date, dt.datetime)):
        return (v.year, v.month)
    s = str(v).strip()
    m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})(?:[-/.]\d{1,2})?", s) or None
    if m:
        return (int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r"(\d{1,2})[-/.](\d{4})", s)
    if m:
        return (int(m.group(2)), int(m.group(1)))
    mois = {"janv": 1, "fev": 2, "mars": 3, "avr": 4, "mai": 5, "juin": 6, "juil": 7, "aout": 8, "sept": 9, "oct": 10, "nov": 11, "dec": 12}
    t = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    m = re.fullmatch(r"([a-z]+)\.?\s+(\d{4})", t)
    if m:
        for k, n in mois.items():
            if m.group(1).startswith(k):
                return (int(m.group(2)), n)
    return "illisible"


def ecart_mois(a, b):
    return (b[0] - a[0]) * 12 + (b[1] - a[1])


def lire_fichier(chemin):
    lignes = []
    titres_inv = {}
    for k, t in TITRES.items():
        titres_inv[cle_nom(t)] = k
        titres_inv[k] = k
    def cle_colonne(h):
        h = re.sub(r"\s*\*\s*$", "", str(h or "")).strip()
        return titres_inv.get(h) or titres_inv.get(cle_nom(h))
    if chemin.lower().endswith(".csv"):
        with open(chemin, newline="", encoding="utf-8-sig") as f:
            echantillon = f.read(4096); f.seek(0)
            delim = ";" if echantillon.count(";") > echantillon.count(",") else ","
            for r in csv.DictReader(f, delimiter=delim):
                lignes.append({cle_colonne(h): v for h, v in r.items() if cle_colonne(h)})
    else:
        wb = load_workbook(chemin, data_only=True)
        ws = wb["Point des dossiers"] if "Point des dossiers" in wb.sheetnames else wb.active
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            return []
        cles = [cle_colonne(h) for h in rows[0]]
        debut = 1
        aides = {c[2] for c in COLONNES}
        if len(rows) > 1 and any(v in aides for v in rows[1] if v):
            debut = 2
        for r in rows[debut:]:
            lignes.append({k: v for k, v in zip(cles, r) if k})
    out = []
    for i, l in enumerate(lignes):
        if not any(str(v or "").strip() for k, v in l.items() if k not in ("collaborateur",)):
            continue
        l = {k: (v.strip() if isinstance(v, str) else v) for k, v in l.items()}
        l["_source"] = f"{os.path.basename(chemin)} ligne {i + (2 if chemin.lower().endswith('.csv') else 3)}"
        out.append(l)
    return out


def analyser(l, ref, seuil, horizon, sortants):
    alertes, completer, niveau = [], [], set()
    ponctuel = str(l.get("suivi") or "").lower().startswith("ponct")
    for k in OBLIGATOIRES:
        if ponctuel and k in ("compta_a_jour", "fiscal_depose", "dsf"):
            continue   # mission ponctuelle : pas de tenue ni de déclarations mensuelles exigées
        if l.get(k) in (None, ""):
            completer.append(f"« {TITRES[k]} » vide")
    a = ref.day > 15
    attendu = (ref.year, ref.month - 1) if a else (ref.year, ref.month - 2)
    if attendu[1] <= 0:
        attendu = (attendu[0] - 1, attendu[1] + 12)
    suivi = str(l.get("suivi") or "").lower()
    mensuel = not suivi.startswith("ponct")
    for k, lib, lim_u in (("compta_a_jour", "Comptabilité", 2), ("fiscal_depose", "Déclarations fiscales", 1), ("social_depose", "Déclarations sociales", None)):
        m = en_mois(l.get(k))
        if m == "illisible":
            completer.append(f"« {TITRES[k]} » illisible : {l.get(k)} (format AAAA-MM)")
        elif m and mensuel:
            r = ecart_mois(m, attendu)
            if r > 0:
                alertes.append(f"{lib} en retard de {r} mois (à jour jusqu'à {m[1]:02d}/{m[0]})")
                niveau.add("urgent" if lim_u and r >= lim_u else "anticiper")
    dates = {}
    for k in ("prochaine_echeance", "derniere_intervention", "pour_quand"):
        d = en_date(l.get(k))
        if d == "illisible":
            completer.append(f"« {TITRES[k]} » illisible : {l.get(k)} (format AAAA-MM-JJ)")
            d = None
        dates[k] = d
    e = dates["prochaine_echeance"]
    if e:
        j = (e - ref).days
        objet = f" ({l.get('objet_echeance')})" if l.get("objet_echeance") else ""
        if j < 0:
            alertes.append(f"Échéance dépassée depuis {-j} j{objet}"); niveau.add("urgent")
        elif j <= horizon:
            alertes.append(f"Échéance dans {j} j{objet}"); niveau.add("anticiper")
            if l.get("blocage"):
                alertes.append("Bloqué alors que l'échéance approche"); niveau.add("urgent")
    p = dates["pour_quand"]
    if p and p < ref:
        alertes.append(f"Action proposée déjà en retard de {(ref - p).days} j"); niveau.add("urgent")
    if not str(l.get("action_proposee") or "").strip() or re.fullmatch(r"(?i)\s*(voir|suivre|ras|rien|néant|neant|-)\s*(le dossier)?\s*", str(l.get("action_proposee") or "")):
        alertes.append("Aucune action concrète proposée"); niveau.add("anticiper")
    if str(l.get("controle") or "").lower().startswith("oui"):
        alertes.append("Contrôle fiscal / redressement en cours"); niveau.add("urgent")
    if str(l.get("paie") or "").lower().startswith("en retard"):
        alertes.append("Paie en retard"); niveau.add("urgent")
    dsf = str(l.get("dsf") or "")
    if dsf in ("En cours", "Non commencés"):
        alertes.append(f"États financiers {dsf.lower()}"); niveau.add("anticiper")
    if l.get("pieces_manquantes"):
        alertes.append("Pièces manquantes : " + str(l["pieces_manquantes"])[:120]); niveau.add("anticiper")
    try:
        h = float(str(l.get("honoraires_impayes") or 0).replace(" ", "").replace(" ", "").replace(",", "."))
    except ValueError:
        h = 0.0; completer.append(f"« {TITRES['honoraires_impayes']} » illisible : {l.get('honoraires_impayes')}")
    if h > 0:
        alertes.append(f"Honoraires impayés : {h:,.0f} F".replace(",", " "))
    d = dates["derniere_intervention"]
    jours = (ref - d).days if d else None
    if jours is None or jours >= seuil:
        alertes.append("Aucune intervention connue" if jours is None else f"Non touché depuis {jours} j"); niveau.add("oublie")
    sortant = any(s and cle_nom(s) in cle_nom(l.get("collaborateur")) for s in sortants)
    if sortant:
        alertes.append("Collaborateur sortant : dossier à réaffecter")
    if completer:
        # Un dossier dont on ignore l'état n'est jamais « à jour ».
        alertes.append("Point incomplet : état réel inconnu tant que la ligne n'est pas complétée"); niveau.add("anticiper")
    n = next((x for x in NIVEAUX if x in niveau), "ok")
    return {"niveau": n, "alertes": alertes, "a_completer": completer, "sortant": sortant, "honoraires": h, "jours_sans_intervention": jours}


def lire_clients(chemin):
    noms = []
    with open(chemin, encoding="utf-8-sig") as f:
        for ligne in f:
            s = ligne.strip().split(";")[0].split(",")[0].strip().strip('"')
            if s and cle_nom(s) not in ("client", "raison sociale", "company"):
                noms.append(s)
    return noms


def consolider(sortie, fichiers, ref, seuil=7, horizon=7, sortants=(), clients_chemin=None):
    dossiers = []
    for f in fichiers:
        dossiers.extend(lire_fichier(f))
    vus = {}
    for d in dossiers:
        d.update(analyser(d, ref, seuil, horizon, sortants))
        k = cle_nom(d.get("client"))
        if k:
            vus.setdefault(k, []).append(d)
    for k, l in vus.items():
        if len(l) > 1:
            for d in l:
                d["alertes"].append("Dossier déclaré " + str(len(l)) + " fois (" + ", ".join(str(x.get("collaborateur") or "?") for x in l) + ") : un seul responsable à fixer")
    sans_point = []
    if clients_chemin:
        for nom in lire_clients(clients_chemin):
            if cle_nom(nom) not in vus:
                sans_point.append(nom)
    ordre = {n: i for i, n in enumerate(NIVEAUX)}
    dossiers.sort(key=lambda d: (ordre[d["niveau"]], str(d.get("collaborateur") or ""), str(d.get("client") or "")))

    wb = Workbook()
    gras = Font(bold=True)
    def entete(ws, titres, larg):
        for i, t in enumerate(titres, start=1):
            c = ws.cell(row=1, column=i, value=t); c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="172033")
            c.alignment = Alignment(wrap_text=True, vertical="center")
            ws.column_dimensions[get_column_letter(i)].width = larg[i - 1] if i - 1 < len(larg) else 18
        ws.freeze_panes = "A2"

    # Synthèse
    s = wb.active; s.title = "Synthèse"
    compte = {n: sum(1 for d in dossiers if d["niveau"] == n) for n in NIVEAUX}
    s.append([f"POINT GLOBAL DES DOSSIERS au {ref.strftime('%d/%m/%Y')}"]); s["A1"].font = Font(bold=True, size=14)
    s.append([f"{len(dossiers)} dossier(s) reçu(s) de {len({str(d.get('collaborateur') or '?') for d in dossiers})} collaborateur(s) ; seuil « non touché » {seuil} j ; horizon {horizon} j."])
    s.append([])
    for n in NIVEAUX:
        s.append([LIB[n], compte[n]])
    s.append(["Dossiers sans aucun point", len(sans_point) if clients_chemin else "liste des clients non fournie"])
    s.append(["Lignes à compléter (relances)", sum(1 for d in dossiers if d["a_completer"])])
    s.append(["Honoraires impayés déclarés (FCFA)", round(sum(d["honoraires"] for d in dossiers))])
    s.append([])
    s.append(["Par collaborateur", "Dossiers", "Urgents", "À anticiper", "Non touchés", "À compléter", "Honoraires impayés", "Sortant"])
    for c in s[s.max_row]:
        c.font = gras
    par = {}
    for d in dossiers:
        par.setdefault(str(d.get("collaborateur") or "Non indiqué"), []).append(d)
    for nom, l in sorted(par.items()):
        s.append([nom, len(l), sum(d["niveau"] == "urgent" for d in l), sum(d["niveau"] == "anticiper" for d in l), sum(d["niveau"] == "oublie" for d in l),
                  sum(1 for d in l if d["a_completer"]), round(sum(d["honoraires"] for d in l)), "OUI — à réaffecter" if any(d["sortant"] for d in l) else ""])
    s.column_dimensions["A"].width = 44
    for col in "BCDEFGH":
        s.column_dimensions[col].width = 16

    # Dossiers
    ws = wb.create_sheet("Dossiers")
    titres = ["Niveau", "Alertes"] + [TITRES[k] for k in CLES] + ["Source"]
    entete(ws, titres, [14, 60] + [30 if c[3] == "texte" else 16 for c in COLONNES] + [24])
    for d in dossiers:
        ws.append([LIB[d["niveau"]], "\n".join(d["alertes"])] + [d.get(k) for k in CLES] + [d["_source"]])
        for c in ws[ws.max_row]:
            c.fill = PatternFill("solid", fgColor=COULEUR[d["niveau"]]); c.alignment = Alignment(wrap_text=True, vertical="top")

    # À compléter
    wc = wb.create_sheet("À compléter")
    entete(wc, ["Collaborateur", "Client", "À compléter ou corriger", "Source"], [24, 32, 80, 24])
    for d in dossiers:
        if d["a_completer"]:
            wc.append([d.get("collaborateur"), d.get("client"), "\n".join(d["a_completer"]), d["_source"]])

    # Plan proposé
    wp = wb.create_sheet("Plan proposé")
    entete(wp, ["Niveau", "Client", "Action proposée", "Responsable proposé", "Pour quand", "Besoin du gérant", "Décision du gérant", "Statut"], [14, 32, 50, 26, 14, 40, 40, 14])
    for d in dossiers:
        resp = "À RÉAFFECTER (" + str(d.get("collaborateur")) + " sort)" if d["sortant"] else d.get("collaborateur")
        wp.append([LIB[d["niveau"]], d.get("client"), d.get("action_proposee") or "— à définir —", resp, d.get("pour_quand"), d.get("besoin_gerant"), "", "À valider"])

    # Sans point
    wn = wb.create_sheet("Sans point")
    entete(wn, ["Client sans aucun point reçu"], [50])
    for n in sans_point:
        wn.append([n])
    if not clients_chemin:
        wn.append(["(liste des clients non fournie : impossible de savoir qui manque)"])
    wb.save(sortie)

    return {"date": ref.isoformat(), "fichier": sortie, "dossiers": len(dossiers), "par_niveau": compte, "sans_point": sans_point,
            "a_completer": sum(1 for d in dossiers if d["a_completer"]), "sortants": sorted({str(d.get("collaborateur")) for d in dossiers if d["sortant"]}),
            "dossiers_sortants": sum(1 for d in dossiers if d["sortant"]),
            "urgents": [{"client": d.get("client"), "collaborateur": d.get("collaborateur"), "alertes": d["alertes"]} for d in dossiers if d["niveau"] == "urgent"][:40],
            "doublons": sorted({str(d.get("client")) for l in vus.values() if len(l) > 1 for d in l})}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sortie")
    p.add_argument("fichiers", nargs="+")
    p.add_argument("--date", default=dt.date.today().isoformat())
    p.add_argument("--seuil", type=int, default=7)
    p.add_argument("--horizon", type=int, default=7)
    p.add_argument("--sortants", default="")
    p.add_argument("--clients", default=None)
    a = p.parse_args()
    r = consolider(a.sortie, a.fichiers, dt.date.fromisoformat(a.date), a.seuil, a.horizon, [x.strip() for x in a.sortants.split(";") if x.strip()], a.clients)
    print(json.dumps(r, ensure_ascii=False, indent=1, default=str))
