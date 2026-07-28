from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import zipfile
from pathlib import Path
from typing import Any

from tools.consolidation.uc04w1b.contracts import read_json
from tools.consolidation.uc04w1bn1.contracts import (
    CANDIDATE_ID,
    ENGINE_ID,
    PROGRAM_ID,
    STAGE_ID,
    write_json,
)

SAFE_MEMBER_RE = re.compile(r"^[A-Za-z0-9._/-]+$")


class EvidenceExportError(ValueError):
    """Raised when native evidence cannot be exported safely."""


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _relative(root: Path, path: Path) -> str:
    resolved_root = root.resolve()
    resolved = path.resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise EvidenceExportError(f"evidence path escapes run root: {path}")
    return resolved.relative_to(resolved_root).as_posix()


def _sanitize_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    output = dict(receipt)
    for key in (
        "metaeditor_path",
        "terminal_path",
        "terminal_data_path",
        "terminal_common_files_path",
        "repository_root",
        "run_root",
    ):
        output.pop(key, None)
    output["host_paths_redacted"] = True
    return output


def _collect_files(run_root: Path, receipt: dict[str, Any]) -> list[Path]:
    files: list[Path] = []
    for row in receipt.get("compile_targets", []):
        if not isinstance(row, dict):
            raise EvidenceExportError("compile target row must be an object")
        for key in ("log_path", "ex5_path"):
            value = row.get(key)
            if not isinstance(value, str):
                raise EvidenceExportError(f"missing compile evidence path: {key}")
            files.append(run_root / value)
    runtime = receipt.get("runtime")
    if not isinstance(runtime, dict):
        raise EvidenceExportError("runtime receipt missing")
    runtime_path = runtime.get("runtime_csv_path")
    if not isinstance(runtime_path, str):
        raise EvidenceExportError("runtime CSV path missing")
    files.append(run_root / runtime_path)
    files.append(run_root / "independent_native_review.json")
    return files


def build_bundle(run_root: Path, output: Path) -> Path:
    run_root = run_root.resolve()
    receipt_path = run_root / "native_acceptance_receipt.json"
    review_path = run_root / "independent_native_review.json"
    if not receipt_path.is_file() or not review_path.is_file():
        raise EvidenceExportError("native receipt and independent review are required")
    receipt = read_json(receipt_path)
    review = read_json(review_path)
    if receipt.get("status") != "PASS" or review.get("status") != "PASS":
        raise EvidenceExportError("native receipt and independent review must both PASS")
    if receipt.get("candidate_id") != CANDIDATE_ID or review.get("candidate_id") != CANDIDATE_ID:
        raise EvidenceExportError("candidate identity drift")
    if receipt.get("engine_id") != ENGINE_ID or review.get("engine_id") != ENGINE_ID:
        raise EvidenceExportError("engine identity drift")

    files = _collect_files(run_root, receipt)
    for path in files:
        if not path.is_file():
            raise EvidenceExportError(f"evidence file missing: {path}")
        _relative(run_root, path)

    candidate_manifests = sorted(
        run_root.parent.parent.joinpath("cutover_candidates").glob(
            "*/CUTOVER_CANDIDATE_MANIFEST.json"
        )
    )
    candidate_manifest = candidate_manifests[-1] if candidate_manifests else None

    sanitized_receipt = _sanitize_receipt(receipt)
    sanitized_path = run_root / "native_acceptance_receipt.sanitized.json"
    write_json(sanitized_path, sanitized_receipt)
    files.append(sanitized_path)
    files.append(review_path)
    if candidate_manifest is not None:
        files.append(candidate_manifest)

    members: list[dict[str, Any]] = []
    for path in sorted(set(files)):
        if path == receipt_path:
            continue
        if path == candidate_manifest:
            archive_name = "candidate/CUTOVER_CANDIDATE_MANIFEST.json"
        else:
            relative = _relative(run_root, path)
            archive_name = relative
        if not SAFE_MEMBER_RE.fullmatch(archive_name) or archive_name.startswith("/") or ".." in Path(archive_name).parts:
            raise EvidenceExportError(f"unsafe evidence member: {archive_name}")
        members.append(
            {
                "path": archive_name,
                "sha256": _sha256(path),
                "size_bytes": path.stat().st_size,
                "source": str(path),
            }
        )

    manifest = {
        "schema_version": "1.0.0",
        "program_id": PROGRAM_ID,
        "stage_id": STAGE_ID,
        "bundle_id": "UC04_W1B_N1_NATIVE_EVIDENCE_BUNDLE_V1",
        "status": "PASS",
        "candidate_id": CANDIDATE_ID,
        "engine_id": ENGINE_ID,
        "host_paths_redacted": True,
        "secret_material_included": False,
        "account_identifiers_included": False,
        "member_count": len(members),
        "members": [{key: value for key, value in row.items() if key != "source"} for row in members],
        "apply_authorized": False,
        "implementation_authority": False,
        "consumer_cutover_authority": False,
        "order_authority": False,
        "capital_authority": False,
    }
    manifest_path = run_root / "bundle_manifest.json"
    write_json(manifest_path, manifest)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    timestamp = (1980, 1, 1, 0, 0, 0)
    payloads = {str(row["path"]): Path(str(row["source"])).read_bytes() for row in members}
    payloads["bundle_manifest.json"] = manifest_path.read_bytes()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(payloads):
            info = zipfile.ZipInfo(name, timestamp)
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payloads[name])
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a sanitized UC04-W1B-N1 native evidence bundle.")
    parser.add_argument("--run-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        output = build_bundle(Path(args.run_root), Path(args.output))
    except (OSError, ValueError, EvidenceExportError) as exc:
        print(f"UC04-W1B-N1 evidence export failed: {exc}")
        return 1
    print(f"UC04-W1B-N1 evidence bundle: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
