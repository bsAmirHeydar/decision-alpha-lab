import json
from pathlib import Path
import jsonschema

def test_all_schemas_are_closed(root):
 paths=sorted((root/'schemas/legacy/strategy_factory/saed_v4_10').glob('*.schema.json'));assert len(paths)>=19
 for p in paths:
  s=json.loads(p.read_text());jsonschema.Draft202012Validator.check_schema(s);assert s.get('additionalProperties') is False

def test_golden_contract_pairs(root):
 base=root/'lab/11_strategy_factory';pairs=[('manual_program_source.schema.json','examples/saed_v4_10/manual_doctrine_reference_v1.json'),('compiled_manual_program.schema.json','artifacts/saed_v4_10/GOLDEN_COMPILED_MANUAL_PROGRAM_1.JSON'),('decision_trace.schema.json','artifacts/saed_v4_10/GOLDEN_DECISION_TRACE_1.JSON'),('baseline_registry.schema.json','artifacts/saed_v4_10/GOLDEN_BASELINE_REGISTRY.JSON'),('benchmark_result.schema.json','artifacts/saed_v4_10/GOLDEN_BENCHMARK_RESULT.JSON'),('pretraining_corpus_manifest.schema.json','artifacts/saed_v4_10/GOLDEN_PRETRAINING_CORPUS_MANIFEST.JSON'),('handoff.schema.json','artifacts/saed_v4_10/V4_10_TO_V4_11_HANDOFF.JSON')]
 for sf,af in pairs:
  s=json.loads((base/'schemas/saed_v4_10'/sf).read_text());a=json.loads((base/af).read_text());jsonschema.validate(a,s)
