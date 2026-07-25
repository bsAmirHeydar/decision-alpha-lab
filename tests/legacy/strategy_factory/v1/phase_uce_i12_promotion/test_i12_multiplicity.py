from dataclasses import replace
import numpy as np
from strategy_factory_promotion_v3.enums import CorrectionMethod,DecisionRole
from strategy_factory_promotion_v3.golden import *
from strategy_factory_promotion_v3.multiplicity import *

def test_bonferroni_exact(): assert np.allclose(adjust_p_values([.01,.02],CorrectionMethod.BONFERRONI),[.02,.04])
def test_holm_monotone():
    q=adjust_p_values([.01,.04,.03],CorrectionMethod.HOLM); assert np.all((q>=0)&(q<=1))
def test_bh_preserves_input_order():
    q=adjust_p_values([.04,.001,.02],CorrectionMethod.BENJAMINI_HOCHBERG); assert q[1]<q[2]<q[0]
def test_by_is_not_less_conservative_than_bh():
    p=[.001,.01,.03,.2]; assert np.all(adjust_p_values(p,CorrectionMethod.BENJAMINI_YEKUTIELY)>=adjust_p_values(p,CorrectionMethod.BENJAMINI_HOCHBERG))
def test_missing_p_values_still_count():
    r=multiplicity_report(golden_universe(),golden_family_definition()); assert r.total_choice_count==9 and r.missing_p_value_count==6
def test_family_definition_changes_identity():
    d=golden_family_definition(); assert multiplicity_report(golden_universe(),d).family_definition_hash!=multiplicity_report(golden_universe(),replace(d,dimensions=('family_id',))).family_definition_hash
def test_trial_universe_reconciliation_passes():
    ids=[t.trial_id for t in golden_universe().trials]; assert reconcile_trial_universe(golden_universe(),ids,ids)['complete']
def test_trial_universe_reconciliation_detects_omission():
    ids=[t.trial_id for t in golden_universe().trials]; assert not reconcile_trial_universe(golden_universe(),ids[:-1],ids)['complete']
def test_nested_selection_passes_when_disjoint_and_frozen(): assert audit_nested_selection(['a'],['b'],['c'],declaration_frozen=True,confirmation_role=DecisionRole.CONFIRMATION)['passed']
def test_nested_selection_rejects_overlap(): assert 'nested_selection_overlap' in audit_nested_selection(['a'],['a'],['c'],declaration_frozen=True,confirmation_role=DecisionRole.CONFIRMATION)['blockers']
