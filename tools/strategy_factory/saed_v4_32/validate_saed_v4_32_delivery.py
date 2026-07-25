from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
from _common import ROOT
idx=ROOT/"releases/history/saed/indexes/SAED_V4_32_FILE_INDEX.txt"; inv=ROOT/"releases/history/saed/inventories/SAED_V4_32_ARTIFACT_INVENTORY.csv"; hashes=ROOT/"releases/history/saed/hashes/SAED_V4_32_FILE_HASHES.sha256"; manifest=ROOT/"releases/history/saed/manifests/SAED_V4_32_PATCH_MANIFEST.json"; qa=ROOT/"releases/history/saed/reports/SAED_V4_32_QA_REPORT.json"
for p in [idx,inv,hashes,manifest,qa]: assert p.exists(),p
files=[x.strip() for x in idx.read_text().splitlines() if x.strip()]
assert files==sorted(set(files))
for rel in files: assert (ROOT/rel).is_file(),rel
expected={line.split('  ',1)[1]:line.split('  ',1)[0] for line in hashes.read_text().splitlines() if line.strip()}
for rel,digest in expected.items(): assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,rel
m=json.loads(manifest.read_text()); q=json.loads(qa.read_text()); assert m["phase"]=="SAED_V4_32" and m["file_count"]==len(files) and q["passed"]
with inv.open(newline='',encoding='utf-8') as fh: rows=list(csv.DictReader(fh)); assert len(rows)==len(files)
print(f"V4-32 delivery validation passed: {len(files)} files")
