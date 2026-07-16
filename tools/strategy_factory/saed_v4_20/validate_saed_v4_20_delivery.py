from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
index=ROOT/'SAED_V4_20_FILE_INDEX.txt';ledger=ROOT/'SAED_V4_20_FILE_HASHES.sha256';manifest_path=ROOT/'SAED_V4_20_PATCH_MANIFEST.json';qa_path=ROOT/'SAED_V4_20_QA_REPORT.json'
assert index.is_file() and ledger.is_file() and manifest_path.is_file() and qa_path.is_file()
paths=[x.strip() for x in index.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(paths)==len(set(paths)) and not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text(encoding='utf-8').splitlines():
    if line.strip():d,p=line.split('  ',1);expected[p]=d
for p,d in expected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d,p
assert set(expected)==set(paths)-{'SAED_V4_20_FILE_HASHES.sha256'}
m=json.loads(manifest_path.read_text(encoding='utf-8'));q=json.loads(qa_path.read_text(encoding='utf-8'))
assert m['phase']=='SAED_V4_20' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed'] and q['passed']
s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_20.json').read_text(encoding='utf-8'))
assert s['qa']['python_tests']==178 and s['qa']['closed_schema_pairs']>=40 and s['qa']['obsidian_notes']>=140 and s['qa']['mql5_static_files']>=18
assert s['claims']['decision_focused_selection_implemented'] and s['claims']['set_valued_selection_implemented'] and s['claims']['selection_certificate_implemented']
assert not s['claims']['real_policy_value_established'] and not s['claims']['production_treatment_selection'] and not s['claims']['production_authorization']
h=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_20/V4_20_TO_V4_21_HANDOFF.JSON').read_text(encoding='utf-8'))
assert h['next_phase']=='SAED_V4_21' and all(h['entry_gates'].values()) and h['research_only'] and not any(h['authority'].values())
c=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_20/GOLDEN_SELECTION_CERTIFICATE.JSON').read_text(encoding='utf-8'))
assert c['research_only'] and not c['runtime_executable'] and not c['decision_authority'] and not c['promotion_authority'] and not c['execution_authority']
print(f'V4-20 delivery validation passed: {len(paths)} files, {len(expected)} hashes')
