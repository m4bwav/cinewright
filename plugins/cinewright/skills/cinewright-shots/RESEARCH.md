# Research: cinewright-shots

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Shot design for AI video: blocking, coverage, shot lists, framing and grouping shots into generations. Tier `slow`. Last refresh 2026-10-04; next due 2027-02-01.

## Current understanding

- Settled (craft): coverage, blocking, the 30-degree rule and framing conventions (Arijon 1976; Katz 1991; Block 2008; Mascelli 1965).
- Settled (AI-specific): each take costs a generation, so coverage is a cut plan with one escape shot per scene, not every angle; seams belong at changes of place or camera side (field lesson 011).
- Moving: multi-shot generation (Kling 3.0, Seedance 2.5, Veo timestamps) lets one generation hold a shot and its reverse; the longest take per model is on its card.
- Unverified: platform button areas on 9:16 frames vary by app; the OTS drift claim comes from general reports, not a test here.

## Open questions

- Does a clean single beat an OTS single for identity on hosted models with references? (S6 A/B)
- Should `cards list` also print generation groups for a named model?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `shot list coverage storyboard AI video <year>`
- `blocking staging director film <year> book`

Tooling:

- `path:SKILL.md "shot list"` on GitHub code search, sorted by recently updated; skills.sh weekly installs for `storyboard`
- `https://registry.modelcontextprotocol.io/v0/servers?search=storyboard`

Practice:

- `multi-shot generation shot reverse shot Kling Seedance <month> <year>`
- `site:reddit.com/r/aivideo shot list workflow <month>`

Testing:

- `video generation multi-shot consistency benchmark <year>`
- `path:SKILL.md storyboard evals`

Best sources (primary first): Arijon, Grammar of the Film Language; Katz, Film Directing Shot by Shot; Block, The Visual Story; Mercado, The Filmmaker's Eye. Noisy: listicles of shot types with no numbers.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §3 shot-design and direction rows and §4 sources (subject), the competitor study (tooling: no competitor prints a shot list from structured cards), the first local render (practice: one generation held three shots), and TESTING.md (testing: the `cards list` last line is the evidence).
- Track: subject
- Sources: https://en.wikipedia.org/wiki/Shot_list, https://en.wikipedia.org/wiki/Blocking_(stage)
- Magnitude: n/a (initial)
- Applied: C-20261004-1
