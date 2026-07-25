import json
from conftest import CLOSURE
def test_adapter_authority_negative():
 r=json.loads((CLOSURE/'authority_negative/authority_negative_test_report.json').read_text());assert r['adapter_count']==483;assert r['passed_count']==483;assert r['failed_count']==0;assert r['live_order_count']==0;assert r['capital_activation_count']==0
def test_forbidden_scan_canonical_clean():
 r=json.loads((CLOSURE/'authority_negative/forbidden_api_scan.json').read_text());assert r['canonical_hit_count']==0;assert r['production_broker_parity']=='UNKNOWN'
