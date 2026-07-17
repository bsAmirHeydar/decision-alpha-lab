from __future__ import annotations
import re
from pathlib import Path
from _common import DOC
phase=DOC/"62_PHASE_DELIVERIES_V4/V4_30"; atomic=DOC/"63_ATOMIC_CONCEPTS_V4/V4_30"; roadmap=DOC/"60_IMPLEMENTATION_PROGRAM_V4/V4_30_Independent_And_Multi_Lab_Replication.md"
phase_notes=sorted(phase.glob("*.md")); atomic_notes=sorted(atomic.glob("*.md")); notes=[roadmap]+phase_notes+atomic_notes
assert len(phase_notes)==181, len(phase_notes)
assert len(atomic_notes)==90, len(atomic_notes)
assert len(notes)==272
for note in notes:
 text=note.read_text(encoding="utf-8")
 assert text.startswith("---\n") and "status:" in text and "# " in text, note
 for raw in re.findall(r"\[\[([^\]]+)\]\]",text):
  target=raw.split("|",1)[0].split("#",1)[0]
  if not target: continue
  candidate=(note.parent/target)
  if candidate.suffix.lower()!=".md": candidate=candidate.with_suffix(".md")
  if not candidate.resolve().exists(): raise AssertionError(f"broken wikilink {raw} in {note}")
print("V4-30 Obsidian validation passed: 272 notes, zero broken links")
