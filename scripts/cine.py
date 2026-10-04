#!/usr/bin/env python3
"""cinewright maintainer CLI. Not shipped; the skills ship shared/lib/cine.py.

  python scripts/cine.py [--root DIR] kb index|search|show|lint
  python scripts/cine.py cards|compile|continuity ...   (same as the skill copy)
  python scripts/cine.py budget [--json]
  python scripts/cine.py zip SKILL [--out DIR]
  python scripts/cine.py build

Python 3.9+, standard library only.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("cine_lib", REPO / "shared" / "lib" / "cine.py")
lib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lib)

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
COMPANIONS = ["RESEARCH.md", "CHANGELOG.md", "LEARNINGS.md", "TESTS.md", "evergreen.json", "evals/evals.json"]
AGENT_PLUGINS_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
SHIPPED = ["plugins", "shared", "examples", "scripts", "tests", ".github", ".claude-plugin", "README.md"]
PRIVATE_PATTERNS = [
    (re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/][A-Za-z]"), "local drive path"),
    (re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b"), "LAN address"),
    (re.compile(r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "LAN address"),
    (re.compile(r"\bRTX ?\d{4}\b"), "GPU model"),
]
BUDGETS = [  # key, label, green max, yellow max
    ("skill_lines", "SKILL.md lines", 80, 120),
    ("skill_tokens", "SKILL.md body tokens (est.)", 1200, 2000),
    ("desc_chars", "one description, characters", 350, 500),
    ("desc_total", "all descriptions, characters", 4000, 5500),
    ("desc_core", "core descriptions, characters", 1800, 2500),
    ("entry_lines", "reference entry lines", 60, 100),
    ("entry_tokens", "reference entry tokens (est.)", 700, 1200),
    ("index_tokens", "references/INDEX.md tokens (est.)", 1500, 3000),
    ("skill_kb", "skill folder KB", 150, 300),
    ("plugin_files", "files per plugin", 350, 450),
    ("repo_zip_kb", "repo ZIP KB", 2048, 5120),
]
HEADER_RE = re.compile(r"copied from (shared/[\w./-]+) sha256:([0-9a-f]{64})")


# ---------- repo layout ----------

def skills(root):
    return sorted(p.parent for p in root.glob("plugins/*/skills/*/SKILL.md"))


def repo_context(root):
    dirs = [s / "references" for s in skills(root) if (s / "references").is_dir()]
    return lib.Context(dirs, dirs, root / "shared" / "schemas", [(d.parent.name, d) for d in dirs])


def find_skill(root, name):
    for s in skills(root):
        if s.name == name:
            return s
    raise SystemExit("no skill '%s' under plugins/*/skills/" % name)


def tokens(text):
    return (len(text.encode("utf-8")) + 3) // 4


def rel(root, p):
    return Path(p).resolve().relative_to(root.resolve()).as_posix()


# ---------- build: copy shared sources into skills ----------

def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render_copy(root, src_rel):
    """Return the exact text a skill copy of shared/<src_rel> must hold."""
    src = lib.read_text(root / src_rel)
    header = "copied from %s sha256:%s; edit the source" % (src_rel, sha(src))
    if src_rel.endswith(".md"):
        end = src.find("\n---\n", 3)
        if not src.startswith("---\n") or end < 0:
            return "<!-- %s -->\n%s" % (header, src)
        cut = end + 5
        return "%s<!-- %s -->\n%s" % (src[:cut], header, src[cut:])
    if src_rel.endswith(".py"):
        lines = src.split("\n", 1)
        if lines[0].startswith("#!"):
            return "%s\n# %s\n%s" % (lines[0], header, lines[1] if len(lines) > 1 else "")
        return "# %s\n%s" % (header, src)
    if src_rel.endswith(".json"):
        data = json.loads(src)
        return json.dumps(dict([("$comment", header)] + list(data.items())), indent=2, ensure_ascii=False) + "\n"
    raise SystemExit("no copy rule for %s" % src_rel)


def planned_copies(root, skill):
    """(source relative to repo, destination path) for every entry in needs.json."""
    nf = skill / "needs.json"
    if not nf.is_file():
        return []
    needs = json.loads(lib.read_text(nf))
    out = []
    for name in needs.get("vocab", []):
        out.append(("shared/vocab/%s" % name, skill / "references" / name))
    for name in needs.get("lib", []):
        out.append(("shared/lib/%s" % name, skill / "scripts" / name))
    for name in needs.get("schemas", []):
        out.append(("shared/schemas/%s" % name, skill / "scripts" / "schemas" / name))
    return out


def cmd_build(root, a):
    n = 0
    for s in skills(root):
        for src, dst in planned_copies(root, s):
            text = render_copy(root, src)
            if not dst.is_file() or lib.read_text(dst) != text:
                lib.write_text(dst, text)
                print("copied %s -> %s" % (src, rel(root, dst)))
                n += 1
        if (s / "references").is_dir():
            idx = lib.index_text(s.name, s / "references")
            if not (s / "references" / "INDEX.md").is_file() or lib.read_text(s / "references" / "INDEX.md") != idx:
                lib.write_text(s / "references" / "INDEX.md", idx)
                print("indexed %s" % rel(root, s / "references" / "INDEX.md"))
                n += 1
    print("build: %d files written" % n)
    return 0


# ---------- lint ----------

def md_files(root):
    out = []
    for top in SHIPPED + ["ai-docs", "AGENTS.md"]:
        p = root / top
        if p.is_file() and p.suffix == ".md":
            out.append(p)
        elif p.is_dir():
            out += [f for f in p.rglob("*.md") if "__pycache__" not in f.parts]
    return out


def check_links(root, path, text, errs):
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    body = re.sub(r"`[^`\n]*`", "", body)
    if "[[" in body:
        errs.append("%s: wikilink found; use relative markdown links" % rel(root, path))
    for target in re.findall(r"\]\(([^)\s]+)\)", body):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        t = target.split("#")[0]
        if t and not (path.parent / t).exists():
            errs.append("%s: broken link %s" % (rel(root, path), target))


def lint_skill(root, s, ctx, errs):
    tag = rel(root, s)
    meta, body = lib.parse_frontmatter(lib.read_text(s / "SKILL.md"))
    extra = set(meta) - ALLOWED_KEYS
    if extra:
        errs.append("%s/SKILL.md: frontmatter keys outside the six allowed: %s" % (tag, ", ".join(sorted(extra))))
    if meta.get("name") != s.name:
        errs.append("%s/SKILL.md: name '%s' must equal the folder name" % (tag, meta.get("name")))
    d = meta.get("description", "")
    if not 1 <= len(d) <= 1024:
        errs.append("%s/SKILL.md: description must be 1-1024 characters (%d)" % (tag, len(d)))
    if "<" in d or ">" in d:
        errs.append("%s/SKILL.md: angle bracket in description" % tag)
    for c in COMPANIONS:
        if not (s / c).is_file():
            errs.append("%s: missing %s" % (tag, c))
    if (s / "evals" / "evals.json").is_file():
        ev = json.loads(lib.read_text(s / "evals" / "evals.json")).get("evals", [])
        trig = [e for e in ev if e.get("kind") == "trigger" and not e.get("decoy")]
        dec = [e for e in ev if e.get("decoy")]
        act = [e for e in ev if e.get("kind") == "action" and e.get("evidence")]
        out = [e for e in ev if e.get("kind") == "outcome"]
        if len(trig) < 2 or len(dec) < 2 or not act or not out:
            errs.append("%s/evals/evals.json: needs 2 triggers, 2 decoys, 1 action with evidence, 1 outcome" % tag)
        if "TODO" in json.dumps([e.get("prompt", "") for e in ev]):
            errs.append("%s/evals/evals.json: TODO left in a prompt" % tag)
    entry_schema = lib.load_schema(ctx, "entry")
    model_schema = lib.load_schema(ctx, "model-card")
    refs = s / "references"
    copies = {dst.resolve() for _, dst in planned_copies(root, s)}
    for p, m, b in (lib.entries(refs) if refs.is_dir() else []):
        ptag = rel(root, p)
        for e in lib.validate(m, entry_schema):
            errs.append("%s: %s" % (ptag, e))
        if m.get("slug") != p.stem:
            errs.append("%s: slug '%s' must equal the file name" % (ptag, m.get("slug")))
        for sec in lib.split_sections(b):
            if sec not in lib.SECTIONS:
                errs.append("%s: section '%s' is not one of %s" % (ptag, sec, ", ".join(lib.SECTIONS)))
        if "model" in m:
            for e in lib.validate(m, model_schema):
                errs.append("%s: %s" % (ptag, e))
            cb = lib.compile_block(b)
            if cb is None:
                errs.append("%s: model card without a Compile json block" % ptag)
            else:
                for e in lib.validate(cb, model_schema["$defs"]["compile"]):
                    errs.append("%s: Compile %s" % (ptag, e))
        if HEADER_RE.search(lib.read_text(p)) and p.resolve() not in copies:
            errs.append("%s: holds a copy header but needs.json does not list it; delete it or list it" % ptag)
    if refs.is_dir():
        idx = refs / "INDEX.md"
        if not idx.is_file() or lib.read_text(idx) != lib.index_text(s.name, refs):
            errs.append("%s: references/INDEX.md is stale; run cine.py build" % tag)
    for src, dst in planned_copies(root, s):
        if not (root / src).is_file():
            errs.append("%s/needs.json: %s does not exist" % (tag, src))
        elif not dst.is_file():
            errs.append("%s: missing copy of %s; run cine.py build" % (rel(root, dst), src))
        elif lib.read_text(dst) != render_copy(root, src):
            errs.append("%s: drift from %s (hand edit or source changed); edit the source, then cine.py build" % (rel(root, dst), src))


def lint_manifests(root, errs):
    mp = root / ".claude-plugin" / "marketplace.json"
    if not mp.is_file():
        errs.append(".claude-plugin/marketplace.json missing")
        return
    m = json.loads(lib.read_text(mp))
    if not m.get("name") or not m.get("owner", {}).get("name") or not m.get("plugins"):
        errs.append("marketplace.json: needs name, owner.name and plugins")
    for entry in m.get("plugins", []):
        src = root / entry.get("source", "")
        if not entry.get("name") or not src.is_dir():
            errs.append("marketplace.json: plugin %s has no folder %s" % (entry.get("name"), entry.get("source")))
            continue
        cp = src / ".claude-plugin" / "plugin.json"
        ap = src / "plugin.json"
        for f in (cp, ap, src / "README.md", src / "LICENSE"):
            if not f.is_file():
                errs.append("%s: missing" % rel(root, f))
        if cp.is_file() and json.loads(lib.read_text(cp)).get("name") != entry["name"]:
            errs.append("%s: name differs from the marketplace entry" % rel(root, cp))
        if ap.is_file():
            j = json.loads(lib.read_text(ap))
            if j.get("$schema") != AGENT_PLUGINS_SCHEMA or j.get("name") != entry["name"]:
                errs.append("%s: needs $schema %s and name %s" % (rel(root, ap), AGENT_PLUGINS_SCHEMA, entry["name"]))
        if (src / "bin").exists():
            errs.append("%s/bin: claude.ai refuses a plugin with a top-level bin/" % rel(root, src))
        if (src / "README.md").is_file() and len(lib.read_text(src / "README.md").split()) < 40:
            errs.append("%s/README.md: under 40 words" % rel(root, src))


def lint(root):
    errs = []
    ctx = repo_context(root)
    for s in skills(root):
        lint_skill(root, s, ctx, errs)
    lint_manifests(root, errs)
    for f in md_files(root):
        text = lib.read_text(f)
        check_links(root, f, text, errs)
        if "—" in text and not rel(root, f).startswith("ai-docs/"):
            errs.append("%s: em dash" % rel(root, f))
    for top in SHIPPED:
        p = root / top
        files = [p] if p.is_file() else ([f for f in p.rglob("*") if f.is_file()] if p.is_dir() else [])
        for f in files:
            if f.is_symlink():
                errs.append("%s: symlink" % rel(root, f))
            if f.suffix not in (".md", ".json", ".py", ".yml", ".txt") or "__pycache__" in f.parts:
                continue
            text = lib.read_text(f)
            for rx, what in PRIVATE_PATTERNS:
                if rx.search(text):
                    errs.append("%s: %s (%s)" % (rel(root, f), what, rx.search(text).group(0)))
    return errs


# ---------- budget ----------

def status(value, green, yellow):
    return "green" if value <= green else ("yellow" if value <= yellow else "red")


def repo_zip_kb(root):
    try:
        names = subprocess.run(["git", "ls-files", "-z"], cwd=str(root), capture_output=True, check=True).stdout.decode("utf-8").split("\0")
        files = [root / n for n in names if n and (root / n).is_file()]
    except (OSError, subprocess.CalledProcessError):
        files = [f for f in root.rglob("*") if f.is_file() and ".git" not in f.parts]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, rel(root, f))
    return buf.tell() // 1024


def duplicates(root):
    seen, dups = {}, []
    for s in skills(root):
        copies = {dst.resolve() for _, dst in planned_copies(root, s)}
        # knowledge only: SKILL.md boilerplate (Step 0, Maintenance) repeats by design
        files = [p for p in (s / "references").glob("*.md") if p.name != "INDEX.md" and p.resolve() not in copies]
        for f in files:
            for para in re.split(r"\n\s*\n", lib.parse_frontmatter(lib.read_text(f))[1]):
                norm = " ".join(para.split())
                if len(norm) < 80:
                    continue
                if norm in seen and seen[norm][0] != s.name:
                    dups.append((rel(root, f), seen[norm][1], norm[:60]))
                else:
                    seen.setdefault(norm, (s.name, rel(root, f)))
    return dups


def measure(root):
    rows = {k: (0, "") for k, *_ in BUDGETS}

    def worst(key, value, where):
        if value >= rows[key][0]:
            rows[key] = (value, where)

    total = core = 0
    for s in skills(root):
        text = lib.read_text(s / "SKILL.md")
        meta, body = lib.parse_frontmatter(text)
        worst("skill_lines", len(text.rstrip("\n").split("\n")), rel(root, s / "SKILL.md"))
        worst("skill_tokens", tokens(body), rel(root, s / "SKILL.md"))
        d = len(meta.get("description", ""))
        worst("desc_chars", d, s.name)
        total += d
        if s.parent.parent.name == "cinewright":
            core += d
        for p in (s / "references").glob("*.md"):
            t = lib.read_text(p)
            if p.name == "INDEX.md":
                worst("index_tokens", tokens(t), rel(root, p))
            else:
                worst("entry_lines", len(t.rstrip("\n").split("\n")), rel(root, p))
                worst("entry_tokens", tokens(t), rel(root, p))
        kb = sum(f.stat().st_size for f in s.rglob("*") if f.is_file() and "__pycache__" not in f.parts) // 1024
        worst("skill_kb", kb, s.name)
    rows["desc_total"] = (total, "%d skills" % len(skills(root)))
    rows["desc_core"] = (core, "plugins/cinewright")
    for pl in root.glob("plugins/*"):
        worst("plugin_files", sum(1 for f in pl.rglob("*") if f.is_file() and "__pycache__" not in f.parts), pl.name)
    rows["repo_zip_kb"] = (repo_zip_kb(root), "tracked files")
    return rows


def cmd_budget(root, a):
    rows = measure(root)
    dups = duplicates(root)
    report = []
    for key, label, g, y in BUDGETS:
        v, where = rows[key]
        report.append({"measure": label, "value": v, "green": g, "yellow": y, "status": status(v, g, y), "worst": where})
    report.append({"measure": "duplicate paragraphs across skills", "value": len(dups), "green": 0, "yellow": 1000,
                   "status": "green" if not dups else "yellow", "worst": dups[0][0] if dups else ""})
    overall = "red" if any(r["status"] == "red" for r in report) else ("yellow" if any(r["status"] == "yellow" for r in report) else "green")
    if a.json:
        print(json.dumps({"overall": overall, "rows": report, "duplicates": dups}, indent=2))
    else:
        print("%-38s %8s %8s %8s  %-6s %s" % ("measure", "value", "green<=", "yellow<=", "status", "worst"))
        for r in report:
            print("%-38s %8s %8s %8s  %-6s %s" % (r["measure"], r["value"], r["green"], r["yellow"], r["status"], r["worst"]))
        for f, other, snippet in dups:
            print("  duplicate: %s repeats %s: %s..." % (f, other, snippet))
        print("budget: %s (tokens are bytes / 4, an estimate)" % overall.upper())
    return 2 if overall == "red" else 0


# ---------- zip ----------

def cmd_zip(root, a):
    s = find_skill(root, a.skill)
    meta, _ = lib.parse_frontmatter(lib.read_text(s / "SKILL.md"))
    extra = set(meta) - ALLOWED_KEYS
    if extra or meta.get("name") != s.name:
        raise SystemExit("SKILL.md frontmatter not uploadable: extra keys %s, name %s" % (sorted(extra), meta.get("name")))
    out = Path(a.out or root / "dist")
    out.mkdir(parents=True, exist_ok=True)
    target = out / ("%s.zip" % s.name)
    files = sorted(f for f in s.rglob("*") if f.is_file() and "__pycache__" not in f.parts and f.suffix != ".pyc")
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, "%s/%s" % (s.name, f.relative_to(s).as_posix()))
    with zipfile.ZipFile(target) as z:
        names = z.namelist()
    tops = {n.split("/")[0] for n in names}
    if tops != {s.name} or "%s/SKILL.md" % s.name not in names:
        raise SystemExit("zip check failed: top level %s" % sorted(tops))
    print("wrote %s: %d files, %d KB, top folder %s/" % (target, len(names), target.stat().st_size // 1024, s.name))
    return 0


# ---------- main ----------

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = REPO
    if argv[:1] == ["--root"]:
        root = Path(argv[1]).resolve()
        argv = argv[2:]
    group = argv[0] if argv else ""
    if group == "kb" and argv[1:2] == ["lint"]:
        errs = lint(root)
        for e in errs:
            print("ERROR %s" % e)
        print("kb lint: %d skills, %d errors" % (len(skills(root)), len(errs)))
        return 1 if errs else 0
    if group in ("budget", "zip", "build"):
        ap = argparse.ArgumentParser(prog="cine.py %s" % group)
        if group == "budget":
            ap.add_argument("--json", action="store_true")
        if group == "zip":
            ap.add_argument("skill")
            ap.add_argument("--out")
        a = ap.parse_args(argv[1:])
        return {"budget": cmd_budget, "zip": cmd_zip, "build": cmd_build}[group](root, a)
    if group in ("", "-h", "--help"):
        print(__doc__)
        lib.build_parser().print_help()
        return 0
    return lib.main(argv, repo_context(root))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
