from __future__ import annotations
import re
from _common import DOC
roots=[DOC/"62_PHASE_DELIVERIES_V4/V4_34",DOC/"63_ATOMIC_CONCEPTS_V4/V4_34"]
files=[]
for root in roots:
    for p in root.glob("*.md"):
        text=p.read_text(encoding="utf-8"); assert text.startswith("---\n"),p; assert "status:" in text and "tags:" in text,p; files.append(p)
assert len(files)>=150
print(f"V4-34 Obsidian validation passed: {len(files)} phase/atomic notes")
