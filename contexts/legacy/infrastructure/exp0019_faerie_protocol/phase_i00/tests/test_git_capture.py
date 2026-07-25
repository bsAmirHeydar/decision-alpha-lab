from pathlib import Path
import subprocess

from fp_i00_governance.git_capture import capture_source_control


def run(path: Path, *args: str):
    subprocess.run(["git", "-C", str(path), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_non_git_directory_is_archive_mode(tmp_path):
    snapshot = capture_source_control(tmp_path)
    assert not snapshot.git_available
    assert snapshot.mode == "ARCHIVE_OR_NON_GIT"
    assert snapshot.clean is None
    assert snapshot.phase_clean is None


def test_git_clean_and_dirty_capture(tmp_path):
    run(tmp_path, "init")
    run(tmp_path, "config", "user.email", "test@example.com")
    run(tmp_path, "config", "user.name", "Test")
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    run(tmp_path, "add", "a.txt")
    run(tmp_path, "commit", "-m", "init")
    clean = capture_source_control(tmp_path)
    assert clean.git_available and clean.clean is True
    assert len(clean.head_commit) == 40
    (tmp_path / "a.txt").write_text("b", encoding="utf-8")
    dirty = capture_source_control(tmp_path, ("a.txt",))
    assert dirty.clean is False
    assert dirty.phase_clean is True
    assert "a.txt" in dirty.changed_paths
    assert dirty.unrelated_changed_paths == ()
