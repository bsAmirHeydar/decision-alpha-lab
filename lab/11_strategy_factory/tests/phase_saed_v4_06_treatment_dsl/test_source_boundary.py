import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];PKG=ROOT/'lab/11_strategy_factory/python/saed_v4_treatment_dsl'
def test_no_model_or_broker_imports():
 forbidden=('torch','tensorflow','sklearn','xgboost','lightgbm','catboost','MetaTrader5','requests','httpx','socket')
 for p in PKG.glob('*.py'):
  tree=ast.parse(p.read_text())
  for n in ast.walk(tree):
   if isinstance(n,ast.Import): assert all(not a.name.startswith(forbidden) for a in n.names)
   if isinstance(n,ast.ImportFrom) and n.module: assert not n.module.startswith(forbidden)
