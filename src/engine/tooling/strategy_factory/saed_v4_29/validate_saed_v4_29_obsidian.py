from tools.repository_paths import find_repository_root
from pathlib import Path

ROOT = find_repository_root(__file__)
DOCS = ROOT / "docs/history/systems/saed_v4"
PHASE = DOCS / "62_PHASE_DELIVERIES_V4/V4_29"
ATOMIC = DOCS / "63_ATOMIC_CONCEPTS_V4/V4_29"
ROADMAP = DOCS / "60_IMPLEMENTATION_PROGRAM_V4/V4_29_Hidden_Evaluation_Air_Gap.md"
files = sorted(PHASE.glob("*.md")) + sorted(ATOMIC.glob("*.md")) + [ROADMAP]
assert ROADMAP.is_file()
assert len(list(PHASE.glob("*.md"))) >= 170
assert len(list(ATOMIC.glob("*.md"))) >= 90
for path in files:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "title:" in text[:500]
    assert "status:" in text[:500]
    assert "# " in text
    if path != ROADMAP:
        assert "[[V4_29_Hidden_Evaluation_Air_Gap]]" in text
print(f"V4-29 Obsidian validation passed: {len(files)} notes")
