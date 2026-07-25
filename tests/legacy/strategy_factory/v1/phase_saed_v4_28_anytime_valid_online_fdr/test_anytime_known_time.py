import copy
from saed_v4_anytime_valid_online_fdr.anytime import build_registry
from saed_v4_anytime_valid_online_fdr.contracts import parse_config,parse_hypotheses
from saed_v4_anytime_valid_online_fdr import run

def parsed(config,hypotheses):
    p=parse_config(config); return parse_hypotheses(hypotheses,{x["family_id"] for x in p["family_allocation"]},{x["stopping_rule_id"] for x in p["stopping_rule_registry"]})
def test_registry_count(config,hypotheses): assert build_registry(parsed(config,hypotheses))["record_count"]==36
def test_future_looks_discarded(config,hypotheses): assert build_registry(parsed(config,hypotheses))["future_look_count_discarded"]==3
def test_future_suffix_does_not_change_decisions(config,upstream,hypotheses):
    base=run(config,upstream,hypotheses); bad=copy.deepcopy(hypotheses)
    bad[0]["looks"].append({"look_sequence":4,"known_at":"2030-01-01T00:00:00Z","anytime_p_value":1e-15,"e_value":1e15,"statistic":999.0,"evidence_hash":"f"*64})
    changed=run(config,upstream,bad)
    a=[(x["hypothesis_id"],x["rejected"],x["alpha"]) for x in base["wealth_ledger"]["entries"]]
    b=[(x["hypothesis_id"],x["rejected"],x["alpha"]) for x in changed["wealth_ledger"]["entries"]]
    assert a==b
def test_selected_look_known_at_decision(outputs):
    assert all(r["selected_known_at"]<=r["decision_time"] for r in outputs["anytime_evidence_registry"]["records"])
def test_future_suffix_flag(outputs): assert sum(r["future_suffix_ignored"] for r in outputs["anytime_evidence_registry"]["records"])==3
def test_known_time_review(outputs):
    x=outputs["known_time_review"]; assert x["passed"] and not x["future_suffix_sensitivity"] and x["retroactive_alpha_mutations"]==0
