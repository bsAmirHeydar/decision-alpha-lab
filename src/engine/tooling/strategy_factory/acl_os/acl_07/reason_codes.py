from __future__ import annotations
REASON_CODES={
 'ACL06_BUNDLE_VERIFIED':'The complete ACL-06 generated root passed integrity checks.',
 'UPSTREAM_KNOWN_TIME_AND_SPLIT_EVIDENCE_VERIFIED':'Known-time and purged-split evidence is bound from ACL-06.',
 'DIAGNOSTIC_LANE_NON_SELECTABLE':'Diagnostic evidence is visible but cannot enter selection or promotion.',
 'RESEARCH_LANE_CONFIRMED':'Candidate belongs to the research lane.',
 'INSUFFICIENT_TOTAL_OR_TEST_SUPPORT':'Total or held-out support is below the frozen threshold.',
 'EFFECT_THRESHOLD_NOT_MET':'Directional effect or signed result is below policy.',
 'SIGNIFICANCE_OR_CONFIDENCE_BOUND_NOT_MET':'Nominal p-value or Wilson lower bound did not clear policy.',
 'FDR_THRESHOLD_NOT_MET':'Family-corrected q-value did not clear policy.',
 'BASELINE_DOMINANCE_NOT_ESTABLISHED':'Held-out behavior did not exceed the best baseline by the required margin.',
 'SEGMENT_GENERALIZATION_NOT_ESTABLISHED':'Train, validation and test behavior is missing or unstable.',
 'OVERFIT_CONTROL_BATTERY_NOT_CLEARED':'Overfit controls did not clear.',
 'TAIL_EVIDENCE_INSUFFICIENT_OR_ADVERSE':'Tail sample is too small or adverse.',
 'EXECUTION_ECONOMICS_EVIDENCE_MISSING':'Side-aware cost and fill evidence is absent.',
 'OOD_EVIDENCE_MISSING':'Out-of-distribution and selective-control evidence is absent.',
 'PROSPECTIVE_EVIDENCE_MISSING':'No frozen prospective run is bound.',
 'INDEPENDENT_REPLICATION_MISSING':'No independent replication is bound.',
 'CANDIDATE_IS_BASELINE':'Baseline artifacts are reference comparators, not promotable candidates.',
 'DIAGNOSTIC_LANE_EXCLUDED_FROM_TESTING_FAMILY':'Diagnostic candidate is excluded from multiple-testing family.',
 'ONE_OR_MORE_REQUIRED_GATES_NOT_PASSED':'At least one required gate is FAIL or UNKNOWN.',
 'BASELINE_NOT_PROMOTABLE':'Baseline remains a comparator only.',
 'ALL_REFERENCE_GATES_PASSED':'All registered reference gates passed; reporting only, not promotion.'
}
