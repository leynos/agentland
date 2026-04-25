# Repository instructions

This repository builds a Rust `pixels` desktop mockup of an AI agent team
management dashboard inside a cosy pixel-art workplace. The core scene is a
warm hipster coffee shop where agents work with laptops, terminals, books,
coffee, shelves, lamps, plants, and status panels.

Treat Codex built-in `image_gen` and GPT Images 2 as development-time visual
asset tools. Treat Rust `pixels`, post-processing scripts, manifests, and the
asset pipeline as the deterministic product surface.

## Project priorities

- Preserve a fixed 512x288 virtual resolution for the initial runtime.
- Preserve integer-scaled, crisp pixel presentation at every window size.
- Use generated raster images for references, source art, concept sheets, and
  carefully validated cutout sources.
- Build final dashboard UI structure in code: panels, tabs, text, charts,
  status pills, progress bars, focus rings, hit areas, and recurring icons.
- Keep every project-bound generated image in the repository with prompt
  provenance, validation notes, and post-processing metadata.
- Prefer small, shippable vertical slices over grand unfinished architecture.

## Source of truth

Use the Markdown files in `docs/` as the living source of truth. Before making
substantive changes, read the relevant document and update it when the design,
workflow, architecture, dependency set, or asset policy changes.

Expected core documents:

- `docs/art-bible.md`
- `docs/imagegen-workflow.md`
- `docs/prompt-style-guide.md`
- `docs/asset-spec.md`
- `docs/runtime-architecture.md`
- `docs/known-limitations.md`
- `docs/iteration-backlog.md`

A documentation style guide may live at `docs/documentation-style-guide.md`.
Follow it when present.

Documentation, comments, and commit messages must use en-GB-oxendict spelling
and grammar. Use `-ize` and `-yse` forms, and use British vocabulary where it
matters. External API names, crate names, filenames, and quoted upstream text
keep their original spelling.

## Repository shape

Use this layout as the default map unless the repository already documents a
newer one:

```text
.
├─ AGENTS.md
├─ .codex/
│  ├─ config.toml
│  └─ agents/
├─ prompts/
│  ├─ generated/
│  └─ templates/
├─ docs/
├─ assets/
│  ├─ source/gpt-images-2/
│  ├─ processed/
│  ├─ atlases/
│  ├─ manifests/
│  └─ palette/
├─ src/
│  ├─ app.rs
│  ├─ input.rs
│  ├─ layout.rs
│  ├─ scene.rs
│  ├─ text.rs
│  ├─ timing.rs
│  ├─ assets/
│  ├─ render/
│  ├─ lighting/
│  └─ day2/
└─ tools/
```

Create directories only when the change needs them. Do not invent empty
architecture for its own entertainment; the repo is not a hat rack for ghosts.

## Codex workflow

- Read the local docs, manifests, prompt templates, and relevant code before
  editing.
- Use subagents for read-heavy planning, comparison, audit, and review.
- Do not run multiple write-heavy agents against the same Rust modules,
  manifests, or prompt directories.
- Make the final implementation in one coherent writing thread unless the task
  is naturally file-isolated.
- Keep changes atomic. Each change should represent one logical unit of work.
- When a task touches generated assets, update prompts, manifests, docs, and
  consuming code together.
- Report real blockers directly. Do not paper over missing assets, failed
  validation, or non-deterministic behaviour with cheerful fog.

## Codex image generation workflow

Use Codex's built-in `image_gen` tool by default for raster image generation
and editing.

Do not configure or use PixelLab Model Context Protocol (MCP) for this
repository. Do not create one-off SDK runners for image generation. Do not ask
for `OPENAI_API_KEY` when using the built-in tool.

Use CLI fallback only when the user explicitly asks for CLI/API/model controls,
or after the user explicitly confirms a true native transparency fallback. If
CLI fallback becomes necessary, document the reason, keep secrets out of logs,
and do not modify Codex's bundled image-generation scripts.

### Built-in image generation rules

- Use one built-in generation call per distinct asset or variant.
- Do not treat `n` variants as a substitute for separate prompts for distinct
  assets.
- Do not rely on a destination-path argument for the built-in tool.
- Inspect generated outputs before accepting them.
- For project-bound images, copy or move the selected output from Codex's
  generated-image area into the workspace before code or docs reference it.
- Never leave a project-referenced asset only under `$CODEX_HOME/*`.
- Save accepted files under stable, descriptive, non-destructive filenames.
- Do not overwrite existing assets unless the user explicitly requests
  replacement. Prefer sibling versioned names such as `ava-reference-v2.png`.
- Discarded preview variants do not need manifests unless the user asks to keep
  them or they influenced a final decision.

### Prompt schema

Use this labelled structure for generation prompts unless a narrower local
template applies:

```text
Use case:
Asset type:
Primary request:
Input images: (optional, label each image by role)
Scene/backdrop:
Subject:
Style/medium:
Composition/framing:
Lighting/mood:
Colour palette:
Materials/textures:
Text (verbatim): ""
Constraints:
Avoid:
```

Use this structure for edits:

```text
Change:
Preserve:
Constraints:
```

Prompt rules:

- Preserve user-provided requirements.
- Add only details that materially improve the result.
- Prefer concrete visual facts over praise words.
- Avoid vague prompt padding such as `stunning`, `epic`, `masterpiece`,
  `beautiful`, `premium`, or `insane detail` unless you replace it with visible
  materials, lighting, typography, layout, or texture.
- Label every input image by role, such as `style reference`, `edit target`,
  `composition reference`, or `subject to insert`.
- For edits, repeat preservation invariants every iteration.
- Iterate with one targeted change at a time.
- Quote exact text under `Text (verbatim)` and specify placement, size,
  typography, colour, and `no duplicate text`.
- Render final runtime dashboard text in Rust rather than baking important UI
  copy into generated images.

### Pixel-art prompt additions

Use these clauses when the asset must function as pixel-art source material:

```text
Pixel-art requirements:
Crisp pixel-art rendering, readable silhouettes, controlled dithering, no
painterly smearing, no blurry anti-aliased subject edges, clear sprite-scale
forms.

Runtime fit:
Designed as source or reference art for a 512x288 fixed-virtual-resolution Rust
`pixels` renderer. Final runtime UI will be assembled deterministically.
```

Do not over-constrain presentation pages or mood boards. Style-book pages can
use richer detail than runtime sprites.

### Transparency and cutouts

For simple transparent or cutout assets, use built-in `image_gen` first with a
flat chroma-key background. Then remove the key locally with Codex's installed
helper.

Default cutout prompt clause:

```text
Scene/backdrop:
Perfectly flat solid #00ff00 chroma-key background for local background removal.
The background must be one uniform colour with no shadows, gradients, texture,
reflections, floor plane, or lighting variation.

Constraints:
Keep the subject fully separated from the background with crisp edges and
generous padding. Do not use #00ff00 anywhere in the subject. No cast shadow,
no contact shadow, no reflection, no watermark, and no text unless explicitly
requested.
```

Run chroma-key removal with the installed helper path:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" \
  --input <source.png> \
  --out <output.png> \
  --auto-key border \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 220 \
  --despill
```

Validate alpha, transparent corners, subject coverage, palette fit, and edge
fringing before accepting the result. If a thin fringe remains, retry once with
`--edge-contract 1`.

Ask before using CLI true transparency for hair, fur, smoke, glass, liquids,
translucent materials, reflective product grounding, soft shadows, or failed
chroma-key validation. Explain that native transparency needs CLI fallback with
`gpt-image-1.5`, because GPT Images 2 does not support `background=transparent`.

## Asset manifests and provenance

Treat generation metadata as source code. Every accepted project-bound image
must have a manifest under `assets/manifests/`.

At minimum, record:

- asset ID and family
- status, such as `approved-source`, `approved-runtime`, `rejected`, or
  `superseded`
- tool mode, usually `codex_builtin_image_gen`
- whether CLI fallback was used
- prompt file path and final prompt text
- reference-image labels, roles, and paths
- Codex generated path when known
- workspace source path
- processed output path when present
- post-processing settings
- validation notes
- runtime use, such as `reference only`, `portrait chip`, `prop sprite`, or
  `atlas input`

Suggested manifest shape:

```json
{
  "id": "ava_reference_sheet_v1",
  "family": "character-reference",
  "status": "approved-source",
  "tool": {
    "mode": "codex_builtin_image_gen",
    "model_family": "gpt-images-2",
    "fallback_cli": false
  },
  "prompt": {
    "path": "prompts/generated/characters/ava-reference-v1.md",
    "use_case": "stylized-concept",
    "asset_type": "pixel-art character reference sheet",
    "input_images": [
      {
        "label": "Image 1",
        "role": "approved dashboard mood reference",
        "path": "assets/source/references/approved-dashboard.png"
      }
    ]
  },
  "files": {
    "workspace_source_path": "assets/source/gpt-images-2/characters/ava-reference-v1.png",
    "processed_path": "assets/processed/characters/ava-reference-v1.quantized.png"
  },
  "validation": {
    "subject_correct": true,
    "style_match": true,
    "text_accuracy": "no generated text used",
    "notes": "Readable silhouette and good accessory separation."
  },
  "runtime_use": "reference only"
}
```

Keep prompts in version control. A manifest without the actual prompt is a
breadcrumb without the loaf.

## Visual direction

Use the approved dashboard mockup and `docs/art-bible.md` as visual authority.
The default house style is:

- cosy pixel-art workplace dashboard
- warm amber pendant lamps and small screen glows
- dark walnut wood, brick, brass trim, ceramic mugs, paper notes, and glass jars
- deep navy panel recesses with cream typography
- moss-green, ember-orange, screen-cyan, and slate-blue status accents
- readable silhouettes and clear sprite-scale forms
- structured dashboard hierarchy over decorative clutter

Generated images may include text for style-book or concept validation, but
runtime-critical copy belongs in Rust text rendering.

Reject generated assets that break the style, obscure the subject, use muddy
shadows, contain watermark-like marks, include real brand logos, hallucinate
unwanted slogans, or fail at target runtime scale.

## Runtime architecture

The runtime uses Rust, `winit`, and `pixels`.

- Keep the virtual framebuffer at 512x288 unless a documented requirement
  changes it.
- Preserve integer scaling and letterboxing where necessary.
- Map input and hit-testing through the same scale and offset calculations as
  rendering.
- Keep the compositor deterministic and testable.
- Use generated assets as source or reference images, not layout authority.
- Keep final UI panels, widgets, text, charts, meters, and recurring icons
  algorithmic.
- Use nine-slice rendering for scalable ornate panels.
- Keep layout constants centralized rather than scattered as magic numbers.
- Avoid one-off panel bitmaps unless a manifest explicitly justifies them.
- Draw debug overlays for sprite bounds, draw order, hit boxes, asset IDs, and
  lighting masks when useful.

Default layer order:

1. base background fill
2. environment tilemap or backplate
3. large props
4. characters
5. desk and counter foreground overlaps
6. UI backplates
7. UI widgets and icons
8. runtime text
9. lighting overlays
10. cursor, focus rings, tooltips, and debug overlays

## Day 2 prompt composer

Codex's built-in `image_gen` is a development workflow, not a Rust runtime API.
Do not build a runtime feature that pretends the app can call the built-in
Codex tool directly.

A Day 2 character creator should operate as a prompt composer:

1. the user edits structured character options in the Rust UI
2. the app writes a JSON asset request under `assets/requests/`
3. Codex reads the request during a development session
4. Codex turns it into a structured GPT Images 2 prompt
5. Codex generates the image, moves it into the workspace, post-processes it,
   and updates manifests
6. the app reloads the approved asset from disk

If the product needs user-triggered runtime image generation, design a separate
OpenAI Images API integration with explicit user consent, API keys, cost
controls, moderation, error handling, and logging policy. Keep that integration
separate from the Codex built-in tool.

## Code style and structure

- Code is for humans. Write code with clarity and empathy. Assume a tired
  teammate will need to debug it at 3 a.m.
- Comment why, not what. Explain assumptions, edge cases, trade-offs, and
  complexity.
- Favour clarity over cleverness. Prefer explicit code over terse or obscure
  idioms.
- Use functions and composition. Avoid repetition by extracting reusable logic.
- Keep functions small, purpose-led, and single responsibility.
- Keep command/query separation clear. Functions that mutate state should not
  also hide surprising queries.
- Name things precisely. For booleans, prefer names with `is`, `has`, or
  `should`.
- Structure modules around coherent responsibilities. Colocate feature-specific
  fixtures, helpers, and data when that improves comprehension.
- Keep code files under 400 lines. Split large dispatch tables, long switch
  logic, and bulky test data into focused modules or external data files.
- Function documentation must include clear examples when the example clarifies
  behaviour. Test documentation should not repeat the test logic in prose.

## Rust guidance

Run these quality gates before considering a Rust change complete:

```bash
make check-fmt
make lint
make test
```

These targets should map to:

```bash
cargo fmt --workspace -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
```

Use `make fmt` or `cargo fmt --workspace` to apply formatting fixes.

Rust rules:

- Clippy warnings must fail the build.
- Fix warnings in code rather than silencing them.
- Every module must start with a module-level `//!` comment explaining its
  purpose and utility.
- Document public APIs with Rustdoc comments.
- Place function attributes after doc comments.
- Prefer immutable data and avoid unnecessary `mut` bindings.
- Avoid `unsafe`. If it becomes unavoidable, keep it tightly scoped and explain
  it with a `SAFETY` comment.
- Do not use `return` in single-line functions.
- Use predicate functions for conditional criteria with more than two branches.
- Use `concat!()` for long string literals instead of escaped newlines.
- Prefer compact single-line constructors when they stay readable, for example
  `pub fn new(id: u64) -> Self { Self(id) }`.
- Use semantic newtypes for domain values rather than passing primitive soup.
- Use `cap_std`, `cap_std::fs_utf8`, and `camino` instead of `std::fs` and
  `std::path` where capability-oriented filesystem access or UTF-8 paths
  improve correctness.
- Use explicit caret-compatible crate versions in `Cargo.toml`.
- Do not use wildcard or open-ended dependency requirements.
- Use tilde requirements only for a documented patch-level lock.

### Rust tests

- Write unit and behavioural tests for new behaviour.
- Add a regression test for every fixed bug where practical.
- Use `rstest` fixtures for shared setup.
- Replace duplicated tests with `#[rstest(...)]` parameterized cases.
- Prefer `mockall` for ad hoc mocks and stubs.
- For environment-dependent code, prefer dependency injection and the
  `mockable` crate.
- If a test must mutate environment variables, wrap the mutation in shared
  guards and mutexes in `test_utils` or `test_helpers`.
- Direct environment mutation in tests is forbidden.
- In tests, prefer `.expect(...)` over `.unwrap()` for clearer diagnostics.
- In production code and shared fixtures, avoid `.expect()` and panics. Return
  `Result` and propagate errors with `?`.
- Keep `expect_used` strict. Do not suppress it to make a test quiet.
- Fallible `rstest` fixtures should make tests return `Result` and use `?`.

### Error handling

- Prefer semantic error enums for errors callers might inspect, retry, or map.
- Derive `std::error::Error` through `thiserror` for domain errors.
- Use opaque reports such as `eyre::Report` only at application boundaries.
- Never export an opaque error type from a library module.
- Convert domain errors to `eyre` only in `main()` or top-level async tasks.
- Use `.context(...)` when converting to opaque reports so diagnostics preserve
  useful failure paths.
- Helpers should return errors rather than panic.

## Python and tooling scripts

Python scripts under `tools/` support the asset pipeline. Keep them boring,
deterministic, and easy to run.

- Prefer explicit argument parsing and clear failure messages.
- Do not hide generated outputs in temporary paths that manifests cannot trace.
- Keep script output deterministic for a given input and options.
- Validate image dimensions, alpha channels, palette budgets, and atlas metadata
  before updating manifests.
- Keep intermediate files under `tmp/` or a documented workspace path.
- Do not commit caches or bulky temporary outputs.
- Use Python only for asset tooling unless the repository documents another
  runtime purpose.

## Asset pipeline checks

Before accepting runtime assets, verify:

- source image exists in `assets/source/gpt-images-2/` or another documented
  source directory
- manifest exists and names the source, prompt, validation, and runtime use
- alpha is valid for cutouts
- palette normalization does not destroy readability
- sprite bounds and anchor points make sense
- atlas metadata matches the packed image
- runtime scale check passes at 1x, 2x, 3x, and 4x where practical
- final app text remains deterministic and legible

If make targets exist, prefer them:

```bash
make assets-check
make manifest-check
```

If they do not exist, run the documented script commands directly and consider
adding a target once the workflow stabilizes.

## Documentation and Markdown

- Validate Markdown with `make markdownlint` when available.
- Run `make fmt` after documentation changes if the target formats Markdown in
  this repository.
- Validate Mermaid diagrams with `make nixie` when diagrams changed.
- Wrap Markdown paragraphs and bullet points at 80 columns.
- Wrap code blocks at 120 columns.
- Do not wrap table rows or headings.
- Use dashes for list bullets.
- Use GitHub-flavoured Markdown footnotes for references and footnotes.
- Keep documentation current with code, prompts, assets, and manifests.

## Change quality and committing

Quality gates for a completed change:

- relevant unit and behavioural tests pass
- lint checks pass
- formatting checks pass
- documentation reflects new decisions or changed behaviour
- generated assets have prompt provenance and manifests
- runtime assets pass scale, alpha, palette, and atlas validation where relevant

Commit rules:

- Commit only changes that meet the quality gates.
- Use small, focused commits.
- Write the subject line in the imperative mood.
- Keep the subject concise, ideally 50 characters or fewer.
- Add a body when the rationale, scope, or trade-offs need explanation.
- Separate subject and body with a blank line.
- Wrap commit body lines at 72 characters.
- Use Markdown in the body only where it helps.

## Refactoring workflow

Regularly watch for:

- long functions
- duplicated logic
- complex conditionals
- large blocks dedicated to deriving one value
- primitive obsession and data clumps
- excessive parameter lists
- feature envy
- shotgun surgery

After a functional change passes quality gates, review nearby code for these
signals. If refactoring helps, make it a separate atomic change after the
functional change. Ensure tests pass before and after the refactor.

## Additional tools

Use available tools when they genuinely help:

- `ripgrep` or `fd` for fast search
- `bat`, `delta`, or `difft` for readable inspection and diffs
- `mbake validate Makefile` or `checkmake` for Makefile validation
- `shellcheck` for shell scripts
- `hyperfine` for benchmark comparisons
- `strace`, `ltrace`, `gdb`, `lldb`, `valgrind`, `bpftrace`, `lsof`, `htop`,
  `iotop`, `ncdu`, `tree`, `eza`, `fzf`, `tcpdump`, and `nmap` for targeted
  debugging and diagnostics

Do not use a dramatic tool when a small command answers the question. Debugging
should feel like turning on lights, not summoning weather.

## Key takeaway

Use GPT Images 2 to explore and source visual richness. Use scripts and Rust to
make the product deterministic, crisp, testable, and maintainable.
