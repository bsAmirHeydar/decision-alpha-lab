from saed_v4_constitution.canonical import canonical_json, content_hash, stable_id, parse_time

def test_canonical_order_independent():
    assert canonical_json({"b": 1, "a": 2}) == canonical_json({"a": 2, "b": 1})

def test_hash_order_independent():
    assert content_hash({"b": 1, "a": 2}) == content_hash({"a": 2, "b": 1})

def test_stable_id_is_stable():
    assert stable_id("x", {"a": 1}) == stable_id("x", {"a": 1})

def test_stable_id_changes_with_payload():
    assert stable_id("x", {"a": 1}) != stable_id("x", {"a": 2})

def test_parse_time_requires_timezone():
    import pytest
    with pytest.raises(ValueError): parse_time("2026-07-13T00:00:00")

def test_parse_time_accepts_z():
    assert parse_time("2026-07-13T00:00:00Z").tzinfo is not None
