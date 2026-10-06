# Learnings archive: cinewright-genvideo

Retired entries from [LEARNINGS.md](LEARNINGS.md), each with the date and reason. Kept so no one re-adds a rule that was retired for cause.

### L-006 · 2026-10-04 · Lead the description with the verb users type
- Trigger: 2026-10-04, S6 matrix T-20261004-1: trigger-1 (write a Veo 3.1 prompt for this shot) and trigger-2 (turn the shot cards into prompts for Veo) invoked the skill Haiku 0 of 3 each; Haiku answered trigger-1 in one turn with no tool; Sonnet and Opus 3 of 3
- Hypothesis: A description that opens with a noun phrase ("AI video prompts: compiles ...") gives a small model no action to match a request against
- Rule: Open with "Writes AI video prompts" and say "Use when asked for a prompt for one of these models or to turn shots into video-model prompts"
- Evidence: C-20261004-2 (description); not confirmed
- Scope: skill
- Status: retired · helpful 0 · harmful 0 · last_confirmed 2026-10-04
- retired: 2026-10-05 · Haiku still invoked the skill 0 of 3 on both triggers after the edit (T-20261005-1); Sonnet and Opus were 3 of 3 before and after. The description keeps its opening; the Haiku failure is recorded under decision item 5
