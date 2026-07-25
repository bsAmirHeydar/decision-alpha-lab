from tools.repository_paths import find_repository_root
import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator,FormatChecker
ROOT=find_repository_root(__file__);S=ROOT/'schemas/legacy/strategy_factory/saed_v4_06';E=ROOT/'examples/legacy/strategy_factory/saed_v4_06'
PAIRS=[('institutional_treatment_dsl_registry.json','treatment_dsl_registry.schema.json'),('institutional_treatment_dsl_policy.json','treatment_dsl_policy.schema.json'),('institutional_capability_profile.json','capability_profile.schema.json'),('golden_treatment_program_source.json','treatment_program_source.schema.json'),('system_skip_program_source.json','treatment_program_source.schema.json'),('system_abstain_program_source.json','treatment_program_source.schema.json'),('golden_canonical_treatment_program.json','canonical_treatment_program.schema.json'),('golden_program_validation.json','program_validation_result.schema.json'),('golden_descriptor_binding.json','descriptor_binding.schema.json'),('golden_treatment_dsl_package.json','treatment_dsl_package.schema.json'),('golden_dsl_integrity_receipt.json','dsl_integrity_receipt.schema.json'),('golden_dsl_replay_receipt.json','dsl_replay_receipt.schema.json'),('golden_dsl_diff.json','dsl_diff.schema.json'),('golden_dsl_telemetry.json','dsl_telemetry.schema.json'),('golden_dsl_partition_manifest.json','dsl_partition_manifest.schema.json'),('golden_exposure_ledger.json','exposure_ledger.schema.json'),('golden_conformance_results.json','conformance_results.schema.json'),('conformance_vectors.json','conformance_vectors.schema.json'),('v4_06_to_v4_07_handoff.json','v4_06_to_v4_07_handoff.schema.json'),('schema_catalog.json','schema_catalog.schema.json')]
@pytest.mark.parametrize('example,schema',PAIRS)
def test_example_validates(example,schema):
 d=json.loads((E/example).read_text());s=json.loads((S/schema).read_text());assert not list(Draft202012Validator(s,format_checker=FormatChecker()).iter_errors(d))
@pytest.mark.parametrize('path',sorted(S.glob('*.schema.json')),ids=lambda p:p.name)
def test_schema_is_valid_and_top_level_closed(path):
 s=json.loads(path.read_text());Draft202012Validator.check_schema(s);assert s.get('additionalProperties') is False
