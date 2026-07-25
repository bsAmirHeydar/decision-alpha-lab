import json
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[2]
SC=ROOT/"schemas"/"v1";EX=ROOT/"examples"/"phase15"
MAP={
 "feature_order.json":"feature_order.schema.json","preprocessing_manifest.json":"preprocessing_manifest.schema.json","calibration_contract.json":"calibration_contract.schema.json","input_tensor_contract.json":"tensor_contract.schema.json","output_tensor_contract.json":"tensor_contract.schema.json","onnx_export_plan.json":"onnx_export_plan.schema.json","linear_scalar_parameters.json":"linear_scalar_parameters.schema.json","onnx_model_manifest.json":"onnx_model_manifest.schema.json","expected_python_reference_parity_report.json":"parity_report.schema.json","expected_mql5_onnx_parity_report_pending.json":"parity_report.schema.json","runtime_compatibility_report.json":"runtime_compatibility_report.schema.json","inference_release_manifest.json":"inference_release_manifest.schema.json"}
def test_all_schemas_meta_validate():
 for p in SC.glob("*schema.json"): jsonschema.Draft202012Validator.check_schema(json.loads(p.read_text()))
def test_examples_validate():
 for example,schema in MAP.items():jsonschema.validate(json.loads((EX/example).read_text()),json.loads((SC/schema).read_text()))
 schema=json.loads((SC/"parity_vector.schema.json").read_text())
 for line in (EX/"parity_vectors.jsonl").read_text().splitlines():jsonschema.validate(json.loads(line),schema)
