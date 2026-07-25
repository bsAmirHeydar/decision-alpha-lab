from __future__ import annotations
from tools.repository_paths import find_repository_root
import hashlib,json
from pathlib import Path
ROOT=find_repository_root(__file__)
required=['releases/history/saed/indexes/SAED_V4_39_FILE_INDEX.txt','releases/history/saed/hashes/SAED_V4_39_FILE_HASHES.sha256','releases/history/saed/inventories/SAED_V4_39_ARTIFACT_INVENTORY.csv','releases/history/saed/manifests/SAED_V4_39_PATCH_MANIFEST.json','releases/history/saed/reports/SAED_V4_39_QA_REPORT.json','releases/history/saed/readmes/README_SAED_V4_39_PROSPECTIVE_SHADOW_MICRO_LIVE.md','releases/history/saed/installers/INSTALL_SAED_V4_39_PROSPECTIVE_SHADOW_MICRO_LIVE.md','COMMIT_MESSAGE.md','releases/history/saed/scripts/EXPAND_REMOVE_SAED_V4_39_PATCH.ps1']
for rel in required:assert (ROOT/rel).exists(),rel
qa=json.loads((ROOT/'releases/history/saed/reports/SAED_V4_39_QA_REPORT.json').read_text());assert qa['passed'] is True and qa['micro_live_authorized'] is False and qa['production_authorized'] is False
manifest=json.loads((ROOT/'releases/history/saed/manifests/SAED_V4_39_PATCH_MANIFEST.json').read_text());assert manifest['phase']=='SAED_V4_39' and manifest['production_authorization'] is False
index=[x for x in (ROOT/'releases/history/saed/indexes/SAED_V4_39_FILE_INDEX.txt').read_text().splitlines() if x];assert len(index)==manifest['file_count']
for rel in index:assert (ROOT/rel).exists(),rel
for line in (ROOT/'releases/history/saed/hashes/SAED_V4_39_FILE_HASHES.sha256').read_text().splitlines():
 if not line:continue
 h,rel=line.split('  ',1);assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
print(f'SAED V4-39 delivery passed: {len(index)} files')
