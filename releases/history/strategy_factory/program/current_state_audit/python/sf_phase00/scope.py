from __future__ import annotations


SELF_PREFIXES = (
    "lab/11_strategy_factory/phase00_current_state_audit/",
    "lab/11_strategy_factory/implementation_program/phase_status/PHASE_00",
    "docs/strategy_factory_implementation/phase00/",
    "docs/obsidian_deep/00_mocs/STRATEGY_FACTORY_PHASE00_CURRENT_STATE_AUDIT_MOC.md",
)

SELF_ROOT_FILES = {
    "releases/history/strategy_factory/readmes/README_STRATEGY_FACTORY_PHASE00_IMPLEMENTATION.md",
    "releases/history/strategy_factory/installers/INSTALL_STRATEGY_FACTORY_PHASE00_IMPLEMENTATION.md",
    "COMMIT_MESSAGE.md",
    "releases/history/strategy_factory/manifests/STRATEGY_FACTORY_PHASE00_PATCH_MANIFEST.json",
    "releases/history/strategy_factory/reports/STRATEGY_FACTORY_PHASE00_QA_REPORT.json",
    "releases/history/strategy_factory/indexes/STRATEGY_FACTORY_PHASE00_FILE_INDEX.txt",
    "releases/history/strategy_factory/hashes/STRATEGY_FACTORY_PHASE00_FILE_HASHES.sha256",
}


def is_phase00_self_path(relative_path: str) -> bool:
    normalized = relative_path.replace("\\", "/")
    return normalized in SELF_ROOT_FILES or any(normalized.startswith(prefix) for prefix in SELF_PREFIXES)
