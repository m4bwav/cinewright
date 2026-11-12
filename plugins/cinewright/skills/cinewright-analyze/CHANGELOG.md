# cinewright-analyze changelog

## 2026-11-11 (unreleased)

- `pan --method auto|orb|phase`: ORB landmarks with a RANSAC fit by default when opencv is present (L-20261111-2); on the benchmark first shot steps are 0 when static and ramp smoothly through pans, where phase gave -256 to +384 px.
- Description: not for judging your own take against its card (cinewright-qc); fixes decoy-2 (T-20261111-1).
- harvest.json: technique-harvest targets (r/aivideo, r/LocalLLaMA, r/Filmmakers, Gemini video docs, arXiv cs.CV).

## 2026-11-11 (0.6.1)

- `aidetect`: tags, C2PA, 32 sampled frame pairs, flow-warp residual, ORB homography, FFT and Laplacian, log-odds score, report.json and contact sheet. Calibrated on 21 generated and 3 phone clips; ai-video-tells records the bands.

## 2026-11-11 (0.6.0)

- New skill: film notation 0.1 and `cine_analyze.py` (probe, shots, frame, pan, scale, notate, rebuild); four entries.
