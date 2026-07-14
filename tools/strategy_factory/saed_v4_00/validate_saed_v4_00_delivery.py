#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
idx=ROOT/'SAED_V4_00_FILE_INDEX.txt'; ledger=ROOT/'SAED_V4_00_FILE_HASHES.sha256'
errors=[]
files=[x.strip() for x in idx.read_text(encoding='utf-8').splitlines() if x.strip()] if idx.exists() else []
if len(files)!=len(set(files)): errors.append('duplicate file-index entry')
for rel in files:
 if not (ROOT/rel).is_file(): errors.append(f'missing: {rel}')
expected={}
if ledger.exists():
 for line in ledger.read_text(encoding='utf-8').splitlines():
  if line.strip():
   digest,rel=line.split('  ',1); expected[rel]=digest
for rel,digest in expected.items():
 p=ROOT/rel
 if not p.is_file(): errors.append(f'hash target missing: {rel}'); continue
 actual=hashlib.sha256(p.read_bytes()).hexdigest()
 if actual!=digest: errors.append(f'hash mismatch: {rel}')
# Ledger intentionally excludes itself but must cover all other indexed files.
missing_hashes=sorted(set(files)-set(expected)-{'SAED_V4_00_FILE_HASHES.sha256'})
extra_hashes=sorted(set(expected)-set(files))
if missing_hashes: errors.append(f'index entries without hash: {missing_hashes[:10]}')
if extra_hashes: errors.append(f'hashes outside index: {extra_hashes[:10]}')
print(json.dumps({'status':'pass' if not errors else 'fail','indexed_files':len(files),'hashed_files':len(expected),'errors':errors},indent=2))
raise SystemExit(0 if not errors else 1)
