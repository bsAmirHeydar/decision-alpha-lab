from __future__ import annotations

from pathlib import Path

from .models import MigrationAction, ModuleRecord, Severity


MODULE_RULES: tuple[ModuleRecord, ...] = (
    ModuleRecord(
        "MOD-DOC-001", "docs/", "research_governance_and_architecture",
        MigrationAction.REUSE_AS_IS,
        "Core research/execution separation and laboratory governance are compatible with Strategy Factory.",
        Severity.LOW, "repository_docs", "shared_governance",
        ("docs/architecture.md", "docs/laboratory_architecture.md", "docs/research-roadmap.md"),
    ),
    ModuleRecord(
        "MOD-DATA-001", "lab/core/CP0000_market_data/connectors/", "market_data_connector",
        MigrationAction.ADAPT,
        "Reusable MT5 ingestion exists, but timezone, dependency injection, retry, and schema contracts are implicit.",
        Severity.HIGH, "CP0000", "strategy_factory.data_connectors",
        ("MT5Connector.py",),
    ),
    ModuleRecord(
        "MOD-DATA-002", "lab/core/CP0000_market_data/services/", "market_data_service",
        MigrationAction.WRAP,
        "MarketDataEngine has reusable shift-style accessors and cache synchronization; preserve behind a canonical data interface.",
        Severity.MEDIUM, "CP0000", "strategy_factory.market_data",
        ("MarketDataEngine.py",),
    ),
    ModuleRecord(
        "MOD-DATA-003", "lab/core/CP0000_market_data/cache/", "parquet_persistence",
        MigrationAction.ADAPT,
        "Persistence is useful but currently path-coupled and lacks artifact identity, locking, schema version, and atomic writes.",
        Severity.HIGH, "CP0000", "strategy_factory.artifacts",
        ("ParquetStore.py",),
    ),
    ModuleRecord(
        "MOD-ANA-001", "lab/core/CP0001_structural_nodes/detectors/", "structural_node_anatomy",
        MigrationAction.WRAP,
        "L-rule detector is strategy/anatomy knowledge and must remain outside the shared kernel behind an Anatomy Adapter.",
        Severity.MEDIUM, "CP0001", "anatomy_plugins.structural_nodes",
        ("L_Rule.py",),
    ),
    ModuleRecord(
        "MOD-MET-001", "lab/core/CP0001_structural_nodes/metrics/", "structural_node_metric",
        MigrationAction.WRAP,
        "RTV metric is reusable research logic but has custom persistence and interface drift; expose through feature/label plugins.",
        Severity.HIGH, "CP0001", "feature_plugins.structural_nodes",
        ("M0001_relative_territory_volatility.py",),
    ),
    ModuleRecord(
        "MOD-EXP-001", "lab/03_experiments/", "experiment_scaffolding",
        MigrationAction.MIGRATE,
        "Experiment directories are mostly empty placeholders; migrate to manifest-driven runs and immutable artifacts.",
        Severity.MEDIUM, "legacy_lab", "strategy_factory.experiments",
        ("EXP0000_sample", "EXP0001_structural_highs_lows_importance"),
    ),
    ModuleRecord(
        "MOD-VAL-001", "lab/05_validation/", "validation_scaffolding",
        MigrationAction.MIGRATE,
        "Validation shell has no implementation; replace with shared purged walk-forward and anti-overfit modules.",
        Severity.HIGH, "legacy_lab", "strategy_factory.validation",
        ("VAL001",),
    ),
    ModuleRecord(
        "MOD-EXE-001", "lab/09_execution/", "execution_boundary_scaffolding",
        MigrationAction.ADAPT,
        "Execution boundary exists only as empty folders; retain ownership boundary and implement later under explicit authority gates.",
        Severity.HIGH, "legacy_lab", "strategy_factory.execution",
        ("bridge", "logging", "mql5"),
    ),
    ModuleRecord(
        "MOD-REG-001", "registry/", "research_registry",
        MigrationAction.ADAPT,
        "Registry files are empty and unversioned; replace with validated machine-readable registries while preserving public location.",
        Severity.MEDIUM, "repository_registry", "strategy_factory.registry",
        ("experiments.yaml", "hypotheses.yaml", "signals.yaml", "validations.yaml"),
    ),
    ModuleRecord(
        "MOD-CACHE-001", "lab/cache_data/", "market_data_cache",
        MigrationAction.MIGRATE,
        "Generated market data is committed inside source tree; move under versioned artifact/data storage with provenance.",
        Severity.HIGH, "legacy_cache", "strategy_factory.artifacts",
        ("GOLD", "#US30"),
    ),
    ModuleRecord(
        "MOD-CACHE-002", "lab/cache_nodes/", "anatomy_cache",
        MigrationAction.MIGRATE,
        "Generated node artifacts require source hash, schema version, producer version, and atomic replacement.",
        Severity.HIGH, "legacy_cache", "strategy_factory.artifacts",
        ("L_rule",),
    ),
    ModuleRecord(
        "MOD-CACHE-003", "lab/cache_metrics/", "metric_cache",
        MigrationAction.MIGRATE,
        "Generated metric artifacts use a second independent path convention and no canonical run identity.",
        Severity.HIGH, "legacy_cache", "strategy_factory.artifacts",
        ("M0001_relative_territory_volatility",),
    ),
    ModuleRecord(
        "MOD-TEST-001", "lab/core/", "legacy_test_and_demo_scripts",
        MigrationAction.MIGRATE,
        "Manual test scripts depend on live MT5 and are mixed with source; move unit tests to deterministic fixtures and mark integration tests.",
        Severity.HIGH, "core_modules", "strategy_factory.tests",
        ("test.py", "test_L_Rule.py", "test_M0001_relative_territory_volatility.py"),
    ),
    ModuleRecord(
        "MOD-EPH-001", "**/__pycache__", "compiled_python_artifacts",
        MigrationAction.DELETE_LATER,
        "Compiled bytecode is ephemeral and must not be version-controlled.",
        Severity.LOW, "repository", "ignored_artifacts",
        ("*.pyc",),
    ),
    ModuleRecord(
        "MOD-EPH-002", ".pytest_cache/", "pytest_cache",
        MigrationAction.DELETE_LATER,
        "Test cache is ephemeral and must be ignored.",
        Severity.LOW, "repository", "ignored_artifacts",
        (".pytest_cache",),
    ),
)


def classify_modules(repo_root: Path) -> list[ModuleRecord]:
    del repo_root  # rules are deliberate and stable for this phase snapshot
    return list(MODULE_RULES)
