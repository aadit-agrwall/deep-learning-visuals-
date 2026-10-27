#!/bin/bash
# common/mux_audio.sh
# Final step: combine a rendered Manim page video with its synced audio
# track using ffmpeg. Trims audio to video length (or pads with silence
# if audio is shorter).
#
# Usage: bash common/mux_audio.sh video.mp4 audio.wav output_final.mp4

set -e

VIDEO="$1"
AUDIO="$2"
OUT="$3"

if [ -z "$VIDEO" ] || [ -z "$AUDIO" ] || [ -z "$OUT" ]; then
  echo "Usage: bash common/mux_audio.sh <video.mp4> <audio.wav> <output.mp4>"
  exit 1
fi

ffmpeg -y -i "$VIDEO" -i "$AUDIO" \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  "$OUT"

echo "Muxed output: $OUT"
