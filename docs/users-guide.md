# User's guide

This guide describes the current Agentland desktop placeholder build for
people launching, viewing, or diagnosing the application.

## Overview

Agentland is a pixel-art artificial intelligence (AI) agent team management
dashboard. The current build opens a desktop window and renders a deterministic
placeholder interface at a fixed `512x288` virtual resolution.

The visual direction is a warm amber coffee-shop dashboard with dark panels,
brass trim, walnut tones, status accents, and crisp pixel presentation. The
placeholder build establishes the screen structure only; no agent interaction,
data loading, or final asset display is present yet.

## Requirements

Agentland uses Rust, `winit`, and `pixels` for desktop windowing and
presentation. The project is expected to run on desktop operating systems
supported by those libraries, including Linux, Windows, and macOS targets with
compatible system libraries.

Graphics support can come from any graphics processing unit (GPU) or software
renderer that satisfies the active `winit` and `pixels` backend requirements.
No project-specific graphics hardware feature is required by the placeholder
build.

Building from source requires the Rust toolchain pinned by
`rust-toolchain.toml`: `nightly-2026-03-26`, with `rustfmt` and `clippy`
components installed.

## Building and launching

Build an optimised release binary with:

```bash
cargo build --release
```

Launch the release build with:

```bash
cargo run --release
```

At launch, the window title is `Agentland`. The initial window size is
`1536x864`, which is the `512x288` virtual framebuffer scaled by the configured
initial factor of `3`.

The window minimum inner size is `512x288`. Presentation uses integer pixel
scaling, so the rendered dashboard remains crisp rather than stretched through
fractional scaling.

## Dashboard layout

The placeholder dashboard has three visible regions.

The top status bar spans the full width of the virtual framebuffer. In the
current build it shows a slate-blue bar, brass lower border, and two coloured
placeholder badges. These shapes reserve space for future application status
and navigation surfaces.

The central scene viewport sits below the top bar. In the current build it
shows a bordered panel with a dark interior, walnut lower strip, warm amber
block, and cyan block. These shapes reserve the future coffee-shop workplace
scene area.

The bottom stat cards form four equal cards across the lower edge of the
dashboard. In the current build each card has a brass border, slate-blue body,
dark content strip, and a coloured accent. These shapes reserve space for
future team and task summary information.

## Asset pipeline overview

Generated art in Agentland is reference or cutout material only. It is never
loaded by the application until it has been processed, checked, and approved
through a manifest.

To check asset metadata health, run `make manifest-check` for manifest records
or `make assets-check` for the combined asset validation pass.

The current build does not display final art assets. Its placeholder shapes
reserve the dashboard regions where future approved scene, character, prop, and
interface assets will appear.

## Window resizing

The renderer keeps the virtual framebuffer fixed at `512x288` for every window
size. Resize handling selects the largest integer scale that fits inside the
physical window.

If the physical window is larger than an exact multiple of the virtual
framebuffer, unused margins become letterbox regions around the centred
dashboard. Those regions are outside the virtual dashboard and are rejected by
the coordinate mapper.

The configured minimum inner size is `512x288`. Window managers may still emit
temporary zero-sized resize events during minimisation; the runtime treats
those events as a hidden surface and resumes rendering after a non-zero size
returns.

## Troubleshooting

A blank or black window on launch usually indicates a graphics backend or
driver problem before the placeholder frame is presented. Confirm that the
system satisfies the `winit` and `pixels` requirements, then run
`cargo run --release` from a terminal to capture renderer errors.

A window that appears too small to resize is constrained by the configured
minimum inner size of `512x288`. Some desktop environments also apply their own
minimum frame decorations around that content area.

Rendering artefacts such as blurred edges usually indicate compositor scaling
outside the application, display scaling applied by the operating system, or a
backend presentation issue. The application itself renders into a fixed
framebuffer and asks `pixels` for pixel-perfect presentation.
