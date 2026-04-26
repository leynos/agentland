# Developer's guide

This guide is an internal reference for maintaining the current Agentland
placeholder runtime and its documentation-adjacent asset workflow.

## Repository layout

`src/` contains the Rust runtime, including window setup, display mapping,
deterministic layout, and software framebuffer drawing.

`docs/` contains the living product, runtime, asset, prompt, graph, user, and
developer documentation. Runtime or workflow changes should keep the relevant
documents current.

`assets/manifests/` contains manifest guidance for generated and processed
assets. Accepted project-bound raster assets require traceable prompt,
validation, and file metadata before runtime use.

`Makefile` exposes repository gates and graph tooling. `make graphs` rebuilds
the generated state graph Scalable Vector Graphics (SVG) files from Graphviz
DOT sources. `make check-graphs` compares regenerated SVG output with the
checked-in files and fails when the generated graph files are stale.

## Module overview

`config` contains compile-time constants for the placeholder runtime:
`VIRTUAL_WIDTH`, `VIRTUAL_HEIGHT`, `INITIAL_WINDOW_SCALE`, and `WINDOW_TITLE`.
The public virtual size is `512x288`, the initial window scale is `3`, and the
current window title is `Agentland`.

`display` contains `PhysicalViewportSize`, `Viewport`, and `VirtualPoint`.
`Viewport::from_window_size` calculates the largest integer scale that fits the
fixed virtual framebuffer into a physical window. `physical_to_virtual` maps
physical coordinates into virtual framebuffer coordinates and returns `None`
for letterbox margins or unfittable windows.

`layout` contains `Rect` and `DashboardLayout`. Geometry is derived
deterministically from configuration constants and local layout constants.
`top_bar()`, `scene_viewport()`, and `stat_cards()` expose the regions used by
the placeholder renderer.

`render::frame` contains `Color` and `FrameBuffer`. `Color` stores red, green,
blue, alpha (RGBA) channel bytes. `FrameBuffer::clear` fills the whole frame,
and `FrameBuffer::fill_rect` performs bounds-checked rectangle drawing.

`render::primitives` contains `render_placeholder_dashboard`. The draw order is
backplate, top bar, scene viewport, then stat cards. `PALETTE` centralises the
placeholder colours, and `card_accent` maps stat-card indices to their accent
colours.

`app` contains `AppError`, `run()`, `Runtime`, and `AgentlandApp`. This module
owns the `winit` event loop, window creation, `pixels` surface, redraw
scheduling, render calls, and zero-sized resize handling for minimised windows.

## Coordinate systems

Virtual framebuffer space is the deterministic layout space. Its origin is the
top-left pixel, its width is `512`, and its height is `288`. All layout
rectangles and placeholder drawing functions operate in this space.

Physical window space is the operating-system window size in physical pixels.
`Viewport::from_window_size` selects the largest integer scale that fits the
virtual framebuffer inside that physical size.

Any unused physical pixels become letterbox margins around the centred
viewport. `Viewport::physical_to_virtual` must be used for input and
hit-testing so points in those margins are rejected instead of being mapped to
dashboard content.

## Adding a new render region

1. Add named layout constants near the existing constants rather than embedding
   magic numbers in drawing code.
2. Add the region as a `Rect` in `DashboardLayout` when other modules need to
   share the geometry.
3. Add a focused draw function in `src/render/primitives.rs`.
4. Call the draw function from `render_placeholder_dashboard` in the intended
   layer order.
5. Add a unit test in the relevant `tests` module. For rendered regions, draw
   into an in-memory frame and assert stable pixel colours at coordinates
   derived from `DashboardLayout`.

## Testing

Run the full Rust test suite with:

```bash
cargo test
```

Repository gates may wrap this through `make test`, which enables the standard
workspace and feature settings.

Existing coverage includes integer scaling and letterbox mapping in `display`,
deterministic section geometry in `layout`, clipped rectangle drawing in
`render::frame`, placeholder pixel regression checks in `render::primitives`,
and zero-sized surface detection in `app`.

Use `rstest` for parametrised cases when a behaviour has multiple clear input
and output examples, such as viewport scale selection or resize edge cases.

## Asset pipeline

The asset workflow is documented in `docs/imagegen-workflow.md`,
`docs/asset-spec.md`, and `assets/manifests/README.md`.

Codex built-in image generation is a development-time authoring path. The Rust
runtime must not call `image_gen` directly. Runtime code should load only
approved, processed, repository-local assets whose manifests describe prompt
provenance, validation, post-processing, and intended use.

### Manifest and asset validation

Use these Makefile targets for asset pipeline checks:

- `make manifest-check` validates JSON manifest structure, required fields, and
  canonical enum values documented in `docs/asset-spec.md` and
  `assets/manifests/README.md`.
- `make assets-check` runs `manifest-check` and then checks asset metadata
  consistency. It is the extension point for alpha, palette, atlas, scale, and
  runtime-use validation as those checks are implemented.

Both targets are prerequisites of `make all`, so the aggregate repository gate
now covers manifest schema validation and combined asset metadata validation.

### Bucket and intent-class classification

`docs/asset-spec.md` is the canonical source for manifest `bucket` and
`intent_class` values. Manifests must use the string values below rather than
numeric shorthand.

Buckets:

- `direct-generated-reference`: built-in `image_gen` output kept as reference,
  style-book, or concept art and not loaded by the runtime.
- `generated-source-converted`: built-in `image_gen` output used as source for
  deterministic crops, slices, cleaned sprites, cutouts, texture studies, or
  ornament references.
- `algorithmic`: scripts, Rust code, metadata, palette files, light masks,
  layout, text, charts, validation reports, or other code-owned assets.

Intent classes:

- `reference-only`: human-facing source of truth that is not loaded at runtime.
- `sliceable-source`: image source intended for deterministic crop or slice.
- `ornament-source`: image source intended for trim, plaque, badge, or
  nine-slice extraction.
- `runtime-processed`: cleaned output approved for runtime loading.
- `lightmask-source`: deterministic mask image or generated reference for mask
  placement.
- `layout-reference`: visual reference for spacing, zone naming, or spatial
  hierarchy.

### Prompt templates

`prompts/templates/` contains concrete prompt templates for repeatable
development-time asset generation. Keep prompts specific, visual, and aligned
with `docs/prompt-style-guide.md`.

- `character-sheet.md` defines character reference sheets for roster identity,
  silhouettes, accessories, pose language, and cleanup notes.
- `animation-sheet.md` defines animation reference sheets for motion studies,
  pose sequences, timing notes, and sliceability checks.
- `prop-cutout.md` defines isolated prop cutout prompts for chroma-key cleanup,
  bounds recording, palette normalization, and atlas promotion.
- `environment-sheet.md` defines environment reference sheets for room layouts,
  material zones, lighting placement, and background-layer planning.
- `ui-ornament.md` defines user interface (UI) ornament references for frames,
  plaques, tabs, badges, dividers, and nine-slice candidates.
- `edit-invariants.md` defines edit prompts that preserve approved identity,
  composition, palette, lighting, and text-safety constraints.
- `transparent-chromakey.md` defines flat chroma-key prompts for deterministic
  local background removal and alpha validation.

### Planned tools

The intended post-processing tool surface is listed in the
`docs/asset-spec.md` "Post-processing scripts" section. Several tools are
marked *(planned)* there, including chroma-key removal, palette normalization,
transparent-bounds cropping, sheet slicing, nine-slice extraction, sprite
packing, and light-mask generation. Do not document those planned scripts as
available commands until the corresponding files exist under `tools/`.
