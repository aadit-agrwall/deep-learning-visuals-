#!/bin/bash
# common/music_render.sh
# Renders a .mid file to a .wav using FluidSynth + the open-source
# MuseScore General soundfont, then outputs a normalized wav for muxing.
#
# Usage: bash common/music_render.sh path/to/track.mid path/to/output.wav

set -e

MIDI_FILE="$1"
OUT_FILE="$2"
SOUNDFONT="assets/audio/raw/MuseScore_General.sf3"

if [ -z "$MIDI_FILE" ] || [ -z "$OUT_FILE" ]; then
  echo "Usage: bash common/music_render.sh <input.mid> <output.wav>"
  exit 1
fi

fluidsynth -ni -F "$OUT_FILE" -r 44100 "$SOUNDFONT" "$MIDI_FILE"

echo "Rendered: $OUT_FILE"
