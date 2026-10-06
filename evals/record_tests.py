"""Record a run of the matrix in each skill: a T- entry at the top of TESTS.md (model per line), the tests block in
evergreen.json through `evergreen.py tested`, and each value case's dated baseline in evals.json.

  python evals/record_tests.py --evergreen <path to evergreen.py> [--out DIR] [--skill S] [--note TEXT] [--dry-run]

A case passes when it passes on every model (trigger 2 of 3 or better, decoy 0 of 3, action and outcome every run).
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_evals as R  # noqa: E402

HARNESS = "evals/run_evals.py (claude -p --restricted, dontAsk, fresh folder on another drive)"
SHORT = {"haiku": "H", "sonnet": "S", "opus": "O"}


def case_rows(name, sk, rows):
    out = []
    for c in R.load_cases(sk):
        k = R.kind_of(c)
        cells, ok_all, fired_fail, n_fail = [], True, 0, 0
        for m in R.MODELS:
            rs = rows.get((name, c["id"], m, "with"), [])
            if not rs:
                cells.append("%s -" % SHORT[m])
                ok_all = False
                continue
            ok, txt = R.verdict(k, c.get("decoy"), rs)
            ok_all = ok_all and ok
            cells.append("%s %s" % (SHORT[m], txt.replace(" invoked", "")))
            for r in rs:
                if not r["pass"]:
                    n_fail += 1
                    fired_fail += bool(r.get("skill_fired"))
        base = []
        for m in R.MODELS:
            b = rows.get((name, c["id"], m, "without"), [])
            base.append(None if not b else all(r["pass"] for r in b))
        out.append({"case": c, "kind": k, "ok": ok_all, "cells": cells, "base": base, "fired_fail": fired_fail,
                    "n_fail": n_fail})
    return out


def klass(row):
    k = row["kind"]
    if k == "trigger":
        return "overtrigger" if row["case"].get("decoy") else "undertrigger"
    if row["n_fail"] and row["fired_fail"] * 2 < row["n_fail"]:
        return "undertrigger (skill not invoked in %d of %d failing runs)" % (row["n_fail"] - row["fired_fail"], row["n_fail"])
    return "no-op" if k == "action" else "wrong-outcome"


def baseline_text(row, stamp):
    b = row["base"]
    names = ["Haiku", "Sonnet", "Opus"]
    got = [(n, x) for n, x in zip(names, b) if x is not None]
    p = sum(1 for _, x in got if x)
    return ("%s, S6 matrix (%s; skills disabled), one run per model: without the skill %d of %d passed (%s)."
            % (stamp, HARNESS, p, len(got), ", ".join("%s %s" % (n, "pass" if x else "fail") for n, x in got)))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--evergreen", required=True)
    ap.add_argument("--out", default=str(R.out_default()))
    ap.add_argument("--skill")
    ap.add_argument("--note", default="")
    ap.add_argument("--notes", help="JSON file: {skill: {case: one-line note}} added to the failing lines")
    ap.add_argument("--led-to", default="{}", help='JSON {skill: "L-..., C-..."}')
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rows = R.summarise(Path(a.out))
    notes = json.loads(Path(a.notes).read_text(encoding="utf-8")) if a.notes else {}
    led = json.loads(a.led_to)
    stamp = time.strftime("%Y-%m-%d")
    for name, (plugin, sk) in R.skills().items():
        if a.skill and name not in a.skill.split(","):
            continue
        cr = case_rows(name, sk, rows)
        passed = [r for r in cr if r["ok"]]
        failing = [r for r in cr if not r["ok"]]
        redundant = [r["case"]["id"] for r in cr if r["kind"] in ("action", "outcome") and r["ok"]
                     and r["base"] and all(x for x in r["base"] if x is not None) and any(x is not None for x in r["base"])]
        cmd = [sys.executable, a.evergreen, "tested", str(sk), "--passed", str(len(passed)), "--failed", str(len(failing)),
               "--harness", HARNESS, "--env", "windows/claude-code", "--no-notify",
               "--note", (a.note or "S6 three-model matrix")[:200]]
        if failing:
            cmd += ["--failing", ",".join(r["case"]["id"] for r in failing)]
        tid = "T-?"
        if not a.dry_run:
            p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
            m = re.search(r"T-\d{8}-\d+", p.stdout + p.stderr)
            if not m:
                raise SystemExit("evergreen.py tested gave no T- id for %s:\n%s%s" % (name, p.stdout, p.stderr))
            tid = m.group(0)
        lines = ["### %s · %s · %s · windows/claude-code, Claude Code 2.1.281 · %d/%d cases on all three models"
                 % (tid, stamp, HARNESS, len(passed), len(cr)),
                 "- Models: H Haiku 4.5, S Sonnet 5, O Opus 5.5; with the skill 3 runs each; trigger counts are invocations.",
                 "- Cases: " + "; ".join("%s %s" % (r["case"]["id"], " ".join(r["cells"])) for r in cr) + "."]
        if a.note:
            lines.append("- " + a.note)
        for r in failing:
            extra = notes.get(name, {}).get(r["case"]["id"])
            lines.append("- FAIL %s · %s · %s · %s%s" % (r["case"]["id"], r["kind"], klass(r), " ".join(r["cells"]),
                                                      " · " + extra if extra else ""))
        if redundant:
            lines.append("- redundant (passed without the skill on every model): " + ", ".join(redundant))
        lines.append("- led to: " + led.get(name, "none"))
        entry = "\n".join(lines) + "\n"
        print(entry)
        if a.dry_run:
            continue
        tp = sk / "TESTS.md"
        t = tp.read_bytes().decode("utf-8")
        t = t.replace("## Runs\n\n", "## Runs\n\n" + entry + "\n", 1)
        tp.write_bytes(t.encode("utf-8"))
        ev = sk / "evals" / "evals.json"
        d = json.loads(ev.read_text(encoding="utf-8"))
        for c in d["evals"]:
            row = next((r for r in cr if r["case"]["id"] == c["id"]), None)
            if row and row["kind"] in ("action", "outcome") and any(x is not None for x in row["base"]):
                c["baseline"] = baseline_text(row, stamp)
        ev.write_bytes((json.dumps(d, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
