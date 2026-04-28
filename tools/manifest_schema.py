"""Canonical schema values for Agentland asset manifests."""

from typing import Final

ALLOWED_BUCKETS: Final[frozenset[str]] = frozenset({
    "direct-generated-reference",
    "generated-source-converted",
    "algorithmic",
})

ALLOWED_INTENT_CLASSES: Final[frozenset[str]] = frozenset({
    "reference-only",
    "sliceable-source",
    "ornament-source",
    "runtime-processed",
    "lightmask-source",
    "layout-reference",
})

ALLOWED_FAMILIES: Final[frozenset[str]] = frozenset({
    "style-guide",
    "character-reference",
    "animation-reference",
    "environment-reference",
    "prop-cutout",
    "ui-ornament-reference",
    "texture-reference",
    "atlas",
    "lightmask",
})

ALLOWED_STATUSES: Final[frozenset[str]] = frozenset({
    "approved-source",
    "approved-runtime",
    "reference-only",
    "rejected",
    "superseded",
})

REQUIRED_TOP_LEVEL: Final[frozenset[str]] = frozenset({
    "id",
    "family",
    "status",
    "bucket",
    "intent_class",
    "tool",
    "prompt",
    "files",
    "source_asset",
    "asset_contract",
    "postprocess",
    "validation",
    "runtime_use",
    "notes",
})

REQUIRED_FILES: Final[frozenset[str]] = frozenset({
    "codex_generated_path",
    "workspace_source_path",
    "processed_path",
    "atlas_image_path",
    "atlas_metadata_path",
    "validation_report_path",
})

REQUIRED_TOOL: Final[frozenset[str]] = frozenset({
    "mode",
    "model_family",
    "fallback_cli",
    "cli_reason",
})

REQUIRED_PROMPT: Final[frozenset[str]] = frozenset({
    "path",
    "use_case",
    "asset_type",
    "text",
    "input_images",
})

REQUIRED_SOURCE_ASSET: Final[frozenset[str]] = frozenset({
    "dimensions",
    "format",
    "has_alpha",
    "intended_scale",
    "source_kind",
})

REQUIRED_ASSET_CONTRACT: Final[frozenset[str]] = frozenset({
    "focal_role",
    "layer",
    "anchor",
    "hit_area",
    "screen_regions",
    "text_policy",
})

REQUIRED_POSTPROCESS: Final[frozenset[str]] = frozenset({
    "steps",
    "palette",
    "quantized_path",
    "crop",
    "slice",
    "nine_slice",
    "atlas",
    "background_removal",
})

REQUIRED_VALIDATION: Final[frozenset[str]] = frozenset({
    "subject_correct",
    "style_match",
    "text_accuracy",
    "alpha_valid",
    "transparent_corners",
    "visible_key_fringe",
    "palette_fit",
    "scale_check",
    "sprite_bounds_valid",
    "atlas_metadata_valid",
    "runtime_text_safe",
    "approved_by",
    "notes",
    "rejection_notes",
})

REQUIRED_RUNTIME_USE: Final[frozenset[str]] = frozenset({
    "kind",
    "consumer",
    "layer",
    "asset_id",
    "notes",
})
