from __future__ import annotations
from _common import DOC
paths = list((DOC / "62_PHASE_DELIVERIES_V4/V4_32").glob("*.md")) + list((DOC / "63_ATOMIC_CONCEPTS_V4/V4_32").glob("*.md"))
status = DOC / "61_PHASE_STATUS_V4/V4_32_MULTI_AGENT_RESEARCH_CONSTITUTION_STATUS.md"
paths.append(status)
assert all(p.exists() for p in paths)
for p in paths:
    text = p.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "phase: V4-32" in text
    assert "research_only: true" in text
    assert "## Authority boundary" in text
    assert "## Acceptance evidence" in text
    assert "production authorization" in text.lower() or "production" in text.lower()
print(f"V4-32 Obsidian validation passed: {len(paths)} notes")
