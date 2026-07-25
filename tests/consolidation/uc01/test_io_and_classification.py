from pathlib import Path

from tools.consolidation.uc01.classification import (
    classify_category,
    classify_lifecycle,
    owner_domain,
)
from tools.consolidation.uc01.io_utils import iter_jsonl_gz, write_jsonl_gz


def test_deterministic_jsonl_gzip(tmp_path: Path) -> None:
    rows = [{"b": 2, "a": 1}, {"path": "x"}]
    first = tmp_path / "a.jsonl.gz"
    second = tmp_path / "b.jsonl.gz"
    write_jsonl_gz(first, rows)
    write_jsonl_gz(second, rows)
    assert first.read_bytes() == second.read_bytes()
    assert list(iter_jsonl_gz(first)) == [{"a": 1, "b": 2}, {"path": "x"}]


def test_artifact_classification_is_total() -> None:
    assert classify_category("tools/example.py") == "source_code"
    assert classify_category("docs/readme.md") == "documentation"
    assert classify_category("registry/x/state.json") == "registry_state"
    assert classify_category("something.unknown") == "other_artifact"
    assert classify_lifecycle("docs/root_archive/old.md") == "historical_or_archived"
    assert owner_domain("tools/strategy_factory/x.py") == "strategy_factory"
