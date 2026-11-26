#!/usr/bin/env python3
"""Miniature YouTube aux couleurs de la marque, avec le grand mot DERRIÈRE la personne.

Usage : python3 miniature.py <projet.json>
Réglages dans projet.json → "miniature" :
  {"t": 100.3,                       # instant du rush (visage expressif, regard caméra)
   "recadrage": [100, 137, 2400, 1350],   # x, y, largeur, hauteur dans le rush 3840×2160 (16:9)
   "haut": "L'administration",       # petite ligne au-dessus (blanc)
   "mot": "ennemi ?",                # grand mot doré placé derrière la tête
   "bas": ""}                        # optionnel : ligne en bas à droite
Sorties : export/<nom>_miniature.jpg (1280×720, < 2 Mo) et export/<nom>_miniature_2k.png.
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from monteur import Projet, GRADE, run  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SEAL = """<svg width="{s}" height="{s}" viewBox="-100 -100 200 200"><defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8C6A14"/><stop offset=".32" stop-color="#F3D77E"/>
<stop offset=".52" stop-color="#C69B2E"/><stop offset=".78" stop-color="#F6DE8E"/><stop offset="1" stop-color="#9A7518"/></linearGradient>
<linearGradient id="gv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7E4A0"/><stop offset=".5" stop-color="#D4AF37"/><stop offset="1" stop-color="#9A7518"/></linearGradient></defs>
<g>{petals}<circle r="82" fill="url(#g)"/><circle r="72" fill="#1B274A"/><circle r="72" fill="none" stroke="url(#g)" stroke-width="3"/>
<circle r="63" fill="none" stroke="#D4AF37" stroke-opacity=".7" stroke-width="1.2"/>
<text x="0" y="22" text-anchor="middle" font-family="Didot, serif" font-weight="700" font-size="64" fill="url(#gv)" letter-spacing="-4">{mono}</text></g></svg>"""


def seal(size, mono):
    import math
    petals = "".join(f'<circle cx="{math.cos(i / 20 * 6.2832) * 78:.1f}" cy="{math.sin(i / 20 * 6.2832) * 78:.1f}" r="16" fill="url(#g)"/>'
                     for i in range(20))
    return SEAL.format(s=size, petals=petals, mono=mono)


BASE_CSS = """<style>html,body{margin:0;background:transparent;width:1280px;height:720px;overflow:hidden}
body{position:relative;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',sans-serif;-webkit-font-smoothing:antialiased}
.abs{position:absolute}.goldg{background:linear-gradient(180deg,#FFF1C9 0%,#FFD98A 30%,#E8B64A 60%,#B8862A 100%);
-webkit-background-clip:text;background-clip:text;color:transparent}</style>"""


def shot(html, out):
    """Capture d'écran Chrome headless (Chrome ne se ferme pas toujours seul : on attend l'image puis on le ferme)."""
    import time
    prof = out + ".profil"
    if os.path.exists(out):
        os.remove(out)
    pr = subprocess.Popen([CHROME, "--headless=new", f"--user-data-dir={prof}", "--hide-scrollbars",
                           "--window-size=1280,720", "--force-device-scale-factor=2",
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
        if pr.poll() is not None and os.path.exists(out):
            break
    pr.kill()
    pr.wait()
    shutil.rmtree(prof, ignore_errors=True)
    if not os.path.exists(out):
        raise SystemExit("capture Chrome en échec")


def main():
    P = Projet(sys.argv[1])
    m = P.p.get("miniature", {})
    t = m.get("t", 100.3)
    x, y, w, h = m.get("recadrage", [100, 137, 2400, 1350])
    d = P.w("miniature")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "in"))
    frame = os.path.join(d, "in", "frame.png")
    run(["ffmpeg", "-y", "-hide_banner", "-display_rotation", "0", "-ss", str(t), "-i", P.src, "-frames:v", "1",
         "-vf", f"crop={w}:{h}:{x}:{y},scale=2560:1440:flags=lanczos,{GRADE}", frame])
    r = subprocess.run(["swift", os.path.join(HERE, "tools", "segment.swift"), os.path.join(d, "in"), os.path.join(d, "m")],
                       capture_output=True, text=True)
    mask = os.path.join(d, "m", "frame.png")
    if not os.path.exists(mask):
        raise SystemExit("détourage en échec " + r.stderr[-400:])
    chan, sub, mono = P.p.get("chaine", "Avec Mon Fiscaliste"), P.p.get("chaine_sous_titre", "CÔTE D'IVOIRE"), P.p.get("monogramme", "MF")
    mot, haut, bas = m.get("mot", "ennemi ?"), m.get("haut", ""), m.get("bas", "")
    # calque arrière : voile bleu nuit + grand mot (sera masqué par la silhouette)
    back = os.path.join(d, "back.html")
    open(back, "w").write(f"""<!doctype html><meta charset="utf-8">{BASE_CSS}
<div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(10,16,38,.78) 0%,rgba(16,26,56,.45) 45%,rgba(10,16,38,.72) 100%)"></div>
<div class="abs" style="inset:0;background:radial-gradient(90% 90% at 50% 45%,transparent 45%,rgba(5,8,20,.65) 100%)"></div>
<div id="w" class="abs goldg" style="left:0;right:0;top:40px;text-align:center;font-weight:900;font-size:230px;letter-spacing:-.03em;
  line-height:1;text-transform:uppercase;white-space:nowrap;filter:drop-shadow(0 10px 30px rgba(0,0,0,.55))">{mot}</div>
<script>const e=document.getElementById('w');if(e.scrollWidth>1180)e.style.fontSize=(230*1180/e.scrollWidth)+'px'</script>""")
    # calque avant : ligne du haut, signature de la marque
    front = os.path.join(d, "front.html")
    open(front, "w").write(f"""<!doctype html><meta charset="utf-8">{BASE_CSS}
{f'''<div class="abs" style="left:0;right:0;top:14px;text-align:center"><span style="display:inline-block;padding:6px 22px;
  background:rgba(12,19,42,.82);border:2px solid #D4AF37;border-radius:10px;color:#fff;font-weight:800;font-size:44px;
  letter-spacing:.04em;text-transform:uppercase">{haut}</span></div>''' if haut else ''}
<div class="abs" style="left:26px;bottom:22px;display:flex;align-items:center;gap:14px;padding:10px 22px 10px 12px;
  background:linear-gradient(90deg,rgba(12,19,42,.92),rgba(12,19,42,.6));border-radius:60px;border:1.5px solid rgba(212,175,55,.7)">
  {seal(74, mono)}<div><div style="font-family:'Snell Roundhand';font-weight:700;font-size:42px;color:#FBF7EC;line-height:1">{chan}</div>
  <div style="display:flex;align-items:center;gap:10px;margin-top:4px"><span style="width:40px;height:2px;background:#D4AF37"></span>
  <span style="color:#EDE6D2;font-weight:600;font-size:14px;letter-spacing:.35em">{sub}</span><span style="width:40px;height:2px;background:#D4AF37"></span></div></div></div>
{f'''<div class="abs" style="right:30px;bottom:34px;color:#fff;font-weight:800;font-size:40px;text-shadow:0 3px 14px rgba(0,0,0,.7)">{bas}</div>''' if bas else ''}""")
    bpng, fpng = os.path.join(d, "back.png"), os.path.join(d, "front.png")
    shot(back, bpng)
    shot(front, fpng)
    big = os.path.join(P.out, f"{P.nom}_miniature_2k.png")
    run(["ffmpeg", "-y", "-hide_banner", "-i", frame, "-i", bpng, "-i", mask, "-i", fpng, "-filter_complex",
         "[0:v]split[bg][fg];[bg]eq=brightness=-0.04:contrast=1.05[bg2];[bg2][1:v]overlay=format=auto[bt];"
         "[2:v]gblur=sigma=1.2,format=gray[m];[fg]eq=contrast=1.06:saturation=1.08:gamma=1.12:brightness=0.02,unsharp=5:5:0.6[fg2];"
         "[fg2][m]alphamerge[p];[bt][p]overlay=format=auto[bp];[bp][3:v]overlay=format=auto", "-frames:v", "1", big])
    small = os.path.join(P.out, f"{P.nom}_miniature.jpg")
    run(["ffmpeg", "-y", "-hide_banner", "-i", big, "-vf", "scale=1280:720:flags=lanczos", "-q:v", "2", small])
    print(f"=> {small} ({os.path.getsize(small) // 1024} Ko)")


if __name__ == "__main__":
    main()
