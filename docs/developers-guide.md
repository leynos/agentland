# Developer's guide

This guide is an internal reference for maintaining the current Agentland
placeholder runtime and its documentation-adjacent asset workflow.

## Spelling policy

Run the spelling gate with:

```bash
make spelling
```

`TYPOS_CONFIG_BUILDER_VERSION` in the `Makefile` pins the
`typos-config-builder` release the gate runs (currently `v0.1.3`). Raise it
together with the regenerated `typos.toml`, never on its own.

The tracked `typos.toml` is regenerated on every run from the live shared
en-GB-oxendict dictionary and the repository-specific `typos.local.toml`
overlay. Never edit generated entries by hand; add only narrow repository
terminology to the overlay. Because the dictionary is live, `typos.toml` must
never be drift checked in continuous integration.

The shared config builder refreshes the dictionary into an untracked local
cache only when the authoritative copy is newer. A valid cache remains usable
when the network is unavailable.

## Coverage publication

Coverage has two workflows, and the split is a contract (concordat's CV-005,
`main-owned-codescene-coverage`), not a convention.

- `ci.yml` measures Cobertura coverage on every pull request with the shared
  `generate-coverage` action, `with-ratchet: 'true'` and
  `publish-artefact: 'false'`. A drop against the ratchet baseline fails the
  pull request. The lane holds no CodeScene credential, has no upload step, and
  never contacts CodeScene.
- `coverage-main.yml` runs on every push to `main` and on dispatch. It measures
  the same source with the same action, format, output path, and default
  baseline files. A push to `main` writes the ratchet baseline every pull
  request compares against; a dispatch reads it without advancing it. The lane
  then uploads the report to CodeScene in explicit upload mode. A check step
  reports whether the secret is set by evaluating
  `${{ secrets.CS_ACCESS_TOKEN != '' }}` into its output, and no step holds the
  token in its `env`, because the composite upload action would hand a step
  `env` to its nested `upload-artifact` and cache steps; the upload step passes
  the secret as its `access-token` input. The check runs earlier in the
  upload's own job, under no default shell, since a step's output is readable
  only there. The upload's `if:` is exactly
  `steps.codescene-token.outputs.available == 'true'` joined by `&&` to
  `github.ref == 'refs/heads/main'` (a dispatch can name any branch, and any
  further conjunct could only narrow, defeat, or invert the upload), and the
  workflow's concurrency group, exactly
  `${{ github.workflow }}-${{ github.ref }}` at every level, never cancels a
  run in progress and never overlaps two runs, so triggered runs (push and
  dispatch) upload in commit order and a burst of merges cannot abandon a
  baseline write. A manual re-run of an older `main` run is an operator action
  that republishes that commit's coverage and baseline until the next push
  supersedes it. The workflow answers exactly a push to `main` and
  `workflow_dispatch`, and the coverage selection both lanes run is pinned in
  the contract.

One known exception: a Dependabot pull request merged by the automerge workflow
with `GITHUB_TOKEN` fires no push event, so that merge is neither measured nor
uploaded until the next push to `main`; shared-actions #518 tracks the fix.
There is deliberately no `schedule` trigger to paper over it. Likewise, a
dispatch that replaces a pending push uploads the same or a newer commit, but
the ratchet baseline is saved only on a push, so it stays one commit behind
until the next push; shared-actions #518 covers that too.

The reasons are both quiet failures: a pull request from a fork cannot read the
secret, so an upload there is silently skipped, and CodeScene accepts an upload
only for a branch it analyses, which a pull request head is not.

`tests/coverage_workflows.rs` enforces the split over every workflow a pull
request can reach, following local reusable-workflow calls transitively, and
over every other workflow too: only the publisher may hold the token, reach a
secret by a computed name, name the CodeScene host, run the CLI or the
uploader, or touch the retired `CODESCENE_CLI_SHA256` variable. It drives each
rule against breaching fixtures under `tests/coverage_workflows/`. The
pull-request surface is seeded by every event that runs a workflow for a pull
request (`pull_request`, `pull_request_target`, `merge_group`, the two review
events, `issue_comment`, `workflow_run`, and any push not limited to exactly
`branches: [main]` or to tags, where a `branches-ignore` beside `tags` still
counts unless it lists `'**'`), and the push side is followed the same way: a
workflow a push starts, or one it calls, may run a ratcheted coverage step only
behind `if: github.event_name == 'pull_request'`, so the publisher stays the
baseline's only writer. When adding a workflow, keep CodeScene, `cs-coverage`,
and the token out of it unless it is the publisher; the contract names the
clause a change breaks.

## The build standard

Development, test, lint, and typecheck builds use the parallel `rustc` frontend
(`-Zthreads=8`) and, on Linux, the `mold` linker (`-Clink-arg=-fuse-ld=mold`).
These are defaults in `.cargo/config.toml`, which Cargo discovers on its own,
so a bare `cargo build` gets them. `mold` ships for Linux only, so the linker
flag lives in a Linux-only table and macOS and Windows keep their platform
linker. Cargo selects one `rustflags` source rather than merging them, so every
source repeats the same flags apart from the linker.

An assigned `RUSTFLAGS` replaces the configuration's flags, so the Makefile
recipes that set it compose the standard's flags onto any inherited value (CI's
`setup-rust` exports one). Two builds are deliberately excluded: coverage
assigns `RUSTFLAGS` without the fast flags, because a measurement should not
depend on them, and the release recipe and workflow keep the platform linker,
because they assign `RUSTFLAGS` (even an empty value displaces the
configuration). Cargo has no per-profile `rustflags`, so a direct
`cargo build --release` takes the configuration's flags unless `RUSTFLAGS` is
assigned too.

On Linux, install `mold` before building: the configuration names it, so a
build without it fails at link time. CI installs it through `setup-rust`'s
`install-mold` input. `tests/build_standard_contract.rs` holds the standard. It
reads the configuration sources, the commands `make -n` prints for each
development target on a Linux host and a macOS host (each keeping the caller's
own `RUSTFLAGS`) and for each coverage and release target on a Linux host, and
the `setup-rust` steps of the CI workflows (each must pass `install-mold`), so
a flag lost through a recipe or workflow edit fails there.

### Cranelift

Cranelift is the development-profile codegen backend. The full suite was
measured under it on the pinned `nightly-2026-03-26` on 2026-09-29: all 168
nextest tests pass (the crate has no doctests). Coverage selects LLVM explicitly
(`CARGO_PROFILE_DEV_CODEGEN_BACKEND=llvm`), because instrumentation needs it,
and release builds use the release profile, which Cranelift does not touch.
Re-measure the whole suite on the next toolchain bump; if it fails, record the
failing tests here as an exception and remove the backend from
`.cargo/config.toml`.

## Runner placement

`ci.yml`'s `build-test` and `coverage-main.yml`'s `coverage-upload`, main's
only cache writer, run on `ubicloud-standard-2`. `runs-on` selects it with the
runner-selection expression
`${{ github.event.pull_request.head.repo.fork && 'ubuntu-latest' ||
'ubicloud-standard-2' }}`.
A pull request from a fork cannot obtain an Ubicloud runner, so it falls back
to `ubuntu-latest`; a push and a dispatch have no pull request, so the fork
value is null and they select Ubicloud. A fork's pull request therefore
restores a hosted cache that main no longer refreshes; fork pull requests are
rare here (Dependabot pull requests are branches, not forks), and a second
hosted writer would pay double on every main push.

The writer sits on Ubicloud because Ubicloud's cache proxy is scoped by ref. A
pull request's Ubicloud lane reads a warm main scope only when a main job on
Ubicloud writes it, so a lane can move to Ubicloud only after its main writer
has.

An Ubicloud runner is a self-hosted just-in-time runner, so GitHub's six-hour
cap for hosted jobs does not bound it and a hung job would hold a billable
runner. Every job whose `runs-on` can select Ubicloud therefore states its own
`timeout-minutes`, twice a measured warm Ubicloud run. `build-test` is at 30
minutes (a warm run took 12.7 min, run 36558912722); `coverage-upload` is at 5
minutes (its first Ubicloud main run took 2.4 min, run 36556909060).

`tests/coverage_workflows/placement_cases.rs` holds this to the files. It
evaluates the expression for a push or dispatch, a same-repository pull request
and a fork, rejects a literal label, inverted arms, another label and another
condition, and asserts an exact inventory of the jobs that can land on Ubicloud
with their ceilings. A change that adds, removes or re-times such a job fails
it until the inventory is updated in the same commit.

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
backplate, top bar, scene viewport, then stat cards. `PALETTE` centralizes the
placeholder colours, and `card_accent` maps stat-card indices to their accent
colours.

`app` contains `AppError`, `run()`, `Runtime`, and `AgentlandApp`. This module
owns the `winit` event loop, window creation, `pixels` surface, redraw
scheduling, render calls, and zero-sized resize handling for minimized windows.

## Coordinate systems

Virtual framebuffer space is the deterministic layout space. Its origin is the
top-left pixel, its width is `512`, and its height is `288`. All layout
rectangles and placeholder drawing functions operate in this space.

Physical window space is the operating-system window size in physical pixels.
`Viewport::from_window_size` selects the largest integer scale that fits the
virtual framebuffer inside that physical size.

Any unused physical pixels become letterbox margins around the centred viewport.
`Viewport::physical_to_virtual` must be used for input and hit-testing so
points in those margins are rejected instead of being mapped to dashboard
content.

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

Use `rstest` for parametrized cases when a behaviour has multiple clear input
and output examples, such as viewport scale selection or resize edge cases.

## Asset pipeline

The asset workflow is documented in `docs/imagegen-workflow.md`,
`docs/asset-spec.md`, and `assets/manifests/README.md`.

Codex built-in image generation is a development-time authoring path. The Rust
runtime must not call `image_gen` directly. Runtime code should load only
approved, processed, repository-local assets whose manifests describe prompt
provenance, validation, post-processing, and intended use.

### 3. Manifest and asset validation

Use these Makefile targets for asset pipeline checks:

- `make manifest-check` validates JSON manifest structure, required fields, and
  canonical enum values documented in `docs/asset-spec.md` and
  `assets/manifests/README.md`.
- `make assets-check` runs manifest validation and deterministic asset metadata
  consistency checks. It is the designated extension point: alpha, palette,
  atlas, scale, and runtime-use validation will be expanded here as those
  checks are implemented.

`make assets-check` is a prerequisite of `make all`, so the aggregate
repository gate covers the current manifest-backed asset validation pass
without running manifest validation twice.

#### tools/check_manifests.py

Validates JSON manifests under `assets/manifests/` against the canonical
schema. Public API:

- `parse_args(argv)` — parses the `--root` command-line interface (CLI)
  argument.
- `manifest_paths(root)` — discovers manifests under `assets/manifests/`.
- `load_manifest(path)` — reads and JSON-parses one manifest file.
- `validate_manifest(root, path)` — returns a list of `ValidationError` values
  for one file.
- `validate_manifest_fields(root, data, errors)` — validates a parsed manifest
  dictionary.
- `main(argv, output)` — CLI entrypoint; returns `0` on success and `1` on any
  failure.
- `ValidationError(field, message)` — frozen dataclass for domain validation
  failures.

#### tools/check_assets.py

Extension-point entrypoint that runs `check_manifests.main()` and deterministic
asset-level metadata checks. Intended to accumulate additional alpha, palette,
and atlas checks as they are implemented.

### 4. Bucket and intent-class classification

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

### 5. Prompt templates

`prompts/templates/` contains concrete prompt templates for repeatable
development-time asset generation. Keep prompts specific, visual, and aligned
with `docs/prompt-style-guide.md`. The shared GPT Images 2 standard lives in
`docs/imagegen-workflow.md` and `prompts/templates/README.md`; update both when
the schema or image-generation rules change.

Use the labelled generation schema for new asset prompts unless a narrower
template applies: `Use case`, `Asset type`, `Primary request`, labelled input
images, `Scene/backdrop`, `Subject`, `Style/medium`, `Composition/framing`,
`Lighting/mood`, `Colour palette`, `Materials/textures`, `Text (verbatim)`,
`Constraints`, and `Avoid`.

Use the edit schema for image edits: `Change`, `Preserve`, and `Constraints`.
Repeat the full `Preserve` list on every edit iteration so identity, layout,
palette, lighting, and text-safety invariants remain explicit.

Codex built-in `image_gen` is the default authoring path for generated raster
references and source art. Do not document CLI fallback or API runners as the
normal workflow. Ask before using CLI `gpt-image-1.5` for true transparency,
and do not rely on a destination-path argument for the built-in tool.

For project-bound outputs, copy accepted images from the built-in output area
into the workspace before any code, manifest, or documentation references them.
Every accepted generated image needs a manifest under `assets/manifests/`.

For exact generated text, put the copy under `Text (verbatim)` and specify
typography, placement, size, colour, and `no duplicate text`. Runtime-critical
text such as agent names, statuses, task labels, buttons, and chart labels
belongs in Rust rendering rather than baked into generated images.

For transparent assets, prompt for a perfectly flat chroma-key background.
Automation for chroma-key removal is not yet available, so templates must keep
manual keying as the current workflow until the helper exists under `tools/`
and has validation coverage.

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

### 6. Planned tools

The intended post-processing tool surface is listed in the `docs/asset-spec.md`
"Post-processing scripts" section. Several tools are marked *(planned)* there,
including chroma-key removal, palette normalization, transparent-bounds
cropping, sheet slicing, nine-slice extraction, sprite packing, and light-mask
generation. Do not document those planned scripts as available commands until
the corresponding files exist under `tools/`.
