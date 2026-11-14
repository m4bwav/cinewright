# Research: cinewright-edit

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Film editing for AI video: assembly from takes, Murch's rule of six, J and L cuts, match cuts, cutting on action, pacing and average shot length, cutting around bad frames, cutting a battle, conform with ffmpeg. Tier `slow`. Last refresh 2026-10-04; next due 2027-02-01.

## Current understanding

- Settled (craft): the rule of six and its order (Murch 2001), split edits, match cuts, cutting on action, a re-establishing wide in battle cutting (Katz 1991, Dancyger 2019, Reisz and Millar 1968).
- Settled (runtime, 2026-10-04): a multi-shot generation's internal cuts are found by ffmpeg scene detection; a frame-accurate conform needs a re-encode (trim, atrim, concat), never stream copy.
- Approximate: average shot length figures by period (Bordwell 2006), not checked against a shot database this session.
- Unverified: how long generated clips take to settle at the head across models (0.1-0.5 s is practice, from one local model).

## Open questions

- Do hosted models (Veo, Kling) show head settle frames, and how many?
- Is a J or L cut worth cutting a multi-shot generation apart for, or do models' own cuts already carry dialogue well?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `film editing technique cutting on action pacing <year>`
- `Murch rule of six editing <year>`

Tooling:

- `path:SKILL.md "video editing"` on GitHub code search; skills.sh weekly installs for `video editing`
- `https://registry.modelcontextprotocol.io/v0/servers?search=video%20editing`

Practice:

- `AI video editing generated clips cut <month> <year>`
- `ffmpeg scene detection trim concat frame accurate <year>`

Testing:

- `automatic video editing evaluation benchmark <year>`
- `path:SKILL.md editing evals`

Best sources (primary first): Murch, In the Blink of an Eye; Dancyger, The Technique of Film and Video Editing; Reisz and Millar; the ffmpeg filter documentation. Noisy: listicles of transition types without reasons.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261114-1 · 2026-11-14 · Time-pressure tags (Sculpting in Time)
- Summary: New entry: still/flowing/rushing tag per shot, flag fast cuts of still frames, regenerate a shot that will not cut. Long takes marked partly applicable to 5-15 s clips. Motion-measure script skipped. Book rules, unverified.
- Track: subject
- Sources: Andrey Tarkovsky, Sculpting in Time, 1986, ch. I and V (paraphrased; no text copied)
- Magnitude: 0.1
- Applied: C-20261114-1

### R-20261113-2 · 2026-11-13 · Early pick-up of a move as a tension beside cut-on-action (Murch)
- Summary: One line: an early pick-up from a new angle can jar, to be judged by watching, not a rule. Book view, unverified.
- Track: subject
- Sources: Walter Murch, Suddenly Something Clicked, 2025 (paraphrased; no text copied)
- Magnitude: 0.1
- Applied: C-20261113-2

### R-20261113-1 · 2026-11-13 · Draft cut review: structure map and draft-cut failures (Documentary Storytelling)
- Summary: New entry draft-cut-review: a structure map (section times, loudness peaks, cut times, train start) and the draft-cut failure list. The map was tried on one 148 s local cut and flagged real faults (transit as loud as the crash, even cut rhythm, train at 30 percent); failure list is book rule, unverified.
- Track: subject
- Sources: Sheila Curran Bernard, Documentary Storytelling, 5th ed. (paraphrased; no text copied)
- Magnitude: 0.2
- Applied: C-20261113-1

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §3 editing row (subject: Murch's six with his weights, J and L cuts, match and smash cuts, cut on action, average shot length), the ffmpeg filter documentation (tooling: trim, atrim, concat, scene detection; checked this session), the S5 exit check on the S2 render (practice: internal cuts at 6.000 s and 10.458 s, 336 frames conformed to 14.000 s), and TESTING.md (testing: a cut list file and a conform whose length matches it are checkable evidence).
- Track: subject
- Sources: https://ffmpeg.org/ffmpeg-filters.html
- Magnitude: n/a (initial)
- Applied: C-20261004-1
