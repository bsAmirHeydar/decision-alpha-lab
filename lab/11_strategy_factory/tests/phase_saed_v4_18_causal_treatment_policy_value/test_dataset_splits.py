import pytest
from saed_v4_causal_treatment_policy_value.validation import validate_split_plan
from saed_v4_causal_treatment_policy_value.errors import LeakageError

@pytest.mark.parametrize('key', ['row_count','environment_count','cluster_count'])
def test_dataset_positive_counts(load,art,key):assert load(f'{art}/GOLDEN_SYNTHETIC_TREATMENT_DATASET.JSON')[key]>0

def test_dataset_known_time_and_synthetic(load,art):
 d=load(f'{art}/GOLDEN_SYNTHETIC_TREATMENT_DATASET.JSON');assert d['known_time_only'] and d['synthetic_only'] and d['protected_evidence_exposures']==0

def test_all_treatments_observed(load,art):
 d=load(f'{art}/GOLDEN_SYNTHETIC_TREATMENT_DATASET.JSON');assert set(r['assigned_treatment'] for r in d['rows'])==set(d['treatment_ids'])

def test_split_audit_passes(load,art):assert load(f'{art}/GOLDEN_SPLIT_AUDIT.JSON')['passed']

@pytest.mark.parametrize('index',range(4))
def test_fold_is_chronological(load,art,index):
 f=load(f'{art}/GOLDEN_SPLIT_PLAN.JSON')['folds'][index];assert max(f['train_ordinals'])<min(f['evaluation_ordinals']) and not set(f['train_ordinals'])&set(f['evaluation_ordinals'])

def test_future_training_mutation_fails(load,art):
 d=load(f'{art}/GOLDEN_SYNTHETIC_TREATMENT_DATASET.JSON');p=load(f'{art}/GOLDEN_SPLIT_PLAN.JSON');p['folds'][0]['train_ordinals'].append(p['folds'][0]['evaluation_ordinals'][0])
 with pytest.raises(LeakageError):validate_split_plan(p,d)

def test_sibling_mutation_fails(load,art):
 d=load(f'{art}/GOLDEN_SYNTHETIC_TREATMENT_DATASET.JSON');p=load(f'{art}/GOLDEN_SPLIT_PLAN.JSON');ev=p['folds'][0]['evaluation_ordinals'][0];cluster=next(r['cluster_id'] for r in d['rows'] if r['ordinal']==ev);sib=next(r['ordinal'] for r in d['rows'] if r['cluster_id']==cluster and r['ordinal']!=ev);p['folds'][0]['train_ordinals'].append(sib)
 with pytest.raises(LeakageError):validate_split_plan(p,d)

def test_ground_truth_is_nonselectable(load,art):
 g=load(f'{art}/GOLDEN_SYNTHETIC_GROUND_TRUTH.JSON');assert g['benchmark_only'] and not g['selectable'] and not g['visible_to_estimators']
