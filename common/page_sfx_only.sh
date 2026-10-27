#!/bin/bash
# Usage: bash common/page_sfx_only.sh <page number> [peak dBFS, default -2]
# SFX only: builds the foley (tactile sound) layer from the page timeline,
# boosts it, and muxes it with the video. No MIDI/piano render, no music.
set -euo pipefail
N="$1"
PEAK="${2:--2}"
VIDEO="media/videos/page_${N}/1080p60/Page_${N}.mp4"
TL="assets/audio/raw/page_${N}_asmr_timeline.json"
MID="assets/audio/raw/page_${N}_full.mid"
FOLEY="assets/audio/raw/page_${N}_foley.wav"
SFX="assets/audio/output/page_${N}_sfx.wav"
OUT="assets/user-data/outputs/page_${N}_full_final.mp4"

[ -f "$VIDEO" ] || { echo "Missing $VIDEO. Render the page first."; exit 1; }
[ -f "$TL" ] || { echo "Missing $TL. Render the page first."; exit 1; }

DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$VIDEO")
echo "Video duration: ${DUR} s"

python common/music_build_asmr.py "$TL" --out "$MID" --foley "$FOLEY" \
  --scene "scenes/chapter05/page_${N}.py"
[ -f "$FOLEY" ] || { echo "Foley file was not written: $FOLEY"; exit 1; }

MAXV=$(ffmpeg -hide_banner -i "$FOLEY" -af volumedetect -f null - 2>&1 \
  | sed -n 's/.*max_volume: \(-\{0,1\}[0-9.]*\) dB.*/\1/p' | tail -1)
[ -n "$MAXV" ] || { echo "Could not measure the foley level."; exit 1; }

GAIN=$(python - "$MAXV" "$PEAK" << 'PY'
import sys
mx, peak = float(sys.argv[1]), float(sys.argv[2])
if mx < -80:
    raise SystemExit("Foley is silent; refusing to boost an empty track.")
print(f"{max(0.0, min(24.0, peak - mx)):.1f}")
PY
)
echo "Foley peak ${MAXV} dB -> applying ${GAIN} dB gain (target peak ${PEAK} dB)"

ffmpeg -hide_banner -y -i "$FOLEY" \
  -af "volume=${GAIN}dB,acompressor=threshold=0.03:ratio=3:attack=5:release=80:makeup=1.6,alimiter=limit=0.94:level=false,apad" \
  -t "$DUR" -ar 44100 "$SFX"

bash common/mux_audio.sh "$VIDEO" "$SFX" "$OUT"
echo "Streams in final file:"
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 "$OUT"
open "$OUT"
