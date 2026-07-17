from __future__ import annotations
import re
from _common import DOC
paths=list((DOC/"62_PHASE_DELIVERIES_V4/V4_31").glob("*.md"))+list((DOC/"63_ATOMIC_CONCEPTS_V4/V4_31").glob("*.md"))+[DOC/"60_IMPLEMENTATION_PROGRAM_V4/V4_31_Formal_Verification_And_Safety_Case.md"]
assert len(paths)>=250
seen=set()
for path in paths:
 text=path.read_text(encoding="utf-8")
 assert text.startswith("---\n") and "status: canonical" in text and "# " in text and "## Contract" in text and "## Verification" in text
 title=re.search(r"^title:\s*(.+)$",text,re.M).group(1).strip(); assert title not in seen; seen.add(title)
 assert "SAED_V4_31" in text or "V4-31" in text
print(f"V4-31 Obsidian validation passed: {len(paths)} notes")
