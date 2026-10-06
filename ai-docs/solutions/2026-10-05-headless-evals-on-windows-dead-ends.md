---
title: Headless evals on Windows, the dead ends
kind: solution
status: active
date: 2026-10-05
verified: 2026-10-05
stale_after: 2027-01-05
tags: [evals, harness, claude-code, windows]
summary: "Read before changing evals/run_evals.py or reading its numbers: each harness fault S6 hit, what it looked like in the results, and the fix"
---

# Headless evals on Windows, the dead ends

Claude Code 2.1.281, Windows 11, `claude -p --restricted --permission-mode dontAsk`. Every item below first showed up as a skill "failure" and was the harness.

| Symptom in the results | Cause | Fix in `evals/run_evals.py` |
|---|---|---|
| Every judge vote "unreadable" | `claude` on PATH is a `.CMD` wrapper; cmd.exe re-parses arguments, so a multi-line prompt arrived empty | call the wrapped `claude.exe` (`claude_exe()`), send every prompt on stdin |
| A failing `cine.py qc loud` (exit 1) did not count as the action | `tool_result.is_error` is set on a nonzero exit too | `tool_uses()` marks a call refused only when the result text says it was denied |
| Run marked contaminated with `d:\n` | the path scan read a Write's file content | scan only `command`, `file_path`, `path` |
| `cp -r examples/three-shot out/x` refused, models copy file by file and run out of turns | `dontAsk` refuses a recursive cp whatever the allow rule (`Bash(cp:*)` and `Bash(cp *)` both; a single-file cp runs) | cases copy the project in `setup` and say so in the prompt |
| `python "C:/.../scripts/cine.py" ...` refused | rule `Bash(python scripts/cine.py:*)` is a prefix match; models use absolute and quoted paths, compound `cd ...;` commands | `Bash(python *cine.py*)` (probed: `python -c` and other scripts stay refused; `cat` of the repository is still refused by `--restricted`) |
| Action graded absent although `cine.py ... continuity diff` ran | the closing quote in `cine.py" continuity` and `P=...; ... "$P"` defeat `cine\.py\s+...\s+\S*out/x` | quotes dropped before matching; evidence regexes accept the path anywhere in the command |
| Camera and history compile cases failed with the skill on every model | `compile` needs genvideo's model cards, in the core plugin, which the craft run did not load | a case's `plugins` field loads other plugins a real install has |
| Baselines passed action cases | `or` file alternatives (a style file with "lighting", a hand-written 1A.txt) proved nothing about the route | evidence is the trace only where a baseline passed on the file |
| 155 runs "failed" in a row, judge 0 votes | the account's session limit (HTTP 429, "You've hit your session limit"); the detector matched only "usage limit" | `env_problem()` reads `error: rate_limit` and `api_error_status`; a hit stops the queue (`LIMITED`); judge limit hits raise |
| Sonnet failed long tasks at 31 turns | `--max-turns 30` | 60 for action and outcome |
| Judge said "no files written" on a correct compile | `written_files()` compared with the repository's example, which still has `compiled/` | paths the fixture stripped always count as written |
| Judge graded a maintenance note, not the answer | a skill's Step 0 reports `tests.failing`; the last message was that note | the judge gets every assistant text, in order (`final_text()`) |

Tools: `run_evals.py regrade` re-grades action runs from traces after an evidence fix; `rejudge` re-grades failed outcome runs from kept folders. A passed run's folder is deleted, so its file evidence cannot be re-read: regrade skips it.

Related: [../decisions/2026-10-05-eval-harness-and-model-matrix.md](../decisions/2026-10-05-eval-harness-and-model-matrix.md)
