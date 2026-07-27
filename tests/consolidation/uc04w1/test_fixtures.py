from __future__ import annotations

import json
import re
from pathlib import Path

from tools.consolidation.uc04w1.characterize import fixture_rows

OUTPUT_RE = re.compile(r"^[0-9]{4}\.[0-9]{2}\.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$")


def test_fixture_corpus_is_reproducible_and_byte_exact(repo_root: Path) -> None:
    payload = json.loads((repo_root / "tests/fixtures/consolidation/uc04w1/datetime_format_vectors.json").read_text())
    assert payload["fixture_count"] == 13
    assert payload["fixtures"] == fixture_rows()
    for row in payload["fixtures"]:
        output = row["expected"]
        assert len(output) == 19
        assert output.isascii()
        assert OUTPUT_RE.fullmatch(output)
        assert (output[4], output[7], output[10], output[13], output[16]) == (".", ".", " ", ":", ":")


def test_fixture_order_is_lexicographically_time_preserving(repo_root: Path) -> None:
    rows = fixture_rows()
    assert [row["unix_seconds"] for row in rows] == sorted(row["unix_seconds"] for row in rows)
    assert [row["expected"] for row in rows] == sorted(row["expected"] for row in rows)
