"""cine_seam.py: score the joins between AI video segments and the drift inside each (stdlib + ffmpeg only).

  python scripts/cine_seam.py A.mp4 B.mp4 [C.mp4 ...]   joins between files (a chain of segments, in order)
  python scripts/cine_seam.py film.mp4 --at 5.04,10.08   joins at these times in one cut film
  python scripts/cine_seam.py film.mp4 --every 5.04      joins every N seconds
  add --json for machine output. Exit 1 when any join fails.

Per join: spike = largest frame-to-frame luma change within 2 frames of the join over the median change of the
second either side (1 = invisible, a hard cut is typically 10+); colour step = CIE76 delta E of the mean Lab colour
of the 6 frames before against the 6 after; hist = L1 distance of their luma histograms (0-2); settle = delta E from
the last frame before the join to 0.5/1/2 s after it (a ramp means the new segment drifts away from the handoff);
scale = centre zoom from the last frame before the join to 1 s after it (block matching at 192x108, median
ratio of point distances), against the same over the last second before the join. It warns when the zoom after the join is more
than 5% from 1 and over 1.5x the rate before it (a push-in that speeds up at the join; spike and step miss it).
Per segment: drift = delta E and hist of its first second against its last second, struct = 1 - correlation of
tiny luma thumbnails (camera moves raise it too, so read it with the clip).
Ported from the technique-harvest sc40 study (S28 seam metric, S30 framing check), 2026-11-19."""
import argparse, json, math, shutil, subprocess, sys

W, H = 96, 54
SPIKE_WARN, SPIKE_FAIL = 3.0, 6.0
STEP_WARN, STEP_FAIL = 3.0, 6.0
DRIFT_WARN = 8.0
SCALE_WARN, SCALE_RATE = 0.05, 1.5


def tool(name):
    exe = shutil.which(name)
    if not exe:
        raise SystemExit("%s not found on PATH; see SETUP.md in cinewright-qc." % name)
    return exe


def probe(clip):
    out = subprocess.run([tool("ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=r_frame_rate", "-of", "csv=p=0", clip], capture_output=True, text=True).stdout.strip()
    n, d = (out.split("/") + ["1"])[:2]
    return float(n) / float(d or 1)


def frames(clip):
    raw = subprocess.run([tool("ffmpeg"), "-v", "error", "-i", clip, "-vf", "scale=%d:%d:flags=area" % (W, H),
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = W * H * 3
    return [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lab(rgb):  # sRGB mean -> CIE Lab (D65)
    r, g, b = (_lin(v) for v in rgb)
    x, y, z = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, 0.2126 * r + 0.7152 * g + 0.0722 * b, \
              (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = [t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116 for t in (x, y, z)]
    return (116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2]))


def mean_rgb(fs):
    s, n = [0, 0, 0], 0
    for f in fs:
        for k in range(3):
            s[k] += sum(f[k::3])
        n += len(f) // 3
    return [v / max(n, 1) for v in s]


def luma(f):
    return [(77 * f[i] + 150 * f[i + 1] + 29 * f[i + 2]) >> 8 for i in range(0, len(f), 3)]


def hist(fs, bins=16):
    h = [0] * bins
    for f in fs:
        for v in luma(f):
            h[v * bins >> 8] += 1
    t = sum(h) or 1
    return [v / t for v in h]


def de(a, b):
    return math.dist(lab(mean_rgb(a)), lab(mean_rgb(b)))


def thumb(f, s=4):  # luma downsampled by s in each direction
    y, out = luma(f), []
    for r in range(0, H, s):
        for c in range(0, W, s):
            out.append(sum(y[(r + i) * W + c + j] for i in range(s) for j in range(s) if r + i < H and c + j < W))
    return out


def corr(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) or 1
    return num / den


def gray(clip, w=192, h=108):
    raw = subprocess.run([tool("ffmpeg"), "-v", "error", "-i", clip, "-vf", "scale=%d:%d:flags=area" % (w, h),
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    return [raw[i:i + w * h] for i in range(0, len(raw) - w * h + 1, w * h)]


def zoom(a, b, w=192, h=108, B=12, R=12):
    """Centre zoom from frame a to frame b (gray, w x h): block matching of textured 12 px patches within
    +/-R px, then the median ratio of point distances after/before over pairs more than 40 px apart.
    Robust to a subject moving across part of the frame; resolution about 1%."""
    pts = []
    for by in range(R + 2, h - B - R - 2, 10):
        for bx in range(R + 2, w - B - R - 2, 12):
            pa = [a[(by + y) * w + bx + x] for y in range(B) for x in range(B)]
            m = sum(pa) / len(pa)
            if sum((v - m) ** 2 for v in pa) / len(pa) < 40:
                continue  # flat patch: nothing to match
            pa = [v - m for v in pa]

            def cost(dx, dy):
                pb = [b[(by + dy + y) * w + bx + dx + x] for y in range(B) for x in range(B)]
                mb = sum(pb) / len(pb)
                return sum(abs(p - q + mb) for p, q in zip(pa, pb))
            _, dx, dy = min((cost(x, y), x, y) for x in range(-R, R + 1, 3) for y in range(-R, R + 1, 3))
            _, dx, dy = min((cost(x, y), x, y) for x in range(max(-R, dx - 2), min(R, dx + 2) + 1)
                            for y in range(max(-R, dy - 2), min(R, dy + 2) + 1))
            px, py = bx + B / 2 - w / 2, by + B / 2 - h / 2
            pts.append((px, py, px + dx, py + dy))
    rs = sorted(math.hypot(p[2] - q[2], p[3] - q[3]) / d for i, p in enumerate(pts) for q in pts[i + 1:]
                for d in [math.hypot(p[0] - q[0], p[1] - q[1])] if d > 40)
    return rs[len(rs) // 2] if rs else 1.0


def framing(gs, fps, j):
    """Zoom from the last frame before the join to 1 s after, against the second before it (S30)."""
    k = max(int(round(fps)), 1)
    if not gs or j - 1 - k < 0 or j + k >= len(gs):
        return None
    before, after = zoom(gs[j - 1 - k], gs[j - 1]), zoom(gs[j - 1], gs[j + k])
    la, lb = abs(math.log(before)), abs(math.log(after))
    rate = lb / la if la > 1e-3 else (99.0 if lb > 1e-3 else 1.0)
    warn = abs(after - 1) > SCALE_WARN and rate > SCALE_RATE
    return {"before": round(before, 3), "after": round(after, 3), "rate": round(min(rate, 99.0), 2), "warn": warn}


def score(fs, fps, joins, gs=None):
    """fs: all frames in order; joins: frame indices where a new segment starts."""
    ys = [luma(f) for f in fs]
    d = [sum(abs(a - b) for a, b in zip(ys[i], ys[i + 1])) / len(ys[i]) for i in range(len(ys) - 1)]  # d[i]: i -> i+1
    sec = max(int(round(fps)), 2)
    out = []
    for j in joins:
        win = range(max(0, j - 3), min(len(d), j + 2))  # transitions j-3..j+1 cover a duplicated handoff frame
        near = [d[i] for i in range(max(0, j - sec), min(len(d), j + sec)) if i not in win]
        med = sorted(near)[len(near) // 2] if near else 1.0
        spike = max(d[i] for i in win) / max(med, 0.25)
        a, b = fs[max(0, j - 6):j], fs[j:j + 6]
        hs = sum(abs(x - y) for x, y in zip(hist(a), hist(b)))
        settle = [round(de([fs[j - 1]], [fs[min(len(fs) - 1, j + int(t * fps))]]), 1) for t in (0.5, 1.0, 2.0)]
        step = de(a, b)
        fr = framing(gs, fps, j)
        st = "FAIL" if spike > SPIKE_FAIL or step > STEP_FAIL else \
            "WARN" if spike > SPIKE_WARN or step > STEP_WARN or (fr and fr["warn"]) else "PASS"
        out.append({"frame": j, "t": round(j / fps, 2), "status": st, "spike": round(spike, 2), "median_diff": round(med, 2),
                    "colour_step": round(step, 2), "hist": round(hs, 3), "settle": settle, "scale": fr})
    return out


def drift(fs, fps):
    k = max(int(round(fps)), 1)
    a, b = fs[:k], fs[-k:]
    st = 1 - corr(thumb(fs[0]), thumb(fs[-1]))
    dE = de(a, b)
    return {"frames": len(fs), "drift_dE": round(dE, 2), "drift_hist": round(sum(abs(x - y) for x, y in zip(hist(a), hist(b))), 3),
            "struct": round(st, 3), "status": "WARN" if dE > DRIFT_WARN else "PASS"}


def run(clips, at=None, every=None):
    fps = probe(clips[0])
    segs = [frames(c) for c in clips]
    if not all(segs):
        raise SystemExit("no frames decoded from %s" % ", ".join(c for c, s in zip(clips, segs) if not s))
    fs = [f for s in segs for f in s]
    gs = [g for c in clips for g in gray(c)]
    if len(clips) > 1:
        joins, n = [], 0
        for s in segs[:-1]:
            n += len(s)
            joins.append(n)
    else:
        dur = len(fs) / fps
        ts = [float(t) for t in at.split(",") if t] if at is not None else [every * k for k in range(1, int(dur / every)) if every * k < dur - 0.2]
        joins = [int(round(t * fps)) for t in ts]
    bounds = [0] + joins + [len(fs)]
    return {"clips": clips, "fps": round(fps, 3), "frames": len(fs), "joins": score(fs, fps, joins, gs if len(gs) == len(fs) else None),
            "segments": [drift(fs[a:b], fps) for a, b in zip(bounds, bounds[1:]) if b - a > 2]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clips", nargs="+")
    ap.add_argument("--at", help="comma list of join times in one cut film, seconds")
    ap.add_argument("--every", type=float, help="joins every N seconds in one cut film")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    r = run(a.clips, at="") if len(a.clips) == 1 and not (a.at or a.every) else run(a.clips, a.at, a.every)
    fails = sum(1 for j in r["joins"] if j["status"] == "FAIL")
    if a.json:
        print(json.dumps(r, indent=1))
        return 1 if fails else 0
    for j in r["joins"]:
        sc = j["scale"]
        print("%-4s join %.2fs: spike %.1fx (median %.2f), colour step dE %.1f, hist %.3f, settle dE %s%s"
              % (j["status"], j["t"], j["spike"], j["median_diff"], j["colour_step"], j["hist"], j["settle"],
                 ", scale %.3f at +1 s (%.3f over the second before, %.1fx)%s" % (sc["after"], sc["before"], sc["rate"],
                 " FRAMING JUMP" if sc["warn"] else "") if sc else ""))
    for i, s in enumerate(r["segments"], 1):
        print("%-4s segment %d (%d frames): drift dE %.1f, hist %.3f, struct %.3f"
              % (s["status"], i, s["frames"], s["drift_dE"], s["drift_hist"], s["struct"]))
    worst = "FAIL" if fails else "WARN" if any(j["status"] == "WARN" for j in r["joins"]) else "PASS"
    tips = []
    if any(j["colour_step"] >= STEP_WARN for j in r["joins"]):
        tips.append("colour step 3 dE or more: colour-match B to A's tail (MKL, constant, never a ramp)")
    if any(j["spike"] > SPIKE_WARN for j in r["joins"]):
        tips.append("a jump at the join: code seam-restart")
    if any(j["scale"] and j["scale"]["warn"] for j in r["joins"]):
        tips.append("framing jump: unless the card plans a push-in, reroll B or rank another take")
    print("qc seam: %d join(s), %s%s" % (len(r["joins"]), worst, ("; " + "; ".join(tips)) if tips else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
