---
title: Failure codes live in shared vocab and drive the rubric
kind: decision
status: active
date: 2026-10-03
verified: 2026-10-03
stale_after: 2027-04-01
tags: [qc, failures, taxonomy, shared, rubric]
entities: [cine.py, failures-picture, failures-motion]
summary: "Read before adding or renaming a failure code or rubric check: where the codes live, how qc rubric parses them, and the test that keeps them in step"
---

# Failure codes live in shared vocab and drive the rubric

## Context

PLAN §2 puts the failure codes in cinewright-genvideo, while `qc rubric` in cinewright-qc has to map each failed check to a code and a fix. Each skill must also work when installed alone.

## Decision

The 24 codes are two entries in `shared/vocab/`: `failures-picture` and `failures-motion`. There are two entries because one table would break the 700-token entry budget. `cine.py build` copies both into genvideo and qc. Each table row gives the code, symptom, cause, cheapest fix, ladder rung and rubric check. `qc rubric` reads every entry tagged `failures` and parses its rows (`taxonomy()`), so the table is the only source. The rubric's checks are fixed in code (`RUBRIC` in `shared/lib/cine.py`). A test asserts that every check has at least one code and every code names an existing check.

## Reasons

There is one source, both skills can read it, and the codes stay readable as knowledge. A JSON data file next to the Markdown was rejected because it would be a second source that drifts. Keeping the codes only in genvideo was rejected because qc installed alone would have no codes.

Related: builds on [2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md](2026-10-03-shared-sources-copied-into-skills-with-a-hash-header.md)
