from src.engine.tooling.strategy_factory.lcm.lcm_09b.canonical import digest_object
from .conftest import ROOT,j

def test_required_artifact_locator_is_complete_and_digest_bound():
 d=j("required_artifact_locator.json"); assert digest_object(d,"locator_digest")==d["locator_digest"]
 expected={"canonical_setup_packages","setup_adapter_registry.json","setup_factory_registration.json","setup_golden_cases.jsonl","setup_golden_traces.jsonl","setup_parity_registry.json","setup_variance_decisions.json","LCM09B_TO_LCM10A_HANDOFF.json"}
 assert set(d["artifacts"])==expected
 for name,item in d["artifacts"].items():
  if isinstance(item,str): assert (ROOT/item.rstrip("/")).is_dir()
  else: assert (ROOT/item["path"]).is_file()

def test_exact_named_handoff_is_byte_equivalent():
 assert (ROOT/"LCM09B_TO_LCM10A_HANDOFF.json").read_bytes()==(ROOT/"handoff/lcm09b_to_lcm10a_handoff.json").read_bytes()
