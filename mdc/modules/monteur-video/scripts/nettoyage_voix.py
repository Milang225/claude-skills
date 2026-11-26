#!/usr/bin/env python3
"""Nettoyage de la voix AVANT le montage : supprime le bruit de fond (climatiseur, ventilateur, ronflement,
souffle, bourdonnement électrique) pour ne garder que la voix.

Méthode (100 % locale, sans téléchargement) :
  1. repère les silences entre les phrases (énergie la plus basse du rush) ;
  2. y apprend l'empreinte spectrale du bruit, fréquence par fréquence (moyenne + dispersion) ;
  3. soustrait cette empreinte sous la voix (soustraction spectrale lissée, pas d'effet « robot ») ;
     garde-fou : si la voix perd plus de 3 dB, le traitement s'adoucit automatiquement ;
  4. hors de la voix (détecteur Silero), tout est ramené au silence (-45 dB) avec des rampes de 40 ms :
     claquements, sifflements, voix lointaines et ronflement disparaissent entre les phrases.

Usage : python3 nettoyage_voix.py <rush.mov> <sortie.wav> [--force 1.0] [--extrait 20:35 extrait.wav]
La sortie est un WAV 48 kHz mono 32 bits, de même durée que le rush : le moteur l'utilise comme « son ».
"""
import argparse, os, subprocess, sys
import numpy as np
from scipy.signal import stft, istft
from scipy.ndimage import uniform_filter, uniform_filter1d

FF = os.path.expanduser("~/bin/ffmpeg")
SR = 48000


def lire(path, canal=None):
    pan = ["-af", f"pan=mono|c0={canal}"] if canal else ["-ac", "1"]
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-vn", *pan, "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def ecrire(path, x):
    p = subprocess.Popen([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                          "-c:a", "pcm_f32le", path], stdin=subprocess.PIPE)
    p.communicate(np.clip(x, -1, 1).astype(np.float32).tobytes())


def zones_voix(x):
    """Détecteur de voix Silero (fourni avec faster-whisper) : [(début, fin)] en secondes."""
    from faster_whisper.vad import get_speech_timestamps, VadOptions
    x16 = x[::3].astype(np.float32)   # 48 kHz → 16 kHz (le détecteur ne regarde que l'enveloppe vocale)
    opt = VadOptions(threshold=0.45, min_silence_duration_ms=160, speech_pad_ms=140, min_speech_duration_ms=120)
    return [(d["start"] / 16000, d["end"] / 16000) for d in get_speech_timestamps(x16, opt)]


def anti_ronflement(x, zones):
    """Ronflement électrique / moteur (50–70 Hz et harmoniques) retiré EN CONTINU, voix comprise :
    passe-haut 85 Hz raide (la voix d'homme commence vers 100 Hz) + filtres coupe-bande sur chaque harmonique
    mesurée dans les silences. Sans ça, le ronflement « apparaît et disparaît » au rythme de la voix."""
    from scipy.signal import butter, sosfiltfilt, iirnotch, filtfilt, welch
    from scipy.signal import medfilt
    y = sosfiltfilt(butter(4, 85, "highpass", fs=SR, output="sos"), x)
    m = np.ones(len(x), bool)
    for a, b in zones:
        m[int(a * SR):int(b * SR)] = False
    bruit = x[m] if m.sum() > SR else x
    f, P = welch(bruit, SR, nperseg=min(len(bruit), 2 * SR))
    db = 10 * np.log10(P + 1e-20)
    exc = db - medfilt(db, 41)
    sel = (f > 45) & (f < 75)
    f0 = float(f[sel][np.argmax(exc[sel])])
    if exc[sel].max() < 4:
        return y, None, []
    coupes = []
    for k in range(2, 25):
        fk = k * f0
        if fk > 3000:
            break
        w = np.abs(f - fk) < 2
        if w.any() and exc[w].max() > 3:
            b_, a_ = iirnotch(fk, 35, SR)
            y = filtfilt(b_, a_, y)
            coupes.append(round(fk))
    return y, f0, coupes


def niveau_voix(x, zones):
    m = np.zeros(len(x), bool)
    for a, b in zones:
        m[int(a * SR):int(b * SR)] = True
    return float(20 * np.log10(np.sqrt(np.mean(x[m] ** 2)) + 1e-12)) if m.any() else -120.0


def nettoyer(x, force=1.0, plancher_db=-35.0, silence_db=-45.0):
    """Garde-fou : la voix ne doit pas perdre plus de 3 dB ; sinon on refait plus doucement."""
    zones = zones_voix(x)
    x, f0, coupes = anti_ronflement(x, zones)
    if f0:
        print(f"  ronflement {f0:.0f} Hz supprimé (harmoniques coupées : {coupes or 'aucune audible'})", flush=True)
    v0 = niveau_voix(x, zones)
    for essai in range(4):
        y, mu, bruit = _nettoyer(x, zones, force, plancher_db, silence_db)
        perte = v0 - niveau_voix(y, zones)
        if perte <= 3.0:
            break
        print(f"  la voix perdait {perte:.1f} dB : nettoyage adouci", flush=True)
        force *= 0.6
    return y, mu, bruit


def _nettoyer(x, zones, force, plancher_db, silence_db):
    n_fft, hop = 2048, 512
    f, t, Z = stft(x, SR, nperseg=n_fft, noverlap=n_fft - hop)
    mag = np.abs(Z) + 1e-10
    db = 20 * np.log10(mag)
    # 1. trames de bruit = hors de la voix (détecteur Silero) ; à défaut, les 12 % les moins énergiques
    voix = np.zeros(len(t), bool)
    for a, b in zones:
        voix[(t >= a) & (t <= b)] = True
    bruit = ~voix
    if bruit.sum() < int(1.5 * SR / hop):
        e_l = uniform_filter1d(db.mean(0), 9)
        bruit = e_l <= np.quantile(e_l, 0.12)
    mu = db[:, bruit].mean(1, keepdims=True)
    sd = db[:, bruit].std(1, keepdims=True)
    # 2. sous la voix : soustraction spectrale de l'empreinte du bruit (clim, ventilateur, souffle), lissée
    #    (anti « musical noise ») — elle n'enlève que le bruit et ne coupe jamais une partie de la voix
    plancher = 10 ** (plancher_db / 20)
    nmag = 10 ** ((mu + 0.5 * np.minimum(sd, 6)) / 20)
    sur = np.where(f[:, None] < 300, 2.0, 1.4) * force    # sur-soustraction plus forte dans les graves
    sous = np.maximum(mag - sur * nmag, plancher * mag) / mag
    G = np.clip(uniform_filter(sous, size=(3, 5)), plancher, 1.0)
    _, y = istft(Z * G, SR, nperseg=n_fft, noverlap=n_fft - hop)
    y = y[:len(x)]
    if len(y) < len(x):
        y = np.pad(y, (0, len(x) - len(y)))
    # 4. hors de la voix : silence (bruits ponctuels, claquements, sifflements, ronflement)
    env = np.full(len(x), 10 ** (silence_db / 20))
    for a, b in zones:
        env[int(a * SR):int(b * SR)] = 1.0
    k = int(0.04 * SR)   # rampes de 40 ms : pas de coupure sèche
    env = np.convolve(env, np.ones(k) / k, "same")
    return y * env, float(np.mean(mu)), bruit


def mesure(x):
    """Niveau des silences (bruit résiduel) et de la voix, en dB."""
    hop = 480
    n = len(x) // hop
    r = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, 1)) + 1e-12
    d = 20 * np.log10(r)
    return float(np.quantile(d, 0.10)), float(np.quantile(d, 0.90))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entree")
    ap.add_argument("sortie")
    ap.add_argument("--force", type=float, default=1.0)
    ap.add_argument("--plancher", type=float, default=-35.0)
    ap.add_argument("--canal", default=None, help="c0, c1 ou 0.5*c0+0.5*c1 (sinon mélange mono)")
    ap.add_argument("--extrait", nargs=2, metavar=("DEBUT:FIN", "WAV"), help="écrit aussi un avant/après de contrôle")
    a = ap.parse_args()
    x = lire(a.entree, a.canal)
    y, _, _ = nettoyer(x, a.force, a.plancher)
    ecrire(a.sortie, y)
    b0, v0 = mesure(x)
    b1, v1 = mesure(y)
    print(f"bruit de fond {b0:.1f} dB → {b1:.1f} dB ({b1 - b0:+.1f} dB) ; voix {v0:.1f} → {v1:.1f} dB")
    if a.extrait:
        s, e = (float(v) for v in a.extrait[0].split(":"))
        i0, i1 = int(s * SR), int(e * SR)
        ab = np.concatenate([x[i0:i1], np.zeros(SR // 2), y[i0:i1]])
        ecrire(a.extrait[1], ab / max(1e-6, np.abs(ab).max()) * 0.8)
        print(f"avant/après : {a.extrait[1]}")


if __name__ == "__main__":
    main()
