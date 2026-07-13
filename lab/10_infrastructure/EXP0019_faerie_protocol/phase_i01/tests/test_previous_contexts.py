from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[5]
INV=ROOT/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i00/artifacts/FP_I00_PREVIOUS_CONTEXT_TEST_INVENTORY.csv'

def test_all_previous_context_test_entrypoints_still_exist():
    rows=list(csv.DictReader(INV.open()))
    assert len(rows)==12
    assert all((ROOT/r['relative_path']).is_file() for r in rows)

def test_previous_context_sources_are_not_owned_by_i01():
    index=ROOT/'EXP0019_FP_I01_FILE_INDEX.txt'
    if index.exists():
        paths=index.read_text().splitlines()
        assert not any(p.startswith('mql5/Include/IntermarketDivergenceExecution/CG/') for p in paths)
        assert not any(p.startswith('mql5/Include/DayeTrader/EXP0018/') for p in paths)
