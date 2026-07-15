#ifndef ALPHALAB_QUALIFICATION_DIFFERENTIAL_EVIDENCE_MQH
#define ALPHALAB_QUALIFICATION_DIFFERENTIAL_EVIDENCE_MQH
struct ALDifferentialEvidence { string case_id; string expected_hash; string observed_hash; double max_abs_error; double max_rel_error; double allowed_abs_error; double allowed_rel_error; int mismatch_count; int future_read_count; int reordered_event_count; };
bool ALDifferentialEvidencePasses(const ALDifferentialEvidence &evidence){ const bool exact=(evidence.expected_hash==evidence.observed_hash); const bool tolerance=(evidence.max_abs_error<=evidence.allowed_abs_error && evidence.max_rel_error<=evidence.allowed_rel_error); return evidence.mismatch_count==0 && evidence.future_read_count==0 && evidence.reordered_event_count==0 && (exact || tolerance); }
#endif
