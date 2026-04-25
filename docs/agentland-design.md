# Codex Built-in GPT Images 2 + Rust `pixels` Style Guide

## 1. Objective

Build a desktop mockup of an AI agent team management tool rendered as a richly lit pixel-art workplace. The core fantasy is a cosy hipster coffee shop where software agents collaborate at laptops, terminals, books, coffee cups, shelves, lamps, and status panels. The output should feel like a tiny JRPG management sim fused with a production dashboard: warm, readable, characterful, and disciplined.

This version updates the earlier PixelLab Model Context Protocol (MCP) plan for
Codex's built-in GPT Images 2 image generation skill. The new pipeline treats
GPT Images 2 as a development-time raster asset and reference generator, while
Rust `pixels` remains the deterministic runtime compositor.

The intended result is a hybrid system:

- **Codex CLI** orchestrates planning, code generation, prompt authoring, image generation, review, post-processing, and integration.
- **Codex built-in `image_gen`** generates and edits raster images by default: style-book pages, character references, environment concepts, prop sheets, UI ornament references, texture references, and chroma-key cutout sources.
- **Algorithmic asset generation** produces repetitive or structurally constrained pieces: frames, tabs, buttons, dividers, graphs, nine-slice panels, lighting masks, text layout, status bars, debug overlays, and deterministic pixel icons.
- **Rust `pixels`** provides the low-level framebuffer renderer for the final application.

## 2. Important change from the PixelLab version

The previous plan assumed PixelLab MCP tools such as `create_character`, `create_map_object`, `create_tiles_pro`, `create_topdown_tileset`, and `animate_character`. The built-in GPT Images 2 workflow is different.

Use this mental model instead:

| Area | PixelLab-era assumption | GPT Images 2 built-in workflow |
| --- | --- | --- |
| Tool access | PixelLab MCP server in `.codex/config.toml` | Built-in Codex `image_gen` skill, preferred for normal generation and editing |
| API key | PixelLab token required | No `OPENAI_API_KEY` needed for built-in mode |
| Job model | Non-blocking jobs and polling | Built-in generation returns visible results and saved images under Codex's generated image area |
| Asset persistence | Store job IDs immediately | Move or copy selected outputs into the repo, then record prompt, source path, workspace path, edit history, and validation |
| Transparent assets | Tool-specific alpha support depended on PixelLab output | Built-in first: flat chroma-key background plus local removal helper. Ask before CLI fallback for true native transparency |
| Character consistency | Locked PixelLab parameters plus character IDs | Reference sheets, repeated anchor details, labelled input images, and strict preservation prompts. No sprite identity is truly seed-locked |
| Animations | Queue PixelLab animations | Treat GPT Images 2 sheets as concept or source art. Build final animation deterministically or crop approved frames with manual quality assurance (QA) |
| Batch assets | PixelLab jobs per asset | One built-in image generation call per distinct asset or variant unless the user explicitly selects CLI batch fallback |
| UI panels | Could use generated ornament pieces | Generate references only, then build final UI widgets algorithmically |

The dragon in the room: GPT Images 2 can create gorgeous concept and reference images, but it does not give a game-asset pipeline with guaranteed direction sets, sprite identity locks, animation loops, tile autotiling, or a stable seed contract in the built-in Codex surface. Design the repo around that truth rather than pretending the model is a tiny deterministic goblin press.

## 3. Codex image generation rules

### 3.1 Default tool mode

Use Codex's built-in `image_gen` tool by default for:

- new raster images
- editing images already visible to Codex
- visual variants from references
- style guides, concept sheets, mockups, spritesheet references, textures, props, and cutout sources
- simple transparent-background requests using chroma-key plus local removal

Do not add PixelLab MCP configuration to the repo. Do not ask for an API key for the built-in path.

### 3.2 CLI fallback

Use the fallback CLI only when the user explicitly asks for CLI/API/model controls, or when they explicitly confirm a true native transparency fallback. Do not silently downgrade or switch models.

In particular:

- `gpt-image-2` is the normal GPT Images 2 path.
- Do not set `input_fidelity` for GPT Images 2. Image inputs already use high fidelity in the documented guidance.
- Use CLI model, quality, output path, masks, and explicit size flags only when the user has chosen CLI mode.
- For true native transparent output, explain that the fallback uses `gpt-image-1.5` because GPT Images 2 does not support `background=transparent`, then ask before proceeding.

### 3.3 Project-bound save policy

For every generated image that the repo consumes:

1. Generate with built-in `image_gen`.
2. Inspect the output for subject, style, composition, text accuracy, avoid-list compliance, and preservation invariants.
3. Move or copy the selected output from Codex's generated image area into the workspace.
4. Save it under a stable, descriptive, non-destructive filename.
5. Record the final prompt and validation notes in an asset manifest.
6. Never leave a project-referenced image only under `$CODEX_HOME/generated_images/...`.

Suggested directories:

```text
assets/source/gpt-images-2/style-book/
assets/source/gpt-images-2/characters/
assets/source/gpt-images-2/environments/
assets/source/gpt-images-2/props/
assets/source/gpt-images-2/ui-ornaments/
assets/processed/
assets/atlases/
assets/manifests/
assets/palette/
```

## 4. Prompt grammar for this project

GPT Images 2 responds best to concrete structure. Every generation prompt should use this spine unless the user provides a more precise form:

```text
Use case:
Asset type:
Primary request:
Input images: (optional)
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

For longer prompts, linebreaks are not decoration. They are steering ropes. Keep each section short and specific.

### 4.1 Pixel-art additions

For this dashboard, add the following details when relevant:

```text
Pixel-art requirements:
Crisp pixel-art rendering, readable silhouettes, controlled dithering, no painterly smearing, no blurry anti-aliased edges in the subject, clear sprite-scale forms.

Runtime fit:
Designed as source/reference art for a 512x288 fixed-virtual-resolution Rust `pixels` renderer. Final runtime UI will be assembled deterministically.
```

Use these clauses judiciously. A design-book poster does not need the same restrictions as a tiny prop cutout.

### 4.2 Anti-slop rules

Avoid vague praise words as instructions. They add noise without telling the model what to render.

Weak:

```text
Stunning, epic, ultra-detailed, beautiful, award-winning, masterpiece, premium.
```

Useful:

```text
Warm amber pendant lamps, dark walnut shelves, brass trim, deep navy UI panels, pixel-perfect borders, legible cream typography, tiny cyan screen glows, moss-green status accents.
```

Say the real thing. If the scene needs a dashboard stat card, say dashboard stat card. If the asset must be a cutout espresso machine, say espresso machine cutout. If text matters, quote it exactly and say where it goes.

### 4.3 Text-in-image rules

Text can work, but it needs typography constraints.

Use this pattern:

```text
Text (verbatim): "AI Agent Dashboard"
Typography: large cream pixel-serif title, centred at the top, high contrast, clean kerning.
Constraints: render the text exactly once; no extra words; no duplicate text; no watermark.
```

For tricky labels, spell the intended copy in a separate line and keep the number of text elements small. For final runtime text, prefer deterministic bitmap fonts in Rust rather than generated text.

### 4.4 Edit prompts

Edits should separate change from preserve.

```text
Change:
Replace only the inactive tab colour with muted brass.

Preserve:
Keep the original layout, frame geometry, title text, character positions, lighting, pixel-art style, and all other UI panels unchanged.

Constraints:
No extra text, no new characters, no watermark, no redesign.
```

Repeat the preserve list on every edit. Do one revision per turn.

### 4.5 Multi-image prompts

Label each image by role.

```text
Input images:
Image 1: approved dashboard mockup to preserve for composition and mood.
Image 2: style-book page showing the preferred frame language.
Image 3: character roster reference for agent proportions and palette.

Primary request:
Generate a new isometric coffee-shop environment sheet using Image 1 for mood, Image 2 for presentation layout, and Image 3 for character scale.

Constraints:
Do not copy the reference exactly. Preserve the visual language: warm amber light, deep navy panels, brass trim, readable pixel forms, cosy work atmosphere.
```

## 5. House style

### 5.1 Scene mood

The world is a productive coffee shop that knows how to compile code and foam oat milk. It should feel warm rather than saccharine, detailed rather than cluttered, and playful rather than unserious.

Target qualities:

- warm amber key lights
- dark wood, brick, brass, ceramic, paper, leather, and glass
- deep navy or charcoal UI recesses
- cyan screen glow and small status lights
- moss green, slate blue, amber, and ember red state colours
- readable silhouettes at small scale
- controlled contrast: cosy, not muddy
- environmental detail that hints at ongoing work: half-full mugs, open notebooks, pinned notes, screens, books, tools, lamps, plants, and signs

### 5.2 Core palette

Use this palette as a target, not a prison:

| Name | Hex | Use |
| --- | --- | --- |
| Near black | `#07101B` | deepest panel recesses, outlines |
| Deep navy | `#0F1A2E` | main UI background |
| Slate blue | `#1E2B44` | inactive panels, inner fills |
| Coffee brown | `#4B2E1A` | shelves, leather, dark wood |
| Walnut wood | `#7A4A2B` | counter, furniture, props |
| Brass gold | `#D4AF37` | trim, icons, dividers |
| Warm amber | `#FFB347` | lamps, highlight glow |
| Candle glow | `#FFD98A` | bright light accents, title highlights |
| Moss green | `#2E5B3F` | active state, plant accents |
| Screen cyan | `#61D6FF` | displays, robot eyes, data glow |
| Ember red | `#B94A2E` | busy or warning states |
| Cream | `#F2E6C9` | text, parchment, high-contrast glyphs |

Generated source images may exceed this palette. Approved runtime assets should be quantized or remapped toward the shared palette unless the asset has a documented exception.

### 5.3 Pixel discipline

- Use crisp silhouettes and readable gestures over maximal detail.
- Keep final runtime sprites small enough to integrate at 512x288.
- Avoid generated micro-text in runtime assets. Render app text in code.
- Preserve outline consistency across characters and props.
- Allow richer source art for style-book pages, but simplify runtime pieces during post-processing.
- Test sprites at 1x, 2x, 3x, and 4x integer scales.

## 6. Character roster

The main team should support both dashboard readability and little narrative sparks.

| Character | Role | Silhouette and details | Primary colour accents | Runtime use |
| --- | --- | --- | --- | --- |
| Ava | Research Specialist | auburn hair, apron or waistcoat, laptop or clipboard, attentive posture | amber, cream, moss green | seated analyst card, research task activity |
| Byte | Operations Manager | rounded white robot shell, cyan face display, blue ear modules, small hands | screen cyan, cream, brass | central operations avatar, status animations |
| Lex | Data Analyst | dark hair, rolled sleeves, mug or tablet, focused expression | slate blue, brass, cyan | analytics card, report review state |
| Sage | Knowledge Advisor | brown hood, dark face void, glowing cyan eyes, book and quill | coffee brown, moss green, candle glow | support and Q&A card, knowledge scene |
| Nova | Systems Engineer | dark cat-like mascot or engineer, headset, wrench, calm competence | slate blue, cyan, brass | systems status, debug and infrastructure panels |
| Patch | Tech Tinkerer | fox or dog-like mechanic, goggles, overalls, tool belt | moss green, amber, walnut | workshop scenes, repair tasks |
| Ember | Community Liaison | red-orange hair, friendly expression, mug or megaphone | ember, cream, brass | announcements, team activity |
| Echo | Support Assistant | small hovering drone, cyan face display, tiny wings or propellers | cyan, cream, brass | help, notifications, onboarding tips |

### 6.1 Character reference workflow

Use GPT Images 2 for reference sheets, not as a guaranteed final animation factory.

Recommended output types:

- group roster sheet for global consistency
- individual character sheet with full-body pose, expression chips, and accessories
- small portrait chip sheet for UI cards
- sprite-scale static pose sheet for possible cropping
- edit iterations that preserve face, proportions, palette, outfit, and silhouette

Character consistency prompt pattern:

```text
Use case: stylized-concept
Asset type: pixel-art character reference sheet
Primary request: character sheet for Ava, the Research Specialist
Subject: same Ava identity across all poses; auburn hair, white shirt, dark apron, thoughtful face, laptop and notebook accessories
Style/medium: crisp cosy pixel-art reference sheet for a game UI
Composition/framing: full-body front pose, three small expression portraits, two accessory callouts, simple dark navy background, brass frame
Lighting/mood: warm amber rim light, subtle cyan screen glow
Colour palette: coffee brown, brass gold, cream, warm amber, moss green accents
Constraints: preserve one consistent character identity across the sheet; no extra text except labels requested; no watermark
Avoid: photorealism, blurry painterly edges, excessive tiny detail, inconsistent costumes
```

## 7. Environments and locations

Use environment sheets to establish spatial logic, lighting, and props. Use the runtime to assemble final compositions.

| Location | Function | Mood | Signature details |
| --- | --- | --- | --- |
| Hipster Coffee Shop | main dashboard workplace | warm, productive, social | bar counter, espresso machine, jars, shelves, plants, pendant lamps, dashboard panels |
| Library Archive | deep research and memory | quiet, timeless, focused | book stacks, ladders, lamps, globes, terminal bank, card drawers |
| Neon Data Loft | analytics and sprints | energetic, modern, collaborative | city view, neon motto, server racks, dashboards, cool cyan and magenta light |
| Rooftop Garden Workspace | solo focus and writing | calm, green, reflective | pergola, planters, string lights, city skyline, outdoor desks |
| Observatory Terrace | strategy and long-range thinking | serene, expansive, night-blue | telescope, stars, lanterns, city lights, charts and notebooks |
| Bot Workshop | prototyping and maintenance | hands-on, industrious, cluttered | workbench, tools, robot parts, monitors, soldering gear, labelled drawers |

### 7.1 Environment prompt pattern

```text
Use case: stylized-concept
Asset type: isometric game environment concept sheet
Primary request: isometric cutaway of the Hipster Coffee Shop agent workplace
Scene/backdrop: cosy brick-and-wood coffee shop interior with shelves, counter, plants, pendant lamps, and workstation tables
Subject: four AI agents working in clearly separated zones: briefing desk, espresso bar, collab tables, lounge corner
Style/medium: richly detailed crisp pixel-art environment sheet, game art bible presentation
Composition/framing: 3/4 isometric cutaway, readable zones, small callout labels, generous dark navy border
Lighting/mood: warm amber pendant lamps, subtle cyan screen glows, darker corners, bright focal work area
Colour palette: deep navy, coffee brown, walnut, brass, cream, warm amber, moss green, screen cyan
Materials/textures: brick, reclaimed wood, brass trim, ceramic mugs, glass jars, paper notes, leafy plants
Text (verbatim): "Hipster Coffee Shop", "Briefing Desk", "Espresso Bar", "Collab Tables", "Lounge Corner"
Constraints: text must be readable; no watermark; no extra location labels; no photorealism
Avoid: muddy shadows, clutter that obscures agents, unstructured fantasy scenery
```

## 8. UI and deterministic runtime design

The UI is a product interface, not just decoration. Keep generated imagery out of the critical text and layout path.

### 8.1 Generated references

Use GPT Images 2 to explore:

- outer frame language
- brass corner motifs
- dashboard card mood
- title treatment
- icon family references
- status badge style
- design-book presentation pages

### 8.2 Algorithmic final UI

Build these in Rust or scripts:

- nine-slice panels
- active, inactive, and hover tabs
- status pills
- progress bars
- task queue cards
- recent activity cards
- stat cards
- small charts and meters
- bitmap icons for repeated dashboard actions
- text layout, clipping, and contrast rules
- focus rings, cursor, tooltip shells, modals

Runtime text should come from a bitmap font or code-rendered glyph atlas. Generated UI mockups can include text for concept validation, but final dashboard copy should not depend on generated lettering.

## 9. Transparent and cutout assets

Use built-in GPT Images 2 first with a flat chroma-key background.

Prompt pattern:

```text
Use case: background-extraction
Asset type: pixel-art prop cutout source
Primary request: isolated espresso machine for a cosy pixel-art coffee shop dashboard
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for local background removal
Subject: brass-and-steel espresso machine with small cups, dark wood base, warm highlights, readable at small game-prop scale
Style/medium: crisp pixel-art prop, no scene background
Composition/framing: centred object with generous padding, straight-on slight 3/4 view
Lighting/mood: warm amber highlights on metal, no cast shadow
Colour palette: brass gold, steel grey, walnut brown, cream highlights; do not use #00ff00 in the subject
Constraints: background must be one uniform colour with no shadows, gradients, texture, reflections, floor plane, or lighting variation; crisp silhouette; no halos; no watermark; no text
Avoid: green reflections, transparent glass complexity, smoke, steam, fur, soft shadows
```

Post-processing sequence:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" \
  --input <source.png> \
  --out <final.png> \
  --auto-key border \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 220 \
  --despill
```

Validate alpha, corners, edge fringing, subject coverage, palette, and scale. If a thin fringe remains, retry once with `--edge-contract 1`. Ask before using CLI true transparency for hair, fur, smoke, glass, liquids, translucent materials, reflective product grounding, or soft shadows.

## 10. Asset taxonomy

### 10.1 Generated directly with GPT Images 2

Use built-in `image_gen` directly for:

- visual design-book pages
- character roster sheets
- individual character reference sheets
- expression and accessory sheets
- environment concept sheets
- isometric cutaway sheets
- UI ornament references
- rich scene backplates for inspiration
- prop cutout source images on chroma-key backgrounds
- tile and material reference sheets
- marketing or presentation images for the project

### 10.2 GPT Images 2 as reference, algorithm as final output

Generate references, then derive deterministic runtime pieces for:

- panel frames
- tab trims
- stat card ornament families
- icon style guides
- bevel and trim language
- colour ramps
- material motifs
- texture studies
- lighting mood references

### 10.3 Pure algorithmic generation

Generate without AI:

- final nine-slice panel renderer
- charts, meters, separators, and grids
- tile repeats that need exact seams
- palette quantization
- outline normalization
- sprite atlas packing
- transparency cleanup validation
- procedural lighting masks
- hit-testing bounds
- layout constants
- runtime text

## 11. Repository layout

```text
.
├─ AGENTS.md
├─ .codex/
│  ├─ config.toml
│  └─ agents/
│     ├─ art_director.toml
│     ├─ image_prompt_designer.toml
│     ├─ asset_integrator.toml
│     ├─ pixels_implementer.toml
│     └─ qa_reviewer.toml
├─ prompts/
│  ├─ 01-bootstrap.md
│  ├─ 02-art-bible.md
│  ├─ 03-style-anchors.md
│  ├─ 04-characters.md
│  ├─ 05-environments.md
│  ├─ 06-props-cutouts.md
│  ├─ 07-ui-kit.md
│  ├─ 08-runtime-composition.md
│  ├─ 09-polish-lighting.md
│  ├─ 10-hardening.md
│  └─ templates/
│     ├─ gpt-image-2-shared.md
│     ├─ character-sheet.md
│     ├─ environment-sheet.md
│     ├─ prop-chromakey.md
│     ├─ ui-ornament-reference.md
│     └─ edit-invariants.md
├─ docs/
│  ├─ art-bible.md
│  ├─ asset-spec.md
│  ├─ runtime-architecture.md
│  ├─ imagegen-workflow.md
│  ├─ prompt-style-guide.md
│  ├─ known-limitations.md
│  └─ iteration-backlog.md
├─ assets/
│  ├─ source/gpt-images-2/
│  ├─ processed/
│  ├─ atlases/
│  ├─ manifests/
│  └─ palette/
├─ src/
│  ├─ main.rs
│  ├─ app.rs
│  ├─ input.rs
│  ├─ scene.rs
│  ├─ layout.rs
│  ├─ text.rs
│  ├─ timing.rs
│  ├─ assets/
│  │  ├─ manifest.rs
│  │  ├─ atlas.rs
│  │  └─ import.rs
│  ├─ render/
│  │  ├─ compositor.rs
│  │  ├─ sprites.rs
│  │  ├─ nine_slice.rs
│  │  └─ charts.rs
│  ├─ lighting/
│  │  ├─ masks.rs
│  │  └─ post.rs
│  └─ day2/
│     ├─ prompt_composer.rs
│     └─ asset_request.rs
└─ tools/
   ├─ quantize.py
   ├─ remove_chroma_and_validate.py
   ├─ crop_nineslice.py
   ├─ pack_sprites.py
   ├─ build_lightmask.py
   └─ sync_manifests.py
```

## 12. Manifest format

Treat generation metadata as source code. Built-in image generation may not provide a job ID in the same way a remote job queue does, so preserve the information that actually matters: prompt, reference roles, selected source file, workspace file, edits, post-processing, validation, and runtime integration.

Example `assets/manifests/characters/ava_reference_sheet.json`:

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
    "use_case": "stylized-concept",
    "asset_type": "pixel-art character reference sheet",
    "text": "Use case: stylized-concept\nAsset type: pixel-art character reference sheet\nPrimary request: character sheet for Ava...",
    "input_images": [
      {
        "label": "Image 1",
        "role": "approved dashboard mood and composition reference",
        "path": "assets/source/references/approved-dashboard.png"
      }
    ]
  },
  "files": {
    "codex_generated_path": "$CODEX_HOME/generated_images/.../ava-reference.png",
    "workspace_source_path": "assets/source/gpt-images-2/characters/ava-reference-v1.png",
    "processed_path": "assets/processed/characters/ava-reference-v1.quantized.png"
  },
  "validation": {
    "subject_correct": true,
    "style_match": true,
    "text_accuracy": "no generated text used",
    "composition_notes": "consistent with roster sheet; readable silhouette; good accessory separation",
    "rejection_notes": null
  },
  "postprocess": {
    "palette": "coffee_shop_master_v1",
    "crop_transparent_bounds": false,
    "normalize_outline": true,
    "atlas": null
  },
  "runtime_use": "reference only; final runtime portrait cropped manually after approval"
}
```

For chroma-key cutouts, include helper settings:

```json
{
  "postprocess": {
    "background_removal": {
      "method": "chroma_key_helper",
      "key": "auto_border",
      "transparent_threshold": 12,
      "opaque_threshold": 220,
      "soft_matte": true,
      "despill": true,
      "edge_contract": 0
    },
    "alpha_validation": {
      "has_alpha": true,
      "transparent_corners": true,
      "visible_key_fringe": false
    }
  }
}
```

## 13. Codex configuration strategy

The built-in image generation tool does not require an MCP server entry. Keep `.codex/config.toml` simple unless the repo needs network for other reasons.

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = false

[agents]
max_threads = 4
max_depth = 1
```

Set `network_access = true` only when the repo actually needs shell-side downloads, API tests, or explicit CLI fallback workflows.

### 13.1 `AGENTS.md` baseline

```md
# Project instructions

## Image generation workflow

- Use Codex's built-in `image_gen` tool by default for raster image generation and editing.
- Do not configure PixelLab MCP for this project.
- Do not ask for `OPENAI_API_KEY` unless the user explicitly chooses CLI/API fallback.
- For transparent assets, use a flat chroma-key background and local removal first.
- Ask before using CLI `gpt-image-1.5` for true native transparency.
- Move or copy every project-bound generated image into the workspace before referencing it.
- Save every prompt, reference-image role, selected output path, post-processing step, and validation note in `assets/manifests/`.
- Use one built-in generation call per distinct asset or variant; do not treat `n` as a substitute for separate asset prompts.
- For edits, state exactly what changes and list the invariants that must be preserved.
- Iterate with one targeted change at a time.

## Runtime workflow

- Use Rust `pixels` with a fixed 512x288 virtual resolution.
- Preserve integer scaling and crisp pixel presentation.
- Use generated images as source or reference assets, not as layout authority.
- Build final UI panels, text, status bars, charts, and recurring icons algorithmically.
- Quantize, crop, and atlas-pack approved runtime assets.
```

## 14. Recommended custom agents

### 14.1 `art_director.toml`

Purpose:

- maintain the house style
- review prompts for concrete visual facts
- classify assets into built-in imagegen, imagegen-as-reference, or algorithmic
- reject incoherent or redundant requests

### 14.2 `image_prompt_designer.toml`

Purpose:

- write structured GPT Images 2 prompts
- label reference images by role
- prepare edit prompts with change and preserve sections
- avoid unsupported CLI-only arguments in built-in mode

### 14.3 `asset_integrator.toml`

Purpose:

- move selected generated images into the workspace
- create manifests
- run post-processing scripts
- pack atlases
- update asset references

### 14.4 `pixels_implementer.toml`

Purpose:

- build the Rust runtime
- own layout, blitting, input mapping, lighting, text, and sprite integration

### 14.5 `qa_reviewer.toml`

Purpose:

- detect palette drift
- detect inconsistent scale
- verify prompt provenance
- verify transparency quality
- verify integer scaling, hit-testing, and text contrast

## 15. Implementation plan

### Phase 1: bootstrap

- create repo
- add Codex config, AGENTS guidance, prompt pack, and manifest schema
- scaffold Rust app with `pixels` + `winit`
- render placeholder coloured rectangles only

### Phase 2: art bible

- analyse the approved mockup image
- produce asset list, palette targets, composition map, and prompt templates
- decide what becomes built-in imagegen output, what becomes imagegen reference, and what becomes procedural

### Phase 3: style anchors

- generate a small visual design book set:
  - dashboard world page
  - character roster page
  - locations guide
  - isometric environment sheet
- save selected outputs under `assets/source/gpt-images-2/style-book/`
- record prompts and validation notes

### Phase 4: character references

- generate a group roster sheet
- generate individual character sheets
- crop or derive approved portrait chips
- document identity anchors for each character
- do not rely on model output for final animation loops without manual QA

### Phase 5: environment and props

- generate environment concept sheets and backplates
- generate prop cutout sources on flat chroma-key backgrounds
- remove backgrounds locally and validate alpha
- quantize and atlas-pack approved props

### Phase 6: deterministic UI kit

- build nine-slice panels, tabs, buttons, stat cards, charts, and icons algorithmically
- use generated ornament references only as style inspiration
- render all final dashboard text with runtime glyphs

### Phase 7: composition and lighting

- integrate sprites and backplates into the Rust compositor
- add procedural lamp pools, screen glow, vignette, and focus highlights
- preserve readability over drama

### Phase 8: hardening

- review manifests, prompts, paths, and provenance
- test integer scaling and hit-testing
- add known limitations and iteration backlog

## 16. Day 2: prompt composer, not magic runtime generation

Codex's built-in `image_gen` tool is a development workflow, not a Rust runtime API. The app should not pretend it can directly call the Codex tool.

A sensible Day 2 feature is a **prompt composer panel**:

1. user edits structured character options in the Rust UI
2. app writes a JSON asset request under `assets/requests/`
3. Codex reads the request during a development session
4. Codex turns it into a structured GPT Images 2 prompt
5. Codex generates the image, moves it into the workspace, post-processes it, and updates manifests
6. the app reloads the approved asset from disk

If the actual product needs user-triggered runtime image generation, design a separate OpenAI Images API integration. Keep that separate from the Codex built-in tool, with explicit API keys, error handling, moderation, cost controls, and user consent.

Example request schema:

```json
{
  "type": "character_reference_request",
  "role": "support analyst",
  "archetype": "calm owl-like night-shift helper",
  "silhouette": "small rounded body, oversized headphones, tiny notebook",
  "head_features": "owl-like face markings, no realistic animal gore or threat",
  "clothing": "dark cardigan, brass pin, soft scarf",
  "signature_prop": "small cup of tea",
  "emotion": "patient and observant",
  "palette_accents": "screen cyan, brass, moss green",
  "scene_fit": "warm coffee shop dashboard, readable at small sprite scale",
  "generation_mode": "codex_development_time"
}
```

## 17. Risks and mitigations

### Risk 1: generated sprites look great but fail at runtime scale

Mitigation:

- validate at target scale before approval
- crop to portraits if full-body sprites fail
- simplify through manual or algorithmic post-processing
- keep runtime UI deterministic

### Risk 2: character consistency drift

Mitigation:

- create roster and individual reference sheets early
- repeat anchor details in every prompt
- label input reference images by role
- use edit prompts that preserve identity, face, proportions, outfit, and palette
- reject inconsistent outputs rather than warping the design around them

### Risk 3: unreadable generated text

Mitigation:

- use generated text only in style-book and concept work
- quote exact text and specify placement for concept images
- render final app text in code

### Risk 4: transparency artifacts

Mitigation:

- use flat chroma-key backgrounds with generous padding
- avoid shadow, smoke, glass, fur, hair, and reflective complexity in cutout prompts
- run alpha validation
- ask before true native transparency fallback

### Risk 5: prompt drift through over-augmentation

Mitigation:

- preserve user requirements
- add only details that materially improve output quality
- keep prompt sections concrete
- avoid extra story elements not implied by the task

## 18. Recommendation

The strongest route is a hybrid pipeline:

- GPT Images 2 built-in for visual exploration, style anchors, character references, environment sheets, prop cutout sources, and edit iterations
- scripts for cutout cleanup, quantization, atlas packing, and deterministic texture/UI preparation
- Rust `pixels` for fixed-resolution composition, input, text, widgets, and lighting
- Codex CLI as the single orchestrator, with subagents for planning and review rather than chaotic parallel writing

That yields a practical creative furnace without surrendering the runtime to
stochastic soup.
