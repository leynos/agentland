# Asset specification

## Scope

This document defines where Agentland stores generated sources, processed
runtime assets, manifests, palettes, validation data, and asset requests. It
also defines the promotion contract used before any generated image becomes
part of the deterministic product surface.

The approved mockups under `ref/` are visual source material. They are not
runtime assets and should not be treated as sprite atlases, layout files, or
text authorities.

## Repository layout

Use this layout as assets are introduced:

```text
prompts/
├─ generated/
│  ├─ style-book/
│  ├─ characters/
│  ├─ animations/
│  ├─ environments/
│  ├─ props/
│  └─ ui-ornaments/
└─ templates/
assets/
├─ source/
│  ├─ gpt-images-2/
│  │  ├─ style-book/
│  │  ├─ characters/
│  │  ├─ animations/
│  │  ├─ environments/
│  │  ├─ props/
│  │  ├─ ui-ornaments/
│  │  └─ transparent-sources/
│  └─ references/
├─ processed/
│  ├─ characters/
│  ├─ animations/
│  ├─ props/
│  ├─ ui/
│  ├─ environments/
│  └─ lightmasks/
├─ atlases/
│  ├─ characters/
│  ├─ props/
│  ├─ ui/
│  └─ environment/
├─ manifests/
├─ palette/
├─ validation/
└─ requests/
```

Create directories only when a change needs them.

## Canonical classification values

This section is the canonical source for bucket and `intent_class` values.
Other documents and prompt templates may use the numeric shorthand, but
manifests must use the string identifier from this table.

| Shorthand | Manifest `bucket` value | Meaning |
| --- | --- | --- |
| Bucket 1 | `direct-generated-reference` | Built-in `image_gen` output kept as reference, style-book, or concept art. It is not a runtime dependency. |
| Bucket 2 | `generated-source-converted` | Built-in `image_gen` output used as source for deterministic crops, slices, cleaned sprites, cutouts, texture studies, or ornament references. |
| Bucket 3 | `algorithmic` | Scripts, Rust code, metadata, palette files, light masks, layout, text, charts, validation reports, or other code-owned assets. |

Allowed `intent_class` values are:

- `reference-only`: human-facing source of truth that is not loaded at runtime.
- `sliceable-source`: image source intended for deterministic crop or slice.
- `ornament-source`: image source intended for trim, plaque, badge, or
  nine-slice extraction.
- `runtime-processed`: cleaned output approved for runtime loading.
- `lightmask-source`: deterministic mask image or generated reference for mask
  placement.
- `layout-reference`: visual reference for spacing, zone naming, or spatial
  hierarchy.

Use the numeric bucket shorthand in tables where it keeps the layout readable.
Use the manifest string values in JSON and validation output.

## Full asset inventory

| Asset | Bucket | Source or path family | Post-processing | Runtime determinism | Manifest requirement |
| --- | --- | --- | --- | --- | --- |
| Approved design-book pages 9-12 | 1 | `ref/design-book-*.png` | Inspect only | Reference only; no runtime dependency | Manifest only if copied into `assets/source/` |
| Future art-bible presentation sheets | 1 | `prompts/generated/style-book/` and `assets/source/gpt-images-2/style-book/` | Inspect, optional palette notes | Not loaded by runtime | `style-guide`, `reference-only` |
| Character roster overview | 1 | `prompts/generated/characters/roster-v*.md` | Validate names, silhouettes, accessories | Reference only | `character-reference` |
| Individual character reference sheets | 1 | `assets/source/gpt-images-2/characters/` | Inspect identity, pose, expression, accessory fit | Reference only until processed | One `character-reference` manifest per sheet |
| Standing character sprites | 2 | `assets/processed/characters/<name>-stand-v*.png` | Slice or redraw, crop, anchor, quantize, scale-check | Fixed frame size, anchor, palette, draw layer | Source manifest plus atlas manifest |
| Seated or working character sprites | 2 | `assets/processed/characters/<name>-seated-v*.png` | Cleanup, crop, occlusion test, quantize | Fixed placement, anchor, z-layer | Source manifest plus atlas manifest |
| Character portrait chips | 2 | `assets/processed/characters/portraits/` | Crop to standard slot, quantize, readability check | Fixed portrait metrics, no baked labels | Processed path and crop metadata |
| Expression chips | 2 | `assets/processed/characters/expressions/` | Slice grid, reject drift, normalize bounds, pack | Equal cell size and named expression IDs | Slice metadata and atlas manifest |
| Accessory callouts | 2 | `assets/processed/props/accessories/` | Crop, alpha cleanup, quantize, classify | Fixed prop or icon IDs | Linked to source sheet |
| Animation reference sheets | 1 | `assets/source/gpt-images-2/animations/` | Inspect consistency; do not promote automatically | Reference only by default | `animation-reference` |
| Runtime animation frames | 2 | `assets/processed/animations/<name>/<motion>/` | Slice, clean, anchor, quantize, pack | Fixed frame count, timing, loop mode | Source slice data and atlas manifest |
| Procedural micro-animation timing | 3 | `src/timing.rs` or future timing modules | Code validation | Deterministic tick model | No image manifest |
| Coffee-shop side-view concept | 1 | `assets/source/gpt-images-2/environments/` | Inspect composition and material fit | Reference only | `environment-reference` |
| Isometric environment concepts | 1 | `assets/source/gpt-images-2/environments/` | Inspect zones and scale | Reference only | `environment-reference` |
| Observatory and workshop concepts | 1 | `assets/source/gpt-images-2/environments/` | Inspect signature props and lighting | Reference only until needed | `environment-reference` |
| Runtime coffee-shop backplate layers | 2 | `assets/processed/environments/coffee-shop/` | Split wall, shelves, counter, floor, foreground | Fixed 512x288 layer placement | Environment source plus atlas manifest |
| Brick, floor, wood, shelf texture tiles | 2 | `assets/processed/environments/tiles/` | Crop, seam-check, quantize | Exact tile dimensions and repeats | `texture-reference` plus atlas manifest |
| Espresso machine | 2 | `assets/source/gpt-images-2/transparent-sources/` | Chroma-key, crop, despill, quantize, scale-check | Fixed bounds, anchor, layer | `prop-cutout` with background-removal settings |
| Pendant lamp fixtures | 2 | `assets/processed/props/lighting/` | Alpha cleanup, crop, quantize | Fixture sprite fixed; glow code-owned | `prop-cutout` plus light-origin notes |
| Shelves with jars, books, and bottles | 2 | `assets/processed/props/shelves/` | Crop or split, simplify, quantize | Deterministic background prop layer | `prop-cutout` or `texture-reference` |
| Books and notebooks | 2 | `assets/processed/props/books/` | Crop variants, alpha cleanup, quantize | Fixed small-prop IDs and anchors | `prop-cutout` |
| Mugs and cups | 2 | `assets/processed/props/cups/` | Chroma-key, crop variants, scale-check | Deterministic prop variants | `prop-cutout` with variant slices |
| Potted plants and greenery | 2 | `assets/processed/props/plants/` | Chroma-key, edge check, quantize | Fixed bounds; sway code-owned if any | `prop-cutout` |
| Laptops, terminals, and small screens | 2 | `assets/processed/props/devices/` | Crop, quantize, define screen regions | Device sprite fixed; screen content Rust-owned | `prop-cutout` plus screen-region metadata |
| Desk clutter | 2 | `assets/processed/props/clutter/` | Slice small props, simplify, quantize | Scene data controls placement | `prop-cutout` or atlas manifest |
| Sign and chalkboard frames | 2 | `assets/processed/ui/signs/` | Remove or ignore generated text, crop, quantize | Frame only; text Rust-owned | `ui-ornament-reference` |
| Brass corner ornaments | 2 | `assets/processed/ui/ornaments/` | Crop, normalize, quantize | Deterministic corner sprites or code motifs | `ui-ornament-reference` plus atlas if used |
| Parchment plaques | 2 | `assets/processed/ui/plaques/` | Crop, define nine-slice metrics, quantize | Geometry and text deterministic | `ui-ornament-reference` |
| Outer frames and dividers | 2 | `assets/processed/ui/frames/` | Crop, redraw, or derive nine-slice metrics | Fixed border thickness and corner rules | `ui-ornament-reference` |
| Nine-slice panels | 3 | Future Rust render module or checked metrics | Validate slice regions if sprite-backed | Deterministic scaling and clipping | Atlas manifest only if image-backed |
| Tabs | 3 | Future Rust user interface (UI) module | None | Code-owned active, hover, focus states | No image manifest |
| Stat cards and task cards | 3 | Future Rust UI module | None | Code-owned layout and content | No image manifest |
| Status pills | 3 | Future Rust UI module and palette file | None | Code-owned enum, colour, label, icon | No image manifest |
| Progress bars and meters | 3 | Future Rust render module | None | Exact data-to-pixel mapping | No image manifest |
| Charts and analytics widgets | 3 | Future Rust render module | None | Code-owned values and axes | No image manifest |
| Repeated dashboard icons | 3 | Future Rust icon module or generated bitmap atlas by script | Validate IDs, sizes, states | Fixed glyph IDs and dimensions | Atlas manifest if bitmap-backed |
| Decorative one-off icons in reference pages | 1 | Style-book pages | Inspect only | Not runtime | Covered by style-guide manifest |
| Typography references | 1 | Style-book or UI-ornament references | Inspect hierarchy and legibility | Reference only | `runtime_text_safe` must be explicit |
| Runtime bitmap font or glyph atlas | 3 | Future `src/text.rs` or `assets/processed/ui/font-*` | Validate glyph metrics and contrast | Deterministic string layout | Atlas manifest if bitmap-backed |
| Runtime labels and strings | 3 | Rust source or data files | None | Fully deterministic | No image manifest |
| Master palette | 3 | `assets/palette/coffee_shop_master_v1.json` | Validate names, hex, ramps | Single source for scripts and runtime | No image manifest |
| Colour ramps | 3 | `assets/palette/ramps/` | Validate ramp entries | Deterministic remapping | No image manifest |
| Amber lamp pools | 3 | Rust lighting or `assets/processed/lightmasks/` | Validate alpha and intensity | Fixed origins and blend mode | `lightmask` if persisted |
| Cyan screen glows | 3 | Rust lighting or generated masks | Validate screen-region fit | Deterministic per device state | `lightmask` if persisted |
| Vignette and ambient shadow | 3 | Rust compositor or generated mask | Validate contrast and readability | Deterministic blend formula | `lightmask` if persisted |
| Cursor, focus rings, tooltips, debug overlays | 3 | Runtime code | None | Code-owned interaction state | No image manifest |
| Hit-test and draw-order metadata | 3 | Rust structs or atlas JSON | Schema validation | Deterministic input mapping | Atlas or validation metadata |
| Character, prop, UI, and environment atlases | 3 | `assets/atlases/**` | Deterministic packing and validation | Stable sprite IDs, rects, anchors | `atlas` manifest |
| Atlas metadata JSON | 3 | `assets/atlases/**/*.json` | Schema and path validation | Runtime loading contract | `atlas` manifest |
| Chroma-key removal outputs | 2 | `tools/remove_chroma_and_validate.py` outputs | Alpha validation and despill | Deterministic command settings recorded in the Bucket 2 source manifest | Source manifest postprocess update required before runtime promotion |
| Quantized runtime assets | 2 | `tools/quantize.py` outputs | Palette remap and readability check | Deterministic palette mapping recorded in the Bucket 2 source manifest | Source manifest postprocess update required before runtime promotion |
| Sprite slicing metadata | 3 | `tools/slice_sheet.py` outputs | Equal-cell and bounds checks | Deterministic frame extraction | Source manifest `slice` data |
| Nine-slice crop metrics | 3 | `tools/crop_nineslice.py` outputs | Validate all nine regions | Deterministic panel rendering | Ornament and atlas manifests |
| Manifest schema and checks | 3 | `tools/check_manifests.py` | JSON schema validation | Deterministic gate | Governs all manifests |
| Asset validation reports | 3 | `assets/validation/` | Deterministic report generation | Evidence for promotion | Referenced from manifests |
| Day 2 asset request JSON | 3 | `assets/requests/` | JSON schema validation | Runtime writes requests only | Accepted outputs get normal manifests later |
| Prompt templates | 3 | `prompts/templates/` | Markdown validation | Deterministic prompt structure | No asset manifest |
| Prompt files for accepted outputs | 3 | `prompts/generated/<family>/` | Review concrete language and banned terms | Deterministic provenance input | Required by each generated-image manifest |

## Manifest status values

Use one JSON manifest per accepted project-bound image. Store it under
`assets/manifests/<family>/<asset-id>.json`.

Allowed `status` values:

- `approved-source`
- `approved-runtime`
- `reference-only`
- `rejected`
- `superseded`

Allowed `family` values:

- `style-guide`
- `character-reference`
- `animation-reference`
- `environment-reference`
- `prop-cutout`
- `ui-ornament-reference`
- `texture-reference`
- `atlas`
- `lightmask`

## Manifest shape

Use this baseline structure:

```json
{
  "id": "ava_reference_sheet_v1",
  "family": "character-reference",
  "status": "approved-source",
  "bucket": "direct-generated-reference",
  "intent_class": "reference-only",
  "tool": {
    "mode": "codex_builtin_image_gen",
    "model_family": "gpt-images-2",
    "fallback_cli": false,
    "cli_reason": null
  },
  "prompt": {
    "path": "prompts/generated/characters/ava-reference-v1.md",
    "use_case": "stylized-concept",
    "asset_type": "pixel-art character reference sheet",
    "text": "Final prompt text may be duplicated here for auditability.",
    "input_images": [
      {
        "label": "Image 1",
        "role": "approved dashboard-world reference",
        "path": "ref/design-book-9.png",
        "notes": "Approved mood, palette, and composition reference."
      }
    ]
  },
  "files": {
    "codex_generated_path": "$CODEX_HOME/generated_images/example.png",
    "workspace_source_path": "assets/source/gpt-images-2/characters/ava-reference-v1.png",
    "processed_path": null,
    "atlas_image_path": null,
    "atlas_metadata_path": null,
    "validation_report_path": null
  },
  "source_asset": {
    "dimensions": [1024, 1024],
    "format": "png",
    "has_alpha": false,
    "intended_scale": "reference",
    "source_kind": "generated-reference"
  },
  "asset_contract": {
    "focal_role": "character identity",
    "layer": null,
    "anchor": null,
    "hit_area": null,
    "screen_regions": [],
    "text_policy": "no runtime-critical text baked into the image"
  },
  "postprocess": {
    "steps": [],
    "palette": null,
    "quantized_path": null,
    "crop": null,
    "slice": null,
    "nine_slice": null,
    "atlas": null,
    "background_removal": null
  },
  "validation": {
    "subject_correct": true,
    "style_match": true,
    "text_accuracy": "no generated runtime text used",
    "alpha_valid": null,
    "transparent_corners": null,
    "visible_key_fringe": null,
    "palette_fit": "reference only",
    "scale_check": "not promoted to runtime",
    "sprite_bounds_valid": null,
    "atlas_metadata_valid": null,
    "runtime_text_safe": true,
    "approved_by": "codex",
    "notes": "Readable silhouette and strong accessory separation.",
    "rejection_notes": null
  },
  "runtime_use": {
    "kind": "reference only",
    "consumer": null,
    "layer": null,
    "asset_id": null,
    "notes": "Do not load directly at runtime."
  },
  "notes": []
}
```

## Post-processing scripts

The expected tool surface is:

- `tools/remove_chroma_and_validate.py` for cutout removal and alpha checks.
- `tools/quantize.py` for palette normalization.
- `tools/crop_transparent.py` for transparent bounds.
- `tools/slice_sheet.py` for validated reference-sheet slicing.
- `tools/crop_nineslice.py` for guided ornament extraction.
- `tools/pack_sprites.py` for atlas generation.
- `tools/build_lightmask.py` for deterministic lamp and screen-glow masks.
- `tools/check_manifests.py` for manifest schema checks.
- `tools/check_assets.py` for combined asset validation.

Scripts must be deterministic, emit clear failures, and avoid hiding outputs in
paths that manifests cannot trace.

`tools/check_manifests.py` validates the canonical classification fields and
the manifest fields added by this specification, including `bucket`,
`intent_class`, `asset_contract`, `files.validation_report_path`, and
`postprocess.nine_slice`. `tools/check_assets.py` runs the manifest checks and
is the extension point for future alpha, palette, atlas, and scale validation.

## Promotion gates

Bucket 2 assets may become `approved-runtime` only when:

- the prompt exists under `prompts/generated/`;
- the accepted source image exists under `assets/source/`;
- the manifest records prompt, source, tool, bucket, intent, and validation;
- post-processing commands and settings are recorded;
- alpha, crop, slice, palette, scale, and atlas checks pass where relevant;
- runtime text safety is explicitly true;
- processed paths and atlas metadata exist;
- the consuming runtime layer and asset ID are named.

Bucket 3 assets use deterministic gates rather than image-generation manifests.
Deterministic processing of generated-image sources does not move the output to
Bucket 3; chroma-key removal, quantized runtime images, slices, and other
processed outputs remain Bucket 2 assets until their source manifest records
the full post-processing and promotion evidence.

If a Bucket 3 asset is image-backed without a generated-image source, such as a
script-built atlas or light mask, it still needs a manifest for path, schema,
palette, dimensions, and runtime use.

## Runtime contract

Rust loads approved runtime assets from processed files, atlases, and
manifest-derived metadata. It does not load from Codex generated-image paths,
unprocessed image-generation output, or design-book reference pages.

The renderer owns layout, text, panels, charts, meters, status pills, focus
rings, hit boxes, debug overlays, and lighting composition. Generated source
images provide visual richness and source material only after validation.
