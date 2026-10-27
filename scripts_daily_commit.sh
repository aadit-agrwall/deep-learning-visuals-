#!/bin/zsh
cd ~/Documents/dpvisual
git add -A
if git diff --cached --quiet; then
  echo "Nothing to commit today."
else
  git commit -m "Daily update $(date +%Y-%m-%d)"
  git push
fi
