from pathlib import Path
from strategy_factory_inference.exporter import *
from strategy_factory_inference.hashing import sha256_bytes,fnv1a64

def test_export_is_deterministic_and_exact():
 p=LinearScalarParameters((0.75,-0.5,0.25,1.1),-0.15)
 a=export_linear_scalar_onnx(p);b=export_linear_scalar_onnx(p)
 assert a==b and len(a)==269
 assert sha256_bytes(a)=="3e0fa5825e5656cfefdcf34bb9e05e1844ab231c8dbb74150619068c392fcac8"
 assert fnv1a64(a)=="1e623513209288b3"

def test_structural_inspection():
 data=export_linear_scalar_onnx(LinearScalarParameters((0.75,-0.5,0.25,1.1),-0.15))
 info=inspect_linear_scalar_onnx(data)
 assert info["ir_version"]==8 and info["opset"]==13
 assert info["graph_name"]=="AlphaLabLinearScalarV1"
 assert [x[1] for x in info["operators"]]==["MatMul","Add"]
 assert info["inputs"]==["features"] and info["outputs"]==["score"]
 assert info["initializers"]==[("weights",(4,1),1),("bias",(1,),1)]
