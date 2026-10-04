# Handoff

## Current state
- S1 (scaffold and one vertical slice) done on 2026-10-03, on branch `s1/scaffold`, PR waiting for Mark's review. Private repo https://github.com/m4bwav/cinewright.
- Built: marketplace plus three plugin folders with both manifests; `shared/` vocab (4), schemas (8), runtime `cine.py`; maintainer `scripts/cine.py` (kb, cards, compile Veo, continuity diff, budget, zip, build); 29 tests; skills `cinewright`, `cinewright-continuity`, `cinewright-genvideo` (Veo 3.1 stub) as evergreen units; worked example `examples/three-shot/`; manual-dispatch CI. Layout: [../CODEMAP.md](../CODEMAP.md).
- Exit check passed, outputs quoted in [log.md](log.md): example clean plus planted error caught, budget GREEN, `claude plugin validate` passes on the marketplace and each plugin, tests pass on Python 3.14 and 3.9, ZIP for `cinewright-continuity` has the skill folder on top.

## In progress
- Mark's review of the S1 PR. D1-D7 still unanswered; S1 used the recommendations ([decision](decisions/2026-10-03-s1-built-on-the-plan-s-recommendations-for-d1-d7.md)).

## Decisions made this session
- Copies of `shared/` carry a sha256 header; lint regenerates and compares byte for byte ([decision](decisions/2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md)).
- Private render lessons are cited as "field lesson NNN" ([decision](decisions/2026-10-03-field-lessons-cited-without-the-private-source-s-name.md)); the mapping is in the vault sidecar.
- Veo card targets Vertex GA `veo-3.1-generate-001`; dialogue in the prompt-guide colon form; 250-word warning is cinewright's own default.

## Watch
- Veo 3.1 Gemini API preview IDs shut down 2026-10-22 (replacement `gemini-omni-1.1-flash`); Vertex GA IDs retire 2026-11-17 or later. Re-check in S2.
- Model cards sit near the 700-token entry budget (Veo: 695).
- Baselines: without cinewright the router prompt went to a local-render skill (film.json and prompts, no bibles or cards); the continuity outcome was solved by reading files, so that case may be redundant (sharpen in S6).

## Next single action
- After Mark reviews the S1 PR, run [next-session-prompt.md](next-session-prompt.md) (S2: every model card and compiler, qc skill, first local render).
