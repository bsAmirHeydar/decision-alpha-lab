import pytest
from saed_v4_baseline_manual.corpus import build_pretraining_corpus_manifest
from saed_v4_baseline_manual.validation import validate_corpus_manifest
from saed_v4_baseline_manual.errors import LeakageError

def test_outcomes_excluded(upstream):
 v,h,l,_=upstream;m=build_pretraining_corpus_manifest(v,h,l);included={x['artifact_class'] for x in m['included_artifacts']};assert 'outcome_cube' not in included and 'execution_twin' not in included;assert m['self_supervised_only'];assert m['label_semantics']=='none';assert not m['training_authority']
def test_tampered_corpus_fails(upstream):
 v,h,l,_=upstream;m=build_pretraining_corpus_manifest(v,h,l);m['included_artifacts'].append({'artifact_class':'outcome_cube'})
 with pytest.raises(LeakageError):validate_corpus_manifest(m)
