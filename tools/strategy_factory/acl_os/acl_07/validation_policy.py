from __future__ import annotations
from typing import Any
from .canonical import verify_embedded_digest
from .errors import PolicyError
from .schema_validation import validate_instance

def validate_policy(policy:dict[str,Any])->dict[str,Any]:
    validate_instance('validation_policy',policy)
    if not verify_embedded_digest(policy,'policy_digest'): raise PolicyError('policy digest invalid')
    t=policy['thresholds']
    numeric=['minimum_total_support','minimum_test_support','minimum_coverage','maximum_coverage','minimum_accuracy','minimum_wilson_lower','minimum_effect_over_chance','maximum_fdr_q','minimum_baseline_accuracy_advantage','maximum_train_test_accuracy_gap','maximum_segment_accuracy_spread','minimum_tail_observations','maximum_single_loss','minimum_prospective_runs','minimum_independent_replications']
    if any(k not in t for k in numeric): raise PolicyError('threshold set incomplete')
    if t['minimum_coverage']<0 or t['maximum_coverage']>1 or t['minimum_coverage']>t['maximum_coverage']: raise PolicyError('coverage thresholds invalid')
    if t['maximum_fdr_q']<=0 or t['maximum_fdr_q']>1: raise PolicyError('FDR threshold invalid')
    if policy['diagnostic_lane_selectable'] or policy['promotion_authority_granted'] or policy['execution_authority_granted']: raise PolicyError('authority escalation in policy')
    return policy
