# Research: cinewright-camera

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Cinematography and lighting for AI video: lens choice, depth of field, exposure, frame rate and shutter, aspect and framing, anamorphic, lighting ratios and setups, color temperature. Tier `slow`. Last refresh 2026-10-04; next due 2027-02-01.

## Current understanding

- Settled (craft): focal-length bands, 180-degree shutter (1/48 s at 24 fps), key-to-fill ratios, portrait setups, color temperatures (Brown 2016, 2018; ASC Manual 2022; RED shutter tutorial; Wikipedia color temperature).
- Settled (dates): Academy 1932, 1.85 in 1953, 2.35 by SMPTE in 1957, 2.39 from 1970 (Wikipedia aspect ratio, checked 2026-10-04).
- Settled (runtime, 2026-10-04): the render aspect stays a size the model offers; `frame_aspect` adds a composition sentence and finishing crops; the lighting string compiles verbatim under a guard.
- Unverified: how far models follow mm numbers, depth words, ratio words, shutter words and the composition sentence; each is marked in its entry.

## Open questions

- Does the 2.39 composition sentence keep heads inside the crop on hosted models? Check on the first render with a frame_aspect.
- Do kelvin numbers help or print as text on any model?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `cinematography lighting ratio technique <year>`
- `ASC American Cinematographer lens choice <year>`

Tooling:

- `path:SKILL.md "cinematography"` on GitHub code search; skills.sh weekly installs for `cinematography`
- `https://registry.modelcontextprotocol.io/v0/servers?search=cinematography`

Practice:

- `AI video prompt lens depth of field lighting <month> <year>`
- `video model aspect ratio 2.39 widescreen prompt <year>`

Testing:

- `camera control evaluation video generation benchmark <year>`
- `path:SKILL.md lighting evals`

Best sources (primary first): ASC Manual; Brown, Cinematography and Motion Picture and Video Lighting; American Cinematographer; vendor prompt guides for each model. Noisy: prompt packs listing camera words without tests.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §3 cinematography and lighting rows (subject), the RED shutter tutorial and Wikipedia pages on aspect ratio, color temperature and anamorphic format (checked this session), the S2 render's prompts (practice: the look string is the only style carrier, so new style fields join it), and TESTING.md (testing: verbatim guard and LENS and MOVE warnings are checkable).
- Track: subject
- Sources: https://www.reddigitalcinema.com/red-101/shutter-angle-tutorial, https://en.wikipedia.org/wiki/Aspect_ratio_(image), https://en.wikipedia.org/wiki/Color_temperature, https://en.wikipedia.org/wiki/Anamorphic_format
- Magnitude: n/a (initial)
- Applied: C-20261004-1
