#!/usr/bin/env python3
"""Validate UCE-I01 delivery structure, schemas, documentation, and evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

REQUIRED_HEADERS = {
    "UCE03_ContractVersion.mqh",
    "UCE03_Enums.mqh",
    "UCE03_CanonicalCodec.mqh",
    "UCE03_Hash.mqh",
    "UCE03_Identity.mqh",
    "UCE03_KnownTime.mqh",
    "UCE03_Schema.mqh",
    "UCE03_SchemaRegistry.mqh",
    "UCE03_Migration.mqh",
    "UCE03_Capability.mqh",
    "UCE03_Compatibility.mqh",
    "UCE03_Telemetry.mqh",
    "UCE03_LegacyBridge.mqh",
    "UCE03_Release.mqh",
    "UCE03_AllContracts.mqh",
}
REQUIRED_SCHEMA_NAMES = {
    "identity_key",
    "known_time_chain",
    "schema_descriptor",
    "migration_edge",
    "migration_evidence",
    "capability_descriptor",
    "compatibility_request",
    "compatibility_decision",
    "legacy_bridge_record",
    "contract_release_manifest",
}
PERSIAN_ARABIC = re.compile(r"[\u0600-\u06ff]")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    headers = root / "mql5/Include/AlphaLab/StrategyFactory/Contracts"
    found_headers = {path.name for path in headers.glob("UCE03_*.mqh")}
    for name in sorted(REQUIRED_HEADERS - found_headers):
        errors.append(f"missing MQL5 header: {name}")

    schemas = root / "lab/11_strategy_factory/schemas/v3"
    for name in sorted(REQUIRED_SCHEMA_NAMES):
        path = schemas / f"{name}.schema.json"
        if not path.is_file():
            errors.append(f"missing schema: {path.relative_to(root)}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - diagnostic path
            errors.append(f"invalid JSON schema {path.name}: {exc}")
            continue
        if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"wrong draft in {path.name}")
        if data.get("additionalProperties") is not False:
            errors.append(f"open top-level object in {path.name}")

    docs = root / "docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i01"
    notes = list(docs.rglob("*.md"))
    if len(notes) < 29:
        errors.append(f"expected at least 29 English phase notes including ADRs, found {len(notes)}")
    for path in notes:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"missing frontmatter: {path.relative_to(root)}")
        if PERSIAN_ARABIC.search(text):
            errors.append(f"non-English script in phase documentation: {path.relative_to(root)}")

    for rel in (
        "lab/11_strategy_factory/test_vectors/v3/uce_i01_cross_language_vectors.json",
        "lab/11_strategy_factory/test_vectors/v3/uce_i01_negative_vectors.json",
        "lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I01.json",
        "lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I01_HANDOFF_TO_UCE_I02.json",
        "UCEE_I01_PATCH_MANIFEST.json",
        "UCEE_I01_QA_REPORT.json",
        "UCEE_I01_FILE_INDEX.txt",
        "UCEE_I01_FILE_HASHES.sha256",
    ):
        if not (root / rel).is_file():
            errors.append(f"missing delivery artifact: {rel}")

    hash_file = root / "UCEE_I01_FILE_HASHES.sha256"
    if hash_file.is_file():
        for line_number, line in enumerate(hash_file.read_text(encoding="utf-8").splitlines(), 1):
            parts = line.split("  ", 1)
            if len(parts) != 2:
                errors.append(f"invalid hash line {line_number}")
                continue
            expected_digest, digest_rel = parts
            path = root / digest_rel
            if not path.is_file():
                errors.append(f"hash target missing: {digest_rel}")
                continue
            actual_digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_digest != expected_digest:
                errors.append(f"hash mismatch: {digest_rel}")

    status_path = root / "lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/phase_status/UCE_I01.json"
    if status_path.is_file():
        status = json.loads(status_path.read_text(encoding="utf-8"))
        if status.get("contract_release") != "3.0.0":
            errors.append("phase status has wrong contract release")
        if status.get("next_phase") != "UCE-I02":
            errors.append("phase status has wrong handoff")

    if errors:
        print("UCE-I01 delivery validation: FAIL")
        for error in errors:
            print("ERROR:", error)
        return 1

    print(
        "UCE-I01 delivery validation: PASS "
        f"({len(found_headers)} headers, {len(notes)} English notes, {len(REQUIRED_SCHEMA_NAMES)} schemas)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
