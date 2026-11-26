#!/usr/bin/env python3
"""Couverture TikTok / Facebook (1080×1920) : titre rouge et blanc en police Impact, placé DERRIÈRE la tête
(style de la référence « INSPECTEUR IMPÔT » validée par le gérant), signature de la marque en bas.

Usage : python3 couverture.py <projet.json>
Réglages dans projet.json → "couverture" :
  {"t": 55.1,                  # instant du rush (regard caméra, geste expressif)
   "haut": "Sans facture",     # 1re ligne
   "bas": "aucune preuve ?",   # 2e ligne (la plus grande, passe derrière la tête)
   "rouge": "haut" | "bas",    # quelle ligne est en rouge (alterner d'une vidéo à l'autre)
   "zoom": 1.15,               # recadrage plus serré que la vidéo
   "descente": 200}            # option : descend l'image de N px quand la tête cache le titre
La zone vue dans la grille du profil TikTok (3:4 au centre, y 240 → 1680) contient tout le texte.
Sortie : export/<nom>_couverture.jpg
"""
import json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from monteur import Projet, GRADE, run  # noqa: E402
from miniature import seal, CHROME  # noqa: E402

CSS = """<style>html,body{margin:0;background:transparent;width:1080px;height:1920px;overflow:hidden}
body{position:relative;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',sans-serif;-webkit-font-smoothing:antialiased}
.abs{position:absolute}.imp{font-family:Impact,'Haettenschweiler',sans-serif;text-transform:uppercase;white-space:nowrap;
text-align:center;line-height:.95}.r{color:#E3262B;text-shadow:0 7px 0 rgba(90,0,0,.4),0 18px 50px rgba(0,0,0,.5)}
.w{color:#fff;text-shadow:0 7px 0 rgba(0,0,0,.25),0 18px 50px rgba(0,0,0,.55)}</style>"""
FIT = """<script>for(const e of document.querySelectorAll('.fit')){const m=+e.dataset.max;
if(e.scrollWidth>m)e.style.fontSize=(parseFloat(getComputedStyle(e).fontSize)*m/e.scrollWidth)+'px'}</script>"""


def shot(html, out):
    prof = out + ".profil"
    if os.path.exists(out):
        os.remove(out)
    pr = subprocess.Popen([CHROME, "--headless=new", f"--user-data-dir={prof}", "--hide-scrollbars",
                           "--window-size=1080,1920", "--force-device-scale-factor=1",
                           "--default-background-color=00000000", "--virtual-time-budget=3000",
                           f"--screenshot={out}", "file://" + html], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    last = -1
    for _ in range(300):
        time.sleep(0.2)
        if os.path.exists(out):
            size = os.path.getsize(out)
            if size > 0 and size == last:
                break
            last = size
    pr.kill()
    pr.wait()
    shutil.rmtree(prof, ignore_errors=True)
    if not os.path.exists(out):
        raise SystemExit("capture Chrome en échec")


def main():
    P = Projet(sys.argv[1])
    info = P.setup()
    c = P.p["couverture"]
    z = c.get("zoom", 1.15)
    sw, sh = P.sw, P.sh
    h = int(sh / z) // 2 * 2
    w = int(h * 9 / 16) // 2 * 2
    x = int(min(max(sw * P.face_x["A"] - w / 2, 0), sw - w))
    y = int(min(sh * c.get("y", 0.03), sh - h))   # option « y » : haut du cadrage (fraction de la hauteur), pour un orateur filmé de loin
    d = P.w("couverture")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "in"))
    frame = os.path.join(d, "in", "frame.png")
    if c.get("photo"):   # photo fournie par le gérant (plus nette qu'une image de la vidéo) : recadrée en 9:16
        # photo 3:4 réduite à la largeur (1080×1440) et posée en bas : la tête reste SOUS le titre ;
        # le haut est prolongé par la même photo floutée
        run(["ffmpeg", "-y", "-hide_banner", "-i", c["photo"], "-frames:v", "1", "-filter_complex",
             "[0:v]scale=1080:-2,split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
             "boxblur=40:2,eq=brightness=-0.05[bg];[bg][b]overlay=0:H-h,eq=contrast=1.03:saturation=1.02", frame])
    else:
        run(["ffmpeg", "-y", "-hide_banner", "-ss", str(c["t"]), "-i", P.src, "-frames:v", "1", "-vf",
             P.p.get("filtre_source", "") + f"crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos,{GRADE}", frame])
    if c.get("descente"):   # image descendue de N px (tête sous le titre) ; le haut est prolongé par la même image floutée
        tmp = frame + ".png"
        os.replace(frame, tmp)
        run(["ffmpeg", "-y", "-hide_banner", "-i", tmp, "-frames:v", "1", "-filter_complex",
             f"[0:v]split[a][b];[a]boxblur=40:2,eq=brightness=-0.05[bg];[bg][b]overlay=0:{int(c['descente'])}", frame])
        os.remove(tmp)
    r = subprocess.run(["swift", os.path.join(HERE, "tools", "segment.swift"), os.path.join(d, "in"), os.path.join(d, "m")],
                       capture_output=True, text=True)
    mask = os.path.join(d, "m", "frame.png")
    if not os.path.exists(mask):
        raise SystemExit("détourage en échec " + r.stderr[-400:])
    rh = c.get("rouge", "haut") == "haut"
    back = os.path.join(d, "back.html")
    open(back, "w").write(f"""<!doctype html><meta charset="utf-8">{CSS}
<div class="abs" style="left:0;right:0;top:0;height:1100px;background:linear-gradient(180deg,rgba(8,12,28,.82) 0%,rgba(8,12,28,.55) 45%,transparent 100%)"></div>
<div class="abs" style="inset:0;background:radial-gradient(85% 70% at 50% 48%,transparent 55%,rgba(5,8,20,.55) 100%)"></div>
<div class="abs imp fit {'r' if rh else 'w'}" data-max="1000" style="left:0;right:0;top:300px;font-size:170px">{c['haut']}</div>
<div class="abs imp fit {'w' if rh else 'r'}" data-max="1020" style="left:0;right:0;top:470px;font-size:250px">{c['bas']}</div>{FIT}""")
    front = os.path.join(d, "front.html")
    chan, sub, mono = P.p.get("chaine", "Mon Fiscaliste"), P.p.get("chaine_sous_titre", "CÔTE D'IVOIRE"), P.p.get("monogramme", "MF")
    open(front, "w").write(f"""<!doctype html><meta charset="utf-8">{CSS}
<div class="abs" style="left:0;right:0;top:1500px;display:flex;justify-content:center"><div style="display:flex;align-items:center;gap:18px;
  padding:14px 34px 14px 16px;background:linear-gradient(90deg,rgba(12,19,42,.94),rgba(12,19,42,.75));border-radius:80px;border:2px solid rgba(212,175,55,.8)">
  {seal(96, mono)}<div><div style="font-family:'Snell Roundhand';font-weight:700;font-size:58px;color:#FBF7EC;line-height:1">{chan}</div>
  <div style="display:flex;align-items:center;gap:12px;margin-top:6px"><span style="width:50px;height:2px;background:#D4AF37"></span>
  <span style="color:#EDE6D2;font-weight:600;font-size:19px;letter-spacing:.35em">{sub}</span><span style="width:50px;height:2px;background:#D4AF37"></span></div></div></div></div>""")
    bpng, fpng = os.path.join(d, "back.png"), os.path.join(d, "front.png")
    shot(back, bpng)
    shot(front, fpng)
    out = os.path.join(P.out, f"{P.nom}_couverture.jpg")
    run(["ffmpeg", "-y", "-hide_banner", "-i", frame, "-i", bpng, "-i", mask, "-i", fpng, "-filter_complex",
         "[0:v]split[bg][fg];[bg]gblur=sigma=6,eq=brightness=-0.05[bg2];[bg2][1:v]overlay=format=auto[bt];"
         "[2:v]gblur=sigma=1.5,format=gray[m];[fg]eq=contrast=1.05:saturation=1.06:gamma=1.08,unsharp=5:5:0.5[fg2];"
         "[fg2][m]alphamerge[p];[bt][p]overlay=format=auto[bp];[bp][3:v]overlay=format=auto", "-frames:v", "1",
         "-q:v", "2", out])
    print(f"=> {out} ({os.path.getsize(out) // 1024} Ko)")


if __name__ == "__main__":
    main()
