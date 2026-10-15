---
title: Checking generated voice lines
slug: voice-qc
summary: Cull generated voice lines by recognition round trip and alignment (skipped, extra, cut-off words), per-character speaker similarity, a glitch scan and an emotion check; MOS only between takes.
tags: [voice, tts, qc, asr, alignment, speaker-similarity]
last_checked: 2026-10-15
sources: ["TTSDS2, arXiv 2506.19441 (v2 2026-03)", "Beyond Naturalness, arXiv 2608.09930, 2026-08", "AudioJudge, arXiv 2507.12705, EACL 2026", "SpeechJudge, arXiv 2511.07931, ICLR 2026", "MUSHRA-DG, arXiv 2411.12719", "Seed-TTS-eval, https://github.com/BytedanceSpeech/seed-tts-eval", "Qwen3-TTS cloning guide, https://ocdevel.com/blog/20260302-qwen-tts-voice-cloning (2026-03)", "Chatterbox-TTS-Extended, https://github.com/petermg/Chatterbox-TTS-Extended"]
volatile_claims: ["MOS predictor correlations on expressive speech", "audio-LLM judge agreement figures"]
---

# Checking generated voice lines

## Rules

- Round trip every line through speech recognition and diff it against the script: missing words, extra words (a prompt sentence spoken aloud is the worst case), substitutions. Use a large model (Whisper large-v3); small ones quietly correct the TTS's own errors.
- For word-level faults, force-align the script to the audio (CTC alignment): a word with a very low score or almost no length is skipped or garbled, and speech after the last aligned word is babble. Alignment cannot invent fluent text the way recognition can.
- Truncation: the last word ends under about 80 ms before the file ends while the level is still high. Runaway length (a loop, humming, laughter on a long take) is a reject: cap the token count, reroll the seed.
- Same voice: score each line's speaker embedding against the character's refs. Set the threshold per character, between ref-to-ref scores and ref-to-other-character scores; there is no universal number (two real recordings of one person score about 0.73-0.75 with WavLM-SV).
- Pronunciation of flagged words (names, homographs, respellings): compare recognised phonemes with the intended reading.
- Emotion: check the planned emotion against a classifier's label and the line's pitch range and loudness swing; a flat read has a narrow range whatever the label says. Never use emotion-embedding cosine: speaker and words dominate it.
- Glitches by measurement: clicks as spikes in spectral flux, metallic tone as spectral-flatness outliers, room or noise copied from the reference, an energy jump inside a word.
- Naturalness predictors (UTMOS, DNSMOS, NISQA) compare takes of the same line only; never a pass mark.
- An audio-language model is a tiebreaker: two takes in one file with a beep between, both orders, keep only a consistent answer.
- Generate several candidates per chunk of about 300 characters and keep the first that passes, rather than one long take.
- Seat a clean TTS line in the scene (low cut, a little room reverb, the scene's room tone) or it sounds spoken into a microphone (cinewright-sound).

## Numbers

- Wild-speech correlation with human ratings: UTMOS -0.12, DNSMOS 0.35, NISQA -0.32; speaker similarity 0.47-0.77, the best family.
- Audio-LLM judges: Gemini Flash under 70 % on naturalness preference; a fine-tuned 7B judge 77-79 %.
- Qwen3-TTS reference: 10-15 s, 24 kHz or more, mono, exact transcript; 0.5 s of silence after the reference smooths the first word.

## Pitfalls

- Passing a line on word recall alone: it does not catch extra words or a different voice.
- One naturalness number as a gate.

## Verify

- A line the reviewer rejected for a wrong word, a cut-off ending or another voice fails here.

Related: builds on [voice-measure](voice-measure.md); see also [reference-clips](reference-clips.md).
