from fp_i00_governance.scanner import scan_dependencies, scan_tests, scan_ownership
from conftest import REPO_ROOT, load_policy


def test_dependency_inventory_is_complete_and_hash_pinned():
    records = scan_dependencies(REPO_ROOT, load_policy())
    assert len(records) == 19
    assert len({record.dependency_id for record in records}) == 19
    assert all(record.file_count > 0 for record in records)
    assert all(len(record.aggregate_sha256) == 64 for record in records)
    assert all(record.mutation_allowed is False for record in records)


def test_previous_context_tests_are_discoverable():
    records = scan_tests(REPO_ROOT, load_policy())
    assert len(records) == 12
    assert all(record.exists for record in records)
    assert {record.context_id for record in records} == {"EXP0017", "EXP0018"}


def test_ownership_is_phase_local_and_rollback_safe():
    records = scan_ownership(load_policy())
    assert len(records) == 4
    assert all(record.owner_phase == "FP-I00" for record in records)
    assert all(record.rollback_policy == "REMOVE_ONLY_INDEXED_FILES" for record in records)
