"""Outcome check for cinewright-continuity outcome-2: exits 0 only when out/cutin validates, card 1B is still a close
shot (MS or tighter) of both Maren and Tomas, and the continuity diff gives 1B no STRAIGHT-IN warning and no
30-DEGREE error. The setup plants a straight-in cut: 1B on the same azimuth as the 1A two-shot, people off centre.

  python evals/check_cutin.py <run folder>
"""
import json
import subprocess
import sys
from pathlib import Path

CINE = Path(__file__).resolve().parent.parent / "scripts" / "cine.py"
CLOSE = ("MS", "MCU", "CU", "ECU")


def main():
    p = Path(sys.argv[1]) / "out" / "cutin"
    bad = []
    try:
        card = json.loads((p / "cards" / "1B.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("FAIL card 1B: %s" % e)
        return 1
    if card.get("camera", {}).get("size") not in CLOSE:
        bad.append("1B size is %r; the shot should stay close" % card.get("camera", {}).get("size"))
    if sorted(m.get("id") for m in card.get("cast", [])) != ["maren", "tomas"]:
        bad.append("1B cast is %s, not Maren and Tomas" % sorted(m.get("id") for m in card.get("cast", [])))
    r = subprocess.run([sys.executable, str(CINE), "cards", "validate", str(p)], capture_output=True, text=True)
    if r.returncode:
        bad.append("cards validate: %s" % (r.stdout + r.stderr).strip().splitlines()[-1:])
    r = subprocess.run([sys.executable, str(CINE), "continuity", "diff", str(p)], capture_output=True, text=True, encoding="utf-8")
    bad += ["diff: " + line for line in r.stdout.splitlines() if " 1B STRAIGHT-IN:" in line or " 1B 30-DEGREE:" in line]
    for b in bad:
        print("FAIL " + b)
    print("check_cutin: %d problems" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
