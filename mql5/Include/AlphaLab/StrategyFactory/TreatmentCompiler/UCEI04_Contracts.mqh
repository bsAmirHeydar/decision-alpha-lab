#ifndef __UCEI04_CONTRACTS_MQH__
#define __UCEI04_CONTRACTS_MQH__
#include "../TreatmentAtoms/UCEI03_All.mqh"
#include "UCEI04_Enums.mqh"
struct UCEI04_AtomSelection{ENUM_UCEI03_ATOM_KIND role;string exact_key;UCEI03_ParameterPacket parameters;string alias;string selection_id;};
struct UCEI04_IntrabarPolicy{string policy_id;string version;ENUM_UCEI04_AMBIGUITY_POLICY ambiguity;ENUM_UCEI04_GAP_POLICY gap;ENUM_UCEI04_STALE_POLICY stale_policy;long max_quote_age_ms;long latency_ms;string definition_id;};
struct UCEI04_RuleFinding{string rule_definition_id;bool passed;bool fatal;string code;string message;string evidence_json;};
struct UCEI04_ActionStep{int sequence;string phase;string action_type;string source_exact_key;string source_plan_id;int priority;string payload_json;};
struct UCEI04_TreatmentDraft{string draft_name;ENUM_UCEI03_SIDE side;int runtime_mode;ENUM_UCEI04_COMPILER_MODE compiler_mode;UCEI04_AtomSelection selections[];UCEI04_IntrabarPolicy intrabar;string required_capabilities_csv;bool pinned;string tags_json;string draft_id;};
struct UCEI04_CompiledTreatment{string treatment_id;string draft_id;string context_occurrence_id;string feature_frame_hash;ENUM_UCEI03_SIDE side;long decision_time_ms;UCEI03_EntryPlan entry;UCEI03_StopPlan stop;UCEI03_TargetPlan target;UCEI03_TrailingPlan trailing;UCEI03_ManagementPlan management[];UCEI03_SizingPlan sizing;UCEI04_ActionStep actions[];UCEI04_RuleFinding findings[];UCEI04_IntrabarPolicy intrabar;string compiler_version;bool manual_baseline;string metadata_json;};
struct UCEI04_PathEvent{int sequence;ENUM_UCEI04_EVENT_TYPE event_type;long event_time_ms;long known_time_ms;bool has_price;double price;double quantity_fraction;string source;string reason;string metadata_json;string event_id;};
struct UCEI04_PathSnapshot{string treatment_id;ENUM_UCEI04_PATH_STATE state;int last_sequence;long last_event_time_ms;long last_known_time_ms;double filled_fraction;double open_fraction;double exited_fraction;bool has_average_entry;double average_entry_price;bool has_active_stop;double active_stop_price;bool has_last_trail;double last_trail_price;string terminal_reason;int transition_count;string snapshot_id;};
struct UCEI04_BarObservation{long open_time_ms;long close_time_ms;double open;double high;double low;double close;long known_time_ms;};
struct UCEI04_MatrixValue{string exact_key;UCEI03_ParameterPacket parameters;string alias;};
struct UCEI04_MatrixAxis{ENUM_UCEI03_ATOM_KIND role;UCEI04_MatrixValue values[];};
struct UCEI04_MatrixSpec{string matrix_id;string version;ENUM_UCEI03_SIDE side;int runtime_mode;ENUM_UCEI04_COMPILER_MODE compiler_mode;UCEI04_MatrixAxis axes[];long max_combinations;long max_compiled;long seed;string definition_id;};
struct UCEI04_MatrixResult{string matrix_definition_id;long generated_count;long compiled_count;long rejected_count;long truncated_count;string deterministic_order_hash;string rejection_summary_json;};
string UCEI04_SelectionMaterial(const UCEI04_AtomSelection &s){return UCEI03_KindName(s.role)+"|"+s.exact_key+"|"+s.parameters.packet_id+"|"+s.alias;}
void UCEI04_SealSelection(UCEI04_AtomSelection &s){s.selection_id="ucesel_"+UCE03_Fnv1a64HexUtf8(UCEI04_SelectionMaterial(s));}
void UCEI04_InitIntrabarPolicy(UCEI04_IntrabarPolicy &p){p.policy_id="intrabar.canonical";p.version="1.0.0";p.ambiguity=UCEI04_WORST_CASE;p.gap=UCEI04_WORST_EXECUTABLE;p.stale_policy=UCEI04_REJECT_STALE;p.max_quote_age_ms=2000;p.latency_ms=0;p.definition_id="uceip_"+UCE03_Fnv1a64HexUtf8(p.policy_id+"|"+p.version+"|"+IntegerToString((long)p.ambiguity)+"|"+IntegerToString((long)p.gap));}
string UCEI04_DraftMaterial(const UCEI04_TreatmentDraft &d){string m=d.draft_name+"|"+UCEI03_SideName(d.side)+"|"+IntegerToString((long)d.runtime_mode)+"|"+IntegerToString((long)d.compiler_mode)+"|"+d.intrabar.definition_id+"|"+(d.pinned?"1":"0");for(int i=0;i<ArraySize(d.selections);i++)m+="|"+UCEI04_SelectionMaterial(d.selections[i]);return m;}
void UCEI04_SealDraft(UCEI04_TreatmentDraft &d){d.draft_id="ucedraft_"+UCE03_Fnv1a64HexUtf8(UCEI04_DraftMaterial(d));}
void UCEI04_SealPathEvent(UCEI04_PathEvent &e){string m=IntegerToString((long)e.sequence)+"|"+UCEI04_EventTypeName(e.event_type)+"|"+IntegerToString(e.event_time_ms)+"|"+IntegerToString(e.known_time_ms)+"|"+DoubleToString(e.price,8)+"|"+DoubleToString(e.quantity_fraction,8)+"|"+e.source+"|"+e.reason;e.event_id="ucepe_"+UCE03_Fnv1a64HexUtf8(m);}
void UCEI04_SealSnapshot(UCEI04_PathSnapshot &s){string m=s.treatment_id+"|"+UCEI04_PathStateName(s.state)+"|"+IntegerToString((long)s.last_sequence)+"|"+DoubleToString(s.filled_fraction,8)+"|"+DoubleToString(s.open_fraction,8)+"|"+DoubleToString(s.exited_fraction,8)+"|"+s.terminal_reason;s.snapshot_id="uceps_"+UCE03_Fnv1a64HexUtf8(m);}
#endif
