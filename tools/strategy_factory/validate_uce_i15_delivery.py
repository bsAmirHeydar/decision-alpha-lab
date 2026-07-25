#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];errors=[];index=ROOT/'releases/history/ucee/indexes/UCEE_I15_FILE_INDEX.txt'
paths=[x.strip() for x in index.read_text().splitlines() if x.strip()] if index.exists() else []
if not index.exists():errors.append('missing releases/history/ucee/indexes/UCEE_I15_FILE_INDEX.txt')
if len(paths)!=len(set(paths)):errors.append('duplicate file-index entries')
for rel in paths:
 if not (ROOT/rel).is_file():errors.append(f'missing indexed file {rel}')
for rel in paths:
 p=ROOT/rel
 if p.suffix=='.json':
  try:json.loads(p.read_text(encoding='utf-8'))
  except Exception as e:errors.append(f'invalid JSON {rel}: {e}')
hp=ROOT/'releases/history/ucee/hashes/UCEE_I15_FILE_HASHES.sha256'
if not hp.exists():errors.append('missing releases/history/ucee/hashes/UCEE_I15_FILE_HASHES.sha256')
else:
 declared={}
 for line in hp.read_text().splitlines():
  if line.strip():digest,rel=line.split('  ',1);declared[rel]=digest
 expected=set(paths)-{'releases/history/ucee/hashes/UCEE_I15_FILE_HASHES.sha256'}
 if set(declared)!=expected:errors.append('hash manifest paths do not match file index')
 for rel,digest in declared.items():
  if (ROOT/rel).is_file() and hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest:errors.append(f'hash mismatch {rel}')
if len(list((ROOT/'lab/11_strategy_factory/python/strategy_factory_tournament_v3').glob('*.py')))!=22:errors.append('expected 22 Python modules')
if len(list((ROOT/'lab/11_strategy_factory/schemas/v3').glob('tournament_*.schema.json')))!=25:errors.append('expected 25 tournament schemas')
if len(list((ROOT/'docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i15').glob('*.md')))!=43:errors.append('expected 43 delivery documents')
if len(list((ROOT/'docs/obsidian_deep/01_concepts').glob('UCE-I15_*.md')))!=12:errors.append('expected 12 atomic concepts')
if len(list((ROOT/'mql5/Include/AlphaLab/StrategyFactory/ContextTournament').glob('*.mqh')))!=10:errors.append('expected 10 MQL5 include files')
if errors:print('\n'.join(errors));raise SystemExit(1)
print(f'UCE-I15 delivery validation: PASS ({len(paths)} indexed files)')
