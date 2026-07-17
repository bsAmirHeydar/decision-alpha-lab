from __future__ import annotations
import json
from _common import AR, MAP, reference_result
result = reference_result()
for key, name in MAP.items():
    expected = json.loads((AR / name).read_text(encoding="utf-8"))
    assert result[key] == expected, name
assert result["replay"]["deterministic"]
assert result["replay"]["future_suffix_records_seen"] == 0
assert result["reproduction"]["exact_match"]
print(f"V4-32 exact golden replay passed: {len(MAP)} artifacts")
