# Environment sheet prompt template

```text
Use case:
Environment reference for Agentland.

Asset type:
Pixel-art environment sheet.

Bucket:
1 - direct generated reference, or 2 - generated source converted to
deterministic reusable pieces when the sheet is explicitly meant for backplate,
tile, or prop extraction.

Primary request:
Create an environment sheet for [environment name], a [perspective type]
workspace where agents [function].

Input images:
Image 1: approved dashboard-world mockup, coffee-shop visual authority,
`ref/design-book-9.png`.
Image 2: approved locations guide, environment-card hierarchy reference,
`ref/design-book-11.png`.
Image 3: approved isometric environment sheet, spatial-zone reference,
`ref/design-book-12.png`.

Visual source of truth:
Use the approved Agentland mockups for cosy pixel-art workplace materials,
disciplined panel hierarchy, warm amber lighting, screen-cyan work glows, and
clear functional zones.

Focal priority:
Primary work zone first, active agents or scale markers second, signature
props third, ambient detail fourth.

Layer intent:
Environment concept and spatial reference. Runtime layout, camera framing,
layer order, hit areas, and UI overlays remain deterministic.

Scene/backdrop:
[side-view coffee shop / isometric room / location card / material study]
showing these zones:
- Zone 1:
- Zone 2:
- Zone 3:
- Zone 4:

Subject:
[environment name] with mood [mood] and function [function]. Include these
signature props:
- Prop:
- Prop:
- Prop:

Style/medium:
Crisp pixel-art environment reference with readable silhouettes, controlled
dithering, clear furniture edges, and no painterly smearing.

Composition/framing:
Use a clear room or scene layout with obvious work areas and walking or
viewing clearance. Do not let decorative clutter obscure characters, screens,
or future UI panels.

Lighting zones:
Key light:
Secondary glow:
Readable areas at 1x:
Shadow pockets:
Rim-light targets:

Colour palette:
Use Agentland deep navy, coffee brown, walnut wood, brass gold, warm amber,
candle glow, moss green, screen cyan, ember red, and cream. Add local accents
only when tied to the environment function.

Materials/textures:
Name the expected materials, such as brick, wood, brass, ceramic, leather,
paper, glass, plants, metal, stone, or circuit boards.

Text (verbatim): ""

Runtime text policy:
Any labels, callouts, status text, signs, and screen content are reference
only unless quoted here for a design-book page. Runtime copy will be rendered
by Rust.

Post-processing target:
Reference-only inspection unless explicitly marked for layer extraction. If
promoted, split into backplate, large props, foreground overlaps, material
tiles, and light-origin notes.

Acceptance checks:
Mood and function are clear; zones are readable; palette matches the approved
mockups; lighting does not hide focal areas; no real brand logos; no
unrequested slogans; no critical text baked into runtime source.

Constraints:
Preserve the Agentland material language and 512x288 runtime fit. Keep
functional zones clear enough to guide deterministic layout later.

Avoid:
Generic office styling, overfilled shelves that obscure the scene, blurred
glows, unreadable micro-text, unrelated signage, and layout decisions that
should belong to runtime code.
```
