#ifndef __FP_I12_CONTRACTS_MQH__
#define __FP_I12_CONTRACTS_MQH__
#include "FP_I12_Enums.mqh"
struct SFP_I12_Config { string instance_id; string object_namespace; bool panel_enabled; ENUM_FP_I12_PANEL_DOCK dock; ENUM_FP_I12_PANEL_MODE mode; int page_size; bool alerts_enabled; bool alert_popup; bool alert_sound; bool alert_push; bool alert_email; bool suppress_historical; int startup_watermark; int max_alerts_per_minute; bool export_enabled; ENUM_FP_I12_EXPORT_FORMAT export_format; string export_prefix; bool auto_export; string open_decision_state; };
struct SFP_I12_Filter { bool show_al;bool show_an;bool show_ln;bool show_na;bool show_nl;bool show_nn;bool show_ww;bool show_bullish;bool show_bearish;bool show_confirmed;bool show_invalidated;bool show_suppressed;bool show_historical;string focus_semantic_id; };
struct SFP_I12_PanelState { ENUM_FP_I12_PANEL_STATE state;ENUM_FP_I12_PANEL_MODE mode;int page;int page_count;string selected_semantic_id;string state_hash; };
struct SFP_I12_AlertCandidate { string alert_id;ENUM_FP_I12_ALERT_TYPE type;datetime event_time;string title;string message;bool historical; };
struct SFP_I12_AuditRecord { string record_id;datetime event_time;string semantic_id;string record_type;string relation;string direction;string state;string disposition;string reason_codes;string payload_hash; };
struct SFP_I12_Diagnostic { bool ready;long panel_updates;long alert_deliveries;long alert_suppressed;long export_records;string reason_code;string diagnostic_hash; };
#endif
