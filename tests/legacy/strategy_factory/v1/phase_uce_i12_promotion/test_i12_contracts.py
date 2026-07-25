from dataclasses import replace
import pytest
from strategy_factory_promotion_v3.contracts import SelectionUniverse, TrialEvidence, PromotionPolicy, ProspectiveChallengeFreeze
from strategy_factory_promotion_v3.enums import TrialDisposition
from strategy_factory_promotion_v3.errors import PromotionError
from strategy_factory_promotion_v3.golden import golden_policy,golden_trials,golden_universe,golden_freeze,h

def test_universe_identity_is_deterministic(): assert golden_universe().universe_hash==golden_universe().universe_hash
def test_universe_counts_every_disposition(): assert sum(golden_universe().disposition_counts().values())==len(golden_universe().trials)
def test_universe_rejects_missing_declared_trial():
    u=golden_universe()
    with pytest.raises(PromotionError,match="trial_universe_count_mismatch"): replace(u,trials=u.trials[:-1])
def test_universe_rejects_incomplete_ledger():
    with pytest.raises(PromotionError,match="incomplete_selection_ledger"): replace(golden_universe(),ledger_complete=False)
def test_duplicate_trial_id_rejected():
    u=golden_universe()
    with pytest.raises(PromotionError,match="duplicate_trial_id"): replace(u,trials=(u.trials[0],)+u.trials[:-1])
def test_invalid_p_value_rejected():
    t=golden_trials()[0]
    with pytest.raises(PromotionError,match="invalid_probability"): replace(t,p_value=1.1)
def test_selected_flag_requires_selected_disposition():
    with pytest.raises(PromotionError,match="selected_disposition_mismatch"): replace(golden_trials()[0],selected=True)
def test_policy_hash_changes_with_threshold(): assert golden_policy().policy_hash!=replace(golden_policy(),maximum_pbo=.2).policy_hash
def test_prospective_freeze_rejects_unfrozen():
    with pytest.raises(PromotionError,match="prospective_challenge_not_frozen"): replace(golden_freeze(),frozen_before_observation=False)
