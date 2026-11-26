"""Musique de fond et bruitages générés (aucune source externe, libre de droits)."""
import wave
import numpy as np

SR = 48000
NOTE = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def hz(name, octave):
    return 440.0 * 2 ** ((NOTE[name] + 12 * (octave - 4) - 9) / 12)


def save(path, x):
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    w = wave.open(path, "wb")
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes())
    w.close()


def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):  # petites longueurs seulement
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


# ---------------------------------------------------------------------------
# Musique : nappe + arpège + basse douce, 92 BPM, La mineur (Am F C G)
# ---------------------------------------------------------------------------
MUSIQUES = [  # (bpm, grille, motif d'arpège, charleston, grosse caisse) — varier d'une vidéo à l'autre
    (92, [("A", ["A", "C", "E", "G"]), ("F", ["F", "A", "C", "E"]), ("C", ["C", "E", "G", "B"]), ("G", ["G", "B", "D", "F#"])],
     (0, 1, 2, 3, 2, 1, 2, 3), True, False),
    (100, [("D", ["D", "F", "A", "C"]), ("A#", ["A#", "D", "F", "A"]), ("F", ["F", "A", "C", "E"]), ("C", ["C", "E", "G", "A#"])],
     (0, 2, 1, 3, 0, 2, 1, 3), True, True),
    (84, [("E", ["E", "G", "B", "D"]), ("C", ["C", "E", "G", "B"]), ("G", ["G", "B", "D", "F#"]), ("D", ["D", "F#", "A", "C#"])],
     (0, 1, 2, 1, 3, 1, 2, 1), False, False),
    (96, [("C", ["C", "D#", "G", "A#"]), ("G#", ["G#", "C", "D#", "G"]), ("D#", ["D#", "G", "A#", "D"]), ("A#", ["A#", "D", "F", "A"])],
     (0, 2, 3, 2, 1, 2, 3, 2), True, True),
    (104, [("F#", ["F#", "A", "C#", "E"]), ("D", ["D", "F#", "A", "C#"]), ("A", ["A", "C#", "E", "G#"]), ("E", ["E", "G#", "B", "D"])],
     (0, 1, 2, 3, 0, 1, 2, 3), True, False),
    (88, [("G", ["G", "A#", "D", "F"]), ("D#", ["D#", "G", "A#", "D"]), ("A#", ["A#", "D", "F", "A"]), ("F", ["F", "A", "C", "E"])],
     (3, 2, 1, 0, 1, 2, 3, 2), False, True),
]


def music(duration, end_card_at, style=0):
    n = int(duration * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    bpm, prog, motif, hats, kick = MUSIQUES[style % len(MUSIQUES)]
    beat = 60 / bpm
    bar = 4 * beat
    nbars = int(duration / bar) + 2
    rng = np.random.default_rng(7)
    for b in range(nbars):
        root, notes = prog[b % 4]
        t0 = b * bar
        i0, i1 = int(t0 * SR), min(n, int((t0 + bar + 0.6) * SR))
        if i0 >= n:
            break
        tt = np.arange(i1 - i0) / SR
        env = np.minimum(1, tt / 0.5) * np.minimum(1, np.maximum(0, (bar + 0.6 - tt) / 0.6))
        # nappe : harmoniques douces, légèrement désaccordées
        for j, nn in enumerate(notes):
            f = hz(nn, 3 if j == 0 else 4)
            for det, pan in ((-0.12, 0.3), (0.12, 0.7)):
                sig = sum(np.sin(2 * np.pi * (f + det) * h * tt + j) / h ** 1.8 for h in range(1, 6))
                out[i0:i1, 0] += 0.018 * sig * env * (1 - pan)
                out[i0:i1, 1] += 0.018 * sig * env * pan
        # basse sur les temps 1 et 3
        for k in (0, 2):
            s = int((t0 + k * beat) * SR)
            L = int(0.9 * SR)
            if s >= n:
                continue
            L = min(L, n - s)
            tb = np.arange(L) / SR
            f = hz(root, 2)
            sig = (np.sin(2 * np.pi * f * tb) + 0.3 * np.sin(4 * np.pi * f * tb)) * np.exp(-tb * 3.5) * np.minimum(1, tb / 0.01)
            out[s:s + L] += 0.10 * sig[:, None]
        # arpège en croches
        arp = [notes[i % 4] for i in motif]
        for k, nn in enumerate(arp):
            s = int((t0 + k * beat / 2) * SR)
            if s >= n:
                continue
            L = min(int(0.6 * SR), n - s)
            tp = np.arange(L) / SR
            f = hz(nn, 5)
            sig = (np.sin(2 * np.pi * f * tp) + 0.25 * np.sin(4 * np.pi * f * tp)) * np.exp(-tp * 7) * np.minimum(1, tp / 0.004)
            pan = 0.35 if k % 2 == 0 else 0.65
            out[s:s + L, 0] += 0.035 * sig * (1 - pan)
            out[s:s + L, 1] += 0.035 * sig * pan
            d = int(beat * 0.75 * SR)  # écho ping-pong
            if s + d + L < n:
                out[s + d:s + d + L, 0] += 0.012 * sig * pan
                out[s + d:s + d + L, 1] += 0.012 * sig * (1 - pan)
        if kick:   # grosse caisse douce sur chaque temps
            for k in range(4):
                s = int((t0 + k * beat) * SR)
                if s >= n:
                    continue
                L = min(int(0.25 * SR), n - s)
                tk = np.arange(L) / SR
                out[s:s + L] += (0.08 * np.sin(2 * np.pi * (55 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 14))[:, None]
        # hi-hat doux sur les contretemps
        for k in range(4 if hats else 0):
            s = int((t0 + (k + 0.5) * beat) * SR)
            if s >= n:
                continue
            L = min(int(0.05 * SR), n - s)
            noise = rng.standard_normal(L)
            noise = noise - np.convolve(noise, np.ones(6) / 6, "same")
            out[s:s + L] += (0.012 * noise * np.exp(-np.arange(L) / SR * 80))[:, None]
    # montée en fin de vidéo, fondu d'entrée et de sortie
    gain = np.ones(n)
    ec = int(end_card_at * SR)
    gain[ec:] = np.minimum(1.9, 1 + (np.arange(n - ec) / SR) / 0.6 * 0.9)
    gain *= np.minimum(1, t / 0.8)
    gain *= np.minimum(1, np.maximum(0, (duration - t) / 1.8))
    return out * gain[:, None]


# ---------------------------------------------------------------------------
# Bruitages
# ---------------------------------------------------------------------------
def whoosh(d=0.5, rng=np.random.default_rng(1)):
    L = int(d * SR)
    tt = np.arange(L) / SR
    x = rng.standard_normal(L)
    # filtre passe-bas qui s'ouvre puis se referme
    out = np.zeros(L)
    acc = 0.0
    for i in range(L):
        p = tt[i] / d
        fc = 300 + 5000 * np.sin(np.pi * p) ** 2
        a = np.exp(-2 * np.pi * fc / SR)
        acc = (1 - a) * x[i] + a * acc
        out[i] = acc
    env = np.sin(np.pi * np.minimum(1, tt / d)) ** 1.5
    y = out * env
    y /= np.abs(y).max() + 1e-9
    pan = np.linspace(0.2, 0.8, L)
    return 0.22 * np.stack([y * (1 - pan) * 1.4, y * pan * 1.4], 1)


def pop(f0=900, f1=450):
    L = int(0.09 * SR)
    tt = np.arange(L) / SR
    f = f0 + (f1 - f0) * (tt / tt[-1])
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-tt * 45) * np.minimum(1, tt / 0.002)
    return 0.20 * np.stack([y, y], 1)


def impact(rng=np.random.default_rng(3)):
    L = int(0.7 * SR)
    tt = np.arange(L) / SR
    f = 42 + 70 * np.exp(-tt * 18)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 5)
    n = rng.standard_normal(L) * np.exp(-tt * 40)
    n = np.convolve(n, np.ones(12) / 12, "same")
    y = np.tanh(1.6 * (body + 0.8 * n))
    return 0.42 * np.stack([y, y], 1)


def tick():
    L = int(0.03 * SR)
    tt = np.arange(L) / SR
    y = np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 220)
    return 0.08 * np.stack([y, y], 1)


def click():
    L = int(0.04 * SR)
    tt = np.arange(L) / SR
    y = (np.sin(2 * np.pi * 3200 * tt) + 0.5 * np.sin(2 * np.pi * 1200 * tt)) * np.exp(-tt * 180)
    return 0.16 * np.stack([y, y], 1)


def ding():
    L = int(1.2 * SR)
    tt = np.arange(L) / SR
    y = (np.sin(2 * np.pi * 1318 * tt) + 0.5 * np.sin(2 * np.pi * 1976 * tt) + 0.2 * np.sin(2 * np.pi * 2637 * tt))
    y *= np.exp(-tt * 3.5) * np.minimum(1, tt / 0.003)
    return 0.12 * np.stack([y, y], 1)


SFX = {"whoosh": whoosh, "pop": pop, "impact": impact, "tick": tick, "click": click, "ding": ding}


def sfx_track(duration, events):
    n = int(duration * SR)
    out = np.zeros((n, 2))
    cache = {}
    for t, kind in events:
        if kind not in cache:
            cache[kind] = SFX[kind]()
        s = cache[kind]
        i = int(t * SR)
        if i < 0 or i >= n:
            continue
        L = min(len(s), n - i)
        out[i:i + L] += s[:L]
    return out


# ---------------------------------------------------------------------------
# Bruitages supplémentaires (v3)
# ---------------------------------------------------------------------------
def _ir(seconds=1.4, seed=11):
    rng = np.random.default_rng(seed)
    L = int(seconds * SR)
    tt = np.arange(L) / SR
    ir = rng.standard_normal((L, 2)) * np.exp(-tt * 4.2)[:, None]
    ir[:, 0] = np.convolve(ir[:, 0], np.ones(8) / 8, "same")
    ir[:, 1] = np.convolve(ir[:, 1], np.ones(8) / 8, "same")
    ir[0] = 1.0
    return ir / np.abs(ir).sum(0) * 6


def reverb(x, wet=0.25, seconds=1.4):
    ir = _ir(seconds)
    n = len(x) + len(ir) - 1
    N = 1 << (n - 1).bit_length()
    y = np.zeros((n, 2))
    for c in range(2):
        y[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], N) * np.fft.rfft(ir[:, c], N), N)[:n]
    y = y / (np.abs(y).max() + 1e-9) * np.abs(x).max()
    out = np.zeros_like(y)
    out[:len(x)] = x * (1 - wet)
    return out + y * wet


def swish(d=0.28):
    return whoosh(d, np.random.default_rng(5)) * 0.6


def riser(d=0.9, rng=np.random.default_rng(8)):
    L = int(d * SR)
    tt = np.arange(L) / SR
    x = rng.standard_normal(L)
    out = np.zeros(L)
    acc = 0.0
    for i in range(L):
        fc = 200 + 7000 * (tt[i] / d) ** 2
        a = np.exp(-2 * np.pi * fc / SR)
        acc = (1 - a) * x[i] + a * acc
        out[i] = acc
    f = 180 + 900 * (tt / d) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35
    env = (tt / d) ** 2.2
    y = (out / (np.abs(out).max() + 1e-9) + tone) * env
    return 0.18 * np.stack([y, y], 1)


def boom():
    return reverb(impact() * 1.1, wet=0.35, seconds=1.8)


def coin(seed=0):
    L = int(0.45 * SR)
    tt = np.arange(L) / SR
    rng = np.random.default_rng(seed)
    base = 2100 * (1 + 0.03 * rng.standard_normal())
    y = np.zeros(L)
    for ratio, amp, dec in ((1, 1, 14), (1.62, .7, 18), (2.47, .5, 22), (3.28, .35, 28), (4.1, .2, 35)):
        y += amp * np.sin(2 * np.pi * base * ratio * tt + rng.uniform(0, 6)) * np.exp(-tt * dec)
    y *= np.minimum(1, tt / 0.0015)
    y /= np.abs(y).max()
    return 0.13 * np.stack([y * .9, y], 1)


def paper(rng=np.random.default_rng(12)):
    L = int(0.35 * SR)
    tt = np.arange(L) / SR
    x = rng.standard_normal(L)
    x = x - np.convolve(x, np.ones(20) / 20, "same")
    env = np.exp(-tt * 9) * (0.6 + 0.4 * np.sin(tt * 90) ** 2)
    y = x * env
    y /= np.abs(y).max()
    return 0.08 * np.stack([y, y], 1)


def fail():
    L = int(0.8 * SR)
    tt = np.arange(L) / SR
    f = 700 * np.exp(-tt * 3.2) + 70
    y = np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-tt * 2.6)
    return reverb(0.16 * np.stack([y, y], 1), wet=.3)


def shimmer():
    L = int(1.3 * SR)
    tt = np.arange(L) / SR
    y = np.zeros(L)
    notes = [1568, 1976, 2349, 2637, 3136, 3951]
    for i, f in enumerate(notes):
        s = int(i * 0.07 * SR)
        seg = tt[:L - s]
        y[s:] += np.sin(2 * np.pi * f * seg) * np.exp(-seg * 4) * 0.5
    y /= np.abs(y).max()
    return reverb(0.09 * np.stack([y, np.roll(y, 300)], 1), wet=.45)


def tock():
    L = int(0.06 * SR)
    tt = np.arange(L) / SR
    y = np.sin(2 * np.pi * 1300 * tt) * np.exp(-tt * 120) + 0.5 * np.sin(2 * np.pi * 650 * tt) * np.exp(-tt * 90)
    return 0.10 * np.stack([y, y], 1)


def thud():
    L = int(0.35 * SR)
    tt = np.arange(L) / SR
    f = 55 + 90 * np.exp(-tt * 30)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 12)
    return 0.30 * np.stack([y, y], 1)


SFX.update({"swish": swish, "riser": riser, "boom": boom, "coin0": lambda: coin(0), "coin1": lambda: coin(1),
            "coin2": lambda: coin(2), "paper": paper, "fail": fail, "shimmer": shimmer, "tock": tock,
            "thud": thud, "whoosh": lambda: reverb(whoosh(), wet=.2), "ding": lambda: reverb(ding(), wet=.3)})


def flashhit(rng=np.random.default_rng(21)):
    L = int(0.5 * SR)
    tt = np.arange(L) / SR
    n = rng.standard_normal(L)
    n = n - np.convolve(n, np.ones(4) / 4, "same")
    y = n * np.exp(-tt * 18) * 0.7 + np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 30) * 0.3
    y /= np.abs(y).max()
    return reverb(0.12 * np.stack([y, y], 1), wet=0.35)


def glitch(rng=np.random.default_rng(22)):
    L = int(0.36 * SR)
    y = np.zeros(L)
    for k, on in enumerate([1, 1, 0, 1, 0, 1, 1, 0, 1]):
        if on:
            s = int(k / 24 * SR)
            seg = min(int(0.03 * SR), L - s)
            y[s:s + seg] += np.sign(np.sin(2 * np.pi * (900 + 300 * k) * np.arange(seg) / SR)) * np.exp(-np.arange(seg) / SR * 90)
    return 0.05 * np.stack([y, y], 1)


SFX.update({"flashhit": flashhit, "glitch": glitch})
