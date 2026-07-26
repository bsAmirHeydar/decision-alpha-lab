import csv

from src.engine.tooling.strategy_factory.lcm.lcm_01.mql5_scan import scan as mql_scan
from src.engine.tooling.strategy_factory.lcm.lcm_01.python_scan import scan as py_scan


def test_unresolved_edges_are_preserved(survey_root):
    with (survey_root / "dependencies/unresolved_dependency_edges.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert all(
        row["resolution_status"]
        in {"UNRESOLVED", "AMBIGUOUS_INTERNAL", "PATH_ESCAPE"}
        for row in rows
    )


def test_capability_hits_are_not_authority(survey_root):
    with (survey_root / "capabilities/capability_findings.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    assert all(
        row["risk_indicator_only"] == "true"
        and row["live_authority_inferred"] == "false"
        for row in rows
    )


def test_seeded_mql_dangerous_patterns_detected(tmp_path):
    path = tmp_path / "x.mq5"
    path.write_text(
        'void OnTick(){ CTrade t; ObjectCreate(0,"x",OBJ_HLINE,0,0,0); '
        'WebRequest("GET","x","",NULL,0,NULL,NULL); }',
        encoding="utf-8",
    )
    _, capabilities, _ = mql_scan(tmp_path, ["x.mq5"], {"x.mq5"})
    kinds = {row["capability_kind"] for row in capabilities}
    assert {"ORDER_API", "DRAWING_API", "NETWORK_API"} <= kinds


def test_seeded_python_risk_patterns_detected(tmp_path):
    path = tmp_path / "x.py"
    path.write_text(
        'import subprocess\n\ndef x():\n    return eval("1")\n',
        encoding="utf-8",
    )
    _, capabilities, _, failures = py_scan(tmp_path, ["x.py"])
    assert not failures
    kinds = {row["capability_kind"] for row in capabilities}
    assert {"SUBPROCESS", "DYNAMIC_EVAL"} <= kinds
