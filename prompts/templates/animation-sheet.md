# Animation sheet prompt template

```plaintext
Use case:
Animation motion reference for Agentland.

Asset type:
Pixel-art animation reference sheet.

Primary request:
Create a reference sheet for [agent name] performing [motion name], such as
idle, blink, typing, thinking, reading, alert, or celebrating. Show [frame
count] clear frame poses with consistent identity and equal visual scale.

Input images: (optional, label each image by role)
Image 1, identity reference: approved character reference for [agent name],
`[path]`.
Image 2, style reference: approved dashboard-world mockup,
`ref/design-book-9.png`.

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
Crisp pixel-art frame poses with controlled dithering, readable silhouettes,
and no blurry anti-aliased subject edges.

Composition/framing:
Arrange frames left to right in a single row or labelled grid. Keep frame
spacing even and leave padding around every pose.

Lighting/mood:
Consistent warm rim light across all frames. Preserve screen-cyan glows or
small display lights only where part of the character identity.

Colour palette:
Use the Agentland master palette and the character accent colours. Avoid
introducing new dominant hues.

Materials/textures:
Keep material details stable across frames: cloth folds, robot shell panels,
books, mugs, screens, tools, or paper props.

Text (verbatim): ""

Constraints:
Do not change costume, silhouette, palette, or role prop between frames. Do
not add labels inside the frame cells. No runtime-critical text; motion names,
frame IDs, and timing metadata will be stored outside the image. Designed as
source or reference art for a 512x288 fixed-virtual-resolution Rust `pixels`
renderer.

Avoid:
Different character identity across frames, motion blur, painterly smearing,
complex background, extra text, and unrequested props.
```
