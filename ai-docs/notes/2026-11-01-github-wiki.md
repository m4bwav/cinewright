# GitHub wiki (2026-11-01)

The wiki at https://github.com/m4bwav/cinewright/wiki was written with the wikiwright skill for cinewright 0.2.0 and pushed as wiki commit 90f13a2 on top of GitHub's placeholder (fast-forward).

- Working copy: `D:\m4bwa\Claude\Projects\Ai\cinewright.wiki` (sibling of the clone), branch `master`.
- Pages: Home, Getting-Started, The-Skills, The-Pipeline, Commands, Video-Models, FAQ, Versions-and-Upgrading, Development, `_Sidebar`, `_Footer`.
- Page set: wikiwright has no tested set for a plugin repository; this one follows polywright's wiki (skills page plus a pipeline page in place of a behaviour page).

## How the examples were verified

`2026-11-01-wiki-verify.sh` runs from a fresh clone of the `v0.2.0` tag (never the working tree). Its output is `2026-11-01-wiki-verify.out.txt` (output paths masked as `<tmp>`). Checks at publish: `wikiwright.py check --version 0.2.0` 0 errors, `outputs` 7 checked, 0 missing, 4 skipped (abridged or path-bearing blocks, marked), `live` 9 pages, 0 failures, everwrite tells 0 strong. Repository tests at v0.2.0: 138 OK. The v0.1.0 example also validates and diffs clean under 0.2.0 (the upgrade claim).

Not tested: `qc`, `takes` and `voice` (they need rendered media); compiling for models other than Veo.

## Facts the README does not state

- `compile` prints a per-shot and total cost estimate with the model card's `last_checked` date.
- An unknown `--model` exits 1 with "no model card for ...".
- `continuity diff` exits 1 on errors (AXIS, EYELINE for the planted card).
- Model card titles: Kling 3.0, Luma Ray3.2, Gemini Omni Flash.

## Rough edges found

1. `.github/workflows/ci.yml` and AGENTS.md still describe the repository as private (manual-dispatch CI on a self-hosted runner). The workflow's own comment plans push and pull_request triggers on a hosted matrix once public. Left for Mark: it changes a workflow.
2. No root CHANGELOG; release notes live only on the GitHub releases.
3. `cine.py budget` is YELLOW at 0.2.0 (known, AGENTS.md asks for a one-line mention).

Fixed this session: homepage set to the wiki, custom social preview uploaded (`assets/social-preview.jpg`, 1280x640 crop of the banner with the title), README links the wiki, CODEMAP's CI line no longer says private.

## Updating at the next release

Clone the new tag into a scratch folder, run the verify script there, `wikiwright.py diffout` the old and new outputs, then fix the pages. Pages that name the version: Home, Commands (intro), Development (test count, budget), Versions-and-Upgrading, `_Footer`. Add new model cards to Video-Models and new skills to The-Skills.
