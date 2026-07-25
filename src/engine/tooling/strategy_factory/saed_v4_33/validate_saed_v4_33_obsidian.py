from _common import DOC
phase=list((DOC/"62_PHASE_DELIVERIES_V4/V4_33").glob("*.md"));atomic=list((DOC/"63_ATOMIC_CONCEPTS_V4/V4_33").glob("*.md"));status=DOC/"61_PHASE_STATUS_V4/V4_33_FEDERATED_CONFIDENTIAL_RESEARCH_STATUS.md"
assert len(phase)>=80 and len(atomic)>=40 and status.exists()
for p in phase+atomic+[status]:
 t=p.read_text(encoding="utf-8"); assert t.startswith("---\n") and "# " in t and "SAED V4-33" in t
print(f"V4-33 Obsidian passed: {len(phase)+len(atomic)+1} notes")
