# cinewright log

## 2026-10-03: research and kickoff prompt

- Mark asked for a researched prompt that plans an evergreen cinematography plugin set (all film roles + AI video coherence; public; Claude Code, Claude Desktop, Copilot; token-lean). His request: `../../prompts/Cinematography Plugin Prompt.md`.
- Four research passes (local prior art, film craft, AI video 2026, cross-host packaging) condensed into [research/2026-10-03-research-brief.md](research/2026-10-03-research-brief.md).
- Name `cinewright` proposed (fits the *wright family; no GitHub repo or search hit on 2026-10-03). Folder holds only ai-docs; no git repo yet. Session 1 creates it.
- Kickoff prompt: [next-session-prompt.md](next-session-prompt.md). It plans and writes the chain; it does not build.
- Findings that shaped the prompt: Sora 2 API closed 2026-09-24; claude.ai ZIPs hold one skill folder, so knowledge sits in each skill's references/; claude.ai rejects Claude Code-only frontmatter keys; the script supervisor (continuity) is the role that matters most for AI video; DirectorSKILL (MIT) and smixs/visual-skills (CC BY 4.0) are the ideas to beat.
- Added brief §12: official listings. Claude directory takes plugin bundles (not bare skills) from paid accounts at claude.ai/directory/manage; awesome-copilot (a default Copilot CLI marketplace) takes skills by PR and external plugins by issue form.

## 2026-10-03: session 1, plan and chain

- Repo set up: git on `main`, everlast doc set (mode repo, sync pr), AGENTS.md, CLAUDE.md importing it, Copilot pointer, private GitHub repo m4bwav/cinewright.
- Four subagent passes: evergreen spec, threewright template and comfyui-gen lessons, packaging re-check, competitor study. Notes: [research/2026-10-03-packaging-verification.md](research/2026-10-03-packaging-verification.md), [research/2026-10-03-competitor-study.md](research/2026-10-03-competitor-study.md).
- Plan written: [plans/PLAN.md](plans/PLAN.md). 13 skills (color and VFX merged into finish), physical plugin folders (core, craft, dev) because strict-false slicing cannot go to the Claude directory, CLI `cine.py`, budgets with thresholds, stages S1-S8, decisions D1-D7 for Mark.
- S1 prompt written to [next-session-prompt.md](next-session-prompt.md).

## [2026-10-03] add | solution: strict false slicing cannot go to the Claude directory
## [2026-10-03] index | rebuilt (3 entries)
## [2026-10-03] add | decision: S1 built on the plan's recommendations for D1-D7
## [2026-10-03] add | decision: Shared sources copied into skills with a hash header
## [2026-10-03] add | decision: Field lessons cited without the private source's name

## 2026-10-03: session S1, scaffold and one vertical slice

- PR #1 was merged with no comments; D1-D7 unanswered, so S1 used the PLAN recommendations ([decision](decisions/2026-10-03-s1-built-on-the-plan-s-recommendations-for-d1-d7.md)). Branch `s1/scaffold` off `main`.
- Three subagent passes: evergreen unit rules (scaffold with `evergreen.py init --pointer`, then `unregister`; there is no `new` command and no flag to skip registration), threewright shape and the private render lessons, a Veo 3.1 re-check from Google pages.
- Veo finding that matters: Gemini API `veo-3.1-*-preview` IDs shut down 2026-10-22 (replacement `gemini-omni-1.1-flash`, GA 2026-08-27); Vertex GA `veo-3.1-generate-001` retires 2026-11-17 or later; no Veo 4. Google gives no word count, only a 1,024-token cap; the dialogue form differs across its three pages (card uses the prompt guide's colon form). Card: `plugins/cinewright/skills/cinewright-genvideo/references/veo-3-1.md`.
- Built: layout per PLAN §3, `shared/` (4 vocab entries, 8 schemas, runtime `cine.py`), maintainer `scripts/cine.py`, 29 tests, three skills as evergreen units, worked example, CI. Copies carry sha256 headers and lint compares them byte for byte ([decision](decisions/2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md)). Private lessons cited as "field lesson NNN" ([decision](decisions/2026-10-03-field-lessons-cited-without-the-private-source-s-name.md)).
- Bugs the first runs caught and fixed: `compile --sequence` described only the first card's cast (the identity-verbatim guard stopped it: genvideo L-001); frontmatter lists kept quotes on items after a comma; `kb search` listed one vocab copy per skill.
- Budget went yellow once (Veo card 906 est. tokens against 700); the card was cut to 695 instead of moving the line. Model cards will sit near that line in S2.
- CI (D6): no self-hosted runner is registered for this repo (`gh api repos/m4bwav/cinewright/actions/runners` returned 0), so `.github/workflows/ci.yml` is `workflow_dispatch` only on `runs-on: [self-hosted]`, and every check below ran locally.
- Baselines (action prompts, Sonnet, headless, bare folders without cinewright): the film-planning prompt went to a local-render skill and wrote a film.json and three prompt files, no bibles, cards or check; the continuity prompt read every file and found the axis error, helped by a note in the planted card that announced it (note removed); the compile prompt searched the disk for a compiler and ran out of 20 turns with no prompt written. Recorded in each skill's evals.json and TESTS.md.

Exit check output (2026-10-03, Windows 11, Python 3.14.6 and 3.9.25, Claude Code 2.1.281):

```
$ python -m unittest discover -s tests
Ran 29 tests in 3.578s
OK
$ py -V:Astral/CPython3.9.25 -m unittest discover -s tests
Ran 29 tests in 3.854s
OK
$ python scripts/cine.py cards validate examples/three-shot
cards validate: 3 cards, 0 errors
$ python scripts/cine.py continuity diff examples/three-shot
continuity diff: 3 cards, 0 errors, 0 warnings
$ python scripts/cine.py continuity diff examples/three-shot --with examples/three-shot/planted/1C.json
ERROR 1C AXIS: camera is on side B of the 1 axis (between Maren and Tomas, across the lens): it crosses the line, so every left and right flips. Move it to side A, or set crosses_axis with a cross_reason (a neutral shot or a move seen on screen).
ERROR 1C EYELINE: Tomas looks frame-left at Maren; from side B the eyeline must be frame-right
continuity diff: 3 cards, 2 errors, 0 warnings
$ python scripts/cine.py compile examples/three-shot --model veo --out examples/three-shot/compiled/veo
== 1A  veo-3.1-generate-001  6s 16:9 720p  185 words
== 1B  veo-3.1-generate-001  4s 16:9 720p  142 words
== 1C  veo-3.1-generate-001  4s 16:9 720p  131 words
wrote 3 prompts to examples/three-shot/compiled/veo (model card veo-3-1.md, last_checked 2026-10-03)
$ python scripts/cine.py kb lint
kb lint: 3 skills, 0 errors
$ python scripts/cine.py budget
budget: GREEN (tokens are bytes / 4, an estimate)   [every row green; worst: Veo card 695/700 est. tokens]
$ claude plugin validate .            -> Validating marketplace manifest ... ✔ Validation passed
$ claude plugin validate plugins/cinewright        -> ✔ Validation passed
$ claude plugin validate plugins/cinewright-craft  -> ✔ Validation passed
$ claude plugin validate plugins/cinewright-dev    -> ✔ Validation passed
$ python scripts/cine.py zip cinewright-continuity
wrote ...\dist\cinewright-continuity.zip: 25 files, 38 KB, top folder cinewright-continuity/
$ evergreen.py lint <each skill>
cinewright: lint OK / cinewright-continuity: lint OK / cinewright-genvideo: lint OK
```
