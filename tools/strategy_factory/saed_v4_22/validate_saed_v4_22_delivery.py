from pathlib import Path
import hashlib,json,csv
ROOT=Path(__file__).resolve().parents[3]
index=ROOT/'releases/history/saed/indexes/SAED_V4_22_FILE_INDEX.txt';ledger=ROOT/'releases/history/saed/hashes/SAED_V4_22_FILE_HASHES.sha256';manifest_path=ROOT/'releases/history/saed/manifests/SAED_V4_22_PATCH_MANIFEST.json';qa_path=ROOT/'releases/history/saed/reports/SAED_V4_22_QA_REPORT.json';inventory=ROOT/'releases/history/saed/inventories/SAED_V4_22_ARTIFACT_INVENTORY.csv'
assert all(p.is_file() for p in [index,ledger,manifest_path,qa_path,inventory])
paths=[x.strip() for x in index.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(paths)==len(set(paths)) and not [x for x in paths if not (ROOT/x).is_file()]
expected={}
for line in ledger.read_text(encoding='utf-8').splitlines():
    if line.strip():digest,path=line.split('  ',1);expected[path]=digest
assert set(expected)==set(paths)-{'releases/history/saed/hashes/SAED_V4_22_FILE_HASHES.sha256'}
for path,digest in expected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
m=json.loads(manifest_path.read_text(encoding='utf-8'));q=json.loads(qa_path.read_text(encoding='utf-8'));s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_22.json').read_text(encoding='utf-8'))
assert m['phase']=='SAED_V4_22' and m['version']=='1.0.0' and m['file_count']==len(paths) and m['hash_count']==len(expected) and m['qa_passed'] and q['passed']
assert s['python_tests']>=120 and s['closed_schemas']>=40 and s['obsidian_notes']>=180 and s['mql5_static_files']>=19
assert s['real_alpha'] is False and s['production_authorization'] is False and s['metaeditor_compile']=='pending_local_windows'
c=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_22/GOLDEN_GENERATIVE_STRESS_CERTIFICATE.JSON').read_text(encoding='utf-8'))
assert c['accepted_for_synthetic_stress_falsification'] and c['positive_alpha_evidence'] is False and c['promotion_authority'] is False and c['runtime_executable'] is False and c['production_authority'] is False
h=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_22/V4_22_TO_V4_23_HANDOFF.JSON').read_text(encoding='utf-8'))
assert h['next_phase']=='SAED_V4_23' and all(h['entry_gates'].values()) and h['research_only'] and not any(h['authority'].values())
b=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_22/GOLDEN_BUDGET_SNAPSHOT.JSON').read_text(encoding='utf-8'))
assert b['hidden_evaluation_queries']==0 and b['protected_evidence_exposures']==0
f=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_22/GOLDEN_FIDELITY_REPORT.JSON').read_text(encoding='utf-8'));i=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_22/GOLDEN_INVARIANT_REPORT.JSON').read_text(encoding='utf-8'));e=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_22/GOLDEN_EXPLOITABILITY_REPORT.JSON').read_text(encoding='utf-8'))
assert f['passed'] and f['positive_evidence_usable'] is False and i['passed'] and e['passed'] and e['synthetic_gain_is_positive_evidence'] is False
with inventory.open(encoding='utf-8',newline='') as fh:
    rows=list(csv.DictReader(fh));assert len(rows)==len(paths) and {r['path'] for r in rows}==set(paths)
print(f'V4-22 delivery validation passed: {len(paths)} files, {len(expected)} hashes')
