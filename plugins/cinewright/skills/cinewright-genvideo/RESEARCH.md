# Research: cinewright-genvideo

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: AI video model prompting and compiling (Veo, Kling, Seedance, Runway, Luma, Wan, LTX-2, MiniMax H3). Tier `fast`. Last refresh 2026-10-03; next due 2026-10-17.

## Current understanding

- Veo 3.1 (checked 2026-10-03): Vertex GA IDs `veo-3.1-generate-001` and `-fast-` since 2025-11-17, retirement 2026-11-17 or later; Gemini API preview IDs shut down 2026-10-22 with `gemini-omni-1.1-flash` named as replacement. No Veo 4 on any Google page.
- Veo 3.1 numbers: 4/6/8 s, 720p/1080p/4k (1080p, 4k and refs force 8 s), 16:9 or 9:16, 24 fps, 1,024-token prompt cap, up to 3 asset refs, no style refs, seed uint32.
- Veo prompt form: cinematography, subject, action, context, style; audio in its own sentences; timestamp blocks `[00:00-00:02]` for several shots (blog only, not in the docs pages).
- Contested: dialogue syntax. The blog uses quotes, the Gemini API page speaker labels, the prompt guide a colon with no quotes. cinewright uses the prompt-guide form (newest page, updated 2026-10-01).
- Unverified: how to stop burnt-in subtitles. Google documents nothing; community advice is colon dialogue and negative-prompt nouns.

## Open questions

- Which IDs offer 4k on Vertex (GA or preview)? Google's pages disagree.
- Does `negativePrompt` still work on the Gemini API? It is missing from the current page.
- Gemini Omni Flash needs its own card (S2).

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `Veo 3.1 OR "Gemini Omni" video prompt guide changes <month> <year>`
- `Kling OR Seedance OR Runway video model release <month> <year>`

Tooling:

- `path:SKILL.md "video prompt"` on GitHub code search, sorted by recently updated; skills.sh weekly installs for `video prompt`
- `https://registry.modelcontextprotocol.io/v0/servers?search=video generation`
- Supersession sweep: `"video prompt" skill deprecated OR archived <year>`; archive flag on DirectorSKILL and smixs/visual-skills

Practice:

- `"prompt" Veo OR Kling consistency workflow site:reddit.com <month>`
- `site:simonwillison.net OR site:latent.space video model <year>`

Testing:

- `video generation prompt adherence benchmark <year>` (VBench-2.0, VideoScore2)
- `path:SKILL.md veo evals`

Best sources (primary first): Vendor docs and deprecation pages first (ai.google.dev deprecations, Vertex model pages), vendor prompt guides second. Noisy: third-party Veo blogs and 'Veo 4' speculation.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261003-1 · 2026-10-03 · Initial research
- Summary: Veo 3.1 re-checked from Google pages for the model card: IDs and dates, durations, sizes, refs, timestamps, dialogue forms (subject). Tooling: no competitor compiles one card into several models' syntax. Practice: community subtitle workarounds, marked unverified. Testing: compile output is checked by the identity-verbatim guard and by tests.
- Track: subject
- Sources: https://ai.google.dev/gemini-api/docs/veo, https://ai.google.dev/gemini-api/docs/deprecations, https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate, https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Magnitude: n/a (initial)
- Applied: C-20261003-1
