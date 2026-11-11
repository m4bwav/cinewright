# cinewright-analyze tests

- Unit: `tests/test_cine.py` TestAnalyze (scale on the benchmark and synthetic cases, notate, rebuild cards checked against the shot-card schema, synthetic shots and pan; aidetect metadata signals, scoring bands, and a synthetic run that writes report.json and the contact sheet).
- Evals: `evals/evals.json` (3 triggers, 3 decoys, 1 action, 1 outcome).

## T-20261111-1 · 2026-11-11 · first run, 1 run per case

7 of 8 passed: trigger-1/2/3, decoy-1 (went to shots), decoy-3 (no skill), action-1 (`cine_analyze.py scale`, width 6.2 H lower bound), outcome-1 (H unit, width lower bound, depth needs horizon). Failed decoy-2: analyze loaded first, then qc. Tuned: description now names qc for own takes (C-20261111-tune). Rerun decoy-2 next session.
