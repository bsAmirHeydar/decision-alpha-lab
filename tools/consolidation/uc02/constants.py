"""Constants for UC-02 standards and authority freeze."""
from __future__ import annotations

from pathlib import Path

PROGRAM_ID = "UCPS"
STAGE_ID = "UC-02"
VERSION = "1.0.0"
UC01_BASELINE_ROOT = Path("registry/consolidation/uc01/baselines/UC01_BASELINE_V1")
AUTHORITY_PACKAGE_NAME = "UC02_AUTHORITY_V1"
AUTHORITY_ROOT = Path("registry/consolidation/uc02/authority_freezes") / AUTHORITY_PACKAGE_NAME
RELEASE_ROOT = Path("releases/unified_consolidation/uc02")
POLICY_ROOT = Path("policies/platform")
CONTRACT_ROOT = Path("contracts/platform")
SCHEMA_ROOT = Path("schemas/consolidation/uc02")

STATIC_POLICY_FILES = (
    POLICY_ROOT / "architecture_constitution.yaml",
    POLICY_ROOT / "naming_standard.yaml",
    POLICY_ROOT / "dependency_rules.yaml",
    POLICY_ROOT / "documentation_authority.yaml",
    POLICY_ROOT / "deprecation_policy.yaml",
    POLICY_ROOT / "root_and_package_guard.yaml",
    POLICY_ROOT / "artifact_disposition_standard.yaml",
)
STATIC_CONTRACT_FILES = (
    CONTRACT_ROOT / "canonical_topology.yaml",
    CONTRACT_ROOT / "artifact_identity_standard.yaml",
    CONTRACT_ROOT / "capability_ownership.yaml",
    CONTRACT_ROOT / "system_disposition.yaml",
    CONTRACT_ROOT / "extension_standard.yaml",
)

PLANNING_DISPOSITIONS = {
    "KEEP_CANONICAL",
    "MOVE",
    "MERGE",
    "GENERATE",
    "EXTERNALIZE",
    "DELETE",
}

AUTHORITY_DOMAINS = (
    "kernel",
    "market",
    "context",
    "treatment",
    "research",
    "evidence",
    "policy",
    "capital",
    "portfolio",
    "runtime",
    "execution",
    "monitoring",
    "memory",
    "adapters",
    "contracts",
    "schemas",
    "registry",
    "configuration",
    "mql5",
    "testing",
    "documentation",
    "engineering",
    "operations",
    "products",
    "examples",
    "release_history",
    "historical_archive",
)

CANONICAL_ROOTS = (
    "src/engine",
    "contexts",
    "adapters",
    "contracts",
    "schemas",
    "policies",
    "registry",
    "configs",
    "mql5",
    "tests",
    "docs",
    "ops",
    "tools",
    "products",
    "examples",
    "releases",
)

DYNAMIC_OUTPUTS = (
    "authority_manifest.json",
    "repository_authority_ledger.jsonl.gz",
    "package_authority_ledger.jsonl.gz",
    "capability_authority_ledger.jsonl.gz",
    "documentation_authority_ledger.jsonl.gz",
    "system_disposition_ledger.jsonl.gz",
    "root_grandfather_baseline.json",
    "package_grandfather_baseline.json",
    "wave_portfolio.json",
    "authority_coverage_report.json",
    "guard_qualification_receipt.json",
    "qualification_receipt.json",
    "stage_exit_decision.json",
    "uc03_handoff.json",
    "unresolved_authority_items.jsonl.gz",
    "authority_output_hashes.sha256",
    "UC02_COMMIT_FILE_INDEX.txt",
)

FORBIDDEN_AUTHORITY_FLAGS = (
    "destructive_authority",
    "runtime_authority",
    "order_authority",
    "broker_authority",
    "capital_authority",
)
