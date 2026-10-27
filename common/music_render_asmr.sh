#!/bin/bash
# FluidSynth music plus the measured stereo tactile layer; gentle fixed levels.
# Usage: bash common/music_render_asmr.sh input.mid foley.wav output.wav duration
set -euo pipefail
MIDI_FILE="$1"
FOLEY_FILE="$2"
OUT_FILE="$3"
DURATION="$4"
PIANO_FILE="${OUT_FILE%.wav}_piano.wav"
MIX_FILE="${OUT_FILE%.wav}_mix.wav"
METER_FILE="${OUT_FILE%.wav}_loudness.json"
FADE_START=$(python -c 'import sys; print(max(0, float(sys.argv[1])-3))' "$DURATION")
bash common/music_render.sh "$MIDI_FILE" "$PIANO_FILE"
ffmpeg -hide_banner -y -i "$PIANO_FILE" -i "$FOLEY_FILE" \
  -filter_complex "[0:a]lowpass=f=3800,volume=0.65,apad[p];[p][1:a]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.63:level=false:latency=true,afade=t=in:st=0:d=0.8,afade=t=out:st=${FADE_START}:d=3[a]" \
  -map "[a]" -t "$DURATION" -ar 44100 -c:a pcm_f32le "$MIX_FILE"
# Measure once, then apply one fixed gain. Preserve the cue dynamics and pauses.
ffmpeg -hide_banner -i "$MIX_FILE" \
  -af loudnorm=I=-27:TP=-6:LRA=11:print_format=json -f null - 2> "$METER_FILE"
GAIN=$(python - "$METER_FILE" <<'PY'
import json
import math
import sys
from pathlib import Path
text = Path(sys.argv[1]).read_text()
meter = json.loads(text[text.rfind('{'):text.rfind('}') + 1])
integrated = float(meter['input_i'])
peak = float(meter['input_tp'])
if not math.isfinite(integrated) or not math.isfinite(peak):
    raise SystemExit('ASMR mix is silent; refusing to master an empty track.')
print(min(-27 - integrated, -6 - peak))
PY
)
ffmpeg -hide_banner -y -i "$MIX_FILE" -af "volume=${GAIN}dB" \
  -ar 44100 -c:a pcm_s16le "$OUT_FILE"
echo "ASMR master: fixed gain ${GAIN} dB; target -27 LUFS, true peak <= -6 dB"
