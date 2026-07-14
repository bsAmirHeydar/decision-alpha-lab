#ifndef __FP_I10_OUTPUT_BUFFERS_MQH__
#define __FP_I10_OUTPUT_BUFFERS_MQH__
#include "FP_I10_Contracts.mqh"
void FP_I10_ClearOutput(SFP_I10_Output &o){ o.health_code=0;o.lifecycle_code=0;o.data_readiness_code=0;o.active_ww_direction=0;o.confirmed_signal_count=0;o.allowed_signal_count=0;o.suppressed_by_ww_count=0;o.suppressed_by_quota_count=0;o.quota_winner_present=0;o.ledger_event_count=0;o.source_revision_sequence=0;o.heartbeat_utc_minute=0;o.snapshot_hash=""; }
#endif
