from __future__ import annotations
PHASE_ID = "LCM-10A"
MASTER_PHASE = "LCM-10"
SCHEMA_VERSION = "1.0.0"
CLAIM_CEILING = "LCM_10A_REFERENCE_ONLY"
PRODUCER = "tools.strategy_factory.lcm.lcm_10a.service:LCM10ATreatmentExecutionInventoryService"
TIME_SEMANTICS = "DETERMINISTIC_FROM_BOUND_INPUTS_NO_WALL_CLOCK_IDENTITY"
UPSTREAM_HANDOFF_DIGEST = "sha256:104e4567686811724302be71f49f08f382196bed235c1fd969ebec1e58cd67ac"
UPSTREAM_SETUP_ROOT = "registry/legacy_context_migration/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9"
LCM01_SURVEY_ROOT = "registry/legacy_context_migration/surveys/SURVEY_D4EC5C533F886BC439DAEEBDE51FA080"
LCM02_CLASSIFICATION_ROOT = "registry/legacy_context_migration/classifications/CLASSIFICATION_B23DFF50BC28E90A66ADA125A850234B"
LCM07_SHARED_ENGINE_ROOT = "registry/legacy_context_migration/shared_engines/SHAREDENG_F1EFFB190FA1F0AE0D31369EEDB82A3A"
INVENTORY_ID = "TREATINV_98D30D63F6B6CA7BEA4ABAC517956B02"
INVENTORY_ROOT = f"registry/legacy_context_migration/treatment_execution_inventories/{INVENTORY_ID}"
SOURCE_ROOTS = ("mql5", "lab", "tools", "product_lab", "research", "reports", "tests", "docs")
SOURCE_SUFFIXES = (".mq5", ".mqh", ".py", ".set", ".toml", ".ini")
EXCLUDED_PARTS = (".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules", "venv", ".venv")
GENERATED_EXCLUDED_PREFIXES = (
    "registry/legacy_context_migration/treatment_execution_inventories/",
    "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/11_PHASE_DELIVERIES/LCM_10A/",
    "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/12_ATOMIC_CONCEPTS/LCM_10A/",
    "lab/11_strategy_factory/migration/tests_lcm_10a/",
    "tools/strategy_factory/lcm/lcm_10a/",
)
AUTHORITY_FALSE_FIELDS = (
    "promotion_authority_created", "runtime_authority_created", "live_order_authority_created",
    "capital_authority_created", "consumer_cutover_allowed", "source_move_allowed", "source_delete_allowed",
)
