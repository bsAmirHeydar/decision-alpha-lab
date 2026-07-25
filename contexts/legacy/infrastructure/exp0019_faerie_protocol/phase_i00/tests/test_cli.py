from pathlib import Path
import json
import subprocess
import sys

from conftest import REPO_ROOT


def test_cli_generate_and_validate():
    script = REPO_ROOT / "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i00/run_phase_i00.py"
    result = subprocess.run([sys.executable, str(script), str(REPO_ROOT), "--generate", "--json"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads(result.stdout)
    assert report["passed"] is True
    assert report["health"] == "READY"
