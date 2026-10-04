# Research: cinewright-movement

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Movement for AI video: weight and contact, one phrase per shot, fights and stunts, and hard subjects (animals, crowds, hands, liquids). Tier `slow`. Last refresh 2026-10-04; next due 2027-02-01.

## Current understanding

- Settled (craft): anticipation, contact, follow-through and settle (Thomas and Johnston 1981; Williams 2001); effort qualities (Laban 1980); one exchange per shot in fights (Katz 1991).
- Settled (AI-specific, field lessons 020 and 021): hard subjects render when few, large and side-on; a far column of animals cannot be drawn; an animal-drawn vehicle from behind gets its order wrong.
- Moving: physics and anatomy keep improving model by model; re-check the hard-subject list at each refresh.
- Unverified: the local resolution figure (1056-1344 px for animals) comes from one local model.

## Open questions

- Which hard subjects have hosted 2026 models fixed? (S8 renders, one per subject)
- Should the HARD-SUBJECT check also look at MWS cards with many named figures?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `animation principles weight follow-through reference <year>`
- `fight choreography for camera film <year>`

Tooling:

- `path:SKILL.md "choreography"` on GitHub code search; skills.sh weekly installs for `motion`
- `https://registry.modelcontextprotocol.io/v0/servers?search=motion`

Practice:

- `AI video horse legs crowd hands fix <month> <year>`
- `site:reddit.com/r/aivideo fight scene consistent`

Testing:

- `video generation physics anatomy benchmark <year>` (VBench-2.0 and successors)
- `path:SKILL.md movement evals`

Best sources (primary first): Thomas and Johnston, The Illusion of Life; Williams, The Animator's Survival Kit; Laban, The Mastery of Movement; Katz, Film Directing Shot by Shot. Noisy: one-off viral clips without settings.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §3 movement row and §7 coherence causes (subject), field lessons 020 and 021 (practice), the competitor study (tooling: no competitor checks crowd framing), and TESTING.md (testing: the diff's HARD-SUBJECT and ONE-ACTION warnings are checkable).
- Track: subject
- Sources: https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation, https://en.wikipedia.org/wiki/Laban_movement_analysis
- Magnitude: n/a (initial)
- Applied: C-20261004-1
