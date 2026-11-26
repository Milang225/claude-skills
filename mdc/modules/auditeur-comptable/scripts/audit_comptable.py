#!/usr/bin/env python3
"""Auditeur comptable MDC — contrôle indépendant en trois axes.

  A. Écritures   : le contrôle bloquant du module ecritures-sans-faute (comptes, schémas, paie, stocks…).
  B. Principes   : principes comptables SYSCOHADA révisé (intangibilité du bilan d'ouverture, indépendance
                   des exercices, non-compensation, prudence, continuité, régularité et sincérité, coût historique).
  C. Mises à jour: le dossier contrôlé est la dernière version ; le skill (module, script, catalogue, taux,
                   listes d'opérations) est cohérent et à jour des dernières notes de revue.

Usage :
  audit_comptable.py ecritures JOURNAL.xlsx --exercice 2025 --forme SARL --regime RSI [--n1 BALANCE_N-1.xlsx]
  audit_comptable.py mises-a-jour
  audit_comptable.py tout JOURNAL.xlsx --exercice 2025 --forme SARL --regime RSI
Option --rapport FICHIER.md : écrit aussi le rapport dans un fichier.
Code retour : 0 conforme, 1 réserves bloquantes.
"""
import argparse
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

MDC = Path(__file__).resolve().parents[3]          # ~/.claude/skills/mdc
MODULES = MDC / "modules"
ESF = MODULES / "ecritures-sans-faute"
sys.path.insert(0, str(ESF / "scripts"))
import controle_ecritures as ce  # noqa: E402

LISTES = Path.home() / "SKILL COMPTABLE"
NOTES_RECUES = Path.home() / "Documents" / "DOCUMENTS_RECUS_PAR_MAIL"
TAUX = MODULES / "fiscalite-ci" / "reference" / "TAUX_ET_SEUILS.md"
CATALOGUE = ESF / "reference" / "CATALOGUE_NOTES_DE_REVUE.md"


class Rapport:
    def __init__(self):
        self.axes = {}

    def axe(self, code, titre):
        self.axes[code] = {"titre": titre, "bloquant": [], "reserve": [], "ok": []}
        return self.axes[code]

    def texte(self):
        out = ["# Rapport de l'auditeur comptable MDC", f"_Édité le {datetime.now():%d/%m/%Y à %H:%M}_", ""]
        bloque = False
        for code, a in self.axes.items():
            verdict = "NON CONFORME" if a["bloquant"] else ("CONFORME AVEC RÉSERVES" if a["reserve"] else "CONFORME")
            bloque |= bool(a["bloquant"])
            out += [f"## Axe {code} — {a['titre']} : **{verdict}**", ""]
            if a["bloquant"]:
                out += [f"**Points bloquants ({len(a['bloquant'])})**", ""] + [f"- ✗ {m}" for m in a["bloquant"]] + [""]
            if a["reserve"]:
                out += [f"**Réserves à justifier ({len(a['reserve'])})**", ""] + [f"- ! {m}" for m in a["reserve"]] + [""]
            if a["ok"]:
                out += ["**Vérifié sans observation**", ""] + [f"- ✓ {m}" for m in a["ok"]] + [""]
        out += ["## Conclusion", "",
                "**NE PAS REMETTRE** : lever les points bloquants, puis relancer l'auditeur." if bloque
                else "Aucun point bloquant. Les réserves doivent être justifiées par écrit (grille de rapprochements) avant remise.",
                "", "_Les contrôles automatiques ne remplacent pas la revue des pièces : la grille G1-G12 du module "
                "ecritures-sans-faute reste à remplir à la main._"]
        return "\n".join(out), bloque


def fmt(x):
    return ce.fmt(x)


def regrouper(lignes, n=40):
    """Condense une longue liste de messages identiques (même texte après la référence de ligne)."""
    par_msg = defaultdict(list)
    for m in lignes:
        ref, _, txt = m.partition("] ")
        par_msg[txt or m].append(ref + "]" if txt else "")
    res = []
    for txt, refs in par_msg.items():
        refs = [r for r in refs if r]
        if len(refs) > 3:
            res.append(f"{txt} — {len(refs)} lignes ({', '.join(refs[:3])} …)")
        else:
            res += [f"{r} {txt}".strip() for r in refs] or [txt]
    return res[:n] + ([f"… et {len(res) - n} autres"] if len(res) > n else [])


# ---------------------------------------------------------------- Axe A — écritures
def axe_ecritures(R, ecr, a, plan):
    A = R.axe("A", "Écritures (contrôle bloquant ecritures-sans-faute)")
    err, ale = ce.controler(ecr, a.exercice, a.forme, plan, a.regime, a.regularisations)
    A["bloquant"] += regrouper(err)
    A["reserve"] += regrouper(ale)
    if not err:
        A["ok"].append(f"{len(ecr)} lignes : comptes AUDCIF, équilibre, schémas, paie, stocks, à-nouveaux sans erreur bloquante")
    if not a.regime:
        A["reserve"].append("régime fiscal non indiqué (--regime TEE/RME/RSI/RNI) : la règle R13 (classe 89) n'a pas pu être appliquée")


# ---------------------------------------------------------------- Axe B — principes
def soldes(ecr, filtre=lambda e: True):
    s = defaultdict(float)
    for e in ecr:
        if filtre(e):
            s[e["compte"]] += e["debit"] - e["credit"]
    return s


def lire_balance_n1(chemin):
    """Balance ou bilan N-1 : colonnes compte + (solde) ou (débit, crédit). Renvoie {compte: solde débiteur}."""
    import csv
    p = Path(chemin)
    if p.suffix.lower() in {".xlsx", ".xlsm"}:
        import openpyxl
        lignes = [list(r) for r in openpyxl.load_workbook(p, data_only=True).active.iter_rows(values_only=True)]
    else:
        txt = p.read_text(encoding="utf-8-sig")
        lignes = list(csv.reader(txt.splitlines(), delimiter=";" if txt.count(";") > txt.count(",") else ","))
    i = next(i for i, r in enumerate(lignes) if any(str(c or "").strip().lower() in ("compte", "n° compte") for c in r))
    ent = [str(c or "").strip().lower() for c in lignes[i]]
    ic = next(j for j, c in enumerate(ent) if c in ("compte", "n° compte"))
    isd = next((j for j, c in enumerate(ent) if c.startswith("solde")), None)
    idb = next((j for j, c in enumerate(ent) if c.startswith(("débit", "debit", "solde débit", "solde debit"))), None)
    icr = next((j for j, c in enumerate(ent) if c.startswith(("crédit", "credit", "solde crédit", "solde credit"))), None)
    res = {}
    for r in lignes[i + 1:]:
        c = re.sub(r"\D", "", str(r[ic] or "").removesuffix(".0"))
        if not c or c[0] not in "12345":
            continue
        if isd is not None and idb is None:
            v = ce.montant(r[isd])
        else:
            v = ce.montant(r[idb] if idb is not None else 0) - ce.montant(r[icr] if icr is not None else 0)
        res[c] = res.get(c, 0) + v
    return res


def axe_principes(R, ecr, a):
    B = R.axe("B", "Principes comptables SYSCOHADA révisé")
    an = [e for e in ecr if e["journal"] in ce.JOURNAUX_AN]
    hors_an = [e for e in ecr if e["journal"] not in ce.JOURNAUX_AN]
    fin = date(a.exercice, 12, 31)
    societe = a.forme.upper() in ce.SOCIETES

    # B1 Intangibilité du bilan d'ouverture
    if not an:
        B["reserve"].append("B1 intangibilité : aucun journal d'à-nouveaux (AN/RAN) — première année ? Sinon reprendre le bilan N-1 visé")
    else:
        sd, sc = sum(e["debit"] for e in an), sum(e["credit"] for e in an)
        if abs(sd - sc) > 0.5:
            B["bloquant"].append(f"B1 intangibilité : à-nouveaux déséquilibrés (D {fmt(sd)} / C {fmt(sc)})")
        if a.n1:
            n1 = lire_balance_n1(a.n1)
            s_an = soldes(an)
            # comparaison par racine à 3 chiffres (les sous-comptes Sage varient d'un fichier à l'autre)
            r4 = lambda d: {k: v for k, v in _par_racine(d, 3).items() if abs(v) > 0.5}
            x, y = r4(s_an), r4(n1)
            ecarts = [(c, x.get(c, 0), y.get(c, 0)) for c in sorted(set(x) | set(y)) if abs(x.get(c, 0) - y.get(c, 0)) > 0.5]
            if ecarts:
                B["bloquant"].append("B1 intangibilité : à-nouveaux ≠ bilan N-1 sur " + f"{len(ecarts)} compte(s) : "
                                     + " ; ".join(f"{c} AN {fmt(u)} / N-1 {fmt(v)}" for c, u, v in ecarts[:12]))
            else:
                B["ok"].append(f"B1 intangibilité : à-nouveaux = bilan N-1 au franc ({len(y)} comptes)")
        else:
            B["reserve"].append("B1 intangibilité : bilan N-1 non fourni (--n1) — rapprochement G1 à faire compte par compte")

    # B2 Indépendance des exercices (rattachement)
    autres_annees = []
    for e in hors_an:
        if e["compte"][0] in "67" and not e["compte"].startswith(("68", "69", "78", "79", "892", "899")):
            annees = {int(y) for y in re.findall(r"\b(20[12]\d)\b", e["libelle"])}
            if annees and a.exercice not in annees and not re.search(r"extourne|annulation|r[ée]gularis|rappel", e["libelle"], re.I):
                autres_annees.append(f"L{e['ligne']} {e['compte']} « {e['libelle'][:60]} »")
    if autres_annees:
        B["reserve"].append(f"B2 indépendance des exercices : {len(autres_annees)} charge(s)/produit(s) dont le libellé vise une autre année — "
                            "rattacher à son exercice (dette à l'ouverture, 129/121 si erreur significative) : " + " ; ".join(autres_annees[:6]))
    cloture = [e for e in hors_an if e["compte"].startswith(("408", "4181", "476", "477", "4286", "4386", "4486", "4496", "1662"))]
    if not cloture and len(hors_an) > 30:
        B["reserve"].append("B2 indépendance des exercices : aucune régularisation de clôture (408, 4181, 476, 477, 4486…) — "
                            "vérifier factures non parvenues, charges constatées d'avance, intérêts courus")
    elif cloture:
        B["ok"].append(f"B2 indépendance des exercices : {len(cloture)} ligne(s) de régularisation de clôture")

    # B3 Non-compensation (présentation : chaque solde à sa place)
    s = soldes(ecr)
    agr = _par_racine(s, 0)
    inv = []
    for c, v in sorted(agr.items()):
        if c.startswith("401") and v > 0.5:
            inv.append(f"{c} fournisseur débiteur {fmt(v)} → 409 (avance) ou erreur")
        elif c.startswith("411") and v < -0.5:
            inv.append(f"{c} client créditeur {fmt(-v)} → 419 (avance reçue) ou erreur")
        elif c.startswith("521") and v < -0.5:
            inv.append(f"{c} banque créditrice {fmt(-v)} → 565 concours bancaires à la clôture (sauf rapprochement)")
        elif c.startswith(("4452", "4454")) and v < -0.5:
            inv.append(f"{c} TVA récupérable créditrice {fmt(-v)}")
        elif c.startswith(("4431", "4432", "4433", "4434")) and v > 0.5:
            inv.append(f"{c} TVA facturée débitrice {fmt(v)}")
    if inv:
        B["reserve"].append("B3 non-compensation : soldes de sens contraire à reclasser au bilan — " + " ; ".join(inv[:10])
                            + (f" … (+{len(inv) - 10})" if len(inv) > 10 else ""))
    else:
        B["ok"].append("B3 non-compensation : tiers, banques et TVA de sens normal")
    meme = [ls for ls in _pieces(hors_an).values()
            if any(x["debit"] for x in ls) and any(
                x["compte"] == y["compte"] and x["debit"] and y["credit"] for x in ls for y in ls)]
    if meme:
        B["reserve"].append(f"B3 non-compensation : {len(meme)} pièce(s) débitent et créditent le même compte (compensation interne ?) — ex. "
                            + ", ".join(f"{l[0]['journal']} {l[0]['piece']}" for l in meme[:5]))

    # B4 Prudence
    immo = sum(v for c, v in s.items() if c.startswith(("21", "22", "23", "24")) and v > 0)
    dot = sum(e["debit"] for e in hors_an if e["compte"].startswith(("6812", "6813", "681")))
    if immo > 0.5 and not dot:
        B["bloquant"].append(f"B4 prudence : immobilisations amortissables {fmt(immo)} sans aucune dotation 681 — "
                             "l'amortissement est obligatoire, même en cas de perte (prorata depuis la mise en service)")
    elif immo:
        B["ok"].append(f"B4 prudence : dotations aux amortissements passées ({fmt(dot)})")
    douteux = sum(v for c, v in s.items() if c.startswith("416"))
    if douteux > 0.5 and not any(c.startswith("491") for c in s):
        B["reserve"].append(f"B4 prudence : clients douteux 416 ({fmt(douteux)}) sans dépréciation 491 (calculée hors taxe)")
    stock = sum(v for c, v in s.items() if c.startswith(("31", "32", "33", "34", "35", "36", "37", "38")))
    if stock > 0.5 and not any(c.startswith("39") for c in s):
        B["reserve"].append(f"B4 prudence : stock {fmt(stock)} sans dépréciation 39 — confirmer par l'inventaire qu'aucun article n'est abîmé, périmé ou invendable")
    clients = sum(v for c, v in s.items() if c.startswith("411") and v > 0)
    if clients > 0.5:
        B["reserve"].append(f"B4 prudence : créances clients {fmt(clients)} au 31/12 — balance âgée et encaissements de début N+1 à vérifier (dépréciation si litige)")

    # B5 Continuité d'exploitation
    resultat = -sum(v for c, v in s.items() if c[0] in "678")
    cp = -sum(v for c, v in s.items() if c.startswith(("10", "11", "12", "13", "14", "15"))) + resultat
    capital = -sum(v for c, v in s.items() if c.startswith(("101", "102", "103")))
    if capital > 0 and cp < capital / 2:
        B["reserve"].append(f"B5 continuité : capitaux propres {fmt(cp)} < moitié du capital {fmt(capital)} (résultat {fmt(resultat)}) — "
                            + ("consultation des associés dans les 4 mois de l'approbation des comptes (AUSCGIE) et " if societe else "")
                            + "mention obligatoire en note 2")
    elif capital > 0:
        B["ok"].append(f"B5 continuité : capitaux propres {fmt(cp)} ≥ moitié du capital {fmt(capital)}")
    if cp < 0:
        B["reserve"].append(f"B5 continuité : capitaux propres négatifs ({fmt(cp)}) — plan de redressement / soutien des associés à documenter (note 2)")

    # B6 Régularité et sincérité (pièces, libellés)
    vides = [e for e in ecr if not e["libelle"]]
    if vides:
        B["bloquant"].append(f"B6 régularité : {len(vides)} ligne(s) sans libellé (ex. L{vides[0]['ligne']})")
    flous = [e for e in hors_an if re.search(r"\b(divers|[ée]quilibr|ajustement|[ée]cart|r[ée]gul\b|solde de tout|forfait)\b", e["libelle"], re.I)
             and e["compte"][0] in "4567"]
    if flous:
        B["reserve"].append(f"B6 sincérité : {len(flous)} ligne(s) au libellé vague (« divers », « équilibre », « écart »…) — chaque ligne doit nommer la nature, le tiers et la pièce : "
                            + " ; ".join(f"L{e['ligne']} {e['compte']} « {e['libelle'][:40]} »" for e in flous[:5]))
    dates_par_piece = defaultdict(set)
    for e in hors_an:
        if e["piece"]:
            dates_par_piece[(e["journal"], e["piece"])].add(e["date"])
    doublons = [k for k, v in dates_par_piece.items() if len(v) > 1]
    if doublons:
        B["reserve"].append(f"B6 régularité : {len(doublons)} n° de pièce réutilisé(s) à des dates différentes dans le même journal — ex. "
                            + ", ".join(f"{j} {p}" for j, p in doublons[:5]))
    sans_piece = [e for e in hors_an if not e["piece"]]
    if sans_piece:
        B["bloquant"].append(f"B6 régularité : {len(sans_piece)} ligne(s) sans n° de pièce (ex. L{sans_piece[0]['ligne']})")
    if not (vides or sans_piece):
        B["ok"].append("B6 régularité : chaque ligne porte une pièce et un libellé")

    # B7 Coût historique
    if any(c.startswith("106") for c in s):
        B["reserve"].append("B7 coût historique : écart de réévaluation 106 — réévaluation légale ou libre documentée (expert, note annexe) ?")
    if not any(c.startswith("106") for c in s):
        B["ok"].append("B7 coût historique : aucune réévaluation")

    # B8 Permanence des méthodes (signal seulement)
    if a.n1 is None:
        B["reserve"].append("B8 permanence des méthodes : comparer avec N-1 (méthode de stock, durées d'amortissement, plan de comptes) — note annexe si changement")


def _par_racine(d, n):
    """Regroupe des soldes par racine de n chiffres (n = 0 : sans regroupement)."""
    if not n:
        return dict(d)
    res = defaultdict(float)
    for c, v in d.items():
        res[c[:n]] += v
    return res


def _pieces(ecr):
    p = defaultdict(list)
    for e in ecr:
        p[(e["journal"], e["piece"], e["date"])].append(e)
    return p


# ---------------------------------------------------------------- Axe C — mises à jour
CAS_NON_REGRESSION = [
    # (compte, libellé, forme, régime, ce que la revue a relevé) — chaque cas doit produire une erreur
    ("6313", "Contribution employeur janvier", "SARL", "RSI", "TRACE : 6313 pour la CE"),
    ("4616", "Souscription capital associé A", "SARL", "RSI", "TRACE : 4616 pour la souscription"),
    ("4611", "Libération capital par virement", "SARL", "RSI", "TRACE : 4611 pour un apport en numéraire"),
    ("629000", "Frais bancaires janvier", "SARL", "RSI", "TRACE : 629 inexistant"),
    ("624100", "Électricité CIE janvier", "SARL", "RSI", "TRACE : 624 pour l'électricité"),
    ("624200", "Facture d'eau SODECI janvier", "SARL", "RSI", "TRACE : 624 pour l'eau"),
    ("626000", "Téléphone Orange janvier", "SARL", "RSI", "TRACE : 626 pour le téléphone"),
    ("702", "Prestation de services client X", "SARL", "RSI", "TIM 7 n° 4 : 702 pour des services"),
    ("196", "Provision pour litige prud'homal", "SARL", "RSI", "TIM 7 n° 4 : 196 pour un litige"),
    ("422", "Loyer bureau janvier bailleur Y", "SARL", "RSI", "KWAANI 3.1 : loyer en 422"),
    ("4486", "Pénalités AMR 2024", "SARL", "RSI", "KWAANI 3.5 : pénalités en 4486"),
    ("401", "Salaires janvier", "SARL", "RSI", "KRA 3.6 : salaires en 401"),
    ("6414/5", "FDFP janvier", "SARL", "RSI", "KRA 3.6 : « 6414/5 »"),
    ("6413", "Taxe d'apprentissage janvier", "EI", "TEE", "KG Q1 : TA en 6413"),
    ("891", "Impôt TEE 2025", "EI", "TEE", "KG : classe 89 au forfait"),
    ("446", "Patente 2025", "EI", "TEE", "KG : patente par 446"),
    ("447", "ITS janvier à payer", "SARL", "RSI", "KRA 3.7 : racine 447 non ventilée"),
    ("6132", "Loyer magasin janvier", "SARL", "RSI", "KRA : 6132 inexistant"),
    ("6041", "Carburant véhicule", "SARL", "RSI", "KRA : carburant en 6041"),
    ("6241", "Entretien camion", "SARL", "RSI", "KRA : 6241 (immobiliers) pour un camion"),
    ("6271", "Transport et manutention sur achats", "SARL", "RSI", "KRA : 6271 (publicité) pour le transport sur achats"),
    ("7062", "Commissions sur ventes mandants", "SARL", "RSI", "KRA : 7062 pour des commissions"),
    ("4671", "Mandants ventes pour compte", "SARL", "RSI", "KRA : 4671 inexistant"),
    ("6388", "Autres charges externes diverses", "SARL", "RSI", "KRA : 6388 inexistant"),
    ("103", "Capital social", "SARL", "RSI", "KRA : 103 dans une SARL"),
    ("101", "Capital", "EI", "TEE", "KG : 101 chez une EI"),
]


CAS_CONFORMES = [
    # écritures justes qui ne doivent PAS être rejetées (garde contre les faux positifs)
    ("647100", "Pénalités sur l'impôt sur les salaires de janvier 2025", "SARL", "RSI"),
    ("6242", "Entretien camion", "SARL", "RSI"),
    ("6611", "Salaires bruts janvier", "SARL", "RSI"),
    ("6413", "Contribution nationale 1,2 % janvier", "SARL", "RSI"),
    ("6414", "Taxe d'apprentissage janvier", "SARL", "RSI"),
    ("6415", "Formation professionnelle continue janvier", "SARL", "RSI"),
    ("6053", "Carburant véhicule de livraison", "SARL", "RSI"),
    ("6222", "Loyer bureau janvier", "SARL", "RSI"),
    ("6318", "Frais bancaires janvier", "SARL", "RSI"),
    ("6418", "TEE janvier 2025", "EI", "TEE"),
    ("7061", "Prestation de services client X", "SARL", "RSI"),
    ("6911", "Provision pour pénalités et intérêts de retard 2025", "SARL", "RSI"),
    ("601", "Achats d'eau ESSENTIELLE pour la cantine", "SARL", "RSI"),
    ("6051", "Facture d'eau SODECI janvier", "SARL", "RSI"),
]


def _test(compte, lib, forme, regime, plan):
    num = re.sub(r"\D", "", compte)
    ecr = [
        {"ligne": 2, "journal": "OD", "date": date(2025, 3, 15), "piece": "T1", "compte": num, "brut": compte,
         "tiers": "", "libelle": lib, "debit": 1000.0, "credit": 0.0},
        {"ligne": 3, "journal": "OD", "date": date(2025, 3, 15), "piece": "T1", "compte": "4011001", "brut": "4011001",
         "tiers": "X", "libelle": "Tiers X", "debit": 0.0, "credit": 1000.0},
    ]
    err, _ = ce.controler(ecr, 2025, forme, plan, regime, regul=True)
    return [m for m in err if m.startswith("L2 ")]


def faux_positifs(plan):
    return [f"{c} « {l} » rejeté à tort : {_test(c, l, f, r, plan)[0]}" for c, l, f, r in CAS_CONFORMES if _test(c, l, f, r, plan)]


def non_regression(plan):
    rates = []
    for compte, lib, forme, regime, origine in CAS_NON_REGRESSION:
        if not _test(compte, lib, forme, regime, plan):
            rates.append(f"{compte} « {lib} » ({origine})")
    return rates


def comptes_cites(texte, colonnes=None):
    """Numéros de comptes cités : dans les colonnes indiquées des tableaux markdown, sinon dans les blocs « D xxx / C xxx ».
    Les numéros de pages (p. 284-286), d'articles, les montants et les titres ne sont pas pris."""
    res = set()
    for ligne in texte.splitlines():
        if colonnes is not None:
            if not ligne.startswith("|") or ligne.startswith("|---"):
                continue
            cells = [c.strip() for c in ligne.strip("|").split("|")]
            zones = [cells[i] for i in colonnes if i < len(cells)]
        else:
            zones = [ligne]
        for z in zones:
            z = re.sub(r"(p\.|art\.|ch\.|chap\.|n°|§)\s*[\d\s,\-–àet]+", " ", z)   # renvois de pages / articles
            for m in re.finditer(r"(?:\b[DC]\s+|\*\*)(\d{2,7})x*\b", z):
                res.add(m.group(1))
            if colonnes is not None:
                for m in re.finditer(r"(?<![\d\s.,/\-–])\b([1-8]\d{2,6})x*\b(?![\s\u202f\xa0]?(?:%|F\b|\d{3}|ans?\b|jours?|mois))", z):
                    res.add(m.group(1))
    return res


def compte_absent(c, plan):
    if len(c) == 2:
        return c not in plan
    return ce.verifier_compte(c, plan) is not None


def axe_mises_a_jour(R, plan, journal=None):
    C = R.axe("C", "Mises à jour (dossier et skill)")

    # C1 Le journal contrôlé est-il la dernière version du dossier ?
    if journal:
        p = Path(journal).resolve()
        racine = re.sub(r"(_REV\d+|_V\d+|_\d{8}|_\d{4}-\d{2}-\d{2}).*$", "", p.stem, flags=re.I)[:25]
        plus_recents = [f for f in p.parent.glob("*.xls*")
                        if f != p and not f.name.startswith(("~$", "OBSOLETE")) and f.name.startswith(racine[:15])
                        and f.stat().st_mtime > p.stat().st_mtime]
        if plus_recents:
            C["bloquant"].append("C1 version : fichier(s) plus récent(s) dans le dossier — vous contrôlez peut-être une version dépassée : "
                                 + ", ".join(f.name for f in sorted(plus_recents, key=lambda f: -f.stat().st_mtime)[:4]))
        else:
            C["ok"].append(f"C1 version : {p.name} est la version la plus récente de sa série")

    # C2 Non-régression du script de contrôle sur les fautes déjà relevées par les réviseurs
    rates = non_regression(plan)
    if rates:
        C["bloquant"].append(f"C2 script : {len(rates)} faute(s) déjà relevée(s) en revue NE SONT PAS détectées par controle_ecritures.py — "
                             "ajouter la règle au script : " + " ; ".join(rates))
    else:
        C["ok"].append(f"C2 script : les {len(CAS_NON_REGRESSION)} fautes relevées en revue sont toutes détectées")
    fp = faux_positifs(plan)
    if fp:
        C["bloquant"].append(f"C2 script : {len(fp)} écriture(s) juste(s) rejetée(s) à tort (faux positif) : " + " ; ".join(fp))
    else:
        C["ok"].append(f"C2 script : les {len(CAS_CONFORMES)} écritures justes de référence passent sans erreur")

    # C3 Comptes cités dans le module et les listes : existent-ils dans le plan AUDCIF ?
    module = (ESF / "MODULE.md").read_text(encoding="utf-8")
    m2 = re.search(r"## 2\..*?(?=\n## 3\.)", module, re.S)
    m3 = re.search(r"## 3\..*?(?=\n## 4\.)", module, re.S)
    cites = comptes_cites(m2.group(0), colonnes=[1]) | comptes_cites(m3.group(0))
    sources = {"MODULE ecritures-sans-faute §2-§3": cites}
    for f in sorted(LISTES.glob("LISTE_OPERATIONS_*.md")):
        sources[f.name] = comptes_cites(f.read_text(encoding="utf-8"), colonnes=[2])
    for nom, cs in sources.items():
        faux = sorted(c for c in cs if compte_absent(c, plan))
        if faux:
            C["bloquant"].append(f"C3 plan AUDCIF : {nom} cite {len(faux)} compte(s) absent(s) du plan : {', '.join(faux[:20])}"
                                 " — vérifier (faute de frappe, compte supprimé, ou plan à compléter)")
        else:
            C["ok"].append(f"C3 plan AUDCIF : les {len(cs)} comptes cités dans {nom} existent")

    # C4 Taux à jour (paie)
    if TAUX.exists():
        t = TAUX.read_text(encoding="utf-8")
        attendus = {"contribution nationale **1,2 %**": "CN 1,2 %", "taxe d'apprentissage **0,4 %**": "TA 0,4 %",
                    "formation professionnelle continue **1,2 %**": "FPC 1,2 %"}
        manquants = [v for k, v in attendus.items() if k not in t]
        if manquants:
            C["reserve"].append("C4 taux : TAUX_ET_SEUILS ne mentionne plus " + ", ".join(manquants) + " — le contrôle de paie du script (2,2 %-2,8 %) est-il encore juste ?")
        else:
            C["ok"].append("C4 taux : CN 1,2 %, TA 0,4 %, FPC 1,2 % concordent entre TAUX_ET_SEUILS et le script")
        vieux = []
        for f in list(MODULES.glob("*/MODULE.md")) + list(MODULES.glob("*/reference/*.md")):
            for n, l in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if re.search(r"FDFP[^|\n]{0,25}\b1 ?%(?! \()", l) and not re.search(r"ancien|faute|à tort|erreur|relev|fusionn|pseudo", l, re.I):
                    vieux.append(f"{f.parent.parent.name if f.parent.name == 'reference' else f.parent.name}/{f.name}:{n}")
        if vieux:
            C["reserve"].append("C4 taux : mention d'un FDFP « 1 % » (ancien taux) sans avertissement : " + ", ".join(vieux[:8]))

    # C5 Catalogue des notes de revue : à jour des dernières notes reçues ? règles non scriptées ?
    if CATALOGUE.exists():
        cat = CATALOGUE.read_text(encoding="utf-8")
        cat_mtime = CATALOGUE.stat().st_mtime
        if NOTES_RECUES.exists():
            nouvelles = [d.name for d in NOTES_RECUES.iterdir()
                         if d.is_dir() and re.search(r"revue|visa", d.name, re.I) and d.stat().st_mtime > cat_mtime]
            if nouvelles:
                C["bloquant"].append("C5 catalogue : note(s) de revue reçue(s) après la dernière mise à jour du catalogue : "
                                     + " ; ".join(nouvelles[:6]) + " — l'ajouter au catalogue, au module et au script")
            else:
                C["ok"].append("C5 catalogue : aucune note de revue reçue depuis sa dernière mise à jour")
        non_script = [l.split("|")[1].strip() + " — " + l.split("|")[2].strip()[:60]
                      for l in cat.splitlines() if l.startswith("|") and re.search(r"\|\s*(non|partiel)[^|]*\|\s*$", l)]
        if non_script:
            C["reserve"].append(f"C5 catalogue : {len(non_script)} observation(s) de revue sans contrôle automatique complet (revue manuelle obligatoire) : "
                                + " ; ".join(non_script[:8]) + (" …" if len(non_script) > 8 else ""))
        if (ESF / "MODULE.md").stat().st_mtime + 60 < cat_mtime:
            C["reserve"].append("C5 catalogue modifié après le MODULE : vérifier que les nouvelles observations sont traduites en règles (§1-§2)")

    # C6 Listes d'opérations : éléments « nouveau » non encore intégrés, décisions « à trancher »
    for f in sorted(LISTES.glob("LISTE_OPERATIONS_*.md")):
        t = f.read_text(encoding="utf-8")
        nouveaux, atrancher = [], []
        for l in t.splitlines():
            if not l.startswith("|") or l.startswith("|---") or "Statut" in l:
                continue
            cells = [c.strip() for c in l.strip("|").split("|")]
            statut = cells[-1].lower()
            ident = cells[0]
            if statut.startswith("à trancher"):
                atrancher.append(f"{ident} {cells[1][:45]}")
            elif "nouveau" in statut:
                nouveaux.append(ident)
        if atrancher:
            C["reserve"].append(f"C6 {f.name} : {len(atrancher)} point(s) « à trancher » en attente de décision du gérant : " + " ; ".join(atrancher))
        if nouveaux:
            C["reserve"].append(f"C6 {f.name} : {len(nouveaux)} opération(s) « nouveau » pas encore intégrée(s) au module ecritures-sans-faute ni au script ({', '.join(nouveaux[:15])}{' …' if len(nouveaux) > 15 else ''})")
        if f.stat().st_mtime > (ESF / "MODULE.md").stat().st_mtime and nouveaux:
            C["reserve"].append(f"C6 {f.name} est plus récent que le MODULE : intégration à planifier")

    # C7 Copies .bak dans les références (risque de lire une version périmée)
    baks = sorted(MODULES.glob("*/reference/*.bak*"))
    if baks:
        C["reserve"].append(f"C7 hygiène : {len(baks)} copie(s) .bak dans les références (ex. {baks[0].name}) — à archiver hors du skill pour qu'aucune version périmée ne soit lue")

    # C8 Routage : le skill renvoie bien à l'auditeur et au garde-fou
    skill = (MDC / "SKILL.md").read_text(encoding="utf-8")
    manque = [m for m in ("ecritures-sans-faute", "auditeur-comptable") if f"`{m}`" not in skill]
    if manque:
        C["bloquant"].append("C8 routage : SKILL.md ne renvoie pas au(x) module(s) " + ", ".join(manque))
    else:
        C["ok"].append("C8 routage : SKILL.md renvoie à ecritures-sans-faute et à auditeur-comptable")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["ecritures", "mises-a-jour", "tout"])
    ap.add_argument("journal", nargs="?")
    ap.add_argument("--exercice", type=int)
    ap.add_argument("--forme")
    ap.add_argument("--regime")
    ap.add_argument("--feuille")
    ap.add_argument("--n1", help="balance ou bilan N-1 visé (xlsx/csv : compte + solde, ou débit/crédit)")
    ap.add_argument("--regularisations", action="store_true")
    ap.add_argument("--rapport", help="écrire aussi le rapport dans ce fichier .md")
    a = ap.parse_args()
    if a.mode != "mises-a-jour" and not (a.journal and a.exercice and a.forme):
        ap.error("modes ecritures et tout : JOURNAL, --exercice et --forme obligatoires")

    if a.journal and not Path(a.journal).expanduser().exists():
        ap.error(f"fichier introuvable : {a.journal!r}. Donner le chemin réel du journal, entre guillemets s'il contient des espaces, "
                 "par ex. \"$HOME/Documents/DOSSIER CLIENTS/KG CONSULTING/…/COMPTABILITE_KG_CONSULTING_2025.xlsx\" "
                 "(astuce : glisser le fichier depuis le Finder dans le Terminal)")
    plan = ce.charger_plan()
    R = Rapport()
    if a.mode in ("ecritures", "tout"):
        ecr = ce.lire(a.journal, a.feuille)
        axe_ecritures(R, ecr, a, plan)
        axe_principes(R, ecr, a)
    if a.mode in ("mises-a-jour", "tout"):
        axe_mises_a_jour(R, plan, a.journal)
    txt, bloque = R.texte()
    entete = ""
    if a.journal:
        entete = f"**Journal :** {Path(a.journal).name} — exercice {a.exercice} — {a.forme.upper()} — régime {(a.regime or 'non précisé').upper()}\n\n"
    txt = txt.replace("\n\n", "\n\n" + entete, 1) if entete else txt
    print(txt)
    if a.rapport:
        Path(a.rapport).write_text(txt + "\n", encoding="utf-8")
    sys.exit(1 if bloque else 0)


if __name__ == "__main__":
    main()
