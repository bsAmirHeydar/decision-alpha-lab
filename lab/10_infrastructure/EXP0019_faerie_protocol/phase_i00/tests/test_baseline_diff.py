from fp_i00_governance.baseline_diff import semantic_diff


def test_semantic_diff_identifies_exact_path():
    changes = semantic_diff({"a": {"b": 1}, "x": 2}, {"a": {"b": 3}, "x": 2})
    assert changes == [{"path": "a.b", "before": 1, "after": 3}]


def test_semantic_diff_can_ignore_source_control():
    left = {"source_control": {"branch": "a"}, "policy": 1}
    right = {"source_control": {"branch": "b"}, "policy": 1}
    assert semantic_diff(left, right, ("source_control",)) == []
