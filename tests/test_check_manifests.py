"""Tests for the asset manifest validation script."""

from __future__ import annotations

import io
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

import check_manifests
from manifest_fixtures import (
    merge_manifest_parts,
    valid_manifest,
    write_manifest,
)


def rendered(error: check_manifests.ValidationError) -> str:
    """Render an error without a manifest path for compact assertions."""
    if error.message.startswith(error.field):
        return error.message
    return f"{error.field} {error.message}"


def rendered_errors(errors: list[check_manifests.ValidationError]) -> list[str]:
    """Render validation errors without path prefixes."""
    return [rendered(error) for error in errors]


def json_lines(output: str) -> list[dict[str, Any]]:
    """Return JSON records from mixed human-readable command output."""
    return [
        json.loads(line) for line in output.splitlines() if line.startswith("{")
    ]


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
    errors: list[check_manifests.ValidationError] = []

    check_manifests.validate_enum(value, {"one", "two"}, "bucket", errors)

    assert rendered_errors(errors) == expected


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
    errors: list[check_manifests.ValidationError] = []

    result = check_manifests.require_mapping(value, "manifest", errors)

    assert result is expected_result, "expected mapping validation result"
    assert rendered_errors(errors) == expected_errors, "expected mapping errors"


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
    errors: list[check_manifests.ValidationError] = []

    check_manifests.require_keys(value, required, "manifest", errors)

    assert rendered_errors(errors) == expected_errors, (
        "expected missing key errors"
    )


@pytest.mark.parametrize(
    ("value", "field", "expected_error"),
    [
        (None, "files.workspace_source_path", None),
        (
            "$CODEX_HOME/generated_images/example.png",
            "files.codex_generated_path",
            None,
        ),
        (
            "$CODEX_HOME/generated_images/example.png",
            "files.workspace_source_path",
            "points to missing path",
        ),
        (
            "missing.png",
            "files.workspace_source_path",
            "points to missing path",
        ),
        (123, "files.workspace_source_path", "must be a string or null"),
    ],
)
def test_validate_optional_path_variants(
    tmp_path: Path, value: Any, field: str, expected_error: str | None
) -> None:
    errors: list[check_manifests.ValidationError] = []

    check_manifests.validate_optional_path(tmp_path, value, field, errors)

    if expected_error is None:
        assert errors == [], "expected no optional path errors"
    else:
        assert len(errors) == 1, "expected one optional path error"
        assert expected_error in rendered(errors[0]), (
            f"expected error contains {expected_error!r}"
        )


def test_validate_optional_path_existing_file(tmp_path: Path) -> None:
    asset_path = tmp_path / "assets" / "source.png"
    asset_path.parent.mkdir(parents=True)
    asset_path.write_text("image placeholder", encoding="utf-8")
    errors: list[check_manifests.ValidationError] = []

    check_manifests.validate_optional_path(
        tmp_path, "assets/source.png", "files.workspace_source_path", errors
    )

    assert errors == [], "expected existing file path to validate"


@pytest.mark.parametrize(
    ("value", "expected_error"),
    [
        ("/tmp/source.png", "must be repository-relative"),
        ("../source.png", "escapes repository root"),
    ],
)
def test_validate_optional_path_rejects_root_escape(
    tmp_path: Path, value: str, expected_error: str
) -> None:
    errors: list[check_manifests.ValidationError] = []

    check_manifests.validate_optional_path(
        tmp_path, value, "files.workspace_source_path", errors
    )

    assert len(errors) == 1, "expected one root escape error"
    assert expected_error in rendered(errors[0]), (
        f"expected error contains {expected_error!r}"
    )


def test_validate_manifest_fields_accepts_minimal_valid_manifest(
    tmp_path: Path,
) -> None:
    errors: list[check_manifests.ValidationError] = []

    check_manifests.validate_manifest_fields(tmp_path, valid_manifest(), errors)

    assert errors == []


def test_validate_manifest_accepts_valid_json(tmp_path: Path) -> None:
    manifest_path = write_manifest(tmp_path, "valid.json", valid_manifest())

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert errors == []


def test_validate_manifest_returns_error_for_malformed_json(
    tmp_path: Path,
) -> None:
    manifest_path = tmp_path / "assets" / "manifests" / "malformed.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text("{", encoding="utf-8")

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert len(errors) == 1
    assert errors[0].field == "manifest"
    assert errors[0].message.startswith("invalid JSON:")


def test_load_manifest_returns_data_for_valid_json(tmp_path: Path) -> None:
    manifest_path = write_manifest(tmp_path, "valid.json", valid_manifest())

    data, errors = check_manifests.load_manifest(manifest_path)

    assert data == valid_manifest()
    assert errors == []


def test_load_manifest_returns_error_for_unreadable_file(
    tmp_path: Path,
) -> None:
    manifest_path = tmp_path / "assets" / "manifests" / "missing.json"

    data, errors = check_manifests.load_manifest(manifest_path)

    assert data is None
    assert len(errors) == 1
    assert errors[0].field == "manifest"
    assert errors[0].message.startswith("cannot read file:")


def test_validate_manifest_reports_missing_top_level_field(
    tmp_path: Path,
) -> None:
    manifest = valid_manifest()
    del manifest["bucket"]
    manifest_path = write_manifest(tmp_path, "missing-bucket.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert "manifest.bucket is required" in rendered_errors(errors)


def test_validate_manifest_reports_invalid_bucket(tmp_path: Path) -> None:
    manifest = merge_manifest_parts(
        valid_manifest(), {"bucket": "not-a-bucket"}
    )
    manifest_path = write_manifest(tmp_path, "invalid-bucket.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert any("not-a-bucket" in rendered(error) for error in errors)


def test_validate_manifest_reports_files_mapping_error(tmp_path: Path) -> None:
    manifest = merge_manifest_parts(valid_manifest(), {"files": []})
    manifest_path = write_manifest(tmp_path, "bad-files.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert "files must be an object" in rendered_errors(errors)


def test_validate_manifest_reports_notes_array_error(tmp_path: Path) -> None:
    manifest = merge_manifest_parts(valid_manifest(), {"notes": "not a list"})
    manifest_path = write_manifest(tmp_path, "bad-notes.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert "notes must be an array" in rendered_errors(errors)


def test_render_errors_writes_path_prefixed_messages() -> None:
    output = io.StringIO()

    check_manifests.render_errors(
        Path("assets/manifests/invalid.json"),
        [check_manifests.ValidationError("bucket", "must be a string")],
        output,
    )

    assert output.getvalue() == (
        "assets/manifests/invalid.json: bucket must be a string\n"
    )


@pytest.mark.parametrize(
    ("initial_setup", "expected_manifests_found", "description"),
    [
        (lambda _tmp_path: None, 0, "zero manifests"),
        (
            lambda tmp_path: write_manifest(
                tmp_path, "valid.json", valid_manifest()
            ),
            1,
            "one valid manifest",
        ),
    ],
)
def test_main_returns_zero_for_valid_manifest_directories(
    initial_setup: Callable[[Path], object],
    expected_manifests_found: int,
    description: str,
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    initial_setup(tmp_path)

    result = check_manifests.main(["--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 0, f"expected success for {description}"
    assert captured.err == "", f"expected no stderr for {description}"
    records = json_lines(captured.out)
    assert records[0] == {
        "op": "manifest-validation",
        "manifests_found": expected_manifests_found,
    }, f"expected manifest count {expected_manifests_found}"
    assert records[1]["op"] == "manifest-validation", (
        "expected elapsed-time manifest validation record"
    )
    assert isinstance(records[1]["elapsed_ms"], float), (
        "expected elapsed time in milliseconds"
    )
    assert (
        f"Validated {expected_manifests_found} manifest file(s)."
        in captured.out
    ), f"expected validated summary for {description}"


def test_main_reports_invalid_manifest_path_and_error(
    tmp_path: Path,
) -> None:
    manifest = merge_manifest_parts(valid_manifest(), {"bucket": "bad-bucket"})
    write_manifest(tmp_path, "invalid.json", manifest)
    output = io.StringIO()

    result = check_manifests.main(["--root", str(tmp_path)], output)

    assert result == 1, "expected invalid manifest to fail"
    records = json_lines(output.getvalue())
    assert records == [
        {
            "op": "manifest-validation",
            "path": "assets/manifests/invalid.json",
            "error_count": 1,
        }
    ], "expected structured invalid manifest failure record"
    assert (
        "assets/manifests/invalid.json: bucket has invalid value 'bad-bucket'"
        in output.getvalue()
    ), "expected invalid bucket error output"
    assert "Manifest validation failed for 1 file(s)." in output.getvalue(), (
        "expected failure summary"
    )


def test_main_writes_errors_to_injected_output(tmp_path: Path) -> None:
    manifest = merge_manifest_parts(valid_manifest(), {"files": []})
    write_manifest(tmp_path, "invalid.json", manifest)
    output_path = tmp_path / "stderr.txt"

    with output_path.open("w", encoding="utf-8") as output:
        result = check_manifests.main(["--root", str(tmp_path)], output)

    assert result == 1, "expected injected-output validation failure"
    assert (
        "assets/manifests/invalid.json: files must be an object"
        in output_path.read_text(encoding="utf-8")
    ), "expected files mapping error in injected output"
