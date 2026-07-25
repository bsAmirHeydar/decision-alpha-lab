from __future__ import annotations
from tools.repository_paths import find_repository_root
import hashlib,json
from pathlib import Path
ROOT=find_repository_root(__file__)
required=['releases/history/saed/indexes/SAED_V4_41_FILE_INDEX.txt','releases/history/saed/hashes/SAED_V4_41_FILE_HASHES.sha256','releases/history/saed/inventories/SAED_V4_41_ARTIFACT_INVENTORY.csv','releases/history/saed/manifests/SAED_V4_41_PATCH_MANIFEST.json','releases/history/saed/reports/SAED_V4_41_QA_REPORT.json','releases/history/saed/readmes/README_SAED_V4_41_CONTINUOUS_SURVEILLANCE_RETIREMENT.md','releases/history/saed/installers/INSTALL_SAED_V4_41_CONTINUOUS_SURVEILLANCE_RETIREMENT.md','COMMIT_MESSAGE.md','releases/history/saed/scripts/EXPAND_REMOVE_SAED_V4_41_PATCH.ps1']
for rel in required:assert (ROOT/rel).exists(),rel
qa=json.loads((ROOT/'releases/history/saed/reports/SAED_V4_41_QA_REPORT.json').read_text());assert qa['passed'] is True and qa['reference_context_cells']==128 and qa['saed_v4_reference_roadmap_complete'] is True and qa['production_authorized'] is False
manifest=json.loads((ROOT/'releases/history/saed/manifests/SAED_V4_41_PATCH_MANIFEST.json').read_text());assert manifest['phase']=='SAED_V4_41' and manifest['next_phase'] is None and manifest['saed_v4_numbered_roadmap_complete'] is True and manifest['production_authorization'] is False
index=[x for x in (ROOT/'releases/history/saed/indexes/SAED_V4_41_FILE_INDEX.txt').read_text().splitlines() if x];assert len(index)==manifest['file_count']
for rel in index:assert (ROOT/rel).exists(),rel
for line in (ROOT/'releases/history/saed/hashes/SAED_V4_41_FILE_HASHES.sha256').read_text().splitlines():
 if not line:continue
 h,rel=line.split('  ',1);assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
print(f'SAED V4-41 delivery passed: {len(index)} files')
