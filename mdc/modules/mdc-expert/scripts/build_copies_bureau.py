#!/usr/bin/env python3
import os, shutil, re
from datetime import datetime

ROOTS = [
    ("/Users/bilefilsseverin/Documents/DOSSIER CLIENTS", ""),
    ("/Users/bilefilsseverin/Desktop/MON JURISTE", "MON JURISTE"),
]
DEST = "/Users/bilefilsseverin/Desktop/00_COPIES DOCUMENTS GENERES"
EXTS = {".pdf", ".docx", ".xlsx", ".md", ".pptx"}

GEN_PREFIXES = (
    "NOTE_", "NOTE MÉTHODOLOGIQUE", "NOTE METHODOLOGIQUE", "NOTE MÉTHODO", "NOTE METHODO",
    "PROPOSITION_", "PROPOSITION FINANCIERE", "PROPOSITION FINANCIÈRE", "PROPOSITION COMMERCIALE",
    "CONTRAT_", "COURRIEL_", "COURRIER_", "RAPPORT_", "RAPPORT ", "ANALYSE_",
    "RECONSTITUTION_", "COMPTABILITE_", "COMPTABILITÉ_", "SYNTHESE_", "SYNTHÈSE_",
    "ETAT_RAPPROCHEMENT", "ETUDE_", "BORDEREAUX_", "BORDEREAU_", "POINT_DECLARATIONS",
    "POINT_PROVISOIRE", "DETAIL_CA", "DETAIL_TVA", "ANNEXES_EDI", "MANUEL_", "CADRE_",
    "PROCEDURE_", "VISA_", "CHECKLIST_", "DIAGNOSTIC_", "DIAGNOSTIC ", "LIASSE_",
    "ORDRE_MISSION", "ORDRE MISSION", "DOSSIER_AUDIT", "DOSSIER_PREUVES",
    "Rapport_", "Dossier_", "Analyse_", "Synthese_", "Synthèse_", "Etude_",
    "Decomposition_", "Sorties_", "Cours_", "Note_", "Etat_", "MC-",
)
GEN_CONTAINS = ("_MDC", "MDC_", " MDC", "_MDLC", "MDLC_")

def keep(name, ext, stem_has_md):
    if name.startswith("OBSOLETE"):
        return False
    if ext == ".md":
        return True
    if name.startswith(GEN_PREFIXES):
        return True
    if any(tok in name for tok in GEN_CONTAINS):
        return True
    if stem_has_md:
        return True
    return False

if os.path.isdir(DEST):
    shutil.rmtree(DEST, ignore_errors=True)
os.makedirs(DEST, exist_ok=True)

copied = []  # (client, relpath, mtime)
for root, prefix_in_dest in ROOTS:
    if not os.path.isdir(root):
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        names = set(filenames)
        for fn in filenames:
            stem, ext = os.path.splitext(fn)
            ext = ext.lower()
            if ext not in EXTS:
                continue
            stem_has_md = (stem + ".md") in names or (stem + ".MD") in names
            if not keep(fn, ext, stem_has_md):
                continue
            src = os.path.join(dirpath, fn)
            rel = os.path.relpath(src, root)
            rel = os.path.join(prefix_in_dest, rel) if prefix_in_dest else rel
            dst = os.path.join(DEST, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                shutil.copy2(src, dst)
                top = rel.split(os.sep)[0]
                mt = datetime.fromtimestamp(os.path.getmtime(src)).strftime("%Y-%m-%d")
                copied.append((top, rel, mt))
            except Exception as e:
                print("ERR", src, e)

# Manifest
copied.sort()
byclient = {}
for top, rel, mt in copied:
    byclient.setdefault(top, []).append((rel, mt))

lines = []
lines.append("# COPIES DES DOCUMENTS GÉNÉRÉS — LA MAISON DE LA CONFORMITÉ")
lines.append("")
lines.append(f"Copie générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}. "
             f"{len(copied)} fichiers, {len(byclient)} dossiers.")
lines.append("")
lines.append("Contenu = documents produits par nos soins (sources .md + versions PDF/Word/Excel brandées). "
             "Les pièces fournies par les clients (relevés, quittances, liasses, scans) sont volontairement exclues.")
lines.append("")
for client in sorted(byclient):
    lines.append(f"## {client}  ({len(byclient[client])} fichiers)")
    for rel, mt in byclient[client]:
        lines.append(f"- {rel}  ·  {mt}")
    lines.append("")
with open(os.path.join(DEST, "MANIFEST.md"), "w") as f:
    f.write("\n".join(lines))

print(f"TOTAL fichiers copiés : {len(copied)}")
print(f"Dossiers : {len(byclient)}")
print("--- Récap par dossier ---")
for client in sorted(byclient):
    print(f"{len(byclient[client]):3d}  {client}")
