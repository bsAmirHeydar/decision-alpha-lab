from pathlib import Path
from helpers import ROOT
PROTECTED=(
 'src/engine/packages/strategy_factory_contexts_v3/',
 'src/engine/packages/strategy_factory_dataset_v3/',
 'src/engine/packages/strategy_factory_trainers_v3/',
 'src/engine/packages/strategy_factory_onboarding_v3/',
 'src/engine/packages/strategy_factory_experiments_v3/',
 'src/engine/tooling/strategy_factory/acl_os/',
 'registry/acl_os/',
)

def test_patch_index_contains_no_central_engine_path():
 index=ROOT/'releases/history/rthp/indexes/RTHP_AI_INPUT_FILE_INDEX.txt'
 if not index.exists(): return
 paths=[x.strip().replace('\\','/') for x in index.read_text().splitlines() if x.strip()]
 assert not [p for p in paths if any(p.startswith(prefix) for prefix in PROTECTED)]

def test_plugin_is_additive_context_owned_package():
 plugin=ROOT/'src/engine/packages/strategy_factory_rthp_context_v1'
 assert plugin.is_dir() and (plugin/'package.py').is_file() and (plugin/'preflight.py').is_file()

def test_no_forbidden_engine_or_trade_calls_in_plugin():
 plugin=ROOT/'src/engine/packages/strategy_factory_rthp_context_v1'
 text='\n'.join(p.read_text(encoding='utf-8') for p in plugin.glob('*.py')).lower()
 for token in ('ordersend','order_send(','ctrade','positionopen','activate_capital','socket.','requests.get','urllib.request'):
  assert token not in text

def _snapshot_prefixes(prefixes):
 import hashlib,json
 hashes={}
 for prefix in prefixes:
  base=ROOT/prefix
  if not base.exists(): continue
  for path in sorted(x for x in base.rglob('*') if x.is_file() and '__pycache__' not in x.parts and '.pytest_cache' not in x.parts):
   hashes[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
 return hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest(),hashes

def test_extended_central_engine_snapshot_is_unchanged():
 import json
 from tools.strategy_factory.lcm.lcm_16a.canonical import object_digest
 ai=ROOT/'contexts/legacy/strategy_factory/generated/rthp_cross_symbol_cycle_divergence/ai_input'
 baseline=json.loads((ai/'generated/engine_extended_baseline_snapshot.json').read_text())
 _,current_files=_snapshot_prefixes(tuple(baseline['protected_prefixes']))
 amendment=json.loads((ai/'generated/engine_extended_baseline_amendment_lcm16a.json').read_text())
 assert amendment['amendment_digest']==object_digest(amendment,'amendment_digest')
 actual={}
 for path in sorted(set(baseline['file_hashes'])|set(current_files)):
  old=baseline['file_hashes'].get(path);new=current_files.get(path)
  if old!=new:
   actual[path]={'previous_sha256':('sha256:'+old) if old else None,'amended_sha256':('sha256:'+new) if new else None}
 approved={row['path']:{'previous_sha256':row['previous_sha256'],'amended_sha256':row['amended_sha256']} for row in amendment['records']}
 assert actual==approved
 assert not any(row.get('runtime_authority_created') or row.get('order_authority_created') or row.get('capital_authority_created') for row in amendment.get('records',[]))

def test_canonical_context_root_is_not_in_patch_payload():
 index=ROOT/'releases/history/rthp/indexes/RTHP_AI_INPUT_FILE_INDEX.txt'
 if not index.exists(): return
 forbidden='contexts/legacy/strategy_factory/authored/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1/'
 assert not [x for x in index.read_text().splitlines() if x.replace('\\','/').startswith(forbidden)]
