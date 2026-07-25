from tools.repository_paths import find_repository_root
import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from saed_v4_data_foundation.contracts import load_document,validate_closed
from saed_v4_data_foundation.errors import ContractError
ROOT=find_repository_root(__file__);S=ROOT/'schemas/legacy/strategy_factory/saed_v4_01';E=ROOT/'examples/legacy/strategy_factory/saed_v4_01'
@pytest.mark.parametrize('path',sorted(S.glob('*.schema.json')))
def test_schema_is_valid_and_closed(path):
 s=json.loads(path.read_text());Draft202012Validator.check_schema(s);assert s.get('additionalProperties') is False
@pytest.mark.parametrize('path',sorted(E.glob('*.json')))
def test_example_validates(path): validate_closed(load_document(path),load_document(S/f'{path.stem}.schema.json'))
@pytest.mark.parametrize('doc,schema',[('sovereign_record_unknown_field.json','sovereign_record.schema.json'),('ingestion_batch_non_atomic.json','ingestion_batch.schema.json'),('handoff_wrong_phase.json','phase_handoff_v4_01_to_v4_02.schema.json')])
def test_negative_rejected(doc,schema):
 with pytest.raises(ContractError):validate_closed(load_document(E/'negative'/doc),load_document(S/schema))
