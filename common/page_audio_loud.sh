#!/bin/bash
# Usage: bash common/page_audio_loud.sh <page number> [target LUFS]
# Build ASMR music + foley from the page timeline, render, boost, mux.
# Default level -16 LUFS (the stock ASMR master is -27, which is very quiet).
# Louder: -14. Softer: -18.
set -euo pipefail
N="$1"
LEVEL="${2:--16}"
VIDEO="media/videos/page_${N}/1080p60/Page_${N}.mp4"
TL="assets/audio/raw/page_${N}_asmr_timeline.json"
MID="assets/audio/raw/page_${N}_full.mid"
FOLEY="assets/audio/raw/page_${N}_foley.wav"
WAV="assets/audio/output/page_${N}_full.wav"
LOUD="assets/audio/output/page_${N}_full_loud.wav"
OUT="assets/user-data/outputs/page_${N}_full_final.mp4"

[ -f "$VIDEO" ] || { echo "Missing $VIDEO. Render the page first."; exit 1; }
[ -f "$TL" ] || { echo "Missing $TL. Render the page first."; exit 1; }

DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$VIDEO")
python - "$DUR" << 'PY'
import sys
d = float(sys.argv[1])
print(f"Video duration: {d:.1f} s", "" if 68 <= d <= 82 else "(outside the 70-80 s target)")
PY

python common/music_build_asmr.py "$TL" --out "$MID" --foley "$FOLEY" \
  --scene "scenes/chapter05/page_${N}.py"
bash common/music_render_asmr.sh "$MID" "$FOLEY" "$WAV" "$DUR"

ffmpeg -hide_banner -y -i "$WAV" \
  -af "loudnorm=I=${LEVEL}:TP=-1.5:LRA=11,alimiter=limit=0.89:level=false" \
  -ar 44100 "$LOUD"

bash common/mux_audio.sh "$VIDEO" "$LOUD" "$OUT"
echo "Streams in final file:"
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 "$OUT"
open "$OUT"
