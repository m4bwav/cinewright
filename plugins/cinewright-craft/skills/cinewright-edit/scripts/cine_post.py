#!/usr/bin/env python3
# copied from shared/lib/cine_post.py sha256:732ab6c6967230103e8c26310b8430de60d0b0f9d30f6abe2dc3d563264a6322; edit the source
"""cinewright post tools: animatic before any video spend, and one grade across every shot after.

Run it; do not read it. Python 3.9+, standard library only, ffmpeg and ffprobe on PATH.

  python scripts/cine_post.py animatic PROJECT --stills DIR [--audio WAV] [--size 960x540] [--out FILE]
  python scripts/cine_post.py grade measure FILE ... [--plan PROJECT]
  python scripts/cine_post.py grade stabilize FILE ... --out DIR [--ref-time S] [--window S] [--luma-only]
  python scripts/cine_post.py grade match --ref STILL FILE ... [--luma N] [--sat C] [--warm W] [--strength S] [--cube-dir DIR]
                                         [--apply DIR [--look LOOK.cube] [--grain N]]

animatic: one still per card (DIR/<card id>.png|jpg|webp, e.g. the approved first frames), held for the
card's duration with its camera move suggested by a slow push or drift, over a scratch audio track; a
card with no still shows a grey frame. Writes the video and a timing sheet (<out>.timing.md) with each
card's in and out point, beat and lines, which lock the cut before a render is paid for.

grade: measure prints each file's mean and spread per RGB channel and its luma; match fits every file to
a hero still (per-channel mean and spread, scaled by --strength) and writes one 3D LUT per file
(.cube, 17 points, readable by ffmpeg lut3d, Resolve and Premiere); --luma also sets a mean luma target,
for light that falls scene by scene; --apply writes graded copies with ffmpeg lut3d: the match, then the
film's one look LUT (--look), then grain (--grain, ffmpeg noise strength; 4 to 8 reads as fine film grain).
Stats are pooled over up to 12 frames a shot, so the correction is one fixed transform and cannot flicker.
--sat and --warm set the scene's colour-script chroma and warmth after the match.

grade measure --plan PROJECT: per shot (named by card id) mean luma, tone spread, chroma, warmth, edge
orientation and motion, each scene's colour row checked by class, and each visual_structure plan ranked
against the cut order (progression) or the intensity (peaks). Exit 1 when the cut runs against the plan.
grade stabilize: per-frame gains toward one reference frame, smoothed over a second, applied with ffmpeg
sendcmd; fixes slow exposure and white balance drift inside a take. Order: stabilize, deflicker, match, look.
"""
import argparse
import importlib.util
import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("cine_runtime", HERE / "cine.py")
cine = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cine)

STILL_EXT = (".png", ".jpg", ".jpeg", ".webp")
# a card's camera move as a zoompan over a still: (zoom start, zoom end, x drift as a share of the width)
MOVE_PAN = {"dolly-in": (1.0, 1.12, 0), "zoom-in": (1.0, 1.12, 0), "dolly-out": (1.12, 1.0, 0), "zoom-out": (1.12, 1.0, 0),
            "truck-left": (1.08, 1.08, -0.06), "truck-right": (1.08, 1.08, 0.06), "pan-left": (1.08, 1.08, -0.06),
            "pan-right": (1.08, 1.08, 0.06), "track": (1.06, 1.06, 0.04), "crane-up": (1.06, 1.1, 0),
            "crane-down": (1.1, 1.06, 0)}
FPS = 24


def ts(seconds):
    m, s = divmod(seconds, 60)
    return "%02d:%06.3f" % (m, s)


def find_still(stills, cid):
    for ext in STILL_EXT:
        f = stills / (cid + ext)
        if f.is_file():
            return f
    return None


def segment(ff, still, card, w, h, out):
    """One card as a clip: the still scaled to cover the frame, its move as a slow zoompan, or grey."""
    dur = float(card["duration_s"])
    n = max(1, int(round(dur * FPS)))
    if still is None:
        args = [ff, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0x404040:s=%dx%d:r=%d:d=%.3f" % (w, h, FPS, dur)]
    else:
        z0, z1, dx = MOVE_PAN.get(card["camera"].get("move"), (1.0, 1.0, 0))
        # work at 2x so zoompan's integer crop steps do not judder
        zoom = "%.4f+(%.4f)*on/%d" % (z0, z1 - z0, n)
        x = "(iw-iw/zoom)/2+(%.4f)*iw*(on/%d-0.5)" % (dx, n)
        vf = ("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,"
              "zoompan=z='%s':x='%s':y='(ih-ih/zoom)/2':d=%d:s=%dx%d:fps=%d") % (w * 2, h * 2, w * 2, h * 2, zoom, x, n, w, h, FPS)
        args = [ff, "-y", "-loglevel", "error", "-loop", "1", "-i", str(still), "-vf", vf, "-frames:v", str(n)]
    cine.run_tool(args + ["-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "20", "-r", str(FPS), str(out)])


def cmd_animatic(a):
    p = cine.Project(a.project)
    ff = cine.need_tool("ffmpeg")
    stills = Path(a.stills)
    w, h = (int(x) for x in a.size.lower().split("x"))
    out = Path(a.out or Path(a.project) / "animatic.mp4")
    work = out.parent / (out.stem + "_parts")
    work.mkdir(parents=True, exist_ok=True)
    rows, missing, t = [], [], 0.0
    lst = []
    for c in p.cards:
        still = find_still(stills, c["id"])
        if still is None:
            missing.append(c["id"])
        part = work / ("%03d_%s.mp4" % (len(lst), c["id"]))
        segment(ff, still, c, w, h, part)
        lst.append("file '%s'" % part.resolve().as_posix())
        lines = " / ".join("%s: %s" % (p.chars[d["character"]]["name"], d["line"]) for d in c.get("dialogue", []))
        rows.append((c["id"], t, t + c["duration_s"], c.get("beat", ""), lines, still.name if still else "(grey)"))
        t += c["duration_s"]
    (work / "list.txt").write_text("\n".join(lst) + "\n", encoding="utf-8")
    args = [ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt")]
    if a.audio:
        # the scratch track sets nothing: the cards' durations are the cut, the audio is trimmed or padded to it
        args += ["-i", a.audio, "-map", "0:v", "-map", "1:a", "-af", "apad", "-t", "%.3f" % t, "-c:a", "aac"]
    cine.run_tool(args + ["-c:v", "copy", str(out)])
    sheet = ["# Animatic timing: %s" % p.style.get("title", ""), "",
             "%d cards, %s total. Stills from `%s`." % (len(rows), ts(t), stills.as_posix()), "",
             "| card | in | out | s | beat | lines | still |", "|---|---|---|---|---|---|---|"]
    for cid, a0, a1, beat, lines, still in rows:
        sheet.append("| %s | %s | %s | %g | %s | %s | %s |" % (cid, ts(a0), ts(a1), a1 - a0, beat.replace("|", "/"), lines.replace("|", "/"), still))
    timing = out.with_suffix(".timing.md")
    timing.write_text("\n".join(sheet) + "\n", encoding="utf-8")
    print("wrote %s (%s) and %s" % (out, ts(t), timing))
    if missing:
        print("no still for %s: grey frames; put <card id>.png in %s" % (", ".join(missing), stills))
    return 0


# ---------- grade ----------

def frames_rgb(path, size=(64, 36), fps=1.0, max_frames=12):
    """Small RGB frames from a still or a clip, as one flat byte string per frame."""
    ff = cine.need_tool("ffmpeg")
    w, h = size
    vf = "scale=%d:%d" % (w, h)
    args = [ff, "-v", "error", "-i", str(path)]
    if Path(path).suffix.lower() not in STILL_EXT:
        vf = "fps=%g,%s" % (fps, vf)
        args += ["-frames:v", str(max_frames)]
    r = subprocess.run(args + ["-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        raise SystemExit("ffmpeg could not read %s: %s" % (path, r.stderr.decode(errors="replace")[-300:]))
    n = w * h * 3
    return [r.stdout[i:i + n] for i in range(0, len(r.stdout) - n + 1, n)]


def stats(path):
    """Mean and standard deviation per channel (0..1) and Rec.709 mean luma (0..255 full range)."""
    sums, sq, count = [0.0] * 3, [0.0] * 3, 0
    for fr in frames_rgb(path):
        for c in range(3):
            ch = fr[c::3]
            sums[c] += sum(ch)
            sq[c] += sum(v * v for v in ch)
        count += len(fr) // 3
    mean = [s / count / 255 for s in sums]
    sd = [math.sqrt(max(0.0, q / count / 65025 - m * m)) for q, m in zip(sq, mean)]
    luma = 255 * (0.2126 * mean[0] + 0.7152 * mean[1] + 0.0722 * mean[2])
    return {"mean": mean, "sd": sd, "luma": luma}


def fit(src, ref, strength=1.0, luma=None):
    """Per-channel gain and offset that move src's mean and spread toward ref's (Reinhard, in RGB),
    blended by strength; then one shared gain so the mean luma lands on `luma` when given."""
    gains, offs = [], []
    for c in range(3):
        g = ref["sd"][c] / src["sd"][c] if src["sd"][c] > 1e-4 else 1.0
        g = min(2.5, max(0.4, g))  # a near-flat shot would otherwise blow up its noise
        o = ref["mean"][c] - g * src["mean"][c]
        gains.append(1 + strength * (g - 1))
        offs.append(strength * o)
    if luma is not None:
        now = 255 * sum(k * (g * m + o) for k, g, m, o in zip((0.2126, 0.7152, 0.0722), gains, src["mean"], offs))
        k = luma / now if now > 1 else 1.0
        gains = [g * k for g in gains]
        offs = [o * k for o in offs]
    return gains, offs


def transform(v, gains, offs, sat=1.0, warm=0.0):
    """One RGB triple (0..1) through the match: per-channel gain and offset, then chroma scaled around luma, then a warm shift."""
    c = [gains[i] * v[i] + offs[i] for i in range(3)]
    if sat != 1.0:
        y = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
        c = [y + sat * (x - y) for x in c]
    return [min(1.0, max(0.0, x)) for x in (c[0] + warm / 2, c[1], c[2] - warm / 2)]


def write_cube(path, gains, offs, n=17, title="cinewright match", sat=1.0, warm=0.0):
    lines = ['TITLE "%s"' % title, "LUT_3D_SIZE %d" % n, "DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1"]
    for b in range(n):  # .cube order: red changes fastest
        for g in range(n):
            for r in range(n):
                lines.append(" ".join("%.6f" % x for x in transform([x / (n - 1) for x in (r, g, b)], gains, offs, sat, warm)))
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------- look measures (Block's components, cinewright-design visual-structure) ----------

# Class bounds: brightness by thirds of the grey scale (Block); chroma and warmth at the sixths of 354 shots from 118
# reviewed takes of local multi-shot films (2026-10-22), so each end class holds about a sixth (shot-matching, Numbers)
BRIGHT_THIRDS = (85, 170)
CHROMA_BOUNDS = (0.10, 0.155)
WARM_BOUNDS = (0.02, 0.13)
CLASSES = {"brightness": ("dark", "middle", "bright"), "saturation": ("muted", "mid", "saturated"), "warmth": ("cool", "neutral", "warm")}
ORD = {"dark": 0, "middle": 1, "bright": 2, "muted": 0, "desaturated": 0, "mid": 1, "saturated": 2, "cool": 0, "neutral": 1, "warm": 2,
       "low": 0, "narrow": 0, "affinity": 0, "high": 2, "wide": 2, "contrast": 2, "horizontal": 0, "vertical": 1, "diagonal": 2,
       "still": 0, "static": 0, "calm": 0, "moving": 2, "fast": 2}
MEASURED = {"tone": "contrast", "brightness": "luma", "saturation": "chroma", "warmth": "warmth", "line": "diagonal", "movement": "motion"}
STABILIZE_WARN = 8  # luma; 7 of 8 real shots drifted 0.3-4.3, the one at 11.9 was a tracking shot whose street changed
PLAN_RHO = 0.3  # |Spearman rho| below this is "weak": the measure neither follows nor fights the plan


def look_stats(path):
    """Block's measurable components of one shot: mean luma and its p5-p95 spread (tone), mean chroma (saturation),
    mean R minus B (warmth), edge orientation shares (line), and mean frame difference (movement, clips only)."""
    w, h = 160, 90
    ys, chroma, warm, edges = [], 0.0, 0.0, [0, 0, 0]  # edges: horizontal, vertical, diagonal
    count = 0
    for fr in frames_rgb(path, size=(w, h), fps=2.0):
        y = [0.2126 * fr[i] + 0.7152 * fr[i + 1] + 0.0722 * fr[i + 2] for i in range(0, len(fr), 3)]
        ys.extend(y)
        for i in range(0, len(fr), 3):
            r, g, b = fr[i], fr[i + 1], fr[i + 2]
            chroma += (max(r, g, b) - min(r, g, b)) / 255
            warm += (r - b) / 255
        count += len(y)
        mags = []
        for yy in range(1, h - 1):
            for xx in range(1, w - 1):
                k = yy * w + xx
                gx = y[k - w + 1] + 2 * y[k + 1] + y[k + w + 1] - y[k - w - 1] - 2 * y[k - 1] - y[k + w - 1]
                gy = y[k + w - 1] + 2 * y[k + w] + y[k + w + 1] - y[k - w - 1] - 2 * y[k - w] - y[k - w + 1]
                mags.append((abs(gx) + abs(gy), gx, gy))
        mags.sort(reverse=True)
        for m, gx, gy in mags[:len(mags) // 5]:  # the strongest fifth of the edges carry the line
            if m < 40:
                break
            ax, ay = abs(gx), abs(gy)
            edges[0 if ay > 2.4 * ax else 1 if ax > 2.4 * ay else 2] += 1  # a vertical gradient is a horizontal edge; 2.4 = tan 67.5
    ys.sort()
    n = max(1, sum(edges))
    out = {"luma": sum(ys) / len(ys), "contrast": ys[int(0.95 * (len(ys) - 1))] - ys[int(0.05 * (len(ys) - 1))],
           "chroma": chroma / count, "warmth": warm / count, "horizontal": edges[0] / n, "vertical": edges[1] / n, "diagonal": edges[2] / n}
    if Path(path).suffix.lower() not in STILL_EXT:
        mo = [m for _, m in cine.frame_motion(path)][1:]
        out["motion"] = sum(mo) / len(mo) if mo else 0.0
    return out


def classify(s):
    def third(v, lo_hi, names):
        return names[0] if v < lo_hi[0] else names[2] if v >= lo_hi[1] else names[1]
    return {"brightness": third(s["luma"], BRIGHT_THIRDS, CLASSES["brightness"]), "saturation": third(s["chroma"], CHROMA_BOUNDS, CLASSES["saturation"]),
            "warmth": third(s["warmth"], WARM_BOUNDS, CLASSES["warmth"])}


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(xs, ys):
    """Spearman rank correlation (ties averaged); None when either side has no spread."""
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sx, sy = math.sqrt(sum((a - mx) ** 2 for a in rx)), math.sqrt(sum((b - my) ** 2 for b in ry))
    return sxy / (sx * sy) if sx and sy else None


def card_for(p, path):
    """The card a shot file belongs to: the longest card id that appears in its name as a whole token (1A, 12B, take_3C-2)."""
    stem = Path(path).stem
    hits = [c for c in p.cards if re.search(r"(?<![0-9A-Za-z])%s(?![A-Z0-9])" % re.escape(c["id"]), stem)]
    return max(hits, key=lambda c: len(c["id"])) if hits else None


def plan_report(p, shots):
    """shots: [(path, card, stats)] in cut order -> report lines. Checks the measured components against the visual plan."""
    out, against = [], 0
    rows = []
    for path, c, s in shots:
        sc = p.scene_map.get(c["scene"], {})
        cls, want = classify(s), sc.get("color", {})
        miss = []
        for k in ("brightness", "saturation", "warmth"):
            if want.get(k) in CLASSES[k]:
                gap = abs(CLASSES[k].index(want[k]) - CLASSES[k].index(cls[k]))
                if gap:
                    miss.append("%s %s, planned %s" % (k, cls[k], want[k]))
                    against += gap == 2
        rows.append((c, s, c.get("intensity", sc.get("intensity")), miss))
        out.append("%-5s int %3s  luma %5.1f  contrast %5.1f  chroma %.3f  warmth %+.3f  diagonal %.2f  motion %s%s" % (
            c["id"], "-" if rows[-1][2] is None else rows[-1][2], s["luma"], s["contrast"], s["chroma"], s["warmth"], s["diagonal"],
            "%.2f" % s["motion"] if "motion" in s else "-", ("  OFF " + "; ".join(miss)) if miss else ""))
    vs = p.style.get("visual_structure", {})
    graded = [r for r in rows if r[2] is not None]
    for pl in vs.get("plans", []):
        key = MEASURED.get(pl["component"])
        if not key:
            out.append("plan %s: not measured (judge it on the contact sheet)" % pl["component"])
            continue
        pts = [r for r in rows if key in r[1]]
        if len(pts) < 4:
            out.append("plan %s: %d shots, too few to rank (4 or more)" % (pl["component"], len(pts)))
            continue
        vals = [r[1][key] for r in pts]
        if pl["mode"] == "progression":
            rho = spearman(list(range(len(pts))), vals)
            a, b = ORD.get(str(pl.get("from", "")).lower()), ORD.get(str(pl.get("to", "")).lower())
            sign = (b > a) - (b < a) if a is not None and b is not None else 0
            what = "over the cut"
        else:
            mid = sorted(vals)[len(vals) // 2]
            pts = [r for r in pts if r[2] is not None]
            rho = spearman([r[2] for r in pts], [abs(r[1][key] - mid) for r in pts]) if len(pts) >= 4 else None
            sign, what = 1, "as contrast against intensity"
        if rho is None:
            out.append("plan %s (%s): no spread to rank" % (pl["component"], pl["mode"]))
            continue
        verdict = "follows" if sign and rho * sign >= PLAN_RHO else "AGAINST" if sign and rho * sign <= -PLAN_RHO else "weak" if sign else "no direction"
        against += verdict == "AGAINST"
        out.append("plan %s (%s %s): %s rho %+.2f %s" % (pl["component"], pl["mode"], "%s to %s" % (pl.get("from", "?"), pl.get("to", "?"))
                   if pl["mode"] == "progression" else "at " + ",".join(pl.get("peaks", [])), key, rho, "%s %s" % (verdict, what)))
    if len(graded) >= 4:
        for key in ("contrast", "chroma", "motion"):
            pts = [r for r in graded if key in r[1]]
            rho = spearman([r[2] for r in pts], [r[1][key] for r in pts]) if len(pts) >= 4 else None
            if rho is not None:
                out.append("intensity vs %s: rho %+.2f" % (key, rho))
    out.append("grade measure --plan: %d shots, %d against the plan (a class two steps off, or a plan the cut runs against)" % (len(shots), against))
    return out, against


def frames_all(path, size=(64, 36)):
    """Every frame of a clip, small, as RGB byte strings, plus the clip's fps."""
    info = cine.probe(path)
    w, h = size
    r = subprocess.run([cine.need_tool("ffmpeg"), "-v", "error", "-i", str(path), "-an", "-vf", "scale=%d:%d" % (w, h),
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    n = w * h * 3
    return [r.stdout[i:i + n] for i in range(0, len(r.stdout) - n + 1, n)], info["fps"]


def channel_means(fr):
    k = len(fr) // 3
    return [sum(fr[c::3]) / k for c in range(3)]


def drift(means, fps):
    """Range of the 1 s mean luma across a shot: slow exposure drift, which frame-to-frame deflicker does not see."""
    y = [0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2] for m in means]
    win = max(1, int(round(fps)))
    sm = [sum(y[i:i + win]) / win for i in range(0, max(1, len(y) - win + 1))]
    return max(sm) - min(sm)


def stabilize_gains(means, fps, ref_t=None, window=1.0, luma_only=False):
    """Per-frame gains that hold each channel at the reference frame's level, smoothed over `window` seconds so
    flicker is left to deflicker; clamped to 0.6-1.6."""
    n = len(means)
    i0 = min(n - 1, max(0, int(round((ref_t if ref_t is not None else n / fps / 2) * fps))))
    near = means[max(0, i0 - int(fps / 4)):i0 + int(fps / 4) + 1]
    ref = [sum(m[c] for m in near) / len(near) for c in range(3)]
    raw = []
    for m in means:
        if luma_only:
            ry, my = (0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2] for v in (ref, m))
            g = [ry / my if my > 1 else 1.0] * 3
        else:
            g = [ref[c] / m[c] if m[c] > 1 else 1.0 for c in range(3)]
        raw.append([min(1.6, max(0.6, x)) for x in g])
    half = max(0, int(window * fps / 2))
    out = []
    for i in range(n):
        span = raw[max(0, i - half):i + half + 1]
        out.append([sum(g[c] for g in span) / len(span) for c in range(3)])
    return out


def cmd_grade(a):
    if a.cmd == "measure" and a.plan:
        p = cine.Project(a.plan)
        shots, loose = [], []
        for f in a.files:
            c = card_for(p, f)
            if c:
                shots.append((f, c, look_stats(f)))
            else:
                loose.append(f)
        if loose:
            print("no card id in the name of %s; name shots <card id>.mp4 (1A.mp4, take_1A-2.mp4)" % ", ".join(str(x) for x in loose))
        shots.sort(key=lambda x: x[1]["order"])
        lines, against = plan_report(p, shots)
        print("\n".join(lines))
        return 1 if against else 0
    if a.cmd == "measure":
        for f in a.files:
            s = stats(f)
            print("%s  luma %.1f  mean %s  sd %s" % (f, s["luma"], " ".join("%.3f" % x for x in s["mean"]), " ".join("%.3f" % x for x in s["sd"])))
        return 0
    if a.cmd == "stabilize":
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        ff = cine.need_tool("ffmpeg")
        for f in a.files:
            frames, fps = frames_all(f)
            means = [channel_means(x) for x in frames]
            gains = stabilize_gains(means, fps, a.ref_time, a.window, a.luma_only)
            cmd = out / (Path(f).stem + ".sendcmd.txt")
            cmd.write_text("".join("%.4f colorchannelmixer rr %.4f, colorchannelmixer gg %.4f, colorchannelmixer bb %.4f;\n" % (i / fps, g[0], g[1], g[2])
                                   for i, g in enumerate(gains)), encoding="utf-8")
            dest = out / Path(f).name
            path = cmd.resolve().as_posix().replace(":", r"\:")
            cine.run_tool([ff, "-y", "-loglevel", "error", "-i", str(f), "-vf", "sendcmd=f='%s',colorchannelmixer" % path,
                           "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy", str(dest)])
            after, fps2 = frames_all(dest)
            was = drift(means, fps)
            print("%s  drift %.1f -> %.1f luma (1 s means), gains %.2f-%.2f  -> %s" % (
                f, was, drift([channel_means(x) for x in after], fps2), min(min(g) for g in gains), max(max(g) for g in gains), dest))
            if was > STABILIZE_WARN:
                print("WARN %s: drift over %d luma is usually the picture changing (a moving camera, a lamp switched on), not exposure; "
                      "compare it by eye and keep the original when the change is meant" % (Path(f).name, STABILIZE_WARN))
        return 0
    ref = stats(a.ref)
    print("ref %s  luma %.1f" % (a.ref, ref["luma"]))
    cube_dir = Path(a.cube_dir or Path(a.files[0]).parent / "grade")
    cube_dir.mkdir(parents=True, exist_ok=True)
    report = {"ref": str(a.ref), "strength": a.strength, "luma": a.luma, "sat": a.sat, "warm": a.warm, "files": {}}
    ff = cine.need_tool("ffmpeg") if a.apply else None
    for f in a.files:
        s = stats(f)
        gains, offs = fit(s, ref, a.strength, a.luma)
        sat, warm = 1.0, 0.0
        if a.sat is not None or a.warm is not None:
            # targets from the colour script: chroma and R minus B after the match, measured on the shot's own frames
            # sampled as look_stats reads them (every 3rd pixel); the warm shift adds chroma and saturation scales R - B, so solve both a few rounds
            px = [[v / 255 for v in fr[i:i + 3]] for fr in frames_rgb(f, size=(160, 90), fps=2.0) for i in range(0, len(fr), 9)]
            for _ in range(4):
                moved = [transform(v, gains, offs, sat, warm) for v in px]
                if a.sat is not None:
                    now = sum(max(v) - min(v) for v in moved) / len(moved)
                    sat = min(2.0, max(0.3, sat * a.sat / now)) if now > 1e-3 else sat
                if a.warm is not None:
                    warm += a.warm - sum(v[0] - v[2] for v in moved) / len(moved)
        cube = cube_dir / (Path(f).stem + ".cube")
        write_cube(cube, gains, offs, title="match %s to %s" % (Path(f).name, Path(a.ref).name), sat=sat, warm=warm)
        row = {"luma": round(s["luma"], 1), "gain": [round(x, 3) for x in gains], "offset": [round(x, 4) for x in offs], "cube": cube.name}
        if sat != 1.0 or warm:
            row.update(sat=round(sat, 3), warm=round(warm, 4))
        if a.apply:
            dest = Path(a.apply) / Path(f).name
            dest.parent.mkdir(parents=True, exist_ok=True)
            # lut3d wants a path ffmpeg can parse inside a filter string: forward slashes, colon escaped
            lut = cube.resolve().as_posix().replace(":", r"\:")
            chain = ["lut3d=file='%s'" % lut]
            if a.look:
                chain.append("lut3d=file='%s'" % Path(a.look).resolve().as_posix().replace(":", r"\:"))
            if a.grain:
                chain.append("noise=alls=%d:allf=t" % a.grain)
            args = [ff, "-y", "-loglevel", "error", "-i", str(f), "-vf", ",".join(chain)]
            if Path(f).suffix.lower() not in STILL_EXT:
                args += ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy"]
            cine.run_tool(args + [str(dest)])
            row["after_luma"] = round(stats(dest)["luma"], 1)
        report["files"][str(f)] = row
        print("%s  luma %.1f -> %s  gain %s" % (f, s["luma"], row.get("after_luma", "(not applied)"), " ".join("%.2f" % x for x in gains)))
    (cube_dir / "grade.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("cubes and grade.json in %s" % cube_dir)
    return 0


def build_parser():
    ap = argparse.ArgumentParser(prog="cine_post.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_subparsers(dest="group", required=True)
    s = g.add_parser("animatic", help="stills timed to the cards, over scratch audio, plus a timing sheet")
    s.add_argument("project")
    s.add_argument("--stills", required=True, help="folder of <card id>.png|jpg|webp")
    s.add_argument("--audio", help="scratch track (temp voices, music) laid under the stills")
    s.add_argument("--size", default="960x540")
    s.add_argument("--out", help="default PROJECT/animatic.mp4")
    gr = g.add_parser("grade", help="measure shots, match them to a hero still").add_subparsers(dest="cmd", required=True)
    s = gr.add_parser("measure", help="per-channel stats; with --plan, Block's components against the visual plan")
    s.add_argument("files", nargs="+")
    s.add_argument("--plan", metavar="PROJECT", help="check each shot (named by its card id) against the scene colour rows and visual_structure plans")
    s = gr.add_parser("stabilize", help="hold exposure and white balance inside a shot to one reference frame (slow drift; before match)")
    s.add_argument("files", nargs="+")
    s.add_argument("--out", required=True, help="folder for the stabilised copies")
    s.add_argument("--ref-time", type=float, help="seconds into the shot of the reference frame (default the middle)")
    s.add_argument("--window", type=float, default=1.0, help="seconds the gains are smoothed over (default 1; flicker is deflicker's job)")
    s.add_argument("--luma-only", action="store_true", help="one gain for all channels: fix brightness, keep the colour drift")
    s = gr.add_parser("match")
    s.add_argument("files", nargs="+")
    s.add_argument("--ref", required=True, help="the hero still every shot is matched to")
    s.add_argument("--strength", type=float, default=0.7, help="0 = no change, 1 = full match (default 0.7)")
    s.add_argument("--luma", type=float, help="mean luma target 0-255 (full range), e.g. darker for night scenes")
    s.add_argument("--sat", type=float, help="mean chroma target after the match (0-1, as grade measure --plan prints it)")
    s.add_argument("--warm", type=float, help="mean R minus B target after the match (-1 to 1, as grade measure --plan prints it)")
    s.add_argument("--cube-dir", help="where the .cube files and grade.json go (default <first file's folder>/grade)")
    s.add_argument("--apply", metavar="DIR", help="write graded copies here")
    s.add_argument("--look", metavar="CUBE", help="the film's one look LUT, applied after the match (with --apply)")
    s.add_argument("--grain", type=int, default=0, help="film grain after the look, ffmpeg noise strength (with --apply)")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    return cmd_animatic(a) if a.group == "animatic" else cmd_grade(a)


if __name__ == "__main__":
    sys.exit(main())
