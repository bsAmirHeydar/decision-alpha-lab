import pytest
from saed_v4_anytime_valid_online_fdr.contracts import parse_config
from saed_v4_anytime_valid_online_fdr.allocation import group
from saed_v4_anytime_valid_online_fdr.procedures import run_all
@pytest.mark.parametrize("procedure",["alpha_spending","alpha_investing","lord_plus_plus","saffron","addis","e_lond"])
def test_each_procedure_runs(config,outputs,procedure):
    row=next(x for x in outputs["challenger_comparison"]["rows"] if x["procedure"]==procedure)
    assert row["hypothesis_count"]==36 and row["minimum_wealth"]>=0 and row["promotion_authority"] is False
@pytest.mark.parametrize("field",["all_wealth_nonnegative","all_alpha_nonnegative"])
def test_wealth_invariants(outputs,field): assert outputs["wealth_ledger"][field]
def test_wealth_chain(outputs): assert outputs["wealth_ledger"]["chain_verification"]["verified"]
def test_rejection_chain(outputs): assert outputs["rejection_ledger"]["chain_verification"]["verified"]
def test_rejections_cross_threshold(outputs):
    for e in outputs["rejection_ledger"]["entries"]: assert e["anytime_p_value"]<=e["alpha"]
def test_alpha_never_negative(outputs): assert min(e["alpha"] for e in outputs["wealth_ledger"]["entries"])>=0
def test_wealth_never_negative(outputs): assert min(e["wealth_after"] for e in outputs["wealth_ledger"]["entries"])>=0
def test_sequence_contiguous(outputs): assert [e["sequence"] for e in outputs["wealth_ledger"]["entries"]]==list(range(1,37))
def test_family_local_indices(outputs):
    for fid in {e["family_id"] for e in outputs["wealth_ledger"]["entries"]}: assert [e["family_local_index"] for e in outputs["wealth_ledger"]["entries"] if e["family_id"]==fid]==list(range(1,7))
def test_synthetic_fixture_has_rejections(outputs): assert outputs["rejection_ledger"]["rejection_count"]>=6
def test_synthetic_fixture_fdp(outputs): assert outputs["online_fdr_audit"]["synthetic_empirical_fdp"]==0
def test_online_fdr_audit_passes(outputs): assert outputs["online_fdr_audit"]["passed"]
@pytest.mark.parametrize("gate",["wealth_nonnegative","alpha_nonnegative","wealth_chain_verified","rejection_chain_verified","rejection_requires_crossing","synthetic_empirical_fdp_within_target"])
def test_fdr_gate(outputs,gate): assert outputs["online_fdr_audit"]["gates"][gate]
def test_family_allocation_sum(outputs): assert abs(outputs["family_allocation"]["weight_sum"]-1)<1e-12
def test_allocation_predictable(outputs): assert outputs["family_allocation"]["predictable"] and not outputs["family_allocation"]["retroactive_reallocation"]
