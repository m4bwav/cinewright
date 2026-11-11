#!/usr/bin/env python3
"""cinewright film analysis: take an existing video apart into film notation and rebuild from it. Run it; do not read it.

  python scripts/cine_analyze.py probe VIDEO [--json]
  python scripts/cine_analyze.py shots VIDEO [--threshold 0.3] [--min-len 0.5] [--out NOTATION.json]
  python scripts/cine_analyze.py frame VIDEO --at SECONDS [--grid 50] --out FRAME.png
  python scripts/cine_analyze.py pan VIDEO --start S --end S [--fps 6]         (needs numpy)
  python scripts/cine_analyze.py scale MEASURE.json [--json]
  python scripts/cine_analyze.py notate NOTATION.json [--out NOTATION.md]
  python scripts/cine_analyze.py rebuild NOTATION.json (--cards DIR | --level OUT.md [--char-height 2.0])

Lengths are in H: one standing character, head to feet. scale turns pixel points read off a gridded frame
into set sizes in H (wall width and height, camera height, floor depth when a horizon is known).
Python 3.9+, standard library plus ffmpeg; numpy only for pan; Pillow only for labelled grids.
"""
import argparse
import importlib.util
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("cine_runtime", HERE / "cine.py")
cine = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cine)

SCHEMA = HERE / "schemas" / "film-notation.schema.json"
if not SCHEMA.is_file():  # repo layout: shared/lib next to shared/schemas
    SCHEMA = HERE.parent / "schemas" / "film-notation.schema.json"
DEFAULT_HFOV = 45.0


def _tool(name):
    p = shutil.which(name)
    if not p:
        raise SystemExit("%s not found on PATH; install ffmpeg" % name)
    return p


def probe(video):
    out = subprocess.run([_tool("ffprobe"), "-v", "error", "-show_entries",
                          "stream=codec_type,width,height,r_frame_rate:format=duration:format_tags",
                          "-of", "json", str(video)], capture_output=True, text=True)
    if out.returncode:
        raise SystemExit("ffprobe failed: %s" % out.stderr.strip())
    d = json.loads(out.stdout)
    info = {"file": Path(video).name, "duration_s": round(float(d.get("format", {}).get("duration", 0)), 3)}
    for s in d.get("streams", []):
        if s.get("codec_type") == "video" and "width" in s:
            info["width"], info["height"] = s["width"], s["height"]
            num, _, den = s.get("r_frame_rate", "0/1").partition("/")
            if float(den or 1):
                info["fps"] = round(float(num) / float(den or 1), 3)
            break
    tags = d.get("format", {}).get("tags") or {}
    if tags:
        info["tags"] = tags
    return info


def scene_cuts(video, threshold):
    out = subprocess.run([_tool("ffmpeg"), "-hide_banner", "-nostats", "-i", str(video), "-an", "-vf",
                          "select='gt(scene,%s)',showinfo" % threshold, "-f", "null", "-"],
                         capture_output=True, text=True)
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", out.stderr)]


def split_shots(cuts, duration, min_len):
    bounds, last = [0.0], 0.0
    for c in sorted(cuts):
        if c - last >= min_len and duration - c >= min_len:
            bounds.append(c)
            last = c
    bounds.append(duration)
    return [(round(a, 3), round(b, 3)) for a, b in zip(bounds, bounds[1:])]


def skeleton(info, spans, url=None):
    src = {k: info[k] for k in ("file", "duration_s", "fps", "width", "height") if k in info}
    if url:
        src["url"] = url
    return {"notation": "0.1", "source": src, "unit": "H", "characters": [], "props": [], "sets": [],
            "scenes": [], "shots": [{"id": "S%03d" % (i + 1), "start": a, "end": b} for i, (a, b) in enumerate(spans)]}


def frame(video, at, out, grid):
    out = Path(out)
    subprocess.run([_tool("ffmpeg"), "-v", "error", "-y", "-ss", str(at), "-i", str(video), "-frames:v", "1",
                    str(out)], check=True)
    if not grid:
        return "plain"
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        tmp = out.with_suffix(".grid" + out.suffix)
        subprocess.run([_tool("ffmpeg"), "-v", "error", "-y", "-i", str(out), "-vf",
                        "drawgrid=w=%d:h=%d:t=1:c=yellow@0.5" % (grid, grid), str(tmp)], check=True)
        tmp.replace(out)
        return "grid, no labels (install Pillow for labels)"
    im = Image.open(out).convert("RGB")
    dr = ImageDraw.Draw(im)
    w, h = im.size
    for x in range(0, w, grid):
        major = x % (grid * 2) == 0
        dr.line([(x, 0), (x, h)], fill=(255, 255, 0) if major else (0, 255, 255), width=1)
        if major:
            dr.text((x + 2, 2), str(x), fill=(255, 255, 0))
    for y in range(0, h, grid):
        major = y % (grid * 2) == 0
        dr.line([(0, y), (w, y)], fill=(255, 255, 0) if major else (0, 255, 255), width=1)
        if major:
            dr.text((2, y + 2), str(y), fill=(255, 255, 0))
    im.save(out)
    return "grid with labels"


def pan(video, start, end, fps, width=320):
    try:
        import numpy as np
    except ImportError:
        raise SystemExit("pan needs numpy (pip install numpy)")
    info = probe(video)
    h = int(round(info["height"] * width / info["width"] / 2)) * 2
    raw = subprocess.run([_tool("ffmpeg"), "-v", "error", "-ss", str(start), "-to", str(end), "-i", str(video),
                          "-vf", "fps=%s,scale=%d:%d,format=gray" % (fps, width, h), "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    n = len(raw) // (width * h)
    frames = np.frombuffer(raw[:n * width * h], dtype=np.uint8).reshape(n, h, width).astype(np.float64)
    win = np.outer(np.hanning(h), np.hanning(width))
    dx_total = dy_total = 0.0
    steps = []
    for a, b in zip(frames, frames[1:]):
        dx, dy = phase_shift(np, a * win, b * win)
        dx_total += dx
        dy_total += dy
        steps.append(round(dx, 2))
    k = info["width"] / width
    return {"frames": n, "pan_px": round(dx_total * k, 1), "tilt_px": round(dy_total * k, 1),
            "steps_px": [round(s * k, 1) for s in steps],
            "move": "static" if abs(dx_total * k) < 0.02 * info["width"] else
            ("pan-right" if dx_total > 0 else "pan-left")}


def phase_shift(np, a, b):
    """Translation of b relative to a, in pixels: positive x means the scene moved left (camera panned right)."""
    fa, fb = np.fft.fft2(a), np.fft.fft2(b)
    r = fa * np.conj(fb)
    r /= np.abs(r) + 1e-9
    c = np.fft.ifft2(r).real
    y, x = np.unravel_index(np.argmax(c), c.shape)
    h, w = c.shape
    return (x - w if x > w // 2 else x), (y - h if y > h // 2 else y)


def scale(m):
    """Sizes in H from a measure file. See the measure-file fields in the skill's film-notation entry."""
    chars = m.get("characters") or []
    if not chars:
        raise SystemExit("measure file needs at least one standing character (head_y, feet_y)")
    wall = m.get("wall") or {}
    floor_y = wall.get("floor_y")
    notes, conf = [], "measured"
    hy = m.get("horizon_y")
    pts = sorted(((c["feet_y"], c["feet_y"] - c["head_y"]) for c in chars), key=lambda t: t[0])
    if hy is None and len(pts) >= 2 and pts[-1][0] - pts[0][0] > 20:
        # H_px = k (feet_y - horizon): straight line through the characters
        n = len(pts)
        mx = sum(p[0] for p in pts) / n
        my = sum(p[1] for p in pts) / n
        sxx = sum((p[0] - mx) ** 2 for p in pts)
        k = sum((p[0] - mx) * (p[1] - my) for p in pts) / sxx
        if k > 0:
            hy = mx - my / k
            notes.append("horizon %.0f px from %d characters at different depths" % (hy, n))
    if hy is not None:
        k = sum(p[1] / (p[0] - hy) for p in pts) / len(pts)
        px_wall = k * (floor_y - hy) if floor_y is not None else pts[0][1]
    else:
        px_wall = sum(p[1] for p in pts) / len(pts)
        if floor_y is not None:
            gap = max(abs(p[0] - floor_y) for p in pts)
            if gap > 0.1 * px_wall:
                conf = "estimated"
                notes.append("characters stand %.0f px in front of the wall line and no horizon is known: wall "
                             "sizes are scaled by their height, so read them as an upper bound" % gap)
        k = None
    out = {"px_per_H_at_wall": round(px_wall, 1), "confidence": conf}
    if "left_x" in wall and "right_x" in wall:
        out["width_H"] = round((wall["right_x"] - wall["left_x"] + m.get("pan_px", 0)) / px_wall, 2)
        if m.get("pan_px"):
            notes.append("width includes %s px of camera pan" % m["pan_px"])
        if wall.get("left_open") or wall.get("right_open"):
            notes.append("a corner is off frame: width is a lower bound")
            out["confidence"] = "estimated"
    if floor_y is not None and "ceiling_y" in wall:
        out["height_H"] = round((floor_y - wall["ceiling_y"]) / px_wall, 2)
    if hy is not None and floor_y is not None:
        out["camera_height_H"] = round((floor_y - hy) / px_wall, 2)
        fy = m.get("floor_front_y")
        if fy is not None and fy > hy:
            hfov = m.get("hfov_deg", DEFAULT_HFOV)
            f = m["width"] / 2 / math.tan(math.radians(hfov / 2))
            d_wall = f / (k * (floor_y - hy))
            d_front = f / (k * (fy - hy))
            out["depth_H"] = round(d_wall - d_front, 2)
            out["camera_to_wall_H"] = round(d_wall, 2)
            notes.append("depth assumes a %.0f degree horizontal field of view%s" %
                         (hfov, "" if "hfov_deg" in m else " (default; set hfov_deg if known)"))
    else:
        notes.append("no depth: give horizon_y or two characters at clearly different depths")
    out["notes"] = notes
    return out


def check_notation(doc):
    schema = json.loads(cine.read_text(SCHEMA))
    schema.pop("$comment", None)
    return cine.validate(doc, schema)


def tc(s):
    return "%d:%04.1f" % (int(s // 60), s % 60)


def notate(doc):
    src = doc["source"]
    lines = ["# Film notation: %s" % (src.get("title") or src.get("file") or src.get("url") or "video"), "",
             "Source: %s, %s, %s s. Unit: H (one standing character)." %
             (src.get("url") or src.get("file", "?"), src.get("medium", "medium unknown"), src["duration_s"]), ""]
    if doc.get("sets"):
        lines += ["## Sets", "", "| Set | Width H | Height H | Depth H | Confidence | Camera |", "|---|---|---|---|---|---|"]
        for s in doc["sets"]:
            cam = s.get("camera", {})
            lines.append("| %s | %s | %s | %s | %s | %s |" % (
                s.get("name") or s["id"], s.get("width_H", "?"), s.get("height_H", "?"), s.get("depth_H", "?"),
                s.get("confidence", "?"), ", ".join("%s %s" % (k, v) for k, v in cam.items()) or "-"))
        for s in doc["sets"]:
            if s.get("features"):
                lines += ["", "### %s features" % (s.get("name") or s["id"]), ""]
                for f in s["features"]:
                    lines.append("- %s on %s wall at x %s, y %s, %s x %s H%s" % (
                        f["kind"], f["wall"], f.get("x_H", "?"), f.get("y_H", "?"), f.get("w_H", "?"),
                        f.get("h_H", "?"), (": " + f["note"]) if f.get("note") else ""))
        lines.append("")
    if doc.get("characters"):
        lines += ["## Characters", ""] + ["- **%s**: %s%s" % (c["id"], c.get("look", ""),
                                                               ("; " + c["wardrobe"]) if c.get("wardrobe") else "")
                                         for c in doc["characters"]] + [""]
    lines += ["## Shots", "", "| Shot | In | Out | Len | Size | Angle | Move | Action | Audio |",
              "|---|---|---|---|---|---|---|---|---|"]
    for s in doc["shots"]:
        audio = "; ".join(x for x in (s.get("dialogue"), s.get("music"), s.get("sfx")) if x)
        lines.append("| %s | %s | %s | %.1f | %s | %s | %s | %s | %s |" % (
            s["id"], tc(s["start"]), tc(s["end"]), s["end"] - s["start"], s.get("size", ""), s.get("angle", ""),
            s.get("move", ""), (s.get("action") or "").replace("|", "/"), audio.replace("|", "/")))
    return "\n".join(lines) + "\n"


def rebuild_cards(doc, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    looks = {c["id"]: c for c in doc.get("characters", [])}
    scene_no = {sc["id"]: i + 1 for i, sc in enumerate(doc.get("scenes", []))}
    letters, written, skipped = {}, [], []
    for s in doc["shots"]:
        if not s.get("action") or len(s["action"]) < 5:
            skipped.append(s["id"])
            continue
        n = scene_no.get(s.get("scene"), 1)
        letters[n] = letters.get(n, 0) + 1
        idx = letters[n] - 1
        slate = "%d%s" % (n, (chr(65 + idx) if idx < 26 else chr(64 + idx // 26) + chr(65 + idx % 26)))
        cast = []
        for c in s.get("cast", []):
            item = {"id": c["id"], "identity": looks.get(c["id"], {}).get("look") or c["id"]}
            if looks.get(c["id"], {}).get("wardrobe"):
                item["wardrobe"] = looks[c["id"]]["wardrobe"]
            if c.get("holding"):
                item["holding"] = c["holding"]
            cast.append(item)
        card = {"id": slate, "scene": str(n), "order": len(written) + 1,
                "duration_s": max(3, min(8, round(s["end"] - s["start"], 1))),
                "camera": {"size": s.get("size", "WS"), "angle": s.get("angle", "eye-level"),
                           "move": s.get("move", "static") if s.get("move") in MOVES else "static", "side": "A"},
                "cast": cast, "action": s["action"][:240], "notes": "rebuilt from film notation shot %s (%s-%s)" % (
                    s["id"], tc(s["start"]), tc(s["end"]))}
        for k in ("sfx",):
            if s.get(k):
                card["sound"] = s[k]
        (out_dir / ("%s.json" % slate)).write_bytes((json.dumps(card, indent=2) + "\n").encode("utf-8"))
        written.append(slate)
    return written, skipped


MOVES = {"static", "pan-left", "pan-right", "tilt-up", "tilt-down", "dolly-in", "dolly-out", "truck-left",
         "truck-right", "track", "crane-up", "crane-down", "handheld", "zoom-in", "zoom-out", "push-in",
         "arc-left", "arc-right", "dolly-zoom"}


def rebuild_level(doc, char_height):
    u = char_height
    lines = ["# Level brief from film notation", "",
             "Sizes in H (one standing character) and in engine units at %s units per character." % u, ""]
    for s in doc.get("sets", []):
        lines += ["## %s" % (s.get("name") or s["id"]), ""]
        for key, label in (("width_H", "Back wall width"), ("height_H", "Wall height"), ("depth_H", "Floor depth")):
            if key in s:
                lines.append("- %s: %.2f H = %.2f units" % (label, s[key], s[key] * u))
        lines.append("- Confidence: %s" % s.get("confidence", "guess"))
        cam = s.get("camera") or {}
        if cam:
            lines.append("- Film camera: %s" % ", ".join("%s %s" % kv for kv in cam.items()))
            if cam.get("view") == "side-on":
                lines.append("  The film shows this room side-on: keep the floor shallow and the back wall wide; "
                             "a game camera that looks down from high will make the room read deeper than the film.")
        for f in s.get("features", []):
            lines.append("- %s, %s wall: x %s, y %s, size %s x %s H%s" % (
                f["kind"], f["wall"], _u(f.get("x_H"), u), _u(f.get("y_H"), u), _u(f.get("w_H"), u),
                _u(f.get("h_H"), u), (" (" + f["note"] + ")") if f.get("note") else ""))
        if s.get("measured_from"):
            lines.append("- Measured from: %s" % ", ".join(s["measured_from"]))
        lines.append("")
    lines += ["## Check", "", "Render the built room with a character of %s units standing at the back wall and put "
              "it beside the film frame the size came from; wall width and height in characters must match." % u]
    return "\n".join(lines) + "\n"


def _u(v, u):
    return "?" if v is None else "%s H (%.2f)" % (v, v * u)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="cine_analyze.py", description=__doc__.splitlines()[0])
    g = ap.add_subparsers(dest="cmd", required=True)
    p = g.add_parser("probe"); p.add_argument("video"); p.add_argument("--json", action="store_true")
    p = g.add_parser("shots"); p.add_argument("video"); p.add_argument("--threshold", type=float, default=0.3)
    p.add_argument("--min-len", type=float, default=0.5); p.add_argument("--url"); p.add_argument("--out")
    p = g.add_parser("frame"); p.add_argument("video"); p.add_argument("--at", type=float, required=True)
    p.add_argument("--grid", type=int, default=50); p.add_argument("--out", required=True)
    p = g.add_parser("pan"); p.add_argument("video"); p.add_argument("--start", type=float, required=True)
    p.add_argument("--end", type=float, required=True); p.add_argument("--fps", type=float, default=6)
    p = g.add_parser("scale"); p.add_argument("measure"); p.add_argument("--json", action="store_true")
    p = g.add_parser("notate"); p.add_argument("notation"); p.add_argument("--out")
    p = g.add_parser("rebuild"); p.add_argument("notation"); p.add_argument("--cards"); p.add_argument("--level")
    p.add_argument("--char-height", type=float, default=2.0)
    a = ap.parse_args(argv)

    if a.cmd == "probe":
        info = probe(a.video)
        print(json.dumps(info, indent=2) if a.json else "\n".join("%s: %s" % kv for kv in info.items()))
    elif a.cmd == "shots":
        info = probe(a.video)
        spans = split_shots(scene_cuts(a.video, a.threshold), info["duration_s"], a.min_len)
        doc = skeleton(info, spans, a.url)
        if a.out:
            Path(a.out).write_bytes((json.dumps(doc, indent=2) + "\n").encode("utf-8"))
        for s in doc["shots"]:
            print("%s %s-%s %.1f s" % (s["id"], tc(s["start"]), tc(s["end"]), s["end"] - s["start"]))
        print("shots: %d in %.1f s (threshold %s)%s" % (len(spans), info["duration_s"], a.threshold,
                                                       (", notation " + a.out) if a.out else ""))
    elif a.cmd == "frame":
        print("frame %s at %s s: %s" % (a.out, a.at, frame(a.video, a.at, a.out, a.grid)))
    elif a.cmd == "pan":
        print(json.dumps(pan(a.video, a.start, a.end, a.fps), indent=2))
    elif a.cmd == "scale":
        r = scale(json.loads(cine.read_text(Path(a.measure))))
        if a.json:
            print(json.dumps(r, indent=2))
        else:
            for k, v in r.items():
                if k != "notes":
                    print("%s: %s" % (k, v))
            for n in r["notes"]:
                print("note: " + n)
    elif a.cmd == "notate":
        doc = json.loads(cine.read_text(Path(a.notation)))
        errs = check_notation(doc)
        if errs:
            print("\n".join(errs))
            return 1
        md = notate(doc)
        if a.out:
            Path(a.out).write_bytes((md).encode("utf-8"))
            print("notation ok: %d shots, %d sets -> %s" % (len(doc["shots"]), len(doc.get("sets", [])), a.out))
        else:
            sys.stdout.write(md)
    elif a.cmd == "rebuild":
        doc = json.loads(cine.read_text(Path(a.notation)))
        errs = check_notation(doc)
        if errs:
            print("\n".join(errs))
            return 1
        if not (a.cards or a.level):
            raise SystemExit("rebuild needs --cards DIR or --level OUT.md")
        if a.cards:
            w, s = rebuild_cards(doc, a.cards)
            print("cards: %d written to %s%s" % (len(w), a.cards, (", skipped (no action): " + ", ".join(s)) if s else ""))
        if a.level:
            Path(a.level).write_bytes((rebuild_level(doc, a.char_height)).encode("utf-8"))
            print("level brief: %s (%d sets, %s units per H)" % (a.level, len(doc.get("sets", [])), a.char_height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
