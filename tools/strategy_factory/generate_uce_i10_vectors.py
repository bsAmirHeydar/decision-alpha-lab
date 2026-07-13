from pathlib import Path
import argparse,json,sys
from dataclasses import asdict
p=argparse.ArgumentParser();p.add_argument('root',nargs='?',default='.');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
root=Path(a.root).resolve();sys.path.insert(0,str(root/'lab/11_strategy_factory/python'))
from strategy_factory_deep_views_v3.conformance import run_conformance
from strategy_factory_deep_views_v3.registry import DeepAlgorithmRegistry
payload={'schema_version':'3.0.0','phase_id':'UCE-I10','conformance':run_conformance(),'registry':asdict(DeepAlgorithmRegistry().freeze().snapshot())}
path=root/'lab/11_strategy_factory/test_vectors/v3/uce_i10_deep_view_conformance_vectors.json'
text=json.dumps(payload,indent=2,sort_keys=True,default=lambda x:x.value)+"\n"
if a.verify_only:
    if not path.exists() or json.loads(path.read_text(encoding='utf-8'))!=json.loads(text):
        print('UCE-I10 vectors differ; regenerate intentionally');raise SystemExit(1)
    print('UCE-I10 vector verification PASS');raise SystemExit(0)
path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8');print(path)
