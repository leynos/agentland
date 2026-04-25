# Codex CLI prompt pack for built-in GPT Images 2 + Rust `pixels`

These prompts are written to be pasted directly into Codex CLI. They assume:

- Codex's image-generation skill is available.
- Built-in `image_gen` is the default path for raster image generation and edits.
- CLI fallback is used only when explicitly requested, or after a confirmed true native transparency fallback.
- The Rust renderer uses the `pixels` crate plus `winit`.
- Asset manifests are checked into `assets/manifests/`.
- Generated project-bound images must be copied into the workspace before code references them.

Use the prompts sequentially. Each one assumes the prior one has already completed. The flock has an order; no asset goose should wander off with an uncited PNG.

---

## Prompt 01 - Bootstrap the repo

```text
Work in a new repository for a pixel-art desktop mockup of an AI agent team
management tool set inside a hipster coffee shop with warm amber JRPG-style
lighting.

Use Codex's built-in image generation skill as the default image authoring path.
Do not configure or use PixelLab Model Context Protocol (MCP). Do not use the
image-generation CLI unless explicit CLI/API/model controls are requested, or a
true native transparency fallback is explicitly confirmed.

Assume the target renderer is Rust with the `pixels` crate plus `winit`.

Spawn three read-heavy subagents in parallel, wait for all of them, and then implement the result yourself:
1. An art-direction subagent that defines the visual grammar, scene layers, palette intent, and the boundary between GPT Images 2-generated references and algorithmic assets.
2. A runtime-architecture subagent that proposes the Rust module layout for a `pixels`-based renderer with fixed virtual resolution, sprite composition, lighting overlays, and hit-testing.
3. An asset-pipeline subagent that proposes the manifest schema, folder layout, and post-processing scripts for Codex `image_gen` outputs.

After all three return:
- create `AGENTS.md`
- create `.codex/config.toml` if missing, but do not overwrite an existing working config without preserving it
- create `docs/art-bible.md`
- create `docs/imagegen-workflow.md`
- create `docs/runtime-architecture.md`
- create `docs/asset-spec.md`
- create `assets/manifests/README.md`
- scaffold the Rust application with `pixels` + `winit`
- make the app open a window and render a placeholder layout at a fixed virtual resolution of 512x288
- implement placeholder rectangles for the top bar, centre scene viewport, and bottom stat cards
- ensure resize handling preserves integer-scaled pixel rendering
- document every assumption in the docs

Do not generate final art yet. This task is about structure, manifests, prompt standards, and a running placeholder renderer.
```

---

## Prompt 02 - Build the art bible from the approved mockup

```text
An approved reference mockup for the interface already exists; convert it into
an implementation-grade art bible for the repository.

Use the mockup as the visual source of truth. Do not call `image_gen` yet unless a tiny exploratory image is absolutely necessary.

Spawn two read-heavy subagents in parallel:
1. A composition analyst that decomposes the mockup into visual layers, focal areas, panel families, props, characters, lighting zones, typography behaviour, and dashboard hierarchy.
2. An asset strategist that classifies every needed asset into one of three buckets:
   - generate directly with built-in `image_gen`
   - generate with built-in `image_gen` as reference and convert into deterministic reusable pieces
   - create algorithmically with scripts or Rust code

Wait for both, then update `docs/art-bible.md`, `docs/imagegen-workflow.md`, and `docs/asset-spec.md` with:
- a full asset inventory
- a palette strategy
- character roster definitions
- environment prop definitions
- UI component families
- lighting notes
- text-in-image rules
- post-processing requirements
- explicit rules for what must be deterministic
- manifest requirements for built-in `image_gen` outputs

Also create prompt template files under `prompts/templates/` for:
- character reference sheets
- animation reference sheets
- prop cutouts
- environment sheets
- UI ornament references
- edit/invariant prompts
- transparent chroma-key prompts

Keep prompt language concrete. Prefer visual facts over vague praise. Do not
write prompts containing words such as "stunning", "epic", "masterpiece", or
"insane detail" unless they are replaced with visible materials, lighting,
composition, or typography.
```

---

## Prompt 03 - Install the GPT Images 2 prompt standard

```text
Create a repository prompt standard for Codex built-in GPT Images 2 work.

Update or create `docs/imagegen-workflow.md` and `prompts/templates/README.md` with this shared schema:

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

Also add a separate edit schema:

Change:
Preserve:
Constraints:

Rules to document:
- use built-in `image_gen` by default
- do not use CLI fallback unless explicitly requested or confirmed for true native transparency
- do not rely on a destination-path argument for the built-in tool
- after generation, copy project-bound outputs from the built-in output area into the workspace
- every accepted generated image needs a manifest
- for transparent assets, generate on a perfectly flat chroma-key background, then run the installed chroma-key removal helper
- ask before using CLI `gpt-image-1.5` for true transparency
- for edits, repeat the preserve list every iteration
- for multi-image generation or compositing, label each input image by role
- for exact text, put it under `Text (verbatim)` and specify typography, placement, and "no duplicate text"
- important runtime UI text should be drawn by the Rust renderer, not baked into generated images

Create these template files:
- `prompts/templates/character-sheet.md`
- `prompts/templates/animation-sheet.md`
- `prompts/templates/environment-sheet.md`
- `prompts/templates/prop-cutout.md`
- `prompts/templates/ui-ornament.md`
- `prompts/templates/edit-invariants.md`
- `prompts/templates/transparent-chromakey.md`

Do not generate images in this prompt. This is the prompt-law codex, not the paintbrush.
```

---

## Prompt 04 - Generate style anchors and design-book pages

```text
Use Codex's built-in `image_gen` tool to generate the first wave of visual style anchors for the coffee shop dashboard.

Stay on the built-in path. Do not use CLI fallback.

Create and persist manifests for these project-bound images:
- overview visual design book page
- character roster and personality guide page
- locations and environment guide page
- isometric environment sheet page
- UI material and ornament guide page

For each image:
- write the final structured prompt to `prompts/generated/style_guides/`
- use the shared prompt schema from `docs/imagegen-workflow.md`
- label any input reference images by role
- call built-in `image_gen`
- inspect the output for style match, text accuracy, layout quality, and obvious artefacts
- copy the accepted output into `assets/source/imagegen/style_guides/`
- create a manifest under `assets/manifests/style_guides/`
- write an evaluation note: approved, rejected, or iterate

Prompt requirements:
- richly detailed pixel-art design-book presentation
- warm amber coffee-shop lighting
- dark navy and brass UI framing
- wood, ceramic, parchment, and screen-glow material cues
- clean section hierarchy and legible title text
- no watermark
- no real brand logos
- no unrequested extra slogans

The goal is to establish the visual language before final asset extraction. Do not start slicing sprites yet.
```

---

## Prompt 05 - Generate character reference sheets

```text
Generate the main cast reference sheets for the coffee shop dashboard scene using Codex's built-in `image_gen` tool.

Characters needed:
- Ava: analyst / planner, research specialist
- Byte: robot assistant, operations manager
- Lex: focused operator, data analyst
- Sage: hooded knowledge worker, knowledge advisor
- optional charm pass: Nova, a systems engineer cat mascot

For each character:
- write a structured prompt file under `prompts/generated/characters/`
- use `Use case: stylized-concept`
- use `Asset type: pixel-art character reference sheet`
- include the approved dashboard-world style anchor as an input image if available, labelled as style reference
- ask for a clean sheet with standing view, seated working pose, expression chips, accessory callouts, and a simple uniform background
- keep identity details concise and concrete: silhouette, head/hair/hood, clothing, prop, attitude, palette accents
- avoid tiny text inside sprite poses
- call built-in `image_gen` once per character
- inspect the result
- copy approved outputs into `assets/source/imagegen/characters/`
- create per-character manifests under `assets/manifests/characters/`

After the sheets land:
- create or update `tools/slice_sheet.py`
- create or update `tools/quantize.py`
- create a first shared palette file under `assets/palette/coffee_shop_master_v1.json`
- add notes to `docs/art-bible.md` about which character details worked and which should be redrawn or cleaned manually

Do not claim these sheets are deterministic sprite atlases. Treat them as source references until slicing, cleanup, and validation pass.
```

---

## Prompt 06 - Generate animation reference sheets

```text
Generate animation reference sheets for the approved main cast.

Use built-in `image_gen`, not CLI fallback.

For each approved character where the source sheet is strong enough:
- load or reference the approved character sheet by role as Image 1
- write a structured prompt under `prompts/generated/animations/`
- ask for one animation at a time
- use a simple grid, such as 6 frames in one row or 8 frames in one row
- specify a flat uniform background for easy slicing
- preserve the same character identity, proportions, outfit, palette, and pixel-art rendering style
- avoid labels inside the frame cells
- avoid camera changes, scale changes, and extra props

Initial animations:
- idle blink or breathing loop
- typing or working loop
- thinking, reading, or small reaction loop

For each generated sheet:
- inspect frame consistency
- copy approved outputs into `assets/source/imagegen/animations/`
- create a manifest under `assets/manifests/animations/`
- run or stub `tools/slice_sheet.py`
- record whether the sheet is approved for runtime cleanup or reference only

Reject sheets that drift identity, change scale per frame, introduce noisy backgrounds, or cannot be sliced cleanly.
```

---

## Prompt 07 - Generate environments and isometric sheets

```text
Generate environment reference assets for the coffee shop dashboard world with built-in `image_gen`.

Create separate structured prompts for:
- main hipster coffee shop dashboard side-view scene
- isometric hipster coffee shop cutaway
- library archive
- neon data loft
- rooftop garden workspace
- observatory terrace
- bot workshop

For each environment:
- use `Use case: stylized-concept`
- use `Asset type: game environment concept art` or `isometric environment sheet`
- specify zones, props, light sources, materials, and intended use
- include palette and material cues: warm amber lamps, dark wood, brass trim, deep navy UI recesses, cyan screen glow, moss-green plants
- keep generated labels non-critical unless this is a design-book page
- avoid real logos and watermarks
- call built-in `image_gen` once per environment
- inspect composition, perspective, style match, and readability
- copy accepted outputs into `assets/source/imagegen/environments/`
- create manifests under `assets/manifests/environments/`

After generation:
- update `docs/art-bible.md` with environmental storytelling rules
- update `docs/asset-spec.md` with extractable prop and texture candidates
- create a list of zones that the Rust renderer will assemble deterministically rather than baking into one giant bitmap
```

---

## Prompt 08 - Generate prop cutouts and texture references

```text
Generate the environment prop set for the coffee shop dashboard scene.

Use built-in `image_gen` first. Do not use CLI fallback.

Props needed:
- espresso machine
- hanging lamp cluster
- shelving section
- books and bottles cluster
- mugs and cups
- potted plant
- laptop and desk clutter
- decorative sign
- brass corner ornament
- parchment label plaque

For simple opaque props that need alpha:
- prompt the prop on a perfectly flat solid chroma-key background
- use #00ff00 unless the prop contains green, then use #ff00ff
- require no shadow, no floor plane, no gradients, no texture, no reflection, and generous padding
- require the key colour not to appear inside the subject

After each built-in generation:
- copy the selected source image into `assets/source/imagegen/transparent_sources/`
- run the installed helper:

python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" --input <source.png> --out <alpha.png> --auto-key border --soft-matte --transparent-threshold 12 --opaque-threshold 220 --despill

- validate alpha corners, edge quality, subject coverage, and absence of green or magenta fringe
- retry once with `--edge-contract 1` if needed
- save final alpha images under `assets/processed/props/`
- create manifests under `assets/manifests/props/`

For complex transparent subjects such as fur, glass, smoke, liquids, translucent material, reflective objects, or soft realistic shadows, stop and ask before using true native transparency via CLI fallback.
```

---

## Prompt 09 - Build the post-processing pipeline

```text
Build the local post-processing pipeline for GPT Images 2 outputs.

Implement or update:
- `tools/quantize.py`
- `tools/crop_transparent.py`
- `tools/slice_sheet.py`
- `tools/crop_nineslice.py`
- `tools/pack_sprites.py`
- `tools/build_lightmask.py`
- `tools/sync_manifests.py`

Pipeline requirements:
- consume accepted images from `assets/source/imagegen/`
- never depend on files remaining under `$CODEX_HOME/generated_images/...`
- quantize approved assets toward `assets/palette/coffee_shop_master_v1.json`
- preserve glyph and generated-text assets separately where quantization would damage readability
- crop padding without clipping shadows or silhouettes
- slice sprite sheets only when grid validation passes
- atlas-pack approved sprites and props
- emit JSON metadata for Rust loading
- record post-processing notes back into manifests

Add tests or smoke checks where practical:
- alpha channel present for transparent props
- atlas metadata references existing files
- sprite frames share dimensions
- palette output stays within budget
- nine-slice descriptors have all required regions

Do not generate new art in this prompt. This is the little factory behind the café curtains.
```

---

## Prompt 10 - Build the deterministic UI kit

```text
Stop using ad hoc panel art. Build a deterministic UI kit.

Use the approved GPT Images 2 UI ornament references as source inspiration, but implement the final UI components algorithmically.

Tasks:
- implement nine-slice panel rendering
- implement tab rendering with active, inactive, and hover states
- implement status pills and progress bars
- implement task queue cards
- implement recent activity cards
- implement stat cards
- implement tiny chart and meter widgets
- implement icon rendering for repeated dashboard functions where algorithmic pixel icons are more robust than generated art
- keep all dimensions on a coherent spacing grid
- render important application text at runtime, not in generated images

If useful, generate one additional built-in `image_gen` UI ornament reference to
clarify the trim language, then convert it into deterministic reusable pieces
with `tools/crop_nineslice.py`. When generated, record the prompt, copy the
output into the workspace, and create a manifest immediately.

The runtime should own the final assembly:
- no hard-coded one-off panel bitmaps unless a manifest explicitly justifies them
- every widget should be reusable
- layout constants should live in code, not in scattered magic numbers

Update the app so the dashboard now looks structurally complete even if some scene art still needs polish.
```

---

## Prompt 11 - Compose the scene with generated references

```text
Integrate approved generated sources into the Rust `pixels` runtime.

Before coding:
- inspect `docs/art-bible.md`, `docs/asset-spec.md`, manifests, palette files, and processed atlas metadata
- identify which generated images are direct sources, which are references only, and which assets are still placeholders

Then:
- load approved atlases and metadata
- replace placeholder character rectangles with processed sprites where validation passed
- place characters so they feel seated and embedded in the coffee shop rather than pasted on top
- draw the environment in proper layer order
- add foreground overlap where appropriate
- preserve fixed virtual resolution and crisp scaling
- keep the UI readable over the scene
- render all critical UI text through the runtime text system

Add a lightweight debug overlay toggle showing:
- sprite bounds
- draw order
- asset IDs
- hit-test rectangles
- lighting mask extents

Update manifests or docs when an asset is used differently from its original plan.
```

---

## Prompt 12 - Add lighting, motion, and polish

```text
Polish the scene so it evokes warm JRPG café lighting without sacrificing dashboard readability.

Implement:
- hanging-lamp light pools
- subtle screen glow on faces and desks
- vignette
- selective rim highlights
- mild ambient animation such as lamp flicker or screen pulse
- agent card activity states
- micro-animations for status bars or queue pulses

Keep the effect restrained:
- readable UI beats dramatic lighting
- avoid muddy shadows
- keep the main work area brighter than the corners
- do not smear pixels with excessive blur
- keep animation loops quiet enough for a productivity dashboard

If the current architecture supports it cleanly, use a custom `pixels.render_with(...)` pass for the final full-screen lighting treatment. Otherwise implement it in the CPU compositor and document the trade-off.

Also perform a QA pass:
- test multiple integer scales
- verify hit detection maps through the scaled framebuffer
- verify text contrast
- verify generated signage spelling where any generated text remains visible
- verify that all final assets have manifests and provenance
```

---

## Prompt 13 - Hardening and review

```text
Run a hardening pass on the project.

Spawn three subagents in parallel:
1. Runtime reviewer: integer scaling, resize behaviour, sprite composition correctness, input mapping.
2. Asset pipeline reviewer: manifest completeness, prompt provenance, atlas packing, post-processing quality, no lingering dependency on `$CODEX_HOME/generated_images/...`.
3. UX reviewer: readability, motion restraint, panel consistency, status semantics, generated-text accuracy, and edit-invariant compliance.

Wait for all three, then:
- make any necessary fixes yourself
- add tests where practical
- add missing documentation
- add a short `docs/known-limitations.md`
- add a `docs/iteration-backlog.md` with sensible future improvements, clearly separated from the finished scope

Do not balloon scope. This pass is for correctness, consistency, and explicit limitations.
```

---

## Prompt 14 - Day 2 character brief authoring

```text
Add a Day 2 character brief authoring flow to the project.

Important boundary:
Codex's built-in `image_gen` tool is available to Codex during authoring sessions. It is not a runtime API that the Rust application can call directly. Do not implement the app as though it can invoke Codex's built-in tool.

Goal:
- the user edits structured character options in the UI or in a local authoring panel
- the app saves those options as a strict JSON character brief
- a Codex authoring session can read the brief, turn it into a structured GPT Images 2 prompt, call built-in `image_gen`, post-process the result, and import the asset
- the character appears in a preview panel once processed assets are available

Constraints:
- do not turn this into a generic chat client
- generated brief JSON must be strict and validated
- keep secrets out of logs and manifests
- do not add external image API calls unless explicitly requested
- store only the minimum runtime metadata needed for regeneration and provenance

Implementation tasks:
- create a character brief editor with structured controls
- define request and response structs with serde
- create a prompt template for converting a brief into the shared GPT Images 2 schema
- persist generated prompts and accepted output paths in manifests
- add a preview state machine for missing, pending, processed, rejected, and approved assets
- document the limitation that built-in Codex image generation is an authoring workflow, not app runtime infrastructure

Also create:
- `docs/day2-character-briefs.md`
- `src/day2/character_brief.rs`
- `src/day2/promptgen.rs`
- tests for JSON validation and state transitions
```

---

## Prompt 15 - Character brief JSON-to-prompt system prompt

Use this as the system prompt for any local text model or Codex-authored conversion step that turns structured character options into a GPT Images 2 prompt. It is not a runtime image-generation call.

```text
Generate concise, implementation-safe GPT Images 2 prompts for a pixel-art dashboard asset pipeline.

The job is to transform structured UI inputs plus an optional house-style brief
into strict JSON that maps cleanly onto the repository's shared
image-generation prompt schema.

Requirements:
- Output JSON only.
- Never output markdown.
- Keep visual instructions concise, concrete, and specific.
- Prefer nouns and adjectives that change silhouette, attitude, costume, lighting, prop, palette, material, and scene fit.
- Avoid vague praise such as stunning, epic, masterpiece, beautiful, premium, or cinematic unless replaced by visible details.
- Respect the provided house style.
- Do not invent unsupported tool arguments.
- Put exact in-image text only in `text_verbatim`.
- For character sheets, request a simple uniform background, clear spacing, and no tiny labels inside sprite poses.
- If the inputs are contradictory or insufficient, still return best-effort JSON using the safest coherent interpretation.

Return this schema exactly:
{
  "use_case": "stylized-concept",
  "asset_type": "pixel-art character reference sheet",
  "primary_request": "string",
  "input_images": [{"role": "string", "path": "string"}],
  "scene_backdrop": "string",
  "subject": "string",
  "style_medium": "string",
  "composition_framing": "string",
  "lighting_mood": "string",
  "color_palette": "string",
  "materials_textures": "string",
  "text_verbatim": "",
  "constraints": "string",
  "avoid": "string",
  "postprocess_intent": ["crop", "quantize", "slice reference poses"]
}
```

---

## Prompt 16 - Character brief user-prompt template

Use this as the user message body template for character brief conversion.

```text
House style:
{{house_style_brief}}

Approved style anchor images:
{{style_anchor_paths_and_roles}}

Role:
{{role}}

Archetype:
{{archetype}}

Silhouette cues:
{{silhouette}}

Head / hair / hood / hat:
{{head_features}}

Clothing:
{{clothing}}

Signature prop:
{{prop}}

Emotion / attitude:
{{emotion}}

Palette accents:
{{palette_accents}}

Scene fit:
This character should belong in a warmly lit pixel-art coffee shop dashboard scene and should read clearly at small sprite scale.

Additional notes:
{{additional_notes}}

Return strict JSON matching the required schema. Do not generate prose.
```

---

## Prompt 17 - One-shot full pipeline prompt

Use this only after the repo already has manifests, scripts, prompt templates, and a working runtime.

```text
A concentrated end-to-end feature pass is required.

Use Codex's built-in `image_gen` tool for image creation and editing by
default. Do not use CLI fallback unless explicitly requested or a true native
transparency fallback is explicitly confirmed.

Spawn subagents only for read-heavy analysis and review; keep actual code writing mostly in one thread.

Goal:
- finish the coffee shop dashboard scene
- use built-in GPT Images 2 for semantic raster references and source images
- use algorithmic generation for deterministic UI structure
- preserve manifest provenance for every generated asset
- keep the Rust `pixels` runtime clean, reusable, and fixed-resolution
- leave the repo in a runnable state with docs and tests updated

Before editing:
- inspect current docs, manifests, prompts, generated sources, processed atlases, and runtime modules
- identify what is still placeholder, inconsistent, undocumented, or not copied into the workspace

Then implement the missing work end-to-end:
- generate or iterate only the missing core assets
- copy accepted project-bound outputs into the workspace
- complete UI widget families
- integrate approved sprites and props
- polish lighting and motion
- harden manifests and post-processing
- update docs
- run tests and report any real blockers explicitly

Bias toward shipping a coherent, runnable vertical slice rather than beginning a giant unfinished architecture rewrite.
```

---

# Appendix A - Copy-paste GPT Images 2 asset prompts

These are starting points. Keep user-provided requirements. Do not inflate every prompt with extra lore.

## Character reference sheet

```text
Use case: stylized-concept
Asset type: pixel-art character reference sheet
Primary request: character sheet for Ava, a research specialist in a cosy AI agent dashboard world
Input images: Image 1: approved dashboard style anchor
Scene/backdrop: simple warm parchment backdrop with faint navy-and-brass frame motifs, no clutter
Subject: red-haired analyst with a thoughtful expression, dark apron over cream shirt, small notebook and coffee mug, readable silhouette at small sprite scale
Style/medium: richly detailed pixel art matching the warm coffee-shop dashboard world
Composition/framing: clean sheet with standing view, seated typing pose, 4 expression chips, and 3 accessory callouts; generous spacing; no labels inside the sprite poses
Lighting/mood: warm amber rim light with subtle cyan laptop glow
Colour palette: auburn hair, cream shirt, deep navy apron, brass accents, moss-green research icon accent
Materials/textures: cloth, leather notebook, ceramic mug, soft pixel dithering
Text (verbatim): "Ava" only once as a sheet title
Constraints: preserve house style; title must be readable; no watermark; no real logos; no extra characters
Avoid: photorealism; 3D render; busy background; duplicate names; tiny unreadable labels
```

## Animation reference sheet

```text
Use case: stylized-concept
Asset type: pixel-art animation reference sheet
Primary request: 6-frame typing loop for Ava from the approved character sheet
Input images: Image 1: approved Ava character sheet
Scene/backdrop: perfectly flat warm neutral background for frame slicing
Subject: same Ava, seated at a small laptop, hands moving through a subtle typing loop
Style/medium: same pixel-art style, same proportions, same outfit, same palette
Composition/framing: 6 evenly spaced frames in one horizontal row, consistent scale and baseline, no labels inside frames
Lighting/mood: warm amber edge light, subtle cyan screen glow
Constraints: preserve identity, outfit, silhouette, palette, and scale across all frames; no watermark
Avoid: camera changes; extra props; changing hairstyle; noisy background; text inside frames
```

## Isometric environment sheet

```text
Use case: stylized-concept
Asset type: isometric game environment sheet
Primary request: isometric cutaway of the hipster coffee shop agent workplace
Scene/backdrop: cosy brick-and-wood café interior with shelves, counter, plants, screens, and warm hanging lamps
Subject: four clearly labelled work zones: briefing desk, espresso bar, collaboration table, lounge corner
Style/medium: richly detailed pixel art, game environment concept sheet, crisp isometric perspective
Composition/framing: single isometric room diorama with small callout labels around the edges and clear empty margins
Lighting/mood: warm amber pendant pools, deep navy shadows, cyan screen glow on desks
Colour palette: coffee browns, walnut wood, brass gold, deep navy, cream highlights, moss green plants
Materials/textures: brick, wood grain, brass trim, ceramic cups, paper notes, glass jars
Text (verbatim): "Briefing Desk", "Espresso Bar", "Collab Table", "Lounge Corner"
Constraints: labels must be readable; no watermark; no real logos; no modern office sterility
Avoid: photorealism; 3D render; fisheye perspective; unreadable micro-text
```

## Prop cutout on chroma key

```text
Use case: stylized-concept
Asset type: pixel-art prop cutout source
Primary request: ornate brass corner ornament for a dashboard frame
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for local background removal
Subject: single brass corner ornament, 32 px game UI scale, symmetrical carved detail, readable silhouette
Style/medium: pixel-art game UI ornament, dark outline, restrained highlights
Composition/framing: centred object with generous padding, no cast shadow, no floor plane
Lighting/mood: soft warm highlight from upper left
Colour palette: brass gold, warm brown shadow, cream highlight; do not use #00ff00 in the subject
Materials/textures: aged brass, tiny pixel bevels, subtle patina
Text (verbatim): ""
Constraints: background must be one uniform colour with no gradients, texture, reflections, or lighting variation; crisp edges; no watermark
Avoid: green inside the subject; shadow; reflection; multiple objects; text
```

## UI ornament reference

```text
Use case: stylized-concept
Asset type: game UI ornament reference sheet
Primary request: navy-and-brass dashboard frame motif for a pixel-art agent management tool
Scene/backdrop: dark navy presentation sheet with no real app content
Subject: outer frame corners, tab trim, status pill trim, small divider ornaments, and parchment label plaque
Style/medium: pixel-art UI kit reference, ornate but readable, inspired by cosy café materials
Composition/framing: organised reference sheet with separated components and generous spacing
Lighting/mood: warm brass highlights, deep recessed navy panels, subtle enamel sheen
Colour palette: deep navy, slate blue, brass gold, walnut brown, cream highlights
Materials/textures: brass, dark enamel, carved wood, parchment label strips
Text (verbatim): "UI Ornament Reference" only once as title
Constraints: no watermark; no real logos; title readable; components separated for later slicing
Avoid: futuristic glass UI; generic SaaS cards; unreadable dense filigree; duplicate title text
```

## Edit with invariants

```text
Change:
Warm the hanging lamps and add a subtle cyan screen glow to the laptop areas.

Preserve:
Keep the original composition, characters, poses, dashboard layout, text placement, wood shelves, plant positions, camera angle, and pixel-art style unchanged.

Constraints:
Do not add new characters, signs, logos, or extra UI panels. No watermark. Do not blur or smear pixel edges.
```
