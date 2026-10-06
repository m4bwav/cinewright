"""Outcome check for cinewright-genvideo outcome-1: exits 0 only when the compiled Veo prompts (in files the run wrote,
or in the reply) carry every cast member's identity string from bibles/characters.json word for word, once for each
card that casts them, and give a durationSeconds of 4, 6 or 8 for every card.

  python evals/check_veo.py <run folder> <reply file>
"""
import json
import re
import sys
from pathlib import Path


def corpus(work, reply):
    texts = [Path(reply).read_text(encoding="utf-8", errors="replace")] if Path(reply).is_file() else []
    proj = work / "examples" / "three-shot"
    for f in work.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in (".txt", ".md", ".json"):
            continue
        rel = f.relative_to(proj).parts if proj in f.parents else ()
        if rel and rel[0] in ("bibles", "cards", "planted", "styles"):
            continue  # the project's own inputs, not output
        if f.name in ("brief.md", "script.md", "takes.md") and f.parent == proj:
            continue
        texts.append(f.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(texts)


def main():
    work, reply = Path(sys.argv[1]), sys.argv[2]
    proj = work / "examples" / "three-shot"
    chars = json.loads((proj / "bibles" / "characters.json").read_text(encoding="utf-8"))
    chars = chars.get("characters", chars) if isinstance(chars, dict) else chars
    ident = {c["id"]: c["identity"] for c in (chars.values() if isinstance(chars, dict) else chars)}
    cards = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((proj / "cards").glob("*.json"))]
    text = corpus(work, reply)
    bad = []
    for cid, s in ident.items():
        need = sum(1 for c in cards if any(m["id"] == cid for m in c.get("cast", [])))
        have = text.count(s)
        if have < need:
            bad.append("%s's identity string appears %d times word for word, want at least %d (one per card)" % (cid, have, need))
    durs = [int(x) for x in re.findall(r"durationSeconds\W{0,3}(\d+)", text)]
    if len(durs) < len(cards):
        bad.append("%d durationSeconds settings found, want one per card (%d)" % (len(durs), len(cards)))
    if any(d not in (4, 6, 8) for d in durs):
        bad.append("durationSeconds %s: Veo takes 4, 6 or 8" % sorted(set(durs)))
    for b in bad:
        print("FAIL " + b)
    print("check_veo: %d problems" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
