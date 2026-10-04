# Research: cinewright-design

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Production and costume design for AI video: turnaround sheets, clean references, prop constants, costume arc and color script. Tier `slow`. Last refresh 2026-10-04; next due 2027-02-01.

## Current understanding

- Settled (craft): color scripts, costume arcs, breakdown stages, silhouette readability and period props (LoBrutto 2002; Landis 2012; Block 2008).
- Settled (AI-specific, field lessons 017 and 019): one turnaround sheet holds identity across views; a reference image outranks the text, so every mark on it is copied.
- Settled (first local render, 2026-10-03): a prop named by one word was drawn differently (cardboard, not tin); a fixed description fixes the look across shots.
- Unverified: the 1%-of-width figure for copied marks is a rule of thumb from local renders.

## Open questions

- Do hosted models (Veo ingredients, Kling elements) copy reference marks as strongly as the local model did?
- Should props.json carry per-scene state (new, burnt, broken) like wardrobe does?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `production design color script film <year>`
- `costume design breakdown continuity <year>`

Tooling:

- `path:SKILL.md "turnaround"` on GitHub code search; skills.sh weekly installs for `character design`
- `https://registry.modelcontextprotocol.io/v0/servers?search=character%20sheet`

Practice:

- `character turnaround sheet consistent AI video reference <month> <year>`
- `reference image logo copied video model <year>`

Testing:

- `subject consistency reference image video benchmark <year>`
- `path:SKILL.md character design evals`

Best sources (primary first): LoBrutto, The Filmmaker's Guide to Production Design; Landis, Costume Design; Block, The Visual Story; vendor reference-image docs. Noisy: prompt packs for character sheets.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §3 production design and costume rows (subject), field lessons 017 and 019 and the first local render's prop drift (practice), the competitor study (tooling: no competitor keeps prop descriptions as data), and TESTING.md (testing: the prompt-verbatim guard and the PROP warning are checkable).
- Track: subject
- Sources: https://en.wikipedia.org/wiki/Production_designer, https://en.wikipedia.org/wiki/Model_sheet
- Magnitude: n/a (initial)
- Applied: C-20261004-1
