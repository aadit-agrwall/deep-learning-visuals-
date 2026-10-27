#!/usr/bin/env python3
"""Spy-thriller score: 5/4, ~168 BPM, E minor -> G minor (up a minor third).
Each video scene is a section; the tempo of every section is bent slightly so
its bar lines land exactly on the dust-wipes. Needs the page's events json."""
import argparse, json, struct, subprocess
import numpy as np

BEAT0 = 60.0 / 168.0
BAR = 5
PPQ = 480
BASS, LEAD, BRASS, STR, FLUTE, PIANO, RCYM, TREM, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9

MOTIF = [
    [(0, 0, .5), (.5, 3, .5), (1.5, 2, .5), (2, 0, 1), (3.5, -1, .5),
     (4, -2, .5), (4.5, -1, .5)],
    [(0, 0, .5), (.5, 3, .5), (1.5, 5, .5), (2, 3, .5), (2.5, 2, .5),
     (3, 0, 1.5), (4.5, -5, .5)],
]
BASS_P = [(0, 0, .5), (1, 0, .5), (1.5, 7, .5), (2.5, 0, .5), (3, 3, .5),
          (3.5, 5, .5), (4, 6, .4), (4.5, 7, .4)]
CH = [(0, [0, 3, 7, 11]), (0, [0, 3, 7, 10]),
      (-4, [0, 4, 7, 11]), (-5, [0, 4, 7, 10])]
BONGO = [(.5, 60), (1.5, 61), (2.5, 60), (3, 60), (3.5, 61), (4.5, 60)]
CONGA = [(0, 64), (1, 62), (2, 62), (2.5, 63), (4, 64)]


def vlq(n):
    b = [n & 0x7F]
    n >>= 7
    while n:
        b.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(b))


def video_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True, check=True).stdout
    return float(out.strip())


class Timeline:
    def __init__(self, bounds):
        self.segs, b = [], 0.0
        for t0, t1 in zip(bounds[:-1], bounds[1:]):
            d = t1 - t0
            n = max(1, round(d / (BAR * BEAT0)))
            self.segs.append(dict(t0=t0, t1=t1, b0=b, bars=n, beats=n * BAR,
                                  mpb=d / (n * BAR)))
            b += n * BAR
        self.total = b

    def sec2beat(self, t):
        t = max(0.0, t)
        for s in self.segs:
            if t < s["t1"]:
                return s["b0"] + (t - s["t0"]) / s["mpb"]
        s = self.segs[-1]
        return s["b0"] + (t - s["t0"]) / s["mpb"]

    def seg_index(self, beat):
        for i, s in enumerate(self.segs):
            if beat < s["b0"] + s["beats"]:
                return i
        return len(self.segs) - 1


class Midi:
    def __init__(self, tl):
        self.tl, self.ev = tl, []

    def raw(self, beat, order, data):
        self.ev.append((int(round(beat * PPQ)), order, bytes(data)))

    def note(self, ch, p, beat, dur, vel):
        p = int(p)
        if not 0 <= p <= 127:
            return
        vel = int(max(1, min(127, vel)))
        self.raw(beat, 1, [0x90 | ch, p, vel])
        self.raw(beat + max(dur, 0.05), 0, [0x80 | ch, p, 0])

    def save(self, path, end_beat):
        evs = list(self.ev)
        for s in self.tl.segs:
            evs.append((int(round(s["b0"] * PPQ)), -2,
                        b"\xff\x51\x03" + int(s["mpb"] * 1e6).to_bytes(3, "big")))
        evs.sort(key=lambda e: (e[0], e[1]))
        out, last = bytearray(), 0
        for tick, _, data in evs:
            out += vlq(tick - last) + data
            last = tick
        end_tick = max(last, int(round(end_beat * PPQ)))
        out += vlq(end_tick - last) + b"\xff\x2f\x00"
        with open(path, "wb") as f:
            f.write(b"MThd" + struct.pack(">IHHH", 6, 0, 1, PPQ))
            f.write(b"MTrk" + struct.pack(">I", len(out)) + out)


def assign_roles(n):
    if n <= 1:
        return ["climax"]
    roles = ["intro"] + [""] * (n - 1)
    k = 2 if n >= 5 else 1
    for i in range(n - k, n):
        roles[i] = "climax"
    mid = list(range(1, n - k))
    if len(mid) >= 2:
        roles[mid.pop()] = "build"
    half = (len(mid) + 1) // 2
    for j, i in enumerate(mid):
        roles[i] = "theme" if j < half else "brass"
    return roles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--events", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    dur = video_duration(a.video)
    ev = json.load(open(a.events))
    wipes = sorted((e["t0"] + e["t1"]) / 2 for e in ev if e["kind"] == "wipe")
    wipes = [w for w in wipes if 1.5 < w < dur - 2.0]
    typing = [(e["t0"], e["t1"]) for e in ev if e["kind"] == "type"]
    pulses = [e["t0"] for e in ev if e["kind"] == "pulse"]
    t_hit = pulses[-1] if pulses else dur - 1.5
    if t_hit <= (wipes[-1] if wipes else 0) + 1.0 or t_hit > dur - 0.3:
        t_hit = dur - 1.5

    bounds = [0.0] + wipes + [t_hit, dur]
    tl = Timeline(bounds)
    n_sec = len(bounds) - 2
    roles = assign_roles(n_sec)
    hit_b = tl.segs[-1]["b0"]

    print(f"Video {dur:.1f}s | final hit at {t_hit:.1f}s | {n_sec} sections")
    for i in range(n_sec):
        s = tl.segs[i]
        print(f"  section {i}: {roles[i]:6s} {s['t0']:5.1f}s  "
              f"{s['bars']} bars  {60 / s['mpb']:.0f} BPM")

    m = Midi(tl)
    progs = {BASS: 33, LEAD: 81, BRASS: 61, STR: 48, FLUTE: 73, PIANO: 0,
             RCYM: 119, TREM: 44}
    vols = {BASS: 110, LEAD: 100, BRASS: 105, STR: 85, FLUTE: 95, PIANO: 105,
            RCYM: 90, TREM: 80, DR: 115}
    for ch, pr in progs.items():
        m.raw(0, -1, [0xC0 | ch, pr])
    for ch, v in vols.items():
        m.raw(0, -1, [0xB0 | ch, 7, v])
        m.raw(0, -1, [0xB0 | ch, 91, 55])

    N = m.note
    for si in range(n_sec):
        seg, role = tl.segs[si], roles[si]
        sh = 3 if role == "climax" else 0
        for bar in range(seg["bars"]):
            b0 = seg["b0"] + bar * BAR
            g = int(round(b0 / BAR))
            off, iv = CH[g % 4]
            rb = 52 + sh + off
            last_bar = bar == seg["bars"] - 1
            prog = (bar * BAR) / seg["beats"]
            M = MOTIF[g % 2]

            # bass ostinato
            bv = {"intro": 62, "theme": 84, "brass": 90, "build": 88,
                  "climax": 100}[role]
            if role == "build":
                for k in range(10):
                    N(BASS, 40 + sh, b0 + k * .5, .45, bv + int(prog * 25))
            else:
                for b, s, d in BASS_P:
                    N(BASS, 40 + sh + off + s, b0 + b, d,
                      bv + (8 if b == 0 else 0))

            # bongos + congas
            if role != "build":
                pv = 78 if role == "intro" else 62
                for b, p in BONGO:
                    N(DR, p, b0 + b, .1, pv + (6 if p == 60 else 0))
                for b, p in CONGA:
                    N(DR, p, b0 + b, .15, pv)

            # kit
            if role == "intro":
                for b in (1, 3):
                    N(DR, 37, b0 + b, .1, 52)
            elif role in ("theme", "brass", "climax"):
                kv = {"theme": 92, "brass": 100, "climax": 115}[role]
                for b in (0, 2, 3.5):
                    N(DR, 36, b0 + b, .1, kv)
                for b in (1, 3):
                    N(DR, 38, b0 + b, .1, kv - 4)
                N(DR, 38, b0 + 4.5, .1, 48)
                for k in range(10):
                    base = 66 if k % 2 else 80
                    N(DR, 42, b0 + k * .5, .05,
                      base - (10 if role == "theme" else 0))
                if role == "climax":
                    for b in range(5):
                        N(DR, 51, b0 + b, .2, 70)
                if last_bar:
                    for j, b in enumerate((3.5, 4, 4.25, 4.5, 4.75)):
                        N(DR, [50, 47, 45, 43, 41][j], b0 + b, .2, 85 + 5 * j)
            elif role == "build":
                N(DR, 36, b0, .1, 95)
                if last_bar:
                    for k in range(20):
                        N(DR, 38, b0 + k * .25, .1, 60 + k * 3)
                else:
                    dens = .5 if prog < .5 else .25
                    for k in range(int(BAR / dens)):
                        v = 55 + int(((bar * BAR + k * dens) / seg["beats"]) * 65)
                        tom = ([45, 43, 41, 47][k % 4] if dens == .5
                               else [50, 48, 47, 45, 43, 41][k % 6])
                        N(DR, tom, b0 + k * dens, dens * .8, v)

            # string pad / tremolo
            if role == "build":
                for k in range(5):
                    pch = 55 + int(((bar * BAR + k) / seg["beats"]) * 14)
                    N(LEAD, pch, b0 + k, .9, 68 + int(prog * 35))
                    N(TREM, pch - 12, b0 + k, 1.0, 60 + int(prog * 45))
            else:
                sv = {"intro": 34, "theme": 50, "brass": 56, "climax": 78}[role]
                for i in iv:
                    N(STR, rb + 12 + i, b0, BAR, sv)

            # motif voices
            if role == "intro" and last_bar:
                for b, s, d in MOTIF[0][:3]:
                    N(FLUTE, 76 + s, b0 + b, d, 58)
            if role == "theme":
                for b, s, d in M:
                    N(LEAD, 76 + s, b0 + b, d * .9, 96)
            if role == "brass":
                for b, s, d in M:
                    N(BRASS, 64 + s, b0 + b, d * .9, 104)
            if role == "climax":
                for b, s, d in M:
                    N(LEAD, 76 + sh + s, b0 + b, d * .9, 108)
                    N(BRASS, 64 + sh + s, b0 + b, d * .9, 112)
                    N(FLUTE, 88 + sh + s, b0 + b, d * .9, 80)

            # staccato brass stabs + flute counter-melody
            if role in ("brass", "climax"):
                for b in (1, 3.5):
                    for i in iv:
                        N(BRASS, rb + 12 + i, b0 + b, .25, 96)
                top = 12 if role == "brass" else 24
                N(FLUTE, rb + top + iv[2], b0, 2.5, 78)
                N(FLUTE, rb + top + iv[3], b0 + 2.5, 2.5, 78)

            # section downbeat hit
            if bar == 0 and si >= 1:
                N(DR, 49, b0, 1.5, 110)
                N(DR, 36, b0, .2, 110)

    # reverse cymbal into every section boundary and the final hit
    for s in tl.segs[1:]:
        if s["t0"] > 1.4:
            sb = tl.sec2beat(s["t0"] - 1.3)
            m.note(RCYM, 60, sb, s["b0"] - sb, 100)

    # soft typing melody (piano only), on the 8th-note grid
    total_typing = 0
    for t0, t1 in typing:
        ba, bb = tl.sec2beat(t0), tl.sec2beat(t1)
        g0 = int(np.ceil(ba * 2))
        g1 = max(int(np.floor(bb * 2)), g0)
        for g in range(g0, g1 + 1):
            beat = g / 2.0
            if beat >= hit_b:
                break
            idx = tl.seg_index(beat)
            sh = 3 if (idx < n_sec and roles[idx] == "climax") else 0
            off, iv = CH[int(beat // BAR) % 4]
            pitch = 52 + sh + off + iv[[0, 1, 2, 3, 2, 1][g % 6]]
            N(PIANO, pitch, beat, 1.0, 62 + (g * 7) % 5)
            total_typing += 1
    print(f"Typing-melody notes: {total_typing}")

    # sharp final hit: Gm(maj7)
    ring = max(0.5, min(4.0, tl.total - hit_b - 0.05))
    for p in (43, 55, 58, 62, 66):
        N(BRASS, p, hit_b, min(ring, 2.0), 120)
    for p in (55, 58, 62, 66, 70):
        N(STR, p, hit_b, ring, 100)
    for p in (43, 55, 62, 70):
        N(PIANO, p, hit_b, ring, 100)
    N(BASS, 43, hit_b, ring, 118)
    N(LEAD, 79, hit_b, min(ring, 2.5), 110)
    N(DR, 49, hit_b, ring, 120)
    N(DR, 36, hit_b, .2, 122)
    N(DR, 38, hit_b, .2, 118)
    N(DR, 41, hit_b, .4, 115)

    m.save(a.out, tl.total)
    print("Wrote", a.out)


if __name__ == "__main__":
    main()
