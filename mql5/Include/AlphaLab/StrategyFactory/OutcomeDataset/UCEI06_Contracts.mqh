#ifndef ALPHALAB_UCEI06_CONTRACTS_MQH
#define ALPHALAB_UCEI06_CONTRACTS_MQH
#include "UCEI06_Enums.mqh"
struct UCEI06_SourceRef{string source_id;string revision;string content_hash;long available_time_ms;};
struct UCEI06_OpportunityAnchor{string opportunity_id;string context_package_key;string context_occurrence_id;string dependence_cluster_id;string symbol;ENUM_TIMEFRAMES timeframe;int side;long event_time_ms;long decision_time_ms;long known_time_ms;string feature_frame_hash;string anchor_hash;bool eligible;string ineligibility_reason;};
struct UCEI06_PathObservation{int sequence;long event_time_ms;long known_time_ms;double bid;double ask;double available_volume;string source_revision;bool gap;};
struct UCEI06_TreatmentSibling{string treatment_id;string treatment_family_id;int side;int entry_style;double entry_price;bool has_entry_price;double stop_price;double target_price;bool has_target;double trail_distance;bool has_trail;long entry_expiry_ms;long exit_horizon_ms;double volume;double cash_per_price_unit;double estimated_cost_cash;double maximum_loss_cash;string economic_envelope_hash;bool admissible;string rejection_reason;bool manual_baseline;};
struct UCEI06_EconomicScenario{string scenario_id;string version;double commission_cash;double slippage_price;double financing_cash;double gap_reserve_cash;double cost_multiplier;};
struct UCEI06_MaturityEvidence{UCEI06_OUTCOME_STATE state;int censoring;long observation_end_ms;long required_end_ms;bool mature;bool event_observed;string competing_event;string reason;};
struct UCEI06_OutcomeCell{string cell_id;string opportunity_id;string treatment_id;string scenario_key;long horizon_ms;UCEI06_OUTCOME_STATE state;UCEI06_TERMINAL_REASON terminal_reason;UCEI06_MaturityEvidence maturity;long entry_time_ms;long exit_time_ms;double entry_price;double exit_price;double filled_fraction;double gross_pnl_cash;double total_cost_cash;double net_pnl_cash;double net_r;double mfe_r;double mae_r;double max_drawdown_r;long time_to_fill_ms;long time_to_exit_ms;string path_hash;string economic_envelope_hash;bool tail_loss;};
struct UCEI06_LabelTask{string task_id;string version;UCEI06_TASK_KIND task_kind;string metric;long horizon_ms;string scenario_key;double threshold;bool maximize;bool require_resolved;bool allow_right_censored;bool require_all_siblings;double bounded_min_utility;};
struct UCEI06_LabelRecord{string label_id;string opportunity_id;string treatment_id;string task_key;string cell_id;bool mature;bool mask;double scalar_value;int class_value;string category_value;long duration_ms;bool event_observed;string competing_event;int rank;double sample_weight;long known_time_ms;string reason;string evidence_hash;};
struct UCEI06_SplitAssignment{string fold_id;string opportunity_id;string dependence_cluster_id;UCEI06_FOLD_ROLE role;long decision_time_ms;string reason;};
struct UCEI06_LeakageFinding{string code;int severity;bool blocking;string message;string evidence;};
#endif
