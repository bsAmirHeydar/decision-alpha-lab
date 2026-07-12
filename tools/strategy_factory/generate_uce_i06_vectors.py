from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();sys.path.insert(0,str(root/'lab/11_strategy_factory/python'))
from strategy_factory_dataset_v3.conformance import run_conformance
from strategy_factory_dataset_v3.golden import golden_anchors,golden_treatments,golden_path,golden_scenarios,golden_tasks
from strategy_factory_dataset_v3.cube import CounterfactualOutcomeCubeBuilder
payload={"conformance":run_conformance(),"anchor":golden_anchors(1)[0].to_dict(),"treatments":[x.to_dict() for x in golden_treatments(golden_anchors(1)[0])],"path":[x.to_dict() for x in golden_path(golden_anchors(1)[0])],"scenarios":[x.to_dict() for x in golden_scenarios()],"tasks":[x.to_dict() for x in golden_tasks()]}
out=root/'lab/11_strategy_factory/test_vectors/v3/uce_i06_golden_dataset_vectors.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(payload,indent=2,sort_keys=True,default=str)+'\n',encoding='utf-8');print(out)
