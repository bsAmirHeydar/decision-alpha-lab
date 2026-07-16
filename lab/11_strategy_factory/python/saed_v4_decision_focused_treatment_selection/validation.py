from .certificates import verify_selection_certificate
from .masks import assert_mask_integrity

def validate_result(result):
    verify_selection_certificate(result['certificate'])
    assert result['baseline_report']['baseline_preserved']
    assert result['decision']['fallback'] in {'none','skip'}
    assert result['certificate']['research_only'] and not result['certificate']['runtime_executable']
    assert result['budget_snapshot']['hidden_evaluation_queries']==0 and result['budget_snapshot']['protected_evidence_exposure']==0
    return True
