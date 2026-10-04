---
title: Prop bible and pre-production checks
kind: decision
status: accepted
date: 2026-10-04
verified: 2026-10-04
stale_after: 2027-02-01
tags: [schema, props, continuity-diff, shared-vocab, s3]
summary: "Read before adding a bible or a diff check: S3 added an optional bible/props.json, DIALOGUE and HARD-SUBJECT warnings, cards list, and moved the thirty-degree rule to shared vocab"
---

# Prop bible and pre-production checks

## Context

S3's rule: a new card or bible field goes into the schemas, the compiler and the continuity diff together, with a test. The S2 render failed 1A on prop drift (a cardboard box where the story meant tin), and its note proposed a prop constant in the bible. The S3 skills also had rules a script could check: dialogue length (script), crowds in wide shots (movement), and one shot list (shots).

## Decision

- **`bibles/props.json`, optional.** `{props: [{name, description, refs?}]}` (`shared/schemas/prop-bible.schema.json`). `cards validate` checks it when present. The compiler's `prop_words()` pastes the description wherever a card's `holding` names the prop (subject and staging parts), and compile stops if it is missing, like the identity guard. The diff accepts its names as allowed props and warns PROP when a held prop has no description while the file exists. `qc rubric` names the description in the props check.
- **Two diff warnings that need no new field.** DIALOGUE: words > 2.5 × (duration − 0.5 s). HARD-SUBJECT: crowd or herd words in the action or subject of an EWS or WS card. Warnings, not errors: both have legitimate exceptions, written in the card's `notes`.
- **`cards list`.** Prints the shot list from the cards in cut order, so nobody keeps a second list by hand.
- **Thirty-degree rule in shared vocab.** It moved from continuity's references to `shared/vocab/`, so shots and continuity read one source (copied by `build`).

## Reasons

A separate file keeps props optional for projects without held objects, and it keeps the character bible's `props` list (which props a person may hold) apart from what a prop looks like. Rejected: a description map inside the style bible (wrong owner), and putting descriptions into the character bible (one prop can pass between characters, as the match does). Rejected for dialogue: an error, because a held line over a long beat is a director's choice.

Related: builds on [2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md](2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md); see also [2026-10-04-proposed-runtime-budget-row.md](2026-10-04-proposed-runtime-budget-row.md)
