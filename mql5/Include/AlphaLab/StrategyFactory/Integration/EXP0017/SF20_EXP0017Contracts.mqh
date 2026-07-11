#ifndef __SF20_EXP0017_CONTRACTS_MQH__
#define __SF20_EXP0017_CONTRACTS_MQH__
#include "SF20_EXP0017Config.mqh"
#include <IntermarketDivergenceExecution/CG/CGD_Types.mqh>
struct SF20_EXP0017GroupEvidence{string group_name;int group_minutes;int candidate_count;int missing_data_count;int symmetric_high_count;int symmetric_low_count;long observed_at_utc_msc;string evidence_hash;};
struct SF20_EXP0017MappingRecord{string mapping_id,legacy_divergence_id,legacy_payload_hash,canonical_event_id,canonical_source_hash,cluster_id,adapter_config_hash,adapter_version,reasons;long mapped_at_utc_msc;};
struct SF20_EXP0017LifecycleRecord{string record_id,event_id,reason;ENUM_SF20_LIFECYCLE_STATE state;long first_seen_utc_msc,last_seen_utc_msc,pulse_sequence;};
struct SF20_EXP0017DifferentialRecord{string record_id,legacy_divergence_id,canonical_event_id,legacy_payload_hash,canonical_payload_hash,mismatched_fields;ENUM_SF20_DIFFERENTIAL_STATUS status;long known_time_utc_msc;};
struct SF20_EXP0017Telemetry{long pulses,legacy_candidates_seen,canonical_events_emitted,duplicate_events_suppressed,events_retired,mapping_failures,differential_mismatches,context_passes,candidate_passes,downstream_gates,live_authority_attempts;};
struct SF20_EXP0017StageEvidence{string stage,input_id,output_id,reason_code,detail,evidence_hash;ENUM_SF20_STAGE_STATUS status;long known_time_utc_msc;};
void SF20_ResetTelemetry(SF20_EXP0017Telemetry &t){t.pulses=0;t.legacy_candidates_seen=0;t.canonical_events_emitted=0;t.duplicate_events_suppressed=0;t.events_retired=0;t.mapping_failures=0;t.differential_mismatches=0;t.context_passes=0;t.candidate_passes=0;t.downstream_gates=0;t.live_authority_attempts=0;}
string SF20_LegacyCandidateIdentity(const SCGDDivergenceCandidate &c)
{return c.divergence_id+"|"+c.group_name+"|"+IntegerToString(c.group_minutes)+"|"+IntegerToString((long)c.trading_day_start_ny)+"|"+IntegerToString((long)c.current_cycle_start_ny)+"|"+IntegerToString((long)c.reference_cycle_start_ny)+"|"+IntegerToString((int)c.direction)+"|"+IntegerToString((int)c.side)+"|"+c.hunter_symbol+"|"+c.clean_symbol;}
string SF20_LegacyCandidatePayload(const SCGDDivergenceCandidate &c)
{return SF20_LegacyCandidateIdentity(c)+"|"+SF01_CanonicalDouble(c.hunter_reference_price)+"|"+SF01_CanonicalDouble(c.clean_reference_price)+"|"+SF01_CanonicalDouble(c.hunter_current_extreme)+"|"+SF01_CanonicalDouble(c.clean_current_extreme)+"|"+SF01_CanonicalDouble(c.clean_stop_reference_price)+"|"+c.note;}
#endif
