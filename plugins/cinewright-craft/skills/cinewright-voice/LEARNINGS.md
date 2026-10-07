# Learnings: cinewright-voice

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-07 · `llm-ear-misjudges-voices`: a listening LLM drafts, it never judges
- Trigger: 2026-10-07, build test: gemma4 through Ollama called a generated guard's voice female; `voice measure` read a 99 Hz median (male range). It also heard "hallowed halls" as "hollows" and, on one host, two speakers where there was one
- Hypothesis: a 12B multimodal model's audio head is tuned for speech content, not speaker traits, and guesses names it does not know
- Rule: use an LLM's hearing for rough transcripts and first descriptions only; take pitch from `voice measure`, words from the script, identity from an ear or an embedding model
- Evidence: C-20261007-1 (references/ollama-voice.md), confirmed 2026-10-07
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07

### L-002 · 2026-10-07 · `music-corrupts-pitch`: measure the line alone
- Trigger: 2026-10-07, build test: whole 15 s generated shots with score and effects under a man's line read 286 and 343 Hz median, 25 semitones of range
- Hypothesis: the tracker locks onto music partials whenever the voice is quieter than the bed
- Rule: cut to the line's span (or isolate the voice) before `voice measure`, `voice ref` or cloning; trust a measurement only without WARNING lines
- Evidence: C-20261007-1 (`voice measure` warns on low voiced share and range over 18 semitones; references/reference-clips.md), confirmed 2026-10-07
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07

### L-003 · 2026-10-07 · `yin-threshold-0-3`: YIN threshold 0.3, pace over the whole span
- Trigger: 2026-10-07, build test: at threshold 0.2 a low creaky voice was voiced only 37% of its speech and a fast read fell under the warning line; pace over gated time read 260 words a minute for a normal read
- Hypothesis: 0.2 rejects rough low voices; gating removes pauses, so pace was an articulation rate
- Rule: `f0_track` uses 0.3 (medians stayed within 1 Hz on clean clips; a noisy line moved from 286 to 124 Hz); pace divides words by first-to-last speech time
- Evidence: C-20261007-1 (shared/lib/cine.py), confirmed 2026-10-07 (normal read 200 wpm, fast read 321)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07
