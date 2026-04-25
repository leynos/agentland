# Art bible

## Purpose and authority

This document translates the approved mockups under `ref/` into
implementation-grade art direction for Agentland. The current visual source of
truth is:

- `ref/design-book-9.png`: dashboard world, palette, agent status cards, and
  visual pillars.
- `ref/design-book-10.png`: character roster and personality guide.
- `ref/design-book-11.png`: locations, environment guide, and shared prop
  vocabulary.
- `ref/design-book-12.png`: isometric environment sheets, spatial zones, and
  scale references.

The mockups are style authority, not runtime screenshots to slice wholesale.
The Rust renderer owns layout, text, panels, charts, status semantics, hit
areas, lighting composition, and animation timing. Generated art supplies
references, source sheets, and cutout candidates only after provenance,
validation, and post-processing are recorded.

`docs/imagegen-workflow.md`, `docs/asset-spec.md`, accepted manifests, and the
prompt templates under `prompts/templates/` govern how new generated assets are
created and promoted.

## Mockup reading

The approved visual language is a design-book treatment of a cosy,
productive workplace dashboard. The key pattern is not the poster layout; it is
the combination of warm material detail, disciplined user-interface hierarchy,
agent personality, and deterministic operational widgets.

- `design-book-9.png` establishes the main runtime fantasy: a side-view
  coffee-shop dashboard scene with agents working behind a long counter, warm
  shelves and lamps, status cards, roster chips, palette swatches, visual
  pillars, and future location thumbnails.
- `design-book-10.png` defines the roster format: numbered character cards
  with full-body pose, expression rail, accessory strip, role label, and short
  personality note.
- `design-book-11.png` defines environment cards: wide scene viewport, mood
  and function rows, lighting and material notes, local palette chips, and a
  bottom strip of common world props.
- `design-book-12.png` defines spatial planning: isometric room diagrams,
  functional callouts, scale reference strips, and clear zones for work,
  research, collaboration, maintenance, and rest.

## Runtime focal order

Every runtime screen should preserve this focal order:

1. The active world scene or workspace.
2. The active agents and their readable silhouettes.
3. Operational state: status cards, task progress, alerts, charts, and focus
   rings.
4. Role and zone props that clarify what the agents are doing.
5. Ambient environmental detail.
6. Decorative trim and page-chrome echoes.

Design-book pages may include explanatory panels, captions, callouts, and
palette blocks. Runtime screens borrow their hierarchy, materials, spacing, and
ornamental vocabulary, but not their poster-page framing.

## Layer grammar

The side-view dashboard scene uses this layer order:

1. Base navy or near-black fill.
2. Environment backplate: brick, shelves, wall signs, distant props, and
   shadow pockets.
3. Large props: counter, espresso machine, terminal banks, plants, seating,
   archive shelves, workshop benches, or garden fixtures.
4. Characters and role props.
5. Foreground overlaps: counter lip, desks, table edges, chair backs, and
   partial prop occluders.
6. User-interface backplates: scene frame, cards, plaques, tabs, and panels.
7. User-interface widgets: icons, charts, meters, status pills, and progress
   bars.
8. Runtime text.
9. Lighting overlays: lamp pools, screen glows, rim highlights, and vignette.
10. Cursor, focus rings, tooltips, debug overlays, and hit-box overlays.

Reference sheets may collapse layers for readability. Runtime assets should
remain separable whenever separation improves hit testing, palette control,
lighting, or iteration.

## Palette strategy

The palette is a contract for runtime clarity, not a limit on exploratory
reference images. Generated sources may contain richer colour, but approved
runtime assets should be quantized or remapped towards the master palette unless
a manifest records an exception.

| Name | Hex | Primary use |
| --- | --- | --- |
| Near black | `#07101B` | Deep outlines, recesses, and contrast anchors |
| Deep navy | `#0F1A2E` | Primary dashboard surfaces and night interiors |
| Slate blue | `#1E2B44` | Inactive panels, subtitle text, and shadowed pockets |
| Coffee brown | `#4B2E1A` | Leather, darkest wood, books, and shelf shadows |
| Walnut wood | `#7A4A2B` | Counter fronts, furniture, floorboards, and prop bases |
| Brass gold | `#D4AF37` | Trim, dividers, corner ornaments, and icon accents |
| Warm amber | `#FFB347` | Lamp light, warm highlights, and active attention points |
| Candle glow | `#FFD98A` | Bright lamp centres, title emphasis, and rim highlights |
| Moss green | `#2E5B3F` | Positive state, plants, research accents, and garden zones |
| Screen cyan | `#61D6FF` | Robot faces, monitors, data glow, and active analysis |
| Ember red | `#B94A2E` | Warning, blocked, busy, and heat accents |
| Cream | `#F2E6C9` | Runtime text, parchment, labels, and readable glyphs |
| Neon magenta | `#D84FA3` | Data-loft signage and rare high-energy accents |
| Leaf green | `#75A65A` | Plant highlights and friendly positive details |

Use ramps rather than single flat colours. At minimum, runtime and
post-processing tools should define ramps for navy, wood, brass, amber glow,
screen cyan, moss, cream, and warning states. Brass and cream must stay
distinct so labels do not disappear into trim.

## Character roster

The approved roster contains eight agents. The first runtime slice may focus on
Ava, Byte, Lex, and Sage, but the art bible records the full cast because the
mockup already establishes their silhouettes, roles, and accessory language.

| Agent | Role | Silhouette and identity anchors | Role props | Accent colours |
| --- | --- | --- | --- | --- |
| Ava | Research specialist | Auburn hair, practical apron or waistcoat, thoughtful posture | Clipboard, laptop, mug, notebook | Warm amber, cream, moss green |
| Byte | Operations manager | Rounded white robot shell, cyan face display, blue ear modules, brass details | Mug, gear, terminal device | Screen cyan, brass, cream |
| Lex | Data analyst | Dark swept hair, rolled sleeves, focused standing or seated pose | Mug, glasses, calculator or tablet | Slate blue, screen cyan, brass |
| Sage | Knowledge advisor | Hooded robe, dark face recess, cyan eye glow, calm pose | Books, quill, notes, small lamp glow | Coffee brown, moss green, candle glow |
| Nova | Systems engineer | Dark outfit, headset silhouette, resourceful operator stance | Headphones, wrench, repair kit | Screen cyan, slate blue, ember red |
| Patch | Tech tinkerer | Goggles, cap, work vest, tool-ready posture | Screwdriver, circuit board, small tools | Moss green, warm amber, brass |
| Ember | Community liaison | Red hair, open stance, energetic expression, casual workwear | Megaphone, heart badge, mug | Ember red, warm amber, cream |
| Echo | Support assistant | Small hovering robot body, wing-like side shapes, cyan face display | Halo ring, cube, support beacon | Screen cyan, candle glow, brass |

Character sheets must capture a full-body pose, seated or working pose,
expression chips, accessory callouts, and identity notes. Runtime sprites must
then be cleaned into fixed bounds, shared scale, stable anchors, and palette
fit.

## Environment definitions

The coffee shop is the initial runtime environment. Other locations are design
targets for later slices and should keep the same material discipline.

| Environment | Mood | Function | Signature zones | Lighting |
| --- | --- | --- | --- | --- |
| Hipster coffee shop | Warm, welcoming, productive | Casual work, quick syncs, ideation | Briefing desk, espresso bar, collab tables, lounge corner | Warm pendant lamps, shelf glow, screen cyan |
| Library archive | Quiet, focused, timeless | Deep research and knowledge preservation | Terminal bank, archive stacks, reading nook, research table | Desk lamps, sconces, shelf shadows |
| Neon data loft | Energetic, modern, collaborative | Team sprints, brainstorming, analysis | Data-wall displays, server racks, analysis table, workshop bench | Cool LEDs, cyan displays, magenta signage |
| Rooftop garden workspace | Calm, refreshing, inspiring | Solo focus, writing, creative thinking | Plant terrace, focus booths, meeting circle, outlook deck | String lights, natural sun, city dusk |
| Observatory terrace | Serene, expansive, reflective | Long-term strategy and planning | Telescope deck, lantern table, skyline rail | Lanterns, starlight, cool night fill |
| Bot workshop | Hands-on, inventive, industrious | Building, prototyping, maintenance | Tool wall, workbench, parts shelves, diagnostic screens | Task lamps, industrial lights, screen glow |

Environment prompts and manifests should record mood, function, lighting,
materials, zones, local palette, reusable props, and whether the perspective is
side-view, isometric, card view, or texture study.

## Prop definitions

Props are role and zone identifiers before they are decoration. A viewer should
understand agent function and room function from props even before reading
labels.

- Coffee-shop anchors: espresso machine, mugs, cups, jars, bottles, shelves,
  chalkboard frame, pendant lamps, potted plants, counter stools, notebooks,
  laptops, and receipts.
- Knowledge props: books, notebooks, archive boxes, ladders, globe, quill,
  parchment notes, reading lamps, and tagged stacks.
- Data props: monitors, terminal banks, small screens, status LEDs, server
  racks, cable trays, tablets, calculators, and analytics boards.
- Workshop props: screwdrivers, wrenches, circuit boards, small parts boxes,
  diagnostic tools, workbench lamps, and component trays.
- Garden props: planters, terracotta pots, string-light poles, chairs, small
  tables, watering cans, and plant shelves.
- Observatory props: telescope, lanterns, star charts, stone floor, skyline
  rail, and glass.
- Character accessories: each roster member gets one to three role-defining
  accessories that can become either cleaned props or deterministic user
  interface (UI) icons.

Runtime props need bounds, anchor points, layer assignment, optional hit area,
and light-response notes. If a prop has a screen or sign, the prop frame may be
image-derived, but the content is rendered by Rust.

## UI component families

The mockups establish a coherent set of panel families:

| Family | Visual treatment | Runtime rule |
| --- | --- | --- |
| Hero scene frame | Large navy recess, brass border, clipped ornamental corners | Deterministic panel geometry; optional ornament sprites |
| Agent status card | Compact card with name, two task rows, icon chips, and status pill | Rust owns text, icons, status, progress, and layout |
| Character roster card | Portrait or full-body slot, name band, role label, accessory area | Generated portraits may be processed; labels are Rust text |
| Environment card | Wide image slot, mood/function rows, material notes, palette chips | Reference-page pattern; runtime uses cards only if code-built |
| Isometric callout | Small brass-edged tag with connector line | Deterministic annotation geometry and text |
| Palette strip | Swatch row with captions | Palette data and labels are deterministic |
| Prop vocabulary strip | Repeated prop cells with icon and label | Prop icons may be processed; text is deterministic |
| Footer note band | Low-height explanatory or status strip | Code-built layout and text |
| Outer ornament frame | Corner caps, divider strokes, centre medallion, brass flourishes | Crop, redraw, or render algorithmically with nine-slice metrics |

The runtime should favour nine-slice panels, fixed grid metrics, shared spacing
tokens, and reusable component families over one-off bitmaps.

## Typography behaviour

Generated mockup text is reference text unless explicitly promoted by a
manifest. Runtime-critical text belongs in Rust.

Typography roles:

- Page title: large cream or brass pixel-serif reference treatment for
  design-book pages only.
- Section plaque: compact uppercase cream or brass label in a navy plaque.
- Card title: agent, location, or panel name in cream with restrained brass
  emphasis.
- Role label: smaller accent-colour text tied to character or location role.
- Metadata label: `Mood`, `Function`, `Lighting`, `Materials`, `Status`, and
  similar labels rendered deterministically.
- Status text: short operational words such as `NORMAL`, `BUSY`, `FOCUSED`,
  `ACTIVE`, `WARNING`, or `BLOCKED`.
- Callout tag: one to three words naming a spatial zone.
- Palette caption: swatch name and hex value in documentation or tooling
  views.

If generated text is requested for a reference sheet, the prompt must quote it
under `Text (verbatim)`, specify placement and typography, and require no
duplicate text. Generated text must not become authoritative runtime copy.

## Lighting notes

Lighting must preserve crisp pixel readability. No glow should blur character
faces, status text, small icons, or prop silhouettes.

Named lighting presets:

- `coffee-shop-amber`: warm pendant pools, shelf glints, dark corners, and
  cyan monitor counterpoints.
- `library-sconce`: desk lamp circles, wall sconces, shelf shadows, and low
  amber edges.
- `neon-data-cyan-magenta`: cyan data walls, magenta signage, cool monitor
  glows, and dark industrial surfaces.
- `garden-string-light`: small amber bulbs, leaf highlights, dusk background,
  and softer outdoor shadow.
- `observatory-lantern-starlight`: lantern warmth, cool sky fill, star points,
  and telescope rim highlights.
- `workshop-task-lamp`: focused bench lamps, metallic highlights, small status
  LEDs, and denser shadow pockets.

Runtime lighting masks are deterministic. Generated environment art may guide
light placement, but lamp pools, screen glow, vignette, and active-state pulses
must be generated by scripts or Rust with fixed origins, alpha budgets, blend
modes, and layer order.

## Asset inventory

Use the canonical classification values in `docs/asset-spec.md` for
implementation. The list below uses the numeric bucket shorthand only for
readability:

- Bucket 1 (`direct-generated-reference`): approved design-book pages, future
  style-book pages, roster overviews, individual character reference sheets,
  animation reference sheets, environment concepts, typography references, and
  presentation-only icon mood.
- Bucket 2 (`generated-source-converted`): standing sprites, seated sprites,
  portrait chips, expression chips, accessory crops,
  coffee-shop backplate layers, material tiles, espresso machine, lamps,
  shelves, books, mugs, plants, laptops, desk clutter, sign frames, brass
  corners, plaques, and outer-frame ornaments.
- Bucket 3 (`algorithmic`): nine-slice panels, tabs, status cards, status
  pills, charts, progress bars, deterministic icons, bitmap text layout,
  palette files, colour ramps, light masks, focus rings, hit-test data, atlas
  metadata, validation reports, and Day 2 request JSON.

Bucket 1 assets are visual authority only. Bucket 2 assets are not runtime
assets until cleaned and validated. Bucket 3 assets define runtime truth.

## Post-processing requirements

Any image-derived runtime candidate must pass the relevant checks before a
manifest can mark it `approved-runtime`:

- The prompt and source image exist in the workspace.
- The source path is not only under `$CODEX_HOME`.
- Chroma-key cutouts have clean alpha, transparent corners, no key-colour
  fringe, and documented removal settings.
- Crops and slices use reproducible coordinates or grid metadata.
- Sprite bounds, anchors, foreground overlaps, and hit areas are recorded.
- Palette normalization keeps silhouettes and important material contrasts
  readable.
- Runtime scale checks pass at 1x, 2x, 3x, and 4x where practical.
- Atlas metadata matches the packed image exactly.
- Runtime-critical text is absent from the image or explicitly ignored.

## Deterministic surface

The following must be deterministic and testable:

- Virtual resolution, integer scaling, letterboxing, and input mapping.
- Scene layout, panel layout, card layout, tabs, charts, meters, status pills,
  focus rings, cursor, tooltips, and hit boxes.
- Runtime text, glyph metrics, labels, clipping, wrapping, and state strings.
- Status semantics, task progress, chart values, and alert thresholds.
- Lighting masks, glow animation, lamp flicker, screen pulse, and timing.
- Sprite atlases, sprite IDs, rectangles, anchors, frame order, frame duration,
  and draw order.
- Palette files, colour ramps, quantization settings, and validation reports.
- Asset request JSON written by future Day 2 prompt-composer features.

## Rejection rules

Reject generated outputs that obscure the subject, weaken the coffee-shop
pixel-art style, contain muddy shadows, include watermark-like marks, use real
brand logos, add unrequested slogans, drift character identity, fail at runtime
scale, bake critical user-interface text into imagery, or make deterministic
layout decisions that belong in Rust.
