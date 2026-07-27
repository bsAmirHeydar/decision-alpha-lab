from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools.consolidation.ci.portable_hash import canonical_sha256
from tools.repository_paths import RepositoryPaths

CANDIDATE_ID = "ENGCAND_5F87C4D5849C4FD141DDBF29590235D8"
ENGINE_ID = "ENG_9599AA665C5BC4B13B020EBA4213CB16"
HISTORICAL_CLUSTER_DIGEST = "sha256:f317c18e7ca700a7f7eff82a9042857d78dc6819a8fb981e5fc7edb6afaea83c"
HISTORICAL_NORMALIZED_BODY_DIGEST = "sha256:e17791f58738094ca4fad01a659c9b4a4055894c1c8c78ec2ef1d7b90a21d68c"
HISTORICAL_CLUSTER_PATH = Path(
    "registry/history/lcm/shared_engines/"
    "SHAREDENG_F1EFFB190FA1F0AE0D31369EEDB82A3A/"
    "candidates/selected_candidate_clusters.jsonl"
)
REGISTRY_ROOT = Path("registry/consolidation/uc04/w1")
FIXTURE_ROOT = Path("tests/fixtures/consolidation/uc04w1")
REFERENCE_HEADER = Path(
    "mql5/Tests/Include/AlphaLab/UC04W1/"
    "AL_UC04W1_ReferenceDateTimeFormat.mqh"
)
SELF_TEST = Path(
    "mql5/Tests/Experts/UC04/"
    "UC04W1_DeterministicDateTimeFormatSelfTest.mq5"
)
PROPOSED_PRODUCTION_TARGET = Path(
    "mql5/Include/AlphaLab/ContextOS/Shared/"
    f"{ENGINE_ID}/AL_DeterministicDateTimeFormat.mqh"
)

MEMBERS: tuple[tuple[str, str, str], ...] = (
    ("mql5/Experts/Debug/D0005_H5NoFutureWalkForwardAudit.mq5", "D0005_FormatDateTime", "DEBUG"),
    ("mql5/Experts/Debug/D0006_H5LiveTouchReplayAudit.mq5", "D0006_FormatDateTime", "DEBUG"),
    ("mql5/Experts/Execution/E0001_ReversalOneToOne.mq5", "E0001_FormatDateTime", "EXECUTION"),
    ("mql5/Experts/Execution/E0002_CloseConfirmedMarket.mq5", "E0002_FormatDateTime", "EXECUTION"),
    ("mql5/Experts/Execution/E0003_ContinuationCloseHunt.mq5", "E0003_FormatDateTime", "EXECUTION"),
    ("mql5/Experts/Execution/E0004_ContinuationHeikinAshiFlip.mq5", "E0004_FormatDateTime", "EXECUTION"),
    ("mql5/Experts/Execution/E0005_ContinuationCloseBreakFixedR.mq5", "E0005_FormatDateTime", "EXECUTION"),
    ("mql5/Experts/Execution/E0006_AllZoneTouchLimitFixedR.mq5", "E0006_FormatDateTime", "EXECUTION"),
    ("mql5/Experts/Execution/E0010_PureHeikinAshiMtfRoulette.mq5", "E0010_FormatDateTime", "EXECUTION"),
    ("mql5/Experts/Execution/E0011_Donchian20Atr3Roulette.mq5", "E0011_FormatDateTime", "EXECUTION"),
)

FUNCTION_RE_TEMPLATE = r"(?ms)^\s*string\s+{name}\s*\(\s*const\s+datetime\s+value\s*\)\s*\{{"
EXPECTED_BODY_COMPACT = re.sub(
    r"\s+",
    "",
    """{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}""",
)

FIXTURE_TIMES: tuple[datetime, ...] = (
    datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    datetime(1970, 1, 1, 0, 0, 1, tzinfo=timezone.utc),
    datetime(1970, 1, 1, 0, 0, 59, tzinfo=timezone.utc),
    datetime(1970, 1, 1, 0, 1, 0, tzinfo=timezone.utc),
    datetime(1970, 1, 1, 23, 59, 59, tzinfo=timezone.utc),
    datetime(1970, 1, 2, 0, 0, 0, tzinfo=timezone.utc),
    datetime(1999, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
    datetime(2000, 2, 29, 12, 34, 56, tzinfo=timezone.utc),
    datetime(2009, 2, 13, 23, 31, 30, tzinfo=timezone.utc),
    datetime(2024, 2, 29, 0, 0, 0, tzinfo=timezone.utc),
    datetime(2026, 7, 27, 12, 34, 56, tzinfo=timezone.utc),
    datetime(2038, 1, 19, 3, 14, 7, tzinfo=timezone.utc),
    datetime(2099, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
)


@dataclass(frozen=True)
class FunctionSnapshot:
    artifact_path: str
    function_name: str
    family: str
    artifact_sha256: str
    function_text_sha256: str
    function_body_sha256: str
    line_start: int
    line_end: int
    call_site_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_path": self.artifact_path,
            "function_name": self.function_name,
            "family": self.family,
            "artifact_sha256": self.artifact_sha256,
            "function_text_sha256": self.function_text_sha256,
            "function_body_sha256": self.function_body_sha256,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "call_site_count": self.call_site_count,
            "signature": "string(const datetime value)",
            "current_bar_access": False,
            "timeframe_access": False,
            "session_or_dst_access": False,
            "file_read_api": False,
            "file_write_api": False,
            "network_api": False,
            "object_mutation_api": False,
            "order_api": False,
        }


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + canonical_sha256(path)


def canonical_digest(document: dict[str, Any], field: str = "document_digest") -> str:
    material = {key: value for key, value in document.items() if key != field}
    payload = json.dumps(
        material,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(payload)


def with_digest(document: dict[str, Any], field: str = "document_digest") -> dict[str, Any]:
    value = dict(document)
    value[field] = canonical_digest(value, field)
    return value


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def extract_function(text: str, function_name: str) -> tuple[str, str, int, int]:
    pattern = re.compile(FUNCTION_RE_TEMPLATE.format(name=re.escape(function_name)))
    match = pattern.search(text)
    if match is None:
        raise ValueError(f"function not found: {function_name}")
    brace_start = match.end() - 1
    depth = 0
    in_string = False
    escaped = False
    end: int | None = None
    for index in range(brace_start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = index + 1
                break
    if end is None:
        raise ValueError(f"unterminated function: {function_name}")
    function_text = text[match.start():end].lstrip("\r\n")
    body_text = text[brace_start:end]
    line_start = text.count("\n", 0, match.start()) + 1
    line_end = text.count("\n", 0, end) + 1
    return function_text, body_text, line_start, line_end


def snapshot_member(repo: Path, artifact_path: str, function_name: str, family: str) -> FunctionSnapshot:
    path = repo / artifact_path
    text = path.read_text(encoding="utf-8-sig")
    function_text, body_text, line_start, line_end = extract_function(text, function_name)
    if re.sub(r"\s+", "", body_text) != EXPECTED_BODY_COMPACT:
        raise ValueError(f"candidate body drift: {artifact_path}:{function_name}")
    call_count = len(re.findall(rf"\b{re.escape(function_name)}\s*\(", text)) - 1
    return FunctionSnapshot(
        artifact_path=artifact_path,
        function_name=function_name,
        family=family,
        artifact_sha256=sha256_file(path),
        function_text_sha256=sha256_bytes(function_text.replace("\r\n", "\n").encode("utf-8")),
        function_body_sha256=sha256_bytes(body_text.replace("\r\n", "\n").encode("utf-8")),
        line_start=line_start,
        line_end=line_end,
        call_site_count=call_count,
    )


def load_historical_candidate(repo: Path) -> dict[str, Any]:
    path = repo / HISTORICAL_CLUSTER_PATH
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("candidate_id") == CANDIDATE_ID:
            return row
    raise ValueError(f"historical candidate not found: {CANDIDATE_ID}")


def fixture_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, value in enumerate(FIXTURE_TIMES, start=1):
        rows.append(
            {
                "fixture_id": f"UC04W1_DT_{index:03d}",
                "unix_seconds": int(value.timestamp()),
                "mql5_literal": value.strftime("D'%Y.%m.%d %H:%M:%S'"),
                "expected": value.strftime("%Y.%m.%d %H:%M:%S"),
            }
        )
    return rows


def characterize(repo: Path) -> dict[str, dict[str, Any]]:
    historical = load_historical_candidate(repo)
    snapshots = [snapshot_member(repo, *member) for member in MEMBERS]
    current_paths = {item.artifact_path for item in snapshots}
    historical_paths = {str(item["artifact_path"]) for item in historical.get("members", [])}
    if current_paths != historical_paths:
        raise ValueError("current candidate membership does not match historical LCM cluster")
    if historical.get("candidate_digest") != HISTORICAL_CLUSTER_DIGEST:
        raise ValueError("historical candidate digest drift")
    if historical.get("normalized_body_sha256") != HISTORICAL_NORMALIZED_BODY_DIGEST:
        raise ValueError("historical normalized body digest drift")
    historical_hashes = {
        str(item["artifact_path"]): str(item["artifact_sha256"])
        for item in historical.get("members", [])
    }
    for item in snapshots:
        if historical_hashes.get(item.artifact_path) != item.artifact_sha256:
            raise ValueError(f"source digest drift from accepted LCM evidence: {item.artifact_path}")

    body_hashes = sorted({item.function_body_sha256 for item in snapshots})
    fixtures = fixture_rows()
    inventory = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/candidate_inventory.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "inventory_id": "UC04_W1A_DETERMINISTIC_DATETIME_CANDIDATE_INVENTORY_V1",
            "status": "PASS",
            "candidate_id": CANDIDATE_ID,
            "engine_id": ENGINE_ID,
            "category": "DETERMINISTIC_FORMATTING",
            "historical_candidate_digest": HISTORICAL_CLUSTER_DIGEST,
            "historical_normalized_body_sha256": HISTORICAL_NORMALIZED_BODY_DIGEST,
            "consumer_count": len(snapshots),
            "active_call_site_count": sum(item.call_site_count for item in snapshots),
            "distinct_function_body_count": len(body_hashes),
            "function_body_sha256": body_hashes[0],
            "members": [item.to_dict() for item in snapshots],
            "repository_wide_exact_match_count": len(snapshots),
            "semantic_change": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
        }
    )
    format_contract = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/datetime_format_contract.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "contract_id": "UC04_W1A_DETERMINISTIC_DATETIME_FORMAT_CONTRACT_V1",
            "status": "FROZEN",
            "candidate_id": CANDIDATE_ID,
            "input_type": "datetime",
            "output_type": "string",
            "exact_format_string": "%04d.%02d.%02d %02d:%02d:%02d",
            "output_regex": "^[0-9]{4}\\.[0-9]{2}\\.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$",
            "output_length": 19,
            "precision": "SECOND",
            "calendar_projection": "MQL5_TimeToStruct",
            "timezone_conversion": "NONE",
            "locale_contract": "ASCII_DIGITS_AND_FIXED_SEPARATORS",
            "zero_value_output": "1970.01.01 00:00:00",
            "null_contract": "NOT_APPLICABLE_DATETIME_IS_VALUE_TYPE",
            "sign_contract": "NOT_APPLICABLE",
            "decimal_contract": "NOT_APPLICABLE",
            "failure_contract": "LEGACY_TimeToStruct_RETURN_VALUE_IGNORED",
            "side_effects": [],
            "known_time_semantics": "PURE_REPRESENTATION_ONLY_NO_TIME_ACQUISITION",
            "semantic_change": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
        }
    )
    fixture_corpus = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/fixture_corpus.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "corpus_id": "UC04_W1A_DATETIME_FORMAT_FIXTURE_CORPUS_V1",
            "status": "PASS_REFERENCE",
            "candidate_id": CANDIDATE_ID,
            "comparison_mode": "BYTE_EXACT_ASCII",
            "fixture_count": len(fixtures),
            "fixtures": fixtures,
            "metamorphic_properties": [
                "FIXED_LENGTH_19",
                "ASCII_ONLY",
                "PUNCTUATION_AT_FIXED_OFFSETS",
                "CHRONOLOGICAL_ORDER_PRESERVES_LEXICOGRAPHIC_ORDER",
                "FUNCTION_NAME_INVARIANCE",
                "LOCALE_INVARIANCE_BY_CONTRACT",
            ],
            "native_execution_performed": False,
            "semantic_change": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
        }
    )
    reference_design = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/reference_design.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "design_id": "UC04_W1A_DETERMINISTIC_DATETIME_REFERENCE_DESIGN_V1",
            "status": "TEST_ONLY_REFERENCE",
            "candidate_id": CANDIDATE_ID,
            "engine_id": ENGINE_ID,
            "reference_header": REFERENCE_HEADER.as_posix(),
            "reference_header_sha256": sha256_file(repo / REFERENCE_HEADER),
            "native_self_test": SELF_TEST.as_posix(),
            "native_self_test_sha256": sha256_file(repo / SELF_TEST),
            "proposed_production_target": PROPOSED_PRODUCTION_TARGET.as_posix(),
            "production_target_materialized": False,
            "consumer_files_modified": False,
            "wrapper_strategy": "PRESERVE_EXISTING_FUNCTION_NAMES_AND_DELEGATE_AFTER_NATIVE_PASS",
            "forbidden_patterns": [
                "DOMAIN_RULE_IN_SHARED_PRIMITIVE",
                "TIME_ACQUISITION",
                "CURRENT_BAR_ACCESS",
                "FILE_OR_NETWORK_IO",
                "CHART_OBJECT_MUTATION",
                "ORDER_OR_CAPITAL_AUTHORITY",
                "MUTABLE_GLOBAL_STATE",
            ],
            "semantic_change": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
        }
    )
    static_equivalence = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/static_equivalence_record.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "record_id": "UC04_W1A_STATIC_EQUIVALENCE_RECORD_V1",
            "status": "PASS_STATIC_NATIVE_PENDING",
            "candidate_id": CANDIDATE_ID,
            "source_member_count": len(snapshots),
            "exact_body_count": len(body_hashes),
            "source_hashes_match_historical_lcm": True,
            "signature_equivalence": True,
            "side_effect_equivalence": True,
            "known_time_equivalence": True,
            "fixture_reference_result": "EQUIVALENT",
            "native_compile_result": "PENDING_LOCAL_WINDOWS",
            "native_runtime_result": "PENDING_LOCAL_WINDOWS",
            "implementation_authorized": False,
            "consumer_cutover_authorized": False,
            "semantic_change": False,
        }
    )
    cutover_plan = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/consumer_cutover_plan.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "plan_id": "UC04_W1A_CONSUMER_CUTOVER_PLAN_V1",
            "status": "PLANNED_NOT_AUTHORIZED",
            "candidate_id": CANDIDATE_ID,
            "target_path": PROPOSED_PRODUCTION_TARGET.as_posix(),
            "strategy": "ADD_CANONICAL_INCLUDE_AND_RETAIN_LOCAL_NAME_WRAPPER",
            "consumer_count": len(snapshots),
            "consumers": [
                {
                    "path": item.artifact_path,
                    "legacy_function_name": item.function_name,
                    "call_site_count": item.call_site_count,
                    "planned_status": "PENDING_NATIVE_ACCEPTANCE",
                }
                for item in snapshots
            ],
            "rollback_strategy": "RESTORE_PRE_CUTOVER_SOURCE_HASHES_AND_REMOVE_CANONICAL_INCLUDE",
            "legacy_helper_deletion_planned": False,
            "consumer_files_modified": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "semantic_change": False,
            "order_authority": False,
            "capital_authority": False,
        }
    )
    native_plan = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/native_acceptance_plan.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "plan_id": "UC04_W1A_NATIVE_ACCEPTANCE_PLAN_V1",
            "status": "PENDING_LOCAL_WINDOWS",
            "candidate_id": CANDIDATE_ID,
            "capture_tool": "tools/consolidation/uc04w1/capture_native_acceptance.ps1",
            "compile_target_count": len(snapshots) + 1,
            "compile_targets": [item.artifact_path for item in snapshots] + [SELF_TEST.as_posix()],
            "required_compile_result": "0_ERRORS_0_WARNINGS",
            "runtime_self_test": SELF_TEST.as_posix(),
            "runtime_fixture_count": len(fixtures),
            "runtime_output_file": "UC04W1_DeterministicDateTimeFormatSelfTest.csv",
            "runtime_output_location": "MT5_COMMON_FILES",
            "required_runtime_summary": "PASS",
            "receipt_output_boundary": ".alpha/runs/uc04w1/native_acceptance",
            "native_compile_performed": False,
            "native_runtime_performed": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "semantic_change": False,
        }
    )
    certificate = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/logic_preservation_certificate.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "certificate_id": "UC04_W1A_LOGIC_PRESERVATION_CERTIFICATE_V1",
            "status": "BLOCKED_PENDING_NATIVE_EVIDENCE",
            "candidate_id": CANDIDATE_ID,
            "source_digests": [
                {"path": item.artifact_path, "sha256": item.artifact_sha256}
                for item in snapshots
            ],
            "reference_target": {
                "path": REFERENCE_HEADER.as_posix(),
                "sha256": sha256_file(repo / REFERENCE_HEADER),
                "production": False,
            },
            "characterization_evidence": [
                "registry/consolidation/uc04/w1/candidate_inventory.json",
                "registry/consolidation/uc04/w1/format_contract.json",
                "registry/consolidation/uc04/w1/fixture_corpus.json",
            ],
            "static_equivalence_evidence": [
                "registry/consolidation/uc04/w1/static_equivalence_record.json"
            ],
            "native_evidence": [],
            "known_time_preserved": True,
            "side_effects_preserved": True,
            "semantic_change": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
            "blocking_reasons": [
                "METAEDITOR_COMPILE_EVIDENCE_NOT_CAPTURED",
                "NATIVE_RUNTIME_FIXTURE_RECEIPT_NOT_CAPTURED",
                "INDEPENDENT_REVIEW_NOT_RECORDED",
            ],
        }
    )
    implementation_decision = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/implementation_decision.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "decision_id": "UC04_W1A_IMPLEMENTATION_DECISION_V1",
            "status": "BLOCKED_PENDING_NATIVE_EVIDENCE",
            "candidate_id": CANDIDATE_ID,
            "reference_implementation_allowed": True,
            "production_materialization_authorized": False,
            "consumer_cutover_authorized": False,
            "source_move_authorized": False,
            "source_delete_authorized": False,
            "required_next_evidence": [
                "METAEDITOR_0_ERROR_0_WARNING_COMPILE_MATRIX",
                "NATIVE_SELF_TEST_13_VECTOR_PASS_RECEIPT",
                "INDEPENDENT_REVIEW_PASS",
            ],
            "semantic_change": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
        }
    )
    ledger = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/capability_migration_ledger.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "ledger_id": "UC04_W1A_CAPABILITY_MIGRATION_LEDGER_V1",
            "status": "OPEN",
            "previous_ledger": "registry/consolidation/uc04/w0/capability_migration_ledger.json",
            "row_count": 1,
            "rows": [
                {
                    "capability_id": "DETERMINISTIC_MQL5_DATETIME_FORMATTING",
                    "candidate_id": CANDIDATE_ID,
                    "source_paths": [item.artifact_path for item in snapshots],
                    "target_path": PROPOSED_PRODUCTION_TARGET.as_posix(),
                    "disposition": "MERGE",
                    "characterization_status": "PASS",
                    "equivalence_status": "BLOCKED_NATIVE_PENDING",
                    "consumer_cutover_status": "NOT_STARTED",
                    "deletion_authority": False,
                }
            ],
            "semantic_change": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
        }
    )
    entry = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/entry_decision.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "decision_id": "UC04_W1A_ENTRY_DECISION_V1",
            "status": "ACCEPTED_CHARACTERIZATION_ONLY",
            "candidate_id": CANDIDATE_ID,
            "upstream_evidence": [
                {
                    "path": "registry/consolidation/uc04/w0/w0_exit_decision.json",
                    "sha256": sha256_file(repo / "registry/consolidation/uc04/w0/w0_exit_decision.json"),
                },
                {
                    "path": "registry/consolidation/uc04/w0/first_candidate_registration.json",
                    "sha256": sha256_file(repo / "registry/consolidation/uc04/w0/first_candidate_registration.json"),
                },
            ],
            "authorized_actions": [
                "SOURCE_AND_CONSUMER_INVENTORY",
                "BYTE_EXACT_FIXTURE_FREEZE",
                "TEST_ONLY_REFERENCE_IMPLEMENTATION",
                "STATIC_DIFFERENTIAL_AND_METAMORPHIC_TESTS",
                "NATIVE_ACCEPTANCE_HARNESS",
                "CUTOVER_PLAN_WITHOUT_WRITE",
            ],
            "prohibited_actions": [
                "PRODUCTION_SHARED_ENGINE_MATERIALIZATION",
                "CONSUMER_SOURCE_MUTATION",
                "ORDER_CAPABLE_CODE_CHANGE",
                "SOURCE_MOVE_OR_DELETE",
                "SEMANTIC_CHANGE",
                "RUNTIME_ORDER_OR_CAPITAL_AUTHORITY",
            ],
            "semantic_change": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
        }
    )
    exit_decision = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1/w1a_exit_decision.schema.json",
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1A",
            "decision_id": "UC04_W1A_EXIT_DECISION_V1",
            "status": "CHARACTERIZATION_ACCEPTED_IMPLEMENTATION_BLOCKED",
            "candidate_id": CANDIDATE_ID,
            "consumer_count": len(snapshots),
            "active_call_site_count": sum(item.call_site_count for item in snapshots),
            "fixture_count": len(fixtures),
            "static_equivalence_status": "PASS",
            "native_compile_status": "PENDING_LOCAL_WINDOWS",
            "native_runtime_status": "PENDING_LOCAL_WINDOWS",
            "logic_preservation_certificate_status": "BLOCKED_PENDING_NATIVE_EVIDENCE",
            "production_target_materialized": False,
            "consumer_files_modified": False,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
            "semantic_change": False,
            "next_delivery": "UC04-W1B_NATIVE_QUALIFICATION_AND_BOUNDED_CUTOVER",
            "accepted_evidence": [
                "entry_decision.json",
                "candidate_inventory.json",
                "format_contract.json",
                "fixture_corpus.json",
                "reference_design.json",
                "static_equivalence_record.json",
                "consumer_cutover_plan.json",
                "native_acceptance_plan.json",
                "logic_preservation_certificate.json",
                "implementation_decision.json",
                "capability_migration_ledger.json",
            ],
        }
    )
    return {
        "entry_decision.json": entry,
        "candidate_inventory.json": inventory,
        "format_contract.json": format_contract,
        "fixture_corpus.json": fixture_corpus,
        "reference_design.json": reference_design,
        "static_equivalence_record.json": static_equivalence,
        "consumer_cutover_plan.json": cutover_plan,
        "native_acceptance_plan.json": native_plan,
        "logic_preservation_certificate.json": certificate,
        "implementation_decision.json": implementation_decision,
        "capability_migration_ledger.json": ledger,
        "w1a_exit_decision.json": exit_decision,
    }


def write_records(repo: Path) -> None:
    documents = characterize(repo)
    for name, document in documents.items():
        write_json(repo / REGISTRY_ROOT / name, document)
    write_json(
        repo / FIXTURE_ROOT / "datetime_format_vectors.json",
        {
            "schema_version": "1.0.0",
            "candidate_id": CANDIDATE_ID,
            "fixture_count": len(FIXTURE_TIMES),
            "fixtures": fixture_rows(),
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Characterize the UC04-W1 deterministic MQL5 datetime formatter candidate.")
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    repo = RepositoryPaths.discover(args.repo_root or Path.cwd()).root
    documents = characterize(repo)
    if args.write:
        write_records(repo)
        print(f"WROTE {len(documents)} UC04-W1A registry documents")
    else:
        print(json.dumps({name: value.get("status") for name, value in documents.items()}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
