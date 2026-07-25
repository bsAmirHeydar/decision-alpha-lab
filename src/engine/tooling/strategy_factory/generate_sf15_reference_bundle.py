from tools.repository_paths import find_repository_root
from pathlib import Path
import sys,json
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/"src/engine/packages"))
from strategy_factory_inference.exporter import LinearScalarParameters,export_to_file
if __name__=="__main__":
 out=ROOT/"mql5/Files/StrategyFactory/Models/phase15/reference_linear_classifier.onnx"
 print(json.dumps(export_to_file(LinearScalarParameters((0.75,-0.5,0.25,1.1),-0.15),out),indent=2))
