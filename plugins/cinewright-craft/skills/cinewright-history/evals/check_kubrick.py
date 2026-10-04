"""Outcome check for cinewright-history outcome-1: exits 0 only when out/kubrick stays renderable (16:9), records the
Kubrick card in the style bible's history field with the moves and lens family that card implies, every card fits that
style (continuity diff: no errors, no MOVE or LENS warnings), and no compiled Veo prompt leans on the director's name.

  python evals/check_kubrick.py <run folder>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

CINE = Path(__file__).resolve().parent.parent / "scripts" / "cine.py"


def main():
    work = Path(sys.argv[1])
    p = work / "out" / "kubrick"
    bad = []
    try:
        st = json.loads((p / "bibles" / "style.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("FAIL style bible: %s" % e)
        return 1
    if st.get("aspect_ratio") != "16:9":
        bad.append("render aspect is %r; no model renders other frames here, crop with frame_aspect" % st.get("aspect_ratio"))
    hist = [str(h).lower() for h in st.get("history") or []]
    if not any("kubrick" in h for h in hist):
        bad.append("style history field does not name the kubrick card (%r)" % hist)
    if not st.get("allowed_moves"):
        bad.append("no allowed_moves in the style bible")
    if not st.get("lens_family"):
        bad.append("no lens_family in the style bible")
    for f in ("look", "lighting"):
        if re.search(r"(?i)kubrick", str(st.get(f, ""))):
            bad.append("style %s names the director instead of his devices" % f)
    r = subprocess.run([sys.executable, str(CINE), "continuity", "diff", str(p)], capture_output=True, text=True)
    out = r.stdout + r.stderr
    if r.returncode:
        bad.append("continuity diff: %s" % out.strip().splitlines()[-1:])
    for line in out.splitlines():
        if re.search(r"\b(MOVE|LENS)\b", line):
            bad.append("card breaks the style: " + line.strip())
    prompts = sorted((p / "compiled" / "veo").glob("*.txt"))
    if len(prompts) < 3:
        bad.append("%d compiled prompts in out/kubrick/compiled/veo, want one per card" % len(prompts))
    for f in prompts:
        if re.search(r"(?i)kubrick", f.read_text(encoding="utf-8")):
            bad.append("%s names Kubrick" % f.name)
    for b in bad:
        print("FAIL " + b)
    print("check_kubrick: %d problems" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
