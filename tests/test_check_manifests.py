"""Tests for the asset manifest validation script."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

import check_manifests


def valid_manifest(source_path: str | None = None) -> dict[str, Any]:
    """Return a minimal manifest that satisfies the required schema."""
    return {
        "id": "ava_reference_sheet_v1",
        "family": "character-reference",
        "status": "approved-source",
        "bucket": "direct-generated-reference",
        "intent_class": "reference-only",
        "tool": {
            "mode": "codex_builtin_image_gen",
            "model_family": "gpt-images-2",
            "fallback_cli": False,
            "cli_reason": None,
        },
        "prompt": {
            "path": "prompts/generated/characters/ava-reference-v1.md",
            "use_case": "stylized-concept",
            "asset_type": "pixel-art character reference sheet",
            "text": "Generate a reference sheet.",
            "input_images": [],
        },
        "files": {
            "codex_generated_path": "$CODEX_HOME/generated_images/example.png",
            "workspace_source_path": source_path,
            "processed_path": None,
            "atlas_image_path": None,
            "atlas_metadata_path": None,
            "validation_report_path": None,
        },
        "source_asset": {
            "dimensions": [1024, 1024],
            "format": "png",
            "has_alpha": False,
            "intended_scale": "reference",
            "source_kind": "generated-reference",
        },
        "asset_contract": {
            "focal_role": "character identity",
            "layer": None,
            "anchor": None,
            "hit_area": None,
            "screen_regions": [],
            "text_policy": "no runtime-critical text baked into the image",
        },
        "postprocess": {
            "steps": [],
            "palette": None,
            "quantized_path": None,
            "crop": None,
            "slice": None,
            "nine_slice": None,
            "atlas": None,
            "background_removal": None,
        },
        "validation": {
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
        },
        "runtime_use": {
            "kind": "reference only",
            "consumer": None,
            "layer": None,
            "asset_id": None,
            "notes": "Do not load directly at runtime.",
        },
        "notes": [],
    }


def write_manifest(root: Path, name: str, manifest: dict[str, Any]) -> Path:
    """Write a manifest under the repository-style manifest directory."""
    manifest_path = root / "assets" / "manifests" / name
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("one", []),
        (
            "three",
            ["bucket has invalid value 'three'; expected one, two"],
        ),
        (7, ["bucket must be a string"]),
    ],
)
def test_validate_enum(value: Any, expected: list[str]) -> None:
    errors: list[str] = []

    check_manifests.validate_enum(value, {"one", "two"}, "bucket", errors)

    assert errors == expected


@pytest.mark.parametrize(
    ("value", "expected_result", "expected_errors"),
    [
        ({}, True, []),
        ([], False, ["manifest must be an object"]),
    ],
)
def test_require_mapping(
    value: Any, expected_result: bool, expected_errors: list[str]
) -> None:
    errors: list[str] = []

    result = check_manifests.require_mapping(value, "manifest", errors)

    assert result is expected_result
    assert errors == expected_errors


@pytest.mark.parametrize(
    ("value", "required", "expected_errors"),
    [
        ({"a": 1, "b": 2}, {"a", "b"}, []),
        ({"a": 1}, {"a", "b"}, ["manifest.b is required"]),
        (
            {"a": 1},
            {"a", "b", "c"},
            ["manifest.b is required", "manifest.c is required"],
        ),
    ],
)
def test_require_keys(
    value: dict[str, Any], required: set[str], expected_errors: list[str]
) -> None:
    errors: list[str] = []

    check_manifests.require_keys(value, required, "manifest", errors)

    assert errors == expected_errors


@pytest.mark.parametrize(
    ("value", "field", "expected_error"),
    [
        (None, "files.workspace_source_path", None),
        (
            "$CODEX_HOME/generated_images/example.png",
            "files.codex_generated_path",
            None,
        ),
        ("missing.png", "files.workspace_source_path", "points to missing path"),
        (123, "files.workspace_source_path", "must be a string or null"),
    ],
)
def test_validate_optional_path_variants(
    tmp_path: Path, value: Any, field: str, expected_error: str | None
) -> None:
    errors: list[str] = []

    check_manifests.validate_optional_path(tmp_path, value, field, errors)

    if expected_error is None:
        assert errors == []
    else:
        assert len(errors) == 1
        assert expected_error in errors[0]


def test_validate_optional_path_existing_file(tmp_path: Path) -> None:
    asset_path = tmp_path / "assets" / "source.png"
    asset_path.parent.mkdir(parents=True)
    asset_path.write_text("image placeholder", encoding="utf-8")
    errors: list[str] = []

    check_manifests.validate_optional_path(
        tmp_path, "assets/source.png", "files.workspace_source_path", errors
    )

    assert errors == []


def test_validate_manifest_fields_accepts_minimal_valid_manifest(tmp_path: Path) -> None:
    errors: list[str] = []

    check_manifests.validate_manifest_fields(tmp_path, valid_manifest(), errors)

    assert errors == []


def test_validate_manifest_accepts_valid_json(tmp_path: Path) -> None:
    manifest_path = write_manifest(tmp_path, "valid.json", valid_manifest())

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert errors == []


def test_validate_manifest_returns_error_for_malformed_json(tmp_path: Path) -> None:
    manifest_path = tmp_path / "assets" / "manifests" / "malformed.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text("{", encoding="utf-8")

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert len(errors) == 1
    assert errors[0].startswith("invalid JSON:")


def test_validate_manifest_reports_missing_top_level_field(tmp_path: Path) -> None:
    manifest = valid_manifest()
    del manifest["bucket"]
    manifest_path = write_manifest(tmp_path, "missing-bucket.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert "manifest.bucket is required" in errors


def test_validate_manifest_reports_invalid_bucket(tmp_path: Path) -> None:
    manifest = valid_manifest()
    manifest["bucket"] = "not-a-bucket"
    manifest_path = write_manifest(tmp_path, "invalid-bucket.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert any("not-a-bucket" in error for error in errors)


def test_validate_manifest_reports_files_mapping_error(tmp_path: Path) -> None:
    manifest = valid_manifest()
    manifest["files"] = []
    manifest_path = write_manifest(tmp_path, "bad-files.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert "files must be an object" in errors


def test_validate_manifest_reports_notes_array_error(tmp_path: Path) -> None:
    manifest = valid_manifest()
    manifest["notes"] = "not a list"
    manifest_path = write_manifest(tmp_path, "bad-notes.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert "notes must be an array" in errors


def test_main_returns_zero_for_directory_with_zero_manifests(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["check_manifests.py", "--root", str(tmp_path)])

    result = check_manifests.main()
    captured = capsys.readouterr()

    assert result == 0
    assert captured.err == ""
    assert captured.out == "Validated 0 manifest file(s).\n"


def test_main_returns_zero_for_directory_with_one_valid_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    write_manifest(tmp_path, "valid.json", valid_manifest())
    monkeypatch.setattr(sys, "argv", ["check_manifests.py", "--root", str(tmp_path)])

    result = check_manifests.main()
    captured = capsys.readouterr()

    assert result == 0
    assert captured.err == ""
    assert captured.out == "Validated 1 manifest file(s).\n"


def test_main_reports_invalid_manifest_path_and_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    manifest = valid_manifest()
    manifest["bucket"] = "bad-bucket"
    write_manifest(tmp_path, "invalid.json", manifest)
    monkeypatch.setattr(sys, "argv", ["check_manifests.py", "--root", str(tmp_path)])

    result = check_manifests.main()
    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == ""
    assert (
        "assets/manifests/invalid.json: bucket has invalid value 'bad-bucket'"
        in captured.err
    )
    assert "Manifest validation failed for 1 file(s)." in captured.err
