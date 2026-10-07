---
title: A fourteenth skill for character voices, with an optional voice bible
kind: decision
status: active
date: 2026-10-07
verified: 2026-10-07
stale_after: 2027-04-01
tags: [voice, skills, budget, schema, runtime]
entities: [cinewright-voice, voice-bible, cine.py]
summary: "Read before merging voice work into another skill, changing bibles/voices.json, or touching the description budget: why voice is its own craft skill, why the bible is optional, and the yellow description total"
---

# A fourteenth skill for character voices, with an optional voice bible

## Context

Mark asked (2026-10-07) for an evergreen skill that makes reference material so each character's voice stays the same across generated videos, from a new design or from voice samples already generated. cinewright-sound mixes and cinewright-script writes lines, but neither owns a voice's identity, and video models drift a voice between clips.

## Decision

- New craft skill `cinewright-voice` (plugins/cinewright-craft), not a section of cinewright-sound: its triggers ("my characters sound different in every shot", "match his voice") differ from mixing, and its knowledge (engines, cloning, consent) would push sound past its budgets.
- `bibles/voices.json` is optional, like props.json. The short `voice` string stays in characters.json, because compile copies it into every prompt. The voice bible holds the sheet, the engine lock, the reference clips with transcripts, and `rights`.
- `cine.py voice measure|ref|check` in the shared runtime, stdlib only: YIN pitch on ffmpeg-decoded 8 kHz audio (threshold 0.3, LEARNINGS L-003 `yin-threshold-0-3` in the skill), pace from the line's words. It proves pitch and pace, never identity; the skill says so on every check.
- Every skill that ships the bible schemas also ships voice-bible.schema.json, because `cards validate` in any skill validates voices.json when it exists.
- Defaults: Qwen3-TTS (open, Apache-2.0, design then clone), ElevenLabs (hosted), TTS Audio Suite in ComfyUI. Ollama drafts text and rough transcripts only (L-001 `llm-ear-misjudges-voices`).

## Consequences

- The all-descriptions budget goes yellow: 4,336 characters against a 4,000 green line (5,500 red). Mark was told in the session; trimming other descriptions would need their trigger evals re-run.
- Runtime shared/lib grows from 78 to 90 KB (green under 100).
- Rejected: speaker-embedding similarity inside cine.py (needs numpy or torch, breaks stdlib-only); it stays an optional step in the skill.

Related: builds on [2026-10-04-prop-bible-and-pre-production-checks.md](2026-10-04-prop-bible-and-pre-production-checks.md); see also [../research/2026-10-07-voice-consistency.md](../research/2026-10-07-voice-consistency.md)
