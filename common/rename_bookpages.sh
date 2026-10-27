#!/bin/bash
# Usage: bash common/rename_bookpages.sh [start page, default 126] [apply]
# Without "apply" it only prints the plan (dry run).
set -euo pipefail
START="${1:-126}"
MODE="${2:-dry}"
cd assets/bookpage

SEEN=$(mktemp)
for p in page_[0-9]*.png; do
  [ -f "$p" ] && echo "$(shasum "$p" | cut -d' ' -f1) $p" >> "$SEEN"
done

N=$START
KEPT=0; DUPS=0
for s in Screenshot*.png; do
  [ -f "$s" ] || continue
  H=$(shasum "$s" | cut -d' ' -f1)
  DUP=$(grep "^$H " "$SEEN" | head -1 | cut -d' ' -f2- || true)
  if [ -n "$DUP" ]; then
    echo "DUPLICATE of $DUP  -> Trash: $s"
    [ "$MODE" = "apply" ] && mv "$s" ~/.Trash/"$(date +%s)_$s"
    DUPS=$((DUPS+1))
    continue
  fi
  while [ -f "page_${N}.png" ]; do
    echo "note: page_${N}.png already exists (different image), skipping that number"
    N=$((N+1))
  done
  echo "RENAME  $s  ->  page_${N}.png"
  if [ "$MODE" = "apply" ]; then
    mv "$s" "page_${N}.png"
    echo "$H page_${N}.png" >> "$SEEN"
  fi
  N=$((N+1)); KEPT=$((KEPT+1))
done
rm -f "$SEEN"

echo
echo "Renamed: $KEPT   Duplicates trashed: $DUPS   Last page number used: $((N-1))"
[ $((N-1)) -eq 150 ] || echo "WARNING: expected the last page to be 150. Check for missing or extra screenshots."
[ "$MODE" = "apply" ] || echo "(dry run: nothing was changed. Add 'apply' to do it.)"
