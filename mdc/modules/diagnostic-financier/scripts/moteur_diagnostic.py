# -*- coding: utf-8 -*-
"""
MOTEUR DE DIAGNOSTIC FINANCIER — MDC (La Maison de la Conformité SARL)

Coeur de calcul partagé par le générateur de classeur et l'export web.
Entrée  : postes de balance SYSCOHADA agrégés, par exercice.
Sortie  : soldes intermédiaires, bilan financier, ratios des 5 étapes,
          score Z'' d'Altman, indice de santé financière MDC, VEA.

Aucune dépendance externe. Les montants sont en FCFA.
"""

from collections import OrderedDict

# ---------------------------------------------------------------------------
# 1. LES POSTES DE SAISIE (balance SYSCOHADA agrégée)
#    (cle, libelle, comptes, section)
# ---------------------------------------------------------------------------
POSTES = [
    # --- compte de résultat
    ("v_march",    "Ventes de marchandises",                                   "701",                        "CR"),
    ("a_march",    "Achats de marchandises",                                   "601",                        "CR"),
    ("var_march",  "Variation de stocks de marchandises",                      "6031  (+) si baisse du stock", "CR"),
    ("v_prod",     "Ventes de produits, travaux et services",                  "702 à 706",                  "CR"),
    ("prod_imm",   "Production immobilisée et variation stocks produits",      "72 / 73",                    "CR"),
    ("a_mat",      "Achats de matières, fournitures et énergie",               "602 / 604 / 605 / 608",      "CR"),
    ("transp",     "Transports",                                               "61",                         "CR"),
    ("serv",       "Services extérieurs",                                      "62 / 63",                    "CR"),
    ("subv",       "Subventions d'exploitation",                               "71",                         "CR"),
    ("imp_tax",    "Impôts et taxes",                                          "64",                         "CR"),
    ("autres_ch",  "Autres charges",                                           "65",                         "CR"),
    ("pers",       "Charges de personnel",                                     "66",                         "CR"),
    ("autres_pr",  "Autres produits",                                          "75",                         "CR"),
    ("dot",        "Dotations aux amortissements et provisions d'exploitation", "68",                        "CR"),
    ("repr",       "Reprises de provisions et transferts de charges",          "78 / 79",                    "CR"),
    ("rev_fin",    "Revenus financiers",                                       "77",                         "CR"),
    ("fr_fin",     "Frais financiers",                                         "67",                         "CR"),
    ("hao",        "Résultat HAO net",                                         "82 à 84",                    "CR"),
    ("partic",     "Participation des travailleurs",                           "87",                         "CR"),
    ("impot",      "Impôts sur le résultat (IS ou IMF)",                       "89",                         "CR"),
    # --- bilan actif
    ("im_inc",     "Immobilisations incorporelles brutes",                     "21",                         "ACTIF"),
    ("im_cor",     "Immobilisations corporelles brutes",                       "22 à 24",                    "ACTIF"),
    ("im_fin",     "Immobilisations financières",                              "26 / 27",                    "ACTIF"),
    ("amort",      "Amortissements et dépréciations des immobilisations",      "28 / 29",                    "ACTIF"),
    ("stock_b",    "Stocks bruts",                                             "31 à 38",                    "ACTIF"),
    ("stock_d",    "Dépréciations des stocks",                                 "39",                         "ACTIF"),
    ("cli_b",      "Créances clients brutes",                                  "411 / 412 / 416 / 418",      "ACTIF"),
    ("cli_d",      "Dépréciations des créances clients",                       "491",                        "ACTIF"),
    ("aut_cr",     "Autres créances d'exploitation (État, personnel, divers)", "44 déb. / 42 déb. / 47 déb.", "ACTIF"),
    ("cr_hao",     "Créances HAO",                                             "485 / 488",                  "ACTIF"),
    ("titres",     "Titres de placement",                                      "50",                         "ACTIF"),
    ("banque",     "Banques, chèques postaux, caisse",                         "52 / 53 / 57",               "ACTIF"),
    # --- bilan passif
    ("capital",    "Capital social",                                           "101 / 103",                  "PASSIF"),
    ("reserv",     "Primes, écarts et réserves",                               "104 à 11",                   "PASSIF"),
    ("ran",        "Report à nouveau (+/-)",                                   "12",                         "PASSIF"),
    ("res_bil",    "Résultat net de l'exercice (au bilan)",                    "13",                         "PASSIF"),
    ("subv_inv",   "Subventions d'investissement",                             "14",                         "PASSIF"),
    ("prov_regl",  "Provisions réglementées",                                  "15",                         "PASSIF"),
    ("emprunt",    "Emprunts et dettes financières",                           "16",                         "PASSIF"),
    ("cbail",      "Dettes de location-acquisition (crédit-bail)",             "17",                         "PASSIF"),
    ("prov_risq",  "Provisions pour risques et charges",                       "19",                         "PASSIF"),
    ("cca",        "Comptes courants d'associés",                              "462",                        "PASSIF"),
    ("fourn",      "Fournisseurs d'exploitation",                              "401 / 408",                  "PASSIF"),
    ("d_fisc",     "Dettes fiscales",                                          "44",                         "PASSIF"),
    ("d_soc",      "Dettes sociales",                                          "42 / 43",                    "PASSIF"),
    ("aut_det",    "Autres dettes d'exploitation",                             "47 créd.",                   "PASSIF"),
    ("det_hao",    "Dettes HAO",                                               "481 / 482",                  "PASSIF"),
    ("decouv",     "Banques, crédits de trésorerie et découverts",             "56",                         "PASSIF"),
]
CLES = [p[0] for p in POSTES]

PARAMS_DEFAUT = {
    "taux_is": 0.25,      # IS de droit commun, Côte d'Ivoire
    "jours": 360,         # base de jours des ratios de rotation
    "cout_fp": 0.18,      # coût des fonds propres exigé (jugement)
    "cout_dette": 0.11,   # coût de la dette avant impôt
    "seuil_dn_ebe": 3.0,
    "seuil_couverture": 3.0,
    "seuil_autonomie": 0.30,
    "seuil_delai_client": 60,
    "seuil_dfs_jours": 20,
}

# ---------------------------------------------------------------------------
# 2. BARÈME DE LA INDICE DE SANTÉ FINANCIÈRE MDC
#    (cle_ratio, libelle, poids, seuil_bon, seuil_moyen, sens, format)
#    sens = "sup" : plus c'est haut, mieux c'est.  "inf" : l'inverse.
# ---------------------------------------------------------------------------
BAREME = [
    ("t_ebe",     "Rentabilité d'exploitation (EBE / CA)",             0.20, 0.08, 0.04, "sup", "pct"),
    ("cfi",       "Couverture des frais financiers (RE / frais fin.)", 0.20, 3.0,  1.5,  "sup", "x"),
    ("dn_ebe",    "Endettement net / EBE",                             0.15, 2.0,  3.5,  "inf", "x"),
    ("auto",      "Autonomie financière (CP / total bilan)",           0.15, 0.30, 0.15, "sup", "pct"),
    ("d_dfs",     "Dettes fiscales et sociales (jours de CA)",         0.15, 20,   45,   "inf", "j"),
    ("d_frn",     "Délai de règlement fournisseurs (jours)",           0.10, 60,   90,   "inf", "j"),
    ("ct_dette",  "Part de l'endettement à court terme",               0.05, 0.20, 0.40, "inf", "pct"),
]

# Charte MDC 2026 : niveaux en mots, jamais de lettres AAA à D (confusion avec la notation de crédit)
ECHELLE = [(85, "Très solide"), (70, "Solide"), (55, "À surveiller"), (40, "Fragile"), (0, "Critique")]


def _d(x, y):
    """Division protégée."""
    try:
        return x / y if y not in (0, None) else None
    except TypeError:
        return None


def calculer(d, prec=None, params=None):
    """Calcule tous les agrégats d'un exercice.

    d    : dict {cle_poste: montant}
    prec : dict des postes de l'exercice précédent (ou None)
    """
    p = dict(PARAMS_DEFAUT)
    if params:
        p.update(params)
    g = lambda k: float(d.get(k, 0) or 0)
    t, J = p["taux_is"], p["jours"]
    r = OrderedDict()

    # --- soldes intermédiaires de gestion
    r["ca"] = g("v_march") + g("v_prod")
    r["camv"] = g("a_march") + g("var_march")
    r["mc"] = g("v_march") - r["camv"]
    r["prod"] = g("v_prod") + g("prod_imm")
    r["conso"] = g("a_mat") + g("transp") + g("serv")
    r["va"] = r["mc"] + r["prod"] - r["conso"]
    r["ebe"] = r["va"] + g("subv") - g("imp_tax") - g("pers") - g("autres_ch")
    r["re"] = r["ebe"] + g("autres_pr") + g("repr") - g("dot")
    r["rf"] = g("rev_fin") - g("fr_fin")
    r["rao"] = r["re"] + r["rf"]
    r["rn"] = r["rao"] + g("hao") - g("partic") - g("impot")
    r["caf"] = r["rn"] + g("dot") - g("repr")

    # --- bilan financier
    r["immo"] = g("im_inc") + g("im_cor") + g("im_fin") - g("amort")
    actif_circ = (g("stock_b") - g("stock_d") + g("cli_b") - g("cli_d")
                  + g("aut_cr"))
    passif_circ = g("fourn") + g("d_fisc") + g("d_soc") + g("aut_det")
    r["bfr_e"] = actif_circ - passif_circ
    r["bfr_h"] = g("cr_hao") - g("det_hao")
    r["bfr"] = r["bfr_e"] + r["bfr_h"]
    r["ae"] = r["immo"] + r["bfr"]
    r["cp"] = (g("capital") + g("reserv") + g("ran") + g("res_bil")
               + g("subv_inv") + g("prov_regl"))
    r["tres_a"] = g("titres") + g("banque")
    r["dette_b"] = g("emprunt") + g("cbail") + g("cca") + g("decouv")
    r["dn"] = r["dette_b"] - r["tres_a"]
    r["tres_n"] = r["tres_a"] - g("decouv")
    r["tot_actif"] = (r["immo"] + g("stock_b") - g("stock_d") + g("cli_b")
                      - g("cli_d") + g("aut_cr") + g("cr_hao") + r["tres_a"])
    r["tot_passif"] = (r["cp"] + g("emprunt") + g("cbail") + g("prov_risq")
                       + g("cca") + g("fourn") + g("d_fisc") + g("d_soc")
                       + g("aut_det") + g("det_hao") + g("decouv"))

    # --- contrôles de cohérence (bloquants)
    r["ctrl_bilan"] = r["tot_actif"] - r["tot_passif"]
    r["ctrl_resultat"] = r["rn"] - g("res_bil")
    r["ctrl_ae"] = r["cp"] + r["dn"] + g("prov_risq") - r["ae"]
    r["controles_ok"] = (abs(r["ctrl_bilan"]) < 1000
                         and abs(r["ctrl_resultat"]) < 1000
                         and abs(r["ctrl_ae"]) < 1000)

    # --- étape 1 : marges
    r["t_mc"] = _d(r["mc"], r["ca"])
    r["t_va"] = _d(r["va"], r["ca"])
    r["t_ebe"] = _d(r["ebe"], r["ca"])
    r["t_re"] = _d(r["re"], r["ca"])
    r["t_pers"] = _d(g("pers"), r["ca"])
    r["cvar"] = g("a_march") + g("var_march") + g("a_mat") + g("transp")
    r["cfix"] = (g("serv") + g("pers") + g("imp_tax") + g("autres_ch")
                 + g("dot") + g("fr_fin") - g("autres_pr") - g("repr") - g("subv"))
    tx_mcv = _d(r["ca"] - r["cvar"], r["ca"])
    r["point_mort"] = _d(r["cfix"], tx_mcv) if tx_mcv else None
    r["marge_secu"] = (_d(r["ca"] - r["point_mort"], r["ca"])
                       if r["point_mort"] is not None else None)

    # --- étape 2 : BFR et investissements
    r["bfr_j"] = _d(r["bfr_e"] * J, r["ca"])
    r["d_cli"] = _d((g("cli_b") - g("cli_d")) * J, r["ca"])
    r["d_stk"] = _d((g("stock_b") - g("stock_d")) * J, r["camv"])
    r["d_frn"] = _d(g("fourn") * J, g("a_march") + g("a_mat") + g("serv"))
    r["d_dfs"] = _d((g("d_fisc") + g("d_soc")) * J, r["ca"])

    # --- étape 3 : financement
    r["gearing"] = _d(r["dn"], r["cp"])
    r["dn_ebe"] = _d(r["dn"], r["ebe"])
    r["cfi"] = _d(r["re"], g("fr_fin"))
    r["caf_dn"] = _d(r["caf"], r["dn"])
    r["auto"] = _d(r["cp"], r["tot_actif"])
    r["cp_cap"] = _d(r["cp"], g("capital"))
    r["ct_dette"] = _d(g("decouv"), r["dette_b"])
    r["tres_ca"] = _d(r["tres_n"] * J, r["ca"])

    # --- étape 4 : rentabilité et effet de levier
    r["re_eco"] = _d(r["re"] * (1 - t), r["ae"])
    r["i_dette"] = _d(g("fr_fin") * (1 - t), r["dn"])
    if r["re_eco"] is not None and r["i_dette"] is not None and r["cp"]:
        r["levier"] = (r["re_eco"] - r["i_dette"]) * r["dn"] / r["cp"]
        r["roe_th"] = r["re_eco"] + r["levier"]
    else:
        r["levier"] = r["roe_th"] = None
    r["roe_re"] = _d(r["rn"], r["cp"])
    r["ecart_roe"] = (r["roe_re"] - r["roe_th"]
                      if None not in (r["roe_re"], r["roe_th"]) else None)

    # --- étape 5 : coût du capital et création de valeur
    engages = r["cp"] + r["dn"]
    r["w_cp"] = _d(r["cp"], engages)
    r["w_d"] = _d(r["dn"], engages)
    r["kd_net"] = p["cout_dette"] * (1 - t)
    if r["w_cp"] is not None:
        r["cmpc"] = p["cout_fp"] * r["w_cp"] + r["kd_net"] * r["w_d"]
    else:
        r["cmpc"] = None
    r["bneai"] = r["re"] * (1 - t)
    r["vea"] = (r["bneai"] - r["cmpc"] * r["ae"]) if r["cmpc"] is not None else None
    r["spread"] = (r["re_eco"] - r["cmpc"]
                   if None not in (r["re_eco"], r["cmpc"]) else None)

    # --- score Z'' d'Altman (working capital, PAS le BFR)
    wc = (actif_circ + g("cr_hao") + r["tres_a"]) - (passif_circ + g("det_hao") + g("decouv"))
    r["x1"] = _d(wc, r["tot_actif"]) or 0
    r["x2"] = _d(g("reserv") + g("ran"), r["tot_actif"]) or 0
    r["x3"] = _d(r["re"], r["tot_actif"]) or 0
    r["x4"] = _d(r["cp"], r["tot_actif"] - r["cp"]) or 0
    r["z"] = 6.56 * r["x1"] + 3.26 * r["x2"] + 6.72 * r["x3"] + 1.05 * r["x4"]
    r["zone_z"] = ("Zone de défaillance" if r["z"] < 1.1
                   else "Zone grise" if r["z"] <= 2.6 else "Zone saine")

    # --- comparaisons avec l'exercice précédent
    if prec:
        pr = calculer(prec, None, params)
        r["croiss_ca"] = _d(r["ca"], pr["ca"]) - 1 if pr["ca"] else None
        ch = g("a_march") + g("var_march") + r["conso"] + g("pers")
        ch_p = (float(prec.get("a_march", 0)) + float(prec.get("var_march", 0))
                + pr["conso"] + float(prec.get("pers", 0)))
        r["ciseau"] = (_d(ch, ch_p) - (_d(r["ca"], pr["ca"]) or 0)
                       if ch_p else None)
        r["invest"] = ((g("im_inc") + g("im_cor") + g("im_fin"))
                       - (float(prec.get("im_inc", 0)) + float(prec.get("im_cor", 0))
                          + float(prec.get("im_fin", 0))))
    else:
        r["croiss_ca"] = r["ciseau"] = r["invest"] = None

    # --- indice de santé financière MDC
    r["note_detail"] = []
    score = 0.0
    for cle, lib, poids, s_bon, s_moy, sens, fmt in BAREME:
        val = r.get(cle)
        if val is None:
            note = 0
        elif sens == "sup":
            note = 100 if val >= s_bon else 50 if val >= s_moy else 0
        else:
            note = 100 if val <= s_bon else 50 if val <= s_moy else 0
        score += poids * note
        r["note_detail"].append({"cle": cle, "libelle": lib, "poids": poids,
                                 "seuil_bon": s_bon, "seuil_moyen": s_moy,
                                 "valeur": val, "note": note,
                                 "contribution": poids * note, "format": fmt})
    r["score_mdc"] = score
    # Un exercice sans chiffre d'affaires n'est pas notable : saisie incomplète,
    # entité non encore en activité, ou exercice non renseigné.
    r["evaluable"] = r["ca"] != 0
    r["note_mdc"] = (next(lab for seuil, lab in ECHELLE if score >= seuil)
                     if r["evaluable"] else "—")
    return r


# ---------------------------------------------------------------------------
# 3. ALERTES — seuils de lecture (vert / orange / rouge)
#    (cle, libelle, format, sens, seuil_ok, seuil_vigilance, libelle_alerte)
# ---------------------------------------------------------------------------
ALERTES = [
    ("t_ebe",     "Taux d'EBE",                          "pct", "sup", 0.08, 0.04, "ALERTE"),
    ("ciseau",    "Effet de ciseau",                     "pct", "inf", 0.0,  0.02, "ALERTE"),
    ("marge_secu", "Marge de sécurité",                  "pct", "sup", 0.15, 0.05, "ALERTE"),
    ("bfr_j",     "BFR en jours de CA",                  "j",   "inf", 45,   75,   "ALERTE"),
    ("d_cli",     "Délai clients",                       "j",   "inf", 60,   90,   "ALERTE"),
    ("d_stk",     "Délai d'écoulement des stocks",       "j",   "inf", 60,   90,   "ALERTE"),
    ("d_frn",     "Délai fournisseurs",                  "j",   "inf", 60,   90,   "ALERTE"),
    ("d_dfs",     "Dettes fiscales et sociales (j de CA)", "j", "inf", 20,   40,   "ALERTE"),
    ("gearing",   "Levier financier",                    "x",   "inf", 1.0,  2.0,  "ALERTE"),
    ("dn_ebe",    "Endettement net / EBE",               "x",   "inf", 3.0,  4.5,  "ALERTE"),
    ("cfi",       "Couverture des frais financiers",     "x",   "sup", 3.0,  1.5,  "ALERTE"),
    ("auto",      "Autonomie financière",                "pct", "sup", 0.30, 0.15, "ALERTE"),
    ("cp_cap",    "Capitaux propres / capital social",   "x",   "sup", 1.0,  0.5,  "ALERTE"),
    ("ct_dette",  "Endettement à court terme",           "pct", "inf", 0.20, 0.40, "ALERTE"),
    ("levier",    "Effet de levier",                     "pct", "sup", 0.0,  -0.02, "EFFET MASSUE"),
    ("roe_re",    "Rentabilité des capitaux propres",    "pct", "sup", 0.0,  -0.001, "PERTE"),
    ("spread",    "Spread (Re − CMPC)",                  "pct", "sup", 0.0,  -0.001, "DÉTRUIT DE LA VALEUR"),
]


def statut(cle, valeur):
    """Retourne 'OK' / 'Vigilance' / le libellé d'alerte, ou None."""
    for c, _lib, _f, sens, s_ok, s_vig, lab in ALERTES:
        if c != cle:
            continue
        if valeur is None:
            return None
        if sens == "sup":
            return "OK" if valeur >= s_ok else "Vigilance" if valeur >= s_vig else lab
        return "OK" if valeur <= s_ok else "Vigilance" if valeur <= s_vig else lab
    return None


# ---------------------------------------------------------------------------
# 4. LECTURE D'UN CLASSEUR MDC RENSEIGNÉ
# ---------------------------------------------------------------------------
def lire_classeur(chemin):
    """Relit les cellules de saisie d'un classeur produit par
    build_classeur_diagnostic.py. Les cellules de saisie sont des valeurs
    littérales : aucune recalculation n'est nécessaire.

    Retourne (identite: dict, exercices: OrderedDict{label: {poste: valeur}}, params: dict)
    """
    from openpyxl import load_workbook
    wb = load_workbook(chemin, data_only=False)
    ws = wb["Saisie_Balance"]

    index = {}
    for row in ws.iter_rows(min_col=1, max_col=1):
        cell = row[0]
        if isinstance(cell.value, str):
            index[cell.value.strip()] = cell.row
    lib2cle = {lib: cle for cle, lib, _c, _s in POSTES}

    exercices = OrderedDict((lab, {}) for lab in ("N-2", "N-1", "N"))
    for lib, cle in lib2cle.items():
        r = index.get(lib)
        if not r:
            continue
        for col, lab in zip("CDE", ("N-2", "N-1", "N")):
            v = ws[f"{col}{r}"].value
            exercices[lab][cle] = float(v) if isinstance(v, (int, float)) else 0.0

    wp = wb["Parametres"]
    pindex = {}
    for row in wp.iter_rows(min_col=1, max_col=1):
        if isinstance(row[0].value, str):
            pindex[row[0].value.strip()] = row[0].row

    def pv(label, defaut=None):
        r = pindex.get(label)
        if not r:
            return defaut
        v = wp[f"B{r}"].value
        return v if v is not None else defaut

    identite = {
        "client": pv("Raison sociale", "—"),
        "forme": pv("Forme juridique", ""),
        "secteur": pv("Secteur d'activité", ""),
        "exercice": pv("Exercice analysé (N)", ""),
        "auditeur": pv("Auditeur MDC", ""),
    }
    params = {
        "taux_is": pv("Taux d'impôt sur les sociétés", PARAMS_DEFAUT["taux_is"]),
        "jours": pv("Base de jours (ratios de rotation)", PARAMS_DEFAUT["jours"]),
        "cout_fp": pv("Coût des fonds propres exigé", PARAMS_DEFAUT["cout_fp"]),
        "cout_dette": pv("Coût de la dette avant impôt", PARAMS_DEFAUT["cout_dette"]),
    }
    return identite, exercices, params


def calculer_serie(exercices, params=None):
    """exercices : OrderedDict {label: {poste: valeur}} du plus ancien au plus récent."""
    labels = list(exercices.keys())
    out = OrderedDict()
    for i, lab in enumerate(labels):
        prec = exercices[labels[i - 1]] if i > 0 else None
        out[lab] = calculer(exercices[lab], prec, params)
    return out


# ---------------------------------------------------------------------------
# 5. FORMATAGE
# ---------------------------------------------------------------------------
def fmt(valeur, kind):
    if valeur is None:
        return "—"
    if kind == "pct":
        return f"{valeur*100:,.1f} %".replace(",", " ")
    if kind == "x":
        return f"{valeur:,.2f}x".replace(",", " ")
    if kind == "j":
        return f"{valeur:,.0f} j".replace(",", " ")
    if kind == "z":
        return f"{valeur:,.2f}".replace(",", " ")
    return f"{valeur:,.0f}".replace(",", " ") + " FCFA"


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 1:
        ident, ex, par = lire_classeur(sys.argv[1])
        res = calculer_serie(ex, par)
        for lab, r in res.items():
            print(f"--- {lab} : CA {fmt(r['ca'],'f')} | EBE {fmt(r['ebe'],'f')} | "
                  f"note {r['note_mdc']} ({r['score_mdc']:.1f}) | Z'' {r['z']:.2f} "
                  f"| contrôles {'OK' if r['controles_ok'] else 'ANOMALIE'}")
    else:
        print(__doc__)
