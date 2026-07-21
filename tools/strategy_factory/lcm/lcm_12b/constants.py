from __future__ import annotations
PHASE_ID = "LCM-12B"
MASTER_PHASE = "LCM-12"
CLAIM_CEILING = "LCM_12B_REFERENCE_ONLY"
SCHEMA_VERSION = "1.0.0"
OWNER = "ALPHA_LAB_DOCUMENTATION_MIGRATION_OWNER"
REVIEWER = "INDEPENDENT_DOCUMENTATION_REVIEWER"
PRODUCER = "tools.strategy_factory.lcm.lcm_12b.service:LCM12BDocumentationReconciliationService"
GENERATED_TIME_SEMANTICS = "DETERMINISTIC_FROM_BOUND_INPUTS_NO_WALL_CLOCK_IDENTITY"
DOCUMENT_EXTENSIONS = (".md", ".mdx", ".rst", ".txt", ".adoc")
EXCLUDED_PARTS = (".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules", ".venv", "venv", "dist", "build")
