# HANDOFF: video analysis chain scout

Status: ready

Split out of the "Video analysis track" in ai-docs/HANDOFF.md on 2026-11-11. Steps are in the chain prompt.

Done (session 1, 2026-11-11):
- Step 1: plugins/cinewright/skills/cinewright-analyze/harvest.json; private everscout beat `video-analysis` in ~/.everscout/beats (sources probed ok 2026-11-11; beat-check warns: few question seeds, literature unresearched).
- Step 2: evals run once each, 7/8 (TESTS.md T-20261111-1). decoy-2 failed; description tuned to point own-take review at cinewright-qc.

Next:
1. Rerun decoy-2 (3 runs) and confirm the tune; rerun others to 3 runs if budget allows.
2. Step 3: aidetect shipped (0.6.1, #113): add trigger and action cases for `cine_analyze.py aidetect`, run them.
3. Optional: fill the beat's questions.md and vocab.md.

Waiting on Mark: nothing.
