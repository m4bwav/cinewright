"""Outcome check for cinewright-shots outcome-3: exits 0 only when out/ots validates, card 1B is an OTS on Maren
with Tomas in it seen from behind through the card's `view` field (back or three-quarter-back), and the compiled Veo
prompt (out/ots/compiled/veo/1B.txt) carries the rear-view words.

  python evals/check_ots.py <run folder>
"""
import json
import subprocess
import sys
from pathlib import Path

CINE = Path(__file__).resolve().parent.parent / "scripts" / "cine.py"
REAR = ("back", "three-quarter-back")


def main():
    p = Path(sys.argv[1]) / "out" / "ots"
    bad = []
    try:
        card = json.loads((p / "cards" / "1B.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("FAIL card 1B: %s" % e)
        return 1
    if card.get("camera", {}).get("framing") != "ots":
        bad.append("1B framing is %r, not ots" % card.get("camera", {}).get("framing"))
    cast = {m.get("id"): m for m in card.get("cast", [])}
    if "maren" not in cast or "tomas" not in cast:
        bad.append("1B cast is %s; an OTS on Maren has both of them" % sorted(cast))
    elif cast["tomas"].get("view") not in REAR:
        bad.append("Tomas's view is %r, not back or three-quarter-back" % cast["tomas"].get("view"))
    r = subprocess.run([sys.executable, str(CINE), "cards", "validate", str(p)], capture_output=True, text=True)
    if r.returncode:
        bad.append("cards validate: %s" % (r.stdout + r.stderr).strip().splitlines()[-1:])
    prompt = p / "compiled" / "veo" / "1B.txt"
    if not prompt.is_file() or "seen from behind" not in prompt.read_text(encoding="utf-8"):
        bad.append("out/ots/compiled/veo/1B.txt is missing or does not say Tomas is seen from behind")
    for b in bad:
        print("FAIL " + b)
    print("check_ots: %d problems" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
