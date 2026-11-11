# HANDOFF: video analysis chain aidetect

Status: finished

Split out of the "Video analysis track" in ai-docs/HANDOFF.md on 2026-11-11. Steps are in the chain prompt.

Done (session 1, 2026-11-11, v0.6.1):
1. `aidetect` command in plugins/cinewright/skills/cinewright-analyze/scripts/cine_analyze.py, tests in tests/test_cine.py TestAnalyze (3 new).
2. Calibrated on 16 of our renders, 5 Sora clips, 3 phone clips plus re-encodes: research/2026-11-11-ai-video-detection.md section 8.
3. ai-video-tells entry records the calibration and the scored band (hf_ratio 0.020 to 0.008); motion signals reported raw, unscored.

Next (outside this chain, optional): a larger phone-clip set to decide whether warp residual, homography and jerk can be scored.
Waiting on Mark: nothing.
