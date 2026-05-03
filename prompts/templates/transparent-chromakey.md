# Transparent chroma-key prompt template

Triage: `[type:docstyle]`

```plaintext
Use case:
Transparent-source cutout for Agentland.

Asset type:
Pixel-art chroma-key source.

Primary request:
Create one isolated [asset name] on a perfectly flat chroma-key background for
local background removal.

Input images: (optional, label each image by role)
Image 1, style reference: approved Agentland mockup or accepted manifest
reference, `[path]`.

Scene/backdrop:
Perfectly flat solid #00ff00 chroma-key background for local background
removal. The background must be one uniform colour with no shadows, gradients,
texture, reflections, floor plane, or lighting variation.

Subject:
[asset name] as a [character accessory / role prop / zone prop / ambient prop /
UI ornament source].
Required details:
- Detail:
- Detail:
- Detail:

Style/medium:
Crisp pixel-art rendering, readable sprite-scale form, controlled dithering, no
painterly smearing, and no blurry anti-aliased subject edges.

Composition/framing:
Single centred subject with generous padding on all sides. Do not crop any
part of the subject.

Lighting/mood:
Small warm amber edge highlight only. No cast shadow, no contact shadow, no
reflection, and no floor plane.

Colour palette:
Use the Agentland master palette. Do not use #00ff00 anywhere in the
subject. If the subject is normally green, shift its hue towards moss or leaf
tones that remain visibly different from #00ff00.

Materials/textures:
[Name material facts: brass, walnut wood, ceramic, leather, paper, glass,
painted shell, metal, cloth, or plants.]

Text (verbatim): ""

Constraints:
Keep the subject fully separated from the background with crisp edges and
generous padding. No extra props unless listed under Subject. No text; any
label, screen content, or status indicator will be rendered by Rust after
processing. After accepting the source, run
`tools/remove_chroma_and_validate.py` with `--auto-key border`, `--soft-matte`,
`--transparent-threshold 12`, `--opaque-threshold 220`, `--despill`, and
`--edge-contract 0`. Retry once with `--edge-contract 1` only if a thin
fringe remains.

Avoid:
Gradients, shadows, floor planes, reflections, watermarks, text, brand logos,
green subject pixels matching #00ff00, and background texture.
```
