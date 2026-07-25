from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
index=ROOT/'releases/history/saed/indexes/SAED_V4_17_FILE_INDEX.txt';ledger=ROOT/'releases/history/saed/hashes/SAED_V4_17_FILE_HASHES.sha256';manifest_path=ROOT/'releases/history/saed/manifests/SAED_V4_17_PATCH_MANIFEST.json';qa_path=ROOT/'releases/history/saed/reports/SAED_V4_17_QA_REPORT.json'
assert index.is_file() and ledger.is_file() and manifest_path.is_file() and qa_path.is_file()
paths=[x.strip() for x in index.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(paths)==len(set(paths)) and not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text(encoding='utf-8').splitlines():
    if line.strip():d,p=line.split('  ',1);expected[p]=d
for p,d in expected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d,p
assert set(expected)==set(paths)-{'releases/history/saed/hashes/SAED_V4_17_FILE_HASHES.sha256'}
m=json.loads(manifest_path.read_text(encoding='utf-8'));q=json.loads(qa_path.read_text(encoding='utf-8'))
assert m['phase']=='SAED_V4_17' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed'] and q['passed']
s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_17.json').read_text(encoding='utf-8'))
assert s['claims']['causal_mechanism_discovery_boundary_implemented'] and not s['claims']['real_causal_mechanism_discovered'] and not s['claims']['treatment_effect_identified'] and not s['claims']['production_authorization']
h=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_17/V4_17_TO_V4_18_HANDOFF.JSON').read_text(encoding='utf-8'))
assert h['next_phase']=='SAED_V4_18' and all(h['entry_gates'].values()) and not h['authority']['assert_real_causality'] and not h['authority']['estimate_production_treatment_effect']
print(f'V4-17 delivery validation passed: {len(paths)} files, {len(expected)} hashes')
