import json
import subprocess
import sys


def test_acl00_cli_accepts_deterministic_as_of(root, tmp_path):
    fixture = root / "lab/11_strategy_factory/acl_os/fixtures/acl_00/valid_semantic_transition.json"
    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.strategy_factory.acl_os.acl_00.cli",
            "evaluate",
            str(fixture),
            "--ledger",
            str(tmp_path / "audit.jsonl"),
            "--as-of",
            "2026-07-17T12:30:00Z",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert process.returncode == 0, process.stderr
    assert json.loads(process.stdout)["decision"] == "ALLOW"
