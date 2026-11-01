#!/bin/sh
# cinewright wiki verification: run from a clone at the release tag.
run() { echo "== $*"; "$@" 2>&1; echo "-- exit $?"; }
run python scripts/cine.py cards list examples/three-shot
run python scripts/cine.py cards validate examples/three-shot
run python scripts/cine.py continuity diff examples/three-shot
run python scripts/cine.py continuity diff examples/three-shot --with examples/three-shot/planted/1C.json
run python scripts/cine.py compile examples/three-shot --model veo --out /tmp/cw-veo
run cat /tmp/cw-veo/1A.txt
run python scripts/cine.py kb search eyeline
run python scripts/cine.py budget
run python scripts/cine.py compile examples/three-shot --model nosuch --out /tmp/cw-x
run python plugins/cinewright/skills/cinewright/scripts/cine.py --help
run python -m unittest discover -s tests -q
