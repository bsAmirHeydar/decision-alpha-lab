from __future__ import annotations

from pathlib import Path

import pytest

from sf_phase00.contracts import extract_python_contracts
from sf_phase00.versioning import validate_schema_version


def test_extracts_public_class_methods(tmp_path: Path) -> None:
    (tmp_path / "lab").mkdir()
    (tmp_path / "docs").mkdir()
    source = "class Engine:\n    def run(self):\n        pass\n    def _private(self):\n        pass\n"
    (tmp_path / "lab" / "engine.py").write_text(source, encoding="utf-8")
    records = extract_python_contracts(tmp_path)
    assert len(records) == 1
    assert records[0].symbol == "Engine"
    assert records[0].public_methods == ("run",)


def test_version_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="Schema major mismatch"):
        validate_schema_version({"schema_version": "2.0.0"}, expected_major=1)


def test_missing_version_is_rejected() -> None:
    with pytest.raises(ValueError, match="Missing schema_version"):
        validate_schema_version({})
