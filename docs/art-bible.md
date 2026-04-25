# Art bible

## Purpose and authority

This document defines the visual source of truth for Agentland's cosy
pixel-art workplace dashboard. The product fantasy is a tiny Japanese
role-playing game (JRPG) management scene fused with an operational dashboard:
warm, readable, characterful, and disciplined.

The current visual authority is `docs/agentland-design.md`,
`docs/prompt-style-guide.md`, the reference images under
`assets/source/references/`, accepted asset manifests, and this document. More
specific approved manifests take precedence for individual assets.

## Assumptions

- The first runtime uses Rust, `pixels`, and `winit`.
- The virtual framebuffer is fixed at `512x288`.
- Window resize changes only the presentation surface and letterbox viewport.
- The initial scene is a hipster coffee shop where software agents work around
  laptops, terminals, books, coffee, shelves, lamps, plants, and status panels.
- No final runtime art is generated in the bootstrap slice.
- GPT Images 2, through Codex built-in `image_gen`, is a development-time
  authoring path, not a runtime API.
- Runtime-critical text, layout, hit areas, charts, focus states, and status
  semantics are rendered deterministically in Rust.

## Visual grammar

- Anchor the scene in a productive coffee shop, not a generic fantasy room or
  corporate dashboard abstraction.
- Let environmental storytelling support the interface without competing with
  status, text, or controls.
- Use readable sprite-scale forms: clear head shapes, props, poses, furniture
  edges, screen silhouettes, and panel boundaries.
- Keep density disciplined. Small details may imply work in progress, but
  clutter must not obscure agents, panels, or focal paths.
- Express materials with simple pixel clusters: dark walnut wood, brick, brass,
  ceramic mugs, parchment, leather, glass jars, plants, and cyan screens.
- Use brass trim, navy recesses, parchment labels, and cream glyphs as the
  recurring user-interface language.

## Scene layers

The runtime compositor uses this default order:

1. Base background fill.
2. Environment tilemap or backplate.
3. Large props.
4. Characters.
5. Desk and counter foreground overlaps.
6. User-interface backplates.
7. User-interface widgets and icons.
8. Runtime text.
9. Lighting overlays.
10. Cursor, focus rings, tooltips, and debug overlays.

Concept art may collapse these layers for presentation. Runtime assets should
remain separable where separation improves composition, hit testing, lighting,
or iteration.

## Palette intent

Use the palette as a target, not a prison. Generated source images may exceed
it during exploration; approved runtime assets should be quantized or remapped
towards it unless a manifest records an exception.

| Name | Hex | Use |
| --- | --- | --- |
| Near black | `#07101B` | Deepest recesses, outlines, contrast anchors |
| Deep navy | `#0F1A2E` | Primary dashboard surfaces |
| Slate blue | `#1E2B44` | Inactive panels and dark pockets |
| Coffee brown | `#4B2E1A` | Shelves, leather, and dark wood |
| Walnut wood | `#7A4A2B` | Counter, furniture, and prop bases |
| Brass gold | `#D4AF37` | Trim, dividers, and icon accents |
| Warm amber | `#FFB347` | Lamp light and warm highlights |
| Candle glow | `#FFD98A` | Bright light accents and title emphasis |
| Moss green | `#2E5B3F` | Active states and plant accents |
| Screen cyan | `#61D6FF` | Displays, data glow, and robot faces |
| Ember red | `#B94A2E` | Warning and blocked states |
| Cream | `#F2E6C9` | Text, parchment, and readable glyphs |

## Lighting

- Warm amber pendant lamps are the primary mood source.
- Small cyan screen glows identify active work zones and create cool contrast.
- The main work area should read brighter than corners, shelves, and decorative
  background zones.
- Rim highlights on characters, mugs, laptops, brass trim, and panel edges
  preserve readability at 1x scale.
- Lighting overlays must stay restrained: no smeared bloom, excessive blur, or
  shadows that hide interface state.

## Pixel-art constraints

- Prioritize crisp silhouettes over dense internal detail.
- Use controlled dithering and readable pixel clusters.
- Preserve consistent outline weight across characters, props, and ornaments.
- Keep character proportions expressive enough for personality but simple
  enough to read inside a `512x288` scene.
- Avoid generated micro-text in runtime sprites. Runtime text belongs in code.
- Test candidate runtime sprites at 1x, 2x, 3x, and 4x integer scales before
  approval.

## Character direction

Each agent needs a distinct silhouette, role prop, and accent colour so the
roster reads before text labels.

| Character | Role | Visual anchors | Accent intent |
| --- | --- | --- | --- |
| Ava | Research specialist | Auburn hair, apron or waistcoat, laptop or clipboard | Amber, cream, moss green |
| Byte | Operations manager | Rounded robot shell, cyan face display, brass details | Screen cyan, cream, brass |
| Lex | Data analyst | Focused posture, tablet or mug, rolled sleeves | Slate blue, brass, cyan |
| Sage | Knowledge advisor | Hooded silhouette, book or quill, candle-lit face | Coffee brown, moss green, glow |

Nova, Patch, Ember, and Echo remain optional until the core roster has strong
visual consistency.

## Runtime and generation boundary

Use GPT Images 2 for style-book pages, character reference sheets, expression
sheets, environment concepts, prop cutout sources, texture references, and
user-interface ornament references.

Build final text rendering, layout, panels, tabs, charts, meters, status pills,
progress bars, focus rings, hit boxes, debug overlays, and lighting composition
in deterministic Rust or local scripts.

Generated images are not deterministic sprite, animation, tiling,
identity-lock, or layout systems. A generated image becomes a project asset
only after it is copied into the workspace, validated, post-processed where
needed, and recorded in a manifest.

## Rejection rules

Reject generated outputs that break the coffee-shop pixel-art style, obscure
the subject, contain muddy shadows, include watermark-like marks, use real
brand logos, add unwanted slogans, drift character identity, fail at runtime
scale, or bake critical user-interface text into imagery.
