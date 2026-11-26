"""Lit une conversation WhatsApp EXPORTÉE (Discussion › Exporter la discussion › Sans médias, fichier .txt
ou .zip) et la rend exploitable : un message par ligne (date, heure, auteur, texte), messages sur plusieurs
lignes recollés, pièces jointes signalées.

    python3 lire_whatsapp.py EXPORT.txt|EXPORT.zip [--depuis 2026-11-20] [--auteur "Awa"] [--csv sortie.csv]

Formats reconnus : Android « 26/11/2026 08:12 - Nom : texte » et iPhone / Mac « [26/11/2026 08:12:33] Nom: texte ».
Sert au point global : on lit ce que chaque collaborateur a envoyé, puis on le transcrit dans la grille
(grille.py) sans rien inventer.
"""
import argparse
import csv
import datetime as dt
import io
import re
import sys
import zipfile

MOTIFS = [
    re.compile(r"^‎?\[(\d{1,2})/(\d{1,2})/(\d{2,4}),? (\d{1,2}):(\d{2})(?::\d{2})?\]\s*([^:]+?):\s?(.*)$"),
    re.compile(r"^‎?(\d{1,2})/(\d{1,2})/(\d{2,4}),? (\d{1,2}):(\d{2})\s*[-–]\s*([^:]+?)\s?:\s?(.*)$"),
]
PJ = re.compile(r"(<pièce jointe|<attached|\.(pdf|xlsx?|docx?|jpg|jpeg|png|opus) \(fichier joint\)|fichier joint|omis|omitted)", re.I)


def lire_texte(chemin):
    if chemin.lower().endswith(".zip"):
        with zipfile.ZipFile(chemin) as z:
            nom = next((n for n in z.namelist() if n.lower().endswith(".txt")), None)
            if not nom:
                raise SystemExit("Aucun fichier .txt dans l'archive.")
            return z.read(nom).decode("utf-8-sig", errors="replace")
    with open(chemin, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def messages(texte):
    out = []
    for ligne in texte.splitlines():
        m = next((x.match(ligne) for x in MOTIFS if x.match(ligne)), None)
        if m:
            j, mo, a, h, mi, auteur, corps = m.groups()
            a = int(a) + (2000 if len(a) == 2 else 0)
            try:
                quand = dt.datetime(a, int(mo), int(j), int(h), int(mi))
            except ValueError:
                quand = None
            out.append({"quand": quand, "auteur": auteur.strip().strip("‎~ "), "texte": corps.strip(), "piece_jointe": bool(PJ.search(corps))})
        elif out and ligne.strip():
            out[-1]["texte"] += "\n" + ligne.strip()
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("export")
    p.add_argument("--depuis", default=None)
    p.add_argument("--auteur", default=None)
    p.add_argument("--csv", default=None)
    a = p.parse_args()
    l = messages(lire_texte(a.export))
    if a.depuis:
        d = dt.datetime.fromisoformat(a.depuis)
        l = [m for m in l if m["quand"] and m["quand"] >= d]
    if a.auteur:
        l = [m for m in l if a.auteur.lower() in m["auteur"].lower()]
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["date", "heure", "auteur", "piece_jointe", "texte"])
            for m in l:
                w.writerow([m["quand"].date().isoformat() if m["quand"] else "", m["quand"].strftime("%H:%M") if m["quand"] else "", m["auteur"], "oui" if m["piece_jointe"] else "", m["texte"]])
    out = io.StringIO()
    for m in l:
        out.write(f"[{m['quand']:%d/%m/%Y %H:%M}] {m['auteur']}{' (pièce jointe)' if m['piece_jointe'] else ''} : {m['texte']}\n" if m["quand"] else f"[?] {m['auteur']} : {m['texte']}\n")
    sys.stdout.write(out.getvalue())
    sys.stderr.write(f"{len(l)} message(s)\n")
