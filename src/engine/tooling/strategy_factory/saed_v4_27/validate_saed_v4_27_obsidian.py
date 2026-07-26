from tools.repository_paths import find_repository_root
from pathlib import Path
import re

ROOT = find_repository_root(__file__)
paths = [
    ROOT / "docs/history/systems/saed_v4/60_IMPLEMENTATION_PROGRAM_V4/V4_27_Complete_Search_And_Exposure_Ledger.md"
]
paths += sorted(
    (ROOT / "docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_27").glob("*.md")
)
paths += sorted(
    (ROOT / "docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_27").glob("*.md")
)
assert len(paths) == 247, len(paths)

for path in paths:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    assert "status: accepted-reference" in text, path
    assert "version: 1.0.0" in text, path
    assert "[[V4_28_Anytime_Valid_Online_FDR]]" in text, path
    assert "runtime" in text.lower() and "authority" in text.lower(), path

local = {path.stem for path in paths}
external = {
    "V4_26_Mechanistic_Interpretability",
    "V4_27_Complete_Search_And_Exposure_Ledger",
    "V4_28_Anytime_Valid_Online_FDR",
}
for path in paths:
    for target in re.findall(r"\[\[([^\]|#]+)", path.read_text(encoding="utf-8")):
        if target not in local and target not in external:
            raise AssertionError(f"broken local link {target} in {path}")

print("V4-27 Obsidian validation passed: 247 notes, 0 broken local links")
