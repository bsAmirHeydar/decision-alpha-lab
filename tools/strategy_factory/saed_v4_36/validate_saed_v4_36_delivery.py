import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];index=ROOT/'releases/history/saed/indexes/SAED_V4_36_FILE_INDEX.txt';paths=[x.strip() for x in index.read_text().splitlines() if x.strip()];assert paths==sorted(set(paths));missing=[p for p in paths if not (ROOT/p).is_file()];assert not missing,missing
m=json.loads((ROOT/'releases/history/saed/manifests/SAED_V4_36_PATCH_MANIFEST.json').read_text());assert m['phase']=='SAED_V4_36' and m['file_count']==len(paths)
rows=list(csv.DictReader((ROOT/'releases/history/saed/inventories/SAED_V4_36_ARTIFACT_INVENTORY.csv').open()));assert len(rows)==len(paths)
ledger={}
for line in (ROOT/'releases/history/saed/hashes/SAED_V4_36_FILE_HASHES.sha256').read_text().splitlines():
 if line.strip():h,p=line.split('  ',1);ledger[p]=h
excluded={'releases/history/saed/hashes/SAED_V4_36_FILE_HASHES.sha256','releases/history/saed/manifests/SAED_V4_36_PATCH_MANIFEST.json','releases/history/saed/reports/SAED_V4_36_QA_REPORT.json','lab/11_strategy_factory/phase_status/SAED_V4_36.json'}
for p in paths:
 if p not in excluded:assert ledger[p]==hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),p
print(f'V4-36 delivery passed: {len(paths)} files')
