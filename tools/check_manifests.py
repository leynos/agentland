#!/usr/bin/env python3
"""Validate Agentland asset manifest structure.

This module enforces the canonical manifest schema defined in
``docs/asset-spec.md`` and ``assets/manifests/README.md``. It recursively
validates all JSON files under ``assets/manifests/``, checking required
fields, enum values, nested object structures, and optional path existence.

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
from pathlib import Path
from typing import Any

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


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


def manifest_paths(root: Path) -> list[Path]:
    """Return manifest JSON files below the repository manifest directory."""
    manifest_root = root / "assets" / "manifests"
    if not manifest_root.exists():
        return []
    return sorted(manifest_root.rglob("*.json"))


def require_mapping(value: Any, field: str, errors: list[str]) -> bool:
    """Check that a value is an object before nested validation."""
    if isinstance(value, dict):
        return True
    errors.append(f"{field} must be an object")
    return False


def require_keys(
    value: dict[str, Any], required: set[str], field: str, errors: list[str]
) -> None:
    """Append errors for missing required keys."""
    missing = sorted(required.difference(value))
    errors.extend(f"{field}.{key} is required" for key in missing)


def validate_enum(
    value: Any, allowed: set[str], field: str, errors: list[str]
) -> None:
    """Validate a string enum value."""
    if not isinstance(value, str):
        errors.append(f"{field} must be a string")
        return
    if value not in allowed:
        expected = ", ".join(sorted(allowed))
        errors.append(f"{field} has invalid value {value!r}; expected {expected}")


def validate_optional_path(
    root: Path, value: Any, field: str, errors: list[str]
) -> None:
    """Validate an optional repository-relative path field."""
    if value is None:
        return
    if not isinstance(value, str):
        errors.append(f"{field} must be a string or null")
        return
    if value.startswith("$CODEX_HOME/"):
        return
    if not (root / value).exists():
        errors.append(f"{field} points to missing path {value!r}")


def validate_top_level_fields(data: dict[str, Any], errors: list[str]) -> None:
    """Validate required top-level fields and their enum values."""
    require_keys(data, REQUIRED_TOP_LEVEL, "manifest", errors)
    validate_enum(data.get("family"), ALLOWED_FAMILIES, "family", errors)
    validate_enum(data.get("status"), ALLOWED_STATUSES, "status", errors)
    validate_enum(data.get("bucket"), ALLOWED_BUCKETS, "bucket", errors)
    validate_enum(
        data.get("intent_class"), ALLOWED_INTENT_CLASSES, "intent_class", errors
    )


def validate_files(root: Path, data: dict[str, Any], errors: list[str]) -> None:
    """Validate manifest file path fields."""
    files = data.get("files")
    if require_mapping(files, "files", errors):
        require_keys(files, REQUIRED_FILES, "files", errors)
        for field in sorted(REQUIRED_FILES):
            validate_optional_path(root, files.get(field), f"files.{field}", errors)


def validate_required_section(
    data: dict[str, Any], field: str, required: set[str], errors: list[str]
) -> None:
    """Validate a required manifest object section by key set."""
    section = data.get(field)
    if require_mapping(section, field, errors):
        require_keys(section, required, field, errors)


def validate_manifest_fields(
    root: Path, data: dict[str, Any], errors: list[str]
) -> None:
    """Validate a parsed manifest object."""
    validate_top_level_fields(data, errors)
    validate_files(root, data, errors)
    validate_required_section(
        data, "asset_contract", REQUIRED_ASSET_CONTRACT, errors
    )
    validate_required_section(data, "postprocess", REQUIRED_POSTPROCESS, errors)
    validate_required_section(data, "validation", REQUIRED_VALIDATION, errors)

    if not isinstance(data.get("notes"), list):
        errors.append("notes must be an array")


def validate_manifest(root: Path, path: Path) -> list[str]:
    """Validate one manifest and return human-readable errors."""
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"invalid JSON: {error}"]

    if not require_mapping(data, "manifest", errors):
        return errors

    validate_manifest_fields(root, data, errors)
    return errors


def main() -> int:
    """Run manifest validation."""
    args = parse_args()
    root = args.root.resolve()
    paths = manifest_paths(root)
    failures = 0

    for path in paths:
        errors = validate_manifest(root, path)
        if errors:
            failures += 1
            rel_path = path.relative_to(root)
            for error in errors:
                print(f"{rel_path}: {error}", file=sys.stderr)

    if failures:
        print(f"Manifest validation failed for {failures} file(s).", file=sys.stderr)
        return 1

    print(f"Validated {len(paths)} manifest file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
