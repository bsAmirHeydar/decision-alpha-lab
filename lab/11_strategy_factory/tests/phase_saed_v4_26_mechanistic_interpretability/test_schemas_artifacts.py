from __future__ import annotations
import json, pytest
import jsonschema

def closed(x):
 if isinstance(x,dict):
  if x.get("type")=="object" and x.get("additionalProperties") is not False: return False
  return all(closed(v) for v in x.values())
 if isinstance(x,list): return all(closed(v) for v in x)
 return True

def test_schema_pairs_are_closed():
 from conftest import EXAMPLES,ARTIFACTS,SCHEMAS,load
 instances=sorted(EXAMPLES.glob("*.JSON"))+sorted(ARTIFACTS.glob("*.JSON"))
 assert len(instances)==39
 for p in instances:
  s=load(SCHEMAS/f"{p.stem}.SCHEMA.JSON"); assert closed(s); jsonschema.validate(load(p),s,cls=jsonschema.Draft202012Validator)
@pytest.mark.parametrize("directory_name",["examples","artifacts"])
def test_unknown_field_rejected(directory_name):
 from conftest import EXAMPLES,ARTIFACTS,SCHEMAS,load
 d=EXAMPLES if directory_name=="examples" else ARTIFACTS
 for p in sorted(d.glob("*.JSON"))[:8]:
  value=load(p); schema=load(SCHEMAS/f"{p.stem}.SCHEMA.JSON")
  if isinstance(value,dict):
   value=dict(value); value["unknown_field"]=1
   with pytest.raises(jsonschema.ValidationError): jsonschema.validate(value,schema,cls=jsonschema.Draft202012Validator)

