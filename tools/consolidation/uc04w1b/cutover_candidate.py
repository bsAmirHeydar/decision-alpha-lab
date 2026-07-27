from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any

from tools.repository_paths import RepositoryPaths
from tools.consolidation.uc04w1.characterize import MEMBERS, characterize, extract_function
from tools.consolidation.uc04w1b.contracts import (
    CANONICAL_FUNCTION_NAME,
    CANDIDATE_ID,
    CUTOVER_BOUNDARY,
    ENGINE_ID,
    PRODUCTION_INCLUDE,
    PRODUCTION_INCLUDE_DIRECTIVE,
    PROGRAM_ID,
    canonical_digest,
    read_json,
    sha256_bytes,
    sha256_file,
    with_digest,
    write_json,
)


class CutoverCandidateError(ValueError):
    """Raised when an evidence-gated cutover candidate cannot be generated."""


PRODUCTION_HEADER = f'''#ifndef ALPHA_LAB_{ENGINE_ID}_DETERMINISTIC_DATETIME_FORMAT_MQH
#define ALPHA_LAB_{ENGINE_ID}_DETERMINISTIC_DATETIME_FORMAT_MQH

// UC04-W1B evidence-gated shared primitive.
// Pure deterministic formatting only: no time acquisition, market data,
// file, network, chart, order, runtime or capital authority.
string {CANONICAL_FUNCTION_NAME}(const datetime value)
{{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}}

#endif
'''

PRODUCTION_RUNNER = f'''//+------------------------------------------------------------------+
//| Alpha Lab UC04-W1B production formatter native qualification     |
//| Test-only script: no trading, order or capital authority          |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property script_show_inputs

#include <AlphaLab/ContextOS/Shared/{ENGINE_ID}/AL_DeterministicDateTimeFormat.mqh>

#define UC04W1B_RUNTIME_OUTPUT "AlphaLab\\UC04W1B\\UC04W1B_ProductionDateTimeFormatNativeRunner.csv"

string UC04W1B_LegacyFormatDateTime(const datetime value)
{{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}}

void OnStart()
{{
   datetime values[] =
   {{
      D'1970.01.01 00:00:00', D'1970.01.01 00:00:01',
      D'1970.01.01 00:00:59', D'1970.01.01 00:01:00',
      D'1970.01.01 23:59:59', D'1970.01.02 00:00:00',
      D'1999.12.31 23:59:59', D'2000.02.29 12:34:56',
      D'2009.02.13 23:31:30', D'2024.02.29 00:00:00',
      D'2026.07.27 12:34:56', D'2038.01.19 03:14:07',
      D'2099.12.31 23:59:59'
   }};
   string expected[] =
   {{
      "1970.01.01 00:00:00", "1970.01.01 00:00:01",
      "1970.01.01 00:00:59", "1970.01.01 00:01:00",
      "1970.01.01 23:59:59", "1970.01.02 00:00:00",
      "1999.12.31 23:59:59", "2000.02.29 12:34:56",
      "2009.02.13 23:31:30", "2024.02.29 00:00:00",
      "2026.07.27 12:34:56", "2038.01.19 03:14:07",
      "2099.12.31 23:59:59"
   }};

   int handle = FileOpen(UC04W1B_RUNTIME_OUTPUT,
                         FILE_COMMON | FILE_WRITE | FILE_CSV | FILE_ANSI,
                         ',');
   if(handle == INVALID_HANDLE)
   {{
      Print("UC04-W1B PRODUCTION SELFTEST FAIL: FileOpen error=", GetLastError());
      return;
   }}
   FileWrite(handle, "fixture_id", "unix_seconds", "expected", "legacy_output", "reference_output", "status");
   bool all_passed = (ArraySize(values) == ArraySize(expected));
   for(int i = 0; i < ArraySize(values); i++)
   {{
      string legacy_output = UC04W1B_LegacyFormatDateTime(values[i]);
      string production_output = {CANONICAL_FUNCTION_NAME}(values[i]);
      bool passed = (legacy_output == expected[i] &&
                     production_output == expected[i] &&
                     legacy_output == production_output &&
                     StringLen(production_output) == 19);
      if(!passed) all_passed = false;
      FileWrite(handle,
                "UC04W1_DT_" + StringFormat("%03d", i + 1),
                IntegerToString((long)values[i]),
                expected[i],
                legacy_output,
                production_output,
                (passed ? "PASS" : "FAIL"));
   }}
   FileWrite(handle,
             "SUMMARY",
             IntegerToString(ArraySize(values)),
             "BYTE_EXACT_ASCII",
             "LEGACY_REFERENCE",
             "PRODUCTION_SHARED_ENGINE",
             (all_passed ? "PASS" : "FAIL"));
   FileFlush(handle);
   FileClose(handle);
   Print("UC04-W1B PRODUCTION SELFTEST ", (all_passed ? "PASS" : "FAIL"));
}}
'''

PRODUCTION_RUNNER_PATH = Path(
    "mql5/Tests/Scripts/UC04/UC04W1B_ProductionDateTimeFormatNativeRunner.mq5"
)


def _verify_review(receipt_path: Path, review_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = read_json(receipt_path)
    review = read_json(review_path)
    if receipt.get("status") != "PASS" or review.get("status") != "PASS":
        raise CutoverCandidateError("native receipt and independent review must both PASS")
    if receipt.get("candidate_id") != CANDIDATE_ID or review.get("candidate_id") != CANDIDATE_ID:
        raise CutoverCandidateError("candidate identity drift")
    if receipt.get("engine_id") != ENGINE_ID or review.get("engine_id") != ENGINE_ID:
        raise CutoverCandidateError("engine identity drift")
    if review.get("receipt_sha256") != sha256_file(receipt_path):
        raise CutoverCandidateError("independent review is not bound to the supplied receipt")
    if review.get("document_digest") != canonical_digest(review):
        raise CutoverCandidateError("independent review document digest mismatch")
    for document in (receipt, review):
        for field in (
            "implementation_authority",
            "consumer_cutover_authority",
            "deletion_authority",
            "runtime_authority",
            "order_authority",
            "capital_authority",
        ):
            if document.get(field) is not False:
                raise CutoverCandidateError(f"evidence document grants forbidden authority: {field}")
    return receipt, review


def _add_include(text: str) -> str:
    if PRODUCTION_INCLUDE_DIRECTIVE in text:
        return text
    matches = list(re.finditer(r"(?m)^#include[^\r\n]*(?:\r?\n)", text))
    if not matches:
        raise CutoverCandidateError("consumer has no include block")
    position = matches[-1].end()
    return text[:position] + PRODUCTION_INCLUDE_DIRECTIVE + "\n" + text[position:]


def _replace_wrapper(text: str, function_name: str) -> str:
    function_text, _, _, _ = extract_function(text, function_name)
    wrapper = (
        f"string {function_name}(const datetime value)\n"
        "{\n"
        f"   return {CANONICAL_FUNCTION_NAME}(value);\n"
        "}"
    )
    if text.count(function_text) != 1:
        raise CutoverCandidateError(f"function replacement is not unique: {function_name}")
    return text.replace(function_text, wrapper, 1)


def _write_payload_file(payload_root: Path, relative: Path, data: bytes) -> None:
    target = payload_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def _zip_payload(candidate_root: Path, output_zip: Path) -> None:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(candidate_root.rglob("*")):
            if path.is_file() and path != output_zip:
                archive.write(path, path.relative_to(candidate_root).as_posix())


def build_cutover_candidate(
    repo: Path,
    receipt_path: Path,
    review_path: Path,
    output_root: Path | None = None,
) -> Path:
    root = RepositoryPaths.discover(repo).root
    receipt_path = receipt_path.resolve()
    review_path = review_path.resolve()
    receipt, review = _verify_review(receipt_path, review_path)

    # Re-run W1A characterization immediately before generating any candidate.
    documents = characterize(root)
    inventory = documents["candidate_inventory.json"]
    receipt_id = str(receipt.get("receipt_id", "UC04_W1B_NATIVE_UNKNOWN"))
    safe_id = re.sub(r"[^A-Za-z0-9_.-]", "_", receipt_id)
    candidate_root = (
        output_root.resolve()
        if output_root is not None
        else (root / CUTOVER_BOUNDARY / safe_id).resolve()
    )
    if candidate_root.exists():
        raise CutoverCandidateError(f"candidate output already exists: {candidate_root}")
    payload_root = candidate_root / "payload"
    payload_root.mkdir(parents=True, exist_ok=False)

    _write_payload_file(payload_root, PRODUCTION_INCLUDE, PRODUCTION_HEADER.encode("utf-8"))
    _write_payload_file(payload_root, PRODUCTION_RUNNER_PATH, PRODUCTION_RUNNER.encode("utf-8"))

    inventory_by_path = {
        str(row["artifact_path"]): row
        for row in inventory.get("members", [])
        if isinstance(row, dict)
    }
    changes: list[dict[str, Any]] = []
    for artifact_path, function_name, family in MEMBERS:
        source = root / artifact_path
        before = source.read_text(encoding="utf-8-sig")
        call_sites_before = len(re.findall(rf"\b{re.escape(function_name)}\s*\(", before)) - 1
        after = _replace_wrapper(_add_include(before), function_name)
        call_sites_after = len(re.findall(rf"\b{re.escape(function_name)}\s*\(", after)) - 1
        if call_sites_after != call_sites_before:
            raise CutoverCandidateError(f"call-site count changed: {artifact_path}")
        if after.count(PRODUCTION_INCLUDE_DIRECTIVE) != 1:
            raise CutoverCandidateError(f"canonical include count is not one: {artifact_path}")
        if after.count(f"return {CANONICAL_FUNCTION_NAME}(value);") != 1:
            raise CutoverCandidateError(f"wrapper count is not one: {artifact_path}")
        _write_payload_file(payload_root, Path(artifact_path), after.encode("utf-8"))
        changes.append(
            {
                "path": artifact_path,
                "family": family,
                "legacy_function_name": function_name,
                "call_site_count_before": call_sites_before,
                "call_site_count_after": call_sites_after,
                "before_sha256": sha256_file(source),
                "accepted_w1a_sha256": str(inventory_by_path[artifact_path]["artifact_sha256"]),
                "after_sha256": sha256_bytes(after.encode("utf-8")),
                "change_class": "INCLUDE_PLUS_LOCAL_NAME_WRAPPER_ONLY",
            }
        )

    patch_paths = sorted(
        path.relative_to(payload_root).as_posix()
        for path in payload_root.rglob("*")
        if path.is_file()
    )
    patch_hashes = {
        relative: sha256_file(payload_root / relative)
        for relative in patch_paths
    }
    manifest = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1b/cutover_candidate_manifest.schema.json",
            "schema_version": "1.0.0",
            "program_id": PROGRAM_ID,
            "stage_id": "UC04-W1B-CANDIDATE",
            "candidate_manifest_id": f"UC04_W1B_CUTOVER_CANDIDATE_{safe_id}",
            "status": "GENERATED_PENDING_POST_CUTOVER_NATIVE_QUALIFICATION",
            "candidate_id": CANDIDATE_ID,
            "engine_id": ENGINE_ID,
            "native_receipt_sha256": sha256_file(receipt_path),
            "independent_review_sha256": sha256_file(review_path),
            "production_include": PRODUCTION_INCLUDE.as_posix(),
            "production_runner": PRODUCTION_RUNNER_PATH.as_posix(),
            "consumer_count": len(changes),
            "active_call_site_count": sum(int(row["call_site_count_before"]) for row in changes),
            "consumer_changes": changes,
            "patch_file_count": len(patch_paths),
            "patch_paths": patch_paths,
            "patch_hashes": patch_hashes,
            "semantic_change": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
            "next_required_evidence": [
                "POST_CUTOVER_METAEDITOR_0_ERROR_0_WARNING_MATRIX",
                "PRODUCTION_SHARED_ENGINE_13_VECTOR_RUNTIME_PASS",
                "FINAL_CUTOVER_REVIEW_PASS",
            ],
        }
    )
    rollback = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1b/rollback_manifest.schema.json",
            "schema_version": "1.0.0",
            "program_id": PROGRAM_ID,
            "stage_id": "UC04-W1B-CANDIDATE",
            "candidate_id": CANDIDATE_ID,
            "engine_id": ENGINE_ID,
            "rollback_id": f"UC04_W1B_ROLLBACK_{safe_id}",
            "status": "READY",
            "strategy": "RESTORE_TEN_ACCEPTED_W1A_CONSUMER_BYTES_AND_DELETE_TWO_NEW_FILES",
            "restore_files": [
                {
                    "path": row["path"],
                    "expected_current_sha256": row["after_sha256"],
                    "restore_sha256": row["before_sha256"],
                }
                for row in changes
            ],
            "delete_files": [PRODUCTION_INCLUDE.as_posix(), PRODUCTION_RUNNER_PATH.as_posix()],
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
        }
    )
    write_json(candidate_root / "CUTOVER_CANDIDATE_MANIFEST.json", manifest)
    write_json(candidate_root / "ROLLBACK_MANIFEST.json", rollback)
    (candidate_root / "PATCH_FILE_INDEX.txt").write_text(
        "\n".join(patch_paths) + "\n", encoding="utf-8", newline="\n"
    )
    (candidate_root / "PATCH_FILE_HASHES.sha256").write_text(
        "\n".join(
            f"{patch_hashes[path].removeprefix('sha256:')}  {path}"
            for path in patch_paths
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (candidate_root / "README.md").write_text(
        "# UC04-W1B Cutover Candidate\n\n"
        "This payload is evidence-gated and is **not apply-authorized**. "
        "Compile the overlay and run the production shared-engine native self-test first.\n",
        encoding="utf-8",
        newline="\n",
    )
    output_zip = candidate_root / f"ALPHA_LAB_UC04_W1B_CUTOVER_CANDIDATE_{safe_id}.zip"
    _zip_payload(candidate_root, output_zip)
    return candidate_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an evidence-gated UC04-W1B cutover candidate.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--review", required=True)
    parser.add_argument("--output-root", default="")
    args = parser.parse_args()
    candidate = build_cutover_candidate(
        Path(args.repo_root),
        Path(args.receipt),
        Path(args.review),
        Path(args.output_root) if args.output_root else None,
    )
    print(f"UC04-W1B cutover candidate generated: {candidate}")
    print("Status: PENDING_POST_CUTOVER_NATIVE_QUALIFICATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
