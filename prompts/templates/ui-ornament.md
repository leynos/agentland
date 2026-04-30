# User interface (UI) ornament reference prompt template

```text
Use case:
User-interface ornament reference for Agentland.

Asset type:
Pixel-art UI ornament reference sheet.

Bucket:
Bucket 2, using manifest value `generated-source-converted`. Use
`docs/asset-spec.md` as the canonical bucket source.

Primary request:
Create a clean reference sheet of [ornament family], such as brass corner
caps, dividers, title plaques, number badges, icon badges, swatch frames,
callout tags, status-strip frames, or outer-frame trim.

Input images:
Image 1: approved dashboard-world mockup, UI frame and panel reference,
`ref/design-book-9.png`.
Image 2: approved character roster mockup, card and badge reference,
`ref/design-book-10.png`.
Image 3: approved isometric environment sheet, callout tag reference,
`ref/design-book-12.png`.

Visual source of truth:
Use deep navy recesses, brass-gold trim, cream highlight pixels, clipped
ornamental corners, compact plaques, and disciplined pixel-grid spacing from
the approved mockups.

Focal priority:
Reusable ornament silhouette first, edge readability second, material texture
third.

Layer intent:
Source reference for deterministic UI geometry, nine-slice metrics, or cleaned
ornament sprites. Runtime text, state, layout, and hit areas remain code-owned.

Scene/backdrop:
Simple dark navy sheet background. Keep each ornament isolated with enough
spacing for later crop or redraw.

Subject:
[ornament family] with these variants:
- Variant 1:
- Variant 2:
- Variant 3:
- Variant 4:

Style/medium:
Crisp pixel-art UI ornaments with clean edges, consistent outline weight, and
controlled brass highlights.

Composition/framing:
Arrange variants in rows. Keep corresponding corners, dividers, badges, and
plaques aligned to an implied pixel grid. Avoid full dashboard mockups.

Lighting zones:
Subtle warm highlight on upper or left edges, dark navy inner recesses, and no
glow that would blur the shape.

Colour palette:
Deep navy, slate blue, brass gold, warm amber, candle glow, coffee brown, and
cream. Use screen cyan or moss green only for small accent variants.

Materials/textures:
Brass trim, dark enamel or navy inset, parchment plaque fill, worn wood edge,
or carved corner detail as appropriate.

Text (verbatim): ""

Runtime text policy:
No runtime-critical text. Plaques and badges must leave blank areas for Rust
text or deterministic icons.

Post-processing target:
Crop candidate ornaments, normalize symmetry, define nine-slice metrics where
needed, quantize to palette, and pack approved pieces into a UI atlas.

Acceptance checks:
Clean isolated parts; consistent style across variants; no baked labels; no
watermark; no brand marks; corner and edge pieces can be mirrored or
nine-sliced without visible seams.

Constraints:
Generate ornament parts only. Do not create a full application screen. Keep
blank plaque interiors usable for deterministic text.

Avoid:
Complete dashboard screenshots, decorative text, irregular scaling, soft
blurred edges, overly thin lines, and ornament shapes that cannot be cropped or
redrawn cleanly.
```
