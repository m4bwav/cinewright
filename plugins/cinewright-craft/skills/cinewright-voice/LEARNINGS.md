# Learnings: cinewright-voice

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format: [MAINTENANCE.md](MAINTENANCE.md) (LEARNINGS-FORMAT in the evergreen protocol). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a workaround, an environment fact, a failed test. Check existing entries first: add, update, retire or none. Trigger and Hypothesis are required.

## Active

### L-001 · 2026-10-07 · `llm-ear-misjudges-voices`: a listening LLM drafts, it never judges
- Trigger: 2026-10-07, build test: gemma4 through Ollama called a generated guard's voice female; `voice measure` read a 99 Hz median (male range). It also heard "hallowed halls" as "hollows" and, on one host, two speakers where there was one
- Hypothesis: a 12B multimodal model's audio head is tuned for speech content, not speaker traits, and guesses names it does not know
- Rule: use an LLM's hearing for rough transcripts and first descriptions only; take pitch from `voice measure`, words from the script, identity from an ear or an embedding model
- Evidence: C-20261007-1 (references/ollama-voice.md), confirmed 2026-10-07
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07

### L-002 · 2026-10-07 · `music-corrupts-pitch`: measure the line alone
- Trigger: 2026-10-07, build test: whole 15 s generated shots with score and effects under a man's line read 286 and 343 Hz median, 25 semitones of range
- Hypothesis: the tracker locks onto music partials whenever the voice is quieter than the bed
- Rule: cut to the line's span (or isolate the voice) before `voice measure`, `voice ref` or cloning; trust a measurement only without WARNING lines
- Evidence: C-20261007-1 (`voice measure` warns on low voiced share and range over 18 semitones; references/reference-clips.md), confirmed 2026-10-07
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07

### L-003 · 2026-10-07 · `yin-threshold-0-3`: YIN threshold 0.3, pace over the whole span
- Trigger: 2026-10-07, build test: at threshold 0.2 a low creaky voice was voiced only 37% of its speech and a fast read fell under the warning line; pace over gated time read 260 words a minute for a normal read
- Hypothesis: 0.2 rejects rough low voices; gating removes pauses, so pace was an articulation rate
- Rule: `f0_track` uses 0.3 (medians stayed within 1 Hz on clean clips; a noisy line moved from 286 to 124 Hz); pace divides words by first-to-last speech time
- Evidence: C-20261007-1 (shared/lib/cine.py), confirmed 2026-10-07 (normal read 200 wpm, fast read 321)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-07

### L-004 · 2026-10-10 · `tts-tone-notch`: Qwen3-TTS clone takes carry a steady tone near 1085 Hz; notch it on the joined track
- Trigger: 2026-10-10, a narrator voice for a short film: Qwen3-TTS voice-clone takes (12Hz 1.7B Base, cloned from a VoiceDesign reference) carried a weak steady tone at about 1080-1090 Hz, up to +10 dB above its neighbours in a 1 Hz-resolution long-window spectrum over speech; joined, the lines summed to a visible line
- Hypothesis: an artefact of the model's codec or vocoder, constant across takes, so it adds up where per-take checks miss it
- Rule: measure narrow peaks on the joined track (Welch, 1 Hz bins, minus a median-filtered baseline), not per short take, where held vowels show narrow peaks too; a 30 Hz-wide -12 dB notch (`ffmpeg -af equalizer=f=1085:t=h:w=30:g=-12`) took it to +0.6 dB without changing the voice
- Evidence: measured before and after the notch, 2026-10-10
- Scope: skill
- Status: new · helpful 1 · harmful 0 · last_confirmed 2026-10-10

### L-005 · 2026-10-10 · `spectrogram-draws-a-line`: a line in a showspectrumpic picture is not proof of a tone
- Trigger: 2026-10-10: ffmpeg `showspectrumpic` drew a horizontal line near 1 kHz even on pink noise
- Hypothesis: a rendering artefact of the filter's scaling, not content in the audio
- Rule: never read a line in its picture as a tone; check against a pink-noise control and measure the spectrum (see L-004 `tts-tone-notch`)
- Evidence: pink-noise control rendered with the same settings, 2026-10-10
- Scope: skill
- Status: new · helpful 1 · harmful 0 · last_confirmed 2026-10-10

### L-006 · 2026-10-11 · `clone-copies-the-delivery`: an in-context clone cannot exclaim louder than its reference
- Trigger: 2026-10-11: a narrator's one-word cry ("Land!") came out flat in every take from an in-context (reference audio plus transcript) Qwen3-TTS Base clone of a quiet, grave reference. The pitch fell like a full stop (66-80 Hz against 76-100 Hz in the same voice's ordinary sentences), whatever the punctuation or capitals ("LAND!", "Land!!!", "Land! Land ahead!"). The director called it "too dull, it should be a grand statement".
- Hypothesis: in-context cloning copies the reference's delivery as well as its timbre. Embedding-only cloning (`x_vector_only_mode=True`) keeps the timbre and lets the text drive the prosody.
- Rule: for a shout, cry or exclamation from a cloned voice, generate takes in embedding-only mode and measure the pitch lift before listening (the best rose to about 106 Hz, against 80). A small formant-preserving pitch lift (about +1.6 semitones) adds a little more. Then set the line's level by hand, because loudness normalization misjudges a one-second clip and left the cry quieter than the narration around it. If the cry is still too small, record it, or give it to a character with a designed voice (a voice-design prompt can ask for shouting).
- Evidence: 23 measured takes across five wordings and two clone modes, 2026-10-11
- Scope: skill
- Status: new · helpful 1 · harmful 0 · last_confirmed 2026-10-11
