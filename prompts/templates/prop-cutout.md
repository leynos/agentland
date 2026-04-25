# Prop cutout prompt template

```text
Use case:
Runtime prop source for Agentland.

Asset type:
Pixel-art prop cutout source.

Bucket:
2 - generated source converted to deterministic reusable pieces.

Primary request:
Create one isolated [prop name] for the Agentland coffee-shop dashboard.
The prop is a [role prop / zone prop / ambient prop / UI icon source].

Input images:
Image 1: approved dashboard-world mockup, material and lighting reference,
`ref/design-book-9.png`.
Image 2: approved environment guide, shared prop vocabulary reference,
`ref/design-book-11.png`.

Visual source of truth:
Use the approved Agentland pixel-art material language: dark walnut wood,
brick, brass trim, ceramic, paper, glass, screen-cyan displays, warm amber
lamp highlights, and deep navy shadow.

Focal priority:
Prop silhouette first, functional details second, material texture third.

Layer intent:
Cutout source for later chroma-key removal, crop, quantization, bounds
validation, and atlas packing.

Scene/backdrop:
Perfectly flat solid #00ff00 chroma-key background for local background
removal. The background must be one uniform colour with no shadows, gradients,
texture, reflections, floor plane, or lighting variation.

Subject:
[prop name] with these required features:
- Overall silhouette:
- Functional details:
- Material:
- Intended runtime size or role:
- Anchor point, if known:

Style/medium:
Crisp pixel-art rendering with readable sprite-scale forms, controlled
dithering, and clean subject edges.

Composition/framing:
Single centred prop, no crop, generous padding on all sides. Use a straight
front, side, or three-quarter view as specified: [view].

Lighting zones:
Small warm amber highlight from upper left. No cast shadow, contact shadow, or
grounding shadow. If the prop has a screen, leave a simple screen area that
Rust can fill later.

Colour palette:
Use the Agentland master palette. Do not use #00ff00 anywhere in the subject.

Materials/textures:
Name the visible material details, such as ceramic rim, brass hinge, walnut
grain, glass screen, paper edge, leather cover, or metal tool shaft.

Text (verbatim): ""

Runtime text policy:
No generated text. Any sign, screen, label, or status content will be rendered
by Rust.

Post-processing target:
Run `tools/remove_chroma_and_validate.py`, crop transparent bounds, quantize
towards the master palette, record anchor and bounds, then pack into the prop
atlas if approved.

Acceptance checks:
Uniform chroma-key background; clean prop separation; no key-colour fringe;
no watermark; no real brand logo; prop reads at 1x, 2x, 3x, and 4x.

Constraints:
Keep the prop fully separated from the background with crisp edges and
generous padding. Use no cast shadow, no contact shadow, no reflection, and no
extra props unless listed under Subject.

Avoid:
Scene backgrounds, gradients, floor plane, labels, duplicate props, brand
marks, muddy shadows, and green details matching the chroma key.
```
