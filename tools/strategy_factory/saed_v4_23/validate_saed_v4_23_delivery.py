from pathlib import Path
import hashlib,json,csv
ROOT=Path(__file__).resolve().parents[3]
index=ROOT/'releases/history/saed/indexes/SAED_V4_23_FILE_INDEX.txt';ledger=ROOT/'releases/history/saed/hashes/SAED_V4_23_FILE_HASHES.sha256';manifest_path=ROOT/'releases/history/saed/manifests/SAED_V4_23_PATCH_MANIFEST.json';qa_path=ROOT/'releases/history/saed/reports/SAED_V4_23_QA_REPORT.json';inventory=ROOT/'releases/history/saed/inventories/SAED_V4_23_ARTIFACT_INVENTORY.csv'
assert all(p.is_file() for p in [index,ledger,manifest_path,qa_path,inventory])
paths=[x.strip() for x in index.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(paths)==len(set(paths)) and not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text(encoding='utf-8').splitlines():
    if line.strip():digest,path=line.split('  ',1);expected[path]=digest
assert set(expected)==set(paths)-{'releases/history/saed/hashes/SAED_V4_23_FILE_HASHES.sha256'}
for path,digest in expected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
m=json.loads(manifest_path.read_text(encoding='utf-8'));q=json.loads(qa_path.read_text(encoding='utf-8'));s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_23.json').read_text(encoding='utf-8'))
assert m['phase']=='SAED_V4_23' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed'] and q['passed']
assert s['python_tests']>=180 and s['closed_schemas']>=60 and s['obsidian_notes']>=230 and s['mql5_static_files']>=22 and s['qa_passed']
assert s['real_alpha'] is False and s['promotion_authority'] is False and s['runtime_executable'] is False and s['production_authorization'] is False and s['metaeditor_compile']=='pending_local_windows'
A=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_23'
c=json.loads((A/'GOLDEN_OFFLINE_POLICY_RESEARCH_CERTIFICATE.JSON').read_text(encoding='utf-8'))
assert c['accepted_for_offline_policy_research'] and all(c['gates'].values()) and c['selection_is_research_only']
assert c['promotion_authority'] is False and c['runtime_executable'] is False and c['production_authority'] is False and c['real_alpha_claim'] is False and c['prospective_success_claim'] is False
assert not any(c['authority_boundary']['authority'].values())
h=json.loads((A/'V4_23_TO_V4_24_HANDOFF.JSON').read_text(encoding='utf-8'))
assert h['next_phase']=='SAED_V4_24' and all(h['entry_gates'].values()) and h['research_only'] and not any(h['authority'].values())
b=json.loads((A/'GOLDEN_BUDGET_SNAPSHOT.JSON').read_text(encoding='utf-8'))
assert b['counts']['hidden_evaluation_queries']==0 and b['counts']['protected_evidence_exposures']==0 and b['counts']['training_trials']==3 and b['counts']['ope_evaluations']==4
x=json.loads((A/'GOLDEN_EXPOSURE_LEDGER.JSON').read_text(encoding='utf-8'))
assert x['complete'] and x['hidden_evaluation_queries']==0 and x['protected_evidence_exposures']==0 and x['runtime_compilations']==0 and x['order_submissions']==0 and x['synthetic_positive_evidence_uses']==0
cm=json.loads((A/'GOLDEN_POLICY_CHALLENGE_MATRIX.JSON').read_text(encoding='utf-8'))
assert cm['selection_is_research_only'] and cm['promotion_authority'] is False and cm['runtime_authority'] is False and cm['abstain_if_no_challenger']
assert all(r['promotion_eligible'] is False and r['runtime_executable'] is False for r in cm['rows'])
ope=json.loads((A/'GOLDEN_OPE_BUNDLE.JSON').read_text(encoding='utf-8'))
assert len(ope['reports'])==4 and all(set(v['estimators'])=={'wis','pdis','fqe','doubly_robust'} for v in ope['reports'].values())
stress=json.loads((A/'GOLDEN_SYNTHETIC_STRESS_CHALLENGE.JSON').read_text(encoding='utf-8'))
assert stress['positive_evidence_contribution']==0.0 and all(v['synthetic_positive_evidence'] is False for v in stress['reports'].values())
with inventory.open(encoding='utf-8',newline='') as fh:
    rows=list(csv.DictReader(fh));assert len(rows)==len(paths) and {r['path'] for r in rows}==set(paths)
print(f'V4-23 delivery validation passed: {len(paths)} files, {len(expected)} hashes')
