from tools.repository_paths import find_repository_root
from pathlib import Path
import re

ROOT = find_repository_root(__file__)
paths = [
    ROOT / "docs/strategy_factory_sovereign_context_intelligence_v4/60_IMPLEMENTATION_PROGRAM_V4/V4_28_Anytime_Valid_Online_FDR.md"
]
paths += sorted(
    (ROOT / "docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_28").glob("*.md")
)
paths += sorted(
    (ROOT / "docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_28").glob("*.md")
)
assert len(paths) == 261, len(paths)

for path in paths:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    assert "status: accepted-reference" in text, path
    assert "version: 1.0.0" in text, path
    assert "[[V4_29_Hidden_Evaluation_Air_Gap]]" in text, path
    assert "authority" in text.lower() and "runtime" in text.lower(), path

local = {path.stem for path in paths}
external = {
    "V4_27_Complete_Search_And_Exposure_Ledger",
    "V4_28_Anytime_Valid_Online_FDR",
    "V4_29_Hidden_Evaluation_Air_Gap",
}
for path in paths:
    for target in re.findall(r"\[\[([^\]|#]+)", path.read_text(encoding="utf-8")):
        if target not in local and target not in external:
            raise AssertionError(f"broken link {target} in {path}")

print("V4-28 Obsidian validation passed: 261 notes, 0 broken local links")
