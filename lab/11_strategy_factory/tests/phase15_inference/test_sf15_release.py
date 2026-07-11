import json
from pathlib import Path
from strategy_factory_inference.examples import *
from strategy_factory_inference.models import OnnxModelManifest
from strategy_factory_inference.enums import OutputSemantics
from strategy_factory_inference.release import validate_release

EX=Path(__file__).resolve().parents[2]/"examples"/"phase15"
def manifest():
 d=json.loads((EX/"onnx_model_manifest.json").read_text())
 d.pop("schema")
 d["output_semantics"]=OutputSemantics(d["output_semantics"])
 return OnnxModelManifest(**d)
def test_release_compatibility_passes():
 r=validate_release(EX/"reference_linear_classifier.onnx",manifest(),FEATURE_ORDER,PREPROCESSING,CALIBRATION,INPUT,OUTPUT,terminal_build=3900)
 assert r.compatible and not r.errors

def test_tamper_fails_closed(tmp_path):
 data=bytearray((EX/"reference_linear_classifier.onnx").read_bytes());data[-1]^=1;p=tmp_path/"tampered.onnx";p.write_bytes(data)
 r=validate_release(p,manifest(),FEATURE_ORDER,PREPROCESSING,CALIBRATION,INPUT,OUTPUT,terminal_build=3900)
 assert not r.compatible and any("SHA-256" in e for e in r.errors)

def test_old_terminal_fails_closed():
 r=validate_release(EX/"reference_linear_classifier.onnx",manifest(),FEATURE_ORDER,PREPROCESSING,CALIBRATION,INPUT,OUTPUT,terminal_build=3899)
 assert not r.compatible and "terminal build below release minimum" in r.errors
