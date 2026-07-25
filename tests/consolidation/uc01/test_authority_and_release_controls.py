from pathlib import Path

from tools.consolidation.uc01.constants import BASELINE_RELATIVE_ROOT


def test_uc01_has_no_destructive_authority() -> None:
    assert BASELINE_RELATIVE_ROOT.as_posix().startswith("registry/consolidation/uc01/")


def test_static_release_index_exists() -> None:
    root = Path(__file__).resolve().parents[3]
    index = root / "releases/unified_consolidation/uc01/UC01_PATCH_FILE_INDEX.txt"
    assert index.is_file()
    paths = [line.strip() for line in index.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(paths) == len(set(paths))
    assert not any(path.startswith("registry/consolidation/uc01/baselines/") for path in paths)


def test_static_patch_verifier_passes() -> None:
    from tools.consolidation.uc01.verify import verify_static_patch

    root = Path(__file__).resolve().parents[3]
    result = verify_static_patch(root)
    assert result["status"] == "PASS", result["errors"]
