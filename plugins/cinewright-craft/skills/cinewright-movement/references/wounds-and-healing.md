---
title: Wounds and healing
slug: wounds-and-healing
summary: Show a wound appear or heal by pinning a wounded first frame and a clean last frame with only the wound changed, or by reversing a wounding shot; untested end to end.
tags: [movement, wounds, healing, injury, transformation, first-last-frame]
last_checked: 2026-10-14
sources: ["Field lesson 098, 2026-10-13: a local-mark image edit (a cut, blood from the ears) keeps the face; a whole-figure wear edit drifts skin and backdrop", "r/StableDiffusion end-frame overshoot thread, 2026-09-21: https://www.reddit.com/r/StableDiffusion/comments/1wmhny6/", "Kling start and end frames guide: https://kling.ai/quickstart/ai-video-start-end-frames"]
---

# Wounds and healing

Unverified as a whole: no forum or model card found (2026-10-14) shows a wound healing on screen. The parts below are each tested separately.

## Rules

- A wound that appears or heals is a change between two frames. Make the wounded frame from the clean still with a local edit on the wound area only; never edit the whole figure, or skin tone and backdrop drift.
- Pin the wounded still first and the clean still last (or the reverse for an injury). Same framing, same light, same pose; only the wound differs. Larger differences read as a cut.
- Write the change as a process with a direction: "the gash knits closed from its edges inward, the blood darkens, dries and flakes away, leaving smooth skin".
- Keep the camera static and the subject still. Motion plus transformation gives melting.
- Fallback for a tight close-up: render the wound being made and reverse the clip in the edit. Anything else moving in frame then moves backwards too.
- Keep temporary marks (cuts, blood, dirt) in the shot text of the cards they belong to; the clean reference sheet keeps identity.

## Numbers

- 4-6 s per healing shot; first/last-frame tests report cleaner motion on short clips.

## Vocabulary

- first frame, last frame, local edit, knit closed, scab, reverse (in the edit).

## Pitfalls

- First/last-frame models force the end frame: motion overshoots, then snaps back onto the last frame in the final second. Trim the snap or shorten the clip.
- A healed wound that leaves no trace in the next card breaks continuity; carry the scar in wardrobe notes if the story keeps it.

## Verify

- Step through the last second for the snap; compare the face in the first and last frames against the reference sheet.

Related: see also [fights-and-stunts](fights-and-stunts.md), [weight-and-contact](weight-and-contact.md).
