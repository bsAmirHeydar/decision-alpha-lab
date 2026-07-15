from pathlib import Path
import ast,re
ROOT=Path(__file__).resolve().parents[3];pkg=ROOT/'lab/11_strategy_factory/python/saed_v4_graph_hypergraph_models';forbidden_imports={'torch','tensorflow','jax','networkx','sklearn','xgboost','lightgbm','catboost','requests','socket'}
for p in pkg.glob('*.py'):
 t=ast.parse(p.read_text());
 for n in ast.walk(t):
  if isinstance(n,(ast.Import,ast.ImportFrom)):
   names=[a.name.split('.')[0] for a in n.names] if isinstance(n,ast.Import) else [str(n.module).split('.')[0]]
   assert not forbidden_imports.intersection(names),(p,names)
a=(ROOT/'lab/11_strategy_factory/artifacts/saed_v4_13/AUTHORITY_BOUNDARY.JSON').read_text();assert '"execution_authority": false' in a and '"runtime_authority": false' in a
print('SAED V4-13 dependency and authority boundaries passed')
