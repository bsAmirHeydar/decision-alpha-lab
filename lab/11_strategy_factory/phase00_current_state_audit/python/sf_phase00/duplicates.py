from __future__ import annotations

from pathlib import Path

from .models import DuplicateCapability, Severity
from .scope import is_phase00_self_path


def detect_duplicate_capabilities(repo_root: Path) -> list[DuplicateCapability]:
    candidates: list[DuplicateCapability] = []

    persistence = [
        "lab/core/CP0000_market_data/cache/ParquetStore.py",
        "lab/core/CP0001_structural_nodes/detectors/L_Rule.py",
        "lab/core/CP0001_structural_nodes/metrics/M0001_relative_territory_volatility.py",
    ]
    existing = tuple(path for path in persistence if (repo_root / path).exists())
    if len(existing) > 1:
        candidates.append(
            DuplicateCapability(
                capability="parquet_artifact_persistence",
                implementations=existing,
                overlap_basis="Independent path construction, directory creation, read/write, and cache invalidation.",
                migration_decision="Create one versioned ArtifactStore; retain strategy-specific serializers as plugins.",
                severity=Severity.HIGH,
            )
        )

    normalization = tuple(
        path for path in (
            "lab/core/CP0000_market_data/connectors/MT5Connector.py",
            "lab/core/CP0000_market_data/services/MarketDataEngine.py",
        ) if (repo_root / path).exists()
    )
    if len(normalization) > 1:
        candidates.append(
            DuplicateCapability(
                capability="market_bar_normalization",
                implementations=normalization,
                overlap_basis="Both layers perform duplicate removal, sorting, index reset, and time normalization.",
                migration_decision="Define one canonical BarFrame contract; connector maps vendor data, service validates once.",
                severity=Severity.MEDIUM,
            )
        )

    manual_tests = tuple(
        path.relative_to(repo_root).as_posix()
        for path in sorted(repo_root.rglob("test*.py"))
        if ".git" not in path.parts and "__pycache__" not in path.parts
        and not is_phase00_self_path(path.relative_to(repo_root).as_posix())
    )
    if len(manual_tests) > 1:
        candidates.append(
            DuplicateCapability(
                capability="manual_live_test_harness",
                implementations=manual_tests,
                overlap_basis="Multiple scripts create MT5 connectors, fetch data, print diagnostics, and require a live terminal.",
                migration_decision="Replace with deterministic unit fixtures plus explicitly marked MT5 integration tests.",
                severity=Severity.HIGH,
            )
        )

    return candidates
