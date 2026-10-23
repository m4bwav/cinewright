"""Outcome check for cinewright-camera outcome-2: exits 0 only when out/lamp validates, card 1C carries the oil lamp
as its light source with a side, marks the smoke as the card's atmosphere, and its compiled Veo prompt (out/lamp/compiled/veo/1C.txt) says
the smoke is backlit.

  python evals/check_lamp.py <run folder>
"""
import json
import subprocess
import sys
from pathlib import Path

CINE = Path(__file__).resolve().parent.parent / "scripts" / "cine.py"


def main():
    p = Path(sys.argv[1]) / "out" / "lamp"
    bad = []
    try:
        card = json.loads((p / "cards" / "1C.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("FAIL card 1C: %s" % e)
        return 1
    light = card.get("light", {})
    if "lamp" not in str(light.get("motivation", "")).lower() or "left" not in str(light.get("motivation", "")).lower():
        bad.append("light.motivation does not carry the lamp and its side: %r" % light.get("motivation"))
    if light.get("atmosphere") != "smoke":
        bad.append("light.atmosphere is %r, not smoke" % light.get("atmosphere"))
    r = subprocess.run([sys.executable, str(CINE), "cards", "validate", str(p)], capture_output=True, text=True)
    if r.returncode:
        bad.append("cards validate: %s" % (r.stdout + r.stderr).strip().splitlines()[-1:])
    prompt = p / "compiled" / "veo" / "1C.txt"
    if not prompt.is_file() or "smoke is backlit" not in prompt.read_text(encoding="utf-8"):
        bad.append("out/lamp/compiled/veo/1C.txt is missing or does not say the smoke is backlit")
    for b in bad:
        print("FAIL " + b)
    print("check_lamp: %d problems" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
