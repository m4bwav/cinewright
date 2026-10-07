"""Outcome check for cinewright-voice outcome-1: exits 0 only when out/film/bibles/voices.json locks maren with a
reference clip that exists and carries the take's words, and out/film/voice-report.md passes line-2 and fails line-3.
Independent of cine.py.

  python evals/check_voices.py <run folder>
"""
import json
import re
import sys
from pathlib import Path

PASS = re.compile(r"\b(pass|passes|passed|match|matches|same voice|consistent|ok|keep)\b", re.I)
FAIL = re.compile(r"\b(drift|fail|fails|failed|mismatch|different|does not match|doesn't match|not her|wrong|reject|regenerate)\b", re.I)


def main():
    film = Path(sys.argv[1]) / "out" / "film"
    bad = []
    vf = film / "bibles" / "voices.json"
    try:
        voices = {v.get("character"): v for v in json.loads(vf.read_text(encoding="utf-8")).get("voices", [])}
    except (OSError, ValueError, AttributeError) as e:
        print("FAIL bibles/voices.json unreadable: %s" % e)
        return 1
    m = voices.get("maren")
    if not m:
        bad.append("voices.json has no maren")
    else:
        refs = m.get("refs") or []
        if not any((film / r.get("file", "")).is_file() for r in refs):
            bad.append("no maren reference file exists")
        if not any("steadier" in r.get("text", "") for r in refs):
            bad.append("no maren reference carries the take's words")
        if not m.get("rights"):
            bad.append("maren has no rights line")
    rf = film / "voice-report.md"
    if not rf.is_file():
        bad.append("no voice-report.md")
    else:
        text = rf.read_text(encoding="utf-8")
        for name, want, other in (("line-2", PASS, FAIL), ("line-3", FAIL, None)):
            lines = [ln for ln in text.splitlines() if name in ln]
            if not lines:
                bad.append("report never names %s" % name)
                continue
            said = " ".join(lines)
            if not want.search(said):
                bad.append("%s: verdict not found in %r" % (name, said[:160]))
            if other is not None and other.search(said) and not want.search(said):
                bad.append("%s marked as a fail" % name)
    for b in bad:
        print("FAIL " + b)
    if not bad:
        print("PASS voices.json locks maren; line-2 passes, line-3 fails")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
