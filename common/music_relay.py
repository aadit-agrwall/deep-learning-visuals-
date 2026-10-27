#!/usr/bin/env python3
"""Spy-jazz action score: 140 BPM nominal, 4/4, E minor. One melody is
relayed guitar -> piano -> violin. Sneaky pizzicato sections explode into
loud brass/strings/drums sections. Each video scene is a section; its tempo
is bent slightly so bar lines land exactly on the dust-wipes. The last
section ends on a sharp hit at the zoom pulse. Needs the page's events json."""
import argparse, json, struct, subprocess
import numpy as np

BEAT0 = 60.0 / 140.0
BAR = 4
PPQ = 480
GTR, PIANO, VIOLIN, BASS, PIZZ, BRASS, STR, TREM, RCYM, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
BASEM = 64                       # E4

MEL = [  # (beat in 2-bar phrase, semitones above E, duration)
    (0, 0, .5), (.5, 3, .5), (1, 7, 1), (2.5, 5, .5), (3, 3, .5), (3.5, 2, .5),
    (4, 0, .5), (4.5, 3, .5), (5, 7, .5), (5.5, 10, .5), (6, 12, 1),
    (7, 11, .5), (7.5, 7, .5),
]
BASS_P = [(0, 0, .5), (.5, 0, .5), (1, 0, .5), (1.5, 7, .5),
          (2, 0, .5), (2.5, 3, .5), (3, 5, .5), (3.5, 6, .5)]
BASS_SOFT = [(0, 0, 1), (1.5, 7, .5), (2, 0, 1), (3.5, 3, .5)]
CH = [(0, [0, 3, 7, 10]), (0, [0, 3, 7, 11]),
      (-4, [0, 4, 7, 11]), (-5, [0, 4, 7, 10])]
BONGO = [(.5, 60), (1.5, 61), (2.5, 60), (3, 60), (3.5, 61)]
CONGA = [(0, 64), (1, 62), (2, 62), (2.5, 63)]


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
    if n == 2:
        return ["sneak", "climax"]
    roles = [""] * n
    roles[0], roles[-1], roles[-2] = "sneak", "climax", "build"
    cyc = ["relay", "sneak", "loud"]
    for k, i in enumerate(range(1, n - 2)):
        roles[i] = cyc[k % 3]
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
    draws = [(e["t0"], e["t1"]) for e in ev if e["kind"] == "play"]
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
        print(f"  section {i}: {roles[i]:6s} {s['t0']:5.1f}s  {s['bars']} bars  "
              f"{60 / s['mpb']:.0f} BPM")

    m = Midi(tl)
    progs = {GTR: 27, PIANO: 0, VIOLIN: 40, BASS: 33, PIZZ: 45, BRASS: 61,
             STR: 48, TREM: 44, RCYM: 119, 10: 46}
    vols = {GTR: 108, PIANO: 105, VIOLIN: 105, BASS: 110, PIZZ: 100,
            BRASS: 105, STR: 90, TREM: 85, RCYM: 90, DR: 115, 10: 80}
    verb = {GTR: 105, PIANO: 50, VIOLIN: 60, BASS: 20, PIZZ: 55, BRASS: 45,
            STR: 55, TREM: 55, RCYM: 80, DR: 40, 10: 85}
    for ch, pr in progs.items():
        m.raw(0, -1, [0xC0 | ch, pr])
    for ch, v in vols.items():
        m.raw(0, -1, [0xB0 | ch, 7, v])
        m.raw(0, -1, [0xB0 | ch, 91, verb[ch]])

    N = m.note
    # extra channels for motion sounds: 10 harp, 11 vibraphone
    for ch, pr, vol, rv in ((10, 46, 85, 85), (11, 11, 78, 75)):
        m.raw(0, -1, [0xC0 | ch, pr])
        m.raw(0, -1, [0xB0 | ch, 7, vol])
        m.raw(0, -1, [0xB0 | ch, 91, rv])
    RELAY = [GTR, PIANO, VIOLIN]
    phr = 0

    def melody(chs, b0, phase, shift, vel):
        for b, s, d in MEL:
            if phase * 4 <= b < phase * 4 + 4:
                for ch, ofs in chs:
                    N(ch, BASEM + shift + ofs + s, b0 + (b - phase * 4),
                      d * .92, vel)

    for si in range(n_sec):
        seg, role = tl.segs[si], roles[si]
        for bar in range(seg["bars"]):
            b0 = seg["b0"] + bar * BAR
            g = int(round(b0 / BAR))
            off, iv = CH[g % 4]
            rb = 52 + off
            last_bar = bar == seg["bars"] - 1
            first_bar = bar == 0
            prog = bar / max(1, seg["bars"])
            phase = bar % 2
            if phase == 0 and role != "build":
                phr += 1
            who = RELAY[(phr - 1) % 3]

            # ---- bass ----
            if role == "sneak":
                for b, s, d in BASS_SOFT:
                    N(BASS, 40 + off + s, b0 + b, d, 58)
            elif role == "build":
                for k in range(8):
                    N(BASS, 40 + int(((bar * 8 + k) / (seg["bars"] * 8)) * 12),
                      b0 + k * .5, .45, 85 + int(prog * 30))
            else:
                bv = {"relay": 88, "loud": 98, "climax": 108}[role]
                for b, s, d in BASS_P:
                    N(BASS, 40 + off + s, b0 + b, d, bv + (8 if b == 0 else 0))

            # ---- drums ----
            if role == "sneak":
                for b, p in BONGO:
                    N(DR, p, b0 + b, .1, 54 + (5 if p == 60 else 0))
                for b, p in CONGA:
                    N(DR, p, b0 + b, .15, 48)
                for b in (1, 3):
                    N(DR, 37, b0 + b, .1, 46)
                for k in range(8):
                    N(DR, 42, b0 + k * .5, .05, 30 + (8 if k % 2 == 0 else 0))
            elif role == "relay":
                for b in (0, 2):
                    N(DR, 36, b0 + b, .1, 88)
                for b in (1, 3):
                    N(DR, 38, b0 + b, .1, 84)
                for k in range(8):
                    N(DR, 42, b0 + k * .5, .05, 72 if k % 2 == 0 else 54)
                for b, p in BONGO:
                    N(DR, p, b0 + b, .1, 60)
            elif role in ("loud", "climax"):
                kv = 106 if role == "loud" else 118
                for b in (0, 1.5, 2, 3.5):
                    N(DR, 36, b0 + b, .1, kv)
                for b in (1, 3):
                    N(DR, 38, b0 + b, .1, kv + 4)
                for k in range(16):
                    N(DR, 42, b0 + k * .25, .04,
                      80 if k % 4 == 0 else 52 + (k % 2) * 12)
                if first_bar or role == "climax":
                    N(DR, 49, b0, 1.2, 100 if role == "climax" else 92)
                if last_bar:
                    for j, b in enumerate((2.5, 3, 3.25, 3.5, 3.75)):
                        N(DR, [47, 45, 43, 41, 41][j], b0 + b, .2, 85 + 6 * j)
            elif role == "build":
                N(DR, 36, b0, .1, 95)
                if last_bar:
                    for k in range(16):
                        N(DR, 38, b0 + k * .25, .1, 60 + k * 4)
                else:
                    dens = .5 if prog < .5 else .25
                    for k in range(int(BAR / dens)):
                        v = 55 + int(((bar * BAR + k * dens) /
                                      seg["beats"]) * 65)
                        tom = ([45, 43, 41, 47][k % 4] if dens == .5
                               else [50, 48, 47, 45, 43, 41][k % 6])
                        N(DR, tom, b0 + k * dens, dens * .8, v)
                    for b in range(4):
                        N(DR, 42, b0 + b, .05, 60)

            # ---- melody relay ----
            if role == "sneak":
                melody([(PIZZ, -12)], b0, phase, 0, 56)
                for b in (1.5, 3.5):
                    for i in iv[:3]:
                        N(PIZZ, rb + 12 + i, b0 + b, .2, 54)
            elif role == "relay":
                melody([(who, 0)], b0, phase, 0, 94)
                for b in (1.5, 3.5):
                    for i in iv[:3]:
                        N(PIZZ, rb + 12 + i, b0 + b, .2, 62)
            elif role == "loud":
                melody([(who, 0)], b0, phase, 12, 106)
            elif role == "climax":
                melody([(GTR, 0), (PIANO, 0), (VIOLIN, 0)], b0, phase, 12, 108)
                melody([(BRASS, -12)], b0, phase, 12, 100)

            # ---- brass stabs + fast strings ----
            if role in ("loud", "climax"):
                for b in (1.5, 3.5):
                    for i in iv:
                        N(BRASS, rb + 12 + i, b0 + b, .25, 98)
                for k in range(16):
                    N(STR, rb + 24 + iv[k % 4], b0 + k * .25, .22,
                      62 if k % 4 else 74)
            if role == "build":
                pch = 55 + int(((bar * BAR) / seg["beats"]) * 14)
                N(TREM, pch, b0, BAR, 60 + int(prog * 45))
                N(TREM, pch + 7, b0, BAR, 55 + int(prog * 45))
                for k in range(8):
                    N(STR, pch + 12 + (k % 2) * 3, b0 + k * .5, .4,
                      50 + int(prog * 55))
            if role == "sneak":
                for i in iv:
                    N(TREM, rb + 12 + i, b0, BAR, 28)

            # ---- section downbeat ----
            if first_bar and si >= 1:
                N(DR, 49, b0, 1.5, 108)
                N(DR, 36, b0, .2, 110)

    # reverse cymbal into each section boundary
    for s in tl.segs[1:]:
        if s["t0"] > 1.4:
            sb = tl.sec2beat(s["t0"] - 1.3)
            m.note(RCYM, 60, sb, s["b0"] - sb, 100)

    # soft typing melody (piano only), 8th-note grid
    total_typing = 0
    for t0, t1 in typing:
        ba, bb = tl.sec2beat(t0), tl.sec2beat(t1)
        g0 = int(np.ceil(ba * 2))
        g1 = max(int(np.floor(bb * 2)), g0)
        for g in range(g0, g1 + 1):
            beat = g / 2.0
            if beat >= hit_b:
                break
            off, iv = CH[int(beat // BAR) % 4]
            pitch = 52 + off + iv[[0, 1, 2, 3, 2, 1][g % 6]]
            N(PIANO, pitch, beat, 1.0, 58 + (g * 7) % 7)
            total_typing += 1
    print(f"Typing-melody notes: {total_typing}")

    # MOTION LAYER: the music follows what is moving on screen
    motion = sorted((e["t0"], e["t1"]) for e in ev
                    if e["kind"] in ("play", "type", "wipe", "pulse")
                    and e["t1"] > e["t0"])
    merged = []
    for t0, t1 in motion:
        if merged and t0 - merged[-1][1] < 0.8:
            merged[-1][1] = max(merged[-1][1], t1)
        else:
            merged.append([t0, t1])
    EXPR = (BASS, GTR, PIANO, VIOLIN, PIZZ, BRASS, STR, TREM, DR)
    STILL, MOVE = 86, 127
    for ch in EXPR:
        m.raw(0, -1, [0xB0 | ch, 11, STILL])
    for t0, t1 in merged:
        for ch in EXPR:
            m.raw(tl.sec2beat(max(0.0, t0 - 0.05)), -1, [0xB0 | ch, 11, MOVE])
            for k, v in enumerate((116, 106, 96, STILL)):
                m.raw(tl.sec2beat(t1 + 0.15 + 0.12 * k), -1,
                      [0xB0 | ch, 11, v])
    print(f"Motion intervals (full volume): {len(merged)}")

    PENT = [0, 3, 5, 7, 10]
    nplay = 0
    for e in ev:
        if e["kind"] != "play":
            continue
        t0, t1 = e["t0"], e["t1"]
        d = t1 - t0
        if d < 0.3 or t0 < 0.8:
            continue
        b0 = tl.sec2beat(t0)
        b1 = tl.sec2beat(t1)
        if b0 >= hit_b - 0.5:
            continue
        n = max(3, min(14, int(d / 0.11)))
        for k in range(n):                        # rising harp run
            p = 64 + PENT[k % 5] + 12 * (k // 5)
            N(10, min(p, 100), tl.sec2beat(t0 + d * k / n), 0.5,
              40 + int(30 * k / n))
        off, iv = CH[int(b0 // BAR) % 4]          # vibraphone swell + bell
        N(11, 52 + off + iv[2] + 12, b0, max(0.6, b1 - b0), 48)
        N(11, 88, b1, 0.8, 62)
        nplay += 1
    print(f"Motion sounds: {nplay} animations")

    # sharp final hit: E minor (maj7)
    ring = max(0.5, min(4.0, tl.total - hit_b - 0.05))
    for p in (40, 52, 55, 59, 63):
        N(BRASS, p, hit_b, min(ring, 2.0), 120)
    for p in (64, 67, 71, 75):
        N(STR, p, hit_b, ring, 100)
        N(VIOLIN, p, hit_b, ring, 100)
    for p in (40, 52, 59, 63, 76):
        N(PIANO, p, hit_b, ring, 105)
    for p in (52, 59, 64, 67):
        N(GTR, p, hit_b, min(ring, 2.5), 110)
    N(BASS, 40, hit_b, ring, 118)
    N(DR, 49, hit_b, ring, 120)
    N(DR, 36, hit_b, .2, 122)
    N(DR, 38, hit_b, .2, 118)
    N(DR, 41, hit_b, .4, 115)

    m.save(a.out, tl.total)
    print("Wrote", a.out)


if __name__ == "__main__":
    main()
