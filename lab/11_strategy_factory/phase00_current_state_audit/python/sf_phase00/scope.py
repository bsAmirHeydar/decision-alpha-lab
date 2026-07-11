from __future__ import annotations


SELF_PREFIXES = (
    "lab/11_strategy_factory/phase00_current_state_audit/",
    "lab/11_strategy_factory/implementation_program/phase_status/PHASE_00",
    "docs/strategy_factory_implementation/phase00/",
    "docs/obsidian_deep/00_mocs/STRATEGY_FACTORY_PHASE00_CURRENT_STATE_AUDIT_MOC.md",
)

SELF_ROOT_FILES = {
    "README_STRATEGY_FACTORY_PHASE00_IMPLEMENTATION.md",
    "INSTALL_STRATEGY_FACTORY_PHASE00_IMPLEMENTATION.md",
    "COMMIT_MESSAGE.md",
    "STRATEGY_FACTORY_PHASE00_PATCH_MANIFEST.json",
    "STRATEGY_FACTORY_PHASE00_QA_REPORT.json",
    "STRATEGY_FACTORY_PHASE00_FILE_INDEX.txt",
    "STRATEGY_FACTORY_PHASE00_FILE_HASHES.sha256",
}


def is_phase00_self_path(relative_path: str) -> bool:
    normalized = relative_path.replace("\\", "/")
    return normalized in SELF_ROOT_FILES or any(normalized.startswith(prefix) for prefix in SELF_PREFIXES)
