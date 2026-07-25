from __future__ import annotations
from tools.repository_paths import find_repository_root

import shutil
from pathlib import Path

import pytest

from tools.strategy_factory.acl_os.acl_03.errors import PrerequisiteError
from tools.strategy_factory.contexts.rthp.acl03_onboarding import compile_rthp_acl03

ROOT = find_repository_root(__file__)
CONTEXT = ROOT / "contexts/legacy/strategy_factory/authored/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1"
EVIDENCE = CONTEXT / "generated/acl_03/evidence"
TEXT_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".txt", ".csv", ".html"}


def _compile(package_root: Path, output_root: Path):
    return compile_rthp_acl03(
        package_root,
        output_root / "compiled",
        output_root / "bindings",
        EVIDENCE / "authority_permit.json",
        EVIDENCE / "semantic_approval.json",
        EVIDENCE / "acl02_readiness.json",
    )


def _crlf_copy(destination: Path) -> Path:
    shutil.copytree(CONTEXT, destination)
    for path in destination.rglob("*"):
        if path.is_file() and path.suffix.casefold() in TEXT_EXTENSIONS:
            payload = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            path.write_bytes(payload.replace(b"\n", b"\r\n"))
    return destination


def test_rthp_acl03_wrapper_accepts_eol_only_windows_checkout(tmp_path):
    package = _crlf_copy(tmp_path / "context")
    result = _compile(package, tmp_path / "out")
    assert result["passed"] is True


def test_rthp_acl03_wrapper_still_rejects_semantic_drift(tmp_path):
    package = _crlf_copy(tmp_path / "context")
    doctrine = package / "doctrine/context_doctrine.md"
    doctrine.write_text(doctrine.read_text(encoding="utf-8") + "\nSEMANTIC DRIFT\n", encoding="utf-8", newline="\r\n")
    with pytest.raises(PrerequisiteError, match="ACL03_SOURCE_CHANGED_AFTER_APPROVAL"):
        _compile(package, tmp_path / "out")
