---
title: cinewright plan
date: 2026-10-03
kind: plan
status: active
summary: Skill set, plugin slices, knowledge layout, scripts, size budgets, tiers, proof, installs, stages S1-S8 and the decisions Mark owns.
tags: [plan, cinewright, stages, budgets]
---

# cinewright plan

Read this before any cinewright build session. It settles what gets built and in what order. Inputs: [research brief](../research/2026-10-03-research-brief.md), [packaging check](../research/2026-10-03-packaging-verification.md), [competitor study](../research/2026-10-03-competitor-study.md).

Contents: 1 Goal and default pipeline · 2 Skill set · 3 Plugin slices and layout · 4 Where the knowledge lives · 5 Scripts · 6 Size budgets · 7 Evergreen tiers · 8 Proof · 9 Install proof · 10 Stages · 11 Decisions for Mark · 12 Risks

## 1. Goal and default pipeline

Generated clips come out random because each clip is generated alone and nothing carries identity, wardrobe, props, eyelines, screen direction or light between them. cinewright makes the agent plan like a film crew and check like a script supervisor, then hand each shot to whatever renders it.

One default pipeline, run by the router: idea → logline and beats → script → shot list (one subject, one action, one camera move, 3-8 s per shot) → bibles (style, characters, locations, axis per scene) → reference sheets and keyframes → image-to-video per shot → QC → edit → grade → mix → deliver. Every stage writes a file; the next stage reads that file, not the chat.

The core artifact is the **shot card**: one generator-neutral JSON record per shot. A compiler turns a card plus the bibles into a given model's prompt. The continuity diff checks cards against the bibles before anything renders, and QC checks rendered clips against the card after.

What no competitor has ([study](../research/2026-10-03-competitor-study.md)): an executable compiler from one card to each model's syntax, a continuity diff script, scripted QC, summary indexes, budgets in CI, per-card freshness, scored evals on three model sizes, and installs on all three hosts. Their minimum load per prompt is 2k-22k tokens; cinewright's target is under 5k for a typical task (§6). Borrowed ideas (MIT sources, credited in README): response-size ceilings and the repair cost ladder (prompt → parameter → regenerate → keyframe → v2v → re-plan → fix in edit → cut), one owning reference per dimension, a continuation needs the previous take's observed end state, one change per reroll, writing a prompt never authorises a paid render. The shot card is designed from film practice, so nothing from visual-skills (CC BY 4.0) needs adapting.

Lessons this design exists to prevent (field lessons from the maintainer's local renders, which have no code names, so cited by title): L-005 chained clips lose identity; L-010 reference images keep characters on-model; L-011 independent shots read as the scene restarting; L-012 fixed screen direction string; L-013 describe what is in the shot, not what to avoid; L-014 same seed keeps the opening; L-015 guide frame at frame 0; L-017 turnaround sheets hold identity; L-019 clean references of emblems; L-020 and L-021 hard subjects side-on, few and large. Each becomes a rule in continuity, genvideo or qc, written without the private project context.

## 2. Skill set

Merged from the 15-skill draft by trigger overlap and listing cost (every description is paid on every session, §6). 13 skills (14 since cinewright-voice, 2026-10-07):

| Skill | Covers | Slice |
|---|---|---|
| `cinewright` | director and router: pipeline, which skill next, producing and delivery specs, project folder layout | core |
| `cinewright-continuity` | script supervisor: bibles, identity strings, axis and screen direction, 30-degree rule, eyelines, per-shot checklist, continuity diff | core |
| `cinewright-shots` | storyboard, blocking, coverage, shot list, shot sizes and angles, camera moves (as vocabulary) | core |
| `cinewright-genvideo` | model cards, prompt compiling per model, references and keyframes, seeds and takes, failure taxonomy (symptom → cause → cheapest fix) | core |
| `cinewright-qc` | frame sampling, contact sheets, rubric, VLM judging, spec checks, routing failures to fixes, three-strikes re-plan | core |
| `cinewright-script` | logline, beats, structure, scene turns, screenplay format, dialogue for generated voices | craft |
| `cinewright-camera` | DP and gaffer: lens, depth of field, exposure, frame rate and shutter, aspect, lighting ratios and setups, color temperature | craft |
| `cinewright-design` | production design, sets, props, locations, period, costume, hair and makeup, character and turnaround sheets | craft |
| `cinewright-movement` | choreography, stunts, fights, large battles (map, sides, phases, scale), crowds, animals, physics that models get wrong | craft |
| `cinewright-edit` | cutting: Murch's six, J and L cuts, match cuts, pacing, cutting around bad frames, assembly to delivery | craft |
| `cinewright-finish` | color (correct, balance, match, look; color spaces) and VFX (compositing, cleanup, upscale, interpolation, crowd multiplication for battle wides, the crop to `frame_aspect`) | craft |
| `cinewright-sound` | sound design, foley, ambience, music, dialogue, stems, mix, loudness targets, battle layers (implied mass, distance, weapons) | craft |
| `cinewright-voice` | voice sheets, designed or cloned character voices locked by reference clips, video-model voices and lip-sync, voice conversion, drift checks, rights (added 2026-10-07, after S7) | craft |
| `cinewright-history` | movements, eras, genres, director and DP style cards | craft |
| `cinewright-curate` | knowledge base upkeep: add, verify, retire entries; refresh model cards | dev |

Merges and why: color and VFX share triggers ("fix the shot", "upscale", "grade") and both act on rendered frames, so one `finish` skill. Producing folds into the router (brief). Kept apart: `shots` (what to shoot and in what order) from `camera` (how it is photographed), because shots is needed in the core pipeline and camera is not. S1 measures each description against the §6 budget; if `shots` and `continuity` overlap on trigger tests, merge them in S6.

Cross-skill links name the skill ("see cinewright-camera, entry lens-choice"), never a path, so a skill installed alone degrades to "install cinewright-craft for this" instead of a broken link.

## 3. Plugin slices and layout

The anthropics/skills pattern (one `skills/` tree, `strict: false` slices) cannot go to the Claude directory, which takes one plugin per submission with its own `.claude-plugin/plugin.json` ([packaging check](../research/2026-10-03-packaging-verification.md)). So the slices are physical folders:

```
.claude-plugin/marketplace.json      lists ./plugins/cinewright and ./plugins/cinewright-craft
plugins/cinewright/                  core: 5 skills
  .claude-plugin/plugin.json         Claude manifest (name, version, description, author, license)
  plugin.json                        Agent Plugins 1.0 ($schema, name) for VS Code and other hosts
  README.md  LICENSE
  skills/<name>/...
plugins/cinewright-craft/            8 skills, same shape
plugins/cinewright-dev/              curate; in the marketplace, never submitted to directories
shared/                              single source: vocab/, schemas/, lib/ (see §4)
scripts/cine.py                      maintainer CLI (build, lint, budgets, zip); not shipped
evals/                               cross-skill and A/B harness (A/B data stays private)
ai-docs/                             this doc set
```

- Craft depends on core in its README, not in a manifest (no cross-plugin dependency mechanism found).
- No top-level `bin/` anywhere (claude.ai refuses the plugin). No symlinks (directory rule).
- The CLI name is `cine.py`, not `cw.py`, because chartwright already ships `cw.py`.
- Root-level Agent Plugins `plugin.json` asked for in the kickoff becomes one per plugin folder, since the root is a marketplace, not a plugin.

## 4. Where the knowledge lives

- Each skill: `SKILL.md` (router to its references), `references/INDEX.md` (generated), `references/<slug>.md` one entry per file, `scripts/` (copied from `shared/lib`), evergreen companions. A claude.ai ZIP of one skill folder then works alone.
- Entry frontmatter (six fields, schema in `shared/schemas/entry.schema.json`): `title`, `slug` (= file name), `summary` (200 characters or fewer, becomes the index line), `tags`, `last_checked`, `sources` (URLs; books as author, title, edition). Model cards add `model`, `vendor`, `version`, `status` (current, deprecated, shut down). Sections: Rules, Numbers, Vocabulary, Pitfalls, Verify, Notes (dated lines). No prose the model already knows.
- `SKILL.md` says: read `references/INDEX.md` once, then `cine.py kb show <slug> --section <name>`; never read the folder.
- Shared vocabulary (shot sizes, moves, lenses, lighting terms, screen-direction strings) lives once in `shared/vocab/*.md`. `cine.py build` copies the entries each skill declares in `skills/<name>/needs.json` into `references/` with a header line `<!-- copied from shared/vocab/<file> sha256:<hash>; edit the source -->`. Copies are committed, so a git install needs no build.
- Drift: `cine.py lint` recomputes each copy's hash; a mismatch, a hand edit, or a source change without a rebuild fails lint and CI.
- History cards follow brief §5: about 60 tokens each, tags not prose, one reference film with timestamp.
- Anything from smixs/visual-skills (CC BY 4.0) carries an attribution line in the entry's sources and a NOTICE file in the plugin. DirectorSKILL (MIT): ideas only; credit in README.

## 5. Scripts

Python 3.9+, stdlib only, `encoding="utf-8"`, pathlib, argv lists, LF endings (evergreen PORTABILITY). The skill copies are run, never read. One entry point per skill: `scripts/cine.py <group> <command>`.

| Group | Commands | Stage |
|---|---|---|
| `kb` | `index`, `search <words>`, `show <slug> [--section]`, `lint` | S1 |
| `cards` | `new`, `validate` (shot list and bibles against `shared/schemas/`), `export --film-json` (a local ComfyUI film runner's `film.json` shape: name, target_seconds, width, height, refs, seam_audio_xfade, shots with name, seed, length, refs, guides; written from the documented shape, no import of the runner) | S1 |
| `compile` | `<card> --model veo|kling|seedance|runway|luma|minimax-h3|wan|ltx2`: card + bibles → that model's prompt text, using the model card's template, word limit and syntax (Veo timestamps, Kling `Name (tone):` dialogue, Seedance `@Image1`, H3 in-sentence moves) | S1 one model, S2 all |
| `continuity` | `diff`: every card against the bibles (identity string verbatim, wardrobe and props, axis side and screen direction, 30-degree and size step against the previous card, time of day and sun direction) | S1 |
| `qc` | `sheet` (ffmpeg frames at 1-2 fps → contact sheet), `spec` (ffprobe fps, size, aspect, duration vs card), `loud` (ffmpeg `ebur128` integrated LUFS and true peak vs target), `rubric` (writes the VLM checklist for a clip, reads verdicts back, maps fails to fix codes) | S2 |
| `takes` | `log` (seed, model, verdict, fix code per take: one record shape for every model), `lastframe` (ffmpeg last frame + observed end state for the next card) | S2 |
| `budget` | duplicates across skills that are not hash-tracked copies, lines, characters and estimated tokens per file, description totals, folder and ZIP sizes; green, yellow, red (§6) | S1 |
| `zip` | one claude.ai ZIP per skill, skill folder at the top level, six frontmatter keys checked | S1 |

ffmpeg is the only outside dependency (qc only); the qc skill gets a SETUP.md. Token estimate is bytes ÷ 4, calibrated once in S1 against the free token-counting endpoint if Mark allows an API key (decision D7), else left as an estimate and labelled so.

## 6. Size budgets

Measured by `cine.py budget`; CI fails at red; at yellow the session tells Mark in one line before going on.

| Measure | Green | Yellow | Red |
|---|---|---|---|
| SKILL.md lines | ≤ 80 | 81-120 | > 120 |
| SKILL.md body tokens (est.) | ≤ 1,200 | 1,201-2,000 | > 2,000 |
| One description, characters (trigger words first) | ≤ 350 | 351-500 | > 500 |
| All descriptions, characters (all skills) | ≤ 4,000 | 4,001-5,500 | > 5,500 |
| Core descriptions only (5 skills) | ≤ 1,800 | 1,801-2,500 | > 2,500 |
| Reference entry lines | ≤ 60 | 61-100 | > 100 |
| Reference entry tokens (est.) | ≤ 700 | 701-1,200 | > 1,200 |
| Model card tokens (est.), Compile block included (entries with `model`) | ≤ 900 | 901-1,200 | > 1,200 |
| `references/INDEX.md` tokens per skill | ≤ 1,500 | 1,501-3,000 | > 3,000 |
| Skill folder size, without the hash-tracked `shared/lib/` copies | ≤ 150 KB | 151-300 KB | > 300 KB |
| Runtime (`shared/lib/`), measured once (decision 2026-10-04, accepted by Mark 2026-10-06) | ≤ 100 KB | 101-150 KB | > 150 KB |
| Files per plugin (directory cap 512) | ≤ 350 | 351-450 | > 450 |
| Repo ZIP (`git archive`) | ≤ 2 MB | 2-5 MB | > 5 MB |

The all-description cap is set so cinewright's whole listing stays under about 1,000 tokens, half of a 200k-context listing budget (1%), because users have other skills installed. Typical task load target: router SKILL.md + one other SKILL.md + one index + two entries ≤ 5,000 tokens.

## 7. Evergreen tiers

| Skill | Tier | Why |
|---|---|---|
| genvideo | fast (14 d start), `verify_at_use` on the model card used; each card has `last_checked` and a `volatile_claims` list | models ship monthly; Sora 2 closed 2026-09-24 |
| qc | moderate | judges and benchmarks move (VBench-2.0, VideoScore2) |
| sound, finish | moderate | loudness and color standards plus delivery specs |
| cinewright (router) | moderate | host packaging and pipeline practice |
| continuity, shots, camera, edit, script, design, movement | slow | craft changes slowly; AI-specific rules inside them get dated Notes |
| history | glacial | |
| curate | moderate | follows the protocol and tooling |

Every skill gets RESEARCH (four tracks: subject, tooling, practice, testing), CHANGELOG, LEARNINGS, TESTS, `evergreen.json` (fields per `evergreen.py new_state`), `evals/evals.json`. SETUP.md for qc (ffmpeg) and genvideo (whatever renderer the user names: a hosted API key or a local server, recorded as `optional` needs).

## 8. Proof that it works

- **Evals per TESTING.md**, every skill: 2 triggers, 2 decoys, 1 action case with evidence outside the transcript (a written shot list, a `cine.py` call in the trace, a contact sheet file), 1 outcome case, baseline without the skill. Three runs each; trigger ≥ 2/3, decoy 0/3. Run on Haiku, Sonnet and Opus (TESTING has no model matrix; cinewright adds one and records the model per T- entry). Harness: `claude plugin eval` plus `claude -p --plugin-dir` headless cases, as threewright does.
- **Outcome rubric** for a planned film (no render needed): every card validates, continuity diff clean, one action and one move per card, identity string verbatim in every compiled prompt, screen direction stated, durations 3-8 s. Scored with and without cinewright on the same one-line idea.
- **Real A/B (S8, private):** one one-line film idea, rendered through the maintainer's local renderer (ComfyUI, MiniMax H3) twice: a plain prompt-per-shot run, and the cinewright pipeline. Same seeds where possible, same shot count. Scored blind by the qc rubric plus Mark's own ranking. Data, renders and the report live in the vault sidecar, never in this repo; the public README may state the result in one sentence.

## 9. Install proof (S7)

| Host | Route | Status |
|---|---|---|
| Claude Code | `/plugin marketplace add m4bwav/cinewright`, `/plugin install cinewright@cinewright` | installed and triggered, private repo, Windows, 2026-10-06; public repo 2026-10-07 |
| claude.ai / Desktop | Customize > Plugins > Add marketplace | 2026-10-07: installed (0.1.0, 5 skills) and triggered; the skill's `cine.py` calls failed (folder guessed wrong, L-006 in continuity). Trigger PASS, scripts FAIL |
| claude.ai | Customize > Skills > upload one ZIP per skill | 2026-10-07: `cinewright-continuity.zip` from the v0.1.0 release uploaded and triggered, Step 0 ran. PASS |
| Copilot CLI | `copilot plugin marketplace add m4bwav/cinewright` (reads `.claude-plugin/`) | installed and triggered, private repo, Windows, 2026-10-06; public repo 2026-10-07 |
| VS Code Copilot | `chat.plugins.marketplaces` or "Chat: Install Plugin From Source" | 2026-10-07: settings set, installed into `~/.copilot/installed-plugins/` with the Copilot CLI, `code chat` called the skill. PASS (UI Install button not exercised) |
| any agent | `gh skill install m4bwav/cinewright cinewright-continuity` | nested discovery works (13 skills); installed and triggered in Claude Code, 2026-10-06; public repo 2026-10-07 |

Each route is run once on Windows; one route on a second OS or `untested elsewhere` in TESTS. Results: [../notes/2026-10-06-s7-install-proof.md](../notes/2026-10-06-s7-install-proof.md). The repo is private until S7, so public-route tests run right after the scrub, before announcing. Claude directory and awesome-copilot submissions come after release (brief §12).

## 10. Stages

Estimates are agent time and output size. Each stage writes the next stage's full prompt (chain rule).

**S1. Scaffold and one vertical slice.** Layout from §3; `shared/schemas/` (entry, shot card, bibles, model card); `cine.py` groups kb, cards, compile (Veo only, the best documented model), continuity, budget, zip; tests for each command; CI workflow; skills `cinewright` and `cinewright-continuity` complete with companions and evals; one model card (Veo 3.1) in genvideo as a stub skill; marketplace and both manifests; README stub; MIT LICENSE once D2 is answered. Exit: a three-shot example idea goes through router → shot cards → bibles → continuity diff (clean, plus one planted error caught) → compiled Veo prompts; `cine.py budget` green; `claude plugin validate .` passes; tests pass. Size: about 45 files, 2,500 lines, 3-4 agent hours.

**S2. genvideo and qc.** Model cards for Veo, Kling, Seedance, Runway, Luma, MiniMax H3, Wan, LTX-2, each re-verified from vendor docs; compiler for all eight; failure taxonomy (about 20 codes, symptom → cause → cheapest fix, mapped to qc rubric items); qc scripts and SETUP.md (ffmpeg); first real render: the S1 example through local H3, contact sheet, rubric, one fix loop. Exit: compile output for every model checked against its vendor's own examples; qc runs on a real clip; one failure routed to a fix and re-rendered. Size: about 50 files, 3,000 lines, 4-5 agent hours.

**S3. Pre-production craft.** script, shots, design, movement: references from the brief's §3 rules and §4 sources, AI-specific rules (L-017 turnarounds, L-019 clean references, L-020 and L-021 hard subjects). Exit: the example idea planned end to end with every skill used once; budgets green. About 70 files, 3 agent hours.

**S4. Camera, lighting and history.** camera references (lens, DoF, exposure, fps and shutter, aspect, lighting ratios, setups, color temperature), history cards (12 movements, 8 eras, 10 genres, about 40 directors and DPs). Exit: "shoot it like 1970s New Hollywood, 2.39" changes the compiled prompts in checkable ways. About 90 files, 3 agent hours.

**S5. Post.** edit, finish, sound: Murch, J and L cuts, cutting around bad frames, cutting a battle (geography wides between fights), crowd multiplication in compositing and battle sound layers (asked for on 2026-10-04; movement's battle-scenes entry plans the shoot), the crop to `frame_aspect`, grade order and color spaces, upscale and interpolation last, loudness targets re-verified (EBU R128 v4, ATSC A/85, Netflix in a browser, web). Exit: the S2 render cut, graded and mixed to a stated target, `qc loud` within tolerance. About 45 files, 3 agent hours.

**S6. Evals and tuning.** Full suite on Haiku, Sonnet, Opus; decoys against neighbours (chartwright, threewright, a ComfyUI image skill, generic video editing); tune failures with evergreen-tune; worth check per skill (`evergreen.py worth`); merge or cut skills that test redundant. Exit: all cases pass, no skill marked CUT, results in each TESTS.md. 4-6 agent hours (run time dominates).

**S7. Packaging, install, release.** Install routes in §9 on every host; per-skill ZIPs; README (40+ words, what it runs and fetches); public scrub (`cine.py scrub`: LAN addresses, hostnames, GPU names, drive paths, private project names, emails) over every file including `ai-docs/` (the brief and session prompts name local paths and private projects today; move those lines to the vault sidecar); make the repo public (Mark's go, D5); tag 0.1.0 with a GitHub Release; register in evergreen and the mark-local marketplace; submit core to the Claude directory and awesome-copilot (Mark's go). Exit: every route installs and triggers once. 3-4 agent hours.

**S8. Private A/B film test.** §8; lessons fed back as LEARNINGS entries and kb edits; a 0.1.x release if knowledge changed. Exit: report in the vault sidecar, one-sentence result in README. 3 agent hours plus render time.

## 11. Decisions for Mark

| # | Decision | Recommendation |
|---|---|---|
| D1 | Name | `cinewright`: free on GitHub 2026-10-03, fits the *wright family, says film plus craft. No strong reason against found |
| D2 | License | MIT (as threewright and chartwright); plus a NOTICE for any CC BY 4.0 adaptation from visual-skills |
| D3 | Slices | Two public plugins, `cinewright` (core, 5 skills) and `cinewright-craft` (8), plus `cinewright-dev` (curate) in the marketplace only. Physical folders, not `strict: false` slicing, so each can go to the Claude directory |
| D4 | Money | None planned. All renders local (H3, Wan, LTX-2). Hosted renders (Veo, Kling, Seedance) only to verify a compiled prompt works: about 3 short clips per model; ask before any |
| D5 | When public | At S7, after the scrub and install tests pass on the private repo, before the directory submissions |
| D6 | CI while private | Self-hosted runner on Mark's PC while private (his rule: no paid Actions); GitHub-hosted Ubuntu, Windows, macOS matrix once public |
| D7 | Token calibration | Use the free token-counting endpoint once in S1 with an Anthropic API key, or keep bytes ÷ 4 labelled as an estimate |

## 12. Risks

- Model churn: cards go stale in weeks. Mitigation: `verify_at_use` on the card in use, `last_checked` on every card, fast tier.
- VLM judging is noisy: rubric items are yes/no on a contact sheet, majority of three, and a person decides on taste.
- Scope creep across 13 skills: S3-S5 each stop at budgets green and the example film passing; depth grows from LEARNINGS, not upfront.
- Listing cost on users with many skills: §6 caps, measured in CI.
- Licensing of sources: books are cited, never quoted at length; CC BY 4.0 text is adapted with attribution or not at all.

Related: builds on [../research/2026-10-03-research-brief.md](../research/2026-10-03-research-brief.md), [../research/2026-10-03-packaging-verification.md](../research/2026-10-03-packaging-verification.md); see also [../research/2026-10-03-competitor-study.md](../research/2026-10-03-competitor-study.md)
