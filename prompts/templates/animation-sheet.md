# Animation reference sheet prompt template

```text
Use case:
Animation motion reference for Agentland.

Asset type:
Pixel-art animation reference sheet.

Bucket:
1 - direct generated reference by default. Promote to Bucket 2 only after
manual review confirms the sheet is suitable for deterministic slicing and
cleanup.

Primary request:
Create a reference sheet for [agent name] performing [motion name], such as
idle, blink, typing, thinking, reading, alert, or celebrating. Show [frame
count] clear frame poses with consistent identity and equal visual scale.

Input images:
Image 1: approved character reference for [agent name], identity reference,
[path].
Image 2: approved dashboard-world mockup, lighting and palette reference,
`ref/design-book-9.png`.

Visual source of truth:
Preserve the approved Agentland character identity, coffee-shop pixel-art
palette, warm amber rim light, and crisp readable silhouette.

Focal priority:
Pose change first, character identity second, role prop continuity third.

Layer intent:
Motion reference sheet. Final frame timing, sprite bounds, anchors, and loop
rules are deterministic runtime data.

Scene/backdrop:
Plain dark navy background or simple sheet grid. No environmental detail.

Subject:
[agent name] performing [motion name]. Preserve these invariants:
- Head or face/display:
- Clothing or shell:
- Role prop:
- Accent colours:
- Approximate height and scale:

Style/medium:
Crisp pixel-art frame poses with controlled dithering and no blurry
anti-aliased subject edges.

Composition/framing:
Arrange frames left to right in a single row or labelled grid. Keep frame
spacing even and leave padding around every pose.

Lighting zones:
Consistent warm rim light across all frames. Preserve screen-cyan glows or
small display lights only where part of the character identity.

Colour palette:
Use the Agentland master palette and the character accent colours. Avoid
introducing new dominant hues.

Materials/textures:
Keep material details stable across frames: cloth folds, robot shell panels,
books, mugs, screens, tools, or paper props.

Text (verbatim): ""

Runtime text policy:
No runtime-critical text in the image. Motion names, frame IDs, and timing
metadata will be stored outside the image.

Post-processing target:
Reference-only unless a later validation pass records exact crop grid, equal
frame dimensions, identity stability, anchors, and atlas metadata.

Acceptance checks:
Identity remains stable; pose progression reads clearly; frame scale is
consistent; no duplicated limbs that confuse the action; no watermark; no
background clutter.

Constraints:
Do not change costume, silhouette, palette, or role prop between frames. Do
not add labels inside the frame cells.

Avoid:
Different character identity across frames, motion blur, painterly smearing,
complex background, extra text, and unrequested props.
```
