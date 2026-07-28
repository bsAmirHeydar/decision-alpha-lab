from __future__ import annotations

import json
import zipfile
from pathlib import Path

from tools.consolidation.uc04w1b.contracts import write_json
from tools.consolidation.uc04w1b.native_review import review_native_receipt
from tools.consolidation.uc04w1bn1.evidence_export import build_bundle
from tests.consolidation.uc04w1b.test_native_review import build_native_evidence


def test_evidence_bundle_is_sanitized_and_hash_bound(repo_root: Path, tmp_path: Path) -> None:
    run_root = tmp_path / "native_host_qualification" / "20260728T000000Z"
    receipt = build_native_evidence(repo_root, run_root)
    document = json.loads(receipt.read_text(encoding="utf-8"))
    document.update(
        {
            "repository_root": "C:/Users/Amir/private/repository",
            "run_root": "C:/Users/Amir/AppData/Local/AlphaLab/run",
            "metaeditor_path": "C:/Broker/metaeditor64.exe",
            "terminal_path": "C:/Broker/terminal64.exe",
            "terminal_data_path": "C:/Users/Amir/AppData/Roaming/MetaQuotes/Terminal/ABC",
            "terminal_common_files_path": "C:/ProgramData/MetaQuotes/Terminal/Common/Files",
        }
    )
    write_json(receipt, document)
    review = run_root / "independent_native_review.json"
    write_json(review, review_native_receipt(repo_root, receipt))

    output = tmp_path / "evidence.zip"
    build_bundle(run_root, output)

    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        assert names == sorted(names)
        assert "native_acceptance_receipt.sanitized.json" in names
        assert "native_acceptance_receipt.json" not in names
        sanitized = json.loads(archive.read("native_acceptance_receipt.sanitized.json"))
        manifest = json.loads(archive.read("bundle_manifest.json"))
        for key in (
            "repository_root",
            "run_root",
            "metaeditor_path",
            "terminal_path",
            "terminal_data_path",
            "terminal_common_files_path",
        ):
            assert key not in sanitized
        assert sanitized["host_paths_redacted"] is True
        assert manifest["host_paths_redacted"] is True
        assert manifest["secret_material_included"] is False
        assert manifest["account_identifiers_included"] is False
        assert manifest["apply_authorized"] is False
        assert manifest["member_count"] == len(manifest["members"])


def test_bundle_is_byte_reproducible(repo_root: Path, tmp_path: Path) -> None:
    run_root = tmp_path / "native_host_qualification" / "20260728T000000Z"
    receipt = build_native_evidence(repo_root, run_root)
    review = run_root / "independent_native_review.json"
    write_json(review, review_native_receipt(repo_root, receipt))
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    build_bundle(run_root, first)
    build_bundle(run_root, second)
    assert first.read_bytes() == second.read_bytes()
