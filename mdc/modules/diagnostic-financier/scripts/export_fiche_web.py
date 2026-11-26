# -*- coding: utf-8 -*-
"""
EXPORT WEB DU DIAGNOSTIC FINANCIER — MDC

Transforme un classeur de diagnostic renseigné en :
  • une FICHE HTML autonome (aucune ressource externe : CSS et logo embarqués),
    publiable telle quelle sur un site, un intranet ou le VPS ;
  • un fichier JSON de données, pour alimenter un site dynamique.

La fiche s'adapte au thème clair/sombre du visiteur et reste lisible sur mobile.

Usage
-----
  python3 export_fiche_web.py CLASSEUR.xlsx --out fiche.html
  python3 export_fiche_web.py CLASSEUR.xlsx --out fiche.html --json donnees.json
  python3 export_fiche_web.py CLASSEUR.xlsx --out fiche.html --anonyme
  python3 export_fiche_web.py CLASSEUR.xlsx --out fiche.html --interne

  --anonyme  masque la raison sociale (publication d'exemple / démonstration)
  --interne  ajoute le bandeau « DOCUMENT INTERNE — NE PAS DIFFUSER »

Rappel déontologique : une note dégradée communiquée à des tiers peut accélérer
la dégradation du client. Ne publiez une fiche nominative qu'avec l'accord écrit
du client, conformément au cadre contractuel de la mission.
"""

import argparse
import base64
import datetime
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur_diagnostic import (lire_classeur, calculer_serie,  # noqa: E402
                               statut, fmt)

LOGO = os.path.expanduser("~/.claude/skills/mdc-expert/scripts/logo-mdc.jpg")

IDENTITE_MDC = ("LA MAISON DE LA CONFORMITÉ SARL — Diagnostic, mise en conformité et défense en contrôle "
                "(Comptable · Fiscal · Social) — NCC 2506426B — "
                "RCCM CI-ABJ-03-2025-B13-10831 — Capital 1 000 000 FCFA")

# (cle, libellé, format, commentaire)
BLOCS = [
    ("1. L'entreprise crée-t-elle de la richesse ?", [
        ("croiss_ca", "Croissance du chiffre d'affaires", "pct", ""),
        ("t_mc", "Taux de marge commerciale", "pct", ""),
        ("t_va", "Taux de valeur ajoutée", "pct", ""),
        ("t_ebe", "Taux d'EBE", "pct", "Indicateur central de la rentabilité d'exploitation"),
        ("ciseau", "Effet de ciseau", "pct", "Positif = les charges progressent plus vite que le CA"),
        ("point_mort", "Point mort financier", "f", ""),
        ("marge_secu", "Marge de sécurité", "pct", "Coussin avant le point mort"),
    ]),
    ("2. Cette richesse exige des investissements", [
        ("bfr_j", "BFR en jours de chiffre d'affaires", "j", "Trésorerie immobilisée par le cycle"),
        ("d_cli", "Délai de recouvrement clients", "j", "Un allongement = impayés ou CA fictif"),
        ("d_stk", "Délai d'écoulement des stocks", "j", ""),
        ("d_frn", "Délai de règlement fournisseurs", "j", "Signal avancé de défaillance"),
        ("d_dfs", "Dettes fiscales et sociales", "j", "Exposition fiscale ET signal de défaillance"),
        ("invest", "Investissements de l'exercice", "f", ""),
    ]),
    ("3. Ces investissements doivent être financés", [
        ("gearing", "Levier financier (dette nette / fonds propres)", "x", ""),
        ("dn_ebe", "Endettement net / EBE", "x", "Norme d'orthodoxie : 3x maximum"),
        ("cfi", "Couverture des frais financiers", "x", "Sous 1x, l'exploitation ne paie plus la banque"),
        ("auto", "Autonomie financière", "pct", ""),
        ("cp_cap", "Capitaux propres / capital social", "x", "Sous 50 %, régularisation AUSCGIE obligatoire"),
        ("ct_dette", "Part de l'endettement à court terme", "pct", ""),
        ("tres_ca", "Trésorerie nette en jours de CA", "j", ""),
    ]),
    ("4. Et être suffisamment rentables", [
        ("re_eco", "Rentabilité économique après impôt (Re)", "pct", ""),
        ("i_dette", "Coût de la dette après impôt (i)", "pct", ""),
        ("levier", "Effet de levier (Re − i) × D/CP", "pct", "Négatif : l'endettement détruit la rentabilité"),
        ("roe_re", "Rentabilité des capitaux propres", "pct", ""),
    ]),
    ("5. Création de valeur et solvabilité", [
        ("cmpc", "Coût moyen pondéré du capital", "pct", ""),
        ("spread", "Spread (Re − CMPC)", "pct", "Le juge de paix"),
        ("vea", "Valeur économique ajoutée", "f", "Négative = destruction de valeur"),
        ("z", "Score Z'' d'Altman", "z", ""),
    ]),
]

CHIFFRES = [("ca", "Chiffre d'affaires"), ("ebe", "Excédent brut d'exploitation"),
            ("re", "Résultat d'exploitation"), ("rn", "Résultat net"),
            ("caf", "Capacité d'autofinancement"), ("ae", "Actif économique"),
            ("cp", "Capitaux propres"), ("dn", "Endettement net"),
            ("bfr", "Besoin en fonds de roulement")]

CSS = """
:root{
  --bg:#ffffff; --surface:#f7f8fa; --border:#e2e5ea; --ink:#1a1d22; --muted:#5c636e;
  --navy:#1F3864; --navy-soft:#e8edf6; --or:#b8860b;
  --ok-bg:#e6f4ea; --ok-ink:#1e6b38; --warn-bg:#fdf3d8; --warn-ink:#8a6100;
  --bad-bg:#fdeaea; --bad-ink:#a11b1b;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#12151a; --surface:#1a1f27; --border:#2b323d; --ink:#e8eaee; --muted:#9aa3b0;
    --navy:#8fb0e8; --navy-soft:#1c2740; --or:#d7a93b;
    --ok-bg:#12301f; --ok-ink:#7ddba0; --warn-bg:#3a2e10; --warn-ink:#e8c46a;
    --bad-bg:#3a1717; --bad-ink:#f0908f;
  }
}
:root[data-theme="dark"]{
  --bg:#12151a; --surface:#1a1f27; --border:#2b323d; --ink:#e8eaee; --muted:#9aa3b0;
  --navy:#8fb0e8; --navy-soft:#1c2740; --or:#d7a93b;
  --ok-bg:#12301f; --ok-ink:#7ddba0; --warn-bg:#3a2e10; --warn-ink:#e8c46a;
  --bad-bg:#3a1717; --bad-ink:#f0908f;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;}
.wrap{max-width:960px;margin:0 auto;padding:28px 20px 64px}
header{display:flex;gap:18px;align-items:center;border-bottom:3px solid var(--navy);padding-bottom:16px}
header img{height:56px;width:auto;border-radius:4px}
.org{font-size:13px;color:var(--muted);letter-spacing:.02em}
h1{font-size:26px;margin:6px 0 2px;color:var(--navy);line-height:1.2}
h2{font-size:17px;margin:34px 0 10px;color:var(--navy);
   border-left:4px solid var(--or);padding-left:10px}
.meta{color:var(--muted);font-size:14px}
.bandeau{margin:18px 0;padding:10px 14px;border-radius:6px;background:var(--bad-bg);
  color:var(--bad-ink);font-weight:600;font-size:14px}
.note-box{display:flex;flex-wrap:wrap;gap:20px;align-items:center;margin:26px 0;
  padding:20px;border:1px solid var(--border);border-radius:10px;background:var(--surface)}
.note{font-size:52px;font-weight:800;line-height:1;color:var(--navy);letter-spacing:-.02em}
.note-lib{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
.score{font-size:15px;color:var(--muted)}
.ctrl{margin-left:auto;font-size:14px;font-weight:600;padding:6px 12px;border-radius:20px}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{width:100%;border-collapse:collapse;font-size:14px;min-width:520px}
th,td{padding:8px 10px;text-align:right;border-bottom:1px solid var(--border);white-space:nowrap}
th:first-child,td:first-child{text-align:left;white-space:normal}
thead th{background:var(--navy-soft);color:var(--navy);font-weight:700;font-size:13px;
  text-transform:uppercase;letter-spacing:.04em}
tbody tr:hover td{background:var(--surface)}
.cmt{display:block;font-size:12px;color:var(--muted);font-weight:400}
.badge{display:inline-block;padding:2px 9px;border-radius:20px;font-size:12px;font-weight:700}
.b-ok{background:var(--ok-bg);color:var(--ok-ink)}
.b-warn{background:var(--warn-bg);color:var(--warn-ink)}
.b-bad{background:var(--bad-bg);color:var(--bad-ink)}
.avert{margin-top:34px;padding:16px;border:1px solid var(--border);border-radius:8px;
  background:var(--surface);font-size:13px;color:var(--muted)}
.avert b{color:var(--ink)}
.avert ul{margin:8px 0 0;padding-left:20px}
footer{margin-top:30px;padding-top:14px;border-top:1px solid var(--border);
  font-size:12px;color:var(--muted)}
@media(max-width:600px){h1{font-size:21px}.note{font-size:42px}.wrap{padding:18px 14px 48px}}
"""


def badge(st):
    if st is None:
        return ""
    cls = "b-ok" if st == "OK" else "b-warn" if st == "Vigilance" else "b-bad"
    return f'<span class="badge {cls}">{html.escape(st)}</span>'


def construire_html(identite, res, anonyme=False, interne=False):
    labels = list(res.keys())
    dernier = labels[-1]
    r = res[dernier]
    e = html.escape
    nom = "CLIENT ANONYMISÉ" if anonyme else str(identite.get("client") or "—")

    logo_tag = ""
    if os.path.exists(LOGO):
        with open(LOGO, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        logo_tag = f'<img src="data:image/jpeg;base64,{b64}" alt="MDC">'

    ctrl_ok = all(res[l]["controles_ok"] for l in labels)
    ctrl_cls = "b-ok" if ctrl_ok else "b-bad"
    ctrl_txt = "Contrôles de cohérence : OK" if ctrl_ok else "CONTRÔLES EN ANOMALIE"

    out = [f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Diagnostic financier — {e(nom)}</title>
<style>{CSS}</style></head><body><div class="wrap">
<header>{logo_tag}<div>
<div class="org">LA MAISON DE LA CONFORMITÉ — Diagnostic, mise en conformité et défense en contrôle</div>
<h1>Diagnostic financier — {e(nom)}</h1>
<div class="meta">{e(str(identite.get('secteur') or ''))} &middot; exercice {e(str(identite.get('exercice') or ''))}
 &middot; établi le {datetime.date.today().strftime('%d/%m/%Y')}</div>
</div></header>"""]

    if interne:
        out.append('<div class="bandeau">DOCUMENT INTERNE — NE PAS DIFFUSER SANS ACCORD ÉCRIT DU CLIENT</div>')
    if not ctrl_ok:
        out.append('<div class="bandeau">Les contrôles de cohérence du bilan ne sont pas satisfaits : '
                   'les indicateurs ci-dessous ne doivent pas être exploités en l\'état.</div>')
    if not r["evaluable"]:
        out.append('<div class="bandeau">Chiffre d\'affaires nul sur le dernier exercice : saisie '
                   'incomplète ou entité sans activité. Aucune note n\'est prononcée.</div>')

    out.append(f"""<div class="note-box">
<div><div class="note-lib">Note de conformité financière</div>
<div class="note">{e(r['note_mdc'])}</div>
<div class="score">{r['score_mdc']:.1f} / 100 &middot; score Z&#8243; {r['z']:.2f} — {e(r['zone_z'])}</div></div>
<div class="ctrl badge {ctrl_cls}">{e(ctrl_txt)}</div></div>""")

    # chiffres clés
    out.append("<h2>Chiffres clés</h2><div class='tw'><table><thead><tr><th>En FCFA</th>"
               + "".join(f"<th>{e(l)}</th>" for l in labels) + "</tr></thead><tbody>")
    for cle, lib in CHIFFRES:
        cells = "".join(f"<td>{fmt(res[l][cle], 'f')}</td>" for l in labels)
        out.append(f"<tr><td>{e(lib)}</td>{cells}</tr>")
    out.append("</tbody></table></div>")

    # les 5 étapes
    for titre, lignes in BLOCS:
        out.append(f"<h2>{e(titre)}</h2><div class='tw'><table><thead><tr><th>Indicateur</th>"
                   + "".join(f"<th>{e(l)}</th>" for l in labels)
                   + "<th>Lecture</th></tr></thead><tbody>")
        for cle, lib, kind, cmt in lignes:
            cells = "".join(f"<td>{fmt(res[l].get(cle), kind)}</td>" for l in labels)
            st = statut(cle, r.get(cle))
            c = f'<span class="cmt">{e(cmt)}</span>' if cmt else ""
            out.append(f"<tr><td>{e(lib)}{c}</td>{cells}<td>{badge(st)}</td></tr>")
        out.append("</tbody></table></div>")

    # détail de la note
    out.append("<h2>Détail de la note</h2><div class='tw'><table><thead><tr><th>Critère</th>"
               "<th>Poids</th><th>Seuil bon</th><th>Seuil moyen</th><th>Valeur</th>"
               "<th>Note</th><th>Contribution</th></tr></thead><tbody>")
    for d in r["note_detail"]:
        k = d["format"]
        out.append(
            f"<tr><td>{e(d['libelle'])}</td><td>{d['poids']*100:.0f} %</td>"
            f"<td>{fmt(d['seuil_bon'], k)}</td><td>{fmt(d['seuil_moyen'], k)}</td>"
            f"<td>{fmt(d['valeur'], k)}</td><td>{d['note']:.0f}</td>"
            f"<td>{d['contribution']:.1f}</td></tr>")
    out.append(f"<tr><td><b>Total</b></td><td colspan='5'></td>"
               f"<td><b>{r['score_mdc']:.1f}</b></td></tr></tbody></table></div>")

    out.append("""<div class="avert"><b>Portée et limites de ce document.</b>
<ul>
<li>Ce diagnostic porte sur la <b>santé financière</b>. Il ne se substitue pas à la note de conformité
administrative (comptable, fiscale, sociale) et ne vaut ni certification ni audit légal des comptes.</li>
<li>Il est établi à partir des <b>documents remis par le client</b>, non audités sauf mention contraire.</li>
<li>Le score Z&#8243; d'Altman est calibré sur des échantillons étrangers : il sert de <b>classement
ordinal</b>, non de probabilité de défaillance.</li>
<li>Les pondérations et seuils de la note MDC sont fixés à dire d'expert et révisés périodiquement.</li>
<li>Aucun élément de ce document ne constitue un conseil en investissement.</li>
</ul></div>""")

    out.append(f'<footer>{e(IDENTITE_MDC)}<br>Montants en francs CFA. '
               f'Document généré automatiquement — toute reprise partielle doit conserver les réserves '
               f'ci-dessus.</footer></div></body></html>')
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Exporte le diagnostic financier en fiche web autonome.")
    ap.add_argument("classeur")
    ap.add_argument("--out", required=True, help="fichier .html de sortie")
    ap.add_argument("--json", dest="json_out", help="fichier .json de sortie (facultatif)")
    ap.add_argument("--anonyme", action="store_true")
    ap.add_argument("--interne", action="store_true")
    a = ap.parse_args()

    identite, exercices, params = lire_classeur(a.classeur)
    res = calculer_serie(exercices, params)

    if not all(v["controles_ok"] for v in res.values()):
        print("AVERTISSEMENT : contrôles de cohérence en anomalie — la fiche portera un bandeau d'alerte.")

    html_txt = construire_html(identite, res, a.anonyme, a.interne)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(html_txt)
    print(f"Fiche web : {a.out}  ({len(html_txt)/1024:.0f} Ko, autonome)")

    if a.json_out:
        payload = {
            "identite": {k: (v if not a.anonyme or k != "client" else "CLIENT ANONYMISÉ")
                         for k, v in identite.items()},
            "parametres": params,
            "exercices": {lab: {k: v for k, v in r.items() if not isinstance(v, list)}
                          for lab, r in res.items()},
            "note_detail": res[list(res)[-1]]["note_detail"],
            "genere_le": datetime.date.today().isoformat(),
        }
        with open(a.json_out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Données JSON : {a.json_out}")


if __name__ == "__main__":
    main()
