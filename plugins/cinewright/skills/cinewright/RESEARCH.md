# Research: cinewright

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: AI filmmaking pipeline: directing, producing and routing an idea to a delivered AI-generated film. Tier `moderate`. Last refresh 2026-10-03; next due 2026-11-02.

## Current understanding

- Settled: generated clips drift because each is generated alone; a written pipeline where each stage writes a file the next stage reads is the fix every serious tool converges on (PLAN.md research brief, 2026-10-03).
- Settled: shots of 3-8 s with one subject, one action and one camera move are the unit hosted and local models follow best; Veo offers 4/6/8 s per generation.
- Settled: several shots inside one generation (timestamp blocks) hide seams better than separate clips cut together.
- Moving: hosted models change monthly (Sora 2 API closed 2026-09-24; Veo 3.1 Gemini API previews shut down 2026-10-22). The router must not hard-code a model; genvideo owns model cards.
- Contested: how much a planning layer improves a finished film. S8 measures it with a blind A/B; until then the claim is unproven.

## Open questions

- Does the router trigger on casual requests ("make me a video about X") without stealing plain video-editing requests? Test in S6.
- Is a brief.md stage worth its tokens, or should beats live in the style bible?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `AI short film workflow shot list consistency <year>`
- `AI filmmaking pipeline storyboard to video model <month> <year>`

Tooling:

- `path:SKILL.md "film director"` on GitHub code search, sorted by recently updated; skills.sh weekly installs for `film director`
- `https://registry.modelcontextprotocol.io/v0/servers?search=video`
- Supersession sweep: `"film director" skill deprecated OR archived <year>`; archive flag on DirectorSKILL and smixs/visual-skills

Practice:

- `"how I made" AI short film Veo OR Kling workflow <year>`
- `site:reddit.com/r/aivideo workflow consistency <month>`

Testing:

- `AI video planning evaluation shot list benchmark <year>`
- `path:SKILL.md video evals`

Best sources (primary first): Google Veo prompt guide, vendor docs per model, Katz and Murch for craft. Noisy: listicles of "best AI video tools".

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261003-1 · 2026-10-03 · Initial research
- Summary: Built the router from PLAN.md and the 2026-10-03 research brief (subject), the packaging check (tooling: physical plugin folders, six frontmatter keys), the competitor study (practice: no competitor ships an executable compiler or continuity diff), and TESTING.md (testing: evidence outside the transcript).
- Track: subject
- Sources: https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1, https://code.claude.com/docs/en/plugins/marketplace-reference
- Magnitude: n/a (initial)
- Applied: C-20261003-1
