from tools.repository_paths import find_repository_root
from pathlib import Path
import re

ROOT = find_repository_root(__file__)
DOC_ROOT = ROOT / "docs/history/systems/saed_v4"
phase_dirs = [
    DOC_ROOT / "62_PHASE_DELIVERIES_V4/V4_26",
    DOC_ROOT / "63_ATOMIC_CONCEPTS_V4/V4_26",
]
files = sorted(path for directory in phase_dirs for path in directory.glob("*.md"))
program = DOC_ROOT / "60_IMPLEMENTATION_PROGRAM_V4/V4_26_Mechanistic_Interpretability.md"
files.append(program)
assert len(files) == 323, len(files)
phase_stems = {path.stem for path in files}
artifact_stems = {
    path.stem
    for path in (ROOT / "releases/history/strategy_factory/artifacts/saed_v4_26").glob("*.JSON")
}
allowed = phase_stems | artifact_stems | {
    "V4_25_Continual_Meta_And_Transfer",
    "V4_27_Complete_Search_And_Exposure_Ledger",
}
broken = []
for path in files:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    assert "phase: SAED_V4_26" in text, path
    assert "status:" in text and "version:" in text, path
    assert len(text.splitlines()) >= 12, path
    for raw in re.findall(r"\[\[([^\]]+)\]\]", text):
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if target and target not in allowed:
            broken.append((path.relative_to(ROOT).as_posix(), target))
assert not broken, broken[:20]
print(f"V4-26 Obsidian validation passed: {len(files)} notes, 0 broken links")
