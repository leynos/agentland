# Prop cutout prompt template

Triage: `[type:docstyle]`

```plaintext
Use case:
Runtime prop source for Agentland.

Asset type:
Pixel-art prop cutout source.

Primary request:
Create one isolated [prop name] for the Agentland coffee-shop dashboard.
The prop is a [role prop / zone prop / ambient prop / UI icon source].

Input images: (optional, label each image by role)
Image 1, material reference: approved dashboard-world mockup,
`ref/design-book-9.png`.
Image 2, prop vocabulary reference: approved environment guide,
`ref/design-book-11.png`.

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

Lighting/mood:
Small warm amber highlight from upper left. No cast shadow, contact shadow,
or grounding shadow. If the prop has a screen, leave a simple screen area that
Rust can fill later.

Colour palette:
Use the Agentland master palette. Do not use #00ff00 anywhere in the subject.

Materials/textures:
Name the visible material details, such as ceramic rim, brass hinge, walnut
grain, glass screen, paper edge, leather cover, or metal tool shaft.

Text (verbatim): ""

Constraints:
Keep the prop fully separated from the background with crisp edges and generous
padding. Use no cast shadow, no contact shadow, no reflection, and no extra
props unless listed under Subject. No generated text; any sign, screen, label,
or status content will be rendered by Rust. Chroma-key removal is not yet
available. For accepted sources, remove the #00ff00 key manually with these current
steps: duplicate the source locally, key out pure #00ff00 with a hard-edged matte,
run local checks for alpha, key spill, and transparent corners, then save a
transparent PNG. Record the prompt, source, processed path, validation notes, and
post-processing settings in the manifest.

Avoid:
Scene backgrounds, gradients, floor plane, labels, duplicate props, brand
marks, muddy shadows, and green details matching the chroma key.
```
