"""Closed migration policy for phase-zero contracts."""
from __future__ import annotations

from copy import deepcopy

from .errors import ContractError

CURRENT_VERSION = "4.0.0"


def migrate_contract(document: dict) -> dict:
    version = document.get("schema_version")
    if version == CURRENT_VERSION:
        return deepcopy(document)
    if version == "3.0.0" and document.get("contract_type") == "research_constitution":
        migrated = deepcopy(document)
        migrated["schema_version"] = CURRENT_VERSION
        migrated.setdefault("known_time_required", True)
        migrated.setdefault("complete_exposure_accounting", True)
        migrated.setdefault("limitations", ["Migrated from SAED V3; requires independent review."])
        return migrated
    raise ContractError(f"unsupported constitutional contract version: {version!r}")
