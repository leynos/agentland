# Environment sheet prompt template

```plaintext
Use case:
Environment reference for Agentland.

Asset type:
Pixel-art environment sheet.

Primary request:
Create an environment sheet for [environment name], a [perspective type]
workspace where agents [function].

Input images: (optional, label each image by role)
Image 1, style reference: approved dashboard-world mockup,
`ref/design-book-9.png`.
Image 2, environment-card reference: approved locations guide,
`ref/design-book-11.png`.
Image 3, spatial-zone reference: approved isometric environment sheet,
`ref/design-book-12.png`.

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
Use a clear room or scene layout with obvious work areas and walking or viewing
clearance. Do not let decorative clutter obscure characters, screens, or future
UI panels.

Lighting/mood:
Warm amber lamp pools, screen-cyan work glows, readable focal areas at 1x,
controlled shadow pockets, and rim light on important silhouettes.

Colour palette:
Use Agentland deep navy, coffee brown, walnut wood, brass gold, warm amber,
candle glow, moss green, screen cyan, ember red, and cream. Add local accents
only when tied to the environment function.

Materials/textures:
Name the expected materials, such as brick, wood, brass, ceramic, leather,
paper, glass, plants, metal, stone, or circuit boards.

Text (verbatim): ""

Constraints:
Preserve the Agentland material language and 512x288 runtime fit. Keep
functional zones clear enough to guide deterministic layout later. Any labels,
callouts, status text, signs, and screen content are reference only unless
quoted exactly; runtime copy will be rendered by Rust.

Avoid:
Generic office styling, overfilled shelves that obscure the scene, blurred
glows, unreadable micro-text, unrelated signage, and layout decisions that
should belong to runtime code.
```
