# Character reference sheet prompt template

```text
Use case:
Character identity reference for Agentland.

Asset type:
Pixel-art character reference sheet.

Bucket:
Bucket 1, using manifest value `direct-generated-reference`. Use
`docs/asset-spec.md` as the canonical bucket source.

Primary request:
Create one clean reference sheet for [agent name], the [role]. Show a
full-body standing pose, a seated or working pose, three expression chips, and
three accessory callouts.

Input images:
Image 1: approved dashboard-world mockup, style and palette reference,
`ref/design-book-9.png`.
Image 2: approved character roster mockup, roster proportions and card
hierarchy reference, `ref/design-book-10.png`.

Visual source of truth:
Use the approved Agentland mockups for warm coffee-shop pixel art, deep navy
panel recesses, brass trim, cream labels, amber lamp light, and screen-cyan
work glows.

Focal priority:
Character silhouette first, face or display second, role prop third,
accessory callouts fourth.

Layer intent:
Reference sheet for identity and future sprite cleanup. Do not create a final
runtime sprite atlas.

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
Crisp pixel-art rendering with readable sprite-scale forms and controlled
dithering.

Composition/framing:
One large standing pose on the left, one smaller seated or working pose near
the centre, three expression chips in a right-side rail, and three accessory
callouts in a lower strip.

Lighting zones:
Warm amber rim light on the character, small screen-cyan glow only where
identity requires it, and no heavy shadow over the face or role props.

Colour palette:
Deep navy, coffee brown, walnut wood, brass gold, warm amber, candle glow,
moss green, screen cyan, ember red, and cream. Keep the named accent colours
for this character visible but restrained.

Materials/textures:
Use visible materials from the identity invariants, such as apron cloth,
brass trim, ceramic mug, paper notebook, glass screen, leather book, or
painted robot shell.

Text (verbatim): ""

Runtime text policy:
No runtime-critical text in the image. Names, roles, labels, statuses, and
user interface (UI) copy will be rendered by Rust.

Post-processing target:
Reference-only manifest first. Future processing may crop portraits,
accessories, expressions, or pose references into deterministic runtime assets.

Acceptance checks:
Readable silhouette at small scale; identity matches the roster; accessories
are distinct; expression chips do not drift identity; no watermark; no real
brand logo; no extra slogans.

Constraints:
Keep all poses on one sheet. Keep the background simple. Keep hands, props,
face, and display areas clear enough for later cleanup.

Avoid:
Tiny unreadable labels, duplicated text, realistic rendering, blurred subject
edges, muddy shadows, modern brand marks, and unrelated props.
```
