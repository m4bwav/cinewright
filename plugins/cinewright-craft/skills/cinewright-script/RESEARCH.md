# Research: cinewright-script

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md).

Topic: Screenwriting for short AI video: logline, beats, scene turns, screenplay format and dialogue for generated voices. Tier `slow`. Last refresh 2026-10-04; next due 2027-02-01.

## Current understanding

- Settled (craft): logline form (the 35-word cap and template are a house rule, not Snyder's), beat structure, one value turn per scene, screenplay format and page timing (Snyder 2005; Field 2005; McKee 1997; Riley 2021).
- Settled (AI-specific): a turn spread over several separately generated shots reads as no turn; put it in one shot.
- Moving: native dialogue in Veo 3.1, Kling 3.0, Seedance 2.5, MiniMax H3 and LTX-2; voice strings and tone tags differ by model (genvideo cards).
- Unverified: 2.5 words a second is a conversational English rate; how each model rushes or pads lines is a field observation, not measured per model.

## Open questions

- Measure spoken words per second per model on the same line (S8 renders).
- Do non-English lines need a lower words-per-second limit?

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `short film screenplay structure beats <year>`
- `logline formula screenwriting <year>`

Tooling:

- `path:SKILL.md "screenplay"` on GitHub code search; skills.sh weekly installs for `screenwriting`
- `https://registry.modelcontextprotocol.io/v0/servers?search=screenplay`

Practice:

- `AI video dialogue lip sync words per second <month> <year>`
- `site:reddit.com/r/aivideo dialogue too long cut off`

Testing:

- `speech rate words per minute conversational study`
- `path:SKILL.md screenplay evals`

Best sources (primary first): McKee, Story; Snyder, Save the Cat!; Field, Screenplay; Riley, The Hollywood Standard; fountain.io syntax. Noisy: logline generators.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261120-3 · 2026-11-20 · Want against need, beat tests, scaled finale (Save the Cat! Writes a Novel)
- Summary: Concrete want with a visible "got it" shot against an inner need; catalyst no-way-back test, all-is-lost bigger than the catalyst and partly the hero's fault, midpoint direction flip, act-two world opposite on a named axis; a five-point finale scaled to one surprise for 2-5 min and one beat at 30-60 s. Brody's percentages are rounder than Snyder's page fractions (break into two 20% against about 23%, all is lost 75% against about 68%); Snyder's are the default, Brody's noted. Noted, not built: Brody's ten-genre table with three ingredients each, and one beat list per point-of-view character. Book rules, unverified.
- Track: subject
- Sources: Jessica Brody, Save the Cat! Writes a Novel, 2018, ch. 1, 2, 4-15 (paraphrased; no text copied)
- Magnitude: 0.15
- Applied: C-20261120-1

### R-20261120-2 · 2026-11-20 · Revision passes and reader notes, leave early, split read (101 Habits)
- Summary: No revise step existed. Fixed passes (scene, whole film, line), known problems fixed before review, a fresh reader per draft, the one/two/three reader count rule, keep the problem and design your own fix, targeted reader questions. Scene jobs (one-job scene merges) and a seconds budget summed against length; leave early beside enter late; the split read test; cut what cannot be said aloud. Caution ours: same-model subagents are not independent readers. Book rules, unverified (anecdote, no tests).
- Track: subject
- Sources: Karl Iglesias, The 101 Habits of Highly Successful Screenwriters, 10th anniv. ed., 2011, ch. 6, 10-14 (paraphrased; no text copied)
- Magnitude: 0.15
- Applied: C-20261120-1

### R-20261120-1 · 2026-11-20 · Bookend pair, logline tests, attribution fixes (Save the Cat!)
- Summary: Bookend pair (opening and final image as opposites on one axis), the one Snyder beat that survives at 45 s. Attribution fixed: Snyder gives no 35-word cap and no when/where + goal + obstacle template (kept as a house rule); his logline tests are irony, implied time frame, an adjective for hero and opponent, and a primal goal. His midpoint is a false high or low mirrored by all is lost; the knowledge flip is not his (kept, credited to nobody). Beat fractions from his 110-page positions; named failures (laying pipe, danger off screen, two kinds of magic, passive hero); conflict line beside the scene charge; hidden-speaker test. He calls strict charge alternation too much (ch. 5), noted beside McKee. Book rules, unverified.
- Track: subject
- Sources: Blake Snyder, Save the Cat!, 2005, ch. 1, 3-7 (paraphrased; no text copied)
- Magnitude: 0.2
- Applied: C-20261120-1

### R-20261113-2 · 2026-11-13 · Clip start and tail, cheat-out (Acting for Film)
- Summary: Set practice carried to clips: start mid-moment, keep the end position alive, cheat out toward camera with the eyeline on the partner. The rest of the book is actor training that does not carry. Book rules, unverified.
- Track: subject
- Sources: Cathy Haase, Acting for Film, 2003, ch. 6 and 14 (paraphrased; no text copied)
- Magnitude: 0.1
- Applied: C-20261113-2

### R-20261113-1 · 2026-11-13 · Narration writing, nonfiction honesty, the train (Documentary Storytelling)
- Summary: New entries narration-writing and nonfiction-honesty (the disclosure rule is ours, marked so); logline-and-beats names the train and the point of attack; SKILL.md step 3 points to both. Book rules, unverified.
- Track: subject
- Sources: Sheila Curran Bernard, Documentary Storytelling, 5th ed. (paraphrased; no text copied)
- Magnitude: 0.2
- Applied: C-20261113-1

### R-20261004-1 · 2026-10-04 · Initial research
- Summary: Built from the research brief §3 story row and §4 sources (subject), vendor dialogue guides on the genvideo cards (practice), the competitor study (tooling: competitors write scripts as prose with no length check), and TESTING.md (testing: the diff's DIALOGUE warning is the checkable part).
- Track: subject
- Sources: https://fountain.io/syntax, https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Magnitude: n/a (initial)
- Applied: C-20261004-1
