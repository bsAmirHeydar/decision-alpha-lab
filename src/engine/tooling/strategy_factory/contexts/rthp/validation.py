from __future__ import annotations

from pathlib import Path

import yaml

REQUIRED = [
    "context_manifest.yaml",
    "owners.yaml",
    "doctrine/context_doctrine.md",
    "doctrine/glossary.yaml",
    "contracts/scope.yaml",
    "contracts/ontology.yaml",
    "contracts/causal_clock.yaml",
    "contracts/data_contract.yaml",
    "contracts/state_machine.yaml",
    "contracts/occurrence_contract.yaml",
    "contracts/treatment_envelope.yaml",
    "contracts/acceptance_gates.yaml",
    "security/security_profile.yaml",
    "fixtures/example_catalog.yaml",
]


def validate_package(root: Path) -> dict:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append("MISSING:" + relative)

    if errors:
        return {"passed": False, "errors": errors}

    manifest = yaml.safe_load((root / "context_manifest.yaml").read_text(encoding="utf-8"))
    if manifest.get("status") != "SEMANTICALLY_VALIDATED":
        errors.append("STATUS")

    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".yaml", ".md", ".json"}
    )
    for forbidden in ["DIRECT_ORDER_SEND: true", "live_order_submission_allowed: true"]:
        if forbidden in text:
            errors.append("AUTHORITY:" + forbidden)

    return {
        "passed": not errors,
        "errors": errors,
        "context_id": manifest.get("context_id"),
    }
