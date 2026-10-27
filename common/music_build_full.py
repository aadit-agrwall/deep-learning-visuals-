"""
common/music_build_full.py  (v2)

Builds a FULL Chapter 5 audio track for a page, fully derived from the
page's actual animation timeline — so tempo stays locked to a steady,
constant beat (matching the animation's constant pace) and only
INTENSITY (velocity / how many instruments are layered in) rises over
time, not the speed. This avoids the music "running ahead" of a
constant-pace animation.

Layers:
  - Steady background groove: drums (kick/hat) + guitar chug, on a FIXED
    beat interval for the whole track. Gets louder / fuller over time,
    never faster.
  - Piano bass pad: slow sustained root notes under everything, also
    at constant tempo.
  - Event-synced SFX, tied to real timeline positions:
      * type_in -> soft rapid piano ticks (duration-matched to the text)
      * create/play -> 3-note rising piano swell (duration-matched)
      * dust_wipe -> Reverse Cymbal whoosh landing on the transition
      * zoom_pulse -> single high piano accent

Usage:
    python common/music_build_full.py scenes/chapter05/page_102.py \
        --out assets/audio/raw/page_102_full.mid
"""

import re
import os
import argparse
import numpy as np
import pretty_midi as pm

PIANO = 0
GUITAR = 25
REVERSE_CYMBAL = 118  # GM "Reverse Cymbal" -- whoosh/riser SFX

KICK = 36
SNARE = 38
HIHAT_CLOSED = 42
HIHAT_OPEN = 46
CRASH = 49

SCALE = [62, 64, 65, 67, 69, 71, 72, 74]       # D minor-ish, mid register
TICK_SCALE = [p + 12 for p in SCALE]            # high register, for ticks
BASS_ROOT = SCALE[0] - 24                        # low root for bass pad

# FIXED beat interval -- tempo never changes, matching the animation's
# own constant pacing. Tune this one number to feel faster/slower overall.
BEAT_INTERVAL = 0.55


# --------------------------------------------------------------
# Timeline parsing (unchanged approach: scan the page .py for real
# self.type_in / self.play / self.dust_wipe / self.zoom_pulse / self.wait
# calls, in source order, to build an actual event timeline)
# --------------------------------------------------------------

def find_calls(content, method_name):
    results = []
    search_str = f"self.{method_name}("
    idx = 0
    while True:
        pos = content.find(search_str, idx)
        if pos == -1:
            break
        paren_start = pos + len(search_str) - 1
        depth = 0
        i = paren_start
        while i < len(content):
            if content[i] == "(":
                depth += 1
            elif content[i] == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        args_str = content[paren_start + 1:i]
        results.append((pos, args_str))
        idx = i + 1
    return results


def parse_timeline(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    raw_events = []

    for pos, args in find_calls(content, "type_in"):
        rt = re.search(r"run_time\s*=\s*([\d.]+)", args)
        dur = float(rt.group(1)) if rt else 1.2
        raw_events.append({"pos": pos, "kind": "type_in", "duration": dur})

    for pos, args in find_calls(content, "play"):
        rt = re.search(r"run_time\s*=\s*([\d.]+)", args)
        dur = float(rt.group(1)) if rt else 1.0
        raw_events.append({"pos": pos, "kind": "create", "duration": dur})

    for pos, args in find_calls(content, "dust_wipe"):
        rt = re.search(r"run_time\s*=\s*([\d.]+)", args)
        dur = float(rt.group(1)) if rt else 2.0
        raw_events.append({"pos": pos, "kind": "wipe", "duration": dur})

    for pos, args in find_calls(content, "zoom_pulse"):
        raw_events.append({"pos": pos, "kind": "zoom", "duration": 1.0})

    for pos, args in find_calls(content, "wait"):
        m = re.match(r"\s*([\d.]+)", args)
        dur = float(m.group(1)) if m else 1.0
        raw_events.append({"pos": pos, "kind": "wait", "duration": dur})

    raw_events.sort(key=lambda e: e["pos"])

    t = 0.0
    timeline = []
    for e in raw_events:
        if e["kind"] == "wait":
            t += e["duration"]
            continue
        timeline.append({"kind": e["kind"], "start": t, "duration": e["duration"]})
        t += e["duration"]

    total_duration = t
    drop_time = next((e["start"] for e in timeline if e["kind"] == "wipe"), 5.0)
    return timeline, total_duration, drop_time


# --------------------------------------------------------------
# Steady background: constant tempo, rising INTENSITY only
# --------------------------------------------------------------

def build_steady_background(total_duration, drop_time):
    piano = pm.Instrument(program=PIANO, name="Piano")
    guitar = pm.Instrument(program=GUITAR, name="Guitar")
    drums = pm.Instrument(program=0, is_drum=True, name="Drums")

    # --- Intro: sparse, quiet piano only, before the drop ---
    t = 0.0
    intro_notes = [SCALE[0], SCALE[2], SCALE[4]]
    if drop_time > 0.5:
        step = drop_time / max(len(intro_notes), 1)
        for i, pitch in enumerate(intro_notes):
            start = i * step
            piano.notes.append(pm.Note(velocity=42, pitch=pitch, start=start, end=start + step * 0.85))

    # --- Drop: low chord stab + kick/snare/crash hit ---
    chord = [SCALE[0] - 12, SCALE[2] - 12, SCALE[4] - 12]
    for pitch in chord:
        piano.notes.append(pm.Note(velocity=100, pitch=pitch, start=drop_time, end=drop_time + 0.6))
    drums.notes.append(pm.Note(velocity=108, pitch=KICK, start=drop_time, end=drop_time + 0.15))
    drums.notes.append(pm.Note(velocity=98, pitch=SNARE, start=drop_time, end=drop_time + 0.15))
    drums.notes.append(pm.Note(velocity=88, pitch=CRASH, start=drop_time, end=drop_time + 1.0))

    # --- Steady groove from drop to end: FIXED interval, rising velocity only ---
    build_span = max(total_duration - drop_time, 0.01)
    t = drop_time + 0.6
    beat_idx = 0
    bass_idx = 0

    while t < total_duration:
        progress = min((t - drop_time) / build_span, 1.0)  # 0 -> 1, controls LOUDNESS/density only
        vel_boost = int(30 * progress)

        # drums: constant pulse, more layers added as progress increases
        if beat_idx % 2 == 0:
            drums.notes.append(pm.Note(velocity=90 + vel_boost, pitch=KICK, start=t, end=t + 0.1))
        else:
            drums.notes.append(pm.Note(velocity=82 + vel_boost, pitch=SNARE, start=t, end=t + 0.1))

        # hihat only kicks in after ~25% progress, for a felt build without speed change
        if progress > 0.25:
            hat = HIHAT_OPEN if beat_idx % 4 == 3 else HIHAT_CLOSED
            drums.notes.append(pm.Note(velocity=50 + vel_boost, pitch=hat, start=t, end=t + BEAT_INTERVAL * 0.4))

        # guitar: chug enters after ~15% progress
        if progress > 0.15:
            root = SCALE[0] - 12
            guitar.notes.append(pm.Note(velocity=48 + vel_boost, pitch=root,
                                         start=t, end=t + BEAT_INTERVAL * 0.5))

        t += BEAT_INTERVAL
        beat_idx += 1

    # --- Slow bass pad underneath, constant tempo (one note per 2 beats) ---
    t = drop_time + 0.6
    pad_interval = BEAT_INTERVAL * 4
    while t < total_duration:
        progress = min((t - drop_time) / build_span, 1.0)
        piano.notes.append(pm.Note(velocity=38 + int(20 * progress), pitch=BASS_ROOT,
                                    start=t, end=t + pad_interval * 0.9))
        t += pad_interval

    midi = pm.PrettyMIDI(initial_tempo=round(60 / BEAT_INTERVAL))
    midi.instruments.extend([piano, guitar, drums])
    return midi


# --------------------------------------------------------------
# Event-synced SFX layer (ticks / swells / whoosh / accents)
# --------------------------------------------------------------

def add_sfx_layer(midi, timeline):
    piano = midi.instruments[0]
    fx = pm.Instrument(program=REVERSE_CYMBAL, name="Transition FX")

    tick_idx = 0
    swell_idx = 0

    for ev in timeline:
        start, dur, kind = ev["start"], ev["duration"], ev["kind"]

        if kind == "type_in":
            step = 0.12
            t = start
            while t < start + dur:
                pitch = TICK_SCALE[tick_idx % len(TICK_SCALE)]
                piano.notes.append(pm.Note(velocity=48, pitch=pitch, start=t, end=t + 0.07))
                tick_idx += 1
                t += step

        elif kind == "create":
            n_notes = 3
            step = dur / n_notes
            for i in range(n_notes):
                pitch = SCALE[swell_idx % len(SCALE)]
                note_start = start + i * step
                piano.notes.append(pm.Note(velocity=55, pitch=pitch,
                                            start=note_start, end=note_start + step * 1.3))
                swell_idx += 1

        elif kind == "wipe":
            fx_start = max(0.0, start - 0.4)
            fx.notes.append(pm.Note(velocity=85, pitch=60, start=fx_start, end=start + dur * 0.5))

        elif kind == "zoom":
            piano.notes.append(pm.Note(velocity=42, pitch=TICK_SCALE[-1], start=start, end=start + 0.5))

    midi.instruments.append(fx)
    return midi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page_file")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    timeline, total_duration, drop_time = parse_timeline(args.page_file)
    print(f"Parsed {len(timeline)} animation events, total {total_duration:.1f}s, first wipe at {drop_time:.1f}s")
    print(f"Steady background tempo: {round(60 / BEAT_INTERVAL)} BPM (constant, no acceleration)")

    midi = build_steady_background(total_duration, drop_time)
    midi = add_sfx_layer(midi, timeline)

    page_name = os.path.splitext(os.path.basename(args.page_file))[0]
    out_path = args.out or f"assets/audio/raw/{page_name}_full.mid"
    midi.write(out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
