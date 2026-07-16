from __future__ import annotations
from .abstention import calibrate as calibrate_abstention
from .authority import boundary
from .budget import ResearchLedger
from .canonical import content_hash
from .certificate import build as build_certificate, handoff as build_handoff
from .conformal import fit as fit_conformal, lower_bound, retrospective_coverage
from .contracts import (
    AbstentionContract, CalibrationDatasetContract, ConformalContract, CoverageRiskContract,
    DriftContract, OODContract, ResearchBudget, SelectiveControlContract, UpstreamIntakeContract,
)
from .coverage import build as build_coverage_risk
from .dataset import by_role, validate
from .drift import assess as assess_drift
from .ood import evaluate as evaluate_ood, fit as fit_ood
from .replay import receipt as replay_receipt
from .security import scan
from .selective import decide
from .upstream import verify

def run(config, upstream_documents, records):
    scan(config)
    scan(upstream_documents)
    scan(records)
    upstream_contract = UpstreamIntakeContract.from_mapping(config['upstream_intake'])
    dataset_contract = CalibrationDatasetContract.from_mapping(config['calibration_dataset_contract'])
    conformal_contract = ConformalContract.from_mapping(config['conformal_contract'])
    ood_contract = OODContract.from_mapping(config['ood_contract'])
    selective_contract = SelectiveControlContract.from_mapping(config['selective_control_contract'])
    coverage_contract = CoverageRiskContract.from_mapping(config['coverage_risk_contract'])
    abstention_contract = AbstentionContract.from_mapping(config['abstention_contract'])
    drift_contract = DriftContract.from_mapping(config['drift_contract'])
    budget_contract = ResearchBudget.from_mapping(config['research_budget'])
    ledger = ResearchLedger(budget_contract)
    upstream = verify(upstream_contract, upstream_documents)
    dataset = validate(records, dataset_contract, ledger)
    roles = by_role(records)
    calibrator = fit_conformal(records, conformal_contract, ledger)
    detector = fit_ood(records, ood_contract, ledger)
    selection_records = roles['selection_validation']
    calibration_records = roles['calibration']
    drift_records = roles['drift_reference']
    conformal_bounds = [lower_bound(record, calibrator) for record in selection_records]
    selection_ood = [evaluate_ood(record, detector, ood_contract, calibration_records) for record in selection_records]
    decisions = [decide(record, bound, ood_result, selective_contract, ledger) for record, bound, ood_result in zip(selection_records, conformal_bounds, selection_ood)]
    coverage = retrospective_coverage(selection_records, calibrator)
    frontier = build_coverage_risk(decisions, selection_records, coverage_contract, ledger)
    abstention = calibrate_abstention(frontier, abstention_contract)
    drift_ood = [evaluate_ood(record, detector, ood_contract, calibration_records) for record in drift_records]
    drift = assess_drift(detector, drift_ood, drift_contract, ledger)
    trial = {
        'phase': 'SAED_V4_24',
        'trials': [
            {'trial_id': 'trial_conformal_001', 'family': 'split_mondrian_conformal', 'status': 'completed', 'promotion_eligible': False},
            {'trial_id': 'trial_ood_001', 'family': 'robust_support_aware_ood', 'status': 'completed', 'promotion_eligible': False},
            {'trial_id': 'trial_selective_001', 'family': 'coverage_risk_selective_control', 'status': 'completed', 'promotion_eligible': False},
        ],
        'complete': True,
    }
    trial['ledger_hash'] = content_hash(trial)
    exposure = {
        'phase': 'SAED_V4_24',
        'hidden_evaluation_queries': 0,
        'protected_evidence_exposures': 0,
        'runtime_compilations': 0,
        'order_submissions': 0,
        'online_policy_mutations': 0,
        'complete': True,
    }
    exposure['ledger_hash'] = content_hash(exposure)
    budget = ledger.snapshot()
    authority = boundary()
    certificate = build_certificate(upstream, dataset, calibrator, detector, coverage, frontier, abstention, drift, budget, trial, exposure, authority)
    handoff = build_handoff(certificate, frontier, drift)
    outputs = {
        'upstream_receipt': upstream,
        'dataset_summary': dataset,
        'conformal_calibrator': calibrator,
        'conformal_bounds': conformal_bounds,
        'retrospective_coverage': coverage,
        'ood_detector': detector,
        'selection_ood_evaluations': selection_ood,
        'selective_decisions': decisions,
        'coverage_risk_frontier': frontier,
        'abstention_policy': abstention,
        'drift_ood_evaluations': drift_ood,
        'drift_report': drift,
        'trial_ledger': trial,
        'exposure_ledger': exposure,
        'budget_snapshot': budget,
        'authority_boundary': authority,
        'certificate': certificate,
        'handoff': handoff,
    }
    outputs['replay_receipt'] = replay_receipt(
        content_hash(config),
        {'upstream_documents': content_hash(upstream_documents), 'records': content_hash(records)},
        {key: content_hash(value) for key, value in outputs.items()},
    )
    return outputs
