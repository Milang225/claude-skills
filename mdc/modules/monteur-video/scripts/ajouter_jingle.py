#!/usr/bin/env python3
"""Place le jingle de la chaîne (assets/jingle_16x9.mp4 ou jingle_vertical.mp4, choisi selon l'orientation)
au DÉBUT d'une vidéo exportée. Cadence et taille alignées sur la vidéo, son 48 kHz stéréo (les deux sont déjà à
-14 LUFS), encodage aux réglages YouTube (4K) ou TikTok/Facebook (vertical).
Usage : python3 ajouter_jingle.py <video.mp4> [sortie.mp4]   (défaut : <video>_avec_jingle.mp4)"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FF = os.path.expanduser("~/bin/ffmpeg")


def infos(path):
    o = subprocess.run([FF, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    w, h = map(int, re.search(r"Video: .*?, (\d{3,5})x(\d{3,5})", o).groups())
    fps = float(re.search(r"(\d+(?:\.\d+)?) fps", o).group(1))
    return w, h, fps


def ajouter(video, sortie=None):
    sortie = sortie or os.path.splitext(video)[0] + "_avec_jingle.mp4"
    w, h, fps = infos(video)
    vertical = h > w
    jingle = os.path.join(HERE, "..", "assets", "jingle_vertical.mp4" if vertical else "jingle_16x9.mp4")
    if vertical:
        enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "17", "-maxrate", "16M", "-bufsize", "32M", "-profile:v", "high",
               "-level:v", "4.2", "-g", str(round(fps * 2)), "-bf", "2", "-c:a", "aac", "-b:a", "320k"]
    else:
        enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "15", "-maxrate", "68M", "-bufsize", "136M", "-profile:v", "high",
               "-level:v", "5.1", "-g", str(max(1, round(fps / 2))), "-bf", "2", "-c:a", "aac", "-b:a", "384k"]
    fc = (f"[0:v]scale={w}:{h}:flags=lanczos,fps={fps},setsar=1,format=yuv420p[j];"
          f"[1:v]fps={fps},setsar=1,format=yuv420p[m];"
          "[0:a]aresample=48000,aformat=channel_layouts=stereo[ja];[1:a]aresample=48000,aformat=channel_layouts=stereo[ma];"
          "[j][ja][m][ma]concat=n=2:v=1:a=1[v][a]")
    subprocess.run([FF, "-v", "error", "-y", "-i", jingle, "-i", video, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    *enc, "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                    "-ar", "48000", "-movflags", "+faststart", sortie], check=True)
    return sortie


if __name__ == "__main__":
    print("=>", ajouter(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))


def inserer_apres_accroche(projet_json, video, sortie=None, min_s=2.0):
    """Accroche (1re phrase) → jingle → reste de la vidéo. La coupe tombe au milieu du silence qui suit la
    première phrase de plus de `min_s` secondes (repérée dans les mots horodatés du montage)."""
    import io, contextlib
    sys.path.insert(0, HERE)
    import monteur as M
    M._ENV = None
    P = M.Projet(projet_json)
    P.setup()
    with contextlib.redirect_stdout(io.StringIO()):
        _, words, _ = M.plan(P, verbose=False)
    k = next(i for i, w in enumerate(words[:-1]) if w["w"].rstrip("»  ")[-1:] in ".?!…" and w["oe"] >= min_s)
    t = (words[k]["oe"] + words[k + 1]["os"]) / 2
    w, h, fps = infos(video)
    t = round(t * fps) / fps
    sortie = sortie or os.path.splitext(video)[0] + "_avec_jingle.mp4"
    vertical = h > w
    jingle = os.path.join(HERE, "..", "assets", "jingle_vertical.mp4" if vertical else "jingle_16x9.mp4")
    enc = (["-c:v", "libx264", "-preset", "slow", "-crf", "17", "-maxrate", "16M", "-bufsize", "32M", "-profile:v", "high",
            "-level:v", "4.2", "-g", str(round(fps * 2)), "-bf", "2", "-c:a", "aac", "-b:a", "320k"] if vertical else
           ["-c:v", "libx264", "-preset", "slow", "-crf", "15", "-maxrate", "68M", "-bufsize", "136M", "-profile:v", "high",
            "-level:v", "5.1", "-g", str(max(1, round(fps / 2))), "-bf", "2", "-c:a", "aac", "-b:a", "384k"])
    fc = (f"[1:v]fps={fps},setsar=1,format=yuv420p,split[v1][v2];"
          f"[v1]trim=0:{t:.4f},setpts=PTS-STARTPTS[a];[v2]trim={t:.4f},setpts=PTS-STARTPTS[b];"
          f"[0:v]scale={w}:{h}:flags=lanczos,fps={fps},setsar=1,format=yuv420p[j];"
          "[1:a]aresample=48000,aformat=channel_layouts=stereo,asplit[x1][x2];"
          f"[x1]atrim=0:{t:.4f},asetpts=PTS-STARTPTS,afade=t=out:st={t - 0.03:.4f}:d=0.03[aa];"
          f"[x2]atrim={t:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03[ba];"
          "[0:a]aresample=48000,aformat=channel_layouts=stereo[ja];"
          "[a][aa][j][ja][b][ba]concat=n=3:v=1:a=1[v][au]")
    subprocess.run([FF, "-v", "error", "-y", "-i", jingle, "-i", video, "-filter_complex", fc, "-map", "[v]", "-map", "[au]",
                    *enc, "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                    "-ar", "48000", "-movflags", "+faststart", sortie], check=True)
    phrase = " ".join(x["w"] for x in words[:k + 1]).replace(" ", " ")
    return sortie, t, phrase
