---
title: Delivery color
slug: delivery-color
summary: Deliver web and TV in Rec.709 (BT.1886 gamma 2.4) with matching tags, cinema in DCI-P3, and HDR in PQ or HLG (BT.2100) only from sources with the range for it; encode once, at the end.
tags: [finish, delivery, rec709, p3, hdr, encode]
last_checked: 2026-10-04
sources: ["https://www.itu.int/rec/R-REC-BT.1886", "https://www.itu.int/rec/R-REC-BT.2100", "https://ffmpeg.org/ffmpeg-filters.html", "ASC Manual, 11th ed., 2022"]
---

# Delivery color

## Rules

- Default delivery for AI films: Rec.709 primaries, BT.1886 display gamma (2.4), limited (tv) range, 4:2:0, tagged bt709 for space, primaries and transfer. Grade on a display set to that (a 100-nit Rec.709 reference, or a calibrated monitor in a dim room).
- Web players treat untagged files inconsistently; tag every delivery file, inside the picture (entry color-spaces).
- Cinema (DCP): DCI-P3 primaries, gamma 2.6, XYZ encoding by the DCP tool; a projection reference of 48 cd/m² for SDR. Grade a separate P3 pass; do not just retag a Rec.709 file.
- HDR (PQ per SMPTE ST 2084, or HLG; both in BT.2100): only from sources with more than 8-bit, wide-latitude data. An 8-bit generated clip pushed to HDR shows banding and noise; deliver SDR.
- Encode once, last, after upscale and interpolation: H.264 (`libx264 -crf 16-18 -preset slow`) or H.265 for web, ProRes or DNxHR for a master. Sizes even; frame rate the film's.
- Masters: keep a high-quality master (ProRes 422 HQ or x264 CRF 12, PCM audio) beside each lossy delivery.

## Numbers

- BT.1886: gamma 2.4 (BT.1886-0, 2011); 100 cd/m² is the reference white in its CRT-matching appendix. DCI direct-view SDR: 48 cd/m² ±4.8 (DCI addendum v1.1, 2023; the main DCI spec unchecked this session). BT.2100 current revision: BT.2100-3 (02/2025).
- Rec.709 code values 8-bit limited range: Y 16-235, chroma 16-240.

## Verify

```
ffmpeg -i graded.mov -i mix.wav -map 0:v -map 1:a -vf "setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709" -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -c:a aac -b:a 256k -ar 48000 -movflags +faststart final.mp4
ffprobe -v error -show_entries stream=color_transfer,color_space,color_primaries,color_range -of compact final.mp4
```

- Then `CINE qc spec` on the delivery file against the cards, and `CINE qc loud` against the stated target (cinewright-sound).
