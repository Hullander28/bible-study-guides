#!/bin/bash
# usage: tools/publish.sh "message" book1 book2 ...
set -e
cd "$(dirname "$0")/.."
python3 tools/build.py
git add -A
git -c user.name="Hullander28" -c user.email="Hullander28@users.noreply.github.com" commit -qm "$1"
git push -q
shift
U=https://hullander28.github.io/bible-study-guides
for b in "$@"; do
  for i in $(seq 1 30); do
    n=$(curl -s "$U/data/$b.json?x=$RANDOM" | python3 -c "import json,sys;d=json.load(sys.stdin);print(len(d['chapterList']))" 2>/dev/null || true)
    [ -n "$n" ] && break; sleep 10
  done
  echo "live $b: ${n:-MISSING} chapters"
done
curl -s "$U/js/books.js?x=$RANDOM" | grep -o ',true\]' | wc -l | xargs echo "ready flags live:"
