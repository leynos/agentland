# Transparent chroma-key prompt template

```text
Use case:
Transparent-source cutout for Agentland.

Asset type:
Pixel-art chroma-key source.

Bucket:
2 - generated source converted to deterministic reusable pieces.

Primary request:
Create one isolated [asset name] on a perfectly flat chroma-key background for
local background removal.

Input images:
Image 1: approved Agentland mockup or accepted manifest reference, [path].

Visual source of truth:
Use the approved Agentland coffee-shop pixel-art style: readable silhouettes,
warm amber highlights, deep navy shadows, brass accents, walnut wood, ceramic,
paper, glass, screen-cyan glow where appropriate, and controlled dithering.

Focal priority:
Subject silhouette first, functional details second, material texture third.

Layer intent:
Cutout source only. Runtime bounds, anchors, hit areas, palette mapping, and
atlas placement will be deterministic.

Scene/backdrop:
Perfectly flat solid #00ff00 chroma-key background for local background
removal. The background must be one uniform colour with no shadows, gradients,
texture, reflections, floor plane, or lighting variation.

Subject:
[asset name] as a [character accessory / role prop / zone prop / ambient prop
/ UI ornament source].
Required details:
- Detail:
- Detail:
- Detail:

Style/medium:
Crisp pixel-art rendering, readable sprite-scale form, controlled dithering,
no painterly smearing, and no blurry anti-aliased subject edges.

Composition/framing:
Single centred subject with generous padding on all sides. Do not crop any
part of the subject.

Lighting zones:
Small warm amber edge highlight only. No cast shadow, no contact shadow, no
reflection, and no floor plane.

Colour palette:
Use the Agentland master palette. Do not use #00ff00 anywhere in the subject.
If the subject is normally green, shift its hue towards moss or leaf tones that
remain visibly different from #00ff00.

Materials/textures:
[Name material facts: brass, walnut wood, ceramic, leather, paper, glass,
painted shell, metal, cloth, or plants.]

Text (verbatim): ""

Runtime text policy:
No text. Any label, screen content, or status indicator will be rendered by
Rust after processing.

Post-processing target:
Run `tools/remove_chroma_and_validate.py` with `--auto-key border`,
`--soft-matte`, `--transparent-threshold 12`, `--opaque-threshold 220`,
`--despill`, and `--edge-contract 0`. Retry once with `--edge-contract 1` only
if a thin fringe remains.

Acceptance checks:
Uniform #00ff00 background; transparent corners after removal; clean alpha;
no key-colour fringe; subject coverage is sufficient; silhouette reads at
runtime scale; manifest records source, prompt, settings, processed path, and
validation notes.

Constraints:
Keep the subject fully separated from the background with crisp edges and
generous padding. No extra props unless listed under Subject.

Avoid:
Gradients, shadows, floor planes, reflections, watermarks, text, brand logos,
green subject pixels matching #00ff00, and background texture.
```
