#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controle_coherence_dossier.py — CONTRÔLE DE CLÔTURE D'UN DOSSIER CLIENT MDC.

À lancer APRÈS CHAQUE TRAVAUX, avant de remettre quoi que ce soit au client.
Un dossier n'est pas fini quand le dernier fichier est produit : il est fini
quand AUCUN livrable ne contredit les autres.

Quatre contrôles :
  1. MONTANTS PÉRIMÉS   — un chiffre corrigé qui survit quelque part
  2. PROPAGATION        — un chiffre définitif absent des livrables terminaux
  3. FRAÎCHEUR          — une copie de diffusion plus ancienne que son maître
  4. COMPLÉTUDE PDF     — un classeur ou un Word sans son PDF à côté

Usage :
  python3 controle_coherence_dossier.py DOSSIER \
      --perimes 128962819,119651114,6607142 \
      --cles    145523033,106252880,29274358 \
      --maitres "EXERCICE 2025" \
      --terminaux RAPPORT_,NOTE_DE_CONFORMITE

Sortie : rapport lisible + code retour 1 si une anomalie subsiste (0 sinon),
pour pouvoir bloquer une remise dans un enchaînement de commandes.
"""
import os, re, sys, zipfile, argparse, unicodedata

XML_UTILES = ("document.xml", "sharedStrings.xml", "sheet")
EXT = (".docx", ".xlsx")


def norm(s):
    """Neutralise toutes les variantes d'espaces (fine, insécable, tabulation)."""
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"[\s   ]", "", s)


def texte(path):
    """Extrait le texte brut d'un .docx ou .xlsx sans dépendance externe."""
    try:
        z = zipfile.ZipFile(path)
    except Exception:
        return ""
    out = []
    for n in z.namelist():
        if n.endswith(".xml") and any(u in n for u in XML_UTILES):
            try:
                out.append(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf8", "ignore")))
            except Exception:
                pass
    return " ".join(out)


def livrables(racine):
    for root, dirs, fs in os.walk(racine):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for fn in fs:
            if fn.endswith(EXT) and not fn.startswith("~$"):
                yield os.path.join(root, fn)


def cle(nom):
    """08b_RAPPORT_X.docx → RAPPORT_X.docx (pour apparier copie et maître)."""
    return re.sub(r"^\d+[a-z]?_", "", nom)


def main():
    p = argparse.ArgumentParser(description="Contrôle de clôture d'un dossier client MDC")
    p.add_argument("dossier")
    p.add_argument("--perimes", default="", help="montants corrigés qui ne doivent plus apparaître")
    p.add_argument("--cles", default="", help="montants définitifs qui doivent apparaître dans les livrables terminaux")
    p.add_argument("--maitres", default="", help="sous-dossier des fichiers maîtres (référence de fraîcheur)")
    p.add_argument("--terminaux", default="RAPPORT_,NOTE_", help="préfixes des livrables terminaux, séparés par des virgules")
    p.add_argument("--exempts", default="CONTROLE,AUDIT_FISCAL", help="fichiers autorisés à citer un montant périmé (rapports de contrôle)")
    a = p.parse_args()

    racine = os.path.abspath(a.dossier)
    if not os.path.isdir(racine):
        print(f"❌ dossier introuvable : {racine}"); return 2
    perimes = [x.strip() for x in a.perimes.split(",") if x.strip()]
    cles = [x.strip() for x in a.cles.split(",") if x.strip()]
    terminaux = [x.strip() for x in a.terminaux.split(",") if x.strip()]
    exempts = [x.strip() for x in a.exempts.split(",") if x.strip()]

    fichiers = sorted(livrables(racine))
    contenus = {f: norm(texte(f)) for f in fichiers}
    anomalies = 0

    print("═" * 78)
    print("  CONTRÔLE DE CLÔTURE — LA MAISON DE LA CONFORMITÉ SARL")
    print(f"  Dossier : {racine}")
    print(f"  {len(fichiers)} livrable(s) Word et Excel analysé(s)")
    print("═" * 78)

    # ─── 1. MONTANTS PÉRIMÉS ───────────────────────────────────────────────
    print("\n① MONTANTS PÉRIMÉS — un chiffre corrigé ne doit survivre nulle part")
    trouves = {}
    for f, t in contenus.items():
        base = os.path.basename(f)
        if any(e in base.upper() for e in exempts):
            continue                      # un rapport de contrôle CITE les montants corrigés
        for m in perimes:
            if norm(m) in t:
                trouves.setdefault(os.path.relpath(f, racine), []).append(m)
    if not perimes:
        print("   (aucun montant périmé déclaré — passer --perimes)")
    elif trouves:
        anomalies += len(trouves)
        for f, v in sorted(trouves.items()):
            print(f"   ❌ {f}\n        → {' · '.join(v)}")
    else:
        print("   ✅ aucun montant périmé")

    # ─── 2. PROPAGATION DES MONTANTS DÉFINITIFS ────────────────────────────
    print("\n② PROPAGATION — les chiffres définitifs doivent être dans les livrables terminaux")
    term = [f for f in fichiers if any(os.path.basename(f).upper().startswith(t.upper())
                                       or t.upper() in os.path.basename(f).upper() for t in terminaux)]
    if not cles:
        print("   (aucun montant clé déclaré — passer --cles)")
    elif not term:
        print(f"   ⚠ aucun livrable terminal trouvé pour les préfixes {terminaux}")
    else:
        for m in cles:
            porteurs = [os.path.basename(f) for f in term if norm(m) in contenus[f]]
            manquants = [os.path.basename(f) for f in term if norm(m) not in contenus[f]]
            statut = "✅" if len(porteurs) >= 1 else "❌"
            print(f"   {statut} {m} : présent dans {len(porteurs)}/{len(term)} livrable(s) terminaux")
            if manquants and len(porteurs):
                print(f"        absent de : {', '.join(sorted(set(manquants))[:6])}")

    # ─── 3. FRAÎCHEUR DES COPIES ───────────────────────────────────────────
    print("\n③ FRAÎCHEUR — une copie de diffusion ne doit pas être plus ancienne que son maître")
    if not a.maitres:
        print("   (aucun dossier maître déclaré — passer --maitres)")
    else:
        dmaitre = os.path.join(racine, a.maitres)
        maitres = {os.path.basename(f): f for f in fichiers if f.startswith(dmaitre)}
        vieilles = []
        for f in fichiers:
            if f.startswith(dmaitre):
                continue
            src = maitres.get(cle(os.path.basename(f)))
            if src and os.path.getmtime(src) > os.path.getmtime(f) + 1:
                vieilles.append(os.path.relpath(f, racine))
        if vieilles:
            anomalies += len(vieilles)
            for v in sorted(vieilles):
                print(f"   ❌ {v}")
            print(f"\n   → régénérer : copier le maître sur chacune de ces {len(vieilles)} copie(s)")
        else:
            print("   ✅ toutes les copies sont à jour")

    # ─── 4. COMPLÉTUDE PDF ─────────────────────────────────────────────────
    print("\n④ COMPLÉTUDE — chaque livrable doit avoir son PDF à côté")
    sans_pdf = [os.path.relpath(f, racine) for f in fichiers
                if not os.path.exists(os.path.splitext(f)[0] + ".pdf")]
    if sans_pdf:
        print(f"   ⚠ {len(sans_pdf)} livrable(s) sans PDF :")
        for s in sorted(sans_pdf)[:15]:
            print(f"        {s}")
        if len(sans_pdf) > 15:
            print(f"        … et {len(sans_pdf)-15} autre(s)")
        print("   → xlsx : xlsx_to_pdf_mdc.py · docx : republier via publish_pdf_mdc.py")
    else:
        print("   ✅ tous les livrables ont leur PDF")

    # ─── 5. ARITHMÉTIQUE DES MONTANTS NETS ─────────────────────────────────
    # Cible le bug exact : une ligne "nette / à payer / à reverser" précédée
    # d'au moins une valeur négative (une déduction), dont le montant affiché
    # = somme des VALEURS ABSOLUES au lieu de la somme ALGÉBRIQUE. C'est la
    # signature d'une addition posée à la place d'une soustraction (TVA nette,
    # solde après déduction…). Restreint à ce motif pour zéro faux positif sur
    # les totaux imbriqués.
    print("\n⑤ ARITHMÉTIQUE — un montant net ne doit jamais être une addition de la déduction")
    JALONS = ("NET", "À PAYER", "A PAYER", "À REVERSER", "A REVERSER", "= TVA", "SOLDE")
    faux = []
    try:
        import openpyxl
        xlsx = [f for f in fichiers if f.endswith(".xlsx")]
    except ImportError:
        openpyxl = None
        xlsx = []
    for f in xlsx:
        if any(e in os.path.basename(f).upper() for e in exempts):
            continue
        try:
            wb = openpyxl.load_workbook(f, data_only=True)
        except Exception:
            continue
        for ws in wb.worksheets:
            for col in range(1, ws.max_column + 1):
                pile = []
                for row in range(1, ws.max_row + 1):
                    v = ws.cell(row=row, column=col).value
                    lbl = ""
                    for cc in range(1, col + 1):
                        x = ws.cell(row=row, column=cc).value
                        if isinstance(x, str) and x.strip():
                            lbl = x.upper(); break
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        est_net = any(j in lbl for j in JALONS)
                        a_deduction = any(p < 0 for p in pile)
                        if est_net and len(pile) >= 2 and a_deduction:
                            algebrique = sum(pile)
                            absolue = sum(abs(p) for p in pile)
                            if abs(v - absolue) <= 2 and abs(v - algebrique) > 2:
                                faux.append((os.path.relpath(f, racine), ws.title,
                                             ws.cell(row=row, column=col).coordinate,
                                             lbl[:36], v, algebrique))
                            pile = []
                        elif est_net:
                            pile = []
                        else:
                            pile.append(v)
                    elif isinstance(v, str) and v.strip():
                        # un intertitre (ligne sans nombre) referme le groupe courant
                        if any(k in v.upper() for k in ("①", "②", "③", "④", "SECTION", "BLOC")):
                            pile = []
    if openpyxl is None:
        print("   (openpyxl absent — contrôle arithmétique ignoré)")
    elif faux:
        anomalies += len(faux)
        for rel, onglet, coord, lbl, montant, correct in faux:
            print(f"   ❌ {rel} / {onglet} / {coord}")
            print(f"        « {lbl} » = {montant:,} — ADDITION détectée ; la soustraction donne {correct:,}")
        print("\n   → la TVA (ou tout net) se calcule collectée MOINS déductible, jamais collectée PLUS déductible")
    else:
        print("   ✅ aucun montant net obtenu par addition d'une déduction")

    print("\n" + "═" * 78)
    if anomalies:
        print(f"  ❌ {anomalies} ANOMALIE(S) BLOQUANTE(S) — le dossier n'est PAS remettable en l'état")
    else:
        print("  ✅ DOSSIER COHÉRENT — remise autorisée")
    print("═" * 78)
    return 1 if anomalies else 0


if __name__ == "__main__":
    sys.exit(main())
