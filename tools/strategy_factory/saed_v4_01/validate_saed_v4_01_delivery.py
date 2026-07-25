#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];idx=ROOT/'releases/history/saed/indexes/SAED_V4_01_FILE_INDEX.txt';ledger=ROOT/'releases/history/saed/hashes/SAED_V4_01_FILE_HASHES.sha256';errors=[];files=[x.strip() for x in idx.read_text().splitlines() if x.strip()] if idx.exists() else []
if len(files)!=len(set(files)):errors.append('duplicate file-index entry')
for rel in files:
 if not (ROOT/rel).is_file():errors.append(f'missing: {rel}')
expected={}
if ledger.exists():
 for line in ledger.read_text().splitlines():
  if line.strip():d,r=line.split('  ',1);expected[r]=d
for rel,d in expected.items():
 p=ROOT/rel
 if not p.is_file():errors.append(f'hash target missing: {rel}')
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=d:errors.append(f'hash mismatch: {rel}')
missing=sorted(set(files)-set(expected)-{'releases/history/saed/hashes/SAED_V4_01_FILE_HASHES.sha256'});extra=sorted(set(expected)-set(files))
if missing:errors.append(f'index entries without hash: {missing[:10]}')
if extra:errors.append(f'hashes outside index: {extra[:10]}')
print(json.dumps({'status':'pass' if not errors else 'fail','indexed_files':len(files),'hashed_files':len(expected),'errors':errors},indent=2));raise SystemExit(0 if not errors else 1)
