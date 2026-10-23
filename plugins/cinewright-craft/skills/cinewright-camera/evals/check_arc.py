"""Outcome check for cinewright-camera outcome-3: exits 0 only when out/arc validates, card 1A circles the two
people with an arc move (arc-left or arc-right, not a pan or a truck), and its compiled Veo prompt
(out/arc/compiled/veo/1A.txt) carries the arc words.

  python evals/check_arc.py <run folder>
"""
import json
import subprocess
import sys
from pathlib import Path

CINE = Path(__file__).resolve().parent.parent / "scripts" / "cine.py"


def main():
    p = Path(sys.argv[1]) / "out" / "arc"
    bad = []
    try:
        card = json.loads((p / "cards" / "1A.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("FAIL card 1A: %s" % e)
        return 1
    move = card.get("camera", {}).get("move")
    if move not in ("arc-left", "arc-right"):
        bad.append("1A move is %r, not arc-left or arc-right" % move)
    r = subprocess.run([sys.executable, str(CINE), "cards", "validate", str(p)], capture_output=True, text=True)
    if r.returncode:
        bad.append("cards validate: %s" % (r.stdout + r.stderr).strip().splitlines()[-1:])
    prompt = p / "compiled" / "veo" / "1A.txt"
    if not prompt.is_file() or "arcs slowly" not in prompt.read_text(encoding="utf-8"):
        bad.append("out/arc/compiled/veo/1A.txt is missing or has no arc words")
    for b in bad:
        print("FAIL " + b)
    print("check_arc: %d problems" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
