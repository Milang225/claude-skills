# -*- coding: utf-8 -*-
"""Ecrit les squelettes des livrables du dossier d'audit, pre-remplis des chiffres de l'Atelier.

Le script ne redige pas : il pose l'en-tete, la reference MC, le plan du document et les
TABLEAUX CHIFFRES, qui ne doivent jamais etre saisis a la main. Chaque passage a ecrire porte
une consigne « A REDIGER » qui dit ce qu'il faut dire et sur quelle matiere de l'Atelier.

  python3 squelettes_audit.py LBTECH "<dossier d'audit>" [--tout|--liste doc1,doc2]
"""
import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from donnees_dossier import charger, pivots, f


def nb(x):
    """Un nombre a virgule a la francaise : 57.1 -> 57,1 ; 29 -> 29."""
    try:
        v = float(x)
    except Exception:
        return str(x)
    return ("%d" % v) if v == int(v) else ("%s" % v).replace(".", ",")


def taux(l):
    """La colonne taux, lisible : 7.5 -> 7,5 %, vide -> l'article, sinon un tiret."""
    t = l.get("taux")
    if t not in (None, "", "—"):
        try:
            return nb(t) + " %"
        except Exception:
            return str(t)
    return l.get("article") or "—"


def base(l):
    b = l.get("base")
    if b in (None, "", "—"):
        return "—"
    try:
        return f(b)
    except Exception:
        return str(b)

MOIS = ("janvier février mars avril mai juin juillet août septembre octobre novembre décembre").split()


def aujourdhui():
    d = datetime.date.today()
    return "%d %s %d" % (d.day, MOIS[d.month - 1], d.year)


def ref(p, type_, n=1):
    return "MC-%s-%s-%d-%03d" % (type_, p["secteur"], datetime.date.today().year, n)


def entete(p, objet, destinataire, type_, n=1, perimetre=True):
    t = ["Objet : %s" % objet, "", "Destinataire : %s" % destinataire,
         "Client : %s — NCC %s" % (p["raison_sociale"], p["ncc"]),
         "Référence : %s" % ref(p, type_, n),
         "Date : Abidjan, le %s" % aujourdhui()]
    if perimetre:
        t.append("Périmètre : exercices %s" % p["exercices"])
    return "\n".join(t) + "\n\n"


def a_rediger(quoi, matiere=""):
    s = "> À RÉDIGER — %s" % quoi
    if matiere:
        s += " Matière : %s." % matiere
    return s + "\n\n"


def exercices(p):
    """Les exercices de la mission, un par un : « 2023 à 2026 » -> [2023, 2024, 2025, 2026]."""
    import re as _re
    s = str(p.get("exercices") or "")
    ans = [int(x) for x in _re.findall(r"(20\d{2})", s)]
    if not ans:
        import datetime as _dt
        return [_dt.date.today().year - 1]
    if len(ans) == 2 and ("à" in s or "a " in s or "-" in s) and ans[1] > ans[0]:
        return list(range(ans[0], ans[1] + 1))
    return sorted(set(ans))


NATURES_PAR_DEFAUT = [
    "Impôt sur les traitements et salaires",
    "Contribution nationale, apprentissage et formation",
    "Cotisations de prévoyance sociale",
    "Droit de timbre de quittance",
    "Taxe de l'entreprenant ou impôt des microentreprises",
    "Taxe sur la valeur ajoutée",
    "Retenues à la source",
    "Taxe spéciale d'équipement",
    "Patente",
    "États annuels 301 et 302",
]


# ─────────────────── la matière venue des formulaires remplis ───────────────────
import json as _json


def collecte(dest):
    """Ce que le classeur des formulaires a recueilli, s'il a ete lu."""
    q = os.path.join(dest, "collecte.json")
    if not os.path.exists(q):
        return {}
    return _json.load(open(q, encoding="utf-8")).get("feuilles", {})


def table_de(coll, feuille, premiere_colonne):
    """Les lignes renseignees du tableau dont la premiere colonne porte ce nom."""
    for nom, blocs in coll.items():
        if not nom.startswith(feuille):
            continue
        for b in blocs:
            if b["colonnes"] and b["colonnes"][0].strip().lower() == premiere_colonne.lower():
                return b["colonnes"], b["lignes"]
    return [], []


def en_tableau(colonnes, lignes, colonnes_gardees=None):
    """Un tableau markdown a partir des lignes du formulaire."""
    cols = colonnes_gardees or colonnes
    t = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    for l in lignes:
        t += "| " + " | ".join(str(l.get(c, "") or "—").replace("\n", " ") for c in cols) + " |\n"
    return t + "\n"


def depuis_formulaire(coll, feuille, premiere_colonne, titre, consigne, gardees=None):
    """Le bloc d'une section : le tableau rempli, ou la consigne si le formulaire est vide."""
    colonnes, lignes = table_de(coll, feuille, premiere_colonne)
    if not lignes:
        return a_rediger(consigne, "le formulaire %s, qui n'a pas encore été rempli" % feuille)
    return en_tableau(colonnes, lignes, gardees) + a_rediger(
        "mettre en forme et commenter le tableau ci-dessus, repris du formulaire %s." % feuille)


# ─────────────────────────── les livrables ───────────────────────────

def tableau_exposition(p, D):
    lignes = (D.get("l06") or {}).get("lignes") or []
    t = entete(p, "tableau de l'exposition de %s par nature" % p["raison_sociale"],
               p["formule"], "TAB")
    t += "| Nature | Exercice | Base de référence | Taux, tarif ou nature | Droits | Position | Pièce |\n"
    t += "|---|---|---|---|---|---|---|\n"
    for l in lignes:
        t += "| %s | %s | %s | %s | %s | %s | %s |\n" % (
            l.get("nature", ""), l.get("exercice", ""), base(l),
            taux(l), f(l.get("droit")),
            l.get("position", ""), l.get("piece", "") or "—")
    t += "| **Total** | | | | **%s** | | |\n\n" % f(p["droits_lignes"])
    t += ("**%s sont déjà exigibles** : ce ne sont pas des risques, ce sont des avis émis et impayés. "
          "L'exposition au scénario central s'établit à **%s**, dans une fourchette de %s à %s selon le "
          "moment de la régularisation.\n\n" % (f(p["deja_exigible"]), f(p["central"]), f(p["bas"]), f(p["haut"])))
    t += a_rediger("une phrase de fin qui dit ce que pèsent les pénalités et ce qui reste discutable, hors total.",
                   "les éléments non cumulables du dossier")
    return t


def synthese_exposition(p, D):
    l3 = D.get("l03") or {}
    t = entete(p, "synthèse de l'exposition de %s par nature d'impôt" % p["raison_sociale"],
               p["formule"], "SYNT")
    t += "%s,\n\n" % p["formule"]
    t += ("Cette synthèse répond à une seule question, nature d'impôt par nature d'impôt : **ce que la loi "
          "imposait, ce qui a été fait, et ce que l'écart expose**. Le détail de chaque calcul, avec son "
          "assiette et son taux, figure dans la note de chiffrage des expositions.\n\n")
    t += "## 1. Le verdict en une phrase\n\n"
    t += ("Au %s, l'exposition de la société s'établit à **%s** au scénario central, dont **%s ne sont pas un "
          "risque mais une dette déjà exigible**, et l'Indice de conformité s'établit à %s sur 100, niveau %s.\n\n"
          % (aujourdhui(), f(p["central"]), f(p["deja_exigible"]), p["indice"], p["niveau"]))
    t += "## 2. Ce qui n'a pas été fait, et ce que cela expose\n\n"
    t += "| Nature | Ce que la loi imposait | Ce qui a été fait | Exposition au central |\n|---|---|---|---|\n"
    groupes = {}
    for l in (D.get("l06") or {}).get("lignes") or []:
        g = l.get("nature_tdb") or l.get("nature", "")
        groupes.setdefault(g, []).append(l)
    for g, ls in groupes.items():
        tot = sum(float(x.get("central") or 0) for x in ls)
        t += "| %s | À RÉDIGER | À RÉDIGER, d'après : %s | **%s** |\n" % (
            g, " ; ".join(sorted({(x.get("situation") or "") for x in ls})), f(tot))
    t += "\n" + a_rediger("les deux colonnes du milieu, ligne par ligne : l'obligation dans le texte, puis ce que les pièces établissent.",
                          "l'état des obligations de l'Atelier (L03) et les pièces citées au tableau d'exposition")
    t += "## 3. Pourquoi cela s'est produit\n\n"
    t += a_rediger("deux causes, pas davantage, dont tout le reste découle ; puis dire si elles reculent.",
                   "les constats du rapport de diagnostic (L04) et la revue des procédures")
    t += "## 4. Ce qui est dû, et ce qui est encore discutable\n\n"
    t += "| | Montant | Ce que l'on peut en faire |\n|---|---|---|\n"
    t += "| Déjà exigible | %s | Rien. Ce sont des avis émis et impayés |\n" % f(p["deja_exigible"])
    t += "| Redressement possible, position prudente | %s | Une partie se réduit par les pièces et les actes |\n" % f(
        float(p["central"] or 0) - float(p["deja_exigible"] or 0))
    t += "| **Exposition totale, scénario central** | **%s** | |\n" % f(p["central"])
    t += "| Scénario favorable | %s | Ce que vaut une régularisation engagée maintenant |\n" % f(p["bas"])
    t += "| Scénario haut | %s | Ce que coûte l'attente jusqu'au contrôle |\n\n" % f(p["haut"])
    t += ("L'écart entre le scénario favorable et le scénario haut, **%s**, mesure exactement ce que vaut la "
          "régularisation volontaire.\n\n" % f(float(p["haut"] or 0) - float(p["bas"] or 0)))
    t += "## 5. Ce qui réduit l'exposition, et ce qu'il faut savoir avant de décider\n\n"
    t += a_rediger("les trois leviers qui pèsent plus que tout le reste, chacun chiffré, et le coût des actes à établir.",
                   "les éléments favorables de l'Atelier (L06) et les priorités")
    return t


def constat_non_conformite(p, D):
    t = entete(p, "constat de non-conformité et Indice de conformité de %s" % p["raison_sociale"],
               p["formule"], "NCF")
    t += "## 1. L'Indice de conformité\n\n"
    t += ("L'Indice de conformité de la société s'établit à **%s sur 100**, niveau **%s**. "
          "L'attestation de diagnostic suppose un Indice d'au moins 70 sans manquement critique : "
          "la société en compte %d, et l'attestation n'est donc pas délivrable.\n\n"
          % (nb(p["indice"]), p["niveau"], p["critiques"]))
    t += "## 2. La décomposition par domaine\n\n"
    t += "| Domaine | Score sur 100 | Ce qui le tient à ce niveau |\n|---|---|---|\n"
    for d in p["domaines"]:
        t += "| %s | %s | À RÉDIGER |\n" % (d.get("nom", ""), nb(d.get("score", "")))
    t += "\n" + a_rediger("pour chaque domaine, la raison de son score, en une ligne, sans jargon.",
                          "les contrôles non tenus du rapport de diagnostic (L04) et les matrices d'anomalies")
    t += "## 3. Ce qui est constaté\n\n"
    t += "| Matrice | Critiques | Majeures | Mineures | Total |\n|---|---|---|---|---|\n"
    tot = [0, 0, 0]
    for a in D.get("anomalies") or []:
        c, m, n = int(a.get("critiques") or 0), int(a.get("majeures") or 0), int(a.get("mineures") or 0)
        tot = [tot[0] + c, tot[1] + m, tot[2] + n]
        t += "| %s | %d | %d | %d | %d |\n" % (a.get("matrice", ""), c, m, n, c + m + n)
    t += "| **Total** | **%d** | **%d** | **%d** | **%d** |\n\n" % (tot[0], tot[1], tot[2], sum(tot))
    t += "## 4. Les leviers de relèvement\n\n"
    t += a_rediger("ce qui relève l'Indice, par ordre de rendement : quel geste, quel domaine, combien de points.",
                   "les priorités de l'Atelier et la méthode de l'Indice")
    t += "## 5. La portée du présent constat\n\n"
    t += ("Le présent constat établit l'état de conformité de la société à la date ci-dessus, sur les pièces "
          "communiquées. Il ne vaut ni attestation, ni certification, ni visa. Il sera remplacé par une "
          "attestation de diagnostic dès que l'Indice aura atteint le niveau requis et que les manquements "
          "critiques auront été levés.\n\n")
    return t


def audit_documentaire(p, D):
    l2 = D.get("l02") or {}
    t = entete(p, "audit documentaire de %s" % p["raison_sociale"], p["formule"], "DOC")
    t += "## 1. L'essentiel\n\n"
    t += ("Sur **%s documents applicables**, **%s sont présents et complets**, soit **%s %%**. "
          "Le reste est à produire ou à compléter.\n\n"
          % (p["documents_applicables"], p["documents_presents"], p.get("documents_taux")))
    t += "## 2. Le score par domaine\n\n"
    t += "| Domaine | Applicables | Présents | Incomplets | Absents | À examiner | Taux |\n|---|---|---|---|---|---|---|\n"
    for d in l2.get("domaines") or []:
        ap = int(d.get("applicables") or 0)
        pr = int(d.get("presents") or 0)
        t += "| %s | %d | %d | %s | %s | %s | %d %% |\n" % (
            d.get("domaine", ""), ap, pr, d.get("incomplets", ""), d.get("absents", ""),
            d.get("a_examiner", ""), round(100.0 * pr / ap) if ap else 0)
    t += "\n## 3. L'inventaire, pièce par pièce\n\n"
    t += "| Domaine | Document | Situation | Pourquoi il manque, et ce que l'absence coûte | Critique |\n|---|---|---|---|---|\n"
    for d in l2.get("documents") or []:
        t += "| %s | %s | %s | %s | %s |\n" % (
            d.get("domaine", ""), d.get("document", ""), d.get("situation", ""),
            d.get("pourquoi", ""), d.get("critique", ""))
    t += "\n## 4. Les pièces à produire, par ordre d'urgence\n\n"
    t += a_rediger("l'ordre dans lequel les réclamer, et ce que chacune referme.",
                   "les documents critiques du tableau ci-dessus")
    return t


def plan_action(p, D):
    t = entete(p, "plan d'action de mise en conformité de %s" % p["raison_sociale"],
               p["formule"], "PLAN")
    t += ("Le plan est rangé par rangs, du geste qui ne coûte qu'une demande à celui qui protège l'avenir. "
          "Chaque rang referme une part de l'exposition.\n\n")
    prios = D.get("priorites") or []
    if prios:
        t += "## Les actions retenues par le diagnostic\n\n"
        t += "| Action | Montant |\n|---|---|\n"
        for pr in prios:
            m = pr.get("texte_montant") or (f(pr["montant"]) if pr.get("montant") else "—")
            t += "| %s | %s |\n" % (pr.get("action", ""), m)
        t += "\n"
    noms = ["Premier rang — ce qui ne coûte que des demandes",
            "Deuxième rang — les actes à signer",
            "Troisième rang — les déclarations à déposer",
            "Quatrième rang — ce qui protège l'avenir"]
    for nom in noms:
        t += "## %s\n\n" % nom
        t += "| Action | Montant | Qui le fait | Ce que le geste referme |\n|---|---|---|---|\n"
        t += "| À RÉDIGER | | | |\n\n"
    t += a_rediger("ranger chaque action ci-dessus dans l'un des quatre rangs, puis dire pour chacune "
                   "qui l'exécute, son montant et ce qu'elle referme exactement. Le numéro porté par "
                   "l'Atelier est un numéro d'action, pas un rang.",
                   "les priorités et la feuille de route de l'Atelier")
    t += "## Ce que le plan produit, rang par rang\n\n"
    t += a_rediger("ce que l'exposition devient une fois chaque rang exécuté.", "le chiffrage de l'exposition")
    return t


def note_chiffrage(p, D):
    lignes = (D.get("l06") or {}).get("lignes") or []
    groupes = {}
    for l in lignes:
        groupes.setdefault(l.get("nature_tdb") or l.get("nature", ""), []).append(l)
    t = entete(p, "note de chiffrage des expositions de %s" % p["raison_sociale"],
               "%s — document sensible, diffusion restreinte" % p["formule"], "EXPO")
    t += "## 1. L'essentiel\n\n"
    t += ("L'exposition s'établit à **%s** au scénario central, **%s** au scénario favorable et **%s** au "
          "scénario haut. Les droits simples, hors intérêts et majorations, s'élèvent à **%s**.\n\n"
          % (f(p["central"]), f(p["bas"]), f(p["haut"]), f(p["droits"])))
    t += "## 2. La méthode, et ce qui la fonde\n\n"
    t += a_rediger("la méthode : droits simples, puis intérêts et majorations, puis les trois scénarios ; "
                   "et la règle selon laquelle une réduction n'entre dans un chiffrage que sur justificatif produit.")
    n = 3
    for g, ls in groupes.items():
        t += "## %d. Poste — %s\n\n" % (n, g)
        t += "| Élément | Exercice | Période | Situation | Base | Taux ou article | Droits | Bas | Central | Haut | Pièce |\n"
        t += "|---|---|---|---|---|---|---|---|---|---|---|\n"
        for l in ls:
            t += "| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n" % (
                l.get("nature", ""), l.get("exercice", ""), l.get("periode", ""), l.get("situation", ""),
                base(l), taux(l),
                f(l.get("droit")), f(l.get("bas")), f(l.get("central")), f(l.get("haut")),
                l.get("piece", "") or "—")
        s = lambda k: f(sum(float(x.get(k) or 0) for x in ls))
        t += "| **Total du poste** | | | | | | **%s** | **%s** | **%s** | **%s** | |\n\n" % (
            s("droit"), s("bas"), s("central"), s("haut"))
        t += a_rediger("ce que le texte impose sur ce poste, ce que les pièces établissent, et la position de "
                       "défense : forte, discutable ou faible.")
        n += 1
    t += "## %d. État récapitulatif consolidé\n\n" % n
    t += "| Scénario | Montant | Ce qu'il suppose |\n|---|---|---|\n"
    t += "| Droits simples | %s | Une régularisation engagée spontanément, hors intérêts et majorations |\n" % f(p["droits"])
    t += "| Favorable | %s | À RÉDIGER |\n" % f(p["bas"])
    t += "| Central | %s | À RÉDIGER |\n" % f(p["central"])
    t += "| Haut | %s | À RÉDIGER |\n\n" % f(p["haut"])
    t += "## %d. Ce qui s'additionne, et ce qui ne se cumule jamais\n\n" % (n + 1)
    t += a_rediger("les qualifications qui s'excluent, présentées hors total et jamais cumulées.",
                   "les risques à part de l'Atelier")
    return t


def rapport_audit(p, D):
    t = entete(p, "rapport d'audit de conformité fiscale, sociale et comptable de %s" % p["raison_sociale"],
               p["formule"], "AUD")
    t += "%s,\n\n" % p["formule"]
    t += "## 1. L'essentiel\n\n"
    t += ("L'audit porte sur les exercices %s. Il relève **%d anomalies, dont %d critiques**, chiffre une "
          "exposition de **%s** au scénario central, et établit un Indice de conformité de **%s sur 100**, "
          "niveau %s.\n\n" % (p["exercices"], p["anomalies"], p["critiques"], f(p["central"]),
                              nb(p["indice"]), p["niveau"]))
    t += a_rediger("les trois ou quatre décisions qui comptent, chacune chiffrée.")
    t += "## 2. Ce que nous avons examiné, et les limites\n\n"
    t += a_rediger("les pièces reçues, la méthode, et les limites déclarées : ce qui n'a pas pu être vérifié.",
                   "les pièces du client et les limites de l'Atelier (L08)")
    t += "## 3. Audit documentaire : l'inventaire des pièces\n\n"
    t += "| Domaine | Applicables | Présents | Taux |\n|---|---|---|---|\n"
    for d in (D.get("l02") or {}).get("domaines") or []:
        ap, pr = int(d.get("applicables") or 0), int(d.get("presents") or 0)
        t += "| %s | %d | %d | %d %% |\n" % (d.get("domaine", ""), ap, pr, round(100.0 * pr / ap) if ap else 0)
    t += "\n"
    for num, nom in ((4, "fiscales"), (5, "sociales"), (6, "comptables")):
        t += "## %d. Matrice des anomalies %s\n\n" % (num, nom)
        t += "| Code | Constat | Exercice | Texte | Exposition | Gravité | Position | Stratégie |\n"
        t += "|---|---|---|---|---|---|---|---|\n"
        t += "| À RÉDIGER | | | | | | | |\n\n"
    t += a_rediger("les trois matrices, une ligne par anomalie, codées F, S et C, chacune sourcée, chiffrée, "
                   "avec sa gravité, sa position de défense et sa stratégie.",
                   "les matrices d'anomalies de l'Atelier et les lignes d'exposition")
    t += "## 7. État récapitulatif\n\n"
    t += "**Par domaine et par gravité :**\n\n"
    t += "| Domaine | Anomalies | Critiques | Majeures | Mineures |\n|---|---|---|---|---|\n"
    tot = [0, 0, 0]
    for a in D.get("anomalies") or []:
        c, m, n2 = int(a.get("critiques") or 0), int(a.get("majeures") or 0), int(a.get("mineures") or 0)
        tot = [tot[0] + c, tot[1] + m, tot[2] + n2]
        t += "| %s | %d | %d | %d | %d |\n" % (a.get("matrice", ""), c + m + n2, c, m, n2)
    t += "| **Total** | **%d** | **%d** | **%d** | **%d** |\n\n" % (sum(tot), tot[0], tot[1], tot[2])
    t += "**Par nature d'impôt ou de cotisation :**\n\n"
    t += "| Nature | Droits | Central |\n|---|---|---|\n"
    gr = {}
    for l in (D.get("l06") or {}).get("lignes") or []:
        g = l.get("nature_tdb") or l.get("nature", "")
        gr.setdefault(g, [0, 0])
        gr[g][0] += float(l.get("droit") or 0)
        gr[g][1] += float(l.get("central") or 0)
    for g, (dr, ce) in gr.items():
        t += "| %s | %s | %s |\n" % (g, f(dr), f(ce))
    t += "| **Total** | **%s** | **%s** |\n\n" % (f(p["droits_lignes"]), f(p["central_lignes"]))
    t += "## 8. Les conseils pour l'avenir\n\n"
    t += a_rediger("les règles de tenue à installer, numérotées, chacune tenant en une phrase.")
    t += "## 9. Ce que nous demandons à votre comptable\n\n"
    t += a_rediger("le renvoi à la note d'instructions au comptable, et l'inventaire des documents qui "
                   "accompagnent le rapport, avec le destinataire de chacun.")
    return t


def simple(p, titre, objet, destinataire, type_, plan, matiere=""):
    t = entete(p, objet, destinataire, type_)
    for i, s in enumerate(plan, 1):
        t += "## %d. %s\n\n" % (i, s)
        t += a_rediger("cette section.", matiere) if i == 1 else a_rediger("cette section.")
    return t


def le_point(p, D, coll=None):
    coll = coll or {}
    t = entete(p, "le point sur les sujets arrêtés avec le Gérant et les bons usages", p["formule"], "PT")
    t += "%s,\n\n" % p["formule"]
    t += ("Cette note reprend, sujet par sujet, ce que vous nous avez demandé d'arrêter, ce que nous avons "
          "répondu, et ce que la décision coûte ou épargne.\n\n")
    t += "## 1. Les sujets arrêtés\n\n"
    t += depuis_formulaire(coll, "F6", "Sujet", "", 
                           "les sujets arrêtés avec le dirigeant, un par section, chacun finissant par ce qu'il faut faire.")
    t += "## 2. Les montants arrêtés, et ce qui les fonde\n\n"
    t += depuis_formulaire(coll, "F6", "Montant arrêté", "",
                           "les montants que la Direction a arrêtés, avec l'assiette retenue et la raison du choix.")
    t += "## 3. Les bons usages à installer\n\n"
    t += a_rediger("les règles de tenue qui évitent que le sujet revienne, en une phrase chacune.")
    t += "## 4. Le coût de la régularisation, en une fois\n\n"
    t += a_rediger("ce que coûte l'ensemble des décisions prises, et ce qu'il épargne.")
    return t


def modeles_actes(p, D, coll=None):
    coll = coll or {}
    t = entete(p, "modèles d'actes et instructions d'ordre juridique pour %s" % p["raison_sociale"],
               "%s, pour remise à l'avocat ou au notaire qui établira les actes" % p["formule"], "ACT")
    t += "Remise : par Monsieur le Gérant, à l'avocat ou au notaire qui établira les actes.\n\n"
    t += ("**Les actes ci-après doivent être établis et déposés par un avocat ou un notaire, qui en assume la "
          "rédaction définitive.** Les modèles qui suivent sont des bases de travail destinées à ce conseil ; "
          "ils ne le remplacent pas.\n\n")
    t += "## 1. Les actes à prendre, et dans quel ordre\n\n"
    t += depuis_formulaire(coll, "F7", "Acte ou convention", "",
                           "la liste des actes manquants, avec qui les établit et dans quel ordre les prendre.")
    t += "## 2. Les biens inscrits à l'actif au nom d'un tiers\n\n"
    t += depuis_formulaire(coll, "F7", "Bien", "",
                           "les biens à régulariser, et par quel acte.")
    t += "## 3. Les baux\n\n"
    t += depuis_formulaire(coll, "F7", "Local", "", "les baux à écrire ou à enregistrer.")
    t += "## 4. Les modèles\n\n"
    t += a_rediger("un modèle par acte : objet, signataires, formalités, droits à payer, conservation.")
    return t


def script_restitution(p, D, coll=None):
    coll = coll or {}
    t = entete(p, "script de l'entretien de restitution de l'audit de %s" % p["raison_sociale"],
               "interne — ne jamais remettre au client", "SCR")
    t += "## 1. Le cadre de l'entretien\n\n"
    t += depuis_formulaire(coll, "F8", "Élément", "", "la date, le lieu et les participants.")
    t += "## 2. Ce qui va bien, à dire en ouverture\n\n"
    t += depuis_formulaire(coll, "F8", "Ce qui va bien", "", "ce qui va bien, et ce qui le prouve.")
    t += "## 3. La règle du jeu, avant les chiffres\n\n"
    t += a_rediger("ce qu'il doit comprendre avant d'entendre un montant.")
    t += "## 4. Le chiffre, en trois parts\n\n"
    t += ("Ce qui est déjà exigible : **%s**. Ce qui est un redressement possible : **%s**. "
          "Ce qui se discute encore, à présenter sans le cumuler au reste.\n\n"
          % (f(p["deja_exigible"]), f(float(p["central"] or 0) - float(p["deja_exigible"] or 0))))
    t += a_rediger("la manière de présenter ces trois parts, sans faire entendre un total qui n'existe pas.")
    t += "## 5. Les questions qu'il va poser, et la réponse\n\n"
    t += depuis_formulaire(coll, "F8", "La question attendue", "", "les questions attendues et les réponses.")
    t += "## 6. Ce que nous attendons de lui\n\n"
    t += depuis_formulaire(coll, "F8", "Ce que nous attendons", "", "ce que l'Agence attend, et ce que cela débloque.")
    t += "## 7. Ce qu'il ne faut pas dire\n\n"
    t += depuis_formulaire(coll, "F8", "À ne pas dire", "", "ce qu'il ne faut pas dire, et quoi dire à la place.")
    return t


def grille_declarations(p, D, coll=None):
    """La grille déclarative : une case par nature et par période, sur TOUS les exercices."""
    coll = coll or {}
    ans = exercices(p)
    t = entete(p, "grille des déclarations de %s, exercice par exercice" % p["raison_sociale"],
               p["formule"], "GRILLE")
    t += ("Cette grille dit, pour chaque nature d'impôt ou de cotisation et pour chaque période, "
          "si la déclaration a été déposée **et** si elle a été payée. Elle couvre les exercices %s.\n\n"
          % " à ".join([str(ans[0]), str(ans[-1])]) if len(ans) > 1 else "Cette grille couvre l'exercice %d.\n\n" % ans[0])
    t += ("**Les codes.** D+ déclaré et payé · D− déclaré non payé · D* déclaré à zéro ou minoré · "
          "N non déclaré · TO+ taxé d'office et payé · TO− taxé d'office non payé · — néant · ~ à vérifier. "
          "Une case inconnue reste à vérifier : elle ne se devine pas.\n\n")
    colonnes, lignes = table_de(coll, "F3", "Nature de l'impôt ou de la cotisation")
    mois = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
    for an in ans:
        t += "## Exercice %d\n\n" % an
        t += "| Nature | " + " | ".join(mois) + " |\n|" + "---|" * 13 + "\n"
        pour_cet_an = [l for l in lignes if str(l.get("Exercice", "")).strip() in (str(an), "")] if lignes else []
        if pour_cet_an:
            for l in pour_cet_an:
                t += "| %s | %s |\n" % (l.get("Nature de l'impôt ou de la cotisation", ""),
                                        " | ".join(str(l.get(m, "") or "~") for m in mois))
        else:
            for n in NATURES_PAR_DEFAUT:
                t += "| %s | %s |\n" % (n, " | ".join(["~"] * 12))
        t += "\n"
    if not lignes:
        t += a_rediger("remplir la grille case par case d'après l'historique e-impôts et les quittances ; "
                       "une case inconnue reste « à vérifier ».", "le formulaire F3, qui n'a pas encore été rempli")
    t += "## Ce que la grille établit\n\n"
    t += a_rediger("ce que la lecture de la grille démontre : les natures jamais déclarées, celles déclarées "
                   "et non payées, et les périodes où la rupture commence.")
    t += "## Les avis émis et les procédures de l'administration\n\n"
    t += depuis_formulaire(coll, "F3", "Nature", "",
                           "les avis émis, leur base, leur montant et ce qui reste dû.")
    t += depuis_formulaire(coll, "F3", "Nature de la procédure", "",
                           "les procédures engagées par l'administration et la suite donnée à chacune.")
    return t


def audit_procedures(p, D, coll=None):
    """L'audit des procédures internes et externes."""
    coll = coll or {}
    l07, l12, l19 = D.get("l07") or {}, D.get("l12") or {}, D.get("l19") or {}
    ans = exercices(p)
    t = entete(p, "audit des procédures internes et externes de %s" % p["raison_sociale"],
               p["formule"], "PROC")
    t += ("Cet audit ne porte pas sur les chiffres mais sur **la manière dont ils se forment** : qui fait quoi, "
          "avec quelle pièce, et ce qui se perd en chemin. Il couvre les exercices %s.\n\n"
          % (" à ".join([str(ans[0]), str(ans[-1])]) if len(ans) > 1 else str(ans[0])))
    t += "## 1. Ce que nous avons examiné\n\n"
    t += a_rediger("les procédures observées, les personnes rencontrées, et ce qui n'a pas pu être observé.")
    t += "## 2. Les procédures internes\n\n"
    t += ("| Procédure | Comment elle fonctionne aujourd'hui | Ce qui s'y perd | Le risque | Ce qu'il faut installer |\n"
          "|---|---|---|---|---|\n")
    for proc in ("Encaissement des recettes", "Décaissements et validation des dépenses",
                 "Tenue de la caisse", "Facturation et numérotation", "Paie et registre du personnel",
                 "Achats et réception des factures fournisseurs", "Classement et conservation des pièces",
                 "Délégations de signature et accès bancaires", "Arrêté périodique des comptes"):
        t += "| %s | À RÉDIGER | | | |\n" % proc
    t += "\n" + a_rediger("remplir ce tableau ligne par ligne, d'après ce qui a été observé.",
                          "la revue des procédures de l'Atelier et les constats du dossier")
    t += "## 3. Les procédures externes\n\n"
    t += ("| Relation | Ce que la règle impose | Ce qui est fait | L'écart et son coût |\n|---|---|---|---|\n")
    for proc in ("Administration fiscale : dépôt et paiement", "Caisse de prévoyance sociale",
                 "Inspection du travail", "Banque : domiciliation et justification des flux",
                 "Clients : facture normalisée et retenues subies",
                 "Fournisseurs et prestataires : facture et retenues à opérer",
                 "Greffe et registre du commerce", "Conseils : comptable, avocat, notaire"):
        t += "| %s | À RÉDIGER | | |\n" % proc
    t += "\n" + a_rediger("remplir ce tableau, chaque écart étant chiffré lorsqu'il l'est ailleurs dans le dossier.")
    t += "## 4. Les points de rupture\n\n"
    t += a_rediger("les trois ou quatre endroits où la chaîne se casse, et ce que chacun produit en aval. "
                   "C'est la section qui explique les anomalies plutôt que de les répéter.")
    t += "## 5. Les procédures à écrire, par ordre\n\n"
    t += "| Procédure | Qui l'écrit | Qui l'applique | Ce qu'elle referme |\n|---|---|---|---|\n"
    t += "| À RÉDIGER | | | |\n\n"
    t += a_rediger("l'ordre dans lequel écrire les procédures manquantes.")
    return t


DOCS = {
    "SYNTHESE_DE_L_EXPOSITION": synthese_exposition,
    "GRILLE_DES_DECLARATIONS": grille_declarations,
    "AUDIT_DES_PROCEDURES": audit_procedures,
    "TABLEAU_D_EXPOSITION": tableau_exposition,
    "RAPPORT_AUDIT_CONFORMITE": rapport_audit,
    "AUDIT_DOCUMENTAIRE": audit_documentaire,
    "NOTE_DE_CHIFFRAGE_DES_EXPOSITIONS": note_chiffrage,
    "CONSTAT_DE_NON_CONFORMITE": constat_non_conformite,
    "PLAN_D_ACTION": plan_action,
    "NOTE_AU_COMPTABLE": lambda p, D: simple(p, "", "instructions comptables et déclaratives pour la tenue du dossier %s" % p["raison_sociale"],
        "le comptable de la société, ou le cabinet qui prendra le dossier", "NC",
        ["L'état du dossier à ce jour", "Le régime, et ce qu'il commande", "Ce qu'il faut ouvrir, et tenir",
         "Les écritures de régularisation à passer", "Les amortissements", "Le calendrier déclaratif à tenir",
         "Les règles de tenue que nous demandons", "Ce que nous vous demandons de nous signaler"],
        "les notes comptables de l'Atelier (L21) et les rapprochements"),
    "LE_POINT_ET_LES_BONS_USAGES": le_point,
    "MODELES_ACTES_JURIDIQUES": modeles_actes,
    "SCRIPT_DE_RESTITUTION": script_restitution,
}


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        raise SystemExit(__doc__)
    dossier, dest = a[0], a[1]
    fichier = a[a.index("--json") + 1] if "--json" in a else None
    liste = a[a.index("--liste") + 1].split(",") if "--liste" in a else list(DOCS)
    D, source = charger(dossier, fichier)
    p = pivots(D)
    p["lignes_sans_piece"] = 0
    coll = collecte(dest)
    if coll:
        print("  matière reprise des formulaires : %d feuille(s)" % len(coll))
    src = os.path.join(dest, "_SOURCES_MD")
    os.makedirs(src, exist_ok=True)
    nom = p["raison_sociale"].replace(" ", "_").replace("'", "")
    ecrits = []
    for cle in liste:
        if cle not in DOCS:
            print("  (inconnu, ignoré : %s)" % cle); continue
        chemin = os.path.join(src, "%s_%s.md" % (cle, nom))
        if os.path.exists(chemin):
            print("  déjà là, non écrasé : %s" % os.path.basename(chemin)); continue
        fonc = DOCS[cle]
        try:
            texte = fonc(p, D, coll)
        except TypeError:
            texte = fonc(p, D)
        open(chemin, "w", encoding="utf-8").write(texte)
        ecrits.append(os.path.basename(chemin))
        print("  écrit : %s" % os.path.basename(chemin))
    print("\n%d squelette(s) dans %s" % (len(ecrits), src))
    print("Source des données : %s" % source)


if __name__ == "__main__":
    main()
