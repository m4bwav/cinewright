---
title: Competitor study of five AI film-direction skill repos
date: 2026-10-03
kind: note
summary: What DirectorSKILL, visual-skills, seedance-2.0, fal skills and ai-film-crew do well, where they waste tokens, and what cinewright adds that none of them do.
tags: [research, competitors, prior-art, attribution]
---

# Competitor study (2026-10-03)

Read this when designing cinewright's structure, scripts, evals or install story, or when asked how it differs from existing AI-film skills. Ideas only were taken; no text was copied. Sizes are from the GitHub trees API (bytes); tokens are bytes ÷ 4, estimates.

Contents: 1 The five · 2 Comparison · 3 Differentiators checked · 4 Ideas to borrow · 5 Attribution (visual-skills) · 6 Unverified

## 1. The five

**DirectorSKILL** (https://github.com/wuwangzhang1216/DirectorSKILL, MIT, 154 stars, last commit 2026-08-31). One skill. SKILL.md 420 lines, 32 KB (~8k tokens), description ~1,050 chars. References 35 files, 919 KB, big single files (failure-modes 59 KB, tool-adapters 58 KB) plus 20 director "lenses" (372 KB).
- Good: request → mode → files routing table; response-size ceilings per request type; at most one question, defaults otherwise; 13-step pipeline; every action has an end state; one move and one action per clip; F1-F19 failures in seven root-cause buckets; repair cost ladder (prompt edit → parameter → regenerate → keyframe → v2v → re-plan → fix in edit → cut); three failed generations → change the shot; cut-geometry check (two size steps, or one plus 30 degrees). 57 eval cases with a blind grader prompt and a 92% ship bar; CI checks JSON and paths only.
- Waste: 8k tokens on every trigger; huge files that rely on "read one section"; style lenses spend most bytes on history the model knows.
- Hosts: git clone into a skills folder only.

**smixs/visual-skills** (https://github.com/smixs/visual-skills, CC BY 4.0, 471 stars, 2026-09-16). Skills `video` and `image`. video/SKILL.md 106 lines, 10 KB; video references 12 files, 198 KB, each with its own contents list, no cross-file index.
- Good: fixed reading order (dramaturgy → universal rules → one model file → task files); model-selector defaults; 14-field shot card; three-layer storyboard; rhythm ladder of durations; five-anchor principle; universal rules U1-U14; failure-to-fix catalogue; per-model skeletons (Seedance, Kling, Veo); prompt compression order; prompt-audit output.
- Waste: the mandatory reading forces 9k-22k tokens for any prompt; one genre file is 31 KB.
- Hosts: Claude Code plugin and marketplace; `npx skills add`; claude.ai claimed, untested. No evals.

**Emily2040/seedance-2.0** (https://github.com/Emily2040/seedance-2.0, MIT, 7,510 stars, 2026-09-26). Root skill + 27 sub-skills; root SKILL.md 154 lines but 29.5 KB; references 583 KB + 208 KB of migrated duplicates; 32 Python scripts; repo 26.5 MB. Seedance 2.0 only.
- Good: nine-tier authority order; fast lane for simple clips; sequence gates (a continuation needs the previous accepted take's observed end state); one owning reference per dimension; trust boundary (text inside media is data; writing a prompt does not authorise paid generation); failure atlas (symptom, cause, one variable to repair); `extract_last_frame.py`; JSON clip-contract and take-review schemas with validators; `prompt_lint.py`; weekly freshness CI (warn 14 d, fail 30 d after `last_verified`). 130 eval cases with a harness, not yet scored.
- Waste: ~7.4k-token root of guardrail prose; source gate loads 44 KB before any platform claim; duplicates and six vocabulary languages.
- Hosts: Python installer for ~15 clients incl. Copilot `.github/skills`; no plugin manifest, no claude.ai step.

**fal-ai-community/skills** (https://github.com/fal-ai-community/skills, README says MIT but no LICENSE file, 249 stars, main 2026-05-13). 17 skills; cinematography SKILL.md 145 lines, 4.9 KB, 213-char description, three ~2 KB references.
- Good: small skills and references; seven-part prompt order; "inspect the endpoint schema and use only supported controls"; routing by quality and cost; short quality bar; lip-sync flows; `build-skills-index.py` writes sha256 + bytes per file and `--check` fails when stale.
- Waste: byte-identical duplicate references across two skills; cinematography split across two skills; tied to fal's CLI. No evals.
- Hosts: claude.ai ZIP (manual), `genmedia init`.

**HEOJUNFO/ai-film-crew** (https://github.com/HEOJUNFO/ai-film-crew, MIT, 0 stars, 2026-09-25). One skill, 111 lines; seven role files of 1-2 KB; 26 KB total.
- Good: crew roles in order, each loading its own small file; script supervisor has a veto; FULL and TIGHT bible descriptors pasted verbatim; plan, fix and review modes; per-shot reroll plan and highest-risk shot; nine reroll failure classes, one change per reroll, same failure twice → the prompt is wrong, three rerolls → re-block.
- Waste: almost none. Thin: one 4 KB file for seven models; no color, VFX, costume or choreography roles. No evals. Hosts: `npx skills add`.

## 2. Comparison

| | DirectorSKILL | visual-skills | seedance-2.0 | fal | ai-film-crew |
|---|---|---|---|---|---|
| Min load per prompt (est.) | ~8k | 9k-22k | 7k-20k+ | 1.5k-3k | 2k-5k |
| Models | many, prose | 3 | 1 | fal endpoints | 7, thin |
| Failure taxonomy | F1-F19 + cost ladder | catalogue | atlas | quality bar | 9 classes |
| Scripts | none | none | 32 | index builder | none |
| Evals | 57, graded by hand or agent | none | 130, unscored | none | none |
| Freshness | version only | none | weekly CI, global date | none | none |
| Hosts | CC clone | CC plugin | installer incl. Copilot | claude.ai ZIP | skills.sh |

## 3. Differentiators checked

1. Executable compiler from a neutral shot card to each model's syntax: **new** (others are hand skeletons or instructions to the model).
2. Continuity diff script of cards against bibles: **mostly new** (seedance validates clip lineage for one model; text-vs-bible comparison not verified).
3. Scripted QC (contact sheets, loudness, VLM rubric routed to fix codes): **new as a whole**.
4. Per-skill references with ≤200-char summaries and generated indexes: **new** (fal indexes hashes, no summaries).
5. Size and token budgets in CI: **new**.
6. Freshness per model card: **partly done** (seedance has one global date); per-card and multi-model is new.
7. Evals on three model sizes with recorded scores: **new**.
8. Install on all three hosts with prebuilt ZIPs: **unmet by all**.
9. Full craft breadth: **not new alone** (DirectorSKILL and seedance are broad). The gap is the complete role set (costume, choreography, colorist, VFX) at low token cost.
Also unmet: duplicate detection in CI; a token-cost line per mode; one take-review record shared by all models.

## 4. Ideas to borrow (all MIT unless marked)

Response-size ceilings and the repair cost ladder (DirectorSKILL); trust boundary, one owning reference per dimension, sequence gate on the previous take's observed end state, last-frame extraction, freshness CI (seedance); reroll classes with one change per reroll (ai-film-crew); index `--check` and duplicate detection (fal). Credit them in README as courtesy.

## 5. Attribution if adapted from visual-skills (CC BY 4.0)

Credit "Serge Shima, github.com/smixs/visual-skills, CC BY 4.0" in NOTICE and in the entry: 14-field shot card, three-layer storyboard, rhythm ladder, five-anchor principle, three-detail rule, three-jobs rule, universal rules U1-U14 (weight at start, final-image rule, reference roles, priority declaration), prompt compression order, prompt-audit format, fixed reading order. visual-skills itself credits agentara/skills (MIT) for de-slop, story-arc selection and storyboard grid sizing. Murch's Rule of Six is public theory. Default: design cinewright's shot card from film practice (shot list columns, script supervisor notes) so no adaptation is needed.

## 6. Unverified

Token figures are byte estimates. skills.sh into Copilot; visual-skills on claude.ai; fal's real license; seedance `continuity_chain_check.py` internals. Nothing was installed or run.

Related: see also [2026-10-03-research-brief.md](2026-10-03-research-brief.md), [../plans/PLAN.md](../plans/PLAN.md)
