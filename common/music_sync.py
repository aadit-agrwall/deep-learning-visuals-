"""
common/music_sync.py

Music-animation alignment helper. Scans a chapter05 page's .py file for
self.wait(...) and run_time=... values to estimate total scene duration,
so the generated music track can be composed/trimmed to match, and so
the beat-drop lands at the first dust_wipe() or zoom_pulse() call
(our proxy for "the first transition").

Usage:
    python common/music_sync.py scenes/chapter05/page_102.py
    # -> prints estimated total duration and suggested drop time

    python common/music_sync.py scenes/chapter05/page_102.py --compose
    # -> also calls music_compose.py with matching --duration/--drop
"""

import re
import sys
import argparse
import subprocess


def estimate_duration(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    run_times = [float(x) for x in re.findall(r"run_time\s*=\s*([\d.]+)", content)]
    waits = [float(x) for x in re.findall(r"self\.wait\(\s*([\d.]+)\s*\)", content)]

    total = sum(run_times) + sum(waits)

    # time of the FIRST dust_wipe or zoom_pulse call -> our proxy for
    # "the beat drop / first transition" moment
    first_transition_match = re.search(r"self\.(dust_wipe|zoom_pulse)\(", content)
    if first_transition_match:
        prefix = content[:first_transition_match.start()]
        prefix_run_times = [float(x) for x in re.findall(r"run_time\s*=\s*([\d.]+)", prefix)]
        prefix_waits = [float(x) for x in re.findall(r"self\.wait\(\s*([\d.]+)\s*\)", prefix)]
        drop_time = sum(prefix_run_times) + sum(prefix_waits)
    else:
        drop_time = 5.0  # fallback default

    return total, drop_time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page_file", help="path to a scenes/chapter05/page_XXX.py file")
    ap.add_argument("--compose", action="store_true", help="also run music_compose.py with matched timing")
    ap.add_argument("--out", default=None, help="output .mid path (default: assets/audio/raw/<page>.mid)")
    args = ap.parse_args()

    total, drop = estimate_duration(args.page_file)
    print(f"Estimated scene duration: {total:.1f}s")
    print(f"Suggested beat-drop time: {drop:.1f}s")

    if args.compose:
        import os
        page_name = os.path.splitext(os.path.basename(args.page_file))[0]
        out_path = args.out or f"assets/audio/raw/{page_name}.mid"
        subprocess.run([
            "python", "common/music_compose.py",
            "--duration", str(round(total, 1)),
            "--drop", str(round(drop, 1)),
            "--out", out_path,
        ], check=True)
        print(f"Composed MIDI written to {out_path}")


if __name__ == "__main__":
    main()
