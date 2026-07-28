from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from tools.consolidation.uc04w1.characterize import CANDIDATE_ID, ENGINE_ID
from tools.consolidation.uc04w1b.contracts import BASELINE_COMPILE_TARGETS

PROGRAM_ID = "UCPS"
STAGE_ID = "UC04-W1B-N1"
REGISTRY_ROOT = Path("registry/consolidation/uc04/w1bn1")
SCHEMA_ROOT = Path("schemas/consolidation/uc04/w1bn1")
RELEASE_ROOT = Path("releases/unified_consolidation/uc04/w1bn1")
DOC_ROOT = Path(
    "docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/"
    "18_UC04_W1B_NATIVE_HOST_HARDENING"
)
RUNNER = Path(
    "tools/consolidation/uc04w1bn1/Invoke-UC04W1BNativeHostQualification.ps1"
)
EVIDENCE_EXPORTER = Path("tools/consolidation/uc04w1bn1/evidence_export.py")
LOCAL_RUN_BOUNDARY = "%LOCALAPPDATA%/AlphaLab/runs/uc04w1b/native_host_qualification"

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
    payload = json.dumps(
        material,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(payload)


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
