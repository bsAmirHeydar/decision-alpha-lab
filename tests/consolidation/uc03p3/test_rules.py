from pathlib import Path

from tools.consolidation.uc03p3.apply import (
    DOC_DIRECTORY_RULES,
    DOC_FILE_RULES,
    LEGACY_IMPORT_RULES,
    REGISTRY_DIRECTORY_RULES,
)


def test_relocation_destinations_are_unique() -> None:
    destinations = [dst for _, dst in (*DOC_DIRECTORY_RULES, *DOC_FILE_RULES, *REGISTRY_DIRECTORY_RULES)]
    assert len(destinations) == len(set(destinations))


def test_documentation_rules_use_canonical_boundaries() -> None:
    allowed = ("docs/architecture/", "docs/standards/", "docs/operations/", "docs/contexts/", "docs/history/", "docs/README.md")
    assert all(destination.startswith(allowed) for _, destination in (*DOC_DIRECTORY_RULES, *DOC_FILE_RULES))


def test_registry_history_rules_do_not_move_consolidation_authority() -> None:
    sources = {source for source, _ in REGISTRY_DIRECTORY_RULES}
    assert "registry/consolidation" not in sources
    assert all(destination.startswith("registry/history/") for _, destination in REGISTRY_DIRECTORY_RULES)


def test_import_rules_leave_no_alpha_lab_nested_product() -> None:
    assert all("alpha_lab" not in destination for _, destination in LEGACY_IMPORT_RULES)
