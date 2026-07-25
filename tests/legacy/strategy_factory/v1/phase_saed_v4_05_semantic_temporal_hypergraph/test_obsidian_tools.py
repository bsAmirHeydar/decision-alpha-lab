from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess
import sys

ROOT = find_repository_root(__file__)


def run(relative):
    return subprocess.run([sys.executable, relative], cwd=ROOT, capture_output=True, text=True)


def test_obsidian_validator_passes():
    result = run("src/engine/tooling/strategy_factory/saed_v4_05/validate_saed_v4_05_obsidian.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Obsidian notes" in result.stdout


def test_boundary_scan_passes():
    result = run("src/engine/tooling/strategy_factory/saed_v4_05/check_saed_v4_05_boundaries.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "boundary scan passed" in result.stdout
