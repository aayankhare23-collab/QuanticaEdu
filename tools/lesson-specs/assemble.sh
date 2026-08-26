#!/bin/sh
# Assemble a runnable authoring workflow: head + (STYLE + tail from the previous
# lesson's runner). The tail is identical across lessons, so it is lifted from the
# most recently shipped runner rather than re-pasted by hand.
#   sh tools/lesson-specs/assemble.sh 9_5 9_4
# writes tools/lesson-specs/_run_<new>.workflow.js
set -e
NEW=$1; PREV=$2
D=$(dirname "$0")
H=$(wc -c < "$D/author_${PREV}.head.js")
cat "$D/author_${NEW}.head.js" > "$D/_run_${NEW}.workflow.js"
tail -c +$((H+1)) "$D/_run_${PREV}.workflow.js" >> "$D/_run_${NEW}.workflow.js"
node --check "$D/_run_${NEW}.workflow.js"
echo "wrote $D/_run_${NEW}.workflow.js ($(wc -c < "$D/_run_${NEW}.workflow.js") bytes), syntax OK"
