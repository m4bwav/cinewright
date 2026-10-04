# Research: cinewright-script

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Screenwriting for short AI video: logline, beats, scene turns, screenplay format and dialogue for generated voices. Tier `slow`. Last refresh 2026-10-04; next due 2027-02-01.

## Current understanding

- Settled (craft): logline form, beat structure, one value turn per scene, screenplay format and page timing (Snyder 2005; Field 2005; McKee 1997; Riley 2021).
- Settled (AI-specific): a turn spread over several separately generated shots reads as no turn; put it in one shot.
- Moving: native dialogue in Veo 3.1, Kling 3.0, Seedance 2.5, MiniMax H3 and LTX-2; voice strings and tone tags differ by model (genvideo cards).
- Unverified: 2.5 words a second is a conversational English rate; how each model rushes or pads lines is a field observation, not measured per model.

## Open questions

- Measure spoken words per second per model on the same line (S8 renders).
- Do non-English lines need a lower words-per-second limit?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `short film screenplay structure beats <year>`
- `logline formula screenwriting <year>`

Tooling:

- `path:SKILL.md "screenplay"` on GitHub code search; skills.sh weekly installs for `screenwriting`
- `https://registry.modelcontextprotocol.io/v0/servers?search=screenplay`

Practice:

- `AI video dialogue lip sync words per second <month> <year>`
- `site:reddit.com/r/aivideo dialogue too long cut off`

Testing:

- `speech rate words per minute conversational study`
- `path:SKILL.md screenplay evals`

Best sources (primary first): McKee, Story; Snyder, Save the Cat!; Field, Screenplay; Riley, The Hollywood Standard; fountain.io syntax. Noisy: logline generators.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §3 story row and §4 sources (subject), vendor dialogue guides on the genvideo cards (practice), the competitor study (tooling: competitors write scripts as prose with no length check), and TESTING.md (testing: the diff's DIALOGUE warning is the checkable part).
- Track: subject
- Sources: https://fountain.io/syntax, https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Magnitude: n/a (initial)
- Applied: C-20261004-1
