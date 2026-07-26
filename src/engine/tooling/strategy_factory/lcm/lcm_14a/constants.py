from __future__ import annotations

PHASE_ID = "LCM-14A"
MASTER_PHASE = "LCM-14"
CLAIM_CEILING = "LCM_14A_REFERENCE_ONLY"
SCHEMA_VERSION = "1.0.0"
PRODUCER = "src.engine.tooling.strategy_factory.lcm.lcm_14a.service:LCM14ADeprecationRedirectService"
OWNER = "ALPHA_LAB_MIGRATION_OWNER"
REVIEWER = "INDEPENDENT_MIGRATION_REVIEWER"
GENERATED_TIME_SEMANTICS = "DETERMINISTIC_FROM_BOUND_INPUTS_NO_WALL_CLOCK_IDENTITY"
UPSTREAM_CLOSURE_ROOT = "registry/history/lcm/cutover_closures/CUTOVERCLOSE_0E477DA8D23F1B8DEB35DDD90B925F4F"
UPSTREAM_CUTOVER_ROOT = "registry/history/lcm/consumer_wave_cutovers/CUTOVER_E38BEC955210CE172483EE47AA2D9E8C"
DOMAINS = ("CONTEXT", "DOCUMENTATION", "TREATMENT", "VISUAL")
DEPRECATION_STATES = (
    "DEPRECATED_REDIRECT_ACTIVE",
    "DEPRECATED_COMPATIBILITY_ACTIVE_REFERENCE_ONLY",
)
REDIRECT_MODES = (
    "EXISTING_DOCUMENTATION_REDIRECT_ACTIVE",
    "REFERENCE_LOCATOR_REDIRECT_REGISTERED",
)
REFERENCE_CLASSES = (
    "LEGACY_DEFINITION_PATH",
    "LEGACY_REDIRECT_PATH",
    "ACTIVE_CODE_REFERENCE",
    "ACTIVE_CONFIGURATION_REFERENCE",
    "TEST_DISCOVERY_OR_REFERENCE",
    "DOCUMENTATION_REFERENCE",
    "RETAINED_MIGRATION_EVIDENCE",
    "RETAINED_MIGRATION_DOCTRINE",
    "UNKNOWN_REFERENCE_SCOPE",
)
BLOCKING_CLASSES = frozenset({
    "ACTIVE_CODE_REFERENCE",
    "ACTIVE_CONFIGURATION_REFERENCE",
    "TEST_DISCOVERY_OR_REFERENCE",
    "UNKNOWN_REFERENCE_SCOPE",
})
TEXT_SUFFIXES = frozenset({
    ".py", ".pyi", ".mq5", ".mqh", ".cpp", ".cc", ".c", ".h", ".hpp",
    ".ps1", ".bat", ".cmd", ".sh", ".yaml", ".yml", ".json", ".jsonl",
    ".toml", ".ini", ".cfg", ".set", ".csv", ".tsv", ".md", ".txt",
    ".xml", ".html", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs",
})
ACTIVE_ROOTS = ("lab", "mql5", "tools", "docs", ".github", "config", "configs", "presets")
GENERATED_SCAN_ROOTS = (
    "registry/history/lcm/consumer_wave_cutovers",
    "registry/history/lcm/cutover_closures",
    "registry/history/lcm/dual_run_evidence",
    "registry/history/lcm/documentation_reconciliations",
    "registry/history/lcm/treatment_package_migrations",
    "registry/history/lcm/visualizer_migrations",
)
