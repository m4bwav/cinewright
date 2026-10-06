"""Outcome check for cinewright-camera outcome-1: exits 0 only when out/cabin keeps a renderable 16:9 aspect, frames
for 2.39:1 in the style bible, states one lighting rule there, validates, and every compiled Veo prompt carries the
lighting and the frame sentence word for word.

  python evals/check_cabin.py <run folder>
"""
import json
import subprocess
import sys
from pathlib import Path

CINE = Path(__file__).resolve().parent.parent / "scripts" / "cine.py"


def main():
    work = Path(sys.argv[1])
    p = work / "out" / "cabin"
    bad = []
    try:
        st = json.loads((p / "bibles" / "style.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("FAIL style bible: %s" % e)
        return 1
    if st.get("aspect_ratio") != "16:9":
        bad.append("render aspect is %r, not the model's 16:9" % st.get("aspect_ratio"))
    if str(st.get("frame_aspect", "")).replace(":1", "") != "2.39":
        bad.append("frame_aspect is %r, not 2.39:1" % st.get("frame_aspect"))
    light = str(st.get("lighting") or "").strip().rstrip(".")
    if len(light.split()) < 4:
        bad.append("no lighting rule in the style bible")
    for cmd in (["cards", "validate"], ["continuity", "diff"]):
        r = subprocess.run([sys.executable, str(CINE)] + cmd + [str(p)], capture_output=True, text=True)
        if r.returncode:
            bad.append("%s: %s" % (" ".join(cmd), (r.stdout + r.stderr).strip().splitlines()[-1:]))
    prompts = sorted((p / "compiled" / "veo").glob("*.txt"))
    if len(prompts) < 3:
        bad.append("%d compiled prompts in out/cabin/compiled/veo, want one per card" % len(prompts))
    for f in prompts:
        t = f.read_text(encoding="utf-8")
        if light and light not in t:
            bad.append("%s lacks the lighting rule word for word" % f.name)
        if "2.39" not in t:
            bad.append("%s does not compose for 2.39" % f.name)
    for b in bad:
        print("FAIL " + b)
    print("check_cabin: %d problems" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
