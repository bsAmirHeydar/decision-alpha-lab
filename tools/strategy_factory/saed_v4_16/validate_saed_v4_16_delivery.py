from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
index=ROOT/'SAED_V4_16_FILE_INDEX.txt';ledger=ROOT/'SAED_V4_16_FILE_HASHES.sha256';manifest_path=ROOT/'SAED_V4_16_PATCH_MANIFEST.json';qa_path=ROOT/'SAED_V4_16_QA_REPORT.json'
assert index.is_file() and ledger.is_file() and manifest_path.is_file() and qa_path.is_file()
paths=[x.strip() for x in index.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(paths)==len(set(paths)) and not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text(encoding='utf-8').splitlines():
    if line.strip():d,p=line.split('  ',1);expected[p]=d
for p,d in expected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d,p
assert set(expected)==set(paths)-{'SAED_V4_16_FILE_HASHES.sha256'}
m=json.loads(manifest_path.read_text(encoding='utf-8'));q=json.loads(qa_path.read_text(encoding='utf-8'))
assert m['phase']=='SAED_V4_16' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed'] and q['passed']
s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_16.json').read_text(encoding='utf-8'))
assert s['claims']['distributional_survival_tail_boundary_implemented'] and not s['claims']['production_authorization'] and not s['claims']['causal_claim']
print(f'V4-16 delivery validation passed: {len(paths)} files, {len(expected)} hashes')
