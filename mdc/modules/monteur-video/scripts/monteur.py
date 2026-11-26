#!/usr/bin/env python3
"""Monteur vidéo « Avec Mon Fiscaliste » — moteur de montage piloté par un fichier projet.json.

Usage :
  python3 monteur.py <projet.json> preparer          # audio 16 kHz, transcription mot à mot, regard (Apple Vision)
  python3 monteur.py <projet.json> regions A B       # zones de parole entre A et B s (pour placer les coupes)
  python3 monteur.py <projet.json> verbatim          # re-transcription zone par zone (bafouillages, reprises)
  python3 monteur.py <projet.json> plan              # plans, mots, scènes, regards couverts, couverture animée
  python3 monteur.py <projet.json> test youtube 1.5,8.2,30   # images de contrôle du calque d'animation
  python3 monteur.py <projet.json> youtube|short|tout        # rendu final
  python3 monteur.py <projet.json> controle          # contrôle qualité des fichiers exportés

Toutes les durées sont en secondes. « Source » = temps dans le rush, « montage » = temps dans la vidéo finale.
"""
import csv, hashlib, json, math, os, shutil, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import audio_fx  # noqa: E402

FPS, SR = 24, 48000
PRE, POST, MAX_GAP = 0.08, 0.14, 0.55
GAZE_MIN = 0.25

CREATIVES = {  # scènes « une métaphore par idée » (motion/scenes_creatives.js) : type → transition par défaut
    "boussole": "whip", "balance": "flash", "boucle": "whip", "ailleurs": "flash", "respire": "burn", "numero": "burn",
    "vague": "whip", "cle": "burn", "reseau": "flash", "billets": "flash", "enveloppe_non": "whip", "foule": "burn",
    "decodage": "flash", "prix": "whip", "calendrier": "flash", "bouclier": "burn", "fondations": "flash",
    "iceberg": "whip", "triptyque": "burn", "flux": "whip", "semaine": "flash", "croissance": "flash",
    "boite_outils": "whip", "orage": "flash", "confidentiel": "whip", "associe": "burn", "parchemin": "burn"}
TIKTOK = {  # scènes verticales (motion/scenes_tiktok.js) : type → transition par défaut
    "preuves": "flash", "decharge": "whip", "aiguillage": "burn", "echeancier": "flash", "dividende": "whip",
    "statuts": "flash", "piece": "burn", "porte": "whip", "duel": "flash", "guichet": "whip", "valise": "burn",
    "ticket": "flash", "agrement": "whip", "machine": "burn", "radar": "whip", "contrat": "flash",
    "surligne": "flash", "cinetique": "whip", "whatsapp": "whip", "jumeaux": "burn", "bulletin": "flash", "caisse": "whip", "maison": "flash", "virement": "whip"}
PHRASES_REGARD = ["cinetique", "surligne", "citation"]   # rotation pour couvrir les regards (jamais deux fois la même)
OVERLAYS_TIKTOK = {"accroche", "commentaire", "rec"}   # habillages sur l'orateur (pas plein écran)
FULL_TYPES = {"mot_geant", "frise", "document", "barre", "contraste", "courbe", "compteur", "marque", "citation",
              "chapitre", "section"} | set(CREATIVES) | set(TIKTOK)
LIGHT_TYPES = {"document", "courbe", "ailleurs", "billets", "decodage", "calendrier", "fondations", "semaine",
               "croissance", "surligne", "bulletin", "maison", "preuves", "decharge", "echeancier", "statuts", "guichet", "ticket", "contrat", "virement"}
TRANS_DEFAUT = {"mot_geant": "burn", "frise": "flicker", "document": "whip", "barre": "flash", "contraste": "whip",
                "courbe": "flash", "compteur": "flicker", "marque": "burn", "citation": "flash", "chapitre": "burn",
                "section": "burn", **CREATIVES, **TIKTOK}

# Étalonnage « propre » (validé) : neutre, clair, sans dominante — la source iPhone est déjà neutre.
GRADE = ("curves=m='0/0.01 0.15/0.165 0.35/0.405 0.6/0.655 0.85/0.885 1/0.98',"
         "huesaturation=colors=g:saturation=-0.18,eq=saturation=1.05:contrast=1.03,unsharp=5:5:0.35")

# Chaîne voix (validée) : recentrage mono, correction micro-cravate, expanseur doux, compression 2 étages.
def voice_chain(chan, propre=False):
    if propre:   # voix déjà nettoyée (nettoyage_voix.py) : pas de second débruiteur ni de porte, qui créent des
        #          « bulles » et des claquements sur un signal déjà silencieux entre les phrases
        return (f"pan=mono|c0={chan},"
                "bass=g=-6:f=140:t=s:w=0.7,equalizer=f=200:t=q:w=1.2:g=-5,equalizer=f=320:t=q:w=1.2:g=-5,"
                "equalizer=f=550:t=q:w=1.4:g=-3,equalizer=f=3200:t=q:w=0.9:g=4,equalizer=f=6000:t=q:w=1.4:g=1,"
                "equalizer=f=10000:t=q:w=1:g=5,equalizer=f=14000:t=q:w=1:g=4,deesser=i=0.1:m=0.5:f=0.5,"
                "acompressor=threshold=-22dB:ratio=2.5:attack=8:release=160:knee=4:makeup=3,"
                "acompressor=threshold=-12dB:ratio=5:attack=1.5:release=60:makeup=1,alimiter=limit=0.89:level=false")
    return (f"pan=mono|c0={chan},highpass=f=75:poles=2,adeclick=w=20:o=50,afftdn=nr=8:nf=-62:tn=1,"
            "bass=g=-6:f=140:t=s:w=0.7,equalizer=f=200:t=q:w=1.2:g=-5,equalizer=f=320:t=q:w=1.2:g=-5,"
            "equalizer=f=550:t=q:w=1.4:g=-3,equalizer=f=3200:t=q:w=0.9:g=4,equalizer=f=6000:t=q:w=1.4:g=1,"
            "equalizer=f=10000:t=q:w=1:g=5,equalizer=f=14000:t=q:w=1:g=4,deesser=i=0.1:m=0.5:f=0.5,"
            "agate=threshold=0.008:ratio=1.8:range=0.3:attack=8:release=220:knee=4,"
            "acompressor=threshold=-22dB:ratio=2.5:attack=8:release=160:knee=4:makeup=3,"
            "acompressor=threshold=-12dB:ratio=5:attack=1.5:release=60:makeup=1,alimiter=limit=0.89:level=false")

# Captation cinématographique simulée (valeurs par défaut, surchargeables par projet.json → "cinema")
CINEMA_DEFAUT = {"push": 0.045,              # travelling avant lent sur chaque plan (4,5 % de zoom)
                 "profondeur": True,          # fond flouté/assombri grâce au détourage (mode Portrait)
                 "flou_fond": 10,             # sigma du flou du fond en 4K (≈ f/2)
                 "fond": "eq=brightness=-0.045:gamma=0.93:saturation=0.9,colorbalance=rs=-0.015:bs=0.025:rm=-0.01:bm=0.015"}


def cinema(P):
    c = dict(CINEMA_DEFAUT)
    c.update(P.p.get("cinema", {}))
    return c


# Encodage recommandé YouTube (H.264 High, GOP = fps/2, 2 B-frames, BT.709, débit élevé)
YT_VIDEO = ["-c:v", "libx264", "-preset", "slow", "-crf", "15", "-maxrate", "68M", "-bufsize", "136M",
            "-profile:v", "high", "-level:v", "5.1", "-g", "12", "-bf", "2", "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
YT_AUDIO = ["-c:a", "aac", "-b:a", "384k", "-ar", "48000", "-ac", "2"]
# Vertical TikTok / Facebook Reels : 1080×1920, H.264 High, ~16 Mb/s (plateformes qui recompressent : fichier léger à
# envoyer depuis le téléphone, qualité conservée), BT.709
VERTICAL_VIDEO = ["-c:v", "libx264", "-preset", "slow", "-crf", "17", "-maxrate", "16M", "-bufsize", "32M",
                  "-profile:v", "high", "-level:v", "4.2", "-g", "48", "-bf", "2", "-pix_fmt", "yuv420p",
                  "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]


# ---------------------------------------------------------------------------
class Projet:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.dir = os.path.dirname(self.path)
        self.p = json.load(open(self.path))
        self.src = self.p["source"]
        self.work = os.path.join(self.dir, "work")
        self.out = os.path.join(self.dir, "export")
        os.makedirs(self.work, exist_ok=True)
        os.makedirs(self.out, exist_ok=True)
        self.nom = self.p.get("nom", os.path.splitext(os.path.basename(self.src))[0])
        self.end_dur = self.p.get("fin", {}).get("duree", 6.0)
        self.clips = []

    def w(self, *a):
        return os.path.join(self.work, *a)

    def setup(self):
        """Cadence et taille réelles du rush A, décalages de la caméra B et du son externe (work/prep.json)."""
        global FPS
        prep = self.w("prep.json")
        info = json.load(open(prep)) if os.path.exists(prep) else {}
        if "fps" not in info:
            info.update(probe_video(self.src))
            json.dump(info, open(prep, "w"), indent=1)
        FPS = info["fps"]
        self.sw, self.sh = info["w"], info["h"]
        self.cam_b = self.p.get("camera_b")
        if self.cam_b and "b_w" not in info:
            vb = probe_video(self.cam_b)
            info.update({"b_w": vb["w"], "b_h": vb["h"], "b_fps": vb["fps"]})
            json.dump(info, open(prep, "w"), indent=1)
        self.size = {"A": (self.sw, self.sh), "B": (info.get("b_w", self.sw), info.get("b_h", self.sh))}
        self.son = self.p.get("son")
        # nettoyage de la voix AVANT tout (bruit de fond, parasites) : par défaut quand il n'y a pas de son externe
        self.nettoye = not self.son and self.p.get("nettoyage", True)
        if self.nettoye:
            self.son = self.w("voix_propre.wav")
            if not os.path.exists(self.son):
                voix_propre(self)
        self.off_b = self.p.get("decalage_camera_b", info.get("off_b"))
        self.off_son = 0.0 if self.nettoye else self.p.get("decalage_son", info.get("off_son"))
        self.face_x = {"A": self.p.get("cadrage_visage_x", info.get("face_a", 0.5)),
                       "B": self.p.get("cadrage_visage_x_b", info.get("face_b", 0.5))}
        g = str(max(1, round(FPS / 2)))
        YT_VIDEO[YT_VIDEO.index("-g") + 1] = g
        VERTICAL_VIDEO[VERTICAL_VIDEO.index("-g") + 1] = str(round(FPS * 2))
        return info


def probe_video(path):
    out = run(["ffmpeg", "-hide_banner", "-display_rotation", "0", "-i", path, "-t", "0.1", "-f", "null", "-"])
    import re
    m = re.search(r"Video: .*?, (\d{3,5})x(\d{3,5})", out)
    f = re.search(r"(\d+(?:\.\d+)?) fps", out)
    fps = float(f.group(1)) if f else 24.0
    fps = int(round(fps)) if abs(fps - round(fps)) < 0.02 else fps
    return {"w": int(m.group(1)) if m else 3840, "h": int(m.group(2)) if m else 2160, "fps": fps}


def audio_offset(ref, other, seconds=240):
    """Décalage (s) tel que t_other = t_ref + décalage, par corrélation des enveloppes sonores."""
    def env(path):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-t", str(seconds), "-vn", "-ac", "1", "-ar", "8000",
                              "-f", "f32le", "-"], capture_output=True).stdout
        x = np.abs(np.frombuffer(raw, dtype=np.float32))
        n = len(x) // 8
        e = x[:n * 8].reshape(-1, 8).mean(1)          # 1000 échantillons / s
        e = e - np.convolve(e, np.ones(200) / 200, "same")
        return e / (np.std(e) + 1e-9)
    a, b = env(ref), env(other)
    N = 1 << (len(a) + len(b)).bit_length()
    c = np.fft.irfft(np.fft.rfft(b, N) * np.conj(np.fft.rfft(a, N)), N)
    lag = int(np.argmax(c))
    if lag > N // 2:
        lag -= N
    return lag / 1000.0


def face_center(P, path, t):
    """Position horizontale (0–1) de la personne dans un rush, par détourage Apple Vision."""
    d = P.w("visage_tmp")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "in"))
    run(["ffmpeg", "-y", "-hide_banner", "-display_rotation", "0", "-ss", str(t), "-i", path, "-frames:v", "1",
         "-vf", "scale=960:-2", os.path.join(d, "in", "f.png")])
    subprocess.run(["swift", os.path.join(HERE, "tools", "segment.swift"), os.path.join(d, "in"), os.path.join(d, "m")],
                   capture_output=True)
    from PIL import Image
    m = np.asarray(Image.open(os.path.join(d, "m", "f.png")).convert("L"), dtype=float)
    col = m.sum(0)
    # centre de la moitié haute du corps (tête/épaules) plutôt que du corps entier
    top = m[: m.shape[0] // 2].sum(0)
    w = top if top.sum() > 0 else col
    return float((w * np.arange(len(w))).sum() / max(w.sum(), 1) / len(w))


def run(cmd, quiet=True):
    r = subprocess.run(cmd, capture_output=quiet, text=True)
    if r.returncode:
        print((r.stderr or "")[-3000:])
        raise SystemExit(f"échec : {' '.join(map(str, cmd[:6]))}…")
    return r.stderr


# ---------------------------------------------------------------------------
# Préparation : audio, transcription, regard
# ---------------------------------------------------------------------------
def voix_propre(P):
    """Voix débarrassée du bruit de fond (scripts/nettoyage_voix.py), même durée que le rush : sert à la
    transcription, aux points de coupe et au mixage. Désactivable par "nettoyage": false dans projet.json."""
    import nettoyage_voix as nv
    ch = voice_channel(P)
    x = nv.lire(P.src, ch if ch in ("c0", "c1") else None)
    y, _, _ = nv.nettoyer(x, P.p.get("nettoyage_force", 1.0))
    tmp = P.son + ".tmp.wav"
    nv.ecrire(tmp, y)
    os.rename(tmp, P.son)
    b0, v0 = nv.mesure(x)
    b1, v1 = nv.mesure(y)
    print(f"  nettoyage de la voix : bruit de fond {b0:.0f} → {b1:.0f} dB, voix {v0:.0f} → {v1:.0f} dB", flush=True)


def voice_channel(P):
    """La voix de l'iPhone (Blackmagic Cam + DJI) n'est souvent que sur un canal : on le détecte."""
    if "canal_voix" in P.p:
        return P.p["canal_voix"]
    out = run(["ffmpeg", "-hide_banner", "-t", "120", "-i", P.src, "-vn", "-af",
               "astats=measure_perchannel=RMS_level:measure_overall=none", "-f", "null", "-"])
    lv = [float(x.split(":")[-1]) if "inf" not in x else -200 for x in out.splitlines() if "RMS level" in x]
    if len(lv) >= 2 and abs(lv[0] - lv[1]) > 12:
        return "c0" if lv[0] > lv[1] else "c1"
    return "0.5*c0+0.5*c1"


def preparer(P):
    a16 = P.w("audio16k.wav")
    if not os.path.exists(a16):
        run(["ffmpeg", "-y", "-hide_banner", "-i", P.son if P.nettoye else P.src, "-vn", "-ac", "1", "-ar", "16000", a16])
    tj = P.w("transcript.json")
    if not os.path.exists(tj):
        print("  transcription (large-v3-turbo)…", flush=True)
        from faster_whisper import WhisperModel
        m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
        segs, _ = m.transcribe(a16, language="fr", word_timestamps=True, condition_on_previous_text=False,
                               initial_prompt=P.p.get("prompt_transcription", "Chaîne YouTube Avec Mon Fiscaliste, "
                                                      "Côte d'Ivoire. Impôts, DGI, TVA, patente, entreprises."))
        out = [{"start": s.start, "end": s.end, "text": s.text,
                "words": [{"s": w.start, "e": w.end, "w": w.word, "p": w.probability} for w in s.words]} for s in segs]
        json.dump(out, open(tj, "w"), ensure_ascii=False, indent=1)
        for s in out:
            print(f"  [{s['start']:7.2f}-{s['end']:7.2f}] {s['text']}")
    gz = P.w("gaze.csv")
    if not os.path.exists(gz):
        print("  regard (Apple Vision)…", flush=True)
        d = P.w("gaze_frames")
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        run(["ffmpeg", "-y", "-hide_banner", "-display_rotation", "0", "-i", P.src, "-vf", "fps=8,scale=1280:-1",
             "-q:v", "3", "-start_number", "0", os.path.join(d, "f_%05d.jpg")])
        for f in sorted(os.listdir(d)):
            i = int(f[2:7])
            os.rename(os.path.join(d, f), os.path.join(d, f"t_{i / 8:08.3f}.jpg"))
        r = subprocess.run(["swift", os.path.join(HERE, "tools", "gaze.swift"), d], capture_output=True, text=True)
        open(gz, "w").write(r.stdout)
    info = P.setup()
    mid = P.p["groupes"][0][0] + 1 if P.p.get("groupes") else 30
    if "face_a" not in info:
        info["face_a"] = face_center(P, P.src, mid)
    if P.cam_b and "off_b" not in info:
        info["off_b"] = audio_offset(P.src, P.cam_b)
        info["face_b"] = face_center(P, P.cam_b, mid + info["off_b"])
    if P.son and not P.nettoye and "off_son" not in info:
        info["off_son"] = audio_offset(P.src, P.son)
    json.dump(info, open(P.w("prep.json"), "w"), indent=1)
    print(f"  cadence {info['fps']} i/s, {info['w']}×{info['h']}, visage A à x={info['face_a']:.2f}")
    if P.cam_b:
        print(f"  caméra B : décalage {info['off_b']:+.3f} s, visage à x={info['face_b']:.2f}")
    if P.son and not P.nettoye:
        print(f"  son externe : décalage {info['off_son']:+.3f} s")
    elif P.nettoye:
        print("  voix nettoyée (bruit de fond supprimé) : work/voix_propre.wav")
    print(f"  canal voix : {voice_channel(P)}")


# ---------------------------------------------------------------------------
# Parole, coupes
# ---------------------------------------------------------------------------
_ENV = None


def envelope(P):
    global _ENV
    if _ENV is None:
        w = wave.open(P.w("audio16k.wav"))
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        hop, n = 160, len(a) // 160
        db = np.array([20 * np.log10(np.sqrt(np.mean(a[i * hop:(i + 1) * hop + 320] ** 2)) + 1e-9) for i in range(n)])
        _ENV = np.convolve(db, np.ones(5) / 5, mode="same")
    return _ENV


def speech_regions(env, a, b, th=-42):
    sp = env[int(a * 100):int(b * 100)] > th
    regs, i = [], 0
    while i < len(sp):
        if sp[i]:
            j = i
            while j < len(sp) and sp[j]:
                j += 1
            regs.append([a + i / 100, a + j / 100])
            i = j
        else:
            i += 1
    merged = []
    for r in regs:
        if merged and r[0] - merged[-1][1] < 0.12:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return [r for r in merged if r[1] - r[0] > 0.08]


def snap(t):
    return round(t * FPS) / FPS


def seuil_parole(env):
    """Seuil de parole : -42 dB, abaissé pour une prise enregistrée bas (voix forte - 20 dB)."""
    return float(min(-42.0, np.percentile(env, 90) - 20))


def build_clips(P):
    env = envelope(P)
    th = seuil_parole(env)
    clips = []
    for gi, (a, b) in enumerate(P.p["groupes"]):
        regs = speech_regions(env, a, b, th) or [[a, b]]
        cur = [max(a, regs[0][0] - PRE), None]
        for k in range(len(regs) - 1):
            if regs[k + 1][0] - regs[k][1] > MAX_GAP:
                cur[1] = regs[k][1] + POST
                clips.append((gi, *cur))
                cur = [regs[k + 1][0] - PRE, None]
        cur[1] = min(b, regs[-1][1] + POST)
        clips.append((gi, *cur))
    # bafouillages retirés à l'intérieur des phrases
    res = []
    for gi, s, e in clips:
        pieces = [(s, e)]
        for a, b in P.p.get("retraits", []):
            nxt = []
            for ps, pe in pieces:
                if b <= ps or a >= pe:
                    nxt.append((ps, pe))
                else:
                    if a > ps:
                        nxt.append((ps, a))
                    if b < pe:
                        nxt.append((b, pe))
            pieces = nxt
        res += [(gi, ps, pe) for ps, pe in pieces if pe - ps > 0.1]
    # plans trop longs : punch-in sur une micro-pause
    final = []
    for gi, s, e in res:
        while e - s > 6.0:
            regs = [r for r in speech_regions(env, s, e, th) if s + 2.5 < r[1] < e - 2.5]
            if not regs:
                break
            r = min(regs, key=lambda r: abs(r[1] - (s + min(4.5, (e - s) / 2))))
            final.append((gi, s, r[1] + 0.06))
            s = r[1] + 0.06
        final.append((gi, s, e))
    out, t = [], 0.0
    for gi, s, e in final:
        s, e = snap(s), snap(e)
        out.append({"group": gi, "src_s": s, "src_e": e, "out_s": t})
        t += e - s
    return out


def total_len(clips):
    return clips[-1]["out_s"] + clips[-1]["src_e"] - clips[-1]["src_s"]


def assign_zoom(clips):
    cycle = ["medium", "close", "wide", "close"]
    prev = None
    for i, c in enumerate(clips):
        z = "close" if i in (0, len(clips) - 1) else cycle[i % len(cycle)]
        if z == prev and i != len(clips) - 1:
            z = "medium" if z == "close" else "close"
        c["zoom"] = prev = z
    for i in range(1, len(clips)):
        a, b = clips[i - 1], clips[i]
        if a["zoom"] == b["zoom"] and abs(a["src_e"] - b["src_s"]) > 1e-3:
            around = {clips[k]["zoom"] for k in (i - 1, i + 1) if 0 <= k < len(clips)}
            b["zoom"] = next(z for z in ("close", "medium", "wide") if z not in around)
    return clips


# ---------------------------------------------------------------------------
# Mots (texte corrigé, horodatage) en temps de montage
# ---------------------------------------------------------------------------
def norm(w):
    return w.lower().replace(" ?", "").replace(" ", " ").strip(",.?!:;«»\"")


def load_tokens(P):
    raw = [w for s in json.load(open(P.w("transcript.json"))) for w in s["words"]]
    toks = []
    for w in raw:
        t = w["w"].strip()
        if toks and (t.startswith("'") or t.startswith("-") or t in {"?", "!"}):
            toks[-1]["e"] = w["e"]
        else:
            toks.append({"s": w["s"], "e": w["e"], "w": t})
    return toks


def caption_words(P, clips):
    toks = load_tokens(P)
    fixes = {(g, w): (s, e) for g, w, s, e in P.p.get("horodatages", [])}
    words = []
    for gi, ((a, b), text) in enumerate(zip(P.p["groupes"], P.p["texte"])):
        tw = text.replace(" ?", " ?").replace(" !", " !").split(" ")
        manual = P.p.get("horodatages_groupe", {}).get(str(gi))
        if manual:
            assert len(manual) == len(tw), f"groupe {gi} : {len(manual)} horodatages pour {len(tw)} mots"
            tt = [tuple(x) for x in manual]
        else:
            src = [t for t in toks if a - 0.7 <= t["s"] < b - 0.2 and t["e"] - t["s"] < 3]
            if len(src) != len(tw):
                raise SystemExit(f"groupe {gi} : {len(src)} mots transcrits vs {len(tw)} mots corrigés.\n"
                                 f"  transcrit : {' '.join(t['w'] for t in src)}\n  corrigé   : {text}\n"
                                 "  → garder le même nombre de mots (un mot corrigé par mot transcrit), "
                                 "ou fournir « horodatages_groupe ».")
            tt = [(t["s"], t["e"]) for t in src]
        for k, (w, (s, e)) in enumerate(zip(tw, tt)):
            s, e = fixes.get((gi, w), (s, e))
            words.append({"w": w, "s": s, "e": e, "g": gi, "brk": [gi, k] in P.p.get("coupures_sous_titres", [])})

    def map_t(t, g):
        cs = [c for c in clips if c["group"] == g]
        for c in cs:
            if t < c["src_s"]:
                return c["out_s"]
            if t <= c["src_e"]:
                return c["out_s"] + t - c["src_s"]
        return cs[-1]["out_s"] + cs[-1]["src_e"] - cs[-1]["src_s"]
    for w in words:
        w["os"], w["oe"] = map_t(w["s"], w["g"]), map_t(w["e"], w["g"])
    for i in range(len(words) - 1):
        words[i]["oe"] = max(words[i]["oe"], words[i]["os"] + 0.12)
        if words[i]["oe"] > words[i + 1]["os"] > words[i]["os"]:
            words[i]["oe"] = words[i + 1]["os"]
    return words


def chunk(words, max_words=4, max_chars=24):
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or len(" ".join(x["w"] for x in cur + [w])) > max_chars
                    or cur[-1]["g"] != w["g"]):
            chunks.append(cur)
            cur = []
        cur.append(w)
        if w["w"][-1] in ".?,!" or w.get("brk"):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


# ---------------------------------------------------------------------------
# Scènes (ancrées sur les mots)
# ---------------------------------------------------------------------------
def anchor(v, words, total):
    """{"mot": [groupe, "texte", n], "bord": "debut"|"fin", "decalage": x}  |  "fin_video"  |  nombre (temps montage)"""
    if isinstance(v, (int, float)):
        return float(v)
    if v == "fin_video":
        return total
    g, txt = v["mot"][0], v["mot"][1]
    n = v["mot"][2] if len(v["mot"]) > 2 else 0
    hits = [w for w in words if w["g"] == g and norm(w["w"]) == norm(txt)]
    if len(hits) <= n:
        raise SystemExit(f"ancre introuvable : groupe {g}, mot « {txt} » n°{n}")
    w = hits[n]
    return (w["oe"] if v.get("bord") == "fin" else w["os"]) + v.get("decalage", 0.0)


def schedule(P, words, total):
    sc = []
    for d in P.p["scenes"]:
        s = {"name": d["type"], "start": anchor(d["debut"], words, total), "end": anchor(d["fin"], words, total),
             "texts": d.get("textes", {}), "keys": {}}
        for k, v in d.get("cles", {}).items():
            s["keys"][k] = anchor(v, words, total)
        if "phrase" in d:   # question / citation : [texte, ancre, "gold"|"white"]
            s["keys"]["words"] = [(x[0], anchor(x[1], words, total), x[2] if len(x) > 2 else "white") for x in d["phrase"]]
        s["full"] = d["type"] in FULL_TYPES
        s["light"] = d["type"] in LIGHT_TYPES
        s["hide_caps"] = d.get("masquer_sous_titres", d["type"] in {"question", "marque", "citation", "surligne", "cinetique"})
        s["transition"] = d.get("transition")
        s["hero"] = d.get("hero", s["texts"].get("big") or s["texts"].get("title") or "")
        s["windows_behind"] = d["type"] == "derriere"
        s["couvre_regard"] = d.get("couvre_regard", d["type"] == "commentaire")
        sc.append(s)
    fin = P.p.get("fin", {"type": "chapitre"})
    sc.append({"name": fin.get("type", "chapitre"), "start": total, "end": total + P.end_dur, "full": True,
               "hide_caps": True, "texts": fin.get("textes", {}), "keys": {}, "transition": fin.get("transition", "burn"),
               "hero": fin.get("textes", {}).get("kicker", "")})
    if P.p.get("couvrir_regards", True):
        sc = cover_gaze(P, sc, words)
    sc.sort(key=lambda s: s["start"])
    fulls = [x for x in sc if x["full"]]
    for a, b in zip(fulls, fulls[1:]):
        a["end"] = min(a["end"], b["start"])
    return sc


def gaze_intervals(P, clips):
    path = P.w("gaze.csv")
    if not os.path.exists(path):
        return []
    fl = lambda x: float(x) if x not in ("", "nan") else math.nan
    rows = list(csv.DictReader(open(path)))
    T = np.array([fl(r["t"]) for r in rows])
    A = {k: np.array([fl(r[k]) for r in rows]) for k in ("yaw", "pitch", "px", "py")}
    keep = np.zeros(len(T), bool)
    for c in clips:
        keep |= (T >= c["src_s"]) & (T < c["src_e"])
    ref = {k: np.nanmedian(v[keep]) for k, v in A.items()}
    tol = {"yaw": 0.22, "pitch": 0.22, "px": 0.045, "py": 0.075}
    score = np.nan_to_num(np.maximum.reduce([np.abs(A[k] - ref[k]) / tol[k] for k in A]), nan=2)
    away = np.convolve((score > 1).astype(float), np.ones(3) / 3, "same") > 0.6
    step = float(np.median(np.diff(T)))
    out = []
    for c in clips:
        cur = None
        for i in np.flatnonzero((T >= c["src_s"]) & (T < c["src_e"])):
            if away[i]:
                cur = [T[i], T[i] + step] if cur is None else [cur[0], T[i] + step]
            elif cur:
                out.append((c, *cur))
                cur = None
        if cur:
            out.append((c, *cur))
    gmin = P.p.get("regard_min", GAZE_MIN)   # TikTok face caméra : les coups d'œil < 0,8 s restent naturels
    return [(c["out_s"] + a - c["src_s"], c["out_s"] + b - c["src_s"]) for c, a, b in out
            if b - a >= gmin and c.get("cam", "A") == "A"]


def cover_gaze(P, sc, words):
    full = lambda: sorted([x for x in sc if x["full"]], key=lambda x: x["start"])
    kw = {norm(k) for k in P.p.get("mots_cles", [])}
    for a, b in gaze_intervals(P, P.clips):
        if any(x["start"] <= a and b <= x["end"] for x in full()):
            continue
        if any(x.get("couvre_regard") and x["start"] - .2 <= a and b <= x["end"] + .2 for x in sc):
            continue   # habillage qui explique le regard (lecture d'un commentaire…)
        part = [x for x in full() if x["start"] <= a < x["end"] or x["start"] < b <= x["end"]]
        before = [x for x in full() if x["end"] <= a + 0.05 and a - x["end"] < 0.9]
        after = [x for x in full() if x["start"] >= b - 0.05 and x["start"] - b < 1.3]
        gb = a - before[-1]["end"] if before else 9
        ga = after[0]["start"] - b if after else 9
        if part:
            x = part[0]
            if x["start"] <= a:
                x["end"] = max(x["end"], b + 0.3)
            else:
                x["start"] = min(x["start"], a - 0.3)
        elif before and gb <= ga:
            before[-1]["end"] = max(before[-1]["end"], b + 0.3)
        elif after:
            after[0]["start"] = min(after[0]["start"], a - 0.3)
        else:
            s0, s1 = a - 0.35, max(b + 0.4, a + 1.4)
            # phrase affichée : du début de la proposition en cours (après la ponctuation précédente, 2,5 s max)
            # jusqu'à la fin de la couverture — jamais un fragment comme « que si tu… » ou « partie. De même… »
            idx = [i for i, w in enumerate(words) if s0 - 0.6 <= w["os"] < s1]
            if not idx:
                continue
            i0 = idx[0]
            while i0 > 0 and words[i0 - 1]["w"][-1] not in ".?!…,:;" and words[i0 - 1]["g"] == words[i0]["g"] \
                    and s0 - words[i0 - 1]["os"] < 2.5:
                i0 -= 1
            i1 = idx[-1]   # … et jusqu'à la fin de la proposition (la couverture est prolongée de 1,6 s au plus)
            while words[i1]["w"][-1] not in ".?!…,:;" and i1 + 1 < len(words) and words[i1 + 1]["g"] == words[i1]["g"] \
                    and words[i1 + 1]["oe"] - s1 < 2.2:
                i1 += 1
            s1 = max(s1, words[i1]["oe"] + 0.3)
            ws = words[i0:i1 + 1]
            fin_phrase = [i for i, w in enumerate(ws[:-1]) if w["w"][-1] in ".?!…" and w["os"] < a - 0.3]
            if fin_phrase:   # ne pas commencer sur la fin de la phrase précédente
                ws = ws[fin_phrase[-1] + 1:]
            used = {n: sum(1 for x in sc if x["name"] == n) for n in PHRASES_REGARD}
            prev = [x["name"] for x in full() if x["end"] <= s0][-1:]
            name = min((n for n in PHRASES_REGARD if [n] != prev), key=lambda n: used[n])
            sc.append({"name": name, "start": s0, "end": s1, "full": True, "light": name in LIGHT_TYPES, "hide_caps": True,
                       "texts": {}, "transition": TRANS_DEFAUT.get(name, "flash"), "hero": "", "gaze": True,
                       "keys": {"words": [(w["w"].replace(" ", " "), w["os"], "gold" if norm(w["w"]) in kw else "white")
                                          for w in ws]}})
    fs = full()
    for x, y in zip(fs, fs[1:]):
        if x["end"] > y["start"]:
            x["end"] = y["start"]
    return sc


TRANSITIONS, VIDEO_WHIPS = [], []


def assign_transitions(sc):
    TRANSITIONS.clear()
    VIDEO_WHIPS.clear()
    full = [x for x in sc if x["full"]]
    exit_whip = True
    for i, x in enumerate(full):
        prev = full[i - 1] if i else None
        adjacent = prev is not None and abs(prev["end"] - x["start"]) < 0.05
        kind = x.get("transition") or TRANS_DEFAUT.get(x["name"], "flash")
        if kind == "flicker" and (adjacent or not x.get("hero")):
            kind = "flash"
        if kind == "whip":
            x["enter"] = "whipin" if adjacent else "whip"
            if adjacent:
                prev["exit"] = "whipin"
            else:
                VIDEO_WHIPS.append((x["start"] - 0.14, x["start"] + 0.02))
        else:
            x["enter"] = "cut"
            TRANSITIONS.append({"type": kind, "t": x["start"], "text": x.get("hero", "")})
            if adjacent:
                prev["exit"] = "cut"
        nxt = full[i + 1] if i + 1 < len(full) else None
        if x is not full[-1] and not (nxt and abs(x["end"] - nxt["start"]) < 0.05):
            if exit_whip:
                x["exit"] = "whip"
                VIDEO_WHIPS.append((x["end"] - 0.02, x["end"] + 0.14))
            exit_whip = not exit_whip


def gaze_src_intervals(P, clips):
    """Regards hors objectif en temps SOURCE (caméra A)."""
    out = []
    for a, b in gaze_intervals(P, clips):
        for c in clips:
            ce = c["out_s"] + c["src_e"] - c["src_s"]
            if c["out_s"] <= a < ce:
                out.append((c["src_s"] + a - c["out_s"], c["src_s"] + b - c["out_s"]))
    return out


def use_camera_b(P, clips):
    """Avec une caméra B : chaque regard vers les notes bascule sur l'angle B (où regarder hors de l'objectif
    est naturel) au lieu d'être couvert par une animation ; et une coupe sur deux passe en B pour varier."""
    if not P.cam_b:
        return clips
    iv = [(a - 0.25, b + 0.25) for a, b in gaze_src_intervals(P, clips)]
    res = []
    for c in clips:
        cuts = [c["src_s"], c["src_e"]]
        for a, b in iv:
            for t in (a, b):
                if c["src_s"] + 0.6 < t < c["src_e"] - 0.6:
                    cuts.append(t)
        cuts = sorted(set(snap(t) for t in cuts))
        for s0, s1 in zip(cuts, cuts[1:]):
            mid = (s0 + s1) / 2
            res.append({"group": c["group"], "src_s": s0, "src_e": s1,
                        "cam": "B" if any(a <= mid <= b for a, b in iv) else "A"})
    # fusion : morceaux contigus d'une même caméra, et aucun plan de moins de 0,8 s
    def contiguous(a, b):
        return a["group"] == b["group"] and abs(a["src_e"] - b["src_s"]) < 1e-3
    changed = True
    while changed:
        changed = False
        for i in range(len(res) - 1):
            a, b = res[i], res[i + 1]
            short = (b["src_e"] - b["src_s"] < 0.8) or (a["src_e"] - a["src_s"] < 0.8)
            if contiguous(a, b) and (a["cam"] == b["cam"] or short):
                keep = a["cam"] if (a["src_e"] - a["src_s"]) >= (b["src_e"] - b["src_s"]) else b["cam"]
                if "B" in (a["cam"], b["cam"]) and short:
                    keep = "B"      # en cas de doute on reste sur B : le regard détourné reste couvert
                res[i] = {"group": a["group"], "src_s": a["src_s"], "src_e": b["src_e"], "cam": keep}
                del res[i + 1]
                changed = True
                break
    # variété : une coupe franche sur deux en B
    flip = False
    for i, c in enumerate(res):
        cut = i == 0 or abs(res[i - 1]["src_e"] - c["src_s"]) > 1e-3
        if cut:
            flip = not flip
        if c["cam"] == "A" and cut and flip and i not in (0, len(res) - 1):
            c["cam"] = "B"
    t = 0.0
    for c in res:
        c["out_s"] = t
        t += c["src_e"] - c["src_s"]
    return res


def plan(P, verbose=True):
    P.clips = build_clips(P)
    if P.cam_b:
        P.clips = use_camera_b(P, P.clips)
    P.clips = assign_zoom(P.clips)
    for i, c in enumerate(P.clips):
        if c.get("cam") == "B":
            prev = P.clips[i - 1] if i else None
            jump = prev is not None and prev.get("cam") == "B" and abs(prev["src_e"] - c["src_s"]) > 1e-3
            c["zoom"] = "b2" if jump and prev["zoom"] == "b" else "b"
    words = caption_words(P, P.clips)
    total = total_len(P.clips)
    scenes = schedule(P, words, total)
    assign_transitions(scenes)
    if verbose:
        print(f"{len(P.clips)} plans, parole {total:.1f} s + fin {P.end_dur:.0f} s")
        for c in P.clips:
            print(f"  plan groupe {c['group']} source {c['src_s']:7.2f}-{c['src_e']:7.2f} → montage {c['out_s']:6.2f} [{c.get('cam', 'A')} {c['zoom']}]")
        for s in scenes:
            print(f"  {s['name']:10s} {s['start']:6.2f}-{s['end']:6.2f} {'plein écran' if s['full'] else 'sur orateur':12s}"
                  f" entrée={s.get('enter', '-'):6s} sortie={s.get('exit', '-'):6s}{'  (regard)' if s.get('gaze') else ''}")
        cov = sum(s["end"] - s["start"] for s in scenes if s["full"] and s["start"] < total)
        print(f"  animations plein écran : {cov:.1f} s / {total:.1f} s ({100 * cov / total:.0f} %)")
        al = check_variety(scenes)
        print(f"  variété : {'OK' if not al else 'À REVOIR → ' + ', '.join(al)}")
        un = [(round(a, 2), round(b, 2)) for a, b in gaze_intervals(P, P.clips)
              if not any(s["full"] and s["start"] <= a and b <= s["end"] for s in scenes)]
        print(f"  regards hors objectif non couverts : {un or 'aucun'}")
    return P.clips, words, scenes


# ---------------------------------------------------------------------------
# Rendu des plans vidéo
# ---------------------------------------------------------------------------
# Recadrages en fractions du rush (valables en 4K comme en 1080p) : large 1,0×, moyen 1,1×, serré 1,2×
CROPS = {"wide": (0, 0, 1, 1), "medium": (0, .028, .909, .909), "close": (.0104, .046, .8333, .8333),
         "b": (0, 0, 1, 1), "b2": (0, .04, .87, .87)}


def crop_169(P, zoom, cam="A"):
    fx, fy, fw, fh = CROPS[zoom]
    sw, sh = P.size[cam]
    w, h = int(sw * fw) // 2 * 2, int(sh * fh) // 2 * 2
    if cam == "B":   # caméra B : cadrée au tournage, centrée sur le visage si on zoome
        x = int(min(max(P.face_x["B"] * sw - w / 2, 0), sw - w))
    else:
        x = int(sw * fx)
    return (x, int(sh * fy), w, h)


APERCU = False   # maquette / aperçu : rendu en 1080p pour aller vite


def dims(fmt):
    if fmt == "youtube":
        return (1920, 1080) if APERCU else (3840, 2160)
    return (1080, 1920)


def crop_vertical(P, zoom, cam="A"):
    k = {"wide": 1.0, "medium": .926, "close": .833, "b": 1.0, "b2": .87}[zoom]
    sw, sh = P.size[cam]
    h = int(sh * k) // 2 * 2
    w = int(h * 9 / 16) // 2 * 2
    cx = int(sw * P.face_x[cam])
    y = int(sh * {"wide": 0, "medium": .0185, "close": .042, "b": 0, "b2": .04}[zoom])
    return (int(min(max(cx - w // 2, 0), sw - w)), y, w, h)


def render_clips(P, fmt):
    W, H = dims(fmt)
    files = []
    for i, c in enumerate(P.clips):
        cam = c.get("cam", "A")
        x, y, w, h = crop_169(P, c["zoom"], cam) if fmt == "youtube" else crop_vertical(P, c["zoom"], cam)
        dur = c["src_e"] - c["src_s"]
        push = cinema(P)["push"]
        f = P.w(f"plan_{fmt}_{cam}_{c['src_s']:.3f}_{c['src_e']:.3f}_{c['zoom']}{f'_p{push:g}' if push else ''}.mov")
        files.append(f)
        if os.path.exists(f):
            continue
        tmp = f + ".tmp.mov"
        vf = P.p.get("filtre_source", "") + f"crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos,"
        if push:   # zoom progressif image par image puis recadrage fixe au centre
            vf += (f"scale=w='trunc({W}*(1+{push}*t/{dur:.4f})/2)*2':h=-2:eval=frame:flags=bicubic,"
                   f"crop={W}:{H},")
        # nombre d'images exact : la fin est complétée par clonage si la source (iPhone, VFR) en fournit une de moins
        nfr = int(round(dur * FPS))
        vf = "setpts=PTS-STARTPTS," + vf + f"{GRADE},fps={FPS},tpad=stop_mode=clone:stop_duration=0.3,format=yuv420p"
        af = (f"asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={dur - 0.03:.3f}:d=0.03,"
              f"atrim=end={nfr / FPS:.5f},apad=whole_dur={nfr / FPS:.5f}")
        src, ss = (P.cam_b, c["src_s"] + P.off_b) if cam == "B" else (P.src, c["src_s"])
        run(["ffmpeg", "-y", "-hide_banner", "-display_rotation", "0", "-ss", f"{ss:.4f}", "-t", f"{dur + 0.5:.4f}", "-i", src,
             "-frames:v", str(nfr), "-vf", vf, "-af", af, "-map", "0:v:0", "-map", "0:a:0",
             "-ar", str(SR), "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "pcm_s16le", tmp])
        os.rename(tmp, f)   # jamais de plan tronqué dans le cache
        print(f"  plan {i + 1}/{len(P.clips)} [{cam} {c['zoom']}] {c['src_s']:.2f}-{c['src_e']:.2f}", flush=True)
    return files


def render_endcard(P, fmt):
    W, H = dims(fmt)
    x, y, w, h = crop_169(P, "wide") if fmt == "youtube" else crop_vertical(P, "wide")
    f = P.w(f"fin_{fmt}.mov")
    if not os.path.exists(f):
        vf = (P.p.get("filtre_source", "") + f"crop={w}:{h}:{x}:{y},scale={W}:{H},{GRADE},gblur=sigma=30,eq=brightness=-0.12:saturation=0.8,"
              f"fps={FPS},tpad=stop_mode=clone:stop_duration=1,format=yuv420p")
        t0 = P.p.get("fond_fin_source", P.clips[-1]["src_e"] + 1)
        tmp = f + ".tmp.mov"   # jamais de carte de fin tronquée dans le cache
        run(["ffmpeg", "-y", "-hide_banner", "-display_rotation", "0", "-ss", f"{t0}", "-i", P.src,
             "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo", "-t", str(P.end_dur),
             "-frames:v", str(int(round(P.end_dur * FPS))), "-vf", vf,
             "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-c:a", "pcm_s16le", tmp])
        os.rename(tmp, f)
    return f


# ---------------------------------------------------------------------------
# Calques d'animation (Chrome headless)
# ---------------------------------------------------------------------------
def overlay_cfg(P, fmt, scenes, words, duration, layer):
    vertical = fmt == "short"
    kw = {norm(k) for k in P.p.get("mots_cles", [])}
    st = P.p.get("style_sous_titres", "classique")
    chs = chunk(words, 3, 18) if st in ("jaune", "pop", "karaoke") else chunk(words)
    chunks = []
    for i, ch in enumerate(chs):
        e = ch[-1]["oe"] + 0.25
        if i + 1 < len(chs):
            e = min(e, chs[i + 1][0]["os"])
        chunks.append({"s": ch[0]["os"], "e": e,
                       "words": [{"t": w["w"].replace(" ", " "), "s": w["os"], "kw": norm(w["w"]) in kw} for w in ch]})
    cfg = {"W": 1080 if vertical else 1920, "H": 1920 if vertical else 1080, "dsf": 1 if (vertical or APERCU) else 2,
           "vertical": vertical, "fps": FPS, "duration": duration, "workers": 5, "html": "scene_cinema.html",
           "layer": layer, "channel": P.p.get("chaine", "Avec Mon Fiscaliste"),
           "caps_style": P.p.get("style_sous_titres", "classique"),
           "channel_sub": P.p.get("chaine_sous_titre", "CÔTE D'IVOIRE"), "monogram": P.p.get("monogramme", "MF"),
           "transitions": TRANSITIONS,
           "scenes": [{k: v for k, v in x.items() if k in ("name", "start", "end", "keys", "texts", "light", "full",
                                                           "enter", "exit")} for x in scenes],
           "hidden": [[x["start"], x["end"]] for x in scenes if x.get("hide_caps")],
           "chunks": chunks}
    if layer == "behind":
        cfg["windows"] = [[x["start"], x["end"]] for x in scenes if x["name"] == "derriere"]
    return cfg


def render_overlay(P, fmt, scenes, words, duration, layer="main", times=None, outdir=None):
    d = outdir or P.w(f"calque_{layer}_{fmt}")
    cfg = overlay_cfg(P, fmt, scenes, words, duration, layer)
    html = os.path.join(HERE, "motion", cfg["html"])
    code = open(html).read() + "".join(open(os.path.join(HERE, "motion", f)).read()
                                       for f in ("scenes_creatives.js", "scenes_tiktok.js"))
    sig = hashlib.sha1((json.dumps(cfg, sort_keys=True, default=str) + code).encode()).hexdigest()
    sigf = os.path.join(d, "signature.txt")
    if not times and not (os.path.exists(sigf) and open(sigf).read() == sig):
        shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)
    if layer == "behind":
        from PIL import Image
        blank = P.w(f"vide_{fmt}.png")
        W, H = dims(fmt)
        Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)
        cfg["blank"] = blank
    if not times:
        open(sigf, "w").write(sig)
    cfgp = P.w(f"calque_{layer}_{fmt}.json")
    json.dump(cfg, open(cfgp, "w"), default=str)
    cmd = ["node", os.path.join(HERE, "motion", "render.mjs"), cfgp, d]
    if times:
        cmd.append(",".join(f"{t:.3f}" for t in times))
    rc = subprocess.run(cmd).returncode
    if rc == 3 and not times:
        rescue_frames(P, cfg, d)
    elif rc:
        raise SystemExit("rendu de l'animation en échec")
    return os.path.join(d, "%05d.png")


def rescue_frames(P, cfg, d):
    """Images que Chrome ne peut pas rendre en 4K (textures trop grandes) : rendu en définition moitié puis
    agrandissement. Ce sont des images de transition (film burn, éclipse) : la différence est invisible."""
    fails = json.load(open(os.path.join(d, "echecs.json")))
    low = dict(cfg)
    low["dsf"] = max(0.5, cfg["dsf"] / 2)
    low.pop("windows", None)
    lowp = P.w("secours.json")
    json.dump(low, open(lowp, "w"), default=str)
    tmp = P.w("secours_images")
    shutil.rmtree(tmp, ignore_errors=True)
    r = subprocess.run(["node", os.path.join(HERE, "motion", "render.mjs"), lowp, tmp,
                        ",".join(f"{j['t']:.4f}" for j in fails)])
    if r.returncode:
        raise SystemExit("rendu de secours en échec")
    W, H = int(cfg["W"] * cfg["dsf"]), int(cfg["H"] * cfg["dsf"])
    for i, j in enumerate(fails):
        run(["ffmpeg", "-y", "-hide_banner", "-i", os.path.join(tmp, f"test_{i:02d}.png"), "-vf",
             f"scale={W}:{H}:flags=lanczos,format=rgba", os.path.join(d, j["name"])])
    os.remove(os.path.join(d, "echecs.json"))
    print(f"  {len(fails)} image(s) rendue(s) en définition réduite puis agrandie(s)")


def speaker_windows(scenes, total, pad=0.5):
    """Instants où l'orateur est visible (hors scènes plein écran), élargis de pad."""
    full = sorted((x["start"], x["end"]) for x in scenes if x["full"] and x["start"] < total)
    wins, t = [], 0.0
    for a, b in full:
        if a > t:
            wins.append((max(0, t - pad), min(total, a + pad)))
        t = max(t, b)
    if t < total:
        wins.append((max(0, t - pad), total))
    return wins


def render_masks(P, fmt, joined, scenes, duration):
    """Silhouette de la personne (Apple Vision) : texte « derrière » et flou de profondeur du fond."""
    wins = [(x["start"], x["end"]) for x in scenes if x["name"] == "derriere"]
    if cinema(P)["profondeur"]:
        wins += speaker_windows(scenes, total_len(P.clips))
    wins = sorted(wins)
    merged = []
    for a, b in wins:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    wins = merged
    d = P.w(f"masques_{fmt}")
    sig = json.dumps([wins, os.path.getmtime(joined)])
    sigf = os.path.join(d, "signature.txt")
    n = int(round(duration * FPS))
    if os.path.exists(sigf) and open(sigf).read() == sig and len(os.listdir(d)) > n:
        return os.path.join(d, "%05d.png")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    fr = P.w(f"masques_src_{fmt}")
    shutil.rmtree(fr, ignore_errors=True)
    os.makedirs(fr)
    for a, b in wins:
        i0, i1 = int(a * FPS), int(math.ceil(b * FPS))
        run(["ffmpeg", "-y", "-hide_banner", "-ss", f"{i0 / FPS:.4f}", "-i", joined, "-frames:v", str(i1 - i0),
             "-vf", "scale=1920:-2" if fmt == "youtube" else "scale=1080:-2", "-q:v", "2", "-start_number", str(i0),
             os.path.join(fr, "%05d.jpg")])
    if wins:
        r = subprocess.run(["swift", os.path.join(HERE, "tools", "segment.swift"), fr, d], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("détourage en échec : " + r.stderr[-500:])
    from PIL import Image
    blank = os.path.join(d, "noir.png")
    Image.new("L", (16, 16), 0).save(blank)
    W, H = dims(fmt)
    Image.new("L", (1920 if fmt == "youtube" else 1080, 1080 if fmt == "youtube" else 1920), 0).save(blank)
    for i in range(n):
        f = os.path.join(d, f"{i:05d}.png")
        if not os.path.exists(f):
            os.link(blank, f)
    open(sigf, "w").write(sig)
    return os.path.join(d, "%05d.png")


# ---------------------------------------------------------------------------
# Audio : voix + musique générée + bruitages, normalisé -14 LUFS
# ---------------------------------------------------------------------------
SFX_CREATIVES = {
    "boussole": [("t", .2, "pop"), ("a", 0, "riser"), ("a", 1.0, "swish")],
    "balance": [("t", .5, "coin0"), ("t", .7, "coin1"), ("t", .9, "coin2"), ("t", 1.3, "thud"), ("b", 0, "shimmer")],
    "boucle": [("t", .3, "swish"), ("t", 1.0, "swish"), ("a", 0, "thud")],
    "ailleurs": [("t", .3, "swish"), ("a", .4, "whoosh"), ("a", .8, "ding")],
    "respire": [("t", .1, "shimmer"), ("a", 0, "fail")],
    "numero": [("t", .05, "riser"), ("t", .95, "boom")],
    "vague": [("t", .1, "whoosh"), ("t", .8, "swish")],
    "cle": [("t", .3, "swish"), ("t", 1.35, "click"), ("t", 1.8, "boom"), ("t", 1.85, "shimmer")],
    "reseau": [("t", .1, "pop"), ("t", .7, "pop"), ("t", 1.0, "pop"), ("t", 1.3, "pop"), ("b", .1, "pop"), ("b", .35, "pop")],
    "billets": [("t", .2, "paper"), ("t", .5, "paper"), ("a", 0, "swish"), ("a", .3, "impact")],
    "enveloppe_non": [("t", .3, "paper"), ("a", 0, "boom")],
    "foule": [("t", .2, "whoosh"), ("t", 1.2, "shimmer"), ("a", 0, "thud")],
    "decodage": [("t", .3 + i * .12, "tick") for i in range(7)] + [("a", 0, "swish"), ("a", .4, "shimmer")],
    "prix": [("t", .4 + i * .15, "tock") for i in range(6)] + [("a", 0, "ding")],
    "calendrier": [("t", .2, "paper"), ("a", 0, "swish"), ("a", .25, "thud")],
    "bouclier": [("t", .2, "paper"), ("a", 0, "riser"), ("a", 1.0, "boom")],
    "fondations": [("t", .3, "thud"), ("t", .7, "thud"), ("t", 1.1, "thud"), ("t", 1.5, "thud"), ("a", 0, "shimmer")],
    "iceberg": [("t", .2, "swish"), ("a", 0, "riser"), ("a", 1.1, "boom")],
    "triptyque": [("t", .4, "swish"), ("t", .75, "swish"), ("t", 1.1, "swish")],
    "flux": [("t", .1, "whoosh"), ("a", 0, "fail")],
    "semaine": [("a", i * .35, "pop") for i in range(4)],
    "croissance": [("t", .3, "riser"), ("t", .7, "pop"), ("t", 1.5, "pop"), ("t", 2.3, "pop")],
    "boite_outils": [("t", .8, "swish"), ("b", 0, "click"), ("b", .3, "shimmer")],
    "orage": [("t", .2, "impact"), ("a", 0, "whoosh"), ("a", .3, "ding")],
    "confidentiel": [("t", .2, "paper"), ("a", .4, "click")],
    "associe": [("t", .6, "pop"), ("b", 0, "whoosh"), ("b", .4, "thud")],
    "parchemin": [("t", .2, "paper"), ("a", 0, "boom"), ("a", .1, "shimmer")],
    # scènes TikTok
    "accroche": [("t", .05, "whoosh"), ("t", .3, "pop"), ("a", 0, "thud")],
    "commentaire": [("t", 0, "pop"), ("t", .05, "click")],
    "surligne": [("t", .05, "flashhit"), ("t", .4, "swish")],
    "jumeaux": [("t", .15, "whoosh"), ("a", 0, "impact"), ("a", .3, "pop"), ("b", 0, "shimmer")],
    "bulletin": [("t", .1, "paper"), ("t", 1.2, "coin1"), ("a", 0, "thud")],
    "maison": [("t", .15, "thud"), ("t", .6, "pop"), ("a", 0, "swish"), ("a", .25, "ding"), ("b", 0, "thud"), ("b", .4, "pop")],
    "virement": [("t", .15, "swish"), ("t", 1.4, "tick"), ("a", -.5, "click"), ("a", 0, "fail"), ("b", 0, "swish")],
    "caisse": [("t", .05, "thud"), ("a", 0, "click"), ("a", .3, "whoosh"), ("a", .5, "paper"), ("a", .8, "paper"), ("b", 0, "impact")],
    "whatsapp": [("t", .1, "swish")] + [("t", .5 + i * .6, "pop") for i in range(4)] + [("b", 0, "ding")],
    "cinetique": [("t", .05, "whoosh"), ("t", .3, "tick"), ("t", .6, "tick"), ("t", .9, "tick")],
    "rec": [("t", 0, "click"), ("t", .15, "ding")],
    "preuves": [("t", .25 + i * .16, "pop") for i in range(6)] + [("a", i * .1, "tick") for i in range(6)] + [("b", 0, "shimmer")],
    "decharge": [("t", .1, "paper"), ("a", 0, "swish"), ("b", 0, "thud")],
    "aiguillage": [("t", .3 + i * .32, "coin%d" % (i % 3)) for i in range(8)] + [("a", -.1, "paper"), ("a", .15, "click")],
    "echeancier": [("t", .25 + i * .32, "pop") for i in range(4)] + [("b", 0, "ding")],
    "dividende": [("t", .5, "whoosh"), ("a", 0, "fail"), ("a", .05, "thud")],
    "statuts": [("t", .1, "thud"), ("a", 0, "paper"), ("b", 0, "impact")],
    "piece": [("t", .1, "whoosh"), ("t", .75, "coin1"), ("t", .8, "thud"), ("a", 0, "fail")],
    "porte": [("t", .4, "swish"), ("a", 0, "whoosh"), ("a", .9, "thud")],
    "duel": [("t", .05, "whoosh"), ("a", 0, "impact")],
    "guichet": [("t", .05, "thud"), ("t", .35, "paper"), ("a", 0, "impact")],
    "valise": [("t", .15, "whoosh"), ("t", .65, "thud"), ("t", 1.1, "pop"), ("b", 0, "shimmer")],
    "ticket": [("t", .1, "paper"), ("a", 0, "impact"), ("a", .35, "coin2"), ("b", 0, "ding")],
    "agrement": [("t", .05, "swish"), ("t", .5, "pop"), ("a", 0, "fail")],
    "machine": [("t", .1, "thud"), ("t", .5, "riser"), ("b", 0, "shimmer")],
    "radar": [("t", .05, "shimmer"), ("a", 0, "ding"), ("b", 0, "glitch"), ("b", .05, "impact")],
    "contrat": [("t", .1, "paper")] + [("a", i * .32, "tick") for i in range(5)]}
DEFAUT_CLES = {"a": 1.3, "b": 2.2}


def check_variety(scenes, max_par_type=2, max_derriere=4):
    """Règle anti-répétition : jamais deux fois de suite le même modèle, 2 fois au plus par vidéo
    (4 pour le texte derrière), hors cartes de partie/fin et citations automatiques."""
    from collections import Counter
    libres = {"section", "chapitre", "citation", "surligne", "cinetique"}
    seq = [s["name"] for s in sorted(scenes, key=lambda s: s["start"]) if s["name"] not in libres]
    c = Counter(seq)
    alertes = [f"{t} ×{n}" for t, n in c.items() if n > (max_derriere if t == "derriere" else max_par_type)]
    alertes += [f"{a} deux fois de suite" for a, b in zip(seq, seq[1:]) if a == b and a != "derriere"]
    return alertes


def sfx_events(scenes, clips):
    ev = []
    full = [(x["start"], x["end"]) for x in scenes if x["full"]]
    for a, b in zip(clips, clips[1:]):
        if abs(a["src_e"] - b["src_s"]) > 1e-3 and not any(x0 <= b["out_s"] < x1 for x0, x1 in full):
            ev.append((b["out_s"] - 0.08, "swish"))
    for tr in TRANSITIONS:
        t = tr["t"]
        ev += {"burn": [(t - 0.5, "riser"), (t - 0.1, "whoosh"), (t, "shimmer")], "flash": [(t - 0.02, "flashhit")],
               "flicker": [(t - 0.34, "glitch"), (t, "thud")]}.get(tr["type"], [])
    ev += [(a - 0.06, "swish") for a, _ in VIDEO_WHIPS]
    for x in scenes:
        n, k, t0 = x["name"], x["keys"], x["start"]
        if x.get("enter") in ("whip", "whipin") and not any(abs(a + 0.14 - t0) < 0.01 for a, _ in VIDEO_WHIPS):
            ev.append((t0 - 0.12, "swish"))
        if n == "mot_geant":
            ev += [(t0 + 0.1, "shimmer"), (k["big"] - 0.9, "riser"), (k["big"], "boom")]
        elif n == "frise":
            ev += [(t0 + 0.35 + i * 0.28, "pop") for i in range(4)] + [(k["sub"], "thud")]
        elif n == "document":
            ev += [(t0 + 0.2, "paper"), (k["card"], "swish"), (k["card"] + 0.1, "shimmer"), (k["big"] - 0.1, "paper"),
                   (k["big"], "fail"), (k["big"] + 0.05, "thud")]
        elif n == "barre":
            ev += [(k["t0"] - 0.1, "pop"), (k["t0"] + 0.35, "swish"), (k["t1"] - 0.1, "pop"), (k["t1"] + 0.35, "swish")]
        elif n == "contraste":
            ev += [(k["high"] - 0.6, "riser"), (k["high"], "thud"), (k["high"] + 0.35, "pop"), (k["stat"] - 0.2, "pop")]
            ev += [(k["stat"] - 0.15 + i * 0.1, "tock") for i in range(8)]
        elif n == "courbe":
            ev += [(t0 + 0.3 + i * 0.9, "pop") for i in range(3)] + [(k["conclusion"], "fail")]
        elif n in ("question",):
            ev += [(t, "thud") for _, t, _ in k["words"]]
        elif n == "citation":
            ev += [(t0 + 0.05, "shimmer")]
        elif n == "compteur":
            ev += [(t0 + 0.35 + i * (k["hit"] - t0 - 0.35) / 8, "tock") for i in range(8)]
            ev += [(k["hit"], "boom"), (k["hit"] + 0.1, "shimmer"), (k["after"] - 0.15, "swish")]
        elif n == "marque":
            ev += [(t0 + 0.1, "shimmer"), (t0 + 0.12, "thud"), (k["l1"] - 0.1, "swish"), (k["l2"] - 0.1, "swish")]
        elif n == "derriere":
            ev += [(t0 - 0.05, "whoosh"), (k.get("main", t0 + 0.1), "thud")]
        elif n == "chapitre":
            ev += [(t0 + 0.9, "boom"), (t0 + 2.1, "shimmer"), (t0 + 3.3, "click"), (t0 + 3.45, "ding")]
        elif n == "section":
            ev += [(t0 + 0.4, "thud"), (t0 + 0.9, "shimmer")]
        elif n in SFX_CREATIVES:
            for rep, dt, snd in SFX_CREATIVES[n]:
                base = t0 if rep == "t" else k.get(rep, t0 + DEFAUT_CLES[rep])
                ev.append((base + dt, snd))
    return ev


def read_wav(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64).reshape(-1, 2)


def external_voice(P, total, duration):
    """Piste voix reconstruite plan par plan depuis l'enregistrement externe (DJI), synchronisé sur la caméra A."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", P.son, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    out = np.zeros(int(duration * SR))
    for c in P.clips:
        a = int((c["src_s"] + P.off_son) * SR)
        n = int(round((c["src_e"] - c["src_s"]) * SR))
        seg = np.zeros(n)
        if a < len(x):
            part = x[max(a, 0):a + n]
            seg[max(0, -a):max(0, -a) + len(part)] = part
        f1, f2 = int(0.02 * SR), int(0.03 * SR)
        seg[:f1] *= np.linspace(0, 1, f1)
        seg[-f2:] *= np.linspace(1, 0, f2)
        o = int(round(c["out_s"] * SR))
        out[o:o + n] += seg[:len(out) - o]
    path = P.w("voix_externe.wav")
    audio_fx.save(path, out)
    return path


def build_audio(P, joined, scenes, total, duration, tag):
    voice = P.w(f"{tag}_voix.wav")
    if P.son:
        src, chan = external_voice(P, total, duration), "c0"
    else:
        src, chan = joined, voice_channel(P)
    run(["ffmpeg", "-y", "-hide_banner", "-i", src, "-vn", "-af", voice_chain(chan, P.nettoye), "-ar", str(SR),
         "-ac", "2", voice])
    v = read_wav(voice)
    n = int(duration * SR)
    v = np.pad(v, ((0, max(0, n - len(v))), (0, 0)))[:n]
    mix = v.copy()
    if P.p.get("musique", True):
        m = audio_fx.music(duration, total, P.p.get("style_musique", 0))
        env = np.sqrt(np.convolve(np.mean(v ** 2, 1), np.ones(2400) / 2400, "same"))
        duck = np.convolve(np.clip(1 - 4.5 * env, 0.35, 1.0), np.ones(4800) / 4800, "same")
        m = m * (0.16 / max(1e-6, np.abs(m).max()))   # même niveau quel que soit le style de musique
        mix += m * duck[:, None] * P.p.get("volume_musique", 0.55)   # TikTok : 0.3 (le gérant veut une musique discrète)
    mix += audio_fx.sfx_track(duration, sfx_events(scenes, P.clips)) * P.p.get("volume_bruitages", 0.45)   # 0.45 (le gérant trouvait 1.15 trop fort, 13/10/2026)
    pre = P.w(f"{tag}_mix_pre.wav")
    audio_fx.save(pre, mix / max(1.0, np.abs(mix).max() / 0.95))
    meas = run(["ffmpeg", "-hide_banner", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json",
                "-f", "null", "-"])
    js = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    out = P.w(f"{tag}_mix.wav")
    run(["ffmpeg", "-y", "-hide_banner", "-i", pre, "-af",
         f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
         f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true",
         "-ar", str(SR), out])
    return out


# ---------------------------------------------------------------------------
# Sous-titres SRT
# ---------------------------------------------------------------------------
def srt_ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def write_srt(words, path):
    lines = []
    for n, ch in enumerate(chunk(words, max_words=8, max_chars=42), 1):
        lines += [str(n), f"{srt_ts(ch[0]['os'])} --> {srt_ts(ch[-1]['oe'] + 0.1)}",
                  " ".join(w["w"] for w in ch).replace(" ", " "), ""]
    open(path, "w").write("\n".join(lines))


# ---------------------------------------------------------------------------
def to_video(P, seq, name, alpha=True, gray=False):
    """Séquence PNG → fichier vidéo intermédiaire. Indispensable : avec une séquence PNG en entrée d'un
    filtre overlay, ffmpeg 7 perd des images de façon aléatoire (≈ 2 à 9 %), d'où des micro-figements."""
    out = P.w(name)
    if gray:
        codec = ["-c:v", "ffv1", "-pix_fmt", "gray"]
    else:
        codec = ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-vendor", "apl0"]
    run(["ffmpeg", "-y", "-hide_banner", "-framerate", str(FPS), "-i", seq, *codec, out])
    return out


def count_frames(path):
    out = run(["ffmpeg", "-hide_banner", "-i", path, "-map", "0:v:0", "-f", "null", "-"])
    import re
    m = re.findall(r"frame=\s*(\d+)", out)
    return int(m[-1]) if m else 0


def assemble(P, fmt, words, scenes):
    total = total_len(P.clips)
    duration = total + P.end_dur
    files = render_clips(P, fmt) + [render_endcard(P, fmt)]
    lst = P.w(f"liste_{fmt}.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    joined = P.w(f"assemble_{fmt}.mov")
    run(["ffmpeg", "-y", "-hide_banner", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])
    print("  calque d'animation…", flush=True)
    ov = render_overlay(P, fmt, scenes, words, duration, "main")
    has_behind = any(x["name"] == "derriere" for x in scenes)
    cine = cinema(P)
    use_mask = has_behind or cine["profondeur"]
    if has_behind:
        print("  texte derrière…", flush=True)
        ovb = render_overlay(P, fmt, scenes, words, duration, "behind")
    if use_mask:
        print("  détourage (Apple Vision)…", flush=True)
        masks = render_masks(P, fmt, joined, scenes, duration)
    print("  audio…", flush=True)
    audio = build_audio(P, joined, scenes, total, duration, fmt)
    if fmt == "youtube":
        write_srt(words, os.path.join(P.out, f"{P.nom}_sous-titres_fr.srt"))
    W, H = dims(fmt)
    whip = ""
    for a, b in VIDEO_WHIPS:
        k = 1.5 if fmt == "youtube" else 1
        whip += f"avgblur=sizeX={int(60 * k)}:sizeY=1:enable='between(t,{a:.3f},{b:.3f})',"
        whip += f"avgblur=sizeX={int(25 * k)}:sizeY=1:enable='between(t,{a - 0.05:.3f},{b + 0.05:.3f})',"
    print("  conversion des calques en vidéo…", flush=True)
    ovv = to_video(P, ov, f"calque_main_{fmt}.mov")
    inputs = ["-i", joined, "-i", ovv, "-i", audio]
    if use_mask:
        k = 1 if fmt == "youtube" else 0.5
        if has_behind:
            inputs += ["-i", to_video(P, ovb, f"calque_behind_{fmt}.mov")]
        inputs += ["-i", to_video(P, masks, f"masques_{fmt}.mkv", gray=True)]
        mi = 4 if has_behind else 3
        # fond : flou de profondeur + un demi-diaphragme plus sombre + légèrement plus froid (seulement là où
        # l'orateur est visible : ailleurs le masque est noir et les scènes plein écran recouvrent tout)
        if cine["profondeur"]:
            bg = f"[base]split[b0][b1];[b1]gblur=sigma={cine['flou_fond'] * k:g},{cine['fond']}[bgb];[b0][bgb]overlay=format=auto[bgc];"
        else:
            bg = "[base]null[bgc];"
        fc = (f"[0:v]{whip}format=yuv420p,split[base][fg];{bg}"
              + (f"[3:v]format=rgba[bh];[bgc][bh]overlay=format=auto[bt];" if has_behind else "[bgc]null[bt];")
              + f"[{mi}:v]scale={W}:{H}:flags=bicubic,gblur=sigma={2.0 * k:g},format=gray[m];[fg][m]alphamerge[person];"
              f"[bt][person]overlay=format=auto[bp];[1:v]format=rgba[o];[bp][o]overlay=format=auto,format=yuv420p[v]")
    else:
        fc = f"[0:v]{whip}format=yuv420p[b];[1:v]format=rgba[o];[b][o]overlay=format=auto,format=yuv420p[v]"
    name = f"{P.nom}_youtube_4k.mp4" if fmt == "youtube" else f"{P.nom}_tiktok_facebook.mp4"
    print("  encodage final…", flush=True)
    venc = YT_VIDEO if fmt == "youtube" else VERTICAL_VIDEO
    run(["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "2:a",
         "-t", f"{duration:.3f}", *venc, *YT_AUDIO, "-write_tmcd", "0", "-movflags", "+faststart",
         os.path.join(P.out, name)])
    n, attendu = count_frames(os.path.join(P.out, name)), int(round(duration * FPS))
    if abs(n - attendu) > 3:   # ±3 images d'arrondi en toute fin (carte de fin) ; les plans, eux, sont exacts
        raise SystemExit(f"CONTRÔLE : {name} a {n} images au lieu de {attendu} (images perdues)")
    print(f"=> {name} ({duration:.1f} s, {n} images sur {attendu})")
    mode = P.p.get("jingle", "apres_accroche")   # "apres_accroche" (défaut, choix du gérant), "debut" ou false
    if mode:
        import ajouter_jingle
        final = os.path.join(P.out, name)
        tmp = final + ".jingle.mp4"
        if mode == "debut":
            ajouter_jingle.ajouter(final, tmp)
            print(f"   jingle de la chaîne ajouté au début ({name})")
        else:
            _, t, phrase = ajouter_jingle.inserer_apres_accroche(P.path, final, tmp)
            print(f"   jingle inséré après l'accroche (à {t:.2f} s : « {phrase[:60]}… »)")
        os.replace(tmp, final)


def controle(P):
    for f in sorted(os.listdir(P.out)):
        if not f.endswith(".mp4"):
            continue
        p = os.path.join(P.out, f)
        info = run(["ffmpeg", "-hide_banner", "-i", p, "-f", "null", "-t", "0.1", "-"])
        st = [l.strip() for l in info.splitlines() if "Stream #" in l or "Duration" in l]
        ch = run(["ffmpeg", "-hide_banner", "-i", p, "-vn", "-af",
                  "astats=measure_perchannel=RMS_level:measure_overall=none", "-f", "null", "-"])
        rms = [l.split(":")[-1].strip() for l in ch.splitlines() if "RMS level" in l]
        lu = run(["ffmpeg", "-hide_banner", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"])
        I = [l.strip() for l in lu.splitlines() if l.strip().startswith("I:")][-1:]
        TP = [l.strip() for l in lu.splitlines() if l.strip().startswith("Peak:")][-1:]
        print(f"— {f}\n  " + "\n  ".join(st) + f"\n  RMS G/D : {rms}  |  {I} {TP}  |  images : {count_frames(p)}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(1)
    P = Projet(sys.argv[1])
    cmd = sys.argv[2]
    P.setup()
    if cmd == "preparer":
        preparer(P)
    elif cmd == "regions":
        a, b = float(sys.argv[3]), float(sys.argv[4])
        env = envelope(P)
        for r in speech_regions(env, a, b, seuil_parole(env)):
            print(f"  {r[0]:7.2f} {r[1]:7.2f}  ({r[1] - r[0]:.2f} s)")
    elif cmd == "verbatim":
        from faster_whisper import WhisperModel
        from faster_whisper.audio import decode_audio
        a = decode_audio(P.w("audio16k.wav"))
        m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
        env = envelope(P)
        pr = "Euh... je, je veux dire... et et... Transcription mot à mot avec hésitations, répétitions et faux départs."
        rngs = P.p.get("groupes") or [[0, len(a) / 16000]]
        for gi, (s, e) in enumerate(rngs):
            print(f"=== groupe {gi}")
            for r0, r1 in speech_regions(env, s - 0.5, e + 0.5, seuil_parole(env)):
                segs, _ = m.transcribe(a[int((r0 - .15) * 16000):int((r1 + .15) * 16000)], language="fr", beam_size=5,
                                       initial_prompt=pr, condition_on_previous_text=False)
                print(f"  [{r0:7.2f}-{r1:7.2f}] {' '.join(s.text.strip() for s in segs)}", flush=True)
    elif cmd == "plan":
        plan(P)
    elif cmd == "test":
        fmt, times = sys.argv[3], [float(x) for x in sys.argv[4].split(",")]
        _, words, scenes = plan(P, verbose=False)
        d = P.w(f"test_{fmt}")
        dur = total_len(P.clips) + P.end_dur
        render_overlay(P, fmt, scenes, words, dur, "main", times, d)
        if any(x["name"] == "derriere" for x in scenes):
            render_overlay(P, fmt, scenes, words, dur, "behind", times, d + "_derriere")
        print(f"images de test dans {d}")
    elif cmd in ("youtube", "short", "tout", "all"):
        _, words, scenes = plan(P)
        for fmt in (["youtube", "short"] if cmd in ("tout", "all") else [cmd]):
            assemble(P, fmt, words, scenes)
        controle(P)
    elif cmd == "controle":
        controle(P)
    else:
        print(__doc__)
