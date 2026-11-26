# -*- coding: utf-8 -*-
"""Publie les livrables du dossier d'audit : chaque source .md en PDF et en Word brandes.

Refuse de publier une source qui porte encore une consigne « A REDIGER » : un squelette
n'est pas un livrable. Archive la version precedente avant d'ecrire la nouvelle.

  python3 publier_dossier_audit.py "<dossier d'audit>" [--un NOM_DU_FICHIER] [--forcer]
"""
import os, re, sys, shutil, subprocess, datetime

GEN = os.path.expanduser("~/.claude/skills/mdc/modules/mdc-expert/scripts")
PDF = os.path.join(GEN, "publish_pdf_mdc.py")
DOCX = os.path.join(GEN, "publish_livrable_mdc.py")

TITRES = {
    "SYNTHESE_DE_L_EXPOSITION": "SYNTHÈSE DE L'EXPOSITION",
    "TABLEAU_D_EXPOSITION": "TABLEAU D'EXPOSITION",
    "RAPPORT_AUDIT_CONFORMITE": "RAPPORT D'AUDIT DE CONFORMITÉ",
    "AUDIT_DOCUMENTAIRE": "AUDIT DOCUMENTAIRE",
    "GRILLE_DES_DECLARATIONS": "GRILLE DES DÉCLARATIONS",
    "AUDIT_DES_PROCEDURES": "AUDIT DES PROCÉDURES INTERNES ET EXTERNES",
    "NOTE_DE_CHIFFRAGE_DES_EXPOSITIONS": "NOTE DE CHIFFRAGE DES EXPOSITIONS",
    "CONSTAT_DE_NON_CONFORMITE": "CONSTAT DE NON-CONFORMITÉ",
    "PLAN_D_ACTION": "PLAN D'ACTION",
    "NOTE_AU_COMPTABLE": "NOTE AU COMPTABLE",
    "LE_POINT_ET_LES_BONS_USAGES": "LE POINT ET LES BONS USAGES",
    "MODELES_ACTES_JURIDIQUES": "MODÈLES D'ACTES JURIDIQUES",
    "SCRIPT_DE_RESTITUTION": "SCRIPT DE RESTITUTION",
    "SOMMAIRE_DU_DOSSIER": "SOMMAIRE DU DOSSIER",
    "BORDEREAU_DE_TRANSMISSION": "BORDEREAU DE TRANSMISSION",
    "CARTOGRAPHIE_DES_DESTINATAIRES": "CARTOGRAPHIE DES DESTINATAIRES",
}


def entetes(texte):
    cl = re.search(r"^Client\s*:\s*(.+)$", texte, re.M)
    rf = re.search(r"^Référence\s*:\s*([A-Z0-9\-]+)", texte, re.M)
    return (cl.group(1).split("—")[0].strip() if cl else ""), (rf.group(1) if rf else "")


def titre(nom):
    for cle, t in TITRES.items():
        if nom.startswith(cle):
            return t
    return nom.replace("_", " ")


def publier(src, dest_dir, forcer=False):
    nom = os.path.basename(src)[:-3]
    texte = open(src, encoding="utf-8").read()
    if "À RÉDIGER" in texte and not forcer:
        return nom, "REFUSÉ", "le document porte encore des consignes à rédiger"
    client, ref = entetes(texte)
    jour = datetime.date.today().isoformat()
    base = os.path.join(dest_dir, "%s_%s" % (nom, jour))
    arch = os.path.join(dest_dir, "_OBSOLETE", "VERSIONS_MODIFIEES")
    for ext, outil in ((".pdf", PDF), (".docx", DOCX)):
        cible = base + ext
        if os.path.exists(cible):
            os.makedirs(arch, exist_ok=True)
            h = datetime.datetime.now().strftime("%Hh%M%S")
            shutil.copy2(cible, os.path.join(arch, "%s_%s_AVANT_%s_%s%s" % (nom, jour, jour, h, ext)))
        r = subprocess.run([sys.executable, outil, src, cible, titre(nom), client, ref],
                           capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(cible):
            return nom, "ÉCHEC", (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "contrôle qualité non passé"
    return nom, "PUBLIÉ", os.path.basename(base) + ".pdf + .docx"


def main():
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    dest = a[0]
    src_dir = os.path.join(dest, "_SOURCES_MD")
    un = a[a.index("--un") + 1] if "--un" in a else None
    forcer = "--forcer" in a
    sources = sorted(f for f in os.listdir(src_dir) if f.endswith(".md"))
    if un:
        sources = [f for f in sources if un in f]
    n = {"PUBLIÉ": 0, "REFUSÉ": 0, "ÉCHEC": 0}
    for s in sources:
        nom, etat, dit = publier(os.path.join(src_dir, s), dest, forcer)
        n[etat] = n.get(etat, 0) + 1
        print("  [%s] %s — %s" % (etat, nom, dit))
    print("\n%d publié(s), %d refusé(s), %d en échec." % (n["PUBLIÉ"], n["REFUSÉ"], n["ÉCHEC"]))
    return 1 if n["ÉCHEC"] else 0


if __name__ == "__main__":
    sys.exit(main())
