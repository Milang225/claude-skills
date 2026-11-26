#!/usr/bin/env python3
"""Contrôle bloquant des écritures SYSCOHADA révisé avant toute remise (module ecritures-sans-faute)."""
import argparse
import csv
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

PLAN = Path(__file__).resolve().parents[2] / "mdc-expert" / "reference" / "PLAN_COMPTABLE_OHADA_COMPLET.md"
JOURNAUX_AN = {"AN", "RAN", "A-AN", "ANOUV", "OUV"}
SOCIETES = {"SARL", "SARLU", "SA", "SAS", "SASU", "SNC", "SCS", "GIE"}

# (regex sur le libellé, préfixes de comptes admis, message). Première règle trouvée = règle appliquée.
REGLES_CHARGES = [
    # Pénalités en premier : « pénalités sur l'impôt sur les salaires » est une pénalité (647x), pas une taxe (6413).
    (r"p[ée]nalit|amende|\bAMR\b|majoration", ("647", "6648", "6714", "6745", "691", "697", "659"),
     "pénalités fiscales → 647x (la dotation à une provision pour pénalités va en 691x)"),
    (r"taxe d.?apprentissage|\bTA\b", ("6414",), "taxe d'apprentissage → 6414"),
    (r"formation professionnelle|\bT?FPC\b", ("6415",), "formation professionnelle continue → 6415"),
    (r"\bFDFP\b", ("6414", "6415"), "FDFP → 6414 (TA) et 6415 (FPC)"),
    # « appoint\w* » : Sage abrège souvent en « TAXE SUR APPOINT.ET SALAIRE » (KRA 2025, faux positif corrigé le 17/11/2026)
    (r"contribution nationale|contribution employeur|\bCN\b|\bCE\b|taxes? sur (les )?(salaires|appoint\w*)|imp[oô]ts? sur (les )?salaires|ITS patronal",
     ("6413",), "taxes patronales sur salaires → 6413 (6313 = location de coffres)"),
    (r"\bCNPS\b|cotisations? sociales?|charges sociales|\bIPS\b", ("664", "647", "6648"), "charges sociales CNPS → 6641"),
    (r"\bTEE\b|entreprenant|imp[oô]t synth[ée]tique", ("6418", "647"), "TEE → 6418 (dette 446)"),
    (r"patente", ("6412", "647"), "patente → 6412 (dette 4421)"),
    (r"foncier", ("6411", "647"), "impôt foncier → 6411 (dette 4421)"),
    (r"agios?|int[ée]r[eê]ts? d[ée]biteurs", ("6745", "674"), "agios → 6745"),
    (r"int[ée]r[eê]ts? (d.?)?emprunt", ("6712", "671"), "intérêts d'emprunt → 6712"),
    (r"frais bancaires?|tenue de compte|frais de compte|commissions? bancaires?|frais (sur |de )?cartes?|frais sms|frais de virement",
     ("631",), "frais bancaires → 6318 (cartes 6315, mobile money 6317) ; 629 n'existe pas"),
    (r"[ée]lectricit|\bCIE\b", ("6052",), "électricité → 6052 (624 = entretien)"),
    # eau consommée (abonnement) ; l'eau achetée pour être revendue ou servie reste un achat 601/602
    (r"SODECI|(consommation|facture|abonnement|fourniture)s? d.eau|\beau (courante|potable)\b", ("6051",), "eau consommée → 6051 (624 = entretien)"),
    (r"(entretien|r[ée]paration|vidange|pneu|garage).{0,30}(v[ée]hicule|camion|voiture|moto|engin|mat[ée]riel|tracteur)"
     r"|(v[ée]hicule|camion|voiture|moto|engin).{0,30}(entretien|r[ée]paration|vidange)",
     ("6242",), "entretien et réparation de véhicules ou de matériel → 6242 biens mobiliers (6241 = biens immobiliers) — revue KRA"),
    (r"carburant|gas-?oil|gazole|\bessence\b|station-service|\bstation\b", ("6053",), "carburant → 6053"),
    (r"t[ée]l[ée]phon|internet|t[ée]l[ée]com|communication|\bORANGE\b|\bMTN\b|\bMOOV\b|forfait mobile",
     ("628",), "télécommunications → 6281 / 6288 (626 = études, documentation)"),
    (r"assurance", ("625",), "assurance → 625x"),
    (r"transport.{0,20}(achat|manutention)|fret|transit|d[ée]douan", ("6015", "6025", "6045", "6085", "612", "618", "613"), "transport et manutention sur achats → 6015 frais sur achats (627 = publicité ; il n'y a pas de 611)"),
    (r"transport", ("61", "6015", "6025", "6045", "6634"), "transports → 612 / 618x (627 = publicité)"),
    (r"\bloyers?\b|location (de |du )?(bureau|local|magasin|b[aâ]timent|entrep[oô]t)", ("622",), "loyer → 6222"),
    (r"honoraires?", ("632",), "honoraires → 6324 / 6327"),
    (r"fournitures? de bureau", ("6047", "6055"), "fournitures de bureau → 6055 (non stockées)"),
    (r"amortissement|dotation", ("681", "691", "852", "659", "697"), "dotations → 681x"),
    (r"logement", ("6631", "6222", "6617"), "indemnité de logement → 6631"),
    (r"salaires?|appointements?|r[ée]mun[ée]ration|paie\b|g[ée]rant",
     ("661", "662", "663", "666", "6618"), "salaires → 6611 (6631 = indemnités de logement)"),
]

REGLES_TIERS = [
    (("401", "408"), r"salaires?|paie\b|net [àa] payer|appointements", "salaires dus → 422, jamais 401 (revue KRA 3.6)"),
    (("422",), r"\bloyers?\b|bailleur", "loyer dû → 401 bailleur, jamais 422 (revue KWAANI 3.1)"),
    (("4486",), r"p[ée]nalit|amende|\bAMR\b", "pénalités fiscales dues → 4421, jamais 4486 (revue KWAANI 3.5)"),
    (("446",), r"patente|foncier|p[ée]nalit|\bAMR\b", "patente, foncier, pénalités → 4421, jamais 446 (revue KG)"),
    (("461",), r"compte courant|\bCCA\b|avance.{0,10}associ|apport en compte courant", "compte courant d'associé → 4621 (461x = opérations sur le capital)"),
    (("4616",), r"capital|souscri|apport|lib[ée]ration", "capital : 4612 Apporteurs, apports en numéraire (4616 = versements anticipés)"),
    (("4611",), r"num[ée]raire|esp[eè]ces|banque|virement|ch[eè]que|versement", "4611 = apports EN NATURE ; numéraire → 4612"),
    (("4428", "4421", "442", "446", "4486"), r"\bITS\b|FDFP|taxes? sur (les )?(salaires|appoint\w*)|apprentissage|formation professionnelle|contribution nationale",
     "ITS, CN, FDFP dus → 447202 (ITS retenu), 447201 (CN/CE), 4478 (TA + FPC) — pas 442x/446/4486 (revue KRA 3.7)"),
    (("196",), r"litige", "provision pour litiges → 191 (196 = retraites)"),
    (("7062",), r"commission|courtage", "7062 = services vendus HORS Région ; commissions → 7072 (ou 7061 si activité principale)"),
]

REGIMES_FORFAIT = {"TEE", "ENTREPRENANT", "FORFAIT", "TCE", "RME", "MICRO", "MICROENTREPRISE"}
REGIMES_REEL = {"RSI", "RNI", "REEL", "RÉEL"}

RACINES_A_VENTILER = {
    "447": "ITS retenu et CN → 4472 (447202 / 447201), FDFP TA + FPC → 4478 (revue KRA 3.7)",
    "442": "patente, foncier, TEE, AMR → 4421",
    "44": "préciser le compte d'impôt (4421, 4472, 4478, 441, 446)",
    "64": "préciser 6411 à 6418 selon l'impôt",
    "641": "préciser 6411 à 6418 selon l'impôt",
    "66": "préciser 6611 (salaires), 6641 (CNPS)…",
    "661": "salaires → 6611 (primes 6612, congés 6613)",
    "681": "dotation → 6812 (incorporelles) ou 6813 (corporelles)",
    "166": "intérêts courus → 1662 (emprunts bancaires)",
    "31": "stock → 311x par famille de marchandises",
}

ATTENTE_ERREUR = ("585", "588", "4719", "472")
ATTENTE_ALERTE = ("4711", "4712", "471")


def charger_plan():
    codes = set()
    for ligne in PLAN.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^[^\w|#*]*(\d{2,6})\s+[^\d\s]", ligne)
        if m:
            codes.add(m.group(1))
    return codes


def montant(v):
    if v is None:
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace(" ", "").replace("\xa0", "").replace(" ", "").replace("FCFA", "")
    if not s or s in {"-", "—"}:
        return 0.0
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    return float(s)


def date_de(v):
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    s = str(v).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y", "%Y-%m-%d %H:%M:%S", "%d.%m.%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"date illisible : {s!r}")


ALIAS = {
    "journal": ("journal", "jnl", "jrn", "jal", "code journal", "c.jnl"),
    "date": ("date",),
    "piece": ("piece", "pièce", "n° pièce", "n° piece", "no piece", "ref", "réf", "réf.", "ref.", "référence"),
    "compte": ("compte", "n° compte", "no compte", "compte général"),
    "tiers": ("tiers", "compte tiers"),
    "libelle": ("libellé de l'écriture", "libelle de l'ecriture", "libellé écriture", "libelle", "libellé", "intitulé"),
    "debit": ("debit", "débit"),
    "credit": ("credit", "crédit"),
}


def normaliser_entete(cols):
    # Priorité à l'ordre des alias, pas à l'ordre des colonnes : « Libellé de l'écriture » l'emporte
    # sur « Intitulé » (intitulé du compte), qui ne sert qu'en dernier recours.
    res = {}
    entetes = [str(c or "").strip().lower().replace("’", "'") for c in cols]
    for cle, noms in ALIAS.items():
        for nom in noms:
            if nom in entetes:
                res[cle] = entetes.index(nom)
                break
    manque = [c for c in ("journal", "date", "piece", "compte", "libelle", "debit", "credit") if c not in res]
    if manque:
        sys.exit(f"Colonnes manquantes : {', '.join(manque)} (trouvées : {cols})")
    return res


def lire(chemin, feuille=None):
    p = Path(chemin)
    if p.suffix.lower() in {".xlsx", ".xlsm"}:
        import openpyxl
        wb = openpyxl.load_workbook(p, data_only=True)
        if feuille:
            ws = wb[feuille]
        else:  # première feuille dont une ligne d'en-tête porte « compte » et « débit »
            def entete(w):
                for r in w.iter_rows(max_row=15, values_only=True):
                    k = {str(c or "").strip().lower() for c in r}
                    if "compte" in k and ({"débit", "debit"} & k):
                        return True
                return False
            ws = next((w for w in wb.worksheets if entete(w)), wb.active)
        lignes = [list(r) for r in ws.iter_rows(values_only=True)]
    else:
        txt = p.read_text(encoding="utf-8-sig")
        sep = ";" if txt.count(";") > txt.count(",") else ","
        lignes = list(csv.reader(txt.splitlines(), delimiter=sep))
    debut = next(i for i, r in enumerate(lignes) if any(str(c or "").strip().lower() in ALIAS["compte"] for c in r))
    idx = normaliser_entete(lignes[debut])
    ecritures = []
    prec = {"journal": "", "date": None, "piece": ""}
    for n, r in enumerate(lignes[debut + 1:], start=debut + 2):
        if not any(str(c or "").strip() for c in r):
            continue
        g = lambda k: r[idx[k]] if k in idx and idx[k] < len(r) else None
        brut = str(g("compte") or "").strip()
        if brut.endswith(".0"):
            brut = brut[:-2]
        compte = re.sub(r"\D", "", brut)
        if not compte:
            continue
        vide = lambda v: v is None or str(v).strip() in {"", "—", "-"}
        jr = prec["journal"] if vide(g("journal")) else str(g("journal")).strip().upper()
        dt = prec["date"] if vide(g("date")) else date_de(g("date"))
        pc = prec["piece"] if vide(g("piece")) else str(g("piece")).strip()
        if dt is None:
            sys.exit(f"ligne {n} : date absente et aucune ligne précédente dont la reprendre")
        prec = {"journal": jr, "date": dt, "piece": pc}
        ecritures.append({
            "ligne": n, "journal": jr, "date": dt,
            "piece": pc, "compte": compte, "brut": brut, "tiers": str(g("tiers") or "").strip(),
            "libelle": str(g("libelle") or "").strip(), "debit": montant(g("debit")), "credit": montant(g("credit")),
        })
    return ecritures


def verifier_compte(c, plan):
    if len(c) < 3:
        return f"« {c} » est une classe ou un chapitre, pas un compte : choisir le compte exact"
    if c[:3] not in plan and c.rstrip("0") in plan and len(c.rstrip("0")) == 2:
        return f"compte {c} = chapitre {c.rstrip('0')} complété par des zéros : choisir le compte exact à 3 chiffres au moins"
    if c[:3] not in plan:
        return f"compte {c} inexistant : la racine {c[:3]} n'existe pas dans le plan AUDCIF"
    if len(c) >= 4 and c[3] != "0" and c[:4] not in plan:
        return f"compte {c} inexistant : le sous-compte {c[:4]} n'existe pas dans le plan AUDCIF"
    return None


def fmt(x):
    return f"{x:,.0f}".replace(",", " ")


def controler(ecr, exercice, forme, plan, regime=None, regul=False):
    err, ale = [], []
    E = lambda e, m: err.append(f"L{e['ligne']} [{e['journal']} {e['piece']} {e['compte']}] {m}" if e else m)
    A = lambda e, m: ale.append(f"L{e['ligne']} [{e['journal']} {e['piece']} {e['compte']}] {m}" if e else m)
    debut, fin = date(exercice, 1, 1), date(exercice, 12, 31)
    societe = forme.upper() in SOCIETES

    regime = (regime or "").upper()
    if not regime and any(e["compte"].startswith("89") for e in ecr):
        A(None, "comptes 89 utilisés : préciser --regime ; la classe 89 (impôt sur les bénéfices, IMF) est réservée au régime du réel")
    for e in ecr:
        c, lib = e["compte"], e["libelle"]
        if regime in REGIMES_FORFAIT and c.startswith("89"):
            E(e, f"compte {c} interdit au régime {regime} : la classe 89 « impôts sur le résultat » est réservée au réel (RSI, RNI) ; au forfait (TEE, microentreprises), l'impôt va en 6418 / dette 446 (revue KG)")
        if re.search(r"[^\d\s]", e.get("brut", c)):
            E(e, f"« {e['brut']} » n'est pas un numéro de compte (un compte par ligne : 6414 TA et 6415 FPC séparés — revue KRA 3.6)")
        elif m := verifier_compte(c, plan):
            E(e, m)
        if c.rstrip("0") in RACINES_A_VENTILER:
            E(e, f"compte racine {c.rstrip('0')} non ventilé : {RACINES_A_VENTILER[c.rstrip('0')]}")
        if e["debit"] and e["credit"]:
            E(e, "ligne portant à la fois un débit et un crédit")
        if e["debit"] < 0 or e["credit"] < 0:
            E(e, "montant négatif : inverser le sens plutôt que saisir un signe moins")
        if not (debut <= e["date"] <= fin):
            E(e, f"date {e['date']:%d/%m/%Y} hors exercice {exercice} (règle R6)")
        an = e["journal"] in JOURNAUX_AN
        if an:
            if c[0] in "6789":
                E(e, "classe 6, 7 ou 8 dans les à-nouveaux : interdit (revue KG, compte 89)")
            if e["date"] != debut:
                E(e, "à-nouveau daté autrement qu'au 01/01 (opération courante saisie en AN ?)")
        if c[0] in "67" and not an:
            for rx, ok, msg in (REGLES_CHARGES if c[0] == "6" else []):
                if re.search(rx, lib, re.I):
                    if not c.startswith(ok):
                        E(e, f"« {lib} » : {msg}")
                    break
            if c.startswith(("701", "702", "703", "704")) and re.search(r"prestation|services?\b|conseil|transport|mission|honoraires", lib, re.I):
                E(e, f"services vendus → 706, pas {c[:3]} (revue TIM 7 n° 4 : 702 = produits finis, 701 = marchandises)")
            if c.startswith("6631") and not re.search(r"logement", lib, re.I):
                E(e, "6631 = indemnités de logement ; salaire du gérant ou du personnel → 6611")
        # Écriture corrective (--regularisations) : la ligne au DÉBIT qui vide un compte mal imputé
        # (« Annulation… », « Sortie… ») corrige la faute ; elle n'en est pas une (revue KWAANI 3.5, KRA 3.7).
        sortie = regul and e["debit"] > 0 and re.match(r"\s*(annulation|sortie)\b", lib, re.I)
        for prefixes, rx, msg in REGLES_TIERS:
            if msg and not sortie and c.startswith(prefixes) and re.search(rx, lib, re.I):
                E(e, msg)
        if c.startswith(("401", "411", "408", "409", "419")) and not an:
            aux = c.rstrip("0")
            if re.match(r"^\s*(clt|client|clients|fournisseurs?|frs|divers|tiers)\b\.?\s*(divers)?\s*$", lib, re.I):
                E(e, f"tiers anonyme « {lib} » : nommer le client ou le fournisseur (revue KG « CLT », TIM 7 FNP)")
            elif re.search(r"\b(NI|NON[-_ ]?IDENT\w*|A[-_ ]?IDENT\w*|DIVERS|GENERIQUE|INCONNU)\b|^(CLT|FRS)[-_]", e["tiers"] or "", re.I) \
                    or re.search(r"(à|a) identifier|non identifi", lib, re.I):
                # Code tiers générique (CLT-2024, FRS-MARCH-NI, FRS-CHARGES…) ou libellé « à identifier » : la faute KG « CLT »
                # sous une autre forme (revue de l'auditeur indépendant, KRA 17/11/2026)
                A(e, f"tiers non nommé (« {e['tiers'] or lib} ») : nommer le fournisseur ou le client d'après la pièce (R2)")
            elif len(aux) <= 4 and not e["tiers"]:
                A(e, "compte collectif sans compte tiers individuel : ouvrir un 4011xxx / 4111xxx par tiers (R2)")
        if societe and c.startswith(("103", "104")):
            E(e, f"compte {c[:3]} réservé à l'entreprise individuelle (personne physique) ; société ({forme}) : capital 1011 → 1012 → 1013, apports et avances 4621")
        if not societe and c.startswith(("101", "1301", "1309", "462", "465", "111")):
            E(e, f"compte {c[:4]} réservé aux sociétés (personne morale) : entreprise individuelle → 103 capital personnel, 1041-1048 compte de l'exploitant, 131/139 (revue KG)")
        if not societe and c.startswith("103") and not an and re.search(r"temporaire|pr[ée]l[eè]v|retrait|d[ée]pense (priv|perso)", lib, re.I):
            E(e, "apport temporaire ou prélèvement : compte 104 (1041 apports temporaires, 1042-1048 prélèvements), viré au 103 à la clôture — le 103 ne reçoit que les apports définitifs (AUDCIF p. 283)")
        if not societe and an and c.startswith("104"):
            E(e, "compte 104 dans les à-nouveaux : il aurait dû être soldé dans le 103 à la clôture précédente (AUDCIF p. 286)")

    pieces = defaultdict(list)
    for e in ecr:
        pieces[(e["journal"], e["piece"], e["date"])].append(e)
    total_d = sum(e["debit"] for e in ecr)
    total_c = sum(e["credit"] for e in ecr)
    if abs(total_d - total_c) > 0.5:
        E(None, f"JOURNAL DÉSÉQUILIBRÉ : débit {fmt(total_d)} ≠ crédit {fmt(total_c)}")
    for (j, p, d), ls in pieces.items():
        sd, sc = sum(x["debit"] for x in ls), sum(x["credit"] for x in ls)
        if abs(sd - sc) > 0.5:
            E(ls[0], f"pièce déséquilibrée : D {fmt(sd)} / C {fmt(sc)}")
        if j in JOURNAUX_AN:
            continue
        comptes = [x["compte"] for x in ls]
        charge_tres = any(c[0] == "6" for c in comptes) and any(c.startswith(("52", "57")) for c in comptes)
        banque_office = all(c.startswith(("631", "674", "671", "162", "52")) for c in comptes)
        if charge_tres and not banque_office and not any(c[0] == "4" for c in comptes):
            E(ls[0], "charge réglée directement en trésorerie : constater d'abord sur un compte de tiers (R4, deux temps)")
        if any(c.startswith("101") and x["credit"] for c, x in zip(comptes, ls)) and any(c.startswith(("52", "57")) for c in comptes):
            E(ls[0], "capital crédité directement contre la trésorerie : souscription 4612/1011 puis libération (schéma 3.1)")
        paie_seule = all(c.startswith(("66", "641", "4", "52", "57")) for c in comptes)
        if not regul and not paie_seule and sum(1 for c in comptes if c[0] in "67") >= 4 and d == fin:
            A(ls[0], f"pièce du 31/12 regroupant {sum(1 for c in comptes if c[0] in '67')} lignes de charges/produits : écriture globale ? (R1)")

    gestion = [e for e in ecr if e["compte"][0] in "67" and e["journal"] not in JOURNAUX_AN
               and not e["compte"].startswith(("68", "69", "79", "78", "659", "759"))]
    vol = sum(e["debit"] + e["credit"] for e in gestion)
    vol_fin = sum(e["debit"] + e["credit"] for e in gestion if e["date"] == fin)
    mois = {e["date"].month for e in gestion}
    if regul:
        pass
    elif vol and vol_fin / vol > 0.6:
        E(None, f"ÉCRITURES GLOBALES : {vol_fin / vol:.0%} des charges et produits datés du 31/12 — passer chaque opération à sa date (R1, revues KG et TIM 7)")
    elif vol and vol_fin / vol > 0.25:
        A(None, f"{vol_fin / vol:.0%} des charges et produits datés du 31/12 : vérifier qu'il ne s'agit que de régularisations")
    if len(gestion) > 12 and len(mois) < 4:
        A(None, f"opérations de gestion sur {len(mois)} mois seulement : activité réellement saisonnière ?")

    def soldes(prefixe_ok):
        s = defaultdict(float)
        for e in ecr:
            if prefixe_ok(e["compte"]):
                s[e["compte"]] += e["debit"] - e["credit"]
        return s

    caisse = defaultdict(float)
    for e in ecr:
        if e["compte"].startswith("57"):
            caisse[e["date"]] += e["debit"] - e["credit"]
    cumul, pire = 0.0, None
    for d in sorted(caisse):
        cumul += caisse[d]
        if cumul < -0.5 and (pire is None or cumul < pire[1]):
            pire = (d, cumul)
    if pire:
        E(None, f"CAISSE CRÉDITRICE : solde le plus bas {fmt(pire[1])} au {pire[0]:%d/%m/%Y} — impossible ; chronologie ou recette manquante (R8, revue TIM 7 n° 27)")

    # Report à nouveau mouvementé hors à-nouveaux : seulement sur PV d'AGO (affectation) ou correction d'erreur significative (note 2)
    for e in ecr:
        if e["compte"].startswith(("121", "129")) and e["journal"] not in JOURNAUX_AN and not re.search(r"\bAGO\b|affectation|proc[eè]s-verbal|\bPV\b", e["libelle"], re.I):
            A(e, "report à nouveau mouvementé sans PV d'AGO : affectation du résultat sur PV, ou correction d'erreur SIGNIFICATIVE mentionnée en note 2 ; "
                 "un rappel non significatif est une charge de l'exercice (principe B1, revue KRA 17/11/2026)")

    # Monnaie électronique (55) : solde débiteur ou nul uniquement (AUDCIF p. 426-427) — R16
    mob = defaultdict(float)
    for e in ecr:
        if e["compte"].startswith("55"):
            mob[e["date"]] += e["debit"] - e["credit"]
    cumul, pire = 0.0, None
    for d in sorted(mob):
        cumul += mob[d]
        if cumul < -0.5 and (pire is None or cumul < pire[1]):
            pire = (d, cumul)
    if pire:
        E(None, f"MONNAIE ÉLECTRONIQUE CRÉDITRICE (55) : solde le plus bas {fmt(pire[1])} au {pire[0]:%d/%m/%Y} — chargement manquant : "
                "D 552 / C 57x ou 52x à la date du chargement, selon le relevé mobile money (R16)")

    # Microfinance passée en banque : 538 Autres organismes financiers, un sous-compte par établissement — R17
    sfd = re.compile(r"\b(BAOBAB|GESCI|GES-CI|COFINA|ADVANS|UNACOOPEC|COOPEC|FIDRA|CELPAID|MICROCRED|microfinance)\b", re.I)
    for e in ecr:
        if e["compte"].startswith("52") and sfd.search(e["libelle"]):
            A(e, "établissement de microfinance sur un compte de banque 52x : 538 Autres organismes financiers, un sous-compte par établissement (R17)")
            break

    # Charges au montant identique chaque mois : forfait sans pièce ? (revue KRA §4) — R15
    rep = defaultdict(set)
    for e in ecr:
        c = e["compte"]
        if c[0] == "6" and e["debit"] and e["journal"] not in JOURNAUX_AN and not c.startswith(("66", "64", "622", "68", "69", "603")):
            rep[(c, round(e["debit"]))].add(e["date"].month)
    for (c, m), mois_ in sorted(rep.items()):
        if len(mois_) >= 10:
            A(None, f"{c} : {fmt(m)} identiques sur {len(mois_)} mois — charge forfaitaire sans pièce ? Factures du mois à produire ; ne jamais « varier » un montant sans pièce (R15)")

    # Marge identique chaque mois : ventes calculées à partir des achats (revue KRA 2025) — R18
    vm, am = defaultdict(float), defaultdict(float)
    for e in ecr:
        if e["journal"] in JOURNAUX_AN:
            continue
        if e["compte"].startswith("701"):
            vm[e["date"].month] += e["credit"] - e["debit"]
        if e["compte"].startswith("601"):
            am[e["date"].month] += e["debit"] - e["credit"]
    taux = [vm[m] / am[m] for m in vm if am.get(m, 0) > 0 and vm[m] > 0]
    if len(taux) >= 6 and max(taux) - min(taux) < 0.0005:
        A(None, f"ventes / achats = {taux[0]:.6f} chaque mois ({len(taux)} mois) : ventes mensuelles calculées, pas relevées — cahier de ventes ou de caisse à produire (R18)")

    for c, s in soldes(lambda c: c.startswith(ATTENTE_ERREUR + ATTENTE_ALERTE)).items():
        if abs(s) > 0.5:
            (E if c.startswith(ATTENTE_ERREUR) else A)(None, f"compte d'attente {c} non soldé au 31/12 : {fmt(s)} — analyser et apurer (R10)")
    for c, s in soldes(lambda c: c.startswith(("1011", "1012", "109", "4612", "4613"))).items():
        if abs(s) > 0.5:
            A(None, f"capital : {c} non soldé ({fmt(s)}) — souscription, appel ou libération incomplet (schéma 3.1)")
    fnp = [e for e in ecr if e["compte"].startswith("408") and e["journal"] not in JOURNAUX_AN]
    if any(e["credit"] for e in fnp) and any(e["debit"] for e in fnp):
        E(None, "compte 408 crédité ET soldé dans le même exercice : une facture non parvenue se constate à la clôture et s'extourne en N+1 (revue TIM 7 n° 13)")
    for c, s in soldes(lambda c: c.startswith(("4011", "401", "4111", "411", "422", "4472", "4478", "4421", "446", "431"))).items():
        sens_normal = -1 if c.startswith(("401", "422", "44", "431")) else 1
        if s * sens_normal < -0.5:
            A(None, f"{c} présente un solde de sens anormal ({fmt(s)}) : paiement sans constatation, ou doublon ?")
    s13 = defaultdict(float)
    for e in ecr:
        if e["compte"].startswith(("12", "13", "89")) and not e["compte"].startswith(("1301", "1309")):
            s13[e["compte"][:3]] += e["debit"] - e["credit"]
    an13 = {e["compte"][:3] for e in ecr if e["journal"] in JOURNAUX_AN and e["compte"].startswith(("131", "139"))}
    for c in sorted(an13):
        if abs(s13.get(c, 0)) > 0.5:
            E(None, f"résultat N-1 repris en {c} et jamais affecté ({fmt(s13[c])}) : "
                    + ("EI → D 131 / C 103 ou D 103 / C 139 au 01/01" if not societe else "société → 1301 / 1309 puis affectation par PV d'AGO")
                    + " (revue KG)")
    if not societe and any(e["compte"].startswith(("121", "129")) for e in ecr):
        E(None, "report à nouveau (121/129) dans une entreprise individuelle : le résultat va directement au 103")
    for e in ecr:
        annees = [int(x) for x in re.findall(r"\b(20[0-9]{2})\b", e["libelle"])]
        if e["compte"].startswith("891") and (re.search(r"ant[ée]rieur|rappel", e["libelle"], re.I) or (annees and min(annees) < e["date"].year)):
            E(e, "impôt sur le résultat d'un exercice antérieur en 891 : 892 (rappel ou erreur non significative) ou report à nouveau 129 avec mention en note 2 (erreur significative, AUDCIF art. 20)")
    if not societe:
        s104 = sum(e["debit"] - e["credit"] for e in ecr if e["compte"].startswith("104"))
        if abs(s104) > 0.5:
            E(None, f"compte de l'exploitant 104 non soldé au 31/12 ({fmt(s104)}) : virer le solde net au 103 — "
                    f"{'D 103 / C 104 (retraits nets)' if s104 > 0 else 'D 104 / C 103 (apports nets)'} (AUDCIF p. 284-286)")
        sous = defaultdict(float)
        for e in ecr:
            if e["compte"].startswith("104"):
                sous[e["compte"]] += e["debit"] - e["credit"]
        for c, v in sorted(sous.items()):
            if abs(v) > 0.5 and abs(s104) <= 0.5:
                E(None, f"sous-compte {c} non soldé ({fmt(v)}) : à la clôture, solder CHAQUE sous-compte du 104 contre le 103")
    controler_stocks(ecr, pieces, E, A)
    if not regul:
        controler_paie(ecr, E, A)
    return err, ale


def controler_stocks(ecr, pieces, E, A):
    hors_an = [e for e in ecr if e["journal"] not in JOURNAUX_AN]
    for (j, p, d), ls in pieces.items():
        if j in JOURNAUX_AN or not any(x["compte"].startswith(("31", "32", "33", "34", "35", "36", "37", "38")) for x in ls):
            continue
        autres = {x["compte"][:3] for x in ls if not x["compte"].startswith("3")}
        if not autres <= {"603", "659", "759", "791", "391", "781", "854", "864", "658", "758"}:
            E(ls[0], f"stock mouvementé contre {', '.join(sorted(autres))} : un stock ne varie qu'à l'inventaire (D 311 / C 6031, D 6031 / C 311) ; "
                     "jamais contre la banque, la caisse ou un tiers (revue KRA 2.1 : « affectation du financement en stock »)")
    si = sum(e["debit"] - e["credit"] for e in ecr if e["journal"] in JOURNAUX_AN and e["compte"].startswith("31"))
    var = [e for e in hors_an if e["compte"].startswith("6031")]
    sf = sum(e["debit"] for e in hors_an if e["compte"].startswith("31") and any(x["compte"].startswith("6031") for x in var if x["piece"] == e["piece"]))
    achats = sum(e["debit"] - e["credit"] for e in hors_an if e["compte"].startswith("601"))
    # Solde du 31 au bilan (inclut un stock passé hors 6031, déjà signalé en erreur) — faux « final 0 » corrigé le 17/11/2026
    sf_bilan = sum(e["debit"] - e["credit"] for e in ecr if e["compte"].startswith("31"))
    if si and not var:
        E(None, f"stock initial {fmt(si)} jamais soldé par 6031 : passer D 6031 / C 311 à la clôture puis le stock final selon inventaire")
    if (si or sf_bilan) and not achats:
        A(None, f"stock (initial {fmt(si)}, au bilan {fmt(sf_bilan)}) mais aucun achat de marchandises en 601 : achats manquants, ou marchandises qui ne vous appartiennent pas (dépôt-vente, mandat) ?")
    if si and var and not sf and abs(sf_bilan) < 0.5:
        A(None, "stock final nul après un stock initial : joindre le PV d'inventaire au 31/12 signé et valorisé (quantités × coût d'achat), sinon le réviseur rejette (revue KRA 2.1)")
    if sf:
        A(None, f"stock final {fmt(sf)} : PV d'inventaire valorisé, fiche par article et factures d'achat justifiant le coût unitaire obligatoires")
    if any(e["compte"].startswith(("4731", "4733")) for e in ecr) and (si or sf):
        A(None, "activité pour compte de mandants ET stock en 31 : les marchandises des mandants ne sont pas votre stock ; contrat de mandat requis (revue KRA 2.2)")


MOIS = "janvier février mars avril mai juin juillet août septembre octobre novembre décembre".split()


def controler_paie(ecr, E, A):
    par_mois = defaultdict(lambda: defaultdict(float))
    for e in ecr:
        if e["journal"] in JOURNAUX_AN:
            continue
        m = e["date"].month
        c = e["compte"]
        for cle, pref in (("brut", ("661", "662", "6661")), ("cn", ("6413",)), ("ta", ("6414",)), ("fpc", ("6415",)), ("cnps", ("6641", "6642"))):
            if c.startswith(pref):
                par_mois[m][cle] += e["debit"] - e["credit"]
        if c.startswith("422"):
            par_mois[m]["422"] += e["credit"]
    for m, v in sorted(par_mois.items()):
        b = v["brut"]
        if b <= 0:
            if v["cn"] or v["ta"] or v["fpc"]:
                A(None, f"{MOIS[m-1]} : taxes sur salaires sans salaire brut le même mois")
            continue
        nom = MOIS[m - 1]
        if not v["422"]:
            E(None, f"{nom} : salaire brut {fmt(b)} sans compte 422 crédité — constater D 6611 / C 4472 + 422, puis payer D 422 / C 52x-57x (revue KRA 3.6)")
        manquants = [n for n, k in (("CN 6413", "cn"), ("TA 6414", "ta"), ("FPC 6415", "fpc")) if not v[k]]
        if manquants:
            E(None, f"{nom} : salaire {fmt(b)} sans {', '.join(manquants)} — reprendre chaque ligne de la déclaration ITS du mois (revue KRA 3.6, KWAANI 3.2)")
        if v["cn"] and v["cn"] / b > 0.015 and not (v["ta"] and v["fpc"]):
            E(None, f"{nom} : 6413 = {v['cn'] / b:.1%} du brut — taux global passé en 6413 ; ventiler CN 1,2 % (6413), TA 0,4 % (6414), FPC (6415). "
                    "La CE ne s'applique pas au personnel local (revue KRA 3.6)")
        tot = (v["cn"] + v["ta"] + v["fpc"]) / b
        if v["cn"] and v["ta"] and v["fpc"] and not (0.021 <= tot <= 0.029 or tot >= 0.10):
            A(None, f"{nom} : taxes sur salaires = {tot:.2%} du brut (attendu 2,2 % à 2,8 % pour du personnel local) : comparer à la déclaration du mois")
    charges = sum(v["cn"] + v["ta"] + v["fpc"] for v in par_mois.values())
    if charges:
        # Paiements aussi reconnus sur un mauvais compte de dette (4428, 442, 446…) : le compte est déjà signalé en erreur,
        # mais le paiement existe (faux « sans aucun paiement » corrigé le 17/11/2026, KRA 2025)
        mauvais = re.compile(r"\bITS\b|FDFP|taxes? sur|apprentissage|formation professionnelle|contribution nationale", re.I)
        payes = [e for e in ecr if e["journal"] not in JOURNAUX_AN and e["debit"] and (
            e["compte"].startswith(("4472", "4478", "447"))
            or (e["compte"].startswith(("4428", "442", "446", "4486")) and mauvais.search(e["libelle"] or ""))
            or (e["compte"].startswith("4428") and e["journal"].upper().startswith(("CA", "BQ")))
        )]
        if not payes:
            # Réellement impayées (« déclaré non payé » sur e-impôts) : la dette reste au bilan, ce n'est pas une faute d'écriture.
            A(None, f"taxes sur salaires {fmt(charges)} comptabilisées sans aucun paiement : vérifier l'historique e-impôts — "
                    "si des quittances existent, passer chaque paiement à sa date (revue KRA 3.7) ; sinon dette maintenue au bilan et pénalités à provisionner")
        else:
            mois_payes = sorted({e["date"].month for e in payes})
            if len(mois_payes) < 3 and len(par_mois) >= 6:
                A(None, f"paiements ITS/FDFP sur {len(mois_payes)} date(s) seulement pour {len(par_mois)} mois déclarés : un paiement par déclaration, à sa date et avec sa référence (revue KRA 3.7)")
        cnps = sum(v["cnps"] for v in par_mois.values())
        if not cnps:
            A(None, "salaires sans aucune charge CNPS (6641) : immatriculation et cotisations à régulariser — motif de rejet du visa dans les quatre notes de revue")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("fichier")
    ap.add_argument("--exercice", type=int, required=True)
    ap.add_argument("--forme", required=True, help="SARL, SA, SAS, SNC… ou EI")
    ap.add_argument("--regime", help="TEE ou RME (forfait), RSI ou RNI (réel)")
    ap.add_argument("--feuille", help="nom de la feuille Excel du journal (par défaut : détectée)")
    ap.add_argument("--regularisations", action="store_true",
                    help="fichier d'écritures correctives seules (réponse à une note de revue) : pas de contrôle d'écritures globales ni de paie mensuelle")
    a = ap.parse_args()
    plan = charger_plan()
    ecr = lire(a.fichier, a.feuille)
    err, ale = controler(ecr, a.exercice, a.forme, plan, a.regime, a.regularisations)
    print(f"Contrôle de {len(ecr)} lignes — exercice {a.exercice} — forme {a.forme.upper()} — régime {(a.regime or 'non précisé').upper()}")
    print(f"\nERREURS BLOQUANTES : {len(err)}")
    for m in err:
        print("  ✗", m)
    print(f"\nALERTES À JUSTIFIER : {len(ale)}")
    for m in ale:
        print("  !", m)
    print("\nVERDICT :", "NE PAS REMETTRE — corriger les erreurs" if err else "contrôle automatique passé ; remplir la grille de rapprochements §4")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
