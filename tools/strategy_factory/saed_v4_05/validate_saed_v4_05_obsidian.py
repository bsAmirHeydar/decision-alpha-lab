from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
DOC_ROOT = ROOT / "docs"
PHASE = DOC_ROOT / "strategy_factory_sovereign_context_intelligence_v4/62_PHASE_DELIVERIES_V4/V4_05"
ATOMIC = DOC_ROOT / "strategy_factory_sovereign_context_intelligence_v4/63_ATOMIC_CONCEPTS_V4/V4_05"
files = sorted(PHASE.glob("*.md")) + sorted(ATOMIC.glob("*.md"))
if len(files) < 60:
    raise SystemExit("V4-05 Obsidian documentation is incomplete")
known = {path.stem for path in DOC_ROOT.rglob("*.md")}
missing = []
for path in files:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "phase: V4-05" not in text:
        raise SystemExit(f"invalid frontmatter: {path.relative_to(ROOT)}")
    for raw in re.findall(r"\[\[([^\]]+)\]\]", text):
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        target = Path(target).name
        if target and target not in known:
            missing.append((str(path.relative_to(ROOT)), target))
if missing:
    raise SystemExit("broken Obsidian links: " + "; ".join(f"{path}->{target}" for path, target in missing[:20]))
print(f"validated {len(files)} V4-05 Obsidian notes with no broken targets")
