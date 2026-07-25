#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import json,hashlib
ROOT=find_repository_root(__file__);errors=[];index=ROOT/'releases/history/ucee/indexes/UCEE_I14_FILE_INDEX.txt'
paths=[x.strip() for x in index.read_text().splitlines() if x.strip()] if index.exists() else []
if not index.exists():errors.append('missing releases/history/ucee/indexes/UCEE_I14_FILE_INDEX.txt')
if len(paths)!=len(set(paths)):errors.append('duplicate file-index entries')
for rel in paths:
 if not (ROOT/rel).is_file():errors.append(f'missing indexed file {rel}')
for rel in paths:
 p=ROOT/rel
 if p.suffix=='.json':
  try:json.loads(p.read_text(encoding='utf-8'))
  except Exception as e:errors.append(f'invalid JSON {rel}: {e}')
hp=ROOT/'releases/history/ucee/hashes/UCEE_I14_FILE_HASHES.sha256'
if not hp.exists():errors.append('missing releases/history/ucee/hashes/UCEE_I14_FILE_HASHES.sha256')
else:
 declared={}
 for line in hp.read_text().splitlines():
  if line.strip():digest,rel=line.split('  ',1);declared[rel]=digest
 expected=set(paths)-{'releases/history/ucee/hashes/UCEE_I14_FILE_HASHES.sha256'}
 if set(declared)!=expected:errors.append('hash manifest paths do not match file index')
 for rel,digest in declared.items():
  if (ROOT/rel).is_file() and hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest:errors.append(f'hash mismatch {rel}')
if len(list((ROOT/'src/engine/packages/strategy_factory_runtime_v3').glob('*.py')))!=24:errors.append('expected 24 Python modules')
if len(list((ROOT/'schemas/legacy/strategy_factory/v3').glob('runtime_*.schema.json')))!=25:errors.append('expected 25 runtime schemas')
if len(list((ROOT/'docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i14').glob('*.md')))!=38:errors.append('expected 38 delivery documents')
if len(list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/ImmutableRuntime').glob('*.mqh')))!=12:errors.append('expected 12 MQL5 include files')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'UCE-I14 delivery validation: PASS ({len(paths)} indexed files)')
