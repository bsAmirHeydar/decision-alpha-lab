from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
required=['SAED_V4_39_FILE_INDEX.txt','SAED_V4_39_FILE_HASHES.sha256','SAED_V4_39_ARTIFACT_INVENTORY.csv','SAED_V4_39_PATCH_MANIFEST.json','SAED_V4_39_QA_REPORT.json','README_SAED_V4_39_PROSPECTIVE_SHADOW_MICRO_LIVE.md','INSTALL_SAED_V4_39_PROSPECTIVE_SHADOW_MICRO_LIVE.md','COMMIT_MESSAGE.md','EXPAND_REMOVE_SAED_V4_39_PATCH.ps1']
for rel in required:assert (ROOT/rel).exists(),rel
qa=json.loads((ROOT/'SAED_V4_39_QA_REPORT.json').read_text());assert qa['passed'] is True and qa['micro_live_authorized'] is False and qa['production_authorized'] is False
manifest=json.loads((ROOT/'SAED_V4_39_PATCH_MANIFEST.json').read_text());assert manifest['phase']=='SAED_V4_39' and manifest['production_authorization'] is False
index=[x for x in (ROOT/'SAED_V4_39_FILE_INDEX.txt').read_text().splitlines() if x];assert len(index)==manifest['file_count']
for rel in index:assert (ROOT/rel).exists(),rel
for line in (ROOT/'SAED_V4_39_FILE_HASHES.sha256').read_text().splitlines():
 if not line:continue
 h,rel=line.split('  ',1);assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
print(f'SAED V4-39 delivery passed: {len(index)} files')
