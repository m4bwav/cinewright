#!/usr/bin/env python3
"""cinewright fight plans: replay a fight, hold its cards to it, write its sheet. Run it; do not read it.

  python scripts/cine_fight.py check FIGHT.json [--project P] [--json]
  python scripts/cine_fight.py sheet FIGHT.json [--project P] [--out DIR]

FIGHT follows scripts/schemas/fight-plan.schema.json (usually PROJECT/fights/<id>.json). check: weapons used
after they left the hand, phrase length and order, a one-sided fight; with --project, each card's held
props, sides, verbatim marks, exchanges per card and length. sheet: <id>.sheet.md (grid, phrases, state per
card) and <id>.csv (time, ahead score per exchange) for a chart. Python 3.9+, standard library only.
"""
import argparse
import copy
import csv
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("cine_runtime", HERE / "cine.py")
cine = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cine)

DEFAULT_SECS = 1.5
PAUSE_SECS = 1.0
MAX_PHRASE = 6
MAX_PER_CARD = 2


def load(path):
    plan = json.loads(cine.read_text(path))
    errs = cine.validate(plan, cine.load_schema(cine.default_context(), "fight-plan"))
    return plan, ["schema: %s" % e for e in errs]


def start_state(plan):
    return {f["id"]: {"right": f.get("right"), "left": f.get("left"), "carried": list(f.get("carried", [])),
                      "marks": list(f.get("marks", [])), "posture": f.get("posture", "standing"), "side": f["side"]}
            for f in plan["fighters"]}


def apply(state, ch, issues, n):
    who = state.get(ch["who"])
    if who is None:
        issues.append(("error", n, "FIGHTER", "change for unknown fighter '%s'" % ch["who"]))
        return
    for hand in ("right", "left"):
        if hand in ch:
            prop = ch[hand]
            if prop:
                # a prop is in one place: drawing or taking it removes it from every hand and belt
                for other in state.values():
                    for h in ("right", "left"):
                        if other[h] == prop:
                            other[h] = None
                    if prop in other["carried"]:
                        other["carried"].remove(prop)
            who[hand] = prop
    if "carried" in ch:
        who["carried"] = list(ch["carried"])
    if ch.get("mark"):
        who["marks"].append(ch["mark"])
    if ch.get("posture"):
        who["posture"] = ch["posture"]
    if ch.get("side") and ch["side"] != who["side"]:
        who["side"] = ch["side"]
        if len(state) == 2:
            other = [s for k, s in state.items() if k != ch["who"]][0]
            other["side"] = cine.FLIP[ch["side"]]


def replay(plan):
    """Yield (exchange, state before it, state after it) and collect plan issues."""
    issues, out = [], []
    ids = [f["id"] for f in plan["fighters"]]
    phrase_ids = [p["id"] for p in plan["phrases"]]
    for p in plan["phrases"]:
        if p["ahead"] not in ids + ["even"]:
            issues.append(("error", None, "AHEAD", "phrase %s: ahead '%s' is not a fighter or 'even'" % (p["id"], p["ahead"])))
    state = start_state(plan)
    last_n, last_phrase = 0, -1
    for e in plan["exchanges"]:
        n = e["n"]
        if n <= last_n:
            issues.append(("error", n, "ORDER", "exchange numbers must rise (%d after %d)" % (n, last_n)))
        last_n = n
        if e["phrase"] not in phrase_ids:
            issues.append(("error", n, "PHRASE", "phrase '%s' is not in phrases" % e["phrase"]))
        else:
            pi = phrase_ids.index(e["phrase"])
            if pi < last_phrase:
                issues.append(("error", n, "PHRASE", "phrase %s comes back after a later phrase" % e["phrase"]))
            last_phrase = max(last_phrase, pi)
        if e["lead"] not in state:
            issues.append(("error", n, "FIGHTER", "lead '%s' is not a fighter" % e["lead"]))
        elif e.get("with") and e["with"] not in (state[e["lead"]]["right"], state[e["lead"]]["left"]):
            lead = state[e["lead"]]
            issues.append(("error", n, "WEAPON", "%s moves with the %s, but holds %s" % (
                e["lead"], e["with"], " and ".join(x for x in (lead["right"], lead["left"]) if x) or "nothing")))
        before = copy.deepcopy(state)
        for c in e.get("changes", []):
            apply(state, c, issues, n)
        out.append((e, before, copy.deepcopy(state)))
    for p in plan["phrases"]:
        k = sum(1 for e in plan["exchanges"] if e["phrase"] == p["id"])
        if k == 0:
            issues.append(("warning", None, "PHRASE", "phrase %s has no exchanges" % p["id"]))
        elif k > MAX_PHRASE:
            issues.append(("warning", None, "PHRASE", "phrase %s has %d exchanges; split it at a pause (2 to %d read as one burst)" % (p["id"], k, MAX_PHRASE)))
    leads = {p["ahead"] for p in plan["phrases"]}
    if len(plan["phrases"]) >= 3 and len(leads) == 1 and "even" not in leads:
        issues.append(("warning", None, "ONE-SIDED", "%s is ahead in every phrase: a fight with no turn reads as an execution; give the loser a phrase" % leads.pop()))
    return out, issues


def card_checks(plan, rows, project):
    p = cine.Project(project)
    cards = {c["id"]: c for c in p.cards}
    issues, by_card = [], {}
    for e, before, after in rows:
        if e.get("card"):
            by_card.setdefault(e["card"], []).append((e, before, after))
    if by_card:
        for e, _, _ in rows:
            if not e.get("card"):
                issues.append(("warning", e["n"], "UNCOVERED", "no card covers this exchange"))
    last_order = 0
    for e, _, _ in rows:
        card = cards.get(e.get("card"))
        if card and card.get("order", 0) < last_order:
            issues.append(("error", e["n"], "CARD", "card %s comes before the previous exchange's card in the cut" % card["id"]))
        last_order = max(last_order, card.get("order", 0) if card else 0)
    for cid, items in by_card.items():
        card = cards.get(cid)
        n0 = items[0][0]["n"]
        if card is None:
            issues.append(("error", n0, "CARD", "card %s is not in cards/" % cid))
            continue
        if len(items) > MAX_PER_CARD:
            issues.append(("warning", n0, "ONE-EXCHANGE", "card %s covers %d exchanges; one per card renders, two at most" % (cid, len(items))))
        secs = sum(e.get("secs", DEFAULT_SECS) for e, _, _ in items)
        if secs > card.get("duration_s", 0):
            issues.append(("warning", n0, "TIME", "card %s is %ss but its exchanges take %.1fs" % (cid, card.get("duration_s"), secs)))
        start, end = items[0][1], items[-1][2]
        text = " ".join(card.get(k, "") for k in ("start_state", "action")).lower()
        end_text = " ".join(card.get(k, "") for k in ("action", "end_state")).lower()
        flipped = card.get("camera", {}).get("crosses_axis")
        for m in card.get("cast", []):
            st = start.get(m.get("id"))
            if st is None:
                continue
            for key, s in (("holding", st), ("holding_end", end[m["id"]])):
                hands = [x for x in (s["right"], s["left"]) if x]
                if m.get(key) and m[key] not in hands:
                    issues.append(("error", n0, "HOLDING", "card %s: %s %s '%s', the fight has %s in hand" % (cid, m["id"], key, m[key], " and ".join(hands) or "nothing")))
            want = cine.FLIP[st["side"]] if flipped else st["side"]
            if m.get("position") in ("frame-left", "frame-right") and m["position"] != want:
                issues.append(("error", n0, "SIDE", "card %s: %s is %s, the fight has them %s" % (cid, m["id"], m["position"], want)))
            for mark in st["marks"]:
                if mark.lower() not in text:
                    issues.append(("warning", n0, "MARK", "card %s: copy %s's mark '%s' verbatim into start_state or action" % (cid, m["id"], mark)))
            for mark in end[m["id"]]["marks"][len(st["marks"]):]:
                if mark.lower() not in end_text:
                    issues.append(("warning", n0, "MARK", "card %s: %s's new mark '%s' belongs in action or end_state" % (cid, m["id"], mark)))
    return issues, by_card, cards


def cmd_check(a):
    plan, errs = load(a.fight)
    if errs:
        print("\n".join(errs))
        return 1
    rows, issues = replay(plan)
    if a.project:
        issues += card_checks(plan, rows, a.project)[0]
    if a.json:
        print(json.dumps([{"level": l, "n": n, "code": c, "message": m} for l, n, c, m in issues], indent=2))
    for level, n, code, msg in ([] if a.json else issues):
        print("%s %s%s: %s" % (level.upper(), code, "" if n is None else " (move %d)" % n, msg))
    nerr = sum(1 for i in issues if i[0] == "error")
    print("fight %s: %d exchanges, %d phrases, %d errors, %d warnings" % (plan["id"], len(rows), len(plan["phrases"]), nerr, len(issues) - nerr))
    return 1 if nerr else 0


def timeline(plan, rows, by_card, cards):
    """Start time of each exchange: from the cut when the cards exist, else from secs and pauses."""
    times, t, prev_phrase = {}, 0.0, None
    pauses = {p["id"]: p.get("pause_secs", PAUSE_SECS) for p in plan["phrases"]}
    if by_card and cards:
        cut, clock = sorted(cards.values(), key=lambda c: c.get("order", 0)), 0.0
        starts = {}
        for c in cut:
            starts[c["id"]] = clock
            clock += c.get("duration_s", 0)
        for cid, items in by_card.items():
            off = 0.0
            for e, _, _ in items:
                times[e["n"]] = starts.get(cid, 0.0) + off
                off += e.get("secs", DEFAULT_SECS)
    for e, _, _ in rows:
        if prev_phrase is not None and e["phrase"] != prev_phrase:
            t += pauses.get(prev_phrase, PAUSE_SECS)
        times.setdefault(e["n"], t)
        t += e.get("secs", DEFAULT_SECS)
        prev_phrase = e["phrase"]
    return times


def describe(st):
    hands = ", ".join("%s hand: %s" % (h, st[h]) for h in ("right", "left") if st[h]) or "empty hands"
    bits = [st["posture"], st["side"], hands]
    if st["carried"]:
        bits.append("worn: " + ", ".join(st["carried"]))
    if st["marks"]:
        bits.append("marks: " + "; ".join(st["marks"]))
    return ", ".join(bits)


def cmd_sheet(a):
    plan, errs = load(a.fight)
    if errs:
        print("\n".join(errs))
        return 1
    rows, _ = replay(plan)
    by_card, cards = {}, {}
    if a.project:
        _, by_card, cards = card_checks(plan, rows, a.project)
    times = timeline(plan, rows, by_card, cards)
    fa, fb = plan["fighters"][0]["id"], plan["fighters"][1]["id"]
    score = {}
    for p in plan["phrases"]:
        m = p.get("margin", 1)
        score[p["id"]] = 0 if p["ahead"] == "even" else (m if p["ahead"] == fa else -m)
    out = Path(a.out or Path(a.fight).parent)
    md = ["# Fight sheet: %s" % plan["id"], "",
          "Generated by cine_fight.py sheet from `%s`; edit the plan, not this file." % Path(a.fight).name, "",
          "- Question: %s" % plan["question"], "- Ending: %s" % plan["ending"]]
    if plan.get("source"):
        md.append("- Source: %s" % plan["source"])
    md += ["", "## Fighters", "", "| Fighter | Goal | Style | Starts |", "|---|---|---|---|"]
    st0 = start_state(plan)
    for f in plan["fighters"]:
        md.append("| %s | %s | %s | %s |" % (f["id"], f["goal"], f.get("style", ""), describe(st0[f["id"]])))
    md += ["", "## Phrases", "", "| Phrase | Ahead | Why | Pause |", "|---|---|---|---|"]
    for p in plan["phrases"]:
        ahead = "even" if p["ahead"] == "even" else "%s +%d" % (p["ahead"], p.get("margin", 1))
        md.append("| %s %s | %s | %s | %s |" % (p["id"], p.get("name", ""), ahead, p["why"], p.get("pause", "")))
    md += ["", "## Exchanges", "", "| # | t | %s | | %s | Result | Card | Source |" % (fa, fb), "|---|---|---|---|---|---|---|---|"]
    bpm = plan.get("bpm")
    rows_csv = []
    for e, _, _ in rows:
        t = times[e["n"]]
        tt = "%.1f" % t
        if bpm:
            beat = t * bpm / 60.0
            tt += " (%d.%d)" % (int(beat // 4) + 1, int(beat % 4) + 1)
        if e["lead"] == fa:
            cells = (e["move"], "->", e["answer"])
        else:
            cells = (e["answer"], "<-", e["move"])
        md.append("| %d | %s | %s | %s | %s | %s | %s | %s |" % (e["n"], tt, cells[0], cells[1], cells[2], e["result"], e.get("card", ""), e.get("src", "added")))
        rows_csv.append({"n": e["n"], "time_s": round(t, 2), "phrase": e["phrase"], "ahead_score": score.get(e["phrase"], 0),
                         "result": e["result"], "lead": e["lead"], "card": e.get("card", "")})
    if by_card:
        md += ["", "## State at each card", "", "Copy marks verbatim into the card's start_state or action.", ""]
        for cid, items in by_card.items():
            md.append("- %s (from move %d): %s" % (cid, items[0][0]["n"], " | ".join("%s: %s" % (k, describe(v)) for k, v in items[0][1].items())))
    md += ["", "## End state", ""] + ["- %s: %s" % (k, describe(v)) for k, v in rows[-1][2].items()] if rows else []
    sheet = out / ("%s.sheet.md" % plan["id"])
    cine.write_text(sheet, "\n".join(md) + "\n")
    data = out / ("%s.csv" % plan["id"])
    with open(data, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_csv[0].keys()) if rows_csv else ["n"])
        w.writeheader()
        w.writerows(rows_csv)
    print("wrote %s and %s (%d exchanges; ahead_score > 0 means %s is ahead, < 0 %s)" % (sheet, data, len(rows), fa, fb))
    print("chart the turns (for people, never for prompts): a step chart of ahead_score over time_s; with chartwright: "
          "cw.py build --chart step --target vega-lite --data %s --x time_s --y ahead_score --out %s.vl.json, "
          "then cw.py render --target vega-lite --in %s.vl.json --out %s-ahead.png" % (data.name, plan["id"], plan["id"], plan["id"]))
    return 0


def build_parser():
    ap = argparse.ArgumentParser(prog="cine_fight.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_subparsers(dest="cmd", required=True)
    s = g.add_parser("check", help="replay the fight and hold the cards to it")
    s.add_argument("fight")
    s.add_argument("--project", help="project folder whose cards cover the fight")
    s.add_argument("--json", action="store_true")
    s = g.add_parser("sheet", help="write the fight sheet (markdown) and its data (csv)")
    s.add_argument("fight")
    s.add_argument("--project")
    s.add_argument("--out", help="folder for the sheet and csv (default: beside the plan)")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    return cmd_check(a) if a.cmd == "check" else cmd_sheet(a)


if __name__ == "__main__":
    sys.exit(main())
