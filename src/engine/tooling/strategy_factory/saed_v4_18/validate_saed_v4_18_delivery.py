from tools.repository_paths import find_repository_root
from pathlib import Path
import hashlib,json
ROOT=find_repository_root(__file__)
index=ROOT/'releases/history/saed/indexes/SAED_V4_18_FILE_INDEX.txt';ledger=ROOT/'releases/history/saed/hashes/SAED_V4_18_FILE_HASHES.sha256';manifest_path=ROOT/'releases/history/saed/manifests/SAED_V4_18_PATCH_MANIFEST.json';qa_path=ROOT/'releases/history/saed/reports/SAED_V4_18_QA_REPORT.json'
assert index.is_file() and ledger.is_file() and manifest_path.is_file() and qa_path.is_file()
paths=[x.strip() for x in index.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(paths)==len(set(paths)) and not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text(encoding='utf-8').splitlines():
    if line.strip():d,p=line.split('  ',1);expected[p]=d
for p,d in expected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d,p
assert set(expected)==set(paths)-{'releases/history/saed/hashes/SAED_V4_18_FILE_HASHES.sha256'}
m=json.loads(manifest_path.read_text(encoding='utf-8'));q=json.loads(qa_path.read_text(encoding='utf-8'))
assert m['phase']=='SAED_V4_18' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed'] and q['passed']
s=json.loads((ROOT/'releases/history/strategy_factory/program/status/SAED_V4_18.json').read_text(encoding='utf-8'))
assert s['claims']['causal_treatment_policy_value_boundary_implemented'] and not s['claims']['real_treatment_effect_established'] and not s['claims']['real_policy_value_established'] and not s['claims']['production_authorization']
h=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_18/V4_18_TO_V4_19_HANDOFF.JSON').read_text(encoding='utf-8'))
assert h['next_phase']=='SAED_V4_19' and all(h['entry_gates'].values()) and h['research_only'] and not h['authority']['select_live_treatment'] and not h['authority']['sign_promotion'] and not h['authority']['send_order']
print(f'V4-18 delivery validation passed: {len(paths)} files, {len(expected)} hashes')
