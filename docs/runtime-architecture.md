# Runtime architecture

## Scope

Agentland is a Rust desktop mockup rendered with `pixels` and `winit`. The
initial runtime opens a window and draws a deterministic placeholder dashboard
into a fixed `512x288` virtual framebuffer.

## Assumptions

- The crate remains a single package until a real crate boundary earns its
  keep.
- `src/main.rs` stays thin and delegates to `agentland::app::run()`.
- Core layout, display mapping, and rendering helpers are testable without a
  live window.
- `pixels` and `winit` are integration details at the application edge.
- Generated image assets are loaded only after they are approved, processed,
  and described by manifests or atlas metadata.

## Module layout

The bootstrap slice uses these modules:

- `src/lib.rs`: crate documentation, module exports, and stable public
  constants.
- `src/main.rs`: binary entry point.
- `src/app.rs`: `winit` event loop, window creation, `pixels` setup, resize
  handling, redraw scheduling, and top-level error conversion.
- `src/config.rs`: virtual size, window title, and presentation constants.
- `src/display.rs`: integer scaling, letterboxing, and pointer mapping.
- `src/layout.rs`: dashboard rectangles for the top bar, scene viewport, and
  bottom stat cards.
- `src/render/mod.rs`: render subsystem boundary.
- `src/render/frame.rs`: framebuffer wrapper and clipped rectangle drawing.
- `src/render/primitives.rs`: placeholder dashboard drawing.

Future slices should add `input`, `hit`, `scene`, `ui`, `text`, `assets`,
`lighting`, `timing`, and debug overlay modules only when a vertical slice needs
them.

## Fixed virtual resolution

The virtual framebuffer is always `512x288`. Window size never becomes layout
authority. Resize events resize the `pixels` surface and recalculate the
letterbox viewport, but the framebuffer width and height remain unchanged.
Zero-width or zero-height resize events are treated as a minimised presentation
surface: the app skips `pixels::Pixels::resize_surface`, preserves the last
valid viewport, and pauses redraw work until a non-zero size arrives.

## Integer scaling and letterboxing

The display mapper calculates the largest integer scale that fits inside the
physical window. The rendered area is centred and any remaining space is
letterboxed by the presentation surface.

Pointer mapping uses the same viewport. Physical coordinates inside the
letterbox margin map to no virtual point, which prevents hit testing against
pixels the app did not render.

## Placeholder layout

The initial layout has three product surfaces:

- a top bar for application navigation and global status;
- a central scene viewport for the coffee-shop workplace;
- four bottom stat cards for team and task state.

These are rectangles rather than final art. They establish the coordinate
system, presentation contract, and future hit-test seams.

## Render path

The render path is deliberately simple:

1. Clear the framebuffer to near black.
2. Compute the dashboard layout in virtual coordinates.
3. Draw the top bar, scene viewport, bottom card rail, and stat-card
   placeholders.
4. Let `pixels` present the fixed framebuffer into the integer-scaled viewport.

No final art is generated or loaded in this slice.

## Future runtime boundaries

Future work should keep these boundaries:

- The renderer owns panels, tabs, charts, status pills, progress bars, focus
  rings, hit boxes, and runtime text.
- The asset loader owns approved processed files and atlas metadata, never
  Codex output paths.
- The lighting module owns amber lamp pools, cyan screen glows, and vignette
  overlays.
- The hit-test module derives regions from layout rectangles rather than
  duplicating constants.
- The text module renders critical user-interface copy deterministically.

## Test seams

The bootstrap tests cover:

- viewport calculation for exact, doubled, non-integral, ultrawide, portrait,
  and tiny windows;
- physical-to-virtual coordinate mapping, including letterbox rejection;
- dashboard layout fitting inside the fixed virtual bounds;
- bottom stat card dimensions and spacing;
- rectangle rendering clipping at framebuffer edges.

Later tests should cover hit ordering, sprite anchors, atlas metadata,
nine-slice metrics, text clipping, animation ticks, and lighting masks.
