# UI ornament prompt template

```plaintext
Use case:
UI ornament reference for Agentland.

Asset type:
Pixel-art UI ornament reference sheet.

Primary request:
Create a clean reference sheet of [ornament family], such as brass corner
caps, dividers, title plaques, number badges, icon badges, swatch frames,
callout tags, status-strip frames, or outer-frame trim.

Input images: (optional, label each image by role)
Image 1, panel reference: approved dashboard-world mockup,
`ref/design-book-9.png`.
Image 2, card reference: approved character roster mockup,
`ref/design-book-10.png`.
Image 3, callout reference: approved isometric environment sheet,
`ref/design-book-12.png`.

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
Crisp pixel-art UI ornaments with clean edges, consistent outline weight,
controlled brass highlights.

Composition/framing:
Arrange variants in rows. Keep corresponding corners, dividers, badges, and
plaques aligned to an implied pixel grid. Avoid full dashboard mockups.

Lighting/mood:
Subtle warm highlight on upper or left edges, dark navy inner recesses, and no
glow that would blur the shape.

Colour palette:
Deep navy, slate blue, brass gold, warm amber, candle glow, coffee brown, and
cream. Use screen cyan or moss green only for small accent variants.

Materials/textures:
Brass trim, dark enamel or navy inset, parchment plaque fill, worn wood edge,
or carved corner detail as appropriate.

Text (verbatim): ""

Constraints:
Generate ornament parts only. Do not create a full application screen. Keep
blank plaque interiors usable for deterministic text. No runtime-critical text;
plaques and badges must leave blank areas for Rust text or deterministic
icons.
Accepted image-derived ornaments need manifests, `slice`, `palette`, and
`atlas` before runtime use.

Avoid:
Complete dashboard screenshots, decorative text, irregular scaling, soft blurred
edges, overly thin lines, and ornament shapes that cannot be cropped or
redrawn cleanly.
```
