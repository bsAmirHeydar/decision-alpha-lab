from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
index=ROOT/'SAED_V4_19_FILE_INDEX.txt';ledger=ROOT/'SAED_V4_19_FILE_HASHES.sha256';manifest_path=ROOT/'SAED_V4_19_PATCH_MANIFEST.json';qa_path=ROOT/'SAED_V4_19_QA_REPORT.json'
assert index.is_file() and ledger.is_file() and manifest_path.is_file() and qa_path.is_file()
paths=[x.strip() for x in index.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(paths)==len(set(paths)) and not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text(encoding='utf-8').splitlines():
    if line.strip():d,p=line.split('  ',1);expected[p]=d
for p,d in expected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d,p
assert set(expected)==set(paths)-{'SAED_V4_19_FILE_HASHES.sha256'}
m=json.loads(manifest_path.read_text(encoding='utf-8'));q=json.loads(qa_path.read_text(encoding='utf-8'))
assert m['phase']=='SAED_V4_19' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed'] and q['passed']
s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_19.json').read_text(encoding='utf-8'))
assert s['claims']['proof_carrying_envelope_implemented'] and s['claims']['counterexample_search_implemented']
assert not s['claims']['real_setup_validity_established'] and not s['claims']['real_mechanism_established'] and not s['claims']['production_treatment_selection'] and not s['claims']['production_authorization']
h=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_19/V4_19_TO_V4_20_HANDOFF.JSON').read_text(encoding='utf-8'))
assert h['next_phase']=='SAED_V4_20' and all(h['entry_gates'].values()) and h['research_only'] and not h['authority']['select_live_treatment'] and not h['authority']['sign_promotion'] and not h['authority']['send_order']
p=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_19/GOLDEN_PROOF_ENVELOPE.JSON').read_text(encoding='utf-8'))
assert p['research_only'] and not p['runtime_executable'] and not p['execution_authority']
print(f'V4-19 delivery validation passed: {len(paths)} files, {len(expected)} hashes')
