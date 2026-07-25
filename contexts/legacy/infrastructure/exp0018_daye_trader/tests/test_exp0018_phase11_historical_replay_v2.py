from tools.repository_paths import find_repository_root
import json,csv,subprocess,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_contract():
    d=json.loads((ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_historical_replay_contract_v2.json').read_text())
    assert d['execution_authority'] is False
    assert 'no_lookahead' in d['required_properties']
def test_fixtures():
    with (ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_historical_replay_cases_v2.csv').open() as f: rows=list(csv.DictReader(f))
    assert len(rows)==18
    assert any(r['case_id']=='R011' and 'same' in r['expected'] for r in rows)
def test_validator():
    p=subprocess.run([sys.executable,str(ROOT/'contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_phase11_historical_replay_v2.py'),str(ROOT)],capture_output=True,text=True)
    assert p.returncode==0,p.stdout+p.stderr
def test_no_execution_tokens():
    text='\n'.join(p.read_text(errors='ignore') for p in (ROOT/'mql5').rglob('DAYE_Replay*.mqh'))
    assert 'OrderSend' not in text and 'WebRequest' not in text
