"""Tests for the asset manifest validation script."""

from __future__ import annotations

import io
import json
import sys
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
    """Validate enum checks for each input."""
    errors: list[check_manifests.ValidationError] = []

    check_manifests.validate_enum(value, {"one", "two"}, "bucket", errors)

    assert rendered_errors(errors) == expected, "expected enum validation errors"


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
    """Verify require_mapping returns the correct bool and expected errors."""
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
    """Verify require_keys appends the expected missing-key errors."""
    errors: list[check_manifests.ValidationError] = []

    check_manifests.require_keys(value, required, "manifest", errors)

    assert rendered_errors(errors) == expected_errors, (
        "expected missing key errors"
    )


@pytest.mark.parametrize(
    ("argv", "expected_root"),
    [
        ([], Path.cwd()),
        (["--root", "/tmp/repo"], Path("/tmp/repo")),
    ],
)
def test_parse_args_sets_root(
    argv: list[str], expected_root: Path
) -> None:
    """Verify parse_args resolves --root to the expected Path."""
    result = check_manifests.parse_args(argv)

    assert result.root == expected_root, "expected parsed root path"


def test_manifest_paths_discovers_nested_files(tmp_path: Path) -> None:
    """Verify manifest_paths returns JSON files in nested subdirectories."""
    base = tmp_path / "assets" / "manifests"
    (base / "sub").mkdir(parents=True)
    (base / "a.json").write_text("{}", encoding="utf-8")
    (base / "sub" / "b.json").write_text("{}", encoding="utf-8")

    paths = check_manifests.manifest_paths(tmp_path)

    assert sorted(path.name for path in paths) == ["a.json", "b.json"], (
        "expected nested manifest files"
    )


def test_manifest_paths_returns_empty_when_directory_absent(
    tmp_path: Path,
) -> None:
    """Verify manifest_paths returns [] when the directory does not exist."""
    assert check_manifests.manifest_paths(tmp_path) == [], (
        "expected no manifests when directory is absent"
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
    """Validate optional path handling for common value variants."""
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
    """Verify validate_optional_path accepts an existing repository file."""
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
    """Verify validate_optional_path rejects absolute and escaping paths."""
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
    """Verify validate_manifest_fields accepts the minimal valid manifest."""
    errors: list[check_manifests.ValidationError] = []

    check_manifests.validate_manifest_fields(tmp_path, valid_manifest(), errors)

    assert errors == [], "expected minimal valid manifest fields to pass"


def test_validate_manifest_accepts_valid_json(tmp_path: Path) -> None:
    """Verify validate_manifest accepts a valid manifest JSON file."""
    manifest_path = write_manifest(tmp_path, "valid.json", valid_manifest())

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert errors == [], "expected valid manifest JSON to pass"


def test_validate_manifest_returns_error_for_malformed_json(
    tmp_path: Path,
) -> None:
    """Verify validate_manifest reports malformed JSON as a manifest error."""
    manifest_path = tmp_path / "assets" / "manifests" / "malformed.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text("{", encoding="utf-8")

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert len(errors) == 1, "expected one malformed JSON error"
    assert errors[0].field == "manifest", "expected manifest field error"
    assert errors[0].message.startswith("invalid JSON:"), (
        "expected invalid JSON error"
    )


def test_load_manifest_returns_data_for_valid_json(tmp_path: Path) -> None:
    """Verify load_manifest returns parsed data for valid JSON."""
    manifest_path = write_manifest(tmp_path, "valid.json", valid_manifest())

    data, errors = check_manifests.load_manifest(manifest_path)

    assert data == valid_manifest(), "expected parsed manifest data"
    assert errors == [], "expected no load errors"


def test_load_manifest_returns_error_for_unreadable_file(
    tmp_path: Path,
) -> None:
    """Verify load_manifest reports unreadable files distinctly."""
    manifest_path = tmp_path / "assets" / "manifests" / "missing.json"

    data, errors = check_manifests.load_manifest(manifest_path)

    assert data is None, "expected unreadable manifest to return no data"
    assert len(errors) == 1, "expected one unreadable file error"
    assert errors[0].field == "manifest", "expected manifest field error"
    assert errors[0].message.startswith("cannot read file:"), (
        "expected cannot read file error"
    )


def test_validate_manifest_reports_missing_top_level_field(
    tmp_path: Path,
) -> None:
    """Verify validate_manifest reports a missing required top-level field."""
    manifest = valid_manifest()
    del manifest["bucket"]
    manifest_path = write_manifest(tmp_path, "missing-bucket.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert "manifest.bucket is required" in rendered_errors(errors), (
        "expected missing bucket error"
    )


def test_validate_manifest_reports_invalid_bucket(tmp_path: Path) -> None:
    """Verify validate_manifest reports invalid bucket enum values."""
    manifest = merge_manifest_parts(
        valid_manifest(), {"bucket": "not-a-bucket"}
    )
    manifest_path = write_manifest(tmp_path, "invalid-bucket.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert any("not-a-bucket" in rendered(error) for error in errors), (
        "expected invalid bucket value error"
    )


def test_validate_manifest_reports_files_mapping_error(tmp_path: Path) -> None:
    """Verify validate_manifest reports a non-object files section."""
    manifest = merge_manifest_parts(valid_manifest(), {"files": []})
    manifest_path = write_manifest(tmp_path, "bad-files.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert "files must be an object" in rendered_errors(errors), (
        "expected files mapping error"
    )


def test_validate_manifest_reports_notes_array_error(tmp_path: Path) -> None:
    """Verify validate_manifest reports a non-array notes field."""
    manifest = merge_manifest_parts(valid_manifest(), {"notes": "not a list"})
    manifest_path = write_manifest(tmp_path, "bad-notes.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert "notes must be an array" in rendered_errors(errors), (
        "expected notes array error"
    )


SECTION_CASES = [
    ("tool", check_manifests.REQUIRED_TOOL),
    ("prompt", check_manifests.REQUIRED_PROMPT),
    ("source_asset", check_manifests.REQUIRED_SOURCE_ASSET),
    ("asset_contract", check_manifests.REQUIRED_ASSET_CONTRACT),
    ("postprocess", check_manifests.REQUIRED_POSTPROCESS),
    ("validation", check_manifests.REQUIRED_VALIDATION),
    ("runtime_use", check_manifests.REQUIRED_RUNTIME_USE),
]


@pytest.mark.parametrize("section,required_keys", SECTION_CASES)
def test_validate_manifest_reports_missing_section_key(
    tmp_path: Path, section: str, required_keys: set[str]
) -> None:
    """Verify each required section key produces a validation error."""
    key = next(iter(sorted(required_keys)))
    manifest = valid_manifest()
    del manifest[section][key]
    manifest_path = write_manifest(
        tmp_path, f"missing-{section}-{key}.json", manifest
    )

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert any(f"{section}.{key}" in rendered(error) for error in errors), (
        f"expected missing {section}.{key} error"
    )


@pytest.mark.parametrize("section", [section for section, _ in SECTION_CASES])
def test_validate_manifest_reports_section_not_object(
    tmp_path: Path, section: str
) -> None:
    """Verify a non-object section value produces a mapping error."""
    manifest = valid_manifest()
    manifest[section] = "not-an-object"
    manifest_path = write_manifest(tmp_path, f"bad-{section}.json", manifest)

    errors = check_manifests.validate_manifest(tmp_path, manifest_path)

    assert any("must be an object" in rendered(error) for error in errors), (
        f"expected {section} mapping error"
    )


def test_render_errors_writes_path_prefixed_messages() -> None:
    """Verify render_errors writes path-prefixed human-readable messages."""
    output = io.StringIO()

    check_manifests.render_errors(
        Path("assets/manifests/invalid.json"),
        [check_manifests.ValidationError("bucket", "must be a string")],
        output,
    )

    assert output.getvalue() == (
        "assets/manifests/invalid.json: bucket must be a string\n"
    ), "expected path-prefixed rendered error"


@pytest.mark.parametrize(
    ("manifest_count", "expected_out"),
    [
        (0, "Validated 0 manifest file(s).\n"),
        (1, "Validated 1 manifest file(s).\n"),
    ],
)
def test_main_returns_zero_for_valid_manifest_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    manifest_count: int,
    expected_out: str,
) -> None:
    """Verify main succeeds for empty and valid manifest directories."""
    for i in range(manifest_count):
        write_manifest(tmp_path, f"valid-{i}.json", valid_manifest())
    monkeypatch.setattr(
        sys,
        "argv",
        ["check_manifests.py", "--root", str(tmp_path)],
    )

    result = check_manifests.main()
    captured = capsys.readouterr()

    assert result == 0, "expected valid manifest directory to pass"
    assert captured.err == "", "expected no stderr for valid manifest directory"
    records = json_lines(captured.out)
    assert records[0] == {
        "op": "manifest-validation",
        "manifests_found": manifest_count,
    }, f"expected manifest count {manifest_count}"
    assert records[1]["op"] == "manifest-validation", (
        "expected elapsed-time manifest validation record"
    )
    assert isinstance(records[1]["elapsed_ms"], float), (
        "expected elapsed time in milliseconds"
    )
    assert (
        expected_out in captured.out
    ), "expected validated manifest count summary"


def test_main_reports_invalid_manifest_path_and_error(
    tmp_path: Path,
) -> None:
    """Verify main reports invalid manifest paths and validation errors."""
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
    """Verify main writes validation failures to the injected error stream."""
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
