"""Quiet music and three-layer tonal sonification from a measured timeline.

Example:
python common/music_build_asmr.py assets/audio/raw/page_106_asmr_timeline.json \
    --scene scenes/chapter05/page_106.py \
    --out assets/audio/raw/page_106_full.mid \
    --foley assets/audio/raw/page_106_foley.wav

The existing full-music composer and its beat interval are unchanged.
"""

import argparse
import ast
import json
from pathlib import Path

import numpy as np
import pretty_midi as pm
from scipy.io import wavfile

from music_build_full import BEAT_INTERVAL

RATE = 44100


def attach_point_profiles(timeline, scene_path):
    """Attach slide profiles where available; preserve measured event timing.

    The source can contain nested or non-executed slide cue blocks.
    Timeline events are authoritative for which cues actually rendered.
    Unmatched slide events use build()'s default transfer profile.
    """
    tree = ast.parse(Path(scene_path).read_text())
    cues = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.With):
            continue

        for item in node.items:
            call = item.context_expr

            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and call.func.attr == "cue"
                and call.args
                and isinstance(call.args[0], ast.Constant)
                and call.args[0].value == "slide"
            ):
                values = {
                    kw.arg: ast.literal_eval(kw.value)
                    for kw in call.keywords
                    if kw.arg == "profile"
                }
                cues.append((node.lineno, values))

    cues.sort(key=lambda item: item[0])

    slides = [
        event for event in timeline["events"]
        if event["kind"] == "slide"
    ]

    if len(slides) != len(cues):
        print(
            "WARNING: Source contains",
            len(cues),
            "slide cue blocks, but the rendered timeline contains",
            len(slides),
            "slide events. Unmatched events will use the default profile."
        )

    for event, (_, values) in zip(slides, cues):
        event.update(values)


def build(timeline, midi_path, foley_path):
    duration = float(timeline["duration"])
    audio = np.zeros((int(round(duration * RATE)), 2), dtype=np.float32)
    midi = pm.PrettyMIDI(initial_tempo=60 / BEAT_INTERVAL)
    piano = pm.Instrument(0, name="Quiet piano")
    guitar = pm.Instrument(24, name="Soft nylon guitar")

    # A stable, sparse phrase grid; the atmosphere never builds in loudness.
    voicings = [(50, 57, 62, 66), (47, 54, 59, 62),
                (43, 50, 57, 62), (45, 52, 57, 64)]
    for phrase, start in enumerate(np.arange(0.8, duration - 4, BEAT_INTERVAL * 16)):
        notes = voicings[phrase % len(voicings)]
        for j, pitch in enumerate(notes):
            at = float(start + j * BEAT_INTERVAL * 2)
            if at >= duration - 3:
                continue
            piano.notes.append(pm.Note(velocity=27 + j % 2 * 3, pitch=pitch,
                                       start=at, end=min(at + 2.8, duration - 1)))
        at = float(start + BEAT_INTERVAL * 8)
        if at < duration - 3:
            guitar.notes.append(pm.Note(velocity=24, pitch=notes[1] + 12,
                                        start=at, end=min(at + 2.2, duration - 1)))

    def oscillator(frequency, n, phase=0):
        frequency = np.broadcast_to(frequency, (n,))
        return np.sin(phase + 2 * np.pi * np.cumsum(frequency) / RATE)

    def motion(u):
        # Exactly the same normalized sigmoid as Manim's smooth rate function.
        error = 1 / (1 + np.exp(5))
        return np.clip((1 / (1 + np.exp(-10 * (u - .5))) - error) / (1 - 2 * error), 0, 1)

    def add(signal, start, pan):
        first = int(round(start * RATE))
        if first >= len(audio):
            return
        if first < 0:
            signal = signal[-first:]
            first = 0
        count = min(len(signal), len(audio) - first)
        signal = signal[:count]
        position = np.asarray(pan)
        if position.ndim:
            position = position[:count]
        angle = (np.clip(position, -1, 1) + 1) * np.pi / 4
        audio[first:first + count, 0] += (signal * np.cos(angle)).astype(np.float32)
        audio[first:first + count, 1] += (signal * np.sin(angle)).astype(np.float32)


    def tap(start, pan, amount=0.028, pitch=520):
        n = int(RATE * 0.105)
        t = np.arange(n) / RATE
        rng = np.random.default_rng(int(start * RATE) % (2**32))
        noise = rng.standard_normal(n)
        env = (1 - np.exp(-t / 0.0015)) * np.exp(-t / 0.022)
        click = (
            np.sin(2 * np.pi * pitch * t) * 0.55
            + np.sin(2 * np.pi * pitch * 2.4 * t) * 0.25
            + noise * 0.32
        )
        body = np.sin(2 * np.pi * 155 * t) * np.exp(-t / 0.012)
        signal = (click * env + body * env * 0.30) * amount
        add(signal, start, pan)

    def arrival(start, pan, pitch=293.6648, amount=0.006):
        # Three resolved bands: low contact, tuned body, and a faint harmonic.
        t = np.arange(int(RATE * 0.30)) / RATE
        attack = 1 - np.exp(-t / 0.006)
        taper = np.sin(np.linspace(0, np.pi, len(t))) ** 0.5
        low = np.sin(2 * np.pi * 146.8324 * t) * np.exp(-t / 0.035) * 0.40
        body = np.sin(2 * np.pi * pitch * t) * np.exp(-t / 0.075) * 0.75
        harmonic = np.sin(2 * np.pi * pitch * 2 * t) * np.exp(-t / 0.13) * 0.16
        add((low + body + harmonic) * attack * taper * amount, start, pan)

    point_profiles = {
        "positive": (220.0, 293.6648, 293.6648, 440.0, 0.16, 0.52),
        "negative": (220.0, 293.6648, 293.6648, 220.0, -0.16, -0.52),
        "zero": (220.0, 293.6648, 293.6648, 293.6648, 0.0, 0.0),
        "converge": (369.9944, 293.6648, 440.0, 293.6648, 0.04, 0.04),
        "transfer": (246.9417, 293.6648, 369.9944, 440.0, 0.0, 0.0),
        "minimum": (369.9944, 293.6648, 440.0, 293.6648, -0.42, 0.0),
    }

    for event in timeline["events"]:
        start, dur, kind = event["start"], event["duration"], event["kind"]
        pan = event.get("pan", 0.0)
        if kind == "type":
            # Each contact follows a small group of glyphs, spread over the reveal.
            count = min(max(1, event.get("glyphs", 18) // 3), max(1, int(dur / 0.09)))
            for j, at in enumerate(np.linspace(start + 0.01, start + max(0.02, dur - 0.10), count)):
                tap(
                    float(at),
                    pan + 0.18 * np.sin(j * 0.7),
                    amount=0.028,
                    pitch=480 + 65 * (j % 4),
                )
        elif kind in ("draw", "slide", "wipe", "grow"):
            n = max(8, int(round(dur * RATE)))
            t = np.arange(n) / RATE
            progress = np.linspace(0, 1, n)
            env = np.sin(np.pi * progress) ** 2
            eased = motion(progress)
            if kind == "wipe":
                # Subtle, centered transition accent.
                # No directional pan or aggressive whoosh.
                low = oscillator(180 - 35 * progress, n)
                upper = oscillator(360 - 70 * progress, n)
                sweep_env = np.sin(np.pi * progress) ** 1.5
                sig = (
                    low * 0.0035
                    + upper * 0.0012
                ) * sweep_env
                add(sig, start, 0.0)
            elif kind == "slide":
                profile = event.get("profile", "transfer")
                if profile not in point_profiles:
                    raise ValueError(f"Unknown point profile: {profile}")
                f0, f1, r0, r1, p0, p1 = point_profiles[profile]
                # Layer 1: continuous pilot follows the eased input/point motion.
                pilot = oscillator(f0 * (f1 / f0) ** eased, n)
                pilot_pan = (-0.14 + 0.68 * eased if profile in ("positive", "negative", "zero")
                             else p0 + (p1 - p0) * eased)
                add(pilot * env * 0.0052, start, pilot_pan)
                # Layer 2: a quieter resonant band sonifies the contribution.
                # Negative weights descend; zero weights hold a constant pitch.
                frequency = r0 * (r1 / r0) ** eased
                resonance = oscillator(frequency, n, phase=np.pi / 3)
                resonance += oscillator(frequency * 2, n) * 0.12
                add(resonance * env * 0.0026, start, p0 + (p1 - p0) * eased)
                # Layer 3: a precise arrival on the final visual frame.
                arrival(start + max(0, dur - 1 / 60), p1, pitch=r1, amount=0.007)
            elif kind == "grow":
                body = oscillator(85 * (1.8 ** eased), n)
                mid = oscillator(220 * (1.5 ** eased), n)
                sheen = oscillator(440 * (1.5 ** eased), n)
                build_env = np.sin(np.pi * progress) ** 0.8
                signal = (
                    body * 0.012 + mid * 0.006 + sheen * 0.0025
                ) * build_env
                add(signal, start, pan)
                arrival(
                    start + max(0, dur - 1 / 60),
                    pan, pitch=440, amount=0.012
                )
                tap(
                    start + max(0, dur - 0.035),
                    pan, amount=0.025, pitch=720
                )
            else:
                trace = oscillator(246.9417 * (1.1892 ** eased), n)
                sheen = oscillator(493.8833 * (1.1892 ** eased), n)
                sig = (trace * 0.0035 + sheen * 0.0009) * env
                add(sig, start, pan)
        elif kind == "settle":
            arrival(start + max(0, dur - 1 / 60), pan, amount=0.006)
        elif kind == "zoom":
            zoom_duration = min(1.2, dur)
            n_zoom = max(1, int(RATE * zoom_duration))
            t = np.arange(n_zoom) / RATE
            progress = np.linspace(0, 1, n_zoom)
            frequency = 280 + 620 * progress
            phase = 2 * np.pi * np.cumsum(frequency) / RATE
            tone = np.sin(phase)
            envelope = np.sin(np.pi * progress) ** 0.7
            add(tone * envelope * 0.012, start, 0)
            tap(
                start + max(0, zoom_duration - 0.04),
                0, amount=0.022, pitch=850
            )

    # Natural quiet ending. No gain increase or tempo changes across the page.
    fade = min(len(audio), int(3 * RATE))
    audio[-fade:] *= np.linspace(1, 0, fade)[:, None]
    midi.instruments.extend([piano, guitar])
    Path(midi_path).parent.mkdir(parents=True, exist_ok=True)
    Path(foley_path).parent.mkdir(parents=True, exist_ok=True)
    midi.write(midi_path)
    wavfile.write(foley_path, RATE, np.clip(audio, -1, 1).astype(np.float32))
    print(f"Measured timeline: {duration:.3f}s, {len(timeline['events'])} ASMR cues")
    print("Three-layer point sonification; quiet tonal wipes; no noise synthesis")
    print(f"Stable phrase grid uses BEAT_INTERVAL={BEAT_INTERVAL}; no drums or crescendo")
    print(f"Wrote {midi_path} and {foley_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("timeline")
    parser.add_argument("--out", required=True)
    parser.add_argument("--foley", required=True)
    parser.add_argument("--scene", help="Read point sound profiles from the scene source")
    args = parser.parse_args()
    timeline = json.loads(Path(args.timeline).read_text())
    if args.scene:
        attach_point_profiles(timeline, args.scene)
    build(timeline, args.out, args.foley)
