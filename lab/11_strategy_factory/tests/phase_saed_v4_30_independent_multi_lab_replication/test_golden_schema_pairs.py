import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[4]
AR=ROOT/"lab/11_strategy_factory/artifacts/saed_v4_30"
SC=ROOT/"lab/11_strategy_factory/schemas/saed_v4_30"
ARTIFACTS=sorted(p.name for p in AR.glob("*.JSON"))
@pytest.mark.parametrize("name",ARTIFACTS)
def test_golden_artifact_matches_closed_schema(name):
 value=json.loads((AR/name).read_text()); schema=json.loads((SC/name.replace(".JSON",".SCHEMA.JSON")).read_text()); Draft202012Validator(schema).validate(value)
@pytest.mark.parametrize("name",ARTIFACTS)
def test_closed_schema_rejects_unknown_root_field(name):
 value=json.loads((AR/name).read_text()); schema=json.loads((SC/name.replace(".JSON",".SCHEMA.JSON")).read_text()); value["__unknown__"]=True
 with pytest.raises(Exception): Draft202012Validator(schema).validate(value)
