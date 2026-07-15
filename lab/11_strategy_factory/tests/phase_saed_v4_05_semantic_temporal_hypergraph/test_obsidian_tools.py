from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]


def run(relative):
    return subprocess.run([sys.executable, relative], cwd=ROOT, capture_output=True, text=True)


def test_obsidian_validator_passes():
    result = run("tools/strategy_factory/saed_v4_05/validate_saed_v4_05_obsidian.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Obsidian notes" in result.stdout


def test_boundary_scan_passes():
    result = run("tools/strategy_factory/saed_v4_05/check_saed_v4_05_boundaries.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "boundary scan passed" in result.stdout
