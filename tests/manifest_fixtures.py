"""Fixture builders for manifest checker tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_tool() -> dict[str, Any]:
    """Return the default tool manifest section."""
    return {
        "mode": "codex_builtin_image_gen",
        "model_family": "gpt-images-2",
        "fallback_cli": False,
        "cli_reason": None,
    }


def build_prompt() -> dict[str, Any]:
    """Return the default prompt manifest section."""
    return {
        "path": "prompts/generated/characters/ava-reference-v1.md",
        "use_case": "stylized-concept",
        "asset_type": "pixel-art character reference sheet",
        "text": "Generate a reference sheet.",
        "input_images": [],
    }


def build_files(source_path: str | None = None) -> dict[str, Any]:
    """Return the default files manifest section."""
    return {
        "codex_generated_path": "$CODEX_HOME/generated_images/example.png",
        "workspace_source_path": source_path,
        "processed_path": None,
        "atlas_image_path": None,
        "atlas_metadata_path": None,
        "validation_report_path": None,
    }


def build_source_asset() -> dict[str, Any]:
    """Return the default source asset manifest section."""
    return {
        "dimensions": [1024, 1024],
        "format": "png",
        "has_alpha": False,
        "intended_scale": "reference",
        "source_kind": "generated-reference",
    }


def build_asset_contract() -> dict[str, Any]:
    """Return the default asset contract manifest section."""
    return {
        "focal_role": "character identity",
        "layer": None,
        "anchor": None,
        "hit_area": None,
        "screen_regions": [],
        "text_policy": "no runtime-critical text baked into the image",
    }


def build_postprocess() -> dict[str, Any]:
    """Return the default postprocess manifest section."""
    return {
        "steps": [],
        "palette": None,
        "quantized_path": None,
        "crop": None,
        "slice": None,
        "nine_slice": None,
        "atlas": None,
        "background_removal": None,
    }


def build_validation() -> dict[str, Any]:
    """Return the default validation manifest section."""
    return {
        "subject_correct": True,
        "style_match": True,
        "text_accuracy": "no generated runtime text used",
        "alpha_valid": None,
        "transparent_corners": None,
        "visible_key_fringe": None,
        "palette_fit": "reference only",
        "scale_check": "not promoted to runtime",
        "sprite_bounds_valid": None,
        "atlas_metadata_valid": None,
        "runtime_text_safe": True,
        "approved_by": "codex",
        "notes": "Readable silhouette.",
        "rejection_notes": None,
    }


def build_runtime_use() -> dict[str, Any]:
    """Return the default runtime use manifest section."""
    return {
        "kind": "reference only",
        "consumer": None,
        "layer": None,
        "asset_id": None,
        "notes": "Do not load directly at runtime.",
    }


def merge_manifest_parts(
    base: dict[str, Any], overrides: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Merge top-level manifest sections and optional test overrides."""
    manifest = dict(base)
    if overrides is None:
        return manifest

    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(manifest.get(key), dict):
            manifest[key] = {**manifest[key], **value}
        else:
            manifest[key] = value
    return manifest


def valid_manifest(source_path: str | None = None) -> dict[str, Any]:
    """Return a minimal manifest that satisfies the required schema."""
    return merge_manifest_parts(
        {
            "id": "ava_reference_sheet_v1",
            "family": "character-reference",
            "status": "approved-source",
            "bucket": "direct-generated-reference",
            "intent_class": "reference-only",
            "tool": build_tool(),
            "prompt": build_prompt(),
            "files": build_files(source_path),
            "source_asset": build_source_asset(),
            "asset_contract": build_asset_contract(),
            "postprocess": build_postprocess(),
            "validation": build_validation(),
            "runtime_use": build_runtime_use(),
            "notes": [],
        }
    )


def write_manifest(root: Path, name: str, manifest: dict[str, Any]) -> Path:
    """Write a manifest under the repository-style manifest directory."""
    manifest_path = root / "assets" / "manifests" / name
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path
