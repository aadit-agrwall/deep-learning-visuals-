#!/usr/bin/env python3
"""Retro spy-thriller score in E minor (electric guitar + piano), synced to
the rendered video: wipes are detected from the video itself."""
import argparse, struct, subprocess
import numpy as np

BEAT = 0.55                     # locked pace (109 BPM)
PPQ = 480
TPS = PPQ / BEAT                # ticks per second

CHORDS = [  # (piano chord, bass note)
    ([52, 55, 59, 63], 40),     # Em(maj7)
    ([52, 55, 59, 62], 40),     # Em7
    ([48, 52, 55, 59], 36),     # Cmaj7
    ([47, 51, 54, 57], 35),     # B7
]
RIFF = [  # per bar: (beat, midi, dur_beats), E harmonic minor, chromatic fall
    [(0, 64, .75), (1, 67, .25), (1.5, 71, .5), (2, 70, .5), (2.5, 69, .5), (3, 67, 1)],
    [(0, 64, .75), (1, 67, .25), (1.5, 71, .5), (2, 70, .5), (2.5, 69, .5), (3, 66, 1)],
    [(0, 67, .5), (.5, 64, .5), (1, 60, 1), (2.5, 64, .5), (3, 67, 1)],
    [(0, 63, .5), (.5, 66, .5), (1, 69, .5), (1.5, 66, .5), (2, 63, .5),
     (2.5, 66, .5), (3, 71, .5), (3.5, 70, .5)],
]


def analyze(video, fps=20, size=108):
    cmd = ["ffmpeg", "-v", "error", "-i", video, "-vf",
           f"fps={fps},scale={size}:{size},format=gray",
           "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (size * size)
    fr = np.frombuffer(raw[:n * size * size], dtype=np.uint8)
    fr = fr.reshape(n, size, size).astype(np.int16)
    diff = (np.abs(fr[1:] - fr[:-1]) > 25).mean(axis=(1, 2))
    return diff, n / fps, fps


def find_wipes(diff, fps, dur, k):
    w = max(1, int(0.6 * fps))
    sm = np.convolve(diff, np.ones(w) / w, mode="same")
    picked = []
    for i in np.argsort(sm)[::-1]:
        t = (i + 1) / fps
        if t < 2.0 or t > dur - 3.0:
            continue
        if all(abs(t - p) > 3.5 for p in picked):
            picked.append(t)
        if len(picked) == k:
            break
    return sorted(picked)


class Midi:
    def __init__(self):
        self.ev = []   # (tick, order, bytes)

    def add(self, t, order, data):
        self.ev.append((int(round(t * TPS)), order, bytes(data)))

    def note(self, ch, p, t, d, v):
        v = int(max(1, min(127, v)))
        self.add(t, 1, [0x90 | ch, p, v])
        self.add(t + max(d, 0.05), 0, [0x80 | ch, p, 0])

    def save(self, path):
        self.ev.sort(key=lambda e: (e[0], e[1]))
        out, last = bytearray(), 0
        out += b"\x00\xff\x51\x03" + int(BEAT * 1e6).to_bytes(3, "big")
        for tick, _, data in self.ev:
            out += vlq(tick - last) + data
            last = tick
        out += b"\x00\xff\x2f\x00"
        with open(path, "wb") as f:
            f.write(b"MThd" + struct.pack(">IHHH", 6, 0, 1, PPQ))
            f.write(b"MTrk" + struct.pack(">I", len(out)) + out)


def vlq(n):
    b = [n & 0x7F]
    n >>= 7
    while n:
        b.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", required=True)
    ap.add_argument("--wipes", default="", help="manual wipe times, e.g. 5.4,12,20")
    ap.add_argument("--k", type=int, default=5, help="number of dust wipes")
    ap.add_argument("--events", default="assets/audio/raw/page_111_events.json")
    a = ap.parse_args()

    diff, dur, fps = analyze(a.video)
    if a.wipes:
        wipes = sorted(float(x) for x in a.wipes.split(","))
    else:
        wipes = find_wipes(diff, fps, dur, a.k)
    import json, os
    typing = []
    if os.path.exists(a.events):
        ev = json.load(open(a.events))
        if not a.wipes:
            wl = sorted((e["t0"] + e["t1"]) / 2 for e in ev if e["kind"] == "wipe")
            if wl:
                wipes = wl
        typing = [(e["t0"], e["t1"], e["n"]) for e in ev if e["kind"] == "type"]
    else:
        print("No events log found: no typing sounds, wipes detected from video")
    print(f"Video {dur:.1f}s | wipes at: " + ", ".join(f"{w:.1f}s" for w in wipes)
          + f" | typing lines: {len(typing)}")

    m = Midi()
    PIANO, GTR, CHUG, FX, DRUM = 0, 1, 2, 3, 9
    for ch, prog in ((PIANO, 0), (GTR, 27), (CHUG, 28), (FX, 119), (4, 0), (5, 27)):
        m.add(0, 2, [0xC0 | ch, prog])
    for ch, rev, vol in ((PIANO, 45, 100), (GTR, 90, 112), (CHUG, 60, 95),
                         (FX, 80, 100), (DRUM, 35, 105), (4, 40, 85), (5, 40, 85)):
        m.add(0, 2, [0xB0 | ch, 91, rev])
        m.add(0, 2, [0xB0 | ch, 7, vol])

    limit = dur - 1.8     # ordinary music stops here; final hit follows

    TYPING_DUCK = 0.88

    def typing_now(t):
        return any(t0 - 0.1 <= t <= t1 + 0.1 for t0, t1, _ in typing)

    def note(ch, p, t, d, v):
        if 0 <= t < limit:
            if typing_now(t):
                v = v * TYPING_DUCK
            m.note(ch, p, t, min(d, limit - t + 0.3), v)

    def level(t):
        return min(sum(1 for w in wipes if w <= t), 4)

    bar_len = 4 * BEAT
    b = 0
    while b * bar_len < limit:
        b0 = b * bar_len
        lvl = level(b0)
        chord, bass = CHORDS[b % 4]
        for beat in range(4):                                   # bass pedal
            note(PIANO, bass, b0 + beat * BEAT, BEAT * .9, 52 + lvl * 4)
        for beat, dd in ((0, 1.8), (2.5, .4), (3.5, .4)):       # piano stabs
            for p in chord:
                note(PIANO, p, b0 + beat * BEAT, dd * BEAT, 58 + lvl * 7)
        if lvl >= 1:                                            # guitar riff
            for beat, p, dd in RIFF[b % 4]:
                note(GTR, p, b0 + beat * BEAT, dd * BEAT * .95, 82 + lvl * 4)
        if lvl >= 2:                                            # drums
            for beat in (0, 2):
                note(DRUM, 36, b0 + beat * BEAT, .1, 100)
            for beat in (1, 3):
                note(DRUM, 37, b0 + beat * BEAT, .1, 90)
            step = .5 if lvl >= 3 else 1
            x = 0
            while x < 4:
                note(DRUM, 42, b0 + x * BEAT, .05, 62)
                x += step
        if lvl >= 3:                                            # muted chug
            for i in range(8):
                note(CHUG, chord[0] - 12 + (0 if i % 4 else 0),
                     b0 + i * BEAT / 2, BEAT * .3, 60)
        b += 1

    for w in wipes:                       # transition sync points
        m.note(FX, 60, max(0, w - 1.3), 1.3, 100)               # reverse cymbal
        m.note(DRUM, 49, w, .5, 105)                            # crash
        for p in (52, 55, 59, 63):
            m.note(PIANO, p, w, .8, 95)                         # stab
        for i, p in enumerate((64, 67, 71, 75)):                # rising arpeggio
            m.note(PIANO, p, w + .25 + i * .15, .3, 72)
        for p in (52, 59, 63):
            m.note(GTR, p, w, .8, 100)

    t_end = max(0, dur - 1.7)             # final Em(maj7) hit
    for p in (40, 52, 55, 59, 63, 76):
        m.note(PIANO, p, t_end, 2.2, 105)
    for p in (52, 59, 63, 67):
        m.note(GTR, p, t_end, 2.0, 100)
    m.note(DRUM, 49, t_end, 1.5, 110)

    STEP = BEAT / 2                       # same 8th-note grid as the guitar riff
    ORDER = [0, 1, 2, 3, 2, 1]            # chord-tone melody pattern
    rng = np.random.default_rng(112)
    total = 0
    for t0, t1, n in typing:
        g0 = int(np.ceil(t0 / STEP))
        g1 = max(int(np.floor(t1 / STEP)), g0)
        for g in range(g0, g1 + 1):
            t = g * STEP
            chord, _bass = CHORDS[int(t // bar_len) % 4]
            pitch = chord[ORDER[g % 6]]   # low register, follows the chord
            v = 58 + int(rng.integers(0, 7))   # soft piano only
            m.note(4, pitch, t, STEP * 2.0, v)            # low piano
            total += 1
        print(f"  typing {t0:5.1f}s -> {t1:5.1f}s : {g1 - g0 + 1} melody notes")
    print(f"Total typing-melody notes: {total}")

    m.save(a.out)
    print("Wrote", a.out)


if __name__ == "__main__":
    main()
