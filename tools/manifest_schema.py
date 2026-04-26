"""Canonical schema values for Agentland asset manifests."""

ALLOWED_BUCKETS = {
    "direct-generated-reference",
    "generated-source-converted",
    "algorithmic",
}

ALLOWED_INTENT_CLASSES = {
    "reference-only",
    "sliceable-source",
    "ornament-source",
    "runtime-processed",
    "lightmask-source",
    "layout-reference",
}

ALLOWED_FAMILIES = {
    "style-guide",
    "character-reference",
    "animation-reference",
    "environment-reference",
    "prop-cutout",
    "ui-ornament-reference",
    "texture-reference",
    "atlas",
    "lightmask",
}

ALLOWED_STATUSES = {
    "approved-source",
    "approved-runtime",
    "reference-only",
    "rejected",
    "superseded",
}

REQUIRED_TOP_LEVEL = {
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
}

REQUIRED_FILES = {
    "codex_generated_path",
    "workspace_source_path",
    "processed_path",
    "atlas_image_path",
    "atlas_metadata_path",
    "validation_report_path",
}

REQUIRED_TOOL = {
    "mode",
    "model_family",
    "fallback_cli",
    "cli_reason",
}

REQUIRED_PROMPT = {
    "path",
    "use_case",
    "asset_type",
    "text",
    "input_images",
}

REQUIRED_SOURCE_ASSET = {
    "dimensions",
    "format",
    "has_alpha",
    "intended_scale",
    "source_kind",
}

REQUIRED_ASSET_CONTRACT = {
    "focal_role",
    "layer",
    "anchor",
    "hit_area",
    "screen_regions",
    "text_policy",
}

REQUIRED_POSTPROCESS = {
    "steps",
    "palette",
    "quantized_path",
    "crop",
    "slice",
    "nine_slice",
    "atlas",
    "background_removal",
}

REQUIRED_VALIDATION = {
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
}

REQUIRED_RUNTIME_USE = {
    "kind",
    "consumer",
    "layer",
    "asset_id",
    "notes",
}
