# Prompt templates

These templates are the repository prompt standard for Codex built-in GPT
Images 2 work. Use them for development-time image prompts only. Runtime
layout, text, state, hit areas, charts, and UI behaviour remain owned by the
Rust renderer and deterministic asset pipeline.

Do not generate images while editing these templates.

## Standard generation schema

Use this labelled schema for every generation prompt unless a narrower
template in this directory applies:

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

## Standard edit schema

Use this schema for every edit prompt:

```plaintext
Change:
Preserve:
Constraints:
```

Repeat the full `Preserve` list every edit iteration.

## Template catalogue

- `character-sheet.md` defines Agentland character identity sheets.
- `animation-sheet.md` defines motion reference sheets.
- `environment-sheet.md` defines environment and spatial-zone sheets.
- `prop-cutout.md` defines chroma-keyed prop sources.
- `ui-ornament.md` defines UI ornament reference sheets.
- `edit-invariants.md` defines edit prompts with repeated preservation rules.
- `transparent-chromakey.md` defines flat-background transparent-source
  prompts.

## Repository rules

- Use built-in `image_gen` by default.
- Do not use CLI fallback unless explicitly requested or confirmed for true
native transparency.
- Do not rely on a destination-path argument for the built-in tool.
- After generation, copy project-bound outputs from the built-in output area
  into the workspace.
- Every accepted generated image needs a manifest.
- For transparent assets, generate on a perfectly flat chroma-key background,
  then run `tools/remove_chroma_and_validate.py`.
- Ask before using CLI `gpt-image-1.5` for true transparency.
- For edits, repeat the preserve list every iteration.
- For multi-image generation or compositing, label each input image by role.
- For exact text, put it under `Text (verbatim)` and specify typography,
  placement, colour, size, and `no duplicate text`.
- Important runtime UI text should be drawn by the Rust renderer, not baked
  into generated images.
