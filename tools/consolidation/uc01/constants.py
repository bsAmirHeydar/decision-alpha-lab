"""UC-01 constants and bounded scope definitions."""
from __future__ import annotations

from pathlib import Path

PROGRAM_ID = "UCPS"
STAGE_ID = "UC-01"
IMPLEMENTATION_VERSION = "1.0.0"
BASELINE_DIRECTORY_NAME = "UC01_BASELINE_V1"
BASELINE_RELATIVE_ROOT = Path("registry/consolidation/uc01/baselines") / BASELINE_DIRECTORY_NAME
RELEASE_RELATIVE_ROOT = Path("releases/unified_consolidation/uc01")

BASELINE_STABILIZATION_REPAIR_PATHS = (
    "lab/11_strategy_factory/python/saed_v4_anytime_valid_online_fdr/cli.py",
    "lab/11_strategy_factory/python/saed_v4_complete_search_exposure_ledger/cli.py",
    "lab/11_strategy_factory/python/saed_v4_decision_focused_treatment_selection/cli.py",
    "lab/11_strategy_factory/python/saed_v4_foundation_model_adapters/cli.py",
    "lab/11_strategy_factory/python/saed_v4_generative_path_stress_lab/cli.py",
    "lab/11_strategy_factory/python/saed_v4_independent_multi_lab_replication/cli.py",
    "lab/11_strategy_factory/python/saed_v4_mechanistic_interpretability/cli.py",
    "lab/11_strategy_factory/python/saed_v4_multimodal_views/cli.py",
    "lab/11_strategy_factory/python/saed_v4_offline_policy_research/cli.py",
    "lab/11_strategy_factory/python/saed_v4_self_supervised_pretraining/serialization.py",
    "tools/strategy_factory/generate_uce_i13_vectors.py",
)

EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".alpha",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    ".idea",
    ".vscode",
}
EXCLUDED_RELATIVE_PREFIXES = {
    BASELINE_RELATIVE_ROOT.as_posix(),
}
TEXT_SUFFIXES = {
    ".py", ".pyi", ".mq5", ".mqh", ".md", ".txt", ".json", ".jsonl",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".csv", ".tsv",
    ".ps1", ".psm1", ".bat", ".cmd", ".sh", ".xml", ".xsd", ".html",
    ".css", ".js", ".jsx", ".ts", ".tsx", ".sql", ".proto", ".canvas",
}
SOURCE_SUFFIXES = {".py", ".pyi", ".mq5", ".mqh", ".ps1", ".psm1", ".sh", ".bat", ".cmd", ".js", ".ts", ".tsx", ".cpp", ".h", ".hpp"}
DOCUMENT_SUFFIXES = {".md", ".rst", ".adoc", ".canvas"}
SCHEMA_SUFFIXES = {".json", ".yaml", ".yml", ".xsd", ".proto"}
ARCHIVE_SUFFIXES = {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz", ".bundle"}
BINARY_SUFFIXES = {".ex5", ".dll", ".so", ".dylib", ".exe", ".bin", ".dat", ".onnx", ".pkl", ".joblib", ".sqlite", ".db"}

CRITICAL_DOMAIN_PATTERNS: dict[str, tuple[str, ...]] = {
    "kernel": ("identity", "lineage", "hash", "canonical", "registry", "state_machine", "authority", "entitlement"),
    "market": ("market", "bar", "tick", "symbol", "session", "calendar", "known_time", "time_kernel", "data_sync"),
    "context": ("context", "occurrence", "detector", "confirmation", "invalidation"),
    "treatment": ("treatment", "setup", "entry", "stop", "target", "management", "abstain"),
    "research": ("research", "feature", "label", "dataset", "train", "model", "experiment", "trial"),
    "evidence": ("evidence", "falsification", "promotion", "rejection", "final_test", "reproduc"),
    "capital": ("capital", "portfolio", "risk", "allocation", "sizing"),
    "runtime": ("runtime", "deployment", "lease", "rollback", "recovery"),
    "execution": ("execution", "broker", "order", "position", "trade", "slippage", "fill"),
    "monitoring": ("monitor", "surveillance", "incident", "drift", "retirement", "health"),
}

KNOWN_TOP_LEVELS = {
    ".github", ".obsidian", "data", "docs", "lab", "licenses", "mql5", "papers",
    "product_lab", "registry", "reports", "research", "tests", "tools", "releases",
    "src", "contexts", "adapters", "contracts", "schemas", "policies", "configs", "ops",
    "products", "examples",
}

PATH_REFERENCE_PREFIXES = (
    "lab/", "tools/", "docs/", "registry/", "mql5/", "research/", "data/",
    "reports/", "product_lab/", "tests/", "releases/", "src/", "contexts/", "adapters/",
    "contracts/", "schemas/", "policies/", "configs/", "ops/", "products/", "examples/",
)

OUTPUT_FILENAMES = (
    "artifact_inventory.jsonl.gz",
    "artifact_inventory_summary.json",
    "python_symbol_inventory.jsonl.gz",
    "python_import_graph.jsonl.gz",
    "python_parse_issues.jsonl.gz",
    "artifact_scan_issues.jsonl.gz",
    "mql5_scan_issues.jsonl.gz",
    "documentation_scan_issues.jsonl.gz",
    "schema_scan_issues.jsonl.gz",
    "path_reference_scan_issues.jsonl.gz",
    "capture_state.json",
    "mql5_symbol_inventory.jsonl.gz",
    "mql5_include_graph.jsonl.gz",
    "mql5_authority_surface.jsonl.gz",
    "documentation_inventory.jsonl.gz",
    "documentation_link_graph.jsonl.gz",
    "documentation_id_collisions.jsonl.gz",
    "schema_inventory.jsonl.gz",
    "path_reference_graph.jsonl.gz",
    "consumer_inventory.jsonl.gz",
    "large_object_inventory.jsonl.gz",
    "git_lfs_inventory.jsonl.gz",
    "critical_logic_inventory.jsonl.gz",
    "behavior_characterization_manifest.json",
    "test_inventory.jsonl.gz",
    "environment_manifest.json",
    "repository_snapshot.json",
    "baseline_manifest.json",
    "preservation_receipt.json",
    "recovery_drill_receipt.json",
    "qualification_receipt.json",
    "no_destructive_change_receipt.json",
    "unresolved_items.jsonl.gz",
    "stage_exit_decision.json",
    "uc02_handoff.json",
    "baseline_output_hashes.sha256",
    "UC01_COMMIT_FILE_INDEX.txt",
)
