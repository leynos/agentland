# Image-generation workflow

## Scope

Agentland uses Codex built-in `image_gen` as the default authoring path for
development-time raster images. Generated images are references, source art, or
validated cutout sources. Rust, local scripts, manifests, atlases, palettes,
and renderer code are the deterministic product surface.

PixelLab Model Context Protocol (MCP) is out of scope. Do not configure
PixelLab MCP, PixelLab job IDs, PixelLab character IDs, PixelLab tileset
generation, or PixelLab animation assumptions for this repository.

The image-generation CLI is out of scope unless the user explicitly asks for
CLI, application programming interface (API), or model controls, or explicitly
confirms a true native transparency fallback.

## Assumptions

- GPT Images 2 is available through Codex built-in `image_gen` during
  development sessions.
- Built-in image generation does not provide a runtime application programming
  interface for Agentland.
- Project-bound generated images must be copied from Codex's generated-image
  area into the workspace before code or docs reference them.
- Every accepted project-bound generated image needs a prompt file and a
  manifest.
- Important runtime user-interface text is rendered by Rust, not baked into
  generated images.

## Generation prompt schema

Use this labelled structure unless a narrower local template applies:

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

## Edit prompt schema

Use this structure for edits:

```text
Change:
Preserve:
Constraints:
```

Repeat preservation invariants on every edit iteration. Make one targeted
change at a time.

## Prompt rules

- Preserve user-provided requirements.
- Add only details that materially improve the result.
- Prefer concrete visual facts over vague quality words.
- Avoid terms such as `stunning`, `epic`, `masterpiece`, `beautiful`,
  `premium`, and `insane detail` unless they are replaced by visible materials,
  lighting, layout, typography, or texture.
- Label each input image by role, such as `style reference`, `edit target`,
  `composition reference`, or `subject reference`.
- Put exact generated text under `Text (verbatim)` and specify placement, size,
  typography, colour, and `no duplicate text`.
- Use one built-in generation call per distinct asset or variant.
- Do not treat multiple variants as a substitute for separate prompts for
  distinct assets.

## Built-in workflow

1. Write the structured prompt under `prompts/generated/<family>/`.
2. Generate with Codex built-in `image_gen`.
3. Inspect the output for subject, style, composition, text accuracy, avoid-list
   compliance, and preservation invariants.
4. Copy or move accepted project-bound output into
   `assets/source/gpt-images-2/<family>/`.
5. Save it with a stable, descriptive, non-destructive filename.
6. Create a manifest under `assets/manifests/<family>/`.
7. Run post-processing only after the prompt and source image are persisted.
8. Update the manifest after every accepted post-processing step.

Discarded preview variants do not need manifests unless they influenced the
final decision or the user asks to keep them.

## Transparency workflow

Use built-in `image_gen` first for simple transparent or cutout assets. Prompt
the source on a perfectly flat chroma-key background, then remove the key
locally.

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
`gpt-image-1.5` because GPT Images 2 does not support `background=transparent`.

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
- critical runtime text remains deterministic.

## Day 2 request flow

A future character creator should write JSON requests under `assets/requests/`.
Codex development sessions can turn those requests into structured GPT Images 2
prompts, generate images, move accepted outputs into the workspace,
post-process them, update manifests, and let the app reload approved assets
from disk.

The Rust runtime must not pretend it can call Codex built-in `image_gen`
directly.
