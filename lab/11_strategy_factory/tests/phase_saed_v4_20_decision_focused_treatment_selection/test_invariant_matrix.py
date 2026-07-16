from pathlib import Path
import json,pytest
ROOT=Path(__file__).resolve().parents[4];M=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_20/INVARIANT_ACCEPTANCE_MATRIX.JSON').read_text(encoding='utf-8'))
@pytest.mark.parametrize('row',M['rows'],ids=[x['invariant_id'] for x in M['rows']])
def test_each_invariant(row):assert row['passed'] and row['evidence_class']=='local_deterministic_synthetic_reference'
