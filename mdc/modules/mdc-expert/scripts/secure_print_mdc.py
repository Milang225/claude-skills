#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMPRESSION SÉCURISÉE MDC — produit des exemplaires NOMINATIFS et TRAÇABLES.

Ce que fait ce script, et ce qu'il ne fait pas.

FAIT   · un fond pantographe : à la photocopie ou au scan, le mot « COPIE » apparaît en clair
       · un filigrane nominatif sur chaque page : nom du porteur et numéro d'exemplaire
       · un pied de page de traçabilité : exemplaire, porteur, date, empreinte
       · un QR de vérification unique par exemplaire
       · un micro-marquage discret, qui survit à une photo partielle
       · un registre des exemplaires émis

NE FAIT PAS · empêcher un scan ou une photocopie : c'est impossible sur du papier
            · alerter automatiquement lors d'une photocopie : le papier ne communique pas
       L'alerte repose sur le QR : elle se déclenche quand quelqu'un le scanne.

Usage :
  python3 secure_print_mdc.py SOURCE.pdf --porteur "NOM Prénom" [--numero 7] [--total 12]
                              [--url https://…] [--sortie DEST.pdf] [--mot COPIE]
  python3 secure_print_mdc.py SOURCE.pdf --liste porteurs.txt --dossier SORTIE/
"""
import argparse, hashlib, os, sys, datetime, csv
import fitz  # PyMuPDF

NAVY = (0.10, 0.10, 0.18)
GRIS_TRAME = (0.45, 0.45, 0.52)     # encre de la trame de sécurité
# --- Dimensionnement du fond de sécurité (pantographe) ---
# Principe : le FOND est fait de hachures très fines (chaque trait est plus fin que ce
# qu'un scanner ou un copieur sait restituer : il s'efface). Le MESSAGE caché est fait de
# points épais, assez espacés pour que la densité d'encre — donc la teinte perçue — soit
# la même. À l'oeil, une page grise uniforme ; à la photocopie, le mot apparaît.
PAS_HACHURE = 1.2      # espacement des hachures du fond, en points PDF
EP_HACHURE = 0.12      # épaisseur d'un trait de fond (0,04 mm : sous le seuil du copieur)
PAS_POINT = 2.8        # grille des points du message
R_POINT = 0.50         # rayon des points du message (1 pt de diamètre : 0,35 mm)
# Couverture d'encre : hachures 0,12/1,2 = 10 % · points pi*0,25/2,8² = 10 %. Les deux
# trames sont donc de même teinte. Ces valeurs se calibrent sur le copieur : voir --calibrage.


def empreinte(source, porteur, numero, date_iso):
    h = hashlib.sha256(f"{os.path.basename(source)}|{porteur}|{numero}|{date_iso}|MDC".encode())
    d = h.hexdigest().upper()
    return f"{d[0:4]}-{d[4:8]}-{d[8:12]}"


def masque_du_mot(mot, largeur, hauteur, pas):
    """Le mot, rendu très gros et répété, sous forme de masque noir et blanc."""
    tmp = fitz.open()
    page = tmp.new_page(width=largeur, height=hauteur)
    taille = max(16, int(largeur / (len(mot) * 0.62)))
    pas_y = max(34, int(hauteur * 0.24))
    for k, y in enumerate(range(int(hauteur * 0.18), int(hauteur * 0.94), pas_y)):
        decalage = (k % 2) * largeur * 0.16
        page.insert_text((largeur * 0.03 + decalage, y), mot,
                         fontname="hebo", fontsize=taille, color=(0, 0, 0))
    pix = page.get_pixmap(matrix=fitz.Matrix(1.0 / pas, 1.0 / pas), colorspace=fitz.csGRAY)
    tmp.close()
    return pix


_CACHE_FOND = {}


def fond_pantographe(largeur, hauteur, mot, ep_hachure=EP_HACHURE, r_point=R_POINT,
                     pas_hachure=PAS_HACHURE, pas_point=PAS_POINT, gris=None):
    """Un PDF d'une page portant le fond de sécurité. Calculé une seule fois par document."""
    gris = gris or GRIS_TRAME
    cle = (round(largeur), round(hauteur), mot, ep_hachure, r_point, pas_hachure, pas_point)
    if cle in _CACHE_FOND:
        return _CACHE_FOND[cle]
    pix = masque_du_mot(mot, largeur, hauteur, pas_point)
    haut = min(118.0, hauteur * 0.06)          # ni sous le bandeau d'en-tête, ni sur le pied
    bas = hauteur - min(46.0, hauteur * 0.05)
    marge = min(26.0, largeur * 0.03)
    gauche, droite = marge, largeur - marge
    doc = fitz.open()
    page = doc.new_page(width=largeur, height=hauteur)

    def dans_le_mot(x, y):
        i, j = int(x / pas_point), int(y / pas_point)
        if 0 <= i < pix.width and 0 <= j < pix.height:
            return pix.pixel(i, j)[0] < 128
        return False

    # 1. les hachures du fond, interrompues là où le mot est caché
    trame = page.new_shape()
    y = haut
    while y <= bas:
        x = gauche
        while x < droite:
            x2 = min(x + pas_point, droite)
            if not dans_le_mot((x + x2) / 2, y):
                trame.draw_line(fitz.Point(x, y), fitz.Point(x2, y))
            x = x2
        y += pas_hachure
    trame.finish(color=gris, width=ep_hachure)
    trame.commit()

    # 2. les points du message caché
    pts = page.new_shape()
    j = 0
    y = haut
    while y <= bas:
        x = gauche + (pas_point / 2 if j % 2 else 0)
        while x < droite:
            if dans_le_mot(x, y):
                pts.draw_circle(fitz.Point(x, y), r_point)
            x += pas_point
        y += pas_point
        j += 1
    pts.finish(fill=gris, color=None)
    pts.commit()
    _CACHE_FOND[cle] = doc
    return doc


def qr_exemplaire(url):
    """QR de vérification, rendu dans un PDF d'une page de 60 x 60 points."""
    from reportlab.graphics.barcode import qr
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics import renderPDF
    from reportlab.pdfgen import canvas
    import io
    widget = qr.QrCodeWidget(url, barLevel='M')
    b = widget.getBounds()
    w, h = b[2] - b[0], b[3] - b[1]
    taille = 60.0
    d = Drawing(taille, taille, transform=[taille / w, 0, 0, taille / h, -b[0], -b[1]])
    d.add(widget)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(taille, taille))
    renderPDF.draw(d, c, 0, 0)
    c.save(); buf.seek(0)
    return fitz.open("pdf", buf.read())


def securiser(source, dest, porteur, numero, total, url_base, mot, date_iso,
              ep_hachure=EP_HACHURE, r_point=R_POINT):
    doc = fitz.open(source)
    emp = empreinte(source, porteur, numero, date_iso)
    code = f"{numero:03d}-{emp.replace('-', '')[:6]}"
    url = f"{url_base.rstrip('/')}/{code}" if url_base else f"MDC/{code}"
    panto = fond_pantographe(doc[0].rect.width, doc[0].rect.height, mot, ep_hachure, r_point)
    qr_doc = qr_exemplaire(url)
    libelle = (f"EXEMPLAIRE NOMINATIF n° {numero:03d}" + (f" / {total}" if total else "") +
               f"  ·  {porteur}  ·  {date_iso}  ·  empreinte {emp}  ·  "
               "reproduction et diffusion interdites  ·  document tracé")
    for page in doc:
        r = page.rect
        # 1. fond de sécurité, sous le texte
        page.show_pdf_page(r, panto, 0, overlay=False)
        # 2. filigrane nominatif, en diagonale
        page.insert_textbox(fitz.Rect(r.width * 0.06, r.height * 0.40, r.width * 0.94, r.height * 0.62),
                            f"{porteur}\nexemplaire n° {numero:03d}",
                            fontname="hebo", fontsize=26, color=(0.87, 0.87, 0.91),
                            align=fitz.TEXT_ALIGN_CENTER, rotate=0, overlay=True)
        # 3. bandeau de traçabilité
        page.draw_rect(fitz.Rect(28, r.height - 26, r.width - 28, r.height - 13),
                       color=None, fill=(0.97, 0.97, 0.99), overlay=True)
        page.insert_textbox(fitz.Rect(30, r.height - 25, r.width - 30, r.height - 14),
                            libelle, fontname="helv", fontsize=5.6, color=NAVY,
                            align=fitz.TEXT_ALIGN_CENTER, overlay=True)
        # 4. micro-marquage : survit à une photo partielle
        for y in (r.height * 0.24, r.height * 0.52, r.height * 0.80):
            page.insert_text((r.width - 34, y), f"{code}", fontname="helv", fontsize=3.4,
                             color=(0.74, 0.74, 0.78), rotate=90, overlay=True)
    # 5. QR de vérification sur la dernière page
    der = doc[-1]; r = der.rect
    der.show_pdf_page(fitz.Rect(r.width - 96, r.height - 96, r.width - 34, r.height - 34),
                      qr_doc, 0, overlay=True)
    der.insert_textbox(fitz.Rect(r.width - 150, r.height - 34, r.width - 28, r.height - 26),
                       "vérifier cet exemplaire", fontname="helv", fontsize=5.2,
                       color=NAVY, align=fitz.TEXT_ALIGN_RIGHT, overlay=True)
    doc.save(dest, deflate=True, garbage=3)
    doc.close(); qr_doc.close()
    return {"exemplaire": f"{numero:03d}", "porteur": porteur, "document": os.path.basename(source),
            "date": date_iso, "empreinte": emp, "code": code, "url": url, "fichier": os.path.basename(dest)}


def planche_calibrage(dest, mot="COPIE"):
    """Une page à photocopier : six réglages côte à côte, pour choisir celui qui marche
    sur le copieur de la maison. Le bon réglage est celui dont le pavé fait apparaître
    le mot le plus nettement sur la COPIE, tout en restant uni sur l'ORIGINAL."""
    reglages = [(0.10, 0.44), (0.12, 0.50), (0.14, 0.56),
                (0.16, 0.62), (0.18, 0.68), (0.22, 0.78)]
    doc = fitz.open(); page = doc.new_page(width=595, height=842)
    page.insert_textbox(fitz.Rect(40, 34, 555, 86),
                        "PLANCHE DE CALIBRAGE DU FOND DE SECURITE\n"
                        "Photocopier cette page, puis comparer : le bon réglage est celui dont le pavé "
                        "laisse apparaître le mot le plus nettement sur la copie, en restant uni sur l'original.",
                        fontname="hebo", fontsize=10.5, color=NAVY, align=fitz.TEXT_ALIGN_CENTER)
    larg, haut = 250, 214
    for k, (ep, rp) in enumerate(reglages):
        cx = 45 + (k % 2) * 265
        cy = 110 + (k // 2) * 232
        bloc = fond_pantographe(larg, haut + 6, mot, ep, rp, gris=GRIS_TRAME)
        page.show_pdf_page(fitz.Rect(cx, cy, cx + larg, cy + haut), bloc, 0, overlay=False)
        page.draw_rect(fitz.Rect(cx, cy, cx + larg, cy + haut), color=(0.75, 0.75, 0.8), width=0.5)
        page.insert_textbox(fitz.Rect(cx, cy + haut + 2, cx + larg, cy + haut + 16),
                            f"réglage {k + 1}  ·  hachure {ep} pt  ·  point {rp} pt",
                            fontname="helv", fontsize=8, color=NAVY, align=fitz.TEXT_ALIGN_CENTER)
    page.insert_textbox(fitz.Rect(40, 800, 555, 826),
                        "LA MAISON DE LA CONFORMITE SARL  ·  usage interne  ·  indiquer au superviseur "
                        "le numéro du réglage retenu, il sera figé pour toutes les impressions.",
                        fontname="helv", fontsize=7.5, color=NAVY, align=fitz.TEXT_ALIGN_CENTER)
    doc.save(dest); doc.close()
    return dest


def main():
    p = argparse.ArgumentParser(description="Exemplaires nominatifs et traçables — MDC")
    p.add_argument("source", nargs="?", default=None)
    p.add_argument("--porteur"); p.add_argument("--liste")
    p.add_argument("--numero", type=int, default=1); p.add_argument("--total", type=int, default=0)
    p.add_argument("--url", default="https://lamaisondelaconformitesarl.net/verif")
    p.add_argument("--mot", default="COPIE")
    p.add_argument("--sortie"); p.add_argument("--dossier", default=".")
    p.add_argument("--calibrage", action="store_true", help="produit la planche de calibrage et sort")
    p.add_argument("--hachure", type=float, default=EP_HACHURE)
    p.add_argument("--point", type=float, default=R_POINT)
    a = p.parse_args()
    if a.calibrage:
        dest = a.sortie or os.path.join(a.dossier, "PLANCHE_CALIBRAGE_FOND_SECURITE.pdf")
        os.makedirs(a.dossier, exist_ok=True)
        print("Planche de calibrage :", planche_calibrage(dest, a.mot)); return
    date_iso = datetime.date.today().isoformat()
    porteurs = []
    if a.liste:
        porteurs = [l.strip() for l in open(a.liste, encoding="utf-8") if l.strip()]
    elif a.porteur:
        porteurs = [a.porteur]
    else:
        sys.exit("Indiquer --porteur ou --liste.")
    total = a.total or len(porteurs)
    os.makedirs(a.dossier, exist_ok=True)
    lignes = []
    for k, porteur in enumerate(porteurs, start=a.numero):
        nom = "".join(c if c.isalnum() else "_" for c in porteur)[:28]
        dest = a.sortie if (a.sortie and len(porteurs) == 1) else os.path.join(
            a.dossier, f"{os.path.splitext(os.path.basename(a.source))[0]}__EX{k:03d}_{nom}.pdf")
        lignes.append(securiser(a.source, dest, porteur, k, total, a.url, a.mot, date_iso,
                                a.hachure, a.point))
        print(f"  exemplaire {k:03d} — {porteur:32s} -> {os.path.basename(dest)}")
    reg = os.path.join(a.dossier, "REGISTRE_DES_EXEMPLAIRES.csv")
    existe = os.path.exists(reg)
    with open(reg, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(lignes[0].keys()))
        if not existe: w.writeheader()
        w.writerows(lignes)
    print(f"\nRegistre : {reg}")


if __name__ == "__main__":
    main()
