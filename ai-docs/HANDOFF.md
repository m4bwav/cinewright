# Handoff

## Current state
- S2 (genvideo and qc) was done on 2026-10-03 on branch `s2/genvideo-qc`. Its PR waits for Mark's review. S1 (PR #2) was merged with no comments. The repo is private: https://github.com/m4bwav/cinewright.
- Built: nine model cards with a compiler for each (`veo`, `omni`, `kling`, `seedance`, `runway`, `luma`, `minimax-h3`, `wan`, `ltx2`), 24 failure codes in `shared/vocab/failures-*.md`, the `cinewright-qc` skill (`qc sheet|spec|loud|rubric`, `takes log|lastframe`, SETUP.md for ffmpeg), and 47 tests. Layout: [../CODEMAP.md](../CODEMAP.md).
- First real render, local H3: one failure (`eyeline-wrong`) was routed to its fix and re-rendered, and the fix held. The take records and note are in the vault sidecar; the media is in the local render folder ([decision](decisions/2026-10-03-render-media-stays-in-the-local-render-folder.md)).
- The exit check passed. Its outputs are quoted in [log.md](log.md): tests on 3.14 and 3.9, `kb lint`, budget GREEN, `claude plugin validate` on the root and each plugin, and `evergreen.py lint` on each skill.

## In progress
- Mark's review of the S2 PR. He has one question to answer: the proposed model-card budget row ([decision](decisions/2026-10-03-proposed-model-card-budget-row.md)). D1-D7 are still on the S1 recommendations.

## Decisions made this session
- Failure codes live in shared vocab and `qc rubric` parses them ([decision](decisions/2026-10-03-failure-codes-live-in-shared-vocab-and-drive-the-rubric.md)).
- Model syntax comes from each vendor's own guide, and each test regex must also match the vendor example (genvideo L-003). The H3 card follows MiniMax's labelled-field form, not the earlier local Timeline form.
- Seedance targets 2.5 and Luma targets `ray-3.2`, the current API models.

## Watch
- Every model card sits at 646-700 est. tokens against the 700 line, and the genvideo folder is at 147 of 150 KB (the runtime copy is 67 KB). S3 adds code, so the folder may go yellow.
- Veo Gemini API preview IDs shut down 2026-10-22, and Seedance 2.0 discounts end 2026-10-07. Re-check before any hosted render.
- Unverified: Omni dialogue syntax and seed; Seedance braces vs quotes for dialogue; the H3 frame grid (field notes only); the local LTX length ceiling.
- Open from the render: 1A's opening (the lens is lit), the tin matchbox prop, and the side of Maren's scar.

## Next single action
- After Mark reviews the S2 PR, run [next-session-prompt.md](next-session-prompt.md) (S3: the script, shots, design and movement skills).
