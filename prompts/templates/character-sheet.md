# Character sheet prompt template

```plaintext
Use case:
Character identity reference for Agentland.

Asset type:
Pixel-art character reference sheet.

Primary request:
Create one clean reference sheet for [agent name], the [role]. Show a
full-body standing pose, a seated or working pose, three expression chips, and
three accessory callouts.

Input images: (optional, label each image by role)
Image 1, style reference: approved dashboard-world mockup,
`ref/design-book-9.png`.
Image 2, roster reference: approved character roster mockup,
`ref/design-book-10.png`.

Scene/backdrop:
Simple dark navy sheet background with subtle brass dividers and enough
negative space for clean inspection.

Subject:
[agent name] with these identity invariants:
- Silhouette:
- Face, hair, hood, display, or head shape:
- Clothing or shell:
- Posture:
- Role props:
- Accent colours:

Style/medium:
Crisp pixel-art rendering, readable silhouettes, controlled dithering, no
painterly smearing, no blurry anti-aliased subject edges, clear sprite-scale
forms.

Composition/framing:
One large standing pose on the left, one smaller seated or working pose near
the centre, three expression chips in a right-side rail, and three accessory
callouts in a lower strip.

Lighting/mood:
Warm amber rim light on the character, small screen-cyan glow only where
identity requires it, and no heavy shadow over the face or role props.

Colour palette:
Deep navy, coffee brown, walnut wood, brass gold, warm amber, candle glow,
moss green, screen cyan, ember red, and cream. Keep the named accent colours
for this character visible but restrained.

Materials/textures:
Use visible materials from the identity invariants, such as apron cloth, brass
trim, ceramic mug, paper notebook, glass screen, leather book, or painted robot
shell.

Text (verbatim): ""

Constraints:
Keep all poses on one sheet. Keep the background simple. Keep hands, props,
face, and display areas clear enough for later cleanup. No runtime-critical
text; names, roles, labels, statuses, and UI copy will be rendered by Rust.
Designed as source or reference art for a 512x288 fixed-virtual-resolution Rust
pixels renderer.

Avoid:
Tiny unreadable labels, duplicated text, realistic rendering, blurred subject
edges, muddy shadows, modern brand marks, and unrelated props.
```
