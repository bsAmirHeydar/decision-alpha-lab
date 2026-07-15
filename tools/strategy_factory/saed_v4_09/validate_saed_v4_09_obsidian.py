from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
dirs = [
    ROOT / "docs/strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_09",
    ROOT / "docs/strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_09",
]
files = [p for d in dirs for p in d.glob("*.md")]
errors = []
for p in files:
    text = p.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n# " not in text:
        errors.append(str(p.relative_to(ROOT)))
    if "status:" not in text[:500] or "phase:" not in text[:500]:
        errors.append(str(p.relative_to(ROOT)) + ":frontmatter")
if errors:
    raise SystemExit("obsidian validation failed: " + ",".join(errors))
print(f"validated {len(files)} SAED V4-09 Obsidian notes")
