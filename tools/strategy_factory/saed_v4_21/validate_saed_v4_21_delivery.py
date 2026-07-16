from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
index=ROOT/'SAED_V4_21_FILE_INDEX.txt';ledger=ROOT/'SAED_V4_21_FILE_HASHES.sha256';manifest_path=ROOT/'SAED_V4_21_PATCH_MANIFEST.json';qa_path=ROOT/'SAED_V4_21_QA_REPORT.json'
assert index.is_file() and ledger.is_file() and manifest_path.is_file() and qa_path.is_file()
paths=[x.strip() for x in index.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(paths)==len(set(paths)) and not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text(encoding='utf-8').splitlines():
    if line.strip():digest,path=line.split('  ',1);expected[path]=digest
for path,digest in expected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
assert set(expected)==set(paths)-{'SAED_V4_21_FILE_HASHES.sha256'}
m=json.loads(manifest_path.read_text(encoding='utf-8'));q=json.loads(qa_path.read_text(encoding='utf-8'))
assert m['phase']=='SAED_V4_21' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed'] and q['passed']
s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_21.json').read_text(encoding='utf-8'))
assert s['qa']['python_tests']>=70 and s['qa']['closed_schema_pairs']>=40 and s['qa']['obsidian_notes']>=150 and s['qa']['mql5_static_files']>=19
assert s['claims']['robust_optimization_implemented'] and s['claims']['regret_analysis_implemented'] and s['claims']['baseline_preservation_implemented']
assert not s['claims']['real_policy_value_established'] and not s['claims']['production_treatment_selection'] and not s['claims']['production_risk_allocation'] and not s['claims']['production_authorization']
assert not any(s['authority'].values())
h=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_21/V4_21_TO_V4_22_HANDOFF.JSON').read_text(encoding='utf-8'))
assert h['next_phase']=='SAED_V4_22' and all(h['entry_gates'].values()) and h['research_only'] and not any(h['authority'].values())
c=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_21/GOLDEN_ROBUST_CERTIFICATE.JSON').read_text(encoding='utf-8'))
assert c['research_only'] and not c['runtime_executable'] and not c['decision_authority'] and not c['risk_allocation_authority'] and not c['promotion_authority'] and not c['execution_authority'] and not c['production_authority']
print(f'V4-21 delivery validation passed: {len(paths)} files, {len(expected)} hashes')
