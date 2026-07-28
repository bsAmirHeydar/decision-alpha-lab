from __future__ import annotations

from tools.consolidation.uc04w1b.contracts import BASELINE_COMPILE_TARGETS
from tools.consolidation.uc04w1bn1.contracts import RUNNER


def test_runner_is_windows_powershell_51_safe_and_non_mutating(repo_root) -> None:
    payload = (repo_root / RUNNER).read_bytes()
    text = payload.decode("utf-8-sig")
    assert payload.endswith(b"\r\n")
    assert payload.count(b"\n") == payload.count(b"\r\n")
    assert "New-Item -ItemType Directory -LiteralPath" not in text
    assert '"/include:$WorkspaceMql5"' in text
    assert '"/log"' in text
    assert '"/inc:$WorkspaceMql5"' not in text
    assert "PYTHONDONTWRITEBYTECODE" in text
    assert "--untracked-files=no" in text
    assert "LOCALAPPDATA" in text
    assert "git add" not in text.lower()
    assert "git commit" not in text.lower()
    assert "git push" not in text.lower()


def test_runner_compile_matrix_is_exact(repo_root) -> None:
    text = (repo_root / RUNNER).read_text(encoding="utf-8-sig")
    matrix = text.split("$Targets = @(", 1)[1].split("\n)", 1)[0]
    observed = [
        line.strip().strip(",").strip('"')
        for line in matrix.splitlines()
        if line.strip().startswith('"mql5/')
    ]
    assert observed == list(BASELINE_COMPILE_TARGETS)


def test_runner_preserves_authority_boundary(repo_root) -> None:
    text = (repo_root / RUNNER).read_text(encoding="utf-8-sig")
    for token in (
        "implementation_authority = $false",
        "consumer_cutover_authority = $false",
        "deletion_authority = $false",
        "runtime_authority = $false",
        "order_authority = $false",
        "capital_authority = $false",
        "AllowLiveTrading=0",
        "AllowDllImport=0",
    ):
        assert token in text
