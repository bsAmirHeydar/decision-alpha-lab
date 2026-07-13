from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
OWNED=(ROOT/"lab/10_infrastructure/EXP0019_faerie_protocol/phase_i03")
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
