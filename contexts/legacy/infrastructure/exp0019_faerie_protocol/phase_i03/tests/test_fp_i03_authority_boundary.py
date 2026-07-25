from tools.repository_paths import find_repository_root
from pathlib import Path

ROOT=find_repository_root(__file__)
OWNED=(ROOT/"contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i03")
FORBIDDEN=("ordersend","ctrade","buy(","sell(","positionopen","webrequest","objectcreate(")


def test_phase_owned_python_has_no_execution_or_chart_authority():
    offenders=[]
    for path in OWNED.rglob("*.py"):
        if path.name == "test_fp_i03_authority_boundary.py":
            continue
        text=path.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN:
            if token in text:offenders.append((str(path.relative_to(ROOT)),token))
    assert offenders==[]
