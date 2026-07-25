from tools.repository_paths import find_repository_root
from pathlib import Path
import json,pytest
ROOT=find_repository_root(__file__);M=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_20/INVARIANT_ACCEPTANCE_MATRIX.JSON').read_text(encoding='utf-8'))
@pytest.mark.parametrize('row',M['rows'],ids=[x['invariant_id'] for x in M['rows']])
def test_each_invariant(row):assert row['passed'] and row['evidence_class']=='local_deterministic_synthetic_reference'
