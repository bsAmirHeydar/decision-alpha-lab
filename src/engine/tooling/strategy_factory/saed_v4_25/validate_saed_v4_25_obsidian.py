from tools.repository_paths import find_repository_root
from pathlib import Path
import re

ROOT = find_repository_root(__file__)
DOC_ROOT = ROOT / "docs/history/systems/saed_v4"
phase_dirs = [
    DOC_ROOT / "62_PHASE_DELIVERIES_V4/V4_25",
    DOC_ROOT / "63_ATOMIC_CONCEPTS_V4/V4_25",
]
phase_files = sorted(path for directory in phase_dirs for path in directory.glob("*.md"))
program = DOC_ROOT / "60_IMPLEMENTATION_PROGRAM_V4/V4_25_Continual_Meta_And_Transfer.md"
phase_files.append(program)
assert len(phase_files) == 255, len(phase_files)
phase_stems = {path.stem for path in phase_files}
artifact_stems = {path.stem for path in (ROOT / "releases/history/strategy_factory/artifacts/saed_v4_25").glob("*.JSON")}
external_stems = {"V4_24_Conformal_OOD_And_Selective_Control", "V4_26_Mechanistic_Interpretability"}
allowed = phase_stems | artifact_stems | external_stems
broken = []
for path in phase_files:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    assert "phase: SAED_V4_25" in text, path
    assert "status:" in text and "version:" in text, path
    assert len(text.splitlines()) >= 12, path
    for raw in re.findall(r"\[\[([^\]]+)\]\]", text):
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if target and target not in allowed:
            broken.append((path.relative_to(ROOT).as_posix(), target))
assert not broken, broken[:20]
print(f"V4-25 Obsidian validation passed: {len(phase_files)} notes, 0 broken links")
