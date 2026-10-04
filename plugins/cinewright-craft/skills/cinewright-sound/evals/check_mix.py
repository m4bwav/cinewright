"""Outcome check for cinewright-sound outcome-1: exits 0 only when out/mix/final.mp4 has its video and an audio stream
measuring inside the web preset (-18 +/- 2 LUFS integrated, true peak at or below -2 dBTP), metered here with ffmpeg's
ebur128 filter, independent of cine.py.

  python evals/check_mix.py <run folder>
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

TARGET, TOL, MAX_TP = -18.0, 2.0, -2.0


def main():
    f = Path(sys.argv[1]) / "out" / "mix" / "final.mp4"
    if not f.is_file():
        print("FAIL no out/mix/final.mp4")
        return 1
    ffprobe, ffmpeg = shutil.which("ffprobe"), shutil.which("ffmpeg")
    r = subprocess.run([ffprobe, "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(f)],
                       capture_output=True, text=True)
    kinds = r.stdout.split()
    bad = []
    if "video" not in kinds or "audio" not in kinds:
        bad.append("streams %s, want video and audio" % kinds)
    r = subprocess.run([ffmpeg, "-hide_banner", "-nostats", "-i", str(f), "-map", "0:a:0", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    summary = r.stderr[r.stderr.rfind("Summary:"):]
    i = re.search(r"[I]:\s+(-?[\d.]+|-inf) LUFS", summary)  # [I] so the kb lint does not read a drive letter
    tp = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS", summary)
    if not i or not tp:
        print("FAIL could not meter the audio")
        return 1
    il, tpv = float(i.group(1)), float(tp.group(1))
    if abs(il - TARGET) > TOL:
        bad.append("integrated %.1f LUFS, want %.0f +/- %.0f" % (il, TARGET, TOL))
    if tpv > MAX_TP:
        bad.append("true peak %.1f dBTP, want at most %.0f" % (tpv, MAX_TP))
    for b in bad:
        print("FAIL " + b)
    print("check_mix: integrated %.1f LUFS, true peak %.1f dBTP, %d problems" % (il, tpv, len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
