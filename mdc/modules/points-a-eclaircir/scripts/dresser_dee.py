#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dresser_dee.py — GÉNÉRATEUR DE DEE GLOBALE (skill points-a-eclaircir, MDC).

Transforme un fichier de configuration JSON (points à éclaircir) en « Document des points à
éclaircir » (DEE globale) au format Markdown, puis — avec --publish — en Word + PDF brandés MDC via
le pipeline règle d'or (contrôle qualité bloquant).

Usage :
  python3 dresser_dee.py points.json --out DEE.md
  python3 dresser_dee.py points.json --out DEE.md --publish        # + DOCX + PDF (règle d'or)

Schéma JSON attendu : voir reference/points_config.example.json.
Chaque section est soit un TABLEAU (colonnes + lignes + total + note),
soit une section EXPOSITION ("type":"exposition", colonnes + scenarios).
"""
import sys, json, argparse, subprocess, os

PIPE = os.path.expanduser("~/.claude/skills/mdc-expert/scripts")


def esc(x): return "" if x is None else str(x)


def render(cfg):
    L = []
    L.append("# DOCUMENT DES POINTS À ÉCLAIRCIR — DEMANDE D'EXPLICATION ÉCRITE (DEE)\n")
    ref = esc(cfg.get("reference", "MC-DEE-[SECT]-[AN]-NNN"))
    rempl = esc(cfg.get("remplace", ""))
    ligne_ref = f"**Référence :** {ref}"
    if rempl: ligne_ref += f" *(consolide et remplace {rempl})*"
    L.append(ligne_ref)
    L.append(f"**À l'attention de** {esc(cfg.get('destinataire', 'Monsieur le Gérant'))}")
    L.append(f"**Objet :** {esc(cfg.get('objet',''))}\n")
    L.append("Monsieur le Gérant,\n")
    L.append(esc(cfg.get("preambule",
        "Dans le cadre de la finalisation de votre comptabilité, l'analyse du relevé bancaire et le "
        "croisement avec vos pièces font apparaître un ensemble d'éléments que nous ne pouvons pas "
        "traiter définitivement sans vos explications.")) + "\n")
    L.append("> **Notre méthode, et notre engagement de prudence.** Tant que ces éléments ne sont pas "
             "justifiés, nous ne passons **AUCUNE écriture qui préjugerait de leur nature**. Ces flux "
             "sont provisoirement inscrits en **comptes d'attente** (ni produit, ni charge, ni compte "
             "courant). Ce n'est **qu'après vos éclaircissements** que chaque élément sera **qualifié et "
             "comptabilisé** dans le bon compte.\n")
    L.append("Nous vous prions de répondre **par écrit**, pièces à l'appui, aux points ci-après.\n")
    L.append("---\n")

    for i, sec in enumerate(cfg.get("sections", []), 1):
        L.append(f"## {i}. {esc(sec.get('titre',''))}\n")
        if sec.get("intro"): L.append(esc(sec["intro"]) + "\n")
        cols = sec.get("colonnes")
        if sec.get("type") == "exposition":
            rows = sec.get("scenarios", [])
        else:
            rows = sec.get("lignes", [])
        if cols and rows:
            L.append("| " + " | ".join(esc(c) for c in cols) + " |")
            L.append("|" + "|".join(["---"] * len(cols)) + "|")
            for r in rows:
                L.append("| " + " | ".join(esc(c) for c in r) + " |")
            if sec.get("total"):
                L.append("| " + " | ".join(f"**{esc(c)}**" if c else "" for c in sec["total"]) + " |")
            L.append("")
        if sec.get("note"):
            L.append(f"> {esc(sec['note'])}\n")
        # demandes explicites d'une section exposition
        if sec.get("demandes"):
            L.append("**Nos demandes :** " + esc(sec["demandes"]) + "\n")
        L.append("---\n")

    L.append(f"## {len(cfg.get('sections', [])) + 1}. Conséquence\n")
    L.append("Tant que ces éléments ne sont pas justifiés par des pièces, **la base comptable ne peut "
             "être arrêtée définitivement** : les flux concernés demeurent en **comptes d'attente**, et "
             "**aucune écriture qualificative n'est passée**. Dès réception de vos explications, chaque "
             "point sera **traité et comptabilisé définitivement**, et l'éventuelle exposition fiscale "
             "sera régularisée.\n")
    L.append(f"Nous vous remercions de nous répondre **par écrit, au plus tard le "
             f"{esc(cfg.get('echeance','[JJ/MM/AAAA]'))}**, en joignant les justificatifs.\n")
    L.append("Nous restons à votre disposition pour tout échange.\n")
    L.append("<br>\nVeuillez agréer, Monsieur le Gérant, l'expression de notre considération "
             "distinguée.\n<br><br>\nPour LA MAISON DE LA CONFORMITÉ SARL\n<br>\nBILE Fils Séverin — Gérant")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config", help="fichier JSON des points")
    ap.add_argument("--out", default="POINTS_A_ECLAIRCIR.md")
    ap.add_argument("--publish", action="store_true", help="produire aussi DOCX + PDF (règle d'or)")
    a = ap.parse_args()

    with open(a.config, encoding="utf-8") as f:
        cfg = json.load(f)
    md = render(cfg)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ DEE Markdown : {a.out}  ({len(cfg.get('sections', []))} sections)")

    if a.publish:
        titre = "Document des points à éclaircir (DEE globale)"
        client = cfg.get("client", "[CLIENT]")
        ref = cfg.get("reference", "MC-DEE")
        base = os.path.splitext(a.out)[0]
        for script, dest in ((f"{PIPE}/publish_livrable_mdc.py", base + ".docx"),
                             (f"{PIPE}/publish_pdf_mdc.py", base + ".pdf")):
            if not os.path.exists(script):
                print(f"   ⚠ pipeline introuvable : {script} — étape sautée"); continue
            r = subprocess.run(["python3", script, a.out, dest, titre, client, ref],
                               capture_output=True, text=True)
            ok = "PUBLISH_OK" in (r.stdout + r.stderr)
            print(("   ✅ " if ok else "   ❌ ") + os.path.basename(dest) +
                  ("" if ok else "  → " + (r.stdout + r.stderr).strip().split(chr(10))[-1][:120]))


if __name__ == "__main__":
    main()
