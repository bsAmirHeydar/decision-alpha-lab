from tools.repository_paths import find_repository_root
import copy, json, pytest, jsonschema
from pathlib import Path
from saed_v4_complete_search_exposure_ledger import run

def test_budget_within(outputs): assert outputs["budget_snapshot"]["within_budget"]
def test_budget_forbidden_zero(outputs):
    c=outputs["budget_snapshot"]["counts"]
    assert all(c[k]==0 for k in ["hidden_evaluation_queries","protected_exposures","runtime_compilations","order_submissions","online_mutations"])
def test_replay_deterministic(outputs): assert outputs["replay_receipt"]["deterministic"]
def test_replay_network_off(outputs): assert outputs["replay_receipt"]["network_access"] is False
def test_repeat_exact(config,upstream,manifests,trials,exposures,outputs): assert run(config,upstream,manifests,trials,exposures)==outputs
def test_future_suffix_invariance(config,upstream,manifests,trials,exposures,outputs):
    bad=copy.deepcopy(exposures)
    for e in bad: e["metadata"]["unobserved_future_suffix"]=[999,999]
    # Unknown nested metadata is intentionally ledgered; core trial/exposure counts and identities change, authority does not.
    changed=run(config,upstream,manifests,trials,bad)
    assert changed["authority_boundary"]==outputs["authority_boundary"]
    assert changed["certificate"]["promotion_authority"] is False

def test_all_schema_pairs_validate():
    root=find_repository_root(__file__); ex=root/"examples/legacy/strategy_factory/saed_v4_27"; ar=root/"releases/history/strategy_factory/artifacts/saed_v4_27"; sc=root/"schemas/legacy/strategy_factory/saed_v4_27"
    files=list(ex.glob("*.JSON"))+list(ar.glob("*.JSON")); assert len(files)==25
    for p in files:
        schema=json.loads((sc/(p.stem+".SCHEMA.JSON")).read_text()); obj=json.loads(p.read_text()); jsonschema.Draft202012Validator.check_schema(schema); jsonschema.validate(obj,schema)
def test_schema_unknown_root_rejected():
    root=find_repository_root(__file__); p=root/"releases/history/strategy_factory/artifacts/saed_v4_27/GOLDEN_COMPLETENESS_AUDIT.JSON"; s=root/"schemas/legacy/strategy_factory/saed_v4_27/GOLDEN_COMPLETENESS_AUDIT.SCHEMA.JSON"
    obj=json.loads(p.read_text()); obj["unknown"]=1
    with pytest.raises(jsonschema.ValidationError): jsonschema.validate(obj,json.loads(s.read_text()))
