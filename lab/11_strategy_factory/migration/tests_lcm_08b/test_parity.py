from pathlib import Path
import json
from tools.strategy_factory.lcm.lcm_08b.parity import compare_case

REPO=Path(__file__).resolve().parents[4]
CTX=REPO/'lab/11_strategy_factory/contexts/CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1'

def catalog():return json.loads((CTX/'fixtures/golden_case_catalog.json').read_text())

def test_all_golden_cases_exact_parity():
    for case in catalog()['cases']:
        result=compare_case(REPO,case,CTX/'fixtures/golden')
        assert result['status']=='PASS',result
        assert result['legacy_digest']==result['canonical_digest']

def test_restart_replay_deterministic():
    case=next(x for x in catalog()['cases'] if x['case_type']=='RESTART')
    a=compare_case(REPO,case,CTX/'fixtures/golden');b=compare_case(REPO,case,CTX/'fixtures/golden')
    assert a['canonical_digest']==b['canonical_digest']
