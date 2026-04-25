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
