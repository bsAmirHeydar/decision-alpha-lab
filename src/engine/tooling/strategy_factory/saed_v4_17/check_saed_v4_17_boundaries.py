from tools.repository_paths import find_repository_root
from pathlib import Path
import ast
ROOT=find_repository_root(__file__);base=ROOT/'src/engine/packages/saed_v4_causal_mechanism_discovery'
forbidden_imports={'MetaTrader5','requests','urllib3','socket','subprocess','torch','tensorflow','jax','xgboost','lightgbm','catboost','mlflow'}
for p in base.glob('*.py'):
 tree=ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
 for n in ast.walk(tree):
  if isinstance(n,(ast.Import,ast.ImportFrom)):
   names=[a.name.split('.')[0] for a in n.names] if isinstance(n,ast.Import) else [str(n.module).split('.')[0]]
   assert not forbidden_imports.intersection(names),(p,names)
a=(ROOT/'releases/history/strategy_factory/artifacts/saed_v4_17/AUTHORITY_BOUNDARY.JSON').read_text(encoding='utf-8')
for token in ['"causal_claim_authority": false','"production_authority": false','"execution_authority": false']:assert token in a
print('SAED V4-17 authority and dependency boundary passed')
