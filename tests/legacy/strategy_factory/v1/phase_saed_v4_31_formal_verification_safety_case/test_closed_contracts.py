from tools.repository_paths import find_repository_root
import copy,json,pytest
from pathlib import Path
ROOT=find_repository_root(__file__); AR=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_31"; SC=ROOT/"schemas/legacy/strategy_factory/saed_v4_31"
from tools.strategy_factory.saed_v4_31._schema_validator import validate
NAMES=sorted(x.name for x in AR.glob("*.JSON"))
@pytest.mark.parametrize("name",NAMES)
def test_golden_schema_pair(name):
 value=json.loads((AR/name).read_text()); schema=json.loads((SC/name.replace(".JSON",".SCHEMA.JSON")).read_text()); validate(value,schema)
@pytest.mark.parametrize("name",NAMES)
def test_unknown_field_rejected(name):
 value=json.loads((AR/name).read_text()); schema=json.loads((SC/name.replace(".JSON",".SCHEMA.JSON")).read_text()); value["__unknown__"]=True
 with pytest.raises(AssertionError): validate(value,schema)
