"""Outcome check for cinewright-sets outcome-1: exits 0 only when out/lighthouse gives the lamp room a walls map,
card 1C faces one of its walls, cards validate and continuity diff pass, and the compiled Veo prompt for 1C carries
that wall's string word for word while 1A (no faces) does not.

  python evals/check_walls.py <run folder>
"""
import json
import subprocess
import sys
from pathlib import Path

CINE = Path(__file__).resolve().parent.parent / "scripts" / "cine.py"


def main():
    work = Path(sys.argv[1])
    p = work / "out" / "lighthouse"
    bad = []
    try:
        locs = json.loads((p / "bibles" / "locations.json").read_text(encoding="utf-8"))["locations"]
        card = json.loads((p / "cards" / "1C.json").read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError) as e:
        print("FAIL reading the project: %s" % e)
        return 1
    room = next((l for l in locs if l.get("id") == "lamp-room"), None)
    walls = (room or {}).get("walls") or {}
    if not walls:
        bad.append("lamp-room has no walls map")
    faces = card.get("camera", {}).get("faces")
    if faces not in walls:
        bad.append("card 1C camera.faces is %r, not a key of the lamp-room walls (%s)" % (faces, ", ".join(walls)))
    for cmd in (["cards", "validate"], ["continuity", "diff"]):
        r = subprocess.run([sys.executable, str(CINE)] + cmd + [str(p)], capture_output=True, text=True)
        if r.returncode != 0:
            bad.append("%s failed: %s" % (" ".join(cmd), (r.stdout + r.stderr).strip().splitlines()[-1:]))
    comp = p / "compiled" / "veo"
    try:
        c1 = (comp / "1C.txt").read_text(encoding="utf-8")
        a1 = (comp / "1A.txt").read_text(encoding="utf-8")
    except OSError as e:
        bad.append("compiled prompts missing: %s" % e)
    else:
        if faces in walls:
            wall = walls[faces].strip().rstrip(".")
            key = wall[1:60]  # compile capitalises the first letter
            if key not in c1:
                bad.append("1C prompt does not carry the %s wall string" % faces)
            if key in a1 and not card_faces(p, "1A"):
                bad.append("1A prompt carries the %s wall string though 1A faces no wall" % faces)
    for b in bad:
        print("FAIL " + b)
    if not bad:
        print("PASS walls map, 1C faces %s, checks clean, compiled prompt carries the wall" % faces)
    return 1 if bad else 0


def card_faces(p, cid):
    try:
        return json.loads((p / "cards" / ("%s.json" % cid)).read_text(encoding="utf-8")).get("camera", {}).get("faces")
    except (OSError, ValueError):
        return None


if __name__ == "__main__":
    sys.exit(main())
