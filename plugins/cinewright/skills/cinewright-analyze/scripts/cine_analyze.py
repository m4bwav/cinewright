#!/usr/bin/env python3
"""cinewright film analysis: take an existing video apart into film notation and rebuild from it. Run it; do not read it.

  python scripts/cine_analyze.py probe VIDEO [--json]
  python scripts/cine_analyze.py shots VIDEO [--threshold 0.3] [--min-len 0.5] [--out NOTATION.json]
  python scripts/cine_analyze.py frame VIDEO --at SECONDS [--grid 50] --out FRAME.png
  python scripts/cine_analyze.py pan VIDEO --start S --end S [--fps 6] [--method auto|orb|phase]   (numpy; orb needs opencv-python)
  python scripts/cine_analyze.py scale MEASURE.json [--json]
  python scripts/cine_analyze.py notate NOTATION.json [--out NOTATION.md]
  python scripts/cine_analyze.py rebuild NOTATION.json (--cards DIR | --level OUT.md [--char-height 2.0])
  python scripts/cine_analyze.py aidetect VIDEO [--frames 32] [--out DIR] [--json]   (needs opencv-python, numpy)

Lengths are in H: one standing character, head to feet. scale turns pixel points read off a gridded frame
into set sizes in H (wall width and height, camera height, floor depth when a horizon is known).
Python 3.9+, standard library plus ffmpeg; numpy only for pan; opencv-python and numpy for aidetect; Pillow only for labelled grids.
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


def pan(video, start, end, fps, width=320, method="auto"):
    """Camera pan in source pixels. orb (default when opencv is present) matches background landmarks with RANSAC,
    so moving characters on a flat cel background do not swamp it; phase is whole-frame phase correlation."""
    try:
        import numpy as np
    except ImportError:
        raise SystemExit("pan needs numpy (pip install numpy)")
    cv2 = None
    if method in ("auto", "orb"):
        try:
            import cv2
        except ImportError:
            if method == "orb":
                raise SystemExit("pan --method orb needs opencv-python")
    method = "orb" if cv2 is not None else "phase"
    if method == "orb":
        width = max(width, 640)
    info = probe(video)
    h = int(round(info["height"] * width / info["width"] / 2)) * 2
    raw = subprocess.run([_tool("ffmpeg"), "-v", "error", "-ss", str(start), "-to", str(end), "-i", str(video),
                          "-vf", "fps=%s,scale=%d:%d,format=gray" % (fps, width, h), "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    n = len(raw) // (width * h)
    frames = np.frombuffer(raw[:n * width * h], dtype=np.uint8).reshape(n, h, width)
    win = np.outer(np.hanning(h), np.hanning(width))
    dx_total = dy_total = 0.0
    steps = []
    weak = 0
    for a, b in zip(frames, frames[1:]):
        if method == "orb":
            dx, dy, ok = orb_shift(cv2, np, a, b)
            weak += not ok
        else:
            dx, dy = phase_shift(np, a.astype(np.float64) * win, b.astype(np.float64) * win)
        dx_total += dx
        dy_total += dy
        steps.append(round(dx, 2))
    k = info["width"] / width
    return {"frames": n, "method": method, "weak_steps": weak,
            "pan_px": round(dx_total * k, 1), "tilt_px": round(dy_total * k, 1),
            "steps_px": [round(s * k, 1) for s in steps],
            "move": "static" if abs(dx_total * k) < 0.02 * info["width"] else
            ("pan-right" if dx_total > 0 else "pan-left")}


def orb_shift(cv2, np, a, b):
    """Shift of b against a from ORB matches and a RANSAC similarity fit, same sign as phase_shift.
    Returns (dx, dy, ok); ok is False when too few landmarks agree and the step counts as zero."""
    orb = cv2.ORB_create(1500)
    ka, da = orb.detectAndCompute(a, None)
    kb, db = orb.detectAndCompute(b, None)
    if da is None or db is None or len(ka) < 8 or len(kb) < 8:
        return 0.0, 0.0, False
    matches = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(da, db)
    if len(matches) < 8:
        return 0.0, 0.0, False
    pa = np.float32([ka[m.queryIdx].pt for m in matches])
    pb = np.float32([kb[m.trainIdx].pt for m in matches])
    M, inl = cv2.estimateAffinePartial2D(pa, pb, method=cv2.RANSAC, ransacReprojThreshold=2.0)
    if M is None or inl is None or int(inl.sum()) < 8:
        return 0.0, 0.0, False
    sel = inl.ravel().astype(bool)
    d = np.median(pb[sel] - pa[sel], axis=0)
    return -float(d[0]), -float(d[1]), True


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


# ---- aidetect: signs of AI generation (version 1; research in ai-docs/research/2026-11-11-ai-video-detection.md)

CAMERA_KEYS = ("com.android.model", "com.android.manufacturer", "com.apple.quicktime.make",
               "com.apple.quicktime.model", "make", "model", "location", "com.apple.quicktime.location.iso6709")
# (name, durations in seconds, frame rates) for format fingerprints; weak evidence only
GENERATOR_FORMATS = (("Veo 3", (4, 6, 8), (24,)), ("Wan 2.x", (5,), (16,)), ("Kling / Runway", (5, 10), (24, 30)),
                     ("MiniMax / Hailuo", (6, 10), (24, 25)), ("Sora", (5, 10, 15, 20), (30,)))
# raw value bands: lo maps to 0 (camera-like), hi to 1 (generator-like). Calibrated 2026-11-11 on 21 generated
# clips and 3 phone clips (ai-video-tells entry): only hf_ratio separated them. warp_residual, homography_inliers
# and jerk are reported raw but not scored until a larger phone set proves them.
BANDS = {"hf_ratio": (0.02, 0.008)}
WEIGHTS = {"provenance": 4.0, "camera_atoms": -1.5, "format": 0.5, "hf_ratio": 0.75}


def ffprobe_full(video):
    out = subprocess.run([_tool("ffprobe"), "-v", "error", "-show_format", "-show_streams", "-of", "json", str(video)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    if out.returncode:
        raise SystemExit("ffprobe failed: %s" % out.stderr.strip())
    return json.loads(out.stdout)


def metadata_signals(d):
    """Provenance, camera atoms and format fingerprint from ffprobe json."""
    fmt = d.get("format", {})
    tags = {k.lower(): v for k, v in (fmt.get("tags") or {}).items()}
    for s in d.get("streams", []):
        for k, v in (s.get("tags") or {}).items():
            tags.setdefault(k.lower(), v)
    vs = next((s for s in d.get("streams", []) if s.get("codec_type") == "video" and "width" in s), {})
    num, _, den = vs.get("r_frame_rate", "0/1").partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 0.0
    dur = float(fmt.get("duration") or 0)
    out = {"duration_s": round(dur, 3), "fps": round(fps, 3), "width": vs.get("width"), "height": vs.get("height"),
           "audio": any(s.get("codec_type") == "audio" for s in d.get("streams", [])),
           "encoder": tags.get("encoder", "")}
    br = float(fmt.get("bit_rate") or 0)
    if br and fps and vs.get("width"):
        out["bits_per_pixel"] = round(br / (vs["width"] * vs["height"] * fps), 4)
    gen = None
    for k in ("prompt", "workflow", "comment", "description", "software"):
        v = str(tags.get(k, ""))
        if "class_type" in v or '"nodes"' in v:
            models = sorted(set(re.findall(r'"(?:unet_name|ckpt_name|model_name)":\s*"([^"]+)"', v)))
            gen = "ComfyUI workflow in the %s tag%s" % (k, (" (" + ", ".join(models) + ")") if models else "")
            break
        m = re.search(r"(sora|veo|runway|kling|hailuo|minimax|pika|luma|dream machine|firefly)", v, re.I)
        if m:
            gen = "%s tag names %s" % (k, m.group(1))
            break
    out["provenance"] = gen
    out["camera_atoms"] = {k: tags[k] for k in CAMERA_KEYS if k in tags}
    out["format_match"] = [name for name, durs, fpss in GENERATOR_FORMATS
                           if any(abs(dur - x) < 0.25 for x in durs) and any(abs(fps - f) < 0.05 for f in fpss)]
    return out


def c2pa(video):
    tool = shutil.which("c2patool")
    if not tool:
        return None
    r = subprocess.run([tool, str(video)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        return {"present": False}
    ai = re.search(r"trainedAlgorithmicMedia|compositeWithTrainedAlgorithmicMedia", r.stdout)
    gen = re.search(r'"claim_generator"\s*:\s*"([^"]+)"', r.stdout)
    return {"present": True, "ai_assertion": bool(ai), "generator": gen.group(1) if gen else None}


def sample_pairs(video, n, width=480):
    """n evenly spaced pairs of consecutive frames, grey, scaled to width. Returns [(t, a, b, colour_a)]."""
    import cv2
    cap = cv2.VideoCapture(str(video))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    pairs = []
    if total < 2:
        return pairs
    for i in sorted(set(int(k * (total - 2) / max(1, n - 1)) for k in range(n))):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok1, f1 = cap.read()
        ok2, f2 = cap.read()
        if not (ok1 and ok2):
            continue
        h = int(round(f1.shape[0] * width / f1.shape[1] / 2)) * 2
        c1 = cv2.resize(f1, (width, h), interpolation=cv2.INTER_AREA)
        c2 = cv2.resize(f2, (width, h), interpolation=cv2.INTER_AREA)
        pairs.append((round(i / fps, 3), cv2.cvtColor(c1, cv2.COLOR_BGR2GRAY), cv2.cvtColor(c2, cv2.COLOR_BGR2GRAY), c1))
    cap.release()
    return pairs


def pair_measures(a, b):
    """Flow-warp residual in textured areas, median motion, ORB homography inlier ratio for one frame pair."""
    import cv2
    import numpy as np
    flow = cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    h, w = a.shape
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    warped = cv2.remap(b, gx + flow[..., 0], gy + flow[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    grad = cv2.magnitude(cv2.Sobel(a, cv2.CV_32F, 1, 0), cv2.Sobel(a, cv2.CV_32F, 0, 1))
    sel = grad > np.percentile(grad, 70)
    sel[:8, :] = sel[-8:, :] = False
    sel[:, :8] = sel[:, -8:] = False
    res = np.abs(warped.astype(np.float32) - a.astype(np.float32))
    # residual relative to local contrast so sharp sources are not punished
    resid = float(np.median(res[sel]) / (np.median(grad[sel]) + 1e-6)) if sel.any() else 0.0
    inl = None
    orb = cv2.ORB_create(800)
    ka, da = orb.detectAndCompute(a, None)
    kb, db = orb.detectAndCompute(b, None)
    if da is not None and db is not None and len(ka) > 20 and len(kb) > 20:
        mt = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(da, db)
        if len(mt) >= 12:
            pa = np.float32([ka[x.queryIdx].pt for x in mt])
            pb = np.float32([kb[x.trainIdx].pt for x in mt])
            _, mask = cv2.findHomography(pa, pb, cv2.RANSAC, 3.0)
            if mask is not None:
                inl = float(mask.mean())
    return {"residual": resid, "motion": float(np.median(np.hypot(flow[..., 0], flow[..., 1]))), "inliers": inl}


def frame_measures(g):
    """High-frequency share of the luma spectrum (upsampled video rolls off) and Laplacian variance."""
    import cv2
    import numpy as np
    f = np.abs(np.fft.fftshift(np.fft.fft2(g.astype(np.float32) - g.mean()))) ** 2
    h, w = f.shape
    yy, xx = np.ogrid[:h, :w]
    r = np.hypot((yy - h / 2) / (h / 2), (xx - w / 2) / (w / 2))
    return {"hf_ratio": float(f[(r > 0.5) & (r <= 1)].sum() / (f[r <= 1].sum() + 1e-9)),
            "lap_var": float(cv2.Laplacian(g, cv2.CV_64F).var())}


def band(x, lo, hi):
    """Map x onto [0,1] between lo (0) and hi (1); hi may be below lo for falling signals."""
    if x is None or lo is None:
        return None
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))


def combine(signals, reliability=1.0):
    """Weighted log-odds sum, prior 0. Picture signals in [0,1] are centred (0.5 neutral) and scaled by
    reliability; provenance, camera atoms and format are present (1) or absent (None)."""
    z, used = 0.0, []
    for k, v in signals.items():
        if v is None:
            continue
        if k in ("provenance", "camera_atoms", "format"):
            c = WEIGHTS[k] * v
        else:
            c = WEIGHTS[k] * reliability * (2 * v - 1)
        z += c
        used.append((k, round(c, 2)))
    return round(1 / (1 + math.exp(-z)), 3), sorted(used, key=lambda t: -abs(t[1]))


def verdict_text(score, provenance):
    if provenance and score >= 0.9:
        return "Provenance states this was generated: %s." % provenance
    if score >= 0.75:
        return "Several independent signs consistent with AI generation."
    if score >= 0.4:
        return "Inconclusive; some signs present."
    return "No strong signs found. This does not show the video is authentic."


def contact_sheet(pairs, out, cols=4):
    import cv2
    import numpy as np
    pick = pairs[:: max(1, len(pairs) // (cols * cols))][: cols * cols]
    tiles = []
    for t, _, _, c in pick:
        im = c.copy()
        cv2.putText(im, "%.2fs" % t, (6, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        tiles.append(im)
    while len(tiles) % cols:
        tiles.append(np.zeros_like(tiles[0]))
    cv2.imwrite(str(out), np.vstack([np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]))


def aidetect(video, n=32, out_dir=None):
    try:
        import cv2  # noqa: F401
        import numpy as np
    except ImportError:
        raise SystemExit("aidetect needs opencv-python and numpy (pip install opencv-python numpy)")
    meta = metadata_signals(ffprobe_full(video))
    cp = c2pa(video)
    if cp and cp.get("ai_assertion"):
        meta["provenance"] = "C2PA content credentials (%s)" % (cp.get("generator") or "AI assertion")
    pairs = sample_pairs(video, n)
    pm = [pair_measures(a, b) for _, a, b, _ in pairs]
    fm = [frame_measures(a) for _, a, _, _ in pairs]
    raw = {}
    if pm:
        mot = [p["motion"] for p in pm]
        moving = [p["inliers"] for p in pm if p["inliers"] is not None and p["motion"] > 0.5]
        raw = {"warp_residual": float(np.median([p["residual"] for p in pm])),
               "homography_inliers": float(np.median(moving)) if len(moving) >= 4 else None,
               "motion_median_px": float(np.median(mot)),
               "jerk": float(np.median(np.abs(np.diff(mot, 2)))) if len(mot) > 3 else None,
               "hf_ratio": float(np.median([f["hf_ratio"] for f in fm])),
               "lap_var": float(np.median([f["lap_var"] for f in fm]))}
    bpp = meta.get("bits_per_pixel")
    rel, caveats = 1.0, []
    if bpp is not None and bpp < 0.05:
        rel = 0.5
        caveats.append("heavy compression (%.3f bits per pixel): picture signals down-weighted" % bpp)
    if meta["duration_s"] and meta["duration_s"] < 2:
        rel *= 0.7
        caveats.append("short clip (%.1f s)" % meta["duration_s"])
    sig = {"provenance": 1.0 if meta["provenance"] else None,
           "camera_atoms": 1.0 if meta["camera_atoms"] else None,
           "format": 1.0 if (meta["format_match"] and not meta["camera_atoms"]) else None}
    for k, (lo, hi) in BANDS.items():
        sig[k] = band(raw.get(k), lo, hi)
    score, used = combine(sig, rel)
    caveats += ["picture signals are calibrated on few clips; detectors miss generators they were not tuned on",
                "animation, CGI, game capture and heavy VFX are out of scope and read as AI"]
    rep = {"file": Path(video).name, "score": score, "verdict": verdict_text(score, meta["provenance"]),
           "evidence": [{"signal": k, "log_odds": c} for k, c in used[:5]],
           "metadata": meta, "c2pa": cp,
           "raw": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in raw.items()},
           "frames_sampled": len(pairs), "reliability": rel, "caveats": caveats}
    if pm:
        worst = sorted(range(len(pm)), key=lambda i: -pm[i]["residual"])[:3]
        rep["top_residual_at_s"] = [pairs[i][0] for i in worst]
    if out_dir and pairs:
        od = Path(out_dir)
        od.mkdir(parents=True, exist_ok=True)
        contact_sheet(pairs, od / "contact-sheet.jpg")
        rep["contact_sheet"] = str(od / "contact-sheet.jpg")
        (od / "report.json").write_bytes((json.dumps(rep, indent=2) + "\n").encode("utf-8"))
    return rep


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
    p.add_argument("--method", choices=["auto", "orb", "phase"], default="auto")
    p = g.add_parser("scale"); p.add_argument("measure"); p.add_argument("--json", action="store_true")
    p = g.add_parser("notate"); p.add_argument("notation"); p.add_argument("--out")
    p = g.add_parser("rebuild"); p.add_argument("notation"); p.add_argument("--cards"); p.add_argument("--level")
    p.add_argument("--char-height", type=float, default=2.0)
    p = g.add_parser("aidetect"); p.add_argument("video"); p.add_argument("--frames", type=int, default=32)
    p.add_argument("--out", help="folder for report.json and contact-sheet.jpg")
    p.add_argument("--json", action="store_true")
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
        print(json.dumps(pan(a.video, a.start, a.end, a.fps, method=a.method), indent=2))
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
    elif a.cmd == "aidetect":
        r = aidetect(a.video, a.frames, a.out)
        if a.json:
            print(json.dumps(r, indent=2))
        else:
            print("%s: score %.2f. %s" % (r["file"], r["score"], r["verdict"]))
            for e in r["evidence"]:
                print("  %s %+.2f" % (e["signal"], e["log_odds"]))
            print("  raw: " + ", ".join("%s %s" % kv for kv in r["raw"].items()))
            for c in r["caveats"]:
                print("  caveat: " + c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
