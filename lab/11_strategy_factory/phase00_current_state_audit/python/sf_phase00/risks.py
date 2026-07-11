from __future__ import annotations

from pathlib import Path

from .models import AuthorityFinding, MigrationRisk, Severity


def build_risk_register(repo_root: Path, authority: list[AuthorityFinding], pytest_passed: bool) -> list[MigrationRisk]:
    risks: list[MigrationRisk] = []
    if authority:
        risks.append(MigrationRisk(
            "RISK-000", "Unidentified live execution authority", "capital_safety", "possible", "critical",
            Severity.CRITICAL,
            tuple(f"{item.path}:{item.line}:{item.token}" for item in authority),
            "Quarantine execution call sites and require an authority manifest before Phase 18.", "PHASE_00",
        ))
    else:
        risks.append(MigrationRisk(
            "RISK-001", "No live order authority present in audited snapshot", "capital_safety", "unlikely", "low",
            Severity.INFO, ("No OrderSend, OrderCheck, CTrade, or mt5.order_send call sites found.",),
            "Preserve the no-send boundary through Phase 18 and rescan every release.", "PHASE_18", "CONTROLLED",
        ))

    if not pytest_passed:
        risks.append(MigrationRisk(
            "RISK-002", "Clean-checkout test collection fails", "testing", "certain", "high",
            Severity.HIGH,
            ("pytest collection fails with ModuleNotFoundError: No module named 'lab'.",),
            "Create an installable package boundary or test bootstrap in Phase 02; separate live MT5 integration tests.", "PHASE_02",
        ))

    risks.extend([
        MigrationRisk(
            "RISK-003", "Generated market and metric artifacts are committed as source", "reproducibility", "certain", "high",
            Severity.HIGH,
            ("lab/cache_data", "lab/cache_nodes", "lab/cache_metrics"),
            "Move to versioned artifact storage with producer/schema/source hashes and retention policy.", "PHASE_05",
        ),
        MigrationRisk(
            "RISK-004", "Three independent persistence conventions", "duplication", "certain", "high",
            Severity.HIGH,
            ("ParquetStore", "LRuleNodeDetector._save_nodes", "M0001RTV._save_cache"),
            "Consolidate through one ArtifactStore contract; preserve domain serializers as adapters.", "PHASE_05",
        ),
        MigrationRisk(
            "RISK-005", "Terminal-local and naive timestamps", "causality", "likely", "critical",
            Severity.CRITICAL,
            ("MT5Connector assigns timezone='terminal' without canonical UTC conversion.", "datetime.now() used for synchronization."),
            "Introduce canonical MarketTimestamp and source timezone/DST contract before event generation.", "PHASE_07",
        ),
        MigrationRisk(
            "RISK-006", "Metric interface drift between implementation and test", "contract_drift", "certain", "high",
            Severity.HIGH,
            ("M0001RTV requires detector in constructor; legacy test passes L keyword.",),
            "Freeze constructor and dependency contracts in Phase 01; add contract tests.", "PHASE_01",
        ),
        MigrationRisk(
            "RISK-007", "Registries and production/validation shells are empty", "governance", "certain", "medium",
            Severity.MEDIUM,
            ("registry/*.yaml are zero bytes.", "validation/production/monitoring directories contain placeholders."),
            "Replace placeholders with schema-validated registries and generated run artifacts.", "PHASE_04",
        ),
        MigrationRisk(
            "RISK-008", "Tests depend on a live MT5 terminal and external package", "test_isolation", "certain", "high",
            Severity.HIGH,
            ("MetaTrader5 imported at module import time.", "Legacy tests call connector.connect()."),
            "Move vendor import behind adapter boundary; add fake connector and deterministic fixtures.", "PHASE_06",
        ),
        MigrationRisk(
            "RISK-009", "Repository snapshot lacks EXP0017 and NDS programs referenced by roadmap", "scope_alignment", "certain", "high",
            Severity.HIGH,
            ("Audited archive contains EXP0000 and EXP0001 only.",),
            "Use this snapshot as foundation audit only; provide the current full repository before Phase 20/21 pilot migration.", "PHASE_20",
        ),
        MigrationRisk(
            "RISK-010", "Python bytecode and pytest cache are tracked in snapshot", "repository_hygiene", "certain", "low",
            Severity.LOW,
            ("__pycache__ directories", ".pytest_cache"),
            "Add ignore rules and remove generated runtime files in Phase 02.", "PHASE_02",
        ),
    ])
    return risks
