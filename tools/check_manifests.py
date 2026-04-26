#!/usr/bin/env python3
"""Validate Agentland asset manifest structure.

This module enforces the canonical manifest schema defined in
``docs/asset-spec.md`` and ``assets/manifests/README.md``. It recursively
validates all JSON files under ``assets/manifests/``, checking required
fields, enum values, nested object structures, and optional path existence.
Validation functions return ``ValidationError`` values so domain validation stays
separate from command-line rendering.

Usage
-----
Run directly or via the Makefile target::

    python tools/check_manifests.py --root /path/to/repo
    make manifest-check

Exit code is non-zero if any manifest fails validation.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

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


@dataclass(frozen=True)
class ValidationError:
    """A manifest validation failure for one logical field."""

    field: str
    message: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate JSON manifests under assets/manifests."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current working directory.",
    )
    return parser.parse_args(argv)


def manifest_paths(root: Path) -> list[Path]:
    """Return manifest JSON files below the repository manifest directory."""
    manifest_root = root / "assets" / "manifests"
    if not manifest_root.exists():
        return []
    return sorted(manifest_root.rglob("*.json"))


def require_mapping(value: Any, field: str, errors: list[ValidationError]) -> bool:
    """Check that a value is an object before nested validation."""
    if isinstance(value, dict):
        return True
    errors.append(ValidationError(field, "must be an object"))
    return False


def require_keys(
    value: dict[str, Any],
    required: set[str],
    field: str,
    errors: list[ValidationError],
) -> None:
    """Append errors for missing required keys."""
    missing = sorted(required.difference(value))
    errors.extend(ValidationError(f"{field}.{key}", "is required") for key in missing)


def validate_enum(
    value: Any, allowed: set[str], field: str, errors: list[ValidationError]
) -> None:
    """Validate a string enum value."""
    if not isinstance(value, str):
        errors.append(ValidationError(field, "must be a string"))
        return
    if value not in allowed:
        expected = ", ".join(sorted(allowed))
        errors.append(
            ValidationError(
                field,
                f"{field} has invalid value {value!r}; expected {expected}",
            )
        )


def validate_optional_path(
    root: Path, value: Any, field: str, errors: list[ValidationError]
) -> None:
    """Validate an optional repository-relative path field."""
    if value is None:
        return
    if not isinstance(value, str):
        errors.append(ValidationError(field, "must be a string or null"))
        return
    if value.startswith("$CODEX_HOME/") and field == "files.codex_generated_path":
        return
    if not (root / value).exists():
        errors.append(ValidationError(field, f"points to missing path {value!r}"))


def validate_top_level_fields(
    data: dict[str, Any], errors: list[ValidationError]
) -> None:
    """Validate required top-level fields and their enum values."""
    require_keys(data, REQUIRED_TOP_LEVEL, "manifest", errors)
    validate_enum(data.get("family"), ALLOWED_FAMILIES, "family", errors)
    validate_enum(data.get("status"), ALLOWED_STATUSES, "status", errors)
    validate_enum(data.get("bucket"), ALLOWED_BUCKETS, "bucket", errors)
    validate_enum(
        data.get("intent_class"), ALLOWED_INTENT_CLASSES, "intent_class", errors
    )


def validate_files(
    root: Path, data: dict[str, Any], errors: list[ValidationError]
) -> None:
    """Validate manifest file path fields."""
    files = data.get("files")
    if require_mapping(files, "files", errors):
        require_keys(files, REQUIRED_FILES, "files", errors)
        for field in sorted(REQUIRED_FILES):
            validate_optional_path(root, files.get(field), f"files.{field}", errors)


def validate_required_section(
    data: dict[str, Any],
    field: str,
    required: set[str],
    errors: list[ValidationError],
) -> None:
    """Validate a required manifest object section by key set."""
    section = data.get(field)
    if require_mapping(section, field, errors):
        require_keys(section, required, field, errors)


def validate_manifest_fields(
    root: Path, data: dict[str, Any], errors: list[ValidationError]
) -> None:
    """Validate a parsed manifest object."""
    validate_top_level_fields(data, errors)
    validate_required_section(data, "tool", REQUIRED_TOOL, errors)
    validate_required_section(data, "prompt", REQUIRED_PROMPT, errors)
    validate_files(root, data, errors)
    validate_required_section(data, "source_asset", REQUIRED_SOURCE_ASSET, errors)
    validate_required_section(
        data, "asset_contract", REQUIRED_ASSET_CONTRACT, errors
    )
    validate_required_section(data, "postprocess", REQUIRED_POSTPROCESS, errors)
    validate_required_section(data, "validation", REQUIRED_VALIDATION, errors)
    validate_required_section(data, "runtime_use", REQUIRED_RUNTIME_USE, errors)

    if not isinstance(data.get("notes"), list):
        errors.append(ValidationError("notes", "must be an array"))


def load_manifest(path: Path) -> tuple[dict[str, Any] | None, list[ValidationError]]:
    """Read and parse one manifest file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        return None, [ValidationError("manifest", f"invalid JSON: {error}")]

    if not isinstance(data, dict):
        return None, [ValidationError("manifest", "must be an object")]

    return data, []


def validate_manifest(root: Path, path: Path) -> list[ValidationError]:
    """Validate one manifest and return domain validation errors."""
    data, errors = load_manifest(path)
    if errors:
        return errors
    if data is None:
        return [ValidationError("manifest", "must be an object")]

    if not require_mapping(data, "manifest", errors):
        return errors

    validate_manifest_fields(root, data, errors)
    return errors


def render_errors(
    rel_path: Path, errors: list[ValidationError], output: TextIO
) -> None:
    """Write rendered validation errors for one manifest."""
    for error in errors:
        if error.message.startswith(error.field):
            message = error.message
        else:
            message = f"{error.field} {error.message}"
        print(f"{rel_path}: {message}", file=output)


def main(argv: list[str] | None = None, output: TextIO = sys.stderr) -> int:
    """Run manifest validation."""
    args = parse_args(argv)
    root = args.root.resolve()
    paths = manifest_paths(root)
    failures = 0

    for path in paths:
        errors = validate_manifest(root, path)
        if errors:
            failures += 1
            rel_path = path.relative_to(root)
            render_errors(rel_path, errors, output)

    if failures:
        print(f"Manifest validation failed for {failures} file(s).", file=output)
        return 1

    print(f"Validated {len(paths)} manifest file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
