from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"lab/11_strategy_factory/python"))
from strategy_factory_inference.exporter import LinearScalarParameters,export_to_file
if __name__=="__main__":
 out=ROOT/"mql5/Files/StrategyFactory/Models/phase15/reference_linear_classifier.onnx"
 print(json.dumps(export_to_file(LinearScalarParameters((0.75,-0.5,0.25,1.1),-0.15),out),indent=2))
