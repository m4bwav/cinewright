"""Outcome check for cinewright-shots outcome-2: exits 0 only when out/flat plans scene 1 as flat space, the cards
still validate, and the continuity diff has no SPACE warning (the copy starts with a 24mm wide and a dolly-in,
both of which put depth back).

  python evals/check_flat.py <run folder>
"""
import json
import subprocess
import sys
from pathlib import Path

CINE = Path(__file__).resolve().parent.parent / "scripts" / "cine.py"


def main():
    p = Path(sys.argv[1]) / "out" / "flat"
    bad = []
    try:
        scenes = json.loads((p / "bibles" / "scenes.json").read_text(encoding="utf-8"))["scenes"]
    except (OSError, ValueError, KeyError) as e:
        print("FAIL scenes.json: %s" % e)
        return 1
    if scenes[0].get("space") != "flat":
        bad.append("scene 1 space is %r, not flat" % scenes[0].get("space"))
    r = subprocess.run([sys.executable, str(CINE), "cards", "validate", str(p)], capture_output=True, text=True)
    if r.returncode:
        bad.append("cards validate: %s" % (r.stdout + r.stderr).strip().splitlines()[-1:])
    r = subprocess.run([sys.executable, str(CINE), "continuity", "diff", str(p)], capture_output=True, text=True, encoding="utf-8")
    bad += ["diff: " + line for line in r.stdout.splitlines() if " SPACE:" in line]
    for b in bad:
        print("FAIL " + b)
    print("check_flat: %d problems" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
