#!/bin/bash
# Usage: bash common/append_page_image.sh <page number> [image path] [seconds]
# Appends the book-page screenshot to the end of
# assets/user-data/outputs/page_<N>_full_final.mp4 (default 4 s, fades in).
# Writes page_<N>_full_final_with_page.mp4 and leaves the original untouched.
set -euo pipefail
N="$1"
IMG="${2:-}"
SECS="${3:-4}"
IN="assets/user-data/outputs/page_${N}_full_final.mp4"
OUT="assets/user-data/outputs/page_${N}_full_final_with_page.mp4"

[ -f "$IN" ] || { echo "Missing $IN. Build the page video first."; exit 1; }

if [ -z "$IMG" ]; then
  # look for the newest screenshot in the usual places
  IMG=$(find ~/Desktop ~/Downloads ~/Pictures . -maxdepth 2 -iname "Screenshot*.png" \
        -not -path "./.venv/*" -print0 2>/dev/null | xargs -0 ls -t 2>/dev/null | head -1)
  echo "No image given; using newest screenshot found: $IMG"
fi
[ -f "$IMG" ] || { echo "Image not found. Pass its path as the second argument."; exit 1; }

ffmpeg -hide_banner -y \
  -i "$IN" \
  -loop 1 -framerate 60 -t "$SECS" -i "$IMG" \
  -f lavfi -t "$SECS" -i "anullsrc=r=44100:cl=stereo" \
  -filter_complex "\
[0:v]fps=60,scale=1080:1080,setsar=1,format=yuv420p[v0];\
[1:v]crop=iw-12:ih-12:6:6,scale=1080:1080:force_original_aspect_ratio=decrease,\
pad=1080:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=60,\
fade=t=in:st=0:d=0.5,format=yuv420p[v1];\
[0:a]aresample=44100,aformat=channel_layouts=stereo[a0];\
[2:a]aformat=channel_layouts=stereo[a1];\
[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"

echo "Duration before: $(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$IN") s"
echo "Duration after:  $(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT") s"
open "$OUT"
