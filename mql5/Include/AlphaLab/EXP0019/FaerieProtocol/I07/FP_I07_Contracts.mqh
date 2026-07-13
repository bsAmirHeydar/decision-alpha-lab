#ifndef FP_I07_CONTRACTS_MQH
#define FP_I07_CONTRACTS_MQH
#include "FP_I07_Enums.mqh"
struct SFP_I07_Config { string context_id; string pair_id; string host_symbol; ENUM_TIMEFRAMES host_timeframe; int host_seconds; string config_hash; };
struct SFP_I07_HostBar { string bar_id; string symbol; ENUM_TIMEFRAMES timeframe; datetime open_time; datetime close_time; double open_price; double high_price; double low_price; double close_price; bool is_closed; bool coverage_complete; string m1_hash; string revision_id; string bar_hash; };
struct SFP_I07_Projection { string projection_id; string candidate_id; string owner_session_id; datetime candidate_time; datetime deadline; string target_bar_id; datetime target_open; datetime target_close; string config_hash; string projection_hash; };
struct SFP_I07_Observation { string observation_id; string candidate_id; string bar_id; ENUM_FP_I07_CLOSE_PAIR_STATE pair_state; datetime available_through; string revision_id; string evidence_hash; string reason_code; };
struct SFP_I07_Result { string result_id; string candidate_id; ENUM_FP_I07_OUTCOME outcome; ENUM_FP_I07_CONFIRMATION_STATE state; string signal_id; datetime finalized_at; string reason_code; string result_hash; };
#endif
