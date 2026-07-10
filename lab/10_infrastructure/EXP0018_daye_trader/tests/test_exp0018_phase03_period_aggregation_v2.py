from __future__ import annotations
import csv, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]

def test_validator_passes():
    p=subprocess.run([sys.executable,str(ROOT/'lab/10_infrastructure/EXP0018_daye_trader/tools/validate_exp0018_phase03_period_aggregation_v2.py'),str(ROOT)],capture_output=True,text=True)
    assert p.returncode==0, p.stdout+p.stderr

def test_contract_has_no_execution_authority():
    c=json.loads((ROOT/'lab/10_infrastructure/EXP0018_daye_trader/contracts/daye_period_aggregation_contract_v2.json').read_text(encoding='utf-8'))
    assert c['execution_authority'] is False
    assert c['weekly_status']=='blocked_until_ADR-DY-A03'
    assert c['p4_minutes']==30

def test_dst_daily_expected_counts_are_explicit():
    rows={r['case_id']:r for r in csv.DictReader((ROOT/'lab/10_infrastructure/EXP0018_daye_trader/fixtures/daye_period_aggregation_cases_v2.csv').open(encoding='utf-8'))}
    assert int(rows['daily_normal_complete']['expected_bars'])==1380
    assert int(rows['daily_spring_dst_complete']['expected_bars'])==1320
    assert int(rows['daily_fall_dst_complete']['expected_bars'])==1440

def test_no_data_is_not_complete():
    rows={r['case_id']:r for r in csv.DictReader((ROOT/'lab/10_infrastructure/EXP0018_daye_trader/fixtures/daye_period_aggregation_cases_v2.csv').open(encoding='utf-8'))}
    assert rows['empty_period']['expected_completeness']=='EMPTY'
