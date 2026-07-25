import copy,pytest
from saed_v4_decision_focused_treatment_selection.treatment_universe import compile_treatment_universe,treatment_by_id
from saed_v4_decision_focused_treatment_selection.contracts import ConstraintContract
from saed_v4_decision_focused_treatment_selection.masks import compile_action_mask,assert_mask_integrity
from saed_v4_decision_focused_treatment_selection.errors import TreatmentUniverseError

def test_universe_is_sorted_frozen_and_hashed(config):
 u=compile_treatment_universe(config['treatment_universe']);assert u['enabled_treatments']==sorted(u['enabled_treatments']);assert u['closed_world'] and not u['runtime_mutation_allowed'];assert len(u['universe_hash'])==64

def test_unknown_treatment_rejected(config):
 u=compile_treatment_universe(config['treatment_universe'])
 with pytest.raises(TreatmentUniverseError):treatment_by_id(u,'UNKNOWN')

def test_golden_mask_integrity(config,context,proofs):
 u=compile_treatment_universe(config['treatment_universe']);c=ConstraintContract.from_mapping(config['constraints']);m=compile_action_mask(context,u,c,proofs);assert assert_mask_integrity(m,u);assert all(r['allowed'] for r in m['rows'])
@pytest.mark.parametrize('mutation,reason',[
 ('support','insufficient_support'),('overlap','positivity_or_overlap_failure'),('estimated_cost','cost_limit'),('proof','proof_missing_or_mismatched')])
def test_mask_failure_reasons(config,context,proofs,mutation,reason):
 c=copy.deepcopy(context);p=copy.deepcopy(proofs);tid='T_BALANCED'
 if mutation=='support':c['support'][tid]=0
 elif mutation=='overlap':c['overlap'][tid]=0.0
 elif mutation=='estimated_cost':c['estimated_cost'][tid]=99.0
 else:c['proof_hashes'][tid]='tampered'
 u=compile_treatment_universe(config['treatment_universe']);cc=ConstraintContract.from_mapping(config['constraints']);m=compile_action_mask(c,u,cc,p);row=next(x for x in m['rows'] if x['treatment_id']==tid);assert not row['allowed'] and reason in row['reasons']

def test_empty_mask_fails_to_skip(config,context,proofs):
 c=copy.deepcopy(context)
 for tid in c['support']:c['support'][tid]=0
 u=compile_treatment_universe(config['treatment_universe']);cc=ConstraintContract.from_mapping(config['constraints']);m=compile_action_mask(c,u,cc,proofs);allowed=[r['treatment_id'] for r in m['rows'] if r['allowed']];assert allowed==['SKIP']
