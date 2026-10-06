"""Headless eval harness for cinewright's skills (the evergreen protocol's TESTING.md, PLAN section 8).

Every run gets a fresh folder on a drive other than the repository's, holding a stripped copy of the example project
(no README, design notes or compiled prompts, so neither arm can read the answer). The with-skill arm loads a per-run
copy of the plugin under test with --plugin-dir (nothing else of the user's); the baseline arm runs with skills
disabled. Both run `claude -p --restricted --strict-mcp-config --permission-mode dontAsk`: file tools confined to the
run folder (and the plugin copy), Bash allowed only for cine.py, ffmpeg, ffprobe and copying inside the folder, no web,
agent, Glob, Grep, PowerShell or ToolSearch. Each run keeps its stream-json trace; every tool input is scanned for paths
outside the folder, and a run that reached the repository is marked contaminated and run again.

Grading (evidence, never the reply's claim):
  trigger  the Skill tool called with this skill (a trigger run stops as soon as it fires); decoy: never called
  action   the case's `evidence`: a tool call in the trace (`input_match` on the input, slashes normalised) or a file
  outcome  every `checks` command exits 0 (run from the skill's folder in the repository, {work} = the run folder),
           then a judge model (3 votes, majority) on the expectations not marked `check:`

  python evals/run_evals.py plan [--skill S] [--model haiku,sonnet,opus] [--runs 3]
  python evals/run_evals.py run  [--skill S] [--case ID] [--model M] [--runs 3] [--arm with|without|both] [--jobs 4]
  python evals/run_evals.py report [--out DIR] [--md FILE]
  python evals/run_evals.py export-worth [--out DIR]   then: evergreen.py worth <skill> --results DIR/worth/<skill>

Results go to --out (default: <temp>/cinewright-evals): results.jsonl, traces/, runs/. They stay outside the repository.
"""
import argparse
import concurrent.futures as cf
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXAMPLE = REPO / "examples" / "three-shot"
STRIP = {"README.md", "design.md", "compiled"}  # files that hold the answers or name the toolkit
MODELS = ["haiku", "sonnet", "opus"]
JUDGE_MODEL = "sonnet"
JUDGE_VOTES = 3
MAX_TURNS = {"trigger": 5, "action": 60, "outcome": 60}  # 30 cut Sonnet off mid-task
TIMEOUT = {"trigger": 300, "action": 1200, "outcome": 1200}
TOOLS = ["Read", "Write", "Edit", "Bash"]
DENY = ["WebFetch", "WebSearch", "Agent", "Task", "Glob", "Grep", "ToolSearch", "PowerShell", "NotebookEdit"]
BASH_ALLOW = [
    # the runtime in any form a model writes it (relative from the skill folder, or by its absolute path, quoted);
    # python -c and other scripts stay refused
    "Bash(python scripts/cine.py:*)", "Bash(python *cine.py*)", "Bash(python3 *cine.py*)", "Bash(py *cine.py*)",
    "Bash(ffmpeg:*)", "Bash(ffprobe:*)",
    # read-only and single-file commands; --restricted refuses their reads outside the working directories, and the
    # path scan flags any that reach out. dontAsk refuses a recursive cp whatever the rule: cases copy in `setup`.
    "Bash(cp:*)", "Bash(mkdir:*)", "Bash(ls:*)", "Bash(dir:*)", "Bash(cd:*)", "Bash(cat:*)", "Bash(head:*)",
    "Bash(tail:*)", "Bash(echo:*)", "Bash(wc:*)",
]
# Said to both arms. Interactively a command outside the allow list prompts the user; under dontAsk it is refused with
# "Permission to use Bash has been denied", which Opus read as the whole shell being off and stopped before cine.py
# (8 of 67 Opus runs with a refusal, every Opus action failure in round 2). Names no tool, so the baseline learns nothing.
UNATTENDED = ("This is an unattended run with no one to approve commands. A shell command that would need approval is "
              "refused instead of asked; the refusal covers that command only, and other commands may still run.")
HARNESS_REV = 2  # recorded on every result; 1 (no field) ran without UNATTENDED
LOCK = threading.Lock()
LIMITED = threading.Event()  # set when a run hits a usage limit: queued runs are skipped, rerun them later


def claude_exe():
    """The CLI by its full path. On Windows `claude` is often a .cmd wrapper, and cmd.exe re-parses every argument
    (quotes, &, newlines), so call the claude.exe it wraps."""
    w = shutil.which("claude")
    if not w:
        raise SystemExit("claude is not on PATH")
    if w.lower().endswith((".cmd", ".bat")):
        m = re.search(r'"%dp0%[\\/]*([^"]+\.exe)"', Path(w).read_text(encoding="utf-8", errors="replace"))
        if m:
            exe = Path(w).parent / m.group(1)
            if exe.is_file():
                return str(exe)
    return w


def out_default():
    return Path(tempfile.gettempdir()) / "cinewright-evals"


def norm(s):
    return str(s).replace("\\", "/").lower()


def check_out_dir(out):
    out = out.resolve()
    if os.name == "nt" and out.drive.lower() == REPO.resolve().drive.lower():
        raise SystemExit("--out %s is on the repository's drive; use another drive so a run cannot wander into it" % out)
    if norm(out).startswith(norm(REPO.resolve())):
        raise SystemExit("--out must be outside the repository")
    return out


def skills():
    """{skill name: (plugin folder, skill folder)} for every skill with evals."""
    found = {}
    for ev in sorted(REPO.glob("plugins/*/skills/*/evals/evals.json")):
        sk = ev.parent.parent
        found[sk.name] = (sk.parent.parent, sk)
    return found


def load_cases(skill_dir):
    return json.loads((skill_dir / "evals" / "evals.json").read_text(encoding="utf-8"))["evals"]


def kind_of(case):
    return case.get("kind", "trigger")


def planned(sel_skills, sel_case, models, runs, arm):
    """(skill, case, model, arm, n) for every run asked for. Baselines: action and outcome cases, once per model."""
    jobs = []
    for name, (plugin, sk) in sel_skills.items():
        for case in load_cases(sk):
            if sel_case and not fnmatch.fnmatch(case["id"], sel_case):
                continue
            k = kind_of(case)
            for m in models:
                if arm in ("with", "both"):
                    for n in range(1, (runs or case.get("runs", 3)) + 1):
                        jobs.append((name, case, m, "with", n))
                if arm in ("without", "both") and k in ("action", "outcome"):
                    jobs.append((name, case, m, "without", 1))
    return jobs


def key(name, case_id, model, arm, n):
    return "%s/%s/%s-%s-%d" % (name, case_id, model, arm, n)


def done_keys(out):
    f = out / "results.jsonl"
    keys = {}
    if f.is_file():
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            keys[r["key"]] = r
    return keys


def make_fixture(work):
    dst = work / "examples" / "three-shot"
    shutil.copytree(EXAMPLE, dst, ignore=lambda d, names: [x for x in names if x in STRIP])
    for f in dst.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".json"):
            t = f.read_text(encoding="utf-8")
            if "cinewright" in t.lower():
                f.write_text(re.sub(r"(?i)cinewright", "the toolkit", t), encoding="utf-8")


def run_setup(case, work):
    """A case's `setup`: ["copy", src, dst], ["delete", path], ["replace", path, old, new] or a command (ffmpeg ...), all inside the run folder."""
    for cmd in case.get("setup", []):
        if cmd[0] == "copy":
            shutil.copytree(work / cmd[1], work / cmd[2])
            continue
        if cmd[0] == "delete":
            (work / cmd[1]).unlink()
            continue
        if cmd[0] == "replace":  # ["replace", path, old, new]: plant a fault in a fixture file
            f = work / cmd[1]
            t = f.read_text(encoding="utf-8")
            if cmd[2] not in t:
                raise RuntimeError("setup replace: %r not in %s" % (cmd[2], cmd[1]))
            f.write_text(t.replace(cmd[2], cmd[3], 1), encoding="utf-8")
            continue
        args = [shutil.which(cmd[0]) or cmd[0]] + cmd[1:]
        for d in {Path(a).parent for a in cmd[1:] if a.startswith("out/")}:
            (work / d).mkdir(parents=True, exist_ok=True)
        p = subprocess.run(args, cwd=str(work), capture_output=True, text=True, encoding="utf-8", errors="replace")
        if p.returncode:
            raise RuntimeError("setup failed: %s\n%s" % (" ".join(cmd), p.stderr[-500:]))


def claude_args(prompt, model, arm, plugin_copy, kind, case):
    tools = TOOLS + (["Skill"] if arm == "with" else [])
    allow = ["Read", "Write", "Edit"] + BASH_ALLOW + (["Skill"] if arm == "with" else [])
    a = [claude_exe(), "-p", "--output-format", "stream-json", "--verbose",
         "--no-session-persistence", "--model", model, "--restricted", "--strict-mcp-config",
         "--permission-mode", "dontAsk", "--tools", ",".join(tools), "--disallowedTools", *DENY,
         "--allowedTools", *allow, "--max-turns", str(case.get("max_turns") or MAX_TURNS[kind]),
         "--append-system-prompt", UNATTENDED]
    if arm == "with":
        for d in plugin_copy:  # the plugin under test, then any the case also needs (`plugins`)
            a += ["--plugin-dir", str(d), "--add-dir", str(d)]
    else:
        a += ["--disable-slash-commands"]
    return a


def stream(args, prompt, cwd, trace_path, timeout, stop_when=None):
    """Run claude with the prompt on stdin, write every stream-json line to the trace, stop early when stop_when(event)
    is true."""
    events, killed, fired = [], False, []
    start = time.time()
    err_path = Path(str(trace_path) + ".err")
    with open(trace_path, "w", encoding="utf-8") as tf, open(err_path, "w", encoding="utf-8") as ef:
        p = subprocess.Popen(args, cwd=str(cwd), stdout=subprocess.PIPE, stderr=ef, stdin=subprocess.PIPE,
                             text=True, encoding="utf-8", errors="replace")
        p.stdin.write(prompt)
        p.stdin.close()

        def on_timeout():
            fired.append(True)
            p.kill()
        timer = threading.Timer(timeout, on_timeout)
        timer.start()
        try:
            for line in p.stdout:
                tf.write(line)
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                events.append(ev)
                if stop_when and stop_when(ev):
                    killed = True
                    p.kill()
                    break
            p.wait()
        finally:
            timer.cancel()
    err = err_path.read_text(encoding="utf-8", errors="replace")
    return events, {"seconds": round(time.time() - start, 1), "exit": p.returncode, "stopped_early": killed,
                    "timed_out": bool(fired), "stderr": err[-800:]}


DENIED = re.compile(r"(?i)permission to use \w+ has been denied|has been denied|is outside .*confines the file tools|"
                    r"requires approval|not allowed")


def tool_uses(events):
    """[(id, name, input dict, refused)] in order. refused: True when the harness refused the call (permission or the
    folder confinement), False when it ran (a nonzero exit still ran), None when no result came back."""
    uses, results = [], {}
    for ev in events:
        msg = ev.get("message") if isinstance(ev.get("message"), dict) else {}
        content = msg.get("content") if isinstance(msg.get("content"), list) else []
        if ev.get("type") == "assistant":
            for c in content:
                if c.get("type") == "tool_use":
                    uses.append([c.get("id"), c.get("name"), c.get("input") or {}, None])
        elif ev.get("type") == "user":
            for c in content:
                if c.get("type") == "tool_result":
                    body = c.get("content")
                    body = " ".join(x.get("text", "") for x in body if isinstance(x, dict)) if isinstance(body, list) else str(body)
                    results[c.get("tool_use_id")] = bool(c.get("is_error")) and bool(DENIED.search(body[:400]))
    for u in uses:
        u[3] = results.get(u[0])
    return uses


def skill_called(uses, name):
    for _, tool, inp, _ in uses:
        if tool == "Skill":
            val = str(inp.get("skill") or inp.get("command") or inp.get("name") or "")
            if val.split(":")[-1].strip().lstrip("/") == name:
                return True
    return False


def skills_called(uses):
    return [str(inp.get("skill") or inp.get("command") or "") for _, tool, inp, _ in uses if tool == "Skill"]


PATH_RE = re.compile(r"(?i)(?:[a-z]:[\\/]|/[a-z]/|~[\\/]|/(?:home|users|mnt)/)[^\s\"'|;&<>]*")


def scan_paths(uses, allowed_roots):
    """Paths in tool inputs outside the run folder and plugin copy. Returns (outside list, touched repository)."""
    roots = [norm(r).rstrip("/") for r in allowed_roots]
    repo = norm(REPO.resolve())
    repo_drive = norm(REPO.resolve().drive) + "/" if os.name == "nt" else None
    outside, touched = [], False
    for _, tool, inp, err in uses:
        # only the fields that name paths: a Write's content or an ffmpeg filter string is not a path
        text = " ".join(str(inp.get(f, "")) for f in ("command", "file_path", "path", "notebook_path"))
        for m in PATH_RE.findall(text):
            p = norm(m)
            if re.match(r"^/[a-z]/", p):
                p = p[1] + ":" + p[2:]
            if any(p.startswith(r) for r in roots) or "/temp/claude" in p or p.startswith("/dev/null"):
                continue
            outside.append("%s %s%s" % (tool, m[:160], " (refused)" if err else ""))
            if (p.startswith(repo) or (repo_drive and p.startswith(repo_drive))) and not err:
                touched = True
    return outside, touched


def evidence_ok(ev, uses, work):
    if not ev:
        return False, "no evidence named"
    t = ev.get("type")
    ok, why = False, ""
    if t == "trace":
        pat = re.compile(ev.get("input_match", ""), re.I)
        for _, tool, inp, err in uses:
            if tool == ev.get("tool") and not err:
                s = inp.get("command") if tool == "Bash" else json.dumps(inp)
                # slashes normalised and quotes dropped: python "C:/x/scripts/cine.py" continuity diff ...
                if pat.search(re.sub(r"[\"']", "", str(s).replace("\\", "/"))):
                    ok, why = True, "trace: %s %s" % (tool, str(s)[:200])
                    break
        if not ok:
            why = "no %s call matching %s" % (ev.get("tool"), ev.get("input_match"))
    elif t == "file":
        files = [work / ev["path"]] if ev.get("path") else [Path(x) for x in work.glob(ev.get("path_glob", ""))]
        for f in files:
            if f.is_file() and (not ev.get("contains") or ev["contains"] in f.read_text(encoding="utf-8", errors="replace")):
                ok, why = True, "file: %s" % f.relative_to(work).as_posix()
                break
        if not ok:
            why = "no file %s%s" % (ev.get("path") or ev.get("path_glob"), " containing %r" % ev["contains"] if ev.get("contains") else "")
    if not ok and ev.get("or"):
        ok2, why2 = evidence_ok(ev["or"], uses, work)
        return ok2, why if not ok2 else why2
    return ok, why


def run_checks(case, skill_dir, work, reply_file):
    res = []
    for c in case.get("checks", []):
        cmd = [x.replace("{work}", str(work)).replace("{reply}", str(reply_file)) for x in c]
        if cmd[0] in ("python", "python3"):
            cmd[0] = sys.executable
        p = subprocess.run(cmd, cwd=str(skill_dir), capture_output=True, text=True, encoding="utf-8", errors="replace")
        res.append({"cmd": " ".join(c), "exit": p.returncode, "tail": (p.stdout + p.stderr).strip()[-400:]})
    return res


def final_text(events):
    """Everything the assistant said, in order: the user reads every message, and a closing note (a skill's Step 0
    report, say) must not hide the answer given before it."""
    texts = []
    for ev in events:
        msg = ev.get("message") if isinstance(ev.get("message"), dict) else {}
        if ev.get("type") == "assistant" and isinstance(msg.get("content"), list):
            texts += [c.get("text", "") for c in msg["content"] if c.get("type") == "text" and c.get("text", "").strip()]
    if texts:
        return "\n\n".join(texts)
    res = next((e for e in reversed(events) if e.get("type") == "result"), {})
    return str(res.get("result") or "")


def written_files(work, limit=24000):
    """Text files the run left under out/ and examples/ that the fixture did not have, for the judge."""
    out, total = [], 0
    for f in sorted(work.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in (".md", ".json", ".txt"):
            continue
        rel = f.relative_to(work).as_posix()
        orig = EXAMPLE / Path(rel).relative_to("examples/three-shot") if rel.startswith("examples/three-shot/") else None
        if orig and Path(rel).relative_to("examples/three-shot").parts[0] in STRIP:
            orig = None  # stripped from the fixture, so the run wrote it, even when it matches the repository's copy
        if orig and orig.is_file() and orig.read_bytes() == f.read_bytes():
            continue
        t = f.read_text(encoding="utf-8", errors="replace")[:6000]
        if total + len(t) > limit:
            break
        total += len(t)
        out.append("--- %s\n%s" % (rel, t))
    return "\n".join(out)


def judge(case, reply, files, jdir):
    exps = [e for e in case.get("expectations", []) if not e.lower().startswith("check:")]
    if not exps:
        return True, []
    numbered = "\n".join("%d. %s" % (i + 1, re.sub(r"^judge:\s*", "", e)) for i, e in enumerate(exps))
    prompt = ("You grade one answer from an assistant against numbered expectations. Judge only what the reply and the "
              "files show; do not reward claims about files that are not shown. An expectation about 'the reply' may be "
              "met by the reply or by the files it wrote. Strip '(2 of 3 votes)' notes; they are for the harness.\n\n"
              "TASK GIVEN TO THE ASSISTANT:\n%s\n\nEXPECTATIONS:\n%s\n\nFINAL REPLY:\n%s\n\nFILES WRITTEN:\n%s\n\n"
              "Answer with only a JSON object: {\"pass\": [true or false for each expectation in order], \"why\": [one short "
              "reason each]}" % (case["prompt"], numbered, reply[:12000] or "(empty)", files or "(none)"))
    votes = []
    jdir.mkdir(parents=True, exist_ok=True)
    for v in range(JUDGE_VOTES):
        a = [claude_exe(), "-p", "--output-format", "json", "--no-session-persistence",
             "--model", JUDGE_MODEL, "--restricted", "--strict-mcp-config", "--tools", "", "--disable-slash-commands",
             "--max-turns", "1"]
        p = subprocess.run(a, cwd=str(jdir), input=prompt, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=300)  # stdin: a multi-line argument does not survive a .cmd wrapper
        try:
            txt = json.loads(p.stdout).get("result", "") if p.stdout.strip() else ""
            if not txt:
                raise ValueError("empty (exit %s) %s" % (p.returncode, p.stderr[-200:]))
            m = re.search(r"\{.*\}", txt, re.S)
            d = json.loads(m.group(0))
            votes.append([bool(x) for x in d["pass"]][:len(exps)] + [False] * max(0, len(exps) - len(d["pass"])))
            votes[-1] = {"pass": votes[-1], "why": d.get("why", [])}
        except Exception as e:  # a vote that cannot be read counts as a fail on every expectation
            if re.search(r"(?i)(session|usage|rate) limit|hit your|\b429\b", p.stdout + p.stderr):
                LIMITED.set()
                raise RuntimeError("judge hit a usage limit; run again after it resets")
            votes.append({"pass": [False] * len(exps), "why": ["unreadable judge output: %s" % e]})
    per = []
    for i, e in enumerate(exps):
        yes = sum(1 for v in votes if v["pass"][i])
        per.append({"expectation": e, "yes": yes, "of": len(votes), "pass": yes * 2 > len(votes),
                    "why": [v["why"][i] if i < len(v["why"]) else "" for v in votes]})
    return all(x["pass"] for x in per), per


def env_problem(events, meta, arm, name):
    init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), None)
    if init is None:
        return "no init event (exit %s): %s" % (meta["exit"], meta["stderr"][-200:])
    loaded = [str(s) for s in init.get("skills") or []]
    if arm == "with" and not any(s.split(":")[-1] == name for s in loaded):
        return "skill not loaded in the with arm"
    if arm == "without" and any(s.split(":")[0] == "cinewright" or s.startswith("cinewright") for s in loaded):
        return "cinewright loaded in the baseline"
    res = next((e for e in reversed(events) if e.get("type") == "result"), None)
    limited = any(e.get("error") == "rate_limit" or e.get("api_error_status") in (429, 529) for e in events)
    if limited or (res and res.get("is_error") and re.search(r"(?i)(usage|session|rate) limit|hit your|overloaded|credit",
                                                            str(res.get("result")))):
        return "usage or rate limit: %s" % str((res or {}).get("result"))[:120]
    return None


def one(job, out, keep):
    name, case, model, arm, n = job
    if LIMITED.is_set():
        raise RuntimeError("skipped: a usage limit was hit; run again after it resets")
    plugin, sk = skills()[name]
    k = kind_of(case)
    rk = key(name, case["id"], model, arm, n)
    rdir = out / "runs" / rk
    if rdir.exists():
        shutil.rmtree(rdir, ignore_errors=True)
    work = rdir / "work"
    work.mkdir(parents=True)
    make_fixture(work)
    run_setup(case, work)
    plugin_copy = []
    if arm == "with":
        # a case's `plugins` names other plugins a real install would have beside it (craft compiles need core's
        # model cards); the skill under test is still the only one graded
        for pdir in [plugin] + [REPO / "plugins" / x for x in case.get("plugins", [])]:
            plugin_copy.append(rdir / "plugin" / pdir.name)
            shutil.copytree(pdir, plugin_copy[-1], ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "results"))
    trace = out / "traces" / (rk.replace("/", "__") + ".jsonl")
    trace.parent.mkdir(parents=True, exist_ok=True)
    stop = None
    if k == "trigger" and not case.get("decoy"):
        def stop(ev):
            return ev.get("type") == "assistant" and skill_called(tool_uses([ev]), name)
    events, meta = stream(claude_args(case["prompt"], model, arm, plugin_copy, k, case), case["prompt"], work, trace,
                         case.get("timeout_seconds") or TIMEOUT[k], stop)
    uses = tool_uses(events)
    init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), {})
    res = next((e for e in reversed(events) if e.get("type") == "result"), {})
    outside, touched = scan_paths(uses, [work.resolve()] + [d.resolve() for d in plugin_copy])
    r = {"key": rk, "skill": name, "plugin": plugin.name, "case": case["id"], "kind": k, "decoy": bool(case.get("decoy")),
         "model": model, "model_id": init.get("model"), "arm": arm, "n": n, "when": time.strftime("%Y-%m-%d %H:%M"),
         "cost_usd": res.get("total_cost_usd"), "turns": res.get("num_turns"), "seconds": meta["seconds"],
         "exit": meta["exit"], "stopped_early": meta["stopped_early"], "skills_called": skills_called(uses),
         "tools": [u[1] for u in uses], "outside": outside[:20], "contaminated": touched, "trace": str(trace),
         "workdir": str(work), "harness": HARNESS_REV}
    r["environment"] = env_problem(events, meta, arm, name)
    if r["environment"] and "limit" in r["environment"]:
        LIMITED.set()
    called = skill_called(uses, name)
    if k == "trigger":
        r["pass"] = (not called) if case.get("decoy") else called
        r["evidence"] = "invoked" if called else "not invoked"
    elif k == "action":
        r["pass"], r["evidence"] = evidence_ok(case.get("evidence"), uses, work)
    else:
        reply = final_text(events)
        r["reply"] = reply[:4000]
        (rdir / "reply.txt").write_text(reply, encoding="utf-8")
        checks = run_checks(case, sk, work, rdir / "reply.txt")
        r["checks"] = checks
        ok_checks = all(c["exit"] == 0 for c in checks)
        ok_judge, per = judge(case, reply, written_files(work), rdir / "judge")
        r["judged"] = per
        r["pass"] = ok_checks and ok_judge
        r["evidence"] = "checks %d/%d, judged %d/%d" % (sum(c["exit"] == 0 for c in checks), len(checks),
                                                       sum(x["pass"] for x in per), len(per))
    if k in ("action", "outcome"):
        r["skill_fired"] = called
    with LOCK:
        with open(out / "results.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(r) + "\n")
    if not keep and r["pass"] and not r["contaminated"]:
        shutil.rmtree(work, ignore_errors=True)
        if plugin_copy:
            shutil.rmtree(plugin_copy[0].parent, ignore_errors=True)
    return r


def select(a):
    allsk = skills()
    names = [s.strip() for s in a.skill.split(",")] if a.skill else list(allsk)
    bad = [s for s in names if s not in allsk]
    if bad:
        raise SystemExit("unknown skill: %s" % ", ".join(bad))
    return {s: allsk[s] for s in names}


def cmd_plan(a):
    jobs = planned(select(a), a.case, a.model.split(","), a.runs, a.arm)
    by = {}
    for name, case, m, arm, n in jobs:
        kk = (kind_of(case) + (" decoy" if case.get("decoy") else ""), arm)
        by[kk] = by.get(kk, 0) + 1
    for kk in sorted(by):
        print("%-16s %-8s %4d" % (kk[0], kk[1], by[kk]))
    judged = sum(1 for _, c, _, _, _ in jobs if kind_of(c) == "outcome")
    print("runs %d, judge calls %d (%d outcome runs x %d votes)" % (len(jobs), judged * JUDGE_VOTES, judged, JUDGE_VOTES))


def cmd_run(a):
    out = check_out_dir(Path(a.out))
    out.mkdir(parents=True, exist_ok=True)
    before = subprocess.run(["git", "status", "--porcelain"], cwd=str(REPO), capture_output=True, text=True).stdout
    jobs = planned(select(a), a.case, a.model.split(","), a.runs, a.arm)
    have = done_keys(out)
    todo = []
    for j in jobs:
        r = have.get(key(j[0], j[1]["id"], j[2], j[3], j[4]))
        if a.rerun or r is None or r.get("contaminated") or r.get("environment"):
            todo.append(j)
    print("runs asked %d, already done %d, to run %d (out: %s)" % (len(jobs), len(jobs) - len(todo), len(todo), out), flush=True)
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = {ex.submit(one, j, out, a.keep): j for j in todo}
        for f in cf.as_completed(futs):
            j = futs[f]
            try:
                r = f.result()
                flag = " CONTAMINATED" if r["contaminated"] else (" ENV: " + r["environment"] if r["environment"] else "")
                print("%-4s %-50s %-24s %6.1fs $%s%s" % ("PASS" if r["pass"] else "FAIL", r["key"], r["evidence"][:24],
                                                     r["seconds"], r["cost_usd"], flag), flush=True)
            except Exception as e:
                print("ERR  %s: %s" % (key(j[0], j[1]["id"], j[2], j[3], j[4]), e), flush=True)
    after = subprocess.run(["git", "status", "--porcelain"], cwd=str(REPO), capture_output=True, text=True).stdout
    if after != before:
        print("WARNING: the repository changed during the run:\n" + after)
    else:
        print("repository unchanged (git status --porcelain identical before and after)")


def summarise(out):
    rows = {}
    for r in done_keys(out).values():
        if r.get("contaminated") or r.get("environment"):
            continue
        kk = (r["skill"], r["case"], r["model"], r["arm"])
        rows.setdefault(kk, []).append(r)
    return rows


def verdict(kind, decoy, rs):
    p = sum(1 for r in rs if r["pass"])
    if kind == "trigger":
        inv = sum(1 for r in rs if (not r["pass"]) == bool(decoy))  # invocations
        ok = inv == 0 if decoy else inv * 3 >= 2 * len(rs)
        return ok, "%d/%d invoked" % (inv, len(rs))
    return p == len(rs), "%d/%d" % (p, len(rs))


def cmd_report(a):
    out = Path(a.out)
    rows = summarise(out)
    cases = {}
    for name, (plugin, sk) in skills().items():
        for c in load_cases(sk):
            cases[(name, c["id"])] = c
    lines = ["| skill | case | kind | " + " | ".join(MODELS) + " | baseline (h/s/o) |", "|---|---|---|" + "---|" * (len(MODELS) + 1)]
    for (name, cid), c in sorted(cases.items()):
        k = kind_of(c)
        cells, base = [], []
        for m in MODELS:
            rs = rows.get((name, cid, m, "with"), [])
            if rs:
                ok, txt = verdict(k, c.get("decoy"), rs)
                cells.append(("" if ok else "**FAIL** ") + txt)
            else:
                cells.append("-")
            b = rows.get((name, cid, m, "without"), [])
            base.append("-" if not b else ("pass" if all(r["pass"] for r in b) else "fail"))
        lines.append("| %s | %s | %s | %s | %s |" % (name, cid, k + (" decoy" if c.get("decoy") else ""), " | ".join(cells),
                                                  "/".join(base) if k in ("action", "outcome") else ""))
    txt = "\n".join(lines)
    sys.stdout.reconfigure(encoding="utf-8")
    print(txt)
    bad = [r for r in done_keys(out).values() if r.get("contaminated") or r.get("environment")]
    if bad:
        print("\nleft out (rerun these): " + ", ".join("%s [%s]" % (r["key"], "contaminated" if r.get("contaminated") else r["environment"]) for r in bad))
    cost = sum(r.get("cost_usd") or 0 for r in done_keys(out).values())
    print("\nruns recorded %d, reported cost $%.2f" % (len(done_keys(out)), cost))
    if a.md:
        Path(a.md).write_text(txt + "\n", encoding="utf-8")


def cmd_export_worth(a):
    """One aggregate-result.json per skill in `claude plugin eval`'s shape, the value cases' with and without arms
    pooled over the models, for `evergreen.py worth <skill> --results <dir>/<skill> --record`."""
    out = Path(a.out)
    rows = summarise(out)
    for name, (plugin, sk) in skills().items():
        cases = []
        for c in load_cases(sk):
            if kind_of(c) not in ("action", "outcome"):
                continue
            arms = {}
            for arm in ("with", "without"):
                arms[arm] = [{"passed": bool(r["pass"]), "costUsd": r.get("cost_usd") or 0, "turns": r.get("turns") or 0,
                              "durationSeconds": r.get("seconds") or 0, "model": r.get("model")}
                             for m in MODELS for r in rows.get((name, c["id"], m, arm), [])]
            if arms["with"] and arms["without"]:
                cases.append({"name": c["id"], "arms": arms})
        if not cases:
            continue
        d = out / "worth" / name
        d.mkdir(parents=True, exist_ok=True)
        agg = {"suite": {"ablation": "with-without", "harness": "evals/run_evals.py (claude -p, --restricted)",
                         "models": MODELS}, "startedAt": time.strftime("%Y-%m-%dT%H:%M:%S"), "cases": cases}
        (d / "aggregate-result.json").write_text(json.dumps(agg, indent=2), encoding="utf-8")
        print("%-22s %s" % (name, d))


def cmd_regrade(a):
    """Grade recorded action runs again from their traces (after an evidence-matching fix); no model calls."""
    out = Path(a.out)
    cases = {(n, c["id"]): c for n, (_, sk) in skills().items() for c in load_cases(sk)}
    changed = 0
    for k, r in done_keys(out).items():
        c = cases.get((r["skill"], r["case"]))
        if not c or r["kind"] != "action" or r.get("environment") or not Path(r["trace"]).is_file():
            continue
        if r["pass"] and not Path(r["workdir"]).is_dir():
            continue  # a passed run's folder is deleted; its file evidence cannot be read again
        events = [json.loads(x) for x in open(r["trace"], encoding="utf-8") if x.strip().startswith("{")]
        ok, why = evidence_ok(c.get("evidence"), tool_uses(events), Path(r["workdir"]))
        if ok != r["pass"]:
            r = dict(r, prev_pass=r["pass"], prev_evidence=r["evidence"])
            r["pass"], r["evidence"] = ok, why + " (regraded)"
            with open(out / "results.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(r) + "\n")
            changed += 1
            print("%s %s: %s" % ("PASS" if ok else "FAIL", k, why[:120]))
    print("regraded %d runs" % changed)


def cmd_rejudge(a):
    """Grade recorded outcome runs that failed again, from their traces and kept folders (after a grading fix):
    checks and judge only, no new runs."""
    out = Path(a.out)
    allsk = skills()
    cases = {(n, c["id"]): c for n, (_, sk) in allsk.items() for c in load_cases(sk)}
    todo = [r for r in done_keys(out).values() if r["kind"] == "outcome" and not r["pass"] and not r.get("environment")
            and Path(r["workdir"]).is_dir() and Path(r["trace"]).is_file() and (r["skill"], r["case"]) in cases
            and (not a.skill or r["skill"] in a.skill.split(","))]
    print("rejudging %d failed outcome runs" % len(todo), flush=True)

    def one_r(r):
        c = cases[(r["skill"], r["case"])]
        events = [json.loads(x) for x in open(r["trace"], encoding="utf-8") if x.strip().startswith("{")]
        work, rdir = Path(r["workdir"]), Path(r["workdir"]).parent
        reply = final_text(events)
        (rdir / "reply.txt").write_text(reply, encoding="utf-8")
        checks = run_checks(c, allsk[r["skill"]][1], work, rdir / "reply.txt")
        ok_j, per = judge(c, reply, written_files(work), rdir / "judge")
        n = dict(r, reply=reply[:4000], checks=checks, judged=per, prev_pass=r["pass"])
        n["pass"] = all(x["exit"] == 0 for x in checks) and ok_j
        n["evidence"] = "checks %d/%d, judged %d/%d (rejudged)" % (sum(x["exit"] == 0 for x in checks), len(checks),
                                                                   sum(x["pass"] for x in per), len(per))
        with LOCK:
            with open(out / "results.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(n) + "\n")
        return n
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for n in ex.map(one_r, todo):
            print("%s %s %s" % ("PASS" if n["pass"] else "FAIL", n["key"], n["evidence"]), flush=True)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nm in ("plan", "run", "report", "export-worth", "regrade", "rejudge"):
        s = sub.add_parser(nm)
        s.add_argument("--out", default=str(out_default()))
        if nm in ("plan", "run"):
            s.add_argument("--skill", help="comma-separated skill names (default all)")
            s.add_argument("--case", help="case id glob")
            s.add_argument("--model", default=",".join(MODELS))
            s.add_argument("--runs", type=int, help="with-skill runs per case (default the case's runs, 3)")
            s.add_argument("--arm", choices=["with", "without", "both"], default="both")
        if nm == "rejudge":
            s.add_argument("--skill")
            s.add_argument("--jobs", type=int, default=4)
        if nm == "run":
            s.add_argument("--jobs", type=int, default=4)
            s.add_argument("--rerun", action="store_true", help="run again even when a result is recorded")
            s.add_argument("--keep", action="store_true", help="keep run folders that passed")
        if nm == "report":
            s.add_argument("--md", help="also write the matrix to this file")
    a = ap.parse_args()
    {"plan": cmd_plan, "run": cmd_run, "report": cmd_report, "export-worth": cmd_export_worth, "regrade": cmd_regrade, "rejudge": cmd_rejudge}[a.cmd](a)


if __name__ == "__main__":
    main()
