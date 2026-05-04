# Image-generation workflow

## Scope

Agentland uses Codex built-in `image_gen` as the default authoring path for
development-time GPT Images 2 raster images. Generated images are references,
source art, concept sheets, or validated cutout sources. Rust, local scripts,
manifests, atlases, palettes, and renderer code remain the deterministic
product surface.

Do not call `image_gen` while writing prompt standards or templates. Generation
tasks must be explicit.

Do not configure PixelLab Model Context Protocol (MCP), create one-off
image generation software development kit (SDK) runners, or ask for
`OPENAI_API_KEY` when using the built-in tool.

CLI fallback is out of scope unless the user explicitly asks for
command-line, application programming interface (API), or model controls, or
explicitly confirms true native transparency after the chroma-key path has been
explained.

## Standard generation schema

Use this labelled schema for every new GPT Images 2 generation prompt unless a
narrower local template applies. Keep the labels in this order so prompts,
manifests, and reviews line up.

```plaintext
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

For multi-image generation or compositing, label each input image by role,
such as `style reference`, `edit target`, `composition reference`, or
`subject to insert`. Include the path or manifest identifier where known.

For exact text, put the literal copy under `Text (verbatim)`. State the
typography, placement, size, colour, and `no duplicate text` in
`Constraints`.
Important runtime user interface (UI) text belongs in the Rust renderer, not in
generated images.

## Standard edit schema

Use this schema for every edit prompt:

```plaintext
Change:
Preserve:
Constraints:
```

Repeat the full `Preserve` list every iteration. Make one targeted edit at a
time so preservation failures and identity drift are easy to detect.

## Built-in generation rules

- Use built-in `image_gen` by default for raster image generation and editing.
- Use one built-in generation call per distinct asset or variant.
- Do not rely on a destination-path argument for the built-in tool.
- Inspect generated outputs before accepting them.
- After generation, copy or move every accepted project-bound output from
  the built-in output area into the workspace.
- Never leave a project-referenced image only under `$CODEX_HOME` or
  another Codex-private generated-output path.
- Save accepted files under stable, descriptive, non-destructive
  filenames.
- Do not overwrite existing assets unless the user explicitly requests
  replacement. Prefer sibling versioned names such as
  `ava-reference-v2.png`.
- Every accepted generated image needs a manifest under `assets/manifests/`.
- Discarded preview variants do not need manifests unless the user asks to keep
  them or they influenced the final accepted asset.

## Prompt language rules

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
lighting, composition, typography, layout, or texture facts.

For pixel-art source material, add the following clauses inside the relevant
schema fields:

```plaintext
Style/medium:
Crisp pixel-art rendering, readable silhouettes, controlled dithering, no
painterly smearing, no blurry anti-aliased subject edges, clear sprite-scale
forms.

Constraints:
Designed as source or reference art for a 512x288
fixed-virtual-resolution Rust `pixels` renderer. Final runtime UI will be
assembled deterministically.
```

## Transparent assets

For simple transparent or cutout assets, use built-in `image_gen` first with a
perfectly flat chroma-key background. Then remove the key locally with the
installed helper.

Use this chroma-key clause:

```plaintext
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

Chroma-key removal is not yet automated. For now:

- duplicate the source locally;
- remove #00ff00 using a hard-edged manual keying workflow;
- save a transparent PNG and validate alpha, transparent corners, subject
  coverage, palette fit, and edge fringing before accepting the result.
- if a thin fringe remains, perform one additional manual edge-cleanup pass.

Ask before using CLI `gpt-image-1.5` for true transparency.
Use that fallback only after the user explicitly requests it or confirms
that native transparency is worth the additional CLI path.

## Runtime text policy

Runtime-critical text belongs in Rust. This includes agent names, statuses,
task descriptions, chart labels, tab labels, button labels, tooltip text,
debug labels, and any copy that reflects application state.

Generated text is allowed only for:

- design-book reference pages;
- human-readable concept sheets;
- non-runtime annotation callouts;
- decorative text that a manifest explicitly marks as non-critical.

When generated text is required, quote it exactly:

```plaintext
Text (verbatim): "AI Agent Dashboard"
Constraints:
Large cream pixel-serif title, centred at the top, high contrast, render the
text exactly once, no extra words, no duplicate text, no watermark.
```

If exact text fails, reject or iterate. Do not silently accept near-miss text
for a prompt, manifest, or design-book source.

## Manifest requirements

Treat generation metadata as source code. Every accepted project-bound
generated image must have a manifest under `assets/manifests/`.

At minimum, the manifest records:

- asset ID and family;
- status, such as `approved-source`, `approved-runtime`, `rejected`, or
  `superseded`;
- tool mode, usually `codex_builtin_image_gen`;
- model family, usually `gpt-images-2`;
- whether CLI fallback was used;
- prompt file path and final prompt text;
- input-image labels, roles, and paths;
- Codex generated path when known;
- workspace source path;
- processed output path when present;
- post-processing settings;
- validation notes;
- runtime use, layer, consumer, and text policy.

The manifest must use canonical asset fields from `docs/asset-spec.md` where
that document defines them.

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
