# Asset specification

## Scope

This document defines where Agentland stores generated sources, processed
runtime assets, manifests, palettes, and asset requests. It also defines the
manifest contract used before any generated image becomes part of the product.

## Assumptions

- No final art is generated in the bootstrap slice.
- Codex built-in `image_gen` is the default raster image authoring path.
- PixelLab MCP is not configured or used.
- CLI image generation is used only after explicit user request or explicit
  native-transparency fallback confirmation.
- Runtime assets must support a fixed `512x288` virtual framebuffer and crisp
  integer scaling.

## Repository layout

Use this layout as assets are introduced:

```text
prompts/
├─ generated/
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
└─ requests/
```

Create directories when a change needs them. Empty architecture should not be
added only for appearance.

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
        "role": "style reference",
        "path": "assets/source/references/approved-dashboard.png",
        "notes": "Approved mood and composition reference."
      }
    ]
  },
  "files": {
    "codex_generated_path": "$CODEX_HOME/generated_images/example.png",
    "workspace_source_path": "assets/source/gpt-images-2/characters/ava-reference-v1.png",
    "processed_path": null,
    "atlas_image_path": null,
    "atlas_metadata_path": null
  },
  "source_asset": {
    "dimensions": [1024, 1024],
    "format": "png",
    "has_alpha": false,
    "intended_scale": "reference",
    "source_kind": "generated-reference"
  },
  "postprocess": {
    "steps": [],
    "palette": null,
    "quantized_path": null,
    "crop": null,
    "slice": null,
    "atlas": null,
    "background_removal": null
  },
  "validation": {
    "subject_correct": true,
    "style_match": true,
    "text_accuracy": "no generated text used",
    "alpha_valid": null,
    "transparent_corners": null,
    "visible_key_fringe": null,
    "palette_fit": "reference only",
    "scale_check": "not promoted to runtime",
    "sprite_bounds_valid": null,
    "atlas_metadata_valid": null,
    "runtime_text_safe": true,
    "approved_by": "codex",
    "notes": "Readable silhouette and strong material separation.",
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

Scripts should be deterministic, emit clear failures, and avoid hiding outputs
in paths that manifests cannot trace.

## Runtime contract

Rust loads approved runtime assets from processed files, atlases, and
manifest-derived metadata. It does not load from Codex generated-image paths or
unprocessed image-generation output.

The renderer owns layout, text, panels, charts, meters, status pills, focus
rings, hit boxes, debug overlays, and lighting composition. Generated source
images provide visual richness and source material only after validation.
