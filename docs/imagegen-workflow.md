# Image-generation workflow

## Scope

Agentland uses Codex built-in `image_gen` as the default authoring path for
development-time raster images. Generated images are references, source art, or
validated cutout sources. Rust, local scripts, manifests, atlases, palettes,
and renderer code are the deterministic product surface.

The approved mockups under `ref/` are the current visual source of truth. Do
not call `image_gen` for this branch unless a later task explicitly asks for
generation or a small exploratory image is necessary and documented.

PixelLab Model Context Protocol (MCP) is out of scope. Do not configure
PixelLab MCP, PixelLab job IDs, PixelLab character IDs, PixelLab tileset
generation, or PixelLab animation assumptions for this repository.

The image-generation CLI is out of scope unless the user explicitly asks for
CLI, application programming interface (API), or model controls, or explicitly
confirms a true native transparency fallback.

## Asset buckets

Every generated-image request must declare one bucket before generation:

- **Bucket 1 - direct generated reference:** use built-in `image_gen`, inspect
  the result, persist accepted output, and keep it as a reference, concept, or
  style-book artefact.
- **Bucket 2 - generated source converted to runtime pieces:** use built-in
  `image_gen` for source art, then clean, slice, crop, quantize, atlas-pack, or
  redraw into deterministic reusable assets.
- **Bucket 3 - algorithmic asset:** create with scripts, Rust code, or checked
  metadata. Generated images may inspire the look but are not a dependency.

Bucket 1 outputs are not loaded by the runtime unless a manifest explicitly
approves a narrow non-critical use. Bucket 2 outputs are not runtime assets
until the full local promotion checks pass. Bucket 3 is the runtime contract.

## Prompt schema

Use this labelled structure unless a narrower template in
`prompts/templates/` applies:

```text
Use case:
Asset type:
Bucket:
Primary request:
Input images: (optional, label each image by role)
Visual source of truth:
Focal priority:
Layer intent:
Scene/backdrop:
Subject:
Style/medium:
Composition/framing:
Lighting zones:
Colour palette:
Materials/textures:
Text (verbatim): ""
Runtime text policy:
Post-processing target:
Acceptance checks:
Constraints:
Avoid:
```

For pixel-art source material, add:

```text
Pixel-art requirements:
Crisp pixel-art rendering, readable silhouettes, controlled dithering, no
painterly smearing, no blurry anti-aliased subject edges, clear sprite-scale
forms.

Runtime fit:
Designed as source or reference art for a 512x288 fixed-virtual-resolution Rust
`pixels` renderer. Final runtime UI will be assembled deterministically.
```

Use these fields concretely:

- `Visual source of truth` should name the relevant approved mockup or accepted
  manifest.
- `Focal priority` should say what must read first, second, and third.
- `Layer intent` should state whether the image is environment, character,
  prop, UI ornament, light source reference, or presentation-only page.
- `Lighting zones` should name lamp pools, screen glows, rim highlights, shadow
  pockets, and areas that must stay readable at 1x.
- `Runtime text policy` should normally say that critical copy is rendered by
  Rust and no runtime-critical text should be baked into the image.
- `Post-processing target` should name the expected cleanup path, such as
  chroma-key removal, slicing, palette normalization, nine-slice extraction, or
  reference-only inspection.

## Edit prompt schema

Use this structure for edits:

```text
Change:
Preserve:
Runtime text policy:
Acceptance checks:
Constraints:
```

Repeat preservation invariants on every edit iteration. Make one targeted
change at a time. Do not use edit prompts to redesign layout, character
identity, lighting, and palette in the same pass.

## Prompt language

Prompt language must be concrete. Prefer visible facts over praise words.

Use phrases such as:

- warm amber pendant lamp pool over the counter;
- dark walnut shelves with brass trim;
- deep navy panel recess with cream runtime text area;
- screen-cyan glow on robot face and monitor glass;
- moss-green status accent and readable sprite-scale silhouette;
- flat `#00ff00` chroma-key background with no shadows.

Avoid vague quality terms such as `stunning`, `epic`, `masterpiece`,
`beautiful`, `premium`, and `insane detail`. Replace them with material,
lighting, composition, typography, or texture facts.

## Built-in generation workflow

1. Identify the bucket and the governing mockup or manifest.
2. Write the structured prompt under `prompts/generated/<family>/`.
3. Generate with Codex built-in `image_gen`.
4. Inspect the output for subject, style, composition, text accuracy,
   avoid-list compliance, preservation invariants, and bucket fit.
5. Decompose accepted outputs into layers, focal order, reusable ornaments,
   deterministic UI obligations, and asset candidates.
6. Copy or move accepted project-bound output into
   `assets/source/gpt-images-2/<family>/`.
7. Save it with a stable, descriptive, non-destructive filename.
8. Create or update a manifest under `assets/manifests/<family>/`.
9. Run post-processing only after the prompt and source image are persisted.
10. Update the manifest after every accepted post-processing step.

Discarded preview variants do not need manifests unless they influenced the
final decision or the user asks to keep them.

## Text-in-image rules

Runtime-critical text belongs in Rust. This includes agent names, statuses,
task descriptions, chart labels, tab labels, button labels, tooltip text, debug
labels, and any copy that reflects application state.

Generated text is allowed only for:

- design-book reference pages;
- human-readable concept sheets;
- non-runtime annotation callouts;
- decorative text that a manifest explicitly marks as non-critical.

When generated text is required, use:

```text
Text (verbatim): "AI Agent Dashboard"
Typography: large cream pixel-serif title, centred at the top, high contrast.
Runtime text policy:
Reference-page title only. Do not use this text as runtime UI copy.
Constraints:
Render the text exactly once; no extra words; no duplicate text; no watermark.
```

If exact text fails, reject or iterate. Do not silently accept near-miss text
for a prompt, manifest, or design-book source.

## Character workflow

Character reference prompts must ask for:

- full-body pose;
- seated or working pose;
- expression chips;
- accessory callouts;
- simple background;
- identity invariants;
- role props;
- accent colours;
- no critical micro-text inside sprite poses.

Character sheets are reference or source sheets, not deterministic sprite
atlases. Runtime sprites require cleanup, fixed dimensions, stable anchors,
palette normalization, and atlas metadata.

## Environment workflow

Environment prompts must record:

- environment name;
- mood and function;
- perspective type;
- functional zones;
- focal priority;
- material palette;
- lighting zones;
- reusable props;
- local palette chips if this is a design-book reference;
- whether labels are reference-only.

Use `design-book-11.png` for environment-card structure and
`design-book-12.png` for spatial-zone clarity. Environment source art should
not decide runtime layout by itself.

## Prop and chroma-key workflow

For simple transparent or cutout assets, use built-in `image_gen` first with a
flat chroma-key background, then remove the key locally.

Default cutout clause:

```text
Scene/backdrop:
Perfectly flat solid #00ff00 chroma-key background for local background
removal. The background must be one uniform colour with no shadows, gradients,
texture, reflections, floor plane, or lighting variation.

Constraints:
Keep the subject fully separated from the background with crisp edges and
generous padding. Do not use #00ff00 anywhere in the subject. No cast shadow,
no contact shadow, no reflection, no watermark, and no text unless explicitly
requested.
```

Run:

```bash
python tools/remove_chroma_and_validate.py \
  --input <source.png> \
  --out <output.png> \
  --auto-key border \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 220 \
  --despill \
  --edge-contract 0
```

If a thin fringe remains, retry once with `--edge-contract 1`.

Ask before using true native transparency for hair, fur, smoke, glass, liquids,
translucent materials, reflective product grounding, soft shadows, or failed
chroma-key validation. Native transparency requires the CLI fallback with
`gpt-image-1.5` because GPT Images 2 does not support
`background=transparent`.

## UI ornament workflow

Generated UI ornament references may define corner caps, dividers, plaques,
badges, swatch frames, callout tags, and trim texture. They must not define
runtime text, state, layout, hit areas, chart values, or responsive behaviour.

Runtime panels should be built from deterministic geometry, nine-slice metrics,
or approved processed ornament sprites. Any image-derived ornament needs slice
coordinates, palette notes, and atlas metadata before runtime use.

## Manifest requirements

Every accepted project-bound built-in `image_gen` output needs a manifest.
At minimum, the manifest records:

- asset ID and family;
- bucket and runtime intent;
- status;
- tool mode `codex_builtin_image_gen`;
- model family `gpt-images-2`;
- whether CLI fallback was used;
- prompt file path and final prompt text;
- input-image labels, roles, and paths;
- Codex generated path when known;
- workspace source path;
- processed output path when present;
- post-processing settings;
- validation notes;
- runtime use, layer, consumer, and text policy.

The manifest must make it clear whether the output is `reference only`,
`sliceable source`, `ornament source`, `runtime processed`, `lightmask source`,
or `layout reference`.

## Validation

Before accepting a generated asset, verify that:

- the prompt file exists;
- the source image exists in the workspace;
- the source image is not referenced only from `$CODEX_HOME`;
- the manifest names the prompt, source, validation, post-processing, and
  runtime use;
- alpha assets have transparent corners, clean edges, and no key-colour fringe;
- palette treatment preserves readability;
- sprite bounds and anchors make sense;
- runtime scale checks pass at 1x, 2x, 3x, and 4x where practical;
- critical runtime text remains deterministic;
- the asset bucket matches the actual intended use.

## Day 2 request flow

A future character creator should write JSON requests under `assets/requests/`.
Codex development sessions can turn those requests into structured GPT Images 2
prompts, generate images, move accepted outputs into the workspace,
post-process them, update manifests, and let the app reload approved assets
from disk.

The Rust runtime must not pretend it can call Codex built-in `image_gen`
directly.
