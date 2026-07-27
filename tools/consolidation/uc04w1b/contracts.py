from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from tools.consolidation.uc04w1.characterize import (
    CANDIDATE_ID,
    ENGINE_ID,
    FIXTURE_ROOT,
    MEMBERS,
    PROPOSED_PRODUCTION_TARGET,
    characterize,
    fixture_rows,
)

STAGE_ID = "UC04-W1B-Q"
PROGRAM_ID = "UCPS"
REGISTRY_ROOT = Path("registry/consolidation/uc04/w1b")
SCHEMA_ROOT = Path("schemas/consolidation/uc04/w1b")
RELEASE_ROOT = Path("releases/unified_consolidation/uc04/w1b")
DOC_ROOT = Path(
    "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/"
    "15_UC04_W1B_NATIVE_QUALIFICATION"
)
EVIDENCE_BOUNDARY = Path(".alpha/runs/uc04w1b/native_qualification")
CUTOVER_BOUNDARY = Path(".alpha/runs/uc04w1b/cutover_candidates")
RUNTIME_OUTPUT_RELATIVE = Path(
    "AlphaLab/UC04W1B/UC04W1B_DeterministicDateTimeFormatNativeRunner.csv"
)
NATIVE_RUNNER_SOURCE = Path(
    "mql5/Tests/Scripts/UC04/UC04W1B_DeterministicDateTimeFormatNativeRunner.mq5"
)
REFERENCE_HEADER = Path(
    "mql5/Tests/Include/AlphaLab/UC04W1/AL_UC04W1_ReferenceDateTimeFormat.mqh"
)
PRODUCTION_INCLUDE = PROPOSED_PRODUCTION_TARGET
PRODUCTION_INCLUDE_DIRECTIVE = (
    f"#include <AlphaLab/ContextOS/Shared/{ENGINE_ID}/AL_DeterministicDateTimeFormat.mqh>"
)
CANONICAL_FUNCTION_NAME = "AL_DeterministicDateTimeFormat"

BASELINE_COMPILE_TARGETS: tuple[str, ...] = tuple(path for path, _, _ in MEMBERS) + (
    "mql5/Tests/Experts/UC04/UC04W1_DeterministicDateTimeFormatSelfTest.mq5",
    NATIVE_RUNNER_SOURCE.as_posix(),
)

AUTHORITY_FIELDS = (
    "implementation_authority",
    "consumer_cutover_authority",
    "deletion_authority",
    "runtime_authority",
    "order_authority",
    "capital_authority",
)


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_digest(document: dict[str, Any], field: str = "document_digest") -> str:
    material = {key: value for key, value in document.items() if key != field}
    return sha256_bytes(
        json.dumps(
            material,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def with_digest(document: dict[str, Any], field: str = "document_digest") -> dict[str, Any]:
    result = dict(document)
    result[field] = canonical_digest(result, field)
    return result


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def current_candidate_inventory(repo: Path) -> dict[str, Any]:
    return characterize(repo)["candidate_inventory.json"]


def expected_fixture_rows() -> list[dict[str, Any]]:
    return fixture_rows()


def authority_false_map() -> dict[str, bool]:
    return {field: False for field in AUTHORITY_FIELDS}
