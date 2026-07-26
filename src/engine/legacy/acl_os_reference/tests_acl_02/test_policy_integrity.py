import hashlib,json,yaml
from src.engine.tooling.strategy_factory.acl_os.acl_02.policies import POLICY_ROOT,SCHEMA_ROOT

def test_policy_files_parse():
 for p in POLICY_ROOT.glob("*.yaml"):assert isinstance(yaml.safe_load(p.read_text()),dict)
def test_no_duplicate_question_ids():
 q=yaml.safe_load((POLICY_ROOT/"question_catalog.yaml").read_text())["questions"];ids=[x["question_id"] for x in q];assert len(ids)==len(set(ids))
def test_no_duplicate_requirement_ids():
 q=yaml.safe_load((POLICY_ROOT/"requirement_catalog.yaml").read_text())["requirements"];ids=[x["requirement_id"] for x in q];assert len(ids)==len(set(ids))
def test_schemas_closed():
 for p in SCHEMA_ROOT.glob("*.schema.json"):
  o=json.loads(p.read_text());assert o.get("additionalProperties") is False
def test_no_execution_authority():
 for p in POLICY_ROOT.glob("*.yaml"):
  text=p.read_text().lower();assert "live_order_submission_allowed: true" not in text;assert "capital_activation_allowed: true" not in text
