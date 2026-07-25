from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
required=['releases/history/saed/indexes/SAED_V4_40_FILE_INDEX.txt','releases/history/saed/hashes/SAED_V4_40_FILE_HASHES.sha256','releases/history/saed/inventories/SAED_V4_40_ARTIFACT_INVENTORY.csv','releases/history/saed/manifests/SAED_V4_40_PATCH_MANIFEST.json','releases/history/saed/reports/SAED_V4_40_QA_REPORT.json','releases/history/saed/readmes/README_SAED_V4_40_CONTEXT_FLEET_SCALEOUT.md','releases/history/saed/installers/INSTALL_SAED_V4_40_CONTEXT_FLEET_SCALEOUT.md','COMMIT_MESSAGE.md','releases/history/saed/scripts/EXPAND_REMOVE_SAED_V4_40_PATCH.ps1']
for rel in required:assert (ROOT/rel).exists(),rel
qa=json.loads((ROOT/'releases/history/saed/reports/SAED_V4_40_QA_REPORT.json').read_text());assert qa['passed'] is True and qa['reference_context_cells']==128 and qa['production_authorized'] is False
manifest=json.loads((ROOT/'releases/history/saed/manifests/SAED_V4_40_PATCH_MANIFEST.json').read_text());assert manifest['phase']=='SAED_V4_40' and manifest['production_authorization'] is False
index=[x for x in (ROOT/'releases/history/saed/indexes/SAED_V4_40_FILE_INDEX.txt').read_text().splitlines() if x];assert len(index)==manifest['file_count']
for rel in index:assert (ROOT/rel).exists(),rel
for line in (ROOT/'releases/history/saed/hashes/SAED_V4_40_FILE_HASHES.sha256').read_text().splitlines():
 if not line:continue
 h,rel=line.split('  ',1);assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
print(f'SAED V4-40 delivery passed: {len(index)} files')
