from pathlib import Path
import sys,json
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); py=root/'lab/11_strategy_factory/python';sys.path.insert(0,str(py))
from strategy_factory_economics_v3 import run_conformance
out=root/'lab/11_strategy_factory/test_vectors/v3/uce_i05_economic_vectors.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(run_conformance(),indent=2,sort_keys=True,default=str)+'\n',encoding='utf-8');print(out)
