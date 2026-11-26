#!/usr/bin/env python3
"""MAQUETTE (animatique) d'un épisode à partir du SCRIPT, avant le tournage.

Montre la vidéo entière telle qu'elle sortira : animations, transitions, textes derrière le personnage,
cartes de partie, sous-titres, musique et bruitages — avec une VOIX DE SYNTHÈSE PROVISOIRE (macOS « Thomas »)
et une image fixe du studio à la place des plans face caméra. Le plan de scènes est le même format que
projet.json : après le tournage, on reprend ce plan et on l'ancre sur les vraies prises.

Usage : python3 maquette.py <dossier>        (le dossier contient script.txt et plan.json)
plan.json : {"nom", "image_orateur": {"source", "t", "recadrage"}, "mots_cles", "sections": {"2": {"kicker", "title"}, …},
             "scenes": [...ancres {"mot": [numéro_de_phrase, "mot", n]}...], "fin": {...}}
Sortie : export/<nom>_MAQUETTE.mp4 (1920×1080) et work/phrases.txt (phrases numérotées).
"""
import json, os, re, shutil, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import monteur as M      # noqa: E402
import audio_fx          # noqa: E402

VOIX, DEBIT = "Thomas", 185
PAUSE, GAP_SECTION, LEAD = 0.30, 2.8, 0.4


def parse_script(text):
    seqs, cur = [], None
    for line in text.splitlines():
        l = line.strip()
        m = re.match(r"S[ÉE]Q\.?\s*(\d+)\s*/\s*\d+\s*[—–-]\s*(.*)", l)
        if m:
            cur = {"n": int(m.group(1)), "titre": m.group(2).strip(), "phrases": []}
            seqs.append(cur)
        elif l and not set(l) <= set("=-_") and cur is not None:
            if cur["phrases"] and cur["phrases"][-1].rstrip(",") in ("Finalement", "Donc", "Alors"):
                cur["phrases"][-1] = cur["phrases"][-1].rstrip(",") + ", " + l[0].lower() + l[1:]
            else:
                cur["phrases"].append(l)
    if not seqs:   # script sans séquences : une seule séquence, une phrase par ligne
        seqs = [{"n": 1, "titre": "", "phrases": [l.strip() for l in text.splitlines() if l.strip()]}]
    return seqs


def oral(p):
    """Texte prononcé par la voix de synthèse (chiffres et abréviations en toutes lettres)."""
    rep = [(r"\b1ère\b", "première"), (r"\b1er\b", "premier"), (r"\b2e\b", "deuxième"), (r"\b3e\b", "troisième"),
           (r"\btaux 0\b", "taux zéro"), (r"\b3\b", "trois"), (r"\b2\b", "deux"), (r"no+n\b", "non")]
    for a, b in rep:
        p = re.sub(a, b, p)
    return p


def main():
    d = os.path.abspath(sys.argv[1])
    work, out = os.path.join(d, "work"), os.path.join(d, "export")
    os.makedirs(os.path.join(work, "tts"), exist_ok=True)
    os.makedirs(out, exist_ok=True)
    plan = json.load(open(os.path.join(d, "plan.json")))
    seqs = parse_script(open(os.path.join(d, "script.txt")).read())
    phrases, seq_of = [], []
    for s in seqs:
        for p in s["phrases"]:
            phrases.append(p)
            seq_of.append(s["n"])
    with open(os.path.join(work, "phrases.txt"), "w") as f:
        for i, p in enumerate(phrases):
            f.write(f"[{i:2d}] (séq {seq_of[i]}) {p}\n")

    # 1. voix provisoire, phrase par phrase
    durs = []
    for i, p in enumerate(phrases):
        wav = os.path.join(work, "tts", f"p{i:03d}.wav")
        if not os.path.exists(wav):
            aiff = wav[:-4] + ".aiff"
            subprocess.run(["say", "-v", VOIX, "-r", str(DEBIT), "-o", aiff, oral(p)], check=True)
            M.run(["ffmpeg", "-y", "-hide_banner", "-i", aiff, "-ar", "48000", "-ac", "1", wav])
            os.remove(aiff)
        w = M.read_wav(wav)
        durs.append(len(w) / M.SR)

    # 2. chronologie : phrases, pauses, cartes de partie entre les séquences
    words, starts, sections, t = [], [], [], LEAD
    for i, p in enumerate(phrases):
        if i and seq_of[i] != seq_of[i - 1]:
            sections.append((seq_of[i], t, t + GAP_SECTION))
            t += GAP_SECTION
        starts.append(t)
        toks = p.split()
        a, b = t + 0.06, t + durs[i] - 0.12
        weights = np.array([len(x) + 2 for x in toks], dtype=float)
        edges = a + (b - a) * np.concatenate([[0], np.cumsum(weights) / weights.sum()])
        for k, tok in enumerate(toks):
            words.append({"w": tok, "g": i, "s": edges[k], "e": edges[k + 1], "os": edges[k], "oe": edges[k + 1]})
        t += durs[i] + PAUSE
    total = t + 0.3

    # 3. projet factice pour réutiliser le moteur (ancres, planning, calques, transitions, bruitages)
    M.APERCU = True
    M.FPS = 24
    pj = {"nom": plan.get("nom", "maquette"), "source": plan["image_orateur"]["source"], "musique": True,
          "couvrir_regards": False, "mots_cles": plan.get("mots_cles", []), "scenes": plan.get("scenes", []),
          "fin": plan.get("fin", {"type": "chapitre", "duree": 6}), "chaine": plan.get("chaine", "Avec Mon Fiscaliste")}
    pjp = os.path.join(d, "projet_maquette.json")
    json.dump(pj, open(pjp, "w"), ensure_ascii=False, indent=1)
    P = M.Projet(pjp)
    P.work, P.out = work, out
    P.clips = []
    scenes = M.schedule(P, words, total)
    for n, a, b in sections:
        sx = plan.get("sections", {}).get(str(n), {})
        tit = next((s["titre"] for s in seqs if s["n"] == n), "")
        scenes.append({"name": "section", "start": a, "end": b + 0.25, "full": True, "light": False, "hide_caps": True,
                       "texts": {"kicker": sx.get("kicker", f"Partie {n}"), "title": sx.get("title", tit.capitalize()),
                                 "sub": sx.get("sub", "")}, "keys": {}, "transition": "burn", "hero": ""})
    scenes.sort(key=lambda s: s["start"])
    fulls = [x for x in scenes if x["full"]]
    for x, y in zip(fulls, fulls[1:]):
        x["end"] = min(x["end"], y["start"])
    M.assign_transitions(scenes)
    duration = total + P.end_dur
    cov = sum(s["end"] - s["start"] for s in scenes if s["full"] and s["start"] < total)
    print(f"{len(phrases)} phrases, {total / 60:.1f} min + fin ; animations plein écran {cov:.0f} s ({100 * cov / total:.0f} %)")
    al = M.check_variety(scenes)
    print(f"variété : {'OK' if not al else 'À REVOIR → ' + ', '.join(al)}")
    if len(sys.argv) > 2 and sys.argv[2] == "test":   # une image de contrôle par scène
        ts = [(s["name"], s["start"] + min(max(1.2, (s["end"] - s["start"]) * .75), s["end"] - s["start"] - .1))
              for s in scenes if s["name"] not in ("section",)]
        dt = os.path.join(work, "test_scenes")
        shutil.rmtree(dt, ignore_errors=True)
        M.render_overlay(P, "youtube", scenes, words, total + P.end_dur, "main", [t for _, t in ts], dt)
        json.dump(ts, open(os.path.join(dt, "index.json"), "w"))
        print(f"images de test : {dt}")
        return

    # 4. image de l'orateur : fond flouté façon cinéma, travelling qui repart à chaque « coupe »
    io = plan["image_orateur"]
    x, y, w, h = io.get("recadrage", [40, 100, 3200, 1800])
    st = os.path.join(work, "still")
    shutil.rmtree(st, ignore_errors=True)
    os.makedirs(os.path.join(st, "in"))
    M.run(["ffmpeg", "-y", "-hide_banner", "-display_rotation", "0", "-ss", str(io["t"]), "-i", io["source"],
           "-frames:v", "1", "-vf", f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,{M.GRADE}",
           os.path.join(st, "in", "orateur.png")])
    subprocess.run(["swift", os.path.join(HERE, "tools", "segment.swift"), os.path.join(st, "in"), os.path.join(st, "m")],
                   capture_output=True)
    still, mask = os.path.join(st, "in", "orateur.png"), os.path.join(st, "m", "orateur.png")
    fond = M.CINEMA_DEFAUT["fond"]
    M.run(["ffmpeg", "-y", "-hide_banner", "-i", still, "-i", mask, "-filter_complex",
           f"[0:v]split[a][b];[b]gblur=sigma=5,{fond}[bg];[1:v]gblur=sigma=1.5,format=gray[m];[a][m]alphamerge[p];"
           f"[bg][p]overlay", os.path.join(st, "orateur_cine.png")])
    cuts = sorted([0.0] + [s["end"] for s in scenes if s["full"]])
    zexpr = "1+0.045*(" + "+".join([f"between(it,{a:.2f},{b:.2f})*(it-{a:.2f})/{max(b - a, 1):.2f}"
                                    for a, b in zip(cuts, cuts[1:] + [duration])]) + ")"
    zp = (f"zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={M.FPS}")
    base = os.path.join(work, "base.mp4")
    M.run(["ffmpeg", "-y", "-hide_banner", "-loop", "1", "-framerate", str(M.FPS), "-t", f"{duration:.3f}", "-i",
           os.path.join(st, "orateur_cine.png"), "-vf",
           zp.replace("it,", "in_time,").replace("(it-", "(in_time-") + ",drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial Bold.ttf:"
           "text='MAQUETTE · plan face caméra à tourner':x=w-tw-28:y=h-th-24:fontsize=22:fontcolor=white@0.55,format=yuv420p",
           "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", base])
    maskv = os.path.join(work, "masque.mkv")
    M.run(["ffmpeg", "-y", "-hide_banner", "-loop", "1", "-framerate", str(M.FPS), "-t", f"{duration:.3f}", "-i", mask,
           "-vf", zp.replace("it,", "in_time,").replace("(it-", "(in_time-") + ",format=gray", "-c:v", "ffv1", maskv])

    # 5. calques d'animation
    ov = M.to_video(P, M.render_overlay(P, "youtube", scenes, words, duration, "main"), "calque_main.mov")
    has_behind = any(s["name"] == "derriere" for s in scenes)
    if has_behind:
        ovb = M.to_video(P, M.render_overlay(P, "youtube", scenes, words, duration, "behind"), "calque_behind.mov")

    # 6. son : voix provisoire + musique + bruitages, -14 LUFS
    n = int(duration * M.SR)
    v = np.zeros(n)
    for i, s0 in enumerate(starts):
        w = M.read_wav(os.path.join(work, "tts", f"p{i:03d}.wav"))[:, 0]
        a = int(s0 * M.SR)
        v[a:a + len(w)] += w[:max(0, n - a)]
    v2 = np.stack([v, v], 1)
    env = np.sqrt(np.convolve(v ** 2, np.ones(2400) / 2400, "same"))
    duck = np.convolve(np.clip(1 - 4.5 * env, 0.35, 1.0), np.ones(4800) / 4800, "same")
    mix = v2 + audio_fx.music(duration, total) * duck[:, None] * 0.55 + audio_fx.sfx_track(duration, M.sfx_events(scenes, [])) * 1.15
    pre = os.path.join(work, "mix_pre.wav")
    audio_fx.save(pre, mix / max(1.0, np.abs(mix).max() / 0.95))
    audio = os.path.join(work, "mix.wav")
    M.run(["ffmpeg", "-y", "-hide_banner", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000", audio])

    # 7. composition (orateur devant le texte « derrière », animations par-dessus)
    inputs = ["-i", base, "-i", ov, "-i", audio]
    if has_behind:
        inputs += ["-i", ovb, "-i", maskv]
        fc = ("[0:v]split[b][fg];[3:v]format=rgba[bh];[b][bh]overlay=format=auto[bt];[4:v]gblur=sigma=1.5,format=gray[m];"
              "[fg][m]alphamerge[p];[bt][p]overlay=format=auto[bp];[1:v]format=rgba[o];[bp][o]overlay=format=auto,format=yuv420p[v]")
    else:
        fc = "[1:v]format=rgba[o];[0:v][o]overlay=format=auto,format=yuv420p[v]"
    name = f"{P.nom}_MAQUETTE.mp4"
    M.run(["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "2:a",
           "-t", f"{duration:.3f}", "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", os.path.join(out, name)])
    nf, att = M.count_frames(os.path.join(out, name)), int(round(duration * M.FPS))
    print(f"=> {name} ({duration / 60:.1f} min, {nf} images sur {att})")


if __name__ == "__main__":
    main()
