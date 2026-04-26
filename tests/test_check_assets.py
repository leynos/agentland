"""Tests for deterministic asset metadata validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import check_assets
from manifest_fixtures import merge_manifest_parts, valid_manifest, write_manifest


def json_lines(output: str) -> list[dict[str, object]]:
    """Return JSON records from mixed command output."""
    return [
        json.loads(line) for line in output.splitlines() if line.startswith("{")
    ]


def test_validate_assets_metadata_accepts_reference_manifest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Verify reference-only manifests pass asset metadata validation."""
    write_manifest(tmp_path, "valid.json", valid_manifest())

    result = check_assets.validate_assets_metadata(["--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 0, "expected reference manifest metadata to pass"
    assert captured.err == "", "expected no asset metadata errors"


def test_validate_assets_metadata_rejects_runtime_manifest_without_runtime_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Verify runtime manifests require a processed or atlas file reference."""
    manifest = merge_manifest_parts(
        valid_manifest(),
        {
            "status": "approved-runtime",
            "intent_class": "runtime-processed",
            "bucket": "generated-source-converted",
            "runtime_use": {"kind": "prop sprite"},
        },
    )
    write_manifest(tmp_path, "runtime-missing-file.json", manifest)

    result = check_assets.validate_assets_metadata(["--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 1, "expected runtime manifest metadata to fail"
    records = json_lines(captured.err)
    assert records == [
        {
            "op": "asset-validation",
            "path": "assets/manifests/runtime-missing-file.json",
            "error_count": 1,
        }
    ], "expected structured asset validation failure"
    assert "runtime assets require processed_path" in captured.err, (
        "expected runtime file requirement error"
    )
