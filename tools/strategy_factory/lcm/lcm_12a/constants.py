from __future__ import annotations
PHASE_ID = 'LCM-12A'
MASTER_PHASE = 'LCM-12'
CLAIM_CEILING = 'LCM_12A_REFERENCE_ONLY'
SCHEMA_VERSION = '1.0.0'
OWNER = 'ALPHA_LAB_DOCUMENTATION_MIGRATION_OWNER'
REVIEWER = 'INDEPENDENT_DOCUMENTATION_REVIEWER'
PRODUCER = 'tools.strategy_factory.lcm.lcm_12a.service:LCM12ADocumentationAuthorityService'
GENERATED_TIME_SEMANTICS = 'DETERMINISTIC_FROM_BOUND_INPUTS_NO_WALL_CLOCK_IDENTITY'
DOCUMENT_EXTENSIONS = (".md", ".mdx", ".rst", ".txt", ".adoc")
REFERENCE_SCAN_EXTENSIONS = DOCUMENT_EXTENSIONS + (".py", ".ps1", ".bat", ".cmd", ".sh", ".mq5", ".mqh", ".cpp", ".c", ".h", ".hpp", ".js", ".jsx", ".ts", ".tsx", ".yaml", ".yml", ".toml")
EXCLUDED_PARTS = (".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules", ".venv", "venv", "dist", "build")
SELF_EXCLUDED_PREFIXES = (
    "registry/legacy_context_migration/documentation_authority_mappings/",
    "registry/legacy_context_migration/lcm_12a/",
    "tools/strategy_factory/lcm/lcm_12a/",
    "lab/11_strategy_factory/migration/tests_lcm_12a/",
)
SELF_EXCLUDED_ROOT_PREFIXES = ("LCM_12A_", "README_ALPHA_LAB_LCM_12A", "INSTALL_ALPHA_LAB_LCM_12A", "ROLLBACK_ALPHA_LAB_LCM_12A", "COMMIT_MESSAGE_LCM_12A")
AUTHORITY_CLASSES = ("CANONICAL", "SUPPORTING_EVIDENCE", "GENERATED_PROJECTION", "SUPERSEDED", "DUPLICATE", "CONTRADICTORY", "ARCHIVE_ONLY", "UNKNOWN")
FORBIDDEN_MUTATION_ACTIONS = ("MOVE", "DELETE", "RENAME", "RELOCATE", "CONTENT_REWRITE")
