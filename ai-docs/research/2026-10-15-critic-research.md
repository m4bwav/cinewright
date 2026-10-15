---
title: Critiquing AI video, images, voices and sound - how people and machines do it (2026-10)
summary: Five-track research for the cinewright critic (human review practice, vision judges, audio and voice judges, agentic critic loops, practitioner forums) plus a logprob experiment on a 600-claim labelled set; ranked changes.
tags: [research, qc, critic, judge, vlm, audio, voice, calibration]
date: 2026-10-15
---

# Critiquing AI video, images, voices and sound (2026-10)

Question: the critic is what lets an agent work semi-self-directed overnight. If it is wrong, the agent rerolls good takes or keeps bad ones. How do people review this material by hand, how do machines do it now, and what should cinewright change?

Read when: changing the qc skill's judge, rubric or take selection; adding an audio or voice check; deciding what to escalate to the reviewer.

Related: builds on the 2026-10-12 automated-scoring survey kept in the maintainer's workspace (VBench, VBench-2.0, VideoScore2, VideoAlign, GenVideoLens, MediaPipe, L2CS-Net, SAM 3, RAFT, DOVER; not repeated here); entries `review-passes`, `vision-judge`, `judge-calibration`, `take-selection` (cinewright-qc), `voice-qc` (cinewright-voice), `audio-qc` (cinewright-sound).

Marks: (src) a primary source, URL in the text; (prac) a practitioner post, single anecdote unless said; (exp) measured here; (inf) inference.

## 0. Where the critic stood

- A claim critic in a private sky-duel film: each card's action split into clauses plus standing claims from reviewer notes, a local VLM (gemma4:26b in Ollama) judging each claim yes / no / unclear on a frame grid, the agent's own reads by eye recorded beside it, and a ledger scoring every prompt variant against the agent. Agreement: v1 (card text given to the judge) 53 %; v2 (no card text, describe first, default no) 79 %; v5 (per-person claims judged on that person's half of native frames) 77 %; v6 (claims keyed by id) 83 % over 624 claims (exp).
- Gates in the companion image skill, measured on 152 of the reviewer's past verdicts: only the speech-extras gate reached reject precision; motion and light stay review-only (exp).
- Nothing scored voices beyond pitch and pace, nothing scored music or effects, and nothing checked sound against picture.

## 1. How people review (manual practice)

- Passes, in order (src, SPOTLIGHT arXiv 2511.18102; MovieLabs QC vocabulary; vendor checklists consistent with each other): real time once, note the first wrong moment; silent continuous (write only the action seen; a different action = structural, reroll); silent with stops at cuts; per element (identity at start, middle, end; props through occlusions; text); sound with eyes closed; the export in another player.
- Note = one record: time range, region, category from a fixed vocabulary, severity 1-5 (how obvious), eight or more words, one fix. Annotators who wrote shorter notes were dropped (src, SPOTLIGHT). Rank by story cost, always give a fix, never ask for the unfixable (src, ProVideo Coalition notes guide).
- Priorities when notes conflict: Murch's Rule of Six (emotion 51 %, story 23 %, rhythm 10 %, eye-trace 7 %, 2D plane 5 %, 3D space 4 %).
- Fresh-eye tricks: mirror the frame; onion skin; linked side-by-side with the previous version; difference image between versions (src, Toon Boom, SyncSketch, RV, Nuke tech-check guides).
- Cut-point check: last second of A beside first second of B: gaze, position, direction, light (src, continuity guides; script-supervisor lists).
- Fault vocabularies to copy: MovieLabs video, audio and production lists (FLICKER, DENSITY-SHIFT, BLENDED-FRAMES, FLASH-FRAME, CONTINUITY-ERROR, COFFEE-CUP, LIP-SYNC, POP-CLICK-TICK, DROPOUTS, LEVEL-SHIFT, DOUBLED-AUDIO, TRUNCATED, SYNC-OFFSET, SYNC-DRIFT, EXTRANEOUS-EFFECT); SPOTLIGHT's AI categories (physics, appearance/disappearance, logical, motion, anatomy, adherence; adherence commonest; anatomy and pop-ins are brief, so they need frame stepping).
- Physics: 83 to 94 % of physics-critical generated clips had a glitch a person could spot (src, arXiv 2603.19607).
- Lip-sync tolerance: detectable at about +45 ms (audio early) to -125 ms (late), acceptable to +90 / -185 ms (ITU-R BT.1359); EBU R37 +40 / -60 ms; at 24 fps about one frame early, one and a half late.
- Voice review (audiobook proofing, ACX, MUSHRA-DG arXiv 2411.12719): word-for-word against the script, stress that contradicts meaning, name pronunciation, unmotivated pauses, character consistency, mouth noise; log defects (mispronunciation, pauses, speed changes, artefacts, energy jumps, skipped words) rather than one naturalness number.
- Cull rates: one commercial ad kept about 15 of 300-400 generations; another 41 of 164; closed-model users report about 1 in 10; a local H3 maker ran 2 takes a clip with an automatic pick and human review only on conflicts (prac and press).
- Calibrating a judge to one expert: binary pass/fail plus a written critique, not 1-5; start with about 30 labelled examples; report true-positive and true-negative rates or Cohen's kappa, never raw agreement; three iterations reached 90 % in one case (src, hamel.dev LLM-judge guide). Expert-to-expert agreement 72-75 %, expert-to-LLM 60-64 % in one study (src, arXiv 2410.20266).

## 2. Vision judges (what is new since 2026-10-12)

- Describe blind, then judge: caption-then-verify caught 79 % of fabricated claims where asking "does the frame support this" caught 0 of 40 (src, arXiv 2608.15574, 2026-08). Same mechanism as our v1 to v2 jump. Test any new prompt under 2-3 paraphrases.
- One pass per fault family: sending the video once per error type raised Qwen3-VL-8B's localisation 1.7x, level with zero-shot Gemini 2.5 Pro (src, SPOTLIGHT). Humans still localise about twice as well.
- VLMs rank better than they score: conformal intervals on score tokens span about 40 % of the scale (src, arXiv 2604.25235). Pairwise with the order swapped for choosing; P(yes) per claim, calibrated, for gates.
- VQAScore: P("Yes") as the score beat question decomposition in its own ablation (src, arXiv 2404.01291).
- Small subjects: accuracy depends on the subject's size in the image while attention still finds it; append a crop of the region to the full image (src, ViCrop arXiv 2502.17422). Gemma 4's per-image visual budget is 70-1120 tokens (default 280 in vLLM), so a 2x2 grid gets about 70 tokens a frame (src, model card): feet and hands at grid size are below what the model sees.
- Left and right: models handle camera-view questions but fail on a person's own left/right (src, ViewSpatial-Bench arXiv 2505.21500). Say screen-left / screen-right, or compute it from detector boxes.
- Frame choice: query- or event-aware selection beats uniform sampling by up to 10 points (src, F2C arXiv 2510.02262); a fast-event benchmark showed Qwen3-VL-8B at 33 % with 2 fps against 45 % at 24 fps (prac, via search). Sample densely around motion peaks.
- Few-shot crops of each known blind spot (ArtifactLens arXiv 2602.09475): a few hundred examples per artifact class gave state of the art; we have labelled crops already.
- Physics judges are gameable: VideoPhy-2-AutoEval, WorldModelBench's judge and PhyJudge barely react to shuffled, frozen or reversed frames, and text overlays raise scores (src, 2026 gameability study). Ask dependency-ordered physics questions instead (PQSG arXiv 2606.25306).
- Local reward models worth a try only as pairwise pickers: UnifiedReward 2.0 on Qwen3.5-9B (fits 16 GB); HPSv3 for still aesthetics; ImageDoctor heatmaps advisory only (false-fires on clean faces and hands).
- Specialists for faults people flag: Hands23 (hand contact state and the touched object), EmotiEffLib/HSEmotion (happy vs fear vs surprise, Apache 2.0, CPU) plus mouth landmarks for smile vs scream, Gaze-LLE (who looks at whom), a person detector with face ids for counts.
- Hosted: Gemini samples video at 1 fps by default with a custom fps and start/end offsets; about 258 tokens a frame at default resolution, 32 tokens a second of audio; a 4 s window at 8 fps costs well under a cent on a Flash model (src, ai.google.dev video docs read 2026-10-15). Use it for escalated timed events, where hearing a scream helps.
- No published artifact-detection numbers for Claude were found.

## 3. Audio and voice judges

- MOS predictors fail on expressive or wild speech: Spearman with human MOS on wild speech UTMOS -0.12, UTMOSv2 0.16, DNSMOS 0.35, NISQA -0.32, Audiobox CE 0.19; only SQUIM-MOS (with a non-matching reference) held at 0.62 (src, TTSDS2 arXiv 2506.19441). MOS predictors collapse onto signal quality and miss linguistic errors (src, arXiv 2608.09930). Use them only A/B between takes of one line.
- Speaker similarity is the best-correlated family (0.47-0.77 with human similarity ratings, TTSDS2), but thresholds are model- and data-specific; two real recordings of one person score about 0.73-0.75 with WavLM-SV. Calibrate per character: refs against each other, refs against other characters, threshold between.
- Words: CTC forced alignment gives a score per word and cannot hallucinate fluent text the way Whisper can; skipped, garbled, repeated words and truncated tails show as low or zero-length words. Phoneme recognition (wav2vec2 espeak) catches homographs. Whisper small models "fix" TTS grammar errors; large-v3 for judging (prac).
- Emotion: use emotion2vec+ class labels and arousal, not embedding cosine (dominated by speaker and words).
- Audio-language judges: pairwise beats pointwise; concatenated clips with four examples is the best format; strong position bias that grows as quality converges (src, AudioJudge arXiv 2507.12705). Gemini Flash agrees with human naturalness preference under 70 %; a fine-tuned Qwen2.5-Omni judge 77-79 % (src, SpeechJudge arXiv 2511.07931). Qwen3-Omni needs about 79 GB in BF16; only experimental GGUF audio in llama.cpp.
- Music and effects: Audiobox Aesthetics (PQ, PC, CE, CU, one model for speech, music, effects; ACE-Step reports PQ 8.35); SongEval for songs with vocals; Beat This! for tempo stability (CPU); CLAP mood ranking against a contrasting prompt, relative only; FAD is set-level and useless per cue.
- Sound against picture: Synchformer DeSync tracks offsets best (tau 0.84) but metrics barely agree with each other and one study saw 900 ms reported on in-sync audio (src, arXiv 2608.25157; Woosh). Flags only, windows of 4.8 s or more. LSE-C/D correlate poorly with people (src, arXiv 2511.04520). Omni models judge whether a sound fits, not timing.
- Spectrograms read by a vision model: fine for structure (gaps, clipping bands, hum lines, click streaks, truncated tails), near chance for words (src, arXiv 2511.13225).
- Practitioner TTS: Qwen3-TTS loops when no end token comes (cap tokens, reroll the seed; a low cap silently truncates), drifts into laughing or humming on long takes, timbre varies per generation (reuse one clone prompt); chunk about 300 characters with several candidates each, Whisper round trip, then denoise, trim stutters, R128 (prac, Chatterbox-Extended, a Qwen3-TTS guide). Clean TTS sounds "spoken into a microphone": low cut and a little reverb seat it in the room. Never stream-copy-concat AAC (118 ms drift over four segments).
- Music cull vocabulary: shimmer on cymbals, reverb tails and sibilants; regenerate a take that starts noisy; stems add their own swirl. Foley: quiet scenes are seed-sensitive (take the loudest of a few seeds), prompt only visible actions, state "no music, no speech" positively (prac, LTX docs).

## 4. Critic loops in agentic generation

- VISTA (arXiv 2510.15831, CVPR 2026): pairwise tournament with both orders (a split counts as a coin flip), then per-dimension critics (visual, audio, context), each a normal, an adversarial and a meta judge; a prompting agent asks whether each fault is a model limit or a prompt problem. Ablations: no pairwise selection fell to 33.3 % win rate from 45.9 %; a normal judge alone fell to 17.2 %, worse than no refinement.
- Verifier quality caps sampling: with an imperfect verifier the best sample count is small (5 or fewer when false positives cost, src arXiv 2411.17501); search overfits a single verifier ("verifier hacking"), an ensemble did best (src, arXiv 2501.09732). At 15-27 minutes a render: cap blind best-of-N near 3, then reroll with the last take and its critique in hand.
- Repair rather than reroll for local faults: VideoRepair (regenerate only misaligned regions), GEARS (repair low-scoring candidates with latent SDEdit, back into the pool).
- Reflection beats blind resampling on hard prompts (ReflectionFlow: 0.10 to 0.81 on hard, 0.95 to 0.97 on easy).
- Iteration side effect: "remove old artifacts but add new ones"; critics find faults better than they fix them (src, CHIEF arXiv 2606.18591).
- Judge reliability: a panel of different-family judges beats one big judge (PoLL); percent agreement misleads, report kappa (83 % with both sides saying yes 80 % of the time is kappa about 0.47); abstain when calibrated confidence is low and escalate (Trust or Escalate, ICLR 2025, over 80 % human agreement at about 80 % coverage); rubric edits that pass validation can still shift a judge by up to 28 points (arXiv 2602.13576), so every rule edit is a regression run on the labelled set.
- Gates on intervals: 27 of 30 correct is a 95 % Wilson interval of 74-97 %; zero keepers rejected out of n bounds the true rate at about 3/n.

## 5. Experiment: P(yes) per claim (2026-10-15)

Ollama 0.35.1 with gemma4:26b returns logprobs for the first generated token only, on /api/generate, /api/chat and /v1, with or without JSON format and streaming (exp). So v7 asks for a description once (image plus prompt, no card text), then each claim alone with a one-word answer; the image and description prefix is cached, so each claim costs 0.3-0.8 s after a 12 s description (exp). Results against the agent's reads (gemma4:26b, Mac Ollama):

| Variant | Claims | Agreement | Kappa |
|---|---|---|---|
| v6 batch, keyed by id (stored run) | 368 | 84.5 % | 0.62 |
| v6 with the claim list reversed | 368 | 78.5 % | 0.55 |
| v7: describe blind, then each claim alone, one-word answer, P(yes) | 74 | 82.4 % (v6 on the same: 91.9 %) | 0.64 |
| v7b: as v7 with a one-sentence reason before a true/false answer | 16 | 68.8 % (v6: 100 %) | 0.43 |

- v7 and v7b were stopped early: asked alone, the judge called false any claim its blind description did not mention ("Neither man is smiling" when faces went undescribed) and flipped negated claims. One reply with all claims, keyed by id, stays the format.
- Both orders together: where they agree (89 % of claims) they are right 86.5 % of the time. The split by verdict is what matters: a yes in both orders was right 228 of 231 times (Wilson 95 % bound 96.3-99.6 %), covering 63 % of all claims; a no in both was right 54 of 95 (47-66 %); 42 claims (11 %) split, and the stored run was right on 29 of those.
- Claims the judge cannot do even on per-person crops: footwear (19 % right), the blade's curve (33 %), a sleeve staying on (33 %). Card clauses ran 72 %.
- Rule taken: accept a both-orders yes; the agent checks every no, split and unclear on full-size frames. In this set that removes the agent's look from about two claims in three.
- Caveat: the labels are the agent's own reads, not the reviewer's, and on some rounds the agent saw the judge's answer before writing its own, which can flatter every figure here. Next: score the same rule on the reviewer's own verdicts.
- The run was stopped at 25 of 44 cards (seven of eleven rounds) when the shared Mac slowed fourfold; the figures were stable from 74 claims on.

## 6. Ranked changes

1. P(yes) per claim with a calibrated abstain band; the band goes to Claude on native-resolution crops, then to a hosted model for timed events. Report kappa and Wilson bounds in the ledger.
2. Geometry before VLM: left/right, people count, gaze to lens, smile vs scream, hand contact from detectors and landmarks; the VLM gets only what geometry cannot answer.
3. Crops as separate images beside the full frame, never a grid, for hands, feet, held props and faces.
4. Take selection by swapped-order pairwise comparison; split verdicts are ties and go to the reviewer.
5. Every reviewer correction becomes a standing claim at once, and a gate only after it passes the labelled set (lower bound 90 %, no keeper rejected); every judge or rule edit is a regression run.
6. One judge pass per fault family, with two to four labelled example crops of its known blind spots.
7. Frames at motion peaks plus 2 s windows at 4 fps for timed events, not uniform quarters.
8. Voice: forced alignment, per-character speaker similarity, a DSP glitch scan, Whisper large-v3 round trip; MOS predictors only A/B.
9. Sound: Audiobox Aesthetics PQ per stem, tempo stability, every effect needs a visible cause; sync metrics as flags only.
10. Reroll budget: about three blind samples, then reroll with the critique; a repair verdict for local faults; classify each fault as a model limit (re-plan) or a prompt cause (edit).
