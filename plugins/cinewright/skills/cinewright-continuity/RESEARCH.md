# Research: cinewright-continuity

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Film continuity (script supervision) applied to AI-generated video. Tier `slow`. Last refresh 2026-10-03; next due 2027-01-31.

## Current understanding

- Settled (craft, decades old): the 180-degree rule, screen direction, the 30-degree rule and matched eyelines decide whether separate shots read as one space (Arijon 1976; Miller 1999).
- Settled (AI-specific, field lessons 005, 011, 012, 013): each generation starts from nothing, so identity, props, direction and sound must be restated verbatim in every prompt; a first frame carries composition, not identity.
- Settled: a verbatim identity string plus reference images is the strongest identity carrier; Veo takes up to 3 asset refs (genvideo card).
- Moving: models with multi-shot generation (Kling, Seedance, Veo timestamps) reduce seam problems; the rules stay, their weight shifts.
- Unverified: the head-trim and audio-overlap numbers in ai-continuity come from one local model; re-check on hosted models in S2.

## Open questions

- Can QC check eyeline and screen direction on rendered frames with a VLM reliably enough to automate? (S2 qc)
- Should key-light side be checked across shot and reverse shot, or is that a DP call (cinewright-camera)?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `script supervisor continuity AI video consistency <year>`
- `180 degree rule AI generated video character consistency <month> <year>`

Tooling:

- `path:SKILL.md "continuity"` on GitHub code search, sorted by recently updated; skills.sh weekly installs for `continuity`
- `https://registry.modelcontextprotocol.io/v0/servers?search=storyboard`
- Supersession sweep: `"continuity" skill deprecated OR archived <year>`; archive flag on DirectorSKILL and smixs/visual-skills

Practice:

- `"character consistency" AI video workflow reference images <year>`
- `site:reddit.com/r/aivideo "same character" shots <month>`

Testing:

- `video generation consistency benchmark identity <year>` (VBench-2.0 and successors)
- `path:SKILL.md continuity evals`

Best sources (primary first): Miller, Script Supervising and Film Continuity; Arijon, Grammar of the Film Language; vendor reference-image docs. Noisy: prompt-pack sellers.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261003-1 · 2026-10-03 · Initial research
- Summary: Built from film continuity practice (subject: Arijon, Miller, Rowlands), four field lessons from the maintainer's local renders (practice), the competitor study (tooling: no competitor ships a scripted continuity diff), and TESTING.md (testing: the diff's summary line is the evidence).
- Track: subject
- Sources: https://en.wikipedia.org/wiki/180-degree_rule, https://en.wikipedia.org/wiki/30-degree_rule
- Magnitude: n/a (initial)
- Applied: C-20261003-1
