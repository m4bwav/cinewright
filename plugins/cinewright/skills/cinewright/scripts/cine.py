#!/usr/bin/env python3
# copied from shared/lib/cine.py sha256:c652df7cb0bb73fe25a9cac0e3fdff2572439aa7050d309f6b32f61653b3a979; edit the source
"""cinewright runtime CLI: kb, cards, compile, continuity.

Run it; do not read it. Python 3.9+, standard library only.

  python scripts/cine.py kb index|search WORDS|show SLUG [--section NAME]
  python scripts/cine.py cards new PROJECT --id 1D --scene 1 [--cast a,b]
  python scripts/cine.py cards validate PROJECT
  python scripts/cine.py cards export PROJECT --film-json [--out FILE]
  python scripts/cine.py compile PROJECT --model veo [--card ID ...] [--sequence] [--out DIR]
  python scripts/cine.py continuity diff PROJECT [--with CARD.json] [--json]

A PROJECT folder holds bibles/style.json, characters.json, locations.json,
scenes.json and cards/*.json (one shot card per file).
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

SIZES = ["EWS", "WS", "FS", "MWS", "MS", "MCU", "CU", "ECU"]
SIZE_WORDS = {
    "EWS": "extreme wide shot", "WS": "wide shot", "FS": "full shot",
    "MWS": "medium wide shot", "MS": "medium shot", "MCU": "medium close-up",
    "CU": "close-up", "ECU": "extreme close-up",
}
ANGLE_WORDS = {
    "eye-level": "eye-level angle", "high": "high angle looking down",
    "low": "low angle looking up", "overhead": "overhead shot looking straight down",
    "ground": "ground-level angle", "dutch": "dutch angle",
}
MOVE_WORDS = {
    "static": "static camera", "pan-left": "slow pan left", "pan-right": "slow pan right",
    "tilt-up": "slow tilt up", "tilt-down": "slow tilt down",
    "dolly-in": "slow dolly in", "dolly-out": "slow dolly out",
    "truck-left": "camera trucks left", "truck-right": "camera trucks right",
    "track": "tracking shot following the subject", "crane-up": "crane up",
    "crane-down": "crane down", "handheld": "handheld camera",
    "zoom-in": "slow zoom in", "zoom-out": "slow zoom out",
}
TRAVEL_WORDS = {
    "left-to-right": "moving from left to right across the frame",
    "right-to-left": "moving from right to left across the frame",
    "toward-camera": "walking toward the camera",
    "away-from-camera": "walking away from the camera",
}
EYELINE_WORDS = {
    "frame-left": "looking toward frame left", "frame-right": "looking toward frame right",
    "up": "looking up", "down": "looking down", "camera": "looking into the lens",
}
POSITION_WORDS = {"frame-left": "on the left of the frame", "center": "in the center of the frame",
                  "frame-right": "on the right of the frame"}
FLIP = {"left-to-right": "right-to-left", "right-to-left": "left-to-right",
        "frame-left": "frame-right", "frame-right": "frame-left"}
POS_INDEX = {"frame-left": 0, "center": 1, "frame-right": 2}
SECTIONS = ["Rules", "Numbers", "Vocabulary", "Pitfalls", "Verify", "Notes", "Compile"]


# ---------- context ----------

class Context:
    """Where references, model cards and schemas live. The repo CLI builds its own."""

    def __init__(self, ref_dirs, model_dirs, schema_dir, index_targets=None):
        self.ref_dirs = [Path(d) for d in ref_dirs]
        self.model_dirs = [Path(d) for d in model_dirs]
        self.schema_dir = Path(schema_dir)
        # (skill name, references dir) pairs that `kb index` rewrites
        self.index_targets = index_targets or []


def default_context():
    skill = HERE.parent
    own = skill / "references"
    siblings = sorted(p / "references" for p in skill.parent.glob("*") if p != skill and (p / "references").is_dir())
    schema_dir = HERE / "schemas"
    if not schema_dir.is_dir():
        for up in HERE.parents:
            if (up / "shared" / "schemas").is_dir():
                schema_dir = up / "shared" / "schemas"
                break
    dirs = ([own] if own.is_dir() else []) + siblings
    return Context(dirs, dirs, schema_dir, [(skill.name, own)] if own.is_dir() else [])


# ---------- small parsers ----------

def read_text(path):
    return Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _scalar(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1].replace('\\"', '"')
    return s


def _list(s):
    items = re.findall(r'\s*(?:"((?:[^"\\]|\\.)*)"|\'([^\']*)\'|([^,\[\]]+))', s.strip()[1:-1])
    out = []
    for a, b, c in items:
        v = a.replace('\\"', '"') if a else (b if b else c.strip())
        if v:
            out.append(v)
    return out


def parse_frontmatter(text):
    """Return (meta, body). Supports key: value, key: [a, b] and '- item' lists."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 3)
    if end < 0:
        if text.rstrip().endswith("\n---"):
            end = text.rstrip().rfind("\n---")
        else:
            return {}, text
    block, body = text[4:end], text[end + 5:]
    meta, key = {}, None
    for line in block.split("\n"):
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            meta[key] = _list(val) if val.startswith("[") else (_scalar(val) if val else [])
        elif line.lstrip().startswith("- ") and key is not None and isinstance(meta.get(key), list):
            meta[key].append(_scalar(line.lstrip()[2:]))
    return meta, body


def split_sections(body):
    out, name = {}, None
    for line in body.split("\n"):
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            name = m.group(1)
            out[name] = []
        elif name:
            out[name].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def compile_block(body):
    sec = split_sections(body).get("Compile", "")
    m = re.search(r"```json\n(.*?)\n```", sec, re.S)
    return json.loads(m.group(1)) if m else None


# ---------- mini JSON Schema validator (the subset the schemas use) ----------

_TYPES = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "null": lambda v: v is None,
}


def validate(inst, schema, path="$", root=None):
    root = root if root is not None else schema
    errs = []
    if "$ref" in schema:
        node = root
        for part in schema["$ref"].lstrip("#/").split("/"):
            node = node[part]
        return validate(inst, node, path, root)
    if "enum" in schema and inst not in schema["enum"]:
        return ["%s: %r is not one of %s" % (path, inst, ", ".join(map(str, schema["enum"])))]
    t = schema.get("type")
    if t:
        types = t if isinstance(t, list) else [t]
        if not any(_TYPES[x](inst) for x in types):
            return ["%s: expected %s, got %s" % (path, "/".join(types), type(inst).__name__)]
    if isinstance(inst, str):
        if len(inst) < schema.get("minLength", 0):
            errs.append("%s: shorter than %d characters" % (path, schema["minLength"]))
        if "maxLength" in schema and len(inst) > schema["maxLength"]:
            errs.append("%s: longer than %d characters (%d)" % (path, schema["maxLength"], len(inst)))
        if "pattern" in schema and not re.search(schema["pattern"], inst):
            errs.append("%s: %r does not match %s" % (path, inst, schema["pattern"]))
        if schema.get("format") == "date":
            try:
                datetime.date.fromisoformat(inst)
            except ValueError:
                errs.append("%s: %r is not a YYYY-MM-DD date" % (path, inst))
    if _TYPES["number"](inst):
        if "minimum" in schema and inst < schema["minimum"]:
            errs.append("%s: %s is below %s" % (path, inst, schema["minimum"]))
        if "maximum" in schema and inst > schema["maximum"]:
            errs.append("%s: %s is above %s" % (path, inst, schema["maximum"]))
    if isinstance(inst, list):
        if len(inst) < schema.get("minItems", 0):
            errs.append("%s: needs at least %d items" % (path, schema["minItems"]))
        if "items" in schema:
            for i, v in enumerate(inst):
                errs += validate(v, schema["items"], "%s[%d]" % (path, i), root)
    if isinstance(inst, dict):
        for k in schema.get("required", []):
            if k not in inst:
                errs.append("%s: missing required '%s'" % (path, k))
        props = schema.get("properties", {})
        extra = schema.get("additionalProperties", True)
        for k, v in inst.items():
            if k in props:
                errs += validate(v, props[k], "%s.%s" % (path, k), root)
            elif extra is False:
                errs.append("%s: unknown key '%s'" % (path, k))
            elif isinstance(extra, dict):
                errs += validate(v, extra, "%s.%s" % (path, k), root)
    return errs


def load_schema(ctx, name):
    path = ctx.schema_dir / ("%s.schema.json" % name)
    data = json.loads(read_text(path))
    data.pop("$comment", None)
    return data


# ---------- knowledge base ----------

def entries(ref_dir):
    out = []
    for p in sorted(Path(ref_dir).glob("*.md")):
        if p.name == "INDEX.md":
            continue
        meta, body = parse_frontmatter(read_text(p))
        out.append((p, meta, body))
    return out


def index_text(skill_name, ref_dir):
    lines = ["# %s references" % skill_name, "",
             "Generated by `cine.py kb index`; do not hand-edit. Open one entry with "
             "`python scripts/cine.py kb show <slug> --section <name>` (sections: Rules, Numbers, "
             "Vocabulary, Pitfalls, Verify, Notes).", ""]
    for p, meta, _ in entries(ref_dir):
        lines.append("- `%s`: %s" % (meta.get("slug", p.stem), meta.get("summary", "(no summary)")))
    return "\n".join(lines) + "\n"


def kb_search(ctx, words):
    terms = [w.lower() for w in words]
    hits, seen = [], set()
    for d in ctx.ref_dirs:
        for p, meta, body in entries(d):
            if p.name in seen:  # the same vocab copy ships in several skills
                continue
            seen.add(p.name)
            head = " ".join([meta.get("title", ""), meta.get("summary", ""), " ".join(meta.get("tags", []))]).lower()
            score = sum(3 * head.count(t) + body.lower().count(t) for t in terms)
            if score:
                hits.append((score, meta.get("slug", p.stem), d.parent.name, meta.get("summary", "")))
    hits.sort(key=lambda h: (-h[0], h[1]))
    return hits


def kb_find(ctx, slug):
    for d in ctx.ref_dirs:
        p = d / ("%s.md" % slug)
        if p.is_file():
            return p
    return None


def cmd_kb(ctx, a):
    if a.cmd == "index":
        for name, d in ctx.index_targets:
            write_text(d / "INDEX.md", index_text(name, d))
            print("wrote %s" % (d / "INDEX.md"))
        return 0
    if a.cmd == "search":
        hits = kb_search(ctx, a.words)
        for score, slug, skill, summary in hits[:a.limit]:
            print("%s (%s): %s" % (slug, skill, summary))
        if not hits:
            print("no entry matches; try fewer or broader words")
        return 0 if hits else 1
    if a.cmd == "show":
        p = kb_find(ctx, a.slug)
        if not p:
            print("no entry '%s'; run `kb search`" % a.slug, file=sys.stderr)
            return 1
        meta, body = parse_frontmatter(read_text(p))
        if a.section:
            secs = split_sections(body)
            if a.section not in secs:
                print("no section '%s' in %s; it has: %s" % (a.section, a.slug, ", ".join(secs)), file=sys.stderr)
                return 1
            print("## %s\n\n%s" % (a.section, secs[a.section]))
        else:
            print(body.strip())
        print("\n(last_checked %s; sources: %s)" % (meta.get("last_checked", "?"), "; ".join(meta.get("sources", []))))
        return 0
    return 2


# ---------- projects and cards ----------

class Project:
    def __init__(self, root, overrides=None):
        self.root = Path(root)
        b = self.root / "bibles"
        self.style = json.loads(read_text(b / "style.json"))
        self.characters = json.loads(read_text(b / "characters.json"))
        self.locations = json.loads(read_text(b / "locations.json"))
        self.scenes = json.loads(read_text(b / "scenes.json"))
        self.card_files = sorted((self.root / "cards").glob("*.json"))
        self.cards = [json.loads(read_text(p)) for p in self.card_files]
        for f in overrides or []:
            # --with FILE: the card in FILE replaces the project card with the same id
            new = json.loads(read_text(f))
            self.cards = [c for c in self.cards if c.get("id") != new.get("id")] + [new]
        self.cards.sort(key=lambda c: c.get("order", 0))
        self.chars = {c["id"]: c for c in self.characters.get("characters", [])}
        self.locs = {x["id"]: x for x in self.locations.get("locations", [])}
        self.scene_map = {s["id"]: s for s in self.scenes.get("scenes", [])}


def wardrobe_for(char, scene_id):
    w = char.get("wardrobe", {})
    return w.get(scene_id, w.get("default", ""))


def validate_project(ctx, p):
    errs = []
    for name, data in [("style-bible", p.style), ("character-bible", p.characters),
                       ("location-bible", p.locations), ("scene-axis-bible", p.scenes)]:
        errs += ["bibles/%s: %s" % (name, e) for e in validate(data, load_schema(ctx, name))]
    card_schema = load_schema(ctx, "shot-card")
    seen_ids, seen_orders = set(), set()
    for path, card in zip(p.card_files, [json.loads(read_text(f)) for f in p.card_files]):
        tag = "cards/%s" % path.name
        errs += ["%s: %s" % (tag, e) for e in validate(card, card_schema)]
        if "TODO" in json.dumps(card):
            errs.append("%s: still holds TODO" % tag)
        cid, order = card.get("id"), card.get("order")
        if cid in seen_ids:
            errs.append("%s: duplicate id %s" % (tag, cid))
        if order in seen_orders:
            errs.append("%s: duplicate order %s" % (tag, order))
        seen_ids.add(cid)
        seen_orders.add(order)
        if card.get("scene") not in p.scene_map:
            errs.append("%s: scene '%s' is not in scenes.json" % (tag, card.get("scene")))
        for m in card.get("cast", []):
            if m.get("id") not in p.chars:
                errs.append("%s: cast '%s' is not in characters.json" % (tag, m.get("id")))
        for d in card.get("dialogue", []):
            if d.get("character") not in p.chars:
                errs.append("%s: speaker '%s' is not in characters.json" % (tag, d.get("character")))
    for s in p.scenes.get("scenes", []):
        if s.get("location") not in p.locs:
            errs.append("bibles/scenes.json: scene %s location '%s' is not in locations.json" % (s.get("id"), s.get("location")))
    return errs


def new_card(p, cid, scene, cast_ids, order=None):
    if scene not in p.scene_map:
        raise SystemExit("scene '%s' is not in scenes.json" % scene)
    cast = []
    for c in cast_ids:
        if c not in p.chars:
            raise SystemExit("character '%s' is not in characters.json" % c)
        ch = p.chars[c]
        cast.append({"id": c, "identity": ch["identity"], "wardrobe": wardrobe_for(ch, scene)})
    return {
        "id": cid, "scene": scene,
        "order": order or (max([c.get("order", 0) for c in p.cards] or [0]) + 1),
        "duration_s": 4,
        "beat": "TODO: what this shot tells the audience",
        "camera": {"size": "MS", "angle": "eye-level", "azimuth_deg": 90, "move": "static", "lens_mm": 35, "side": "A", "framing": "single"},
        "cast": cast,
        "action": "TODO: one action, present tense",
        "time_of_day": p.scene_map[scene]["time_of_day"],
    }


def resolution_size(resolution, aspect):
    short = {"480p": 480, "720p": 720, "1080p": 1080, "1440p": 1440, "4k": 2160, "2160p": 2160}.get(resolution.lower())
    if short is None:
        raise SystemExit("unknown resolution '%s'" % resolution)
    a, b = (float(x) for x in aspect.split(":"))
    long_side = int(round(short * max(a, b) / min(a, b) / 2.0)) * 2
    return (long_side, short) if a >= b else (short, long_side)


def film_json(p, xfade=0.16):
    st = p.style
    w, h = resolution_size(st["resolution"], st["aspect_ratio"])
    fps = st["fps"]
    refs = list(st.get("refs", []))
    for ch in p.characters.get("characters", []):
        for r in ch.get("refs", []):
            if r not in refs:
                refs.append(r)
    shots = []
    for c in p.cards:
        shot = {"name": "shot_%s" % c["id"], "seed": c.get("seed", c["order"]), "length": int(round(c["duration_s"] * fps))}
        if c.get("refs"):
            shot["refs"] = c["refs"]
        shots.append(shot)
    name = re.sub(r"[^a-z0-9]+", "_", st["title"].lower()).strip("_")
    out = {"name": name, "target_seconds": st.get("target_seconds", sum(c["duration_s"] for c in p.cards)),
           "width": w, "height": h}
    if refs:
        out["refs"] = refs
    out["seam_audio_xfade"] = xfade
    out["shots"] = shots
    return out


def cmd_cards(ctx, a):
    p = Project(a.project)
    if a.cmd == "validate":
        errs = validate_project(ctx, p)
        for e in errs:
            print("ERROR %s" % e)
        print("cards validate: %d cards, %d errors" % (len(p.cards), len(errs)))
        return 1 if errs else 0
    if a.cmd == "new":
        card = new_card(p, a.id, a.scene, [c for c in (a.cast or "").split(",") if c], a.order)
        out = p.root / "cards" / ("%s.json" % a.id)
        if out.exists():
            raise SystemExit("%s exists" % out)
        write_text(out, json.dumps(card, indent=2, ensure_ascii=False) + "\n")
        print("wrote %s (fill every TODO, then run cards validate)" % out)
        return 0
    if a.cmd == "export":
        if not a.film_json:
            raise SystemExit("choose an export format: --film-json")
        text = json.dumps(film_json(p, a.xfade), indent=2, ensure_ascii=False) + "\n"
        if a.out:
            write_text(a.out, text)
            print("wrote %s" % a.out)
        else:
            sys.stdout.write(text)
        return 0
    return 2


# ---------- continuity diff ----------

def continuity_diff(p):
    """Every card against the bibles and against the previous card in its scene."""
    issues = []

    def add(level, card, code, msg):
        issues.append({"level": level, "card": card.get("id", "?"), "code": code, "message": msg})

    prev_by_scene = {}
    for card in p.cards:
        sc = p.scene_map.get(card.get("scene"))
        if not sc:
            add("error", card, "SCENE", "scene '%s' is not in scenes.json" % card.get("scene"))
            continue
        axis = sc.get("axis", {})
        cam = card.get("camera", {})
        side = cam.get("side", "A")
        flipped = side == "B"
        if flipped and not cam.get("crosses_axis"):
            add("error", card, "AXIS", "camera is on side B of the %s axis (%s): it crosses the line, so every left and right flips. "
                "Move it to side A, or set crosses_axis with a cross_reason (a neutral shot or a move seen on screen)." % (sc["id"], axis.get("line", "")))
        if cam.get("crosses_axis") and not cam.get("cross_reason"):
            add("error", card, "AXIS", "crosses_axis is set without a cross_reason")
        if card.get("time_of_day") and card["time_of_day"] != sc["time_of_day"]:
            add("error", card, "TIME", "time of day %s, scene %s is %s" % (card["time_of_day"], sc["id"], sc["time_of_day"]))
        sun = card.get("light", {}).get("sun")
        if sun and sc.get("sun") and sun != sc["sun"]:
            add("error", card, "SUN", "sun '%s' differs from the scene's '%s'" % (sun, sc["sun"]))
        if cam.get("angle") == "dutch" and not p.style.get("allow_dutch"):
            add("warning", card, "STYLE", "dutch angle but the style bible does not allow it")
        positions = axis.get("positions", {})
        travel = axis.get("travel", {})
        allowed_props = set(sc.get("props", [])) | set(p.locs.get(sc.get("location"), {}).get("props", []))
        on_screen = []
        for m in card.get("cast", []):
            ch = p.chars.get(m.get("id"))
            if not ch:
                add("error", card, "CAST", "'%s' is not in characters.json" % m.get("id"))
                continue
            allowed_props |= set(ch.get("props", []))
            if m.get("identity") != ch["identity"]:
                add("error", card, "IDENTITY", "%s identity is not the bible's string verbatim; copy it exactly" % ch["name"])
            want = wardrobe_for(ch, sc["id"])
            if "wardrobe" in m and m["wardrobe"] != want:
                add("error", card, "WARDROBE", "%s wears '%s', the bible says '%s' in scene %s" % (ch["name"], m["wardrobe"], want, sc["id"]))
            t = m.get("travel")
            if t in FLIP and travel.get(m["id"]) in FLIP:
                exp = FLIP[travel[m["id"]]] if flipped else travel[m["id"]]
                if t != exp:
                    add("error", card, "DIRECTION", "%s travels %s, screen direction for this scene from side %s is %s" % (ch["name"], t, side, exp))
            tgt, eye = m.get("looks_at"), m.get("eyeline")
            if eye in FLIP and tgt in positions and m["id"] in positions and positions[tgt] != positions[m["id"]]:
                exp = "frame-right" if POS_INDEX[positions[m["id"]]] < POS_INDEX[positions[tgt]] else "frame-left"
                exp = FLIP[exp] if flipped else exp
                if eye != exp:
                    tname = p.chars.get(tgt, {}).get("name", tgt)
                    add("error", card, "EYELINE", "%s looks %s at %s; from side %s the eyeline must be %s" % (ch["name"], eye, tname, side, exp))
            if eye == "camera" and cam.get("framing") != "pov":
                add("warning", card, "EYELINE", "%s looks into the lens outside a POV shot" % ch["name"])
            if m.get("position") in POS_INDEX and m["id"] in positions:
                on_screen.append(m)
            for key in ("holding", "holding_end"):
                if m.get(key) and m[key] not in allowed_props:
                    add("warning", card, "PROP", "%s holds '%s', which no bible lists" % (ch["name"], m[key]))
        for i, a in enumerate(on_screen):
            for b in on_screen[i + 1:]:
                want = POS_INDEX[positions[a["id"]]] - POS_INDEX[positions[b["id"]]]
                got = POS_INDEX[a["position"]] - POS_INDEX[b["position"]]
                if flipped:
                    want = -want
                if want and got and (want > 0) != (got > 0):
                    add("error", card, "POSITION", "%s and %s have swapped sides of the frame" % (a["id"], b["id"]))
        action = card.get("action", "")
        if len(re.findall(r"[.!?](\s|$)", action.strip())) > 1 or re.search(r"\b(then|and then|after that)\b", action):
            add("warning", card, "ONE-ACTION", "the action reads as more than one action; split the card")
        prev = prev_by_scene.get(sc["id"])
        if prev:
            pcast = {m["id"]: m for m in prev.get("cast", [])}
            for m in card.get("cast", []):
                pm = pcast.get(m.get("id"))
                if pm and "holding" in m and ("holding" in pm or "holding_end" in pm):
                    before = pm.get("holding_end", pm.get("holding"))
                    if before != m["holding"]:
                        add("error", card, "PROP", "%s ends %s holding %s but starts %s holding %s" % (
                            m["id"], prev["id"], before or "nothing", card["id"], m["holding"] or "nothing"))
            same = sorted(m.get("id") for m in card.get("cast", [])) == sorted(pcast) and (
                card.get("cast") or card.get("subject") == prev.get("subject"))
            pc = prev.get("camera", {})
            if same and cam.get("size") in SIZES and pc.get("size") in SIZES:
                step = abs(SIZES.index(cam["size"]) - SIZES.index(pc["size"]))
                az, paz = cam.get("azimuth_deg"), pc.get("azimuth_deg")
                if step < 2:
                    if az is None or paz is None:
                        add("warning", card, "30-DEGREE", "same subject as %s with %d size step(s); add azimuth_deg to both to check the 30-degree rule" % (prev["id"], step))
                    elif abs(az - paz) < 30:
                        add("error", card, "30-DEGREE", "jump cut from %s: same subject, %d size step(s) and %d degrees; change size by 2+ steps or angle by 30+ degrees" % (
                            prev["id"], step, abs(az - paz)))
        prev_by_scene[sc["id"]] = card
    return issues


def cmd_continuity(ctx, a):
    p = Project(a.project, a.with_card)
    issues = continuity_diff(p)
    errors = [i for i in issues if i["level"] == "error"]
    if a.json:
        print(json.dumps({"cards": len(p.cards), "issues": issues}, indent=2))
    else:
        for i in issues:
            print("%s %s %s: %s" % (i["level"].upper(), i["card"], i["code"], i["message"]))
        print("continuity diff: %d cards, %d errors, %d warnings" % (len(p.cards), len(errors), len(issues) - len(errors)))
    return 1 if errors else 0


# ---------- compile ----------

def find_model_card(ctx, model):
    for d in ctx.model_dirs:
        for p, meta, body in entries(d):
            if meta.get("model") == model:
                return p, meta, compile_block(body)
    return None, None, None


def _sentence(s):
    s = s.strip()
    return s if not s or s[-1] in ".!?\"" else s + "."


def _cap(s):
    return s[:1].upper() + s[1:]


def card_parts(p, card, prof):
    sc = p.scene_map[card["scene"]]
    loc = p.locs[sc["location"]]
    cam = card["camera"]
    flipped = cam.get("side") == "B"
    parts = {}
    lens = ", %smm lens" % int(cam["lens_mm"]) if cam.get("lens_mm") else ""
    parts["camera"] = _sentence("%s, %s%s, %s" % (_cap(SIZE_WORDS[cam["size"]]), ANGLE_WORDS[cam["angle"]], lens, MOVE_WORDS[cam["move"]]))
    subj = []
    for m in card.get("cast", []):
        ch = p.chars[m["id"]]
        line = "%s, %s, wearing %s" % (ch["name"], ch["identity"].rstrip("."), wardrobe_for(ch, sc["id"]).rstrip("."))
        if m.get("position"):
            line += ", %s" % POSITION_WORDS[m["position"]]
        if m.get("holding"):
            line += ", holding the %s" % m["holding"]
        subj.append(_sentence(line))
    if card.get("subject"):
        subj.append(_sentence(_cap(card["subject"])))
    parts["subject"] = " ".join(subj)
    act = [_sentence(card["action"])]
    for m in card.get("cast", []):
        name = p.chars[m["id"]]["name"]
        t = m.get("travel") or sc.get("axis", {}).get("travel", {}).get(m["id"])
        if t in TRAVEL_WORDS:
            t = t if m.get("travel") or not flipped else FLIP.get(t, t)
            act.append(_sentence("%s is %s" % (name, TRAVEL_WORDS[t])))
        if m.get("eyeline") in EYELINE_WORDS:
            act.append(_sentence("%s is %s" % (name, EYELINE_WORDS[m["eyeline"]])))
    parts["action"] = " ".join(act)
    tod = card.get("time_of_day", sc["time_of_day"]).replace("-", " ")
    parts["context"] = _sentence(_cap("%s, %s" % (loc["description"].rstrip("."), tod)))
    light = card.get("light", {})
    lt = []
    if sc.get("sun"):
        lt.append(sc["sun"])
    if light.get("key_side"):
        lt.append("%s key light from %s" % (light.get("quality", "soft"), light["key_side"].replace("-", " ")))
    if light.get("motivation"):
        lt.append(light["motivation"])
    parts["light"] = _sentence(_cap(", ".join(lt))) if lt else ""
    # --sequence: the scene's sun goes in the shared header, each shot keeps its own key side
    parts["sun"] = _sentence(_cap(sc["sun"])) if sc.get("sun") else ""
    parts["key"] = _sentence(_cap(", ".join(lt[1:] if sc.get("sun") else lt))) if lt[1 if sc.get("sun") else 0:] else ""
    parts["style"] = _sentence(p.style["look"])
    audio = []
    for d in card.get("dialogue", []):
        tone = d.get("tone")
        audio.append(prof["dialogue"].format(name=p.chars[d["character"]]["name"], tone_clause=(" " + tone) if tone else "", line=d["line"]))
    if card.get("sound"):
        audio.append(prof["audio"].format(sound=card["sound"].rstrip(".")))
    parts["audio"] = " ".join(_sentence(x) for x in audio)
    return parts


def snap_duration(seconds, allowed):
    up = [d for d in sorted(allowed) if d >= seconds]
    return up[0] if up else max(allowed)


def compile_cards(p, cards, prof, sequence=False):
    """Return a list of (label, prompt, params, warnings)."""
    out = []
    st = p.style
    problems = []
    if st["aspect_ratio"] not in prof["aspect_ratios"]:
        problems.append("aspect %s not offered (%s)" % (st["aspect_ratio"], ", ".join(prof["aspect_ratios"])))
    if st["resolution"] not in prof["resolutions"]:
        problems.append("resolution %s not offered (%s)" % (st["resolution"], ", ".join(prof["resolutions"])))
    if problems:
        raise SystemExit("style bible does not fit %s: %s" % (prof["model_id"], "; ".join(problems)))
    groups = [[c] for c in cards]
    if sequence:
        groups, cur = [], []
        limit = max(prof["durations_s"])
        for c in cards:
            if cur and (c["scene"] != cur[-1]["scene"] or sum(x["duration_s"] for x in cur) + c["duration_s"] > limit):
                groups.append(cur)
                cur = []
            cur.append(c)
        if cur:
            groups.append(cur)
    for g in groups:
        warnings = []
        refs = []
        for c in g:
            refs += [r for r in c.get("refs", []) if r not in refs]
        if len(g) == 1:
            parts = card_parts(p, g[0], prof)
            text = " ".join(parts[k] for k in prof["order"] if parts.get(k))
            total = g[0]["duration_s"]
        elif "timestamp" not in prof:
            raise SystemExit("%s has no timestamp syntax; compile without --sequence" % prof["model_id"])
        else:
            first = card_parts(p, g[0], prof)
            people = []
            for c in g:
                for m in c.get("cast", []):
                    ch = p.chars[m["id"]]
                    line = _sentence("%s, %s, wearing %s" % (ch["name"], ch["identity"].rstrip("."), wardrobe_for(ch, c["scene"]).rstrip(".")))
                    if line not in people:
                        people.append(line)
            head = " ".join(people + [first[k] for k in ("context", "sun", "style") if first.get(k)])
            blocks, t = [], 0.0
            for c in g:
                parts = card_parts(p, c, prof)
                start, end = t, t + c["duration_s"]
                stamp = prof["timestamp"].format(start="%02d:%02d" % divmod(int(start), 60), end="%02d:%02d" % divmod(int(end), 60))
                body = " ".join(parts[k] for k in ("camera", "action", "key", "audio") if parts.get(k))
                blocks.append("%s %s" % (stamp, body))
                t = end
            text = head + "\n" + "\n".join(blocks)
            total = t
        dur = snap_duration(total, prof["durations_s"])
        forced = prof.get("resolution_duration_s", {}).get(st["resolution"])
        if refs and prof.get("reference_duration_s"):
            forced = prof["reference_duration_s"]
        if forced:
            dur = forced
        if refs and len(refs) > prof.get("max_reference_images", 0):
            warnings.append("%d reference images, %s takes %d" % (len(refs), prof["model_id"], prof.get("max_reference_images", 0)))
        if dur != total:
            warnings.append("planned %ss, rendered at %ss: trim in the edit" % (total, dur))
        words = len(text.split())
        if words > prof["max_words"]:
            warnings.append("%d words, over the %d-word guide: shorten action or context, never the identity string" % (words, prof["max_words"]))
        for c in g:
            for m in c.get("cast", []):
                if p.chars[m["id"]]["identity"] not in text:
                    raise SystemExit("compiler bug: identity of %s not verbatim in %s" % (m["id"], c["id"]))
        params = {"model": prof["model_id"], "durationSeconds": dur, "aspectRatio": st["aspect_ratio"],
                  "resolution": st["resolution"]}
        seeds = [c["seed"] for c in g if "seed" in c]
        if seeds and prof.get("seed"):
            params["seed"] = seeds[0]
        if refs:
            params["referenceImages"] = refs
        if prof.get("negative_prompt") == "field" and prof.get("negative_terms"):
            params["negativePrompt"] = prof["negative_terms"]
        label = "+".join(c["id"] for c in g)
        out.append((label, text, params, warnings))
    return out


def cmd_compile(ctx, a):
    p = Project(a.project)
    path, meta, prof = find_model_card(ctx, a.model)
    if not prof:
        print("no model card for '%s'. Install cinewright-genvideo, or check `kb search %s`." % (a.model, a.model), file=sys.stderr)
        return 1
    if meta.get("status") in ("deprecated", "shut-down"):
        print("warning: %s is %s" % (meta.get("title"), meta.get("status")), file=sys.stderr)
    cards = [c for c in p.cards if not a.card or c["id"] in a.card]
    if not cards:
        print("no matching cards", file=sys.stderr)
        return 1
    results = compile_cards(p, cards, prof, a.sequence)
    for label, text, params, warnings in results:
        if a.out:
            out = Path(a.out)
            write_text(out / ("%s.txt" % label), text + "\n")
            write_text(out / ("%s.params.json" % label), json.dumps(params, indent=2) + "\n")
        print("== %s  %s  %ss %s %s  %d words" % (label, params["model"], params["durationSeconds"], params["aspectRatio"], params["resolution"], len(text.split())))
        if not a.out:
            print(text)
            print("params: %s" % json.dumps(params))
        for w in warnings:
            print("  warning: %s" % w)
    if a.out:
        print("wrote %d prompts to %s (model card %s, last_checked %s)" % (len(results), a.out, path.name, meta.get("last_checked")))
    return 0


# ---------- argument parsing ----------

def build_parser(prog="cine.py"):
    ap = argparse.ArgumentParser(prog=prog, description="cinewright: plan, check and compile shots.")
    g = ap.add_subparsers(dest="group", required=True)

    kb = g.add_parser("kb", help="knowledge base").add_subparsers(dest="cmd", required=True)
    kb.add_parser("index", help="rewrite references/INDEX.md")
    s = kb.add_parser("search", help="find entries by words")
    s.add_argument("words", nargs="+")
    s.add_argument("--limit", type=int, default=8)
    s = kb.add_parser("show", help="print one entry or one section")
    s.add_argument("slug")
    s.add_argument("--section")

    cards = g.add_parser("cards", help="shot cards").add_subparsers(dest="cmd", required=True)
    s = cards.add_parser("new", help="write a skeleton card filled from the bibles")
    s.add_argument("project")
    s.add_argument("--id", required=True)
    s.add_argument("--scene", required=True)
    s.add_argument("--cast", help="comma-separated character ids")
    s.add_argument("--order", type=int)
    s = cards.add_parser("validate", help="check bibles and cards against the schemas")
    s.add_argument("project")
    s = cards.add_parser("export", help="export the shot list")
    s.add_argument("project")
    s.add_argument("--film-json", action="store_true", help="film.json shape for a local long-render pipeline")
    s.add_argument("--xfade", type=float, default=0.16, help="seam_audio_xfade seconds")
    s.add_argument("--out")

    s = g.add_parser("compile", help="card plus bibles to one model's prompt")
    s.add_argument("project")
    s.add_argument("--model", required=True)
    s.add_argument("--card", action="append", help="card id; repeat; default all")
    s.add_argument("--sequence", action="store_true", help="join consecutive cards of a scene into one timestamped generation")
    s.add_argument("--out")

    c = g.add_parser("continuity", help="script supervisor checks").add_subparsers(dest="cmd", required=True)
    s = c.add_parser("diff", help="check every card against the bibles and the previous card")
    s.add_argument("project")
    s.add_argument("--json", action="store_true")
    s.add_argument("--with", dest="with_card", action="append", metavar="FILE", help="check this card in place of the project card with the same id")
    return ap


HANDLERS = {"kb": cmd_kb, "cards": cmd_cards, "compile": cmd_compile, "continuity": cmd_continuity}


def main(argv=None, ctx=None):
    a = build_parser().parse_args(argv)
    return HANDLERS[a.group](ctx or default_context(), a)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
