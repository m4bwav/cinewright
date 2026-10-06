"""Print one recorded run for a person: its tool calls with inputs and errors, paths outside the folder, checks, the
judge's reasons and the reply.

  python evals/inspect_run.py <key glob, e.g. cinewright-sound/action-1/haiku-*> [--out DIR] [--reply]
"""
import argparse
import fnmatch
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_evals  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("--out", default=str(run_evals.out_default()))
    ap.add_argument("--reply", action="store_true")
    a = ap.parse_args()
    for k, r in sorted(run_evals.done_keys(Path(a.out)).items()):
        if not fnmatch.fnmatch(k, a.key):
            continue
        print("=" * 8, k, "PASS" if r["pass"] else "FAIL", r["evidence"], "model", r.get("model_id"), "turns", r.get("turns"),
              "contaminated" if r.get("contaminated") else "", r.get("environment") or "")
        events = [json.loads(x) for x in open(r["trace"], encoding="utf-8") if x.strip().startswith("{")]
        for _, tool, inp, err in run_evals.tool_uses(events):
            s = inp.get("command") if tool == "Bash" else (inp.get("file_path") or inp.get("skill") or json.dumps(inp))
            print("  %s%-6s %s" % ("x " if err else "  ", tool, str(s).replace("\n", " ")[:220]))
        for o in r.get("outside", []):
            print("  outside:", o)
        for c in r.get("checks", []):
            print("  check exit %s: %s | %s" % (c["exit"], c["cmd"], c["tail"].replace("\n", " | ")[:300]))
        for j in r.get("judged", []):
            print("  judge %d/%d %s :: %s" % (j["yes"], j["of"], j["expectation"][:90], " / ".join(w[:120] for w in j["why"])))
        if a.reply:
            print("  REPLY:", (r.get("reply") or "")[:2500])


if __name__ == "__main__":
    main()
