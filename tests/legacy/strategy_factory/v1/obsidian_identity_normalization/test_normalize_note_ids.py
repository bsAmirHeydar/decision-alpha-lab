from __future__ import annotations
from tools.repository_paths import find_repository_root

import importlib.util
import json
import shutil
import sys
from pathlib import Path

MODULE_PATH = find_repository_root(__file__) / "tools/engineering/obsidian_identity/normalize_note_ids.py"
spec = importlib.util.spec_from_file_location("normalize_note_ids", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_canonical_map_matches_vault_standard():
    path = MODULE_PATH.parent / "canonical_note_id_map.v1.json"
    mapping, digest = module.load_canonical_map(path)
    assert digest.startswith("sha256:")
    assert mapping["00_START_HERE/01_System_Map.md"] == "AIEOS-834106945E"
    assert mapping["01_FOUNDATIONS/_MOC.md"] == "AIEOS-7FE301EBF9"
    assert mapping["18_ALPHA_LAB_ENGINEERING_STANDARD/01_Authority_Hierarchy.md"] == "AIEOS2-DB06E6EA9040"


def test_inserts_only_id_and_is_idempotent(tmp_path):
    vault = tmp_path / "docs/ai_algorithm_engineering_os"
    note = vault / "01_FOUNDATIONS/01_AI_Role_Model.md"
    original = "---\ntitle: AI Role Model\nstatus: active\n---\n# Body\n"
    write(note, original)
    changes, originals, updated, *_ = module.plan(vault)
    assert len(changes) == 1
    module.apply_transactionally(updated, originals)
    result = note.read_text(encoding="utf-8")
    assert result.replace(f"id: {changes[0].note_id}\n", "", 1) == original
    second, *_ = module.plan(vault)
    assert second == ()


def test_preserves_existing_custom_id(tmp_path):
    vault = tmp_path / "docs/ai_algorithm_engineering_os"
    note = vault / "A.md"
    write(note, "---\nid: CUSTOM-1\ntitle: A\n---\n# A\n")
    changes, *_ = module.plan(vault)
    assert changes == ()
    assert "CUSTOM-1" in note.read_text(encoding="utf-8")


def test_duplicate_existing_id_fails_closed(tmp_path):
    vault = tmp_path / "docs/ai_algorithm_engineering_os"
    write(vault / "A.md", "---\nid: DUP\ntitle: A\n---\n# A\n")
    write(vault / "B.md", "---\nid: DUP\ntitle: B\n---\n# B\n")
    changes, _originals, _updated, _existing, collisions, malformed = module.plan(vault)
    assert changes == ()
    assert collisions and not malformed


def test_malformed_frontmatter_fails_closed(tmp_path):
    vault = tmp_path / "docs/ai_algorithm_engineering_os"
    write(vault / "A.md", "# No frontmatter\n")
    changes, _originals, _updated, _existing, collisions, malformed = module.plan(vault)
    assert changes == ()
    assert malformed and not collisions


def test_crlf_and_bom_are_preserved(tmp_path):
    vault = tmp_path / "docs/ai_algorithm_engineering_os"
    note = vault / "A.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    raw = b"\xef\xbb\xbf---\r\ntitle: A\r\n---\r\n# A\r\n"
    note.write_bytes(raw)
    changes, originals, updated, *_ = module.plan(vault)
    assert len(changes) == 1
    module.apply_transactionally(updated, originals)
    out = note.read_bytes()
    assert out.startswith(b"\xef\xbb\xbf") and b"\r\n" in out
    assert out.replace(f"id: {changes[0].note_id}\r\n".encode(), b"", 1) == raw


def test_exempt_readme_is_unchanged(tmp_path):
    vault = tmp_path / "docs/ai_algorithm_engineering_os"
    readme = vault / "README.md"
    write(readme, "# README\n")
    changes, *_ = module.plan(vault)
    assert changes == ()


def test_existing_id_mismatch_against_canonical_map_fails_closed(tmp_path):
    vault = tmp_path / "docs/ai_algorithm_engineering_os"
    write(vault / "A.md", "---\nid: WRONG\ntitle: A\n---\n# A\n")
    changes, _originals, _updated, _existing, collisions, malformed = module.plan(vault, {"A.md": "EXPECTED"})
    assert changes == ()
    assert not collisions
    assert any(item.startswith("existing_id_mismatch:") for item in malformed)
