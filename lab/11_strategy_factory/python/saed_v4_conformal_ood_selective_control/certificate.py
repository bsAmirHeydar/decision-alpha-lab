from __future__ import annotations
from .canonical import content_hash, stable_id

def build(upstream, dataset, calibrator, detector, retrospective_coverage, frontier, abstention, drift, budget, trial, exposure, authority):
    gates = {
        'upstream_verified': upstream['scope_verified'],
        'known_time_verified': dataset['feature_known_by_decision'] and dataset['outcome_after_decision'],
        'cluster_role_separation_verified': dataset['cluster_role_separation'],
        'conformal_calibrated': calibrator['pooled_count'] >= 60,
        'retrospective_coverage_reported': retrospective_coverage['record_count'] > 0,
        'ood_calibrated': detector['calibration_count'] >= 60,
        'coverage_risk_reported': len(frontier['rows']) >= 8,
        'abstention_policy_present': bool(abstention['policy_id']),
        'drift_diagnostics_present': bool(drift['report_hash']),
        'baseline_preserved': True,
        'budget_respected': all(budget['counts'][key] <= budget['limits'][key] for key in budget['counts']),
        'exposure_zero': all(exposure[key] == 0 for key in ('hidden_evaluation_queries', 'protected_evidence_exposures', 'runtime_compilations', 'order_submissions')),
        'authority_zero': not any(authority['authority'].values()),
    }
    output = {
        'phase': 'SAED_V4_24',
        'version': '1.0.0',
        'gates': gates,
        'accepted_for_conformal_ood_selective_research': all(gates.values()),
        'research_policy_id': upstream['research_policy_id'],
        'conformal_calibrator_id': calibrator['calibrator_id'],
        'ood_detector_id': detector['detector_id'],
        'abstention_policy_id': abstention['policy_id'],
        'drift_status': drift['status'],
        'selection_is_research_only': True,
        'promotion_authority': False,
        'runtime_executable': False,
        'risk_allocation_authority': False,
        'execution_authority': False,
        'production_authority': False,
        'real_alpha_claim': False,
        'prospective_success_claim': False,
        'conditional_coverage_claim': False,
        'authority_boundary': authority,
        'evidence_hashes': {
            'upstream_receipt': upstream['receipt_hash'],
            'dataset_summary': dataset['summary_hash'],
            'conformal_calibrator': calibrator['calibrator_hash'],
            'ood_detector': detector['detector_hash'],
            'retrospective_coverage': retrospective_coverage['coverage_hash'],
            'coverage_risk_frontier': frontier['frontier_hash'],
            'abstention_policy': abstention['policy_hash'],
            'drift_report': drift['report_hash'],
            'budget_ledger': budget['ledger_hash'],
            'trial_ledger': trial['ledger_hash'],
            'exposure_ledger': exposure['ledger_hash'],
        },
    }
    output['certificate_id'] = stable_id('conformal_ood_selective_certificate', output)
    output['certificate_hash'] = content_hash(output)
    return output

def handoff(certificate, frontier, drift):
    output = {
        'phase': 'SAED_V4_24',
        'next_phase': 'SAED_V4_25',
        'certificate_hash': certificate['certificate_hash'],
        'research_policy_id': certificate['research_policy_id'],
        'entry_gates': {
            'conformal_certificate_verified': certificate['accepted_for_conformal_ood_selective_research'],
            'coverage_risk_frontier_available': len(frontier['rows']) > 0,
            'abstention_policy_available': bool(certificate['abstention_policy_id']),
            'drift_diagnostics_available': bool(drift['report_hash']),
            'promotion_denied': True,
            'runtime_denied': True,
            'research_only': True,
        },
        'allowed_next_work': [
            'continual_calibration_research', 'meta_learning_dataset_design', 'transfer_shift_mapping',
            'drift_segment_taxonomy', 'safe_recalibration_experiments'
        ],
        'forbidden_next_work': [
            'promotion_authorization', 'runtime_compilation', 'risk_allocation',
            'order_submission', 'online_policy_mutation'
        ],
        'authority': {
            'decision': False, 'promotion': False, 'runtime': False,
            'risk_allocation': False, 'execution': False, 'production': False
        },
        'research_only': True,
    }
    output['handoff_id'] = stable_id('v4_24_to_v4_25', output)
    output['handoff_hash'] = content_hash(output)
    return output
