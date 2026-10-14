---
title: Violence, wounds, healing and flying people on local video models
summary: Forum and model-card research (2026-10-14) on impalement, real fights, a wound that heals and flying people with MiniMax H3; nothing is refused locally, fight LoRA advice conflicts, healing has no source, flying works from storyboards.
tags: [research, violence, fights, wounds, healing, flying, levitation, minimax-h3, lora]
date: 2026-10-14
---

# Violence, wounds, healing and flying people on local video models

Question (the user): can the local video models show a person impaled, a wound that then heals, real fights, and flying people?

Method: web searches (Hugging Face, Civitai, guides), Reddit r/StableDiffusion through its public RSS (search and thread feeds, one request every 30-40 s), the model cards of the fight LoRAs, and the field record of earlier local renders.

## Findings

- **Content filter.** The local H3 weights refuse nothing. MiniMax's hosted service strips blood. A hosted third-party H3 endpoint rendered 36 of 36 gore probes unsoftened; a commenter there says the model "wasn't trained for the upper rungs", which is an anatomy limit, not a refusal. Source: https://spicyapi.ai/reviews/minimax-h3-image-lora
- **Impalement.** No LoRA or thread targets it. In the field record, text alone gave a muddled impact; a still of the contact pinned as a guide frame made lances drive into shields with blood (field lesson 015). Forum alternative: a storyboard or sketch-sequence image as a reference with a stated role. Sources: https://www.reddit.com/r/StableDiffusion/comments/1x050ne/, https://www.reddit.com/r/StableDiffusion/comments/1w9ew6g/
- **Fights.** One tester ran 24 renders changing one setting at a time on a trident-and-spear fight scored by a vision model (https://www.reddit.com/r/StableDiffusion/comments/1wtcitg/): run a step-distilled LoRA only at its trained step count (all 8-step arms "lost the kill"); Combat Base V2 at 0.7 and 1.0 brought weapon morphing back; RunningHub Weapon Combat (`BUNNY`) at 0.7 scored best; HyperFlow at 8 steps with no other LoRA had the best weapon consistency for about 25% more time; the original HyperFlow node double-patches a cached model. The field record found the opposite for swords and axes (Combat Base V2 at 0.9 won a same-seed test), so the conflict stays open until a same-seed spear test. Combat Base V2's card: `prfight2, prfin1` for heavy stunt impact. JOKER141's Fight Flow LoRA targets fighters resetting between blows. Commenters agree one LoRA beats a stack. Cards: https://huggingface.co/JOKER141/MiniMax-H3-Combat-Base-V2, https://huggingface.co/RunningHubAI/rh-v1-weapon-combat-lora, https://huggingface.co/JOKER141/H3-Fight-Flow-Fight-Interaction-LoRA, https://huggingface.co/Jojocodex/minimax-h3-wushu-action-lora
- **Wound then healing.** No source found on any model. The plan in [wounds-and-healing](../../plugins/cinewright-craft/skills/cinewright-movement/references/wounds-and-healing.md) joins tested parts: a local-mark edit for the wounded frame (field lesson 098), first and last frames pinned, and the warning that first/last-frame H3 forces its end frame (overshoot, then snap back; https://www.reddit.com/r/StableDiffusion/comments/1wmhny6/).
- **Flying.** The Superman vs Saitama maker got a hero floating over Earth from a storyboard reference plus a character sheet in 29+ renders, and found first/end frames stable for one continuous move. The field record: "as though from wires" drew wires; "floating free, held up by nothing but sorcery" did not (library film test, 2026-10-06); a small dark upright shape in the sky reads as a person (field lesson 099).

## Landed

- cinewright-movement: [fights-and-stunts](../../plugins/cinewright-craft/skills/cinewright-movement/references/fights-and-stunts.md) (contact, blood, one LoRA, long weapons), new [wounds-and-healing](../../plugins/cinewright-craft/skills/cinewright-movement/references/wounds-and-healing.md) and [flying-and-levitation](../../plugins/cinewright-craft/skills/cinewright-movement/references/flying-and-levitation.md).
- cinewright-genvideo: [minimax-h3](../../plugins/cinewright/skills/cinewright-genvideo/references/minimax-h3.md) rules on violence, fight LoRAs and the forced end frame.
- The private image-generation skill got the same findings with local detail.

## Open

- Same-seed spear test: Weapon Combat at 0.7 against Combat Base V2 at 0.9.
- A healing test both ways (first/last frame, reversed wounding).
