# Research: cinewright-curate

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: cinewright knowledge-base upkeep: reference entries and video model cards. Tier `moderate`. Last refresh 2026-10-06; next due 2026-11-05.

## Current understanding

- Settled (repository rules): an entry is one file with six frontmatter fields (`shared/schemas/entry.schema.json`); model cards add `model`, `vendor`, `version`, `status` (current, preview, deprecated, shut-down) and `volatile_claims`. `INDEX.md` and shared-vocab copies are generated and hash-checked by `kb lint`, so hand edits fail CI.
- Settled (evergreen protocol, TESTING.md and MAINTENANCE.md): a claim that moves (price, length, model IDs, shutdown dates) is a volatile claim, re-checked against a primary page before use; a check is recorded with its date and source.
- Settled (cinewright-genvideo): `compile` warns on a deprecated or shut-down card, so a retired card stays in place rather than being deleted; shot lists from before the shutdown still resolve.
- Moving: the genvideo tier is fast (14 days) because video models ship monthly; `kb due` follows each skill's `interval_days`, so the curate cadence moves with it.
- Tooling: chartwright-curate (same author) is the closest pattern: route by ask, change through the CLI, validate, log a `C-` entry. Curate follows it; the difference is that cinewright's CLI writes the date stamps and the retire log itself.

## Open questions

- Should `kb verify` refuse a source that is not already listed or that is not a primary page (vendor docs, standards body)? Today it accepts any URL the maintainer names.
- Does a model card retired as `shut-down` need a removal date after which `compile` refuses it outright?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- the evergreen protocol's MAINTENANCE.md and TESTING.md in the installed plugin (`evergreen.py where`): changes to volatile-claim and verification rules
- `"knowledge base" maintenance "agent skill" verify sources <year>`

Tooling:

- `path:SKILL.md "knowledge base" curate OR upkeep` on GitHub code search, sorted by recently updated
- chartwright-curate and sitewright-curate changelogs (sibling curate skills)

Practice:

- `"model card" OR "model registry" video generation deprecation schedule <year>` (how vendors announce shutdowns; feeds `kb retire`)

Testing:

- `cinewright` evals harness (`evals/run_evals.py`) dead-ends note in ai-docs/solutions; `"agent skill" eval "file evidence" OR trace <year>`

Best sources (primary first): the evergreen protocol files, this repository's schemas and `scripts/cine.py`, vendor deprecation pages linked from each model card.

## Findings log

### R-20261006-1 · 2026-10-06 · Initial research
- Summary: read this session: the entry schema, the evergreen protocol's TESTING.md, chartwright-curate's SKILL.md, and `compile`'s status warning in the runtime. They gave the route table, the rule that a model card stays on retirement, and the evidence (`kb lint` line). No web search: the subject is this repository's own rules; the tooling track found only the sibling curate skills.
- Track: subject, tooling
- Sources: shared/schemas/entry.schema.json, the evergreen protocol's TESTING.md (plugin 0.13.0), chartwright-curate SKILL.md
- Magnitude: n/a (initial)
- Applied: C-20261006-1
