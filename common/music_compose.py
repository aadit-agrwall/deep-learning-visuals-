"""
common/music_compose.py

Algorithmically composes the Chapter 5 theme: piano + guitar + drums,
structured as intro -> beat-drop -> rising build, matching the
page animation pacing (quiet typewriter intro -> zoom-transition drop
-> accelerating dust-wipe/scene build).

Outputs a .mid file. Render it to audio with FluidSynth + a GM soundfont
(see music_render.sh).

Usage:
    python common/music_compose.py --duration 45 --out assets/audio/raw/chapter05_theme.mid
"""

import argparse
import pretty_midi as pm
import numpy as np

# General MIDI program numbers (0-indexed)
PIANO = 0           # Acoustic Grand Piano
GUITAR = 25          # Acoustic Guitar (steel)
DRUM_CHANNEL = 9     # GM drum channel (program ignored, uses channel 9)

# GM drum note numbers
KICK = 36
SNARE = 38
HIHAT_CLOSED = 42
HIHAT_OPEN = 46
CRASH = 49

SCALE = [62, 64, 65, 67, 69, 71, 72, 74]  # D minor-ish (D E F G A B C D)


def build_track(total_duration=45.0, drop_time=5.0, bpm_start=60, bpm_end=112):
    midi = pm.PrettyMIDI(initial_tempo=bpm_start)

    piano = pm.Instrument(program=PIANO, name="Piano")
    guitar = pm.Instrument(program=GUITAR, name="Guitar")
    drums = pm.Instrument(program=0, is_drum=True, name="Drums")

    # ------------------------------------------------------------
    # INTRO (0 -> drop_time): sparse, quiet piano only
    # ------------------------------------------------------------
    t = 0.0
    intro_notes = [SCALE[0], SCALE[2], SCALE[4]]
    step = drop_time / len(intro_notes)
    for i, pitch in enumerate(intro_notes):
        start = i * step
        end = start + step * 0.9
        piano.notes.append(pm.Note(velocity=45, pitch=pitch, start=start, end=end))

    # ------------------------------------------------------------
    # DROP (at drop_time): low piano chord stab + kick+snare hit
    # ------------------------------------------------------------
    chord = [SCALE[0] - 12, SCALE[2] - 12, SCALE[4] - 12]
    for pitch in chord:
        piano.notes.append(pm.Note(velocity=100, pitch=pitch, start=drop_time, end=drop_time + 0.6))
    drums.notes.append(pm.Note(velocity=110, pitch=KICK, start=drop_time, end=drop_time + 0.15))
    drums.notes.append(pm.Note(velocity=100, pitch=SNARE, start=drop_time, end=drop_time + 0.15))
    drums.notes.append(pm.Note(velocity=90, pitch=CRASH, start=drop_time, end=drop_time + 1.0))

    # ------------------------------------------------------------
    # BUILD (drop_time -> total_duration): rising energy
    # piano melody + guitar rhythm + driving drum groove, tempo/density
    # increasing smoothly via decreasing beat interval
    # ------------------------------------------------------------
    build_duration = total_duration - drop_time
    t = drop_time + 0.6

    beat_idx = 0
    melody_idx = 0
    while t < total_duration:
        progress = (t - drop_time) / build_duration  # 0 -> 1
        # interval shrinks as progress increases => tempo feels like it rises
        interval = np.interp(progress, [0, 1], [0.5, 0.22])

        # --- drums: kick on strong beats, hihat subdivisions, snare on backbeat
        if beat_idx % 2 == 0:
            drums.notes.append(pm.Note(velocity=95, pitch=KICK, start=t, end=t + 0.1))
        else:
            drums.notes.append(pm.Note(velocity=85, pitch=SNARE, start=t, end=t + 0.1))
        hat = HIHAT_OPEN if beat_idx % 4 == 3 else HIHAT_CLOSED
        drums.notes.append(pm.Note(velocity=60 + int(30 * progress), pitch=hat, start=t, end=t + interval * 0.4))

        # --- guitar: rhythmic chug on root, density increases with progress
        if beat_idx % 2 == 0 or progress > 0.5:
            root = SCALE[0] - 12
            guitar.notes.append(pm.Note(velocity=55 + int(35 * progress), pitch=root,
                                         start=t, end=t + interval * 0.5))

        # --- piano: rising arpeggio melody, more notes as progress increases
        pitch = SCALE[melody_idx % len(SCALE)]
        piano.notes.append(pm.Note(velocity=65 + int(35 * progress), pitch=pitch,
                                    start=t, end=t + interval * 0.9))
        melody_idx += 1 if progress < 0.6 else 2  # faster melodic movement later

        t += interval
        beat_idx += 1

    midi.instruments.extend([piano, guitar, drums])
    return midi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, default=45.0, help="total track length in seconds")
    ap.add_argument("--drop", type=float, default=5.0, help="time of the beat-drop in seconds")
    ap.add_argument("--out", type=str, default="assets/audio/raw/chapter05_theme.mid")
    args = ap.parse_args()

    midi = build_track(total_duration=args.duration, drop_time=args.drop)
    midi.write(args.out)
    print(f"Wrote {args.out} ({args.duration}s, drop at {args.drop}s)")


if __name__ == "__main__":
    main()
