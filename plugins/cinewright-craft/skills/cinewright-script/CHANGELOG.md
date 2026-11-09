# Changelog: cinewright-script

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:`, `files:`, and a sentence on what changed.

### C-20261109-3 · 2026-11-09 · Structure and performance rules from Mamet, Proferes, DeKoven and Bordwell (books round 5, track 23)
- because: book distillation (round 5), pre-approved
- files: references/logline-and-beats.md, scene-turns.md, performance-words.md; shared/vocab/performance-verbs.md
- Short rules merged into existing entries: capped objective and `ends_when`, beats below the objective, Thompson's parts, midpoint knowledge flip, rule of three and plants, why-now opening, unfilmable lines; scene chain and dialogue hook, fulcrum and blocks, knowledge range and deadline; need chain, no be/look verbs, playable in silence, activity vs action, restraint card, facts not attitudes; intensity ladders, gaze and blink, eyes-only push-in. Knowledge only, no new checks; prose trimmed to stay under the entry token cap.

### C-20261109-2 · 2026-11-09 · RESULT check for performance text (books round 5, track 22)
- because: book distillation (round 5), pre-approved
- files: references/performance-words.md; shared/lib/cine.py
- `continuity diff` RESULT warns when a `perform` verb or body holds only result words and no task (Weston ch. 1). A warning, never an error.

### C-20261109-1 · 2026-11-09 · Performance words, beats and voice lines from Weston and Rabiger
- because: book notes round5 (books/plugin-learnings, track 21)
- files: references/performance-words.md (new), scene-turns.md, logline-and-beats.md, dialogue-for-generated-voices.md; vocab performance-verbs; card cast[].perform, dialogue[].intent
- New entry: objective, playable verb, task, posture, masks, enters_from; turns as a change of awareness with question and stakes; need paired with a visible task; line intent and subtext.

### C-20261016-1 · 2026-10-16 · Lesson: a card holds 8 s, so a long line is cut at a comma across two shots
- because: L-004
- files: LEARNINGS.md (Active: L-004)
- From a duel's words before a stab: the card schema caps a card at 8 s, so a line past about 17 words is split across two setups instead of sped up or trimmed.

### C-20261007-2 · 2026-10-07 · Point locked voices to cinewright-voice
- because: user request (cinewright-voice created, its C-20261007-1)
- files: references/dialogue-for-generated-voices.md
- The voice-string rule now says a voice that must match across shots gets a locked reference in cinewright-voice.

### C-20261007-1 · 2026-10-07 · Speaker in the shot, pronounce respellings, tone as an adverb
- because: L-003 (owner's review of the library film), the cinewright-genvideo lesson on off-screen speakers
- files: SKILL.md, references/dialogue-for-generated-voices.md, LEARNINGS.md
- Step 2 asks for each speaker in the shot and a `pronounce` respelling for spoken rare names; the reference names the new SPEAKERS, OFFSCREEN, TONE and PRONOUNCE warnings and was tightened to stay in its token budget

### C-20261004-2 · 2026-10-04 · Step 4 runs the diff whenever a line changes (S6)
- because: T-20261004-2, L-002
- files: SKILL.md
- Step 4.2 now runs `continuity diff` whenever a line changes and forbids counting words by hand instead

### C-20261004-1 · 2026-10-04 · Created as an evergreen unit (cinewright S3)
- because: user request, R-20261004-1
- files: SKILL.md, references/, needs.json, RESEARCH.md, LEARNINGS.md, TESTS.md, evals/evals.json, evergreen.json, MAINTENANCE.md
- Initial version. Tier `slow`, interval 120d. First test run is logged in TESTS.md.
