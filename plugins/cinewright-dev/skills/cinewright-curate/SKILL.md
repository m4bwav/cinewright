---
name: cinewright-curate
description: "Upkeep of cinewright's knowledge base in a repo checkout: add, verify or retire entries, refresh model cards when a video model changes. Also 'refresh cinewright-curate'."
license: MIT
---

# cinewright-curate

Outcome: cinewright's knowledge base gained, re-verified or retired an entry through `cine.py kb`, `kb lint` passes, and the change is dated in the entry and logged in the skill's CHANGELOG.

Work in a cinewright repository checkout: the folder holding `scripts/cine.py`, `shared/` and `plugins/`. If the current folder is not one, ask for it; never edit an installed plugin's cache. `CINE` means `python scripts/cine.py` run from that root (run it, never read it).

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task with the current content, then run `evergreen-refresh` if the evergreen plugin is installed. If `tests.failing` is non-empty, say so and run `evergreen-tune` after the task.

## Step 1: find the entry

`CINE kb search <words>` finds slugs; `CINE kb due` lists entries past their skill's interval, oldest first, with each model card's `volatile_claims`. A slug in `shared/vocab/` is one source copied into several skills: the commands edit the source and rebuild the copies. Never edit a copy, a generated `INDEX.md`, or the frontmatter dates by hand.

## Step 2: change it through `CINE kb`

| Ask | Command | Rule |
|---|---|---|
| New knowledge | `CINE kb new <skill> <slug> --title T --summary S --tags a,b --source URL` | search first; an existing entry gets an edit, not a twin. Then fill Rules (plus Numbers, Vocabulary, Pitfalls as needed) and Verify |
| Re-checked a page | `CINE kb verify <slug> --source URL [--note "what changed"]` | `--source` is the page read this session; edit the body first if it changed |
| A model card's claims moved (price, length, IDs, dates) | edit the card's Rules, Numbers and `volatile_claims`, then `kb verify` | one card per model; the Compile block changes only with a vendor example that shows the new syntax |
| A model shut down | `CINE kb retire <slug> --reason R` (status `shut-down`, the default) | the card stays (old shot lists name it; compile warns) |
| A model still served but with an announced end | the same, plus `--status deprecated` | only when the vendor still serves it |
| Knowledge that is wrong or merged elsewhere | `CINE kb retire <slug> --reason R` | refused while another file names the slug; edit those first |

Write knowledge as rules, numbers and vocabulary: one default, not a menu; no prose a model already knows. An entry stays at 60 lines or fewer and its summary at 200 characters or fewer (`CINE budget`).

## Step 3: prove it

Run `CINE kb lint` (the evidence is its last line, `kb lint: N skills, 0 errors`) and quote it. A change to `scripts/cine.py` or `shared/lib/` also runs `python -m unittest discover -s tests`. `kb new` and `kb verify` do not write the CHANGELOG: add a `C-` entry to the edited skill's CHANGELOG.md (`kb retire` writes its own). Lint also refuses LAN addresses, drive paths and GPU names; keep machine details out of entries.

## Output

One to three lines: the slug and file changed, the command run, the `kb lint` line, and the CHANGELOG id.

## While working: capture learnings

If the user corrects you, the same error happens twice, or a workaround turns up, add an entry to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If it proves a rule here wrong, fix the rule, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `moderate`; state in `evergreen.json`). Files: [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`. How to maintain it, with or without the evergreen plugin: [MAINTENANCE.md](MAINTENANCE.md). Refresh with `evergreen-refresh`, test with `evergreen-test`, fix with `evergreen-tune`.
