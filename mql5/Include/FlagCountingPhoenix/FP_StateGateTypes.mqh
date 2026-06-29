#ifndef __FP_STATE_GATE_TYPES_MQH__
#define __FP_STATE_GATE_TYPES_MQH__
#property strict

#include "FP_Types.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Types
// ----------------------------------------------------------------------------
// The State Gate is a read-only anatomy projection layer above the locked Node,
// Hook/ND, Flag Body, Internal Count, F1/F2/F3 lifecycle, ownership,
// canonicalization, renderer, validation, release, and license logic.
//
// Phase 9 preserves closed-bar tracking, Rally/Hook projection, panel
// section toggles, and State Contract storage, then adds visual/debug contract
// fields for compile and panel-hardening checks. It still does not modify F-counting, Hook/ND,
// node, ownership, canonicalization, renderer, validation, release, or license
// logic.
// ============================================================================

#define FP_STATE_GATE_VERSION "19.220-phase22"
#define FP_STATE_GATE_TF_SLOTS 3
#define FP_STATE_GATE_MAX_RALLY_ROWS 24
#define FP_STATE_GATE_MAX_HOOK_ROWS 48
#define FP_STATE_GATE_MAX_EXTREME_CANDIDATE_ROWS 72
#define FP_STATE_GATE_MAX_MTF_ALIGNMENT_ROWS 12
#define FP_STATE_GATE_MAX_ENTRY_IDEA_ROWS 24
#define FP_STATE_GATE_MAX_ENTRY_DECISION_ROWS 24
#define FP_STATE_GATE_MAX_PAPER_LEDGER_ROWS 24
#define FP_STATE_GATE_MAX_PAPER_LIFECYCLE_ROWS 24
#define FP_STATE_GATE_MAX_PAPER_RESULT_ROWS 24
#define FP_STATE_GATE_MAX_PAPER_PORTFOLIO_ROWS 4
#define FP_STATE_GATE_MAX_PAPER_REGIME_ROWS 24
#define FP_STATE_GATE_MAX_PAPER_FILTER_ROWS 16
#define FP_STATE_GATE_DEFAULT_PREFIX "FP_L19_STATE_GATE_"
#define FP_STATE_GATE_DEFAULT_EXPORT_FOLDER "FlagCountingPhoenix"

#define FP_STATE_GATE_STATUS_DISABLED "STATE_GATE_DISABLED"
#define FP_STATE_GATE_STATUS_TRACKING "TRACKING_CLOSED_BAR"
#define FP_STATE_GATE_STATUS_UNCHANGED "CLOSED_BAR_UNCHANGED"
#define FP_STATE_GATE_STATUS_DIRTY "CLOSED_BAR_CHANGED"
#define FP_STATE_GATE_STATUS_FIRST "FIRST_CLOSED_BAR_SNAPSHOT"
#define FP_STATE_GATE_STATUS_TF_UNUSABLE "TF_UNUSABLE"
#define FP_STATE_GATE_STATUS_TF_UNAVAILABLE "TF_DATA_UNAVAILABLE"

#define FP_STATE_GATE_REASON_PHASE2 "phase2_closed_bar_tracker"
#define FP_STATE_GATE_REASON_PHASE3 "phase3_rally_projection"
#define FP_STATE_GATE_REASON_PHASE4 "phase4_hook_projection"
#define FP_STATE_GATE_REASON_PHASE5 "phase5_panel_polish"
#define FP_STATE_GATE_REASON_PHASE6 "phase6_state_contract_storage"
#define FP_STATE_GATE_REASON_PHASE12 "phase12_extreme_candidate_map"
#define FP_STATE_GATE_REASON_PHASE13 "phase13_mtf_alignment_map"
#define FP_STATE_GATE_REASON_PHASE14 "phase14_entry_geometry_readiness"
#define FP_STATE_GATE_REASON_PHASE15 "phase15_entry_idea_layer"
#define FP_STATE_GATE_REASON_PHASE16 "phase16_entry_decision_dry_run"
#define FP_STATE_GATE_REASON_PHASE17 "phase17_paper_execution_ledger"
#define FP_STATE_GATE_REASON_PHASE18 "phase18_paper_ledger_lifecycle_tracking"
#define FP_STATE_GATE_REASON_PHASE19 "phase19_paper_result_metrics"
#define FP_STATE_GATE_REASON_PHASE20 "phase20_paper_portfolio_aggregate_metrics"
#define FP_STATE_GATE_REASON_PHASE21 "phase21_paper_regime_attribution"
#define FP_STATE_GATE_REASON_PHASE22 "phase22_paper_filter_diagnostics"
#define FP_STATE_GATE_REASON_PHASE11 "phase11_entry_bridge_readiness"
#define FP_STATE_GATE_REASON_PROJECTION_PENDING "projection_pending"

#define FP_STATE_GATE_RALLY_NO_ROWS "NO_CANONICAL_F_ROWS"
#define FP_STATE_GATE_RALLY_ESTABLISHED_NONE "NO_ESTABLISHED_F"
#define FP_STATE_GATE_RALLY_PROBABLE_NONE "NO_PROBABLE_NEXT_F"
#define FP_STATE_GATE_HOOK_NO_ROWS "NO_HOOK_ROWS"
#define FP_STATE_GATE_CONTRACT_READY "STATE_CONTRACT_READY_CONTEXT_ONLY"
#define FP_STATE_GATE_CONTRACT_PARTIAL "STATE_CONTRACT_PARTIAL"
#define FP_STATE_GATE_CONTRACT_NO_DATA "STATE_CONTRACT_NO_DATA"

enum FP_StateGateViewType
{
   FP_STATE_GATE_VIEW_NONE  = 0,
   FP_STATE_GATE_VIEW_RALLY = 1,
   FP_STATE_GATE_VIEW_HOOK  = 2
};

enum FP_StateGateRowStatus
{
   FP_STATE_GATE_ROW_EMPTY       = 0,
   FP_STATE_GATE_ROW_PLACEHOLDER = 1,
   FP_STATE_GATE_ROW_PROJECTED   = 2,
   FP_STATE_GATE_ROW_UNKNOWN     = 3
};

struct FP_StateGateConfig
{
   bool enabled;
   ENUM_TIMEFRAMES tf1;
   ENUM_TIMEFRAMES tf2;
   ENUM_TIMEFRAMES tf3;

   bool panel_enabled;
   bool panel_start_minimized;
   int  panel_corner;
   int  panel_x;
   int  panel_y;
   int  panel_width;
   int  panel_font_size;
   int  panel_rally_preview_rows_per_tf;
   int  panel_hook_preview_rows_per_tf;
   bool panel_force_right_upper;
   bool panel_force_left_upper;
   bool panel_compact_mode;
   bool panel_show_closed_bar;
   bool panel_show_row_counts;
   bool panel_show_contract_key;
   bool panel_show_diagnostics;
   int  max_rally_rows_per_tf;
   int  max_hook_rows_per_tf;
   int  max_extreme_candidates_per_tf;
   bool show_ids;
   bool show_scale_l;
   bool export_csv;
   bool export_overwrite_latest;
   bool export_contract_csv;
   bool export_diagnostics_csv;
   bool export_panel_lines_csv;
   bool export_entry_bridge_csv;
   bool export_extreme_candidates_csv;
   bool export_mtf_alignment_csv;
   bool export_entry_geometry_csv;
   bool export_entry_ideas_csv;
   bool export_entry_decisions_csv;
   bool export_paper_ledger_csv;
   bool export_paper_lifecycle_csv;
   bool export_paper_results_csv;
   bool export_paper_portfolio_csv;
   bool export_paper_regime_csv;
   bool export_paper_filters_csv;
   string export_folder;
   bool print_audit;
   string object_prefix;
};

struct FP_StateGateTimeframeState
{
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime last_closed_bar_time;
   datetime previous_closed_bar_time;
   double last_closed_bar_close;
   bool closed_bar_available;
   bool dirty;
   bool initialized;
   int bars_available;
   int update_count;
   int rally_row_count;
   int hook_row_count;
   int extreme_candidate_row_count;
   int mtf_alignment_row_count;
   int entry_idea_row_count;
   string latest_established_f_summary;
   string probable_next_f_summary;
   string hook_summary;
   string state_key;
   string primary_rally_key;
   string primary_hook_key;
   string anatomy_status;
   string storage_status;
   string entry_bridge_status;
   string entry_bridge_readiness;
   string entry_bridge_key;
   string candidate_extreme_status;
   string candidate_extreme_key;
   string candidate_extreme_source;
   string candidate_direction;
   string candidate_scale_context;
   string x_invalidation_status;
   string x_invalidation_key;
   string x_destination_status;
   string x_destination_key;
   string optionality_status;
   string optionality_key;
   string extreme_map_status;
   string extreme_map_key;
   string primary_extreme_source;
   string primary_extreme_direction;
   string primary_extreme_side;
   string primary_extreme_role;
   string primary_extreme_price_status;
   double primary_extreme_price;
   int primary_extreme_node_id;
   int primary_extreme_scale_L;
   string extreme_map_notes;
   string mtf_alignment_status;
   string mtf_alignment_key;
   string mtf_parent_timeframe;
   string mtf_parent_extreme_key;
   string mtf_parent_direction;
   string mtf_parent_side;
   string mtf_direction_relation;
   string mtf_side_relation;
   string mtf_context_role;
   string mtf_alignment_notes;
   string candidate_entry_price_status;
   double candidate_entry_price;
   string candidate_invalidation_price_status;
   double candidate_invalidation_price;
   string candidate_destination_price_status;
   double candidate_destination_price;
   string risk_distance_status;
   double risk_distance;
   string destination_distance_status;
   double destination_distance;
   string potential_R_status;
   double potential_R;
   string geometry_readiness;
   string geometry_key;
   string geometry_notes;
   string entry_idea_status;
   string entry_idea_readiness;
   string entry_idea_key;
   string primary_entry_idea_family;
   string primary_entry_idea_type;
   string primary_entry_idea_direction;
   string primary_entry_idea_source;
   string primary_entry_idea_role;
   string primary_entry_idea_geometry_status;
   string primary_entry_idea_mtf_context;
   string entry_idea_notes;
   int entry_decision_row_count;
   string entry_decision_status;
   string entry_decision_readiness;
   string entry_decision_key;
   string entry_decision_direction;
   string entry_decision_type;
   string entry_decision_mode;
   bool entry_decision_allowed;
   string entry_decision_price_status;
   double entry_decision_price;
   string entry_decision_invalidation_status;
   double entry_decision_invalidation_price;
   string entry_decision_destination_status;
   double entry_decision_destination_price;
   string entry_decision_risk_status;
   string entry_decision_potential_R_status;
   string entry_decision_block_reason;
   string entry_decision_execution_status;
   string entry_decision_notes;
   int paper_ledger_row_count;
   string paper_ledger_status;
   string paper_ledger_record_status;
   string paper_ledger_key;
   string paper_ledger_event_id;
   string paper_ledger_mode;
   string paper_ledger_direction;
   string paper_ledger_type;
   double paper_ledger_entry_price;
   double paper_ledger_invalidation_price;
   double paper_ledger_destination_price;
   string paper_ledger_lifecycle_status;
   string paper_ledger_execution_status;
   string paper_ledger_source_decision_key;
   string paper_ledger_notes;
   int paper_lifecycle_row_count;
   string paper_lifecycle_status;
   string paper_lifecycle_key;
   string paper_lifecycle_event_id;
   string paper_lifecycle_path_state;
   string paper_entry_touch_status;
   string paper_invalidation_touch_status;
   string paper_destination_touch_status;
   string paper_lifecycle_outcome;
   string paper_lifecycle_execution_status;
   string paper_lifecycle_notes;
   int paper_result_row_count;
   string paper_result_status;
   string paper_result_key;
   string paper_result_outcome;
   string paper_result_direction;
   string paper_result_type;
   double paper_result_entry_price;
   double paper_result_exit_anchor_price;
   double paper_result_price_delta;
   double paper_result_abs_distance;
   string paper_result_r_status;
   double paper_result_r_multiple;
   string paper_result_bucket;
   string paper_result_execution_status;
   string paper_result_notes;
   int paper_regime_row_count;
   int paper_filter_row_count;
   string paper_regime_status;
   string paper_regime_key;
   string paper_regime_context_family;
   string paper_regime_source_context;
   string paper_regime_mtf_context;
   string paper_regime_geometry_context;
   string paper_regime_outcome;
   string paper_regime_result_bucket;
   string paper_regime_execution_status;
   string paper_regime_notes;
   string contract_status;
   string tracker_status;
   string status;
   string reason;
};

struct FP_StateGateRallyRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   int source_event_id;
   int sequence_id;
   int parent_event_id;
   int scale_L;
   int direction;
   int f_level;
   string latest_established_f;
   string probable_next_f;
   string body_state;
   string flag_stage;
   string post_flag_stage;
   string source_id;
   string label;
};

struct FP_StateGateHookRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   int source_hook_id;
   int sequence_id;
   int scale_L;
   int direction;
   string polarity;
   int current_node_number;
   int latest_high_node_id;
   double latest_high_node_price;
   int latest_low_node_id;
   double latest_low_node_price;
   string position_label;
   string source_id;
   string label;
};


struct FP_StateGateExtremeCandidateRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   string source_kind;
   string source_id;
   int source_row_index;
   int direction;
   string direction_label;
   string side;
   string role;
   int scale_L;
   int node_id;
   double price;
   string price_status;
   int rank;
   string source_key;
   string readiness;
   string label;
};


struct FP_StateGateMtfAlignmentRow
{
   int child_slot;
   int parent_slot;
   string child_timeframe_label;
   string parent_timeframe_label;
   datetime child_closed_bar_time;
   datetime parent_closed_bar_time;
   int status;
   string readiness;
   string child_extreme_key;
   string parent_extreme_key;
   string child_source;
   string parent_source;
   string child_direction;
   string parent_direction;
   string child_side;
   string parent_side;
   string direction_relation;
   string side_relation;
   string context_role;
   int child_node_id;
   int parent_node_id;
   double child_price;
   double parent_price;
   string child_price_status;
   string parent_price_status;
   string alignment_key;
   string label;
};


struct FP_StateGateEntryIdeaRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   string readiness;
   string idea_family;
   string idea_type;
   string idea_direction;
   string idea_source;
   string idea_role;
   string geometry_status;
   string mtf_context_role;
   string extreme_side;
   double entry_price;
   double invalidation_anchor_price;
   double destination_anchor_price;
   double destination_distance;
   string risk_status;
   string potential_R_status;
   double potential_R;
   string idea_key;
   string label;
};


struct FP_StateGateEntryDecisionRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   string readiness;
   string decision_status;
   string decision_direction;
   string decision_type;
   string decision_mode;
   bool decision_allowed;
   string decision_price_status;
   double decision_price;
   string invalidation_status;
   double invalidation_price;
   string destination_status;
   double destination_price;
   string risk_status;
   string potential_R_status;
   string source_idea_key;
   string source_geometry_key;
   string source_mtf_key;
   string block_reason;
   string execution_status;
   string decision_key;
   string label;
};


struct FP_StateGatePaperLedgerRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime recorded_at;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   string record_status;
   string ledger_mode;
   string lifecycle_status;
   string decision_status;
   string decision_readiness;
   string decision_direction;
   string decision_type;
   bool decision_allowed;
   double entry_price;
   double invalidation_price;
   double destination_price;
   string risk_status;
   string potential_R_status;
   string source_decision_key;
   string source_idea_key;
   string source_geometry_key;
   string source_mtf_key;
   string execution_status;
   string block_reason;
   string ledger_key;
   string event_id;
   string label;
};


struct FP_StateGatePaperLifecycleRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime evaluated_at;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   string lifecycle_status;
   string path_state;
   string entry_touch_status;
   string invalidation_touch_status;
   string destination_touch_status;
   string outcome;
   string direction;
   string decision_type;
   double entry_price;
   double invalidation_price;
   double destination_price;
   bool entry_touched;
   bool invalidation_touched;
   bool destination_touched;
   string source_ledger_key;
   string source_decision_key;
   string event_id;
   string lifecycle_key;
   string execution_status;
   string label;
};


struct FP_StateGatePaperResultRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime summarized_at;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   string result_status;
   string outcome;
   string result_bucket;
   string direction;
   string decision_type;
   double entry_price;
   double exit_anchor_price;
   double destination_price;
   double invalidation_price;
   double price_delta;
   double abs_distance;
   string r_status;
   double r_multiple;
   string source_lifecycle_key;
   string source_ledger_key;
   string source_decision_key;
   string event_id;
   string result_key;
   string execution_status;
   string label;
};


struct FP_StateGatePaperPortfolioRow
{
   int row_index;
   datetime summarized_at;
   int status;
   string portfolio_status;
   string portfolio_key;
   int total_result_rows;
   int win_like_rows;
   int loss_like_rows;
   int open_rows;
   int waiting_rows;
   int ambiguous_rows;
   int unknown_rows;
   int r_ready_rows;
   int r_pending_rows;
   double net_delta;
   double avg_delta;
   double avg_R;
   double best_R;
   double worst_R;
   string result_distribution;
   string execution_status;
   string label;
};


struct FP_StateGatePaperRegimeRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime attributed_at;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   string attribution_status;
   string context_family;
   string source_context;
   string mtf_context;
   string mtf_direction_relation;
   string mtf_side_relation;
   string geometry_context;
   string idea_family;
   string idea_type;
   string decision_type;
   string extreme_source;
   string extreme_side;
   string hook_context;
   string rally_context;
   string lifecycle_path_state;
   string outcome;
   string result_bucket;
   double price_delta;
   string r_status;
   double r_multiple;
   string source_result_key;
   string source_lifecycle_key;
   string source_portfolio_key;
   string attribution_key;
   string execution_status;
   string label;
};


struct FP_StateGatePaperFilterRow
{
   int filter_index;
   string filter_name;
   string filter_family;
   string filter_status;
   string filter_rule;
   int rows_before;
   int rows_after;
   int win_like_rows;
   int loss_like_rows;
   int open_rows;
   int waiting_rows;
   int ambiguous_rows;
   int unknown_rows;
   int r_ready_rows;
   int r_pending_rows;
   double net_delta;
   double avg_delta;
   double avg_R;
   double pass_rate;
   string strongest_context;
   string diagnostic_key;
   string execution_status;
   string label;
};

struct FP_StateGateSnapshot
{
   bool initialized;
   string symbol;
   ENUM_TIMEFRAMES chart_timeframe;
   datetime generated_at;
   int timeframe_count;
   int dirty_timeframes;
   int available_timeframes;
   int unchanged_timeframes;
   int unavailable_timeframes;
   int update_serial;
   bool any_dirty;
   FP_StateGateTimeframeState tf_states[FP_STATE_GATE_TF_SLOTS];
   FP_StateGateRallyRow rally_rows[FP_STATE_GATE_MAX_RALLY_ROWS];
   FP_StateGateHookRow hook_rows[FP_STATE_GATE_MAX_HOOK_ROWS];
   FP_StateGateExtremeCandidateRow extreme_candidate_rows[FP_STATE_GATE_MAX_EXTREME_CANDIDATE_ROWS];
   FP_StateGateMtfAlignmentRow mtf_alignment_rows[FP_STATE_GATE_MAX_MTF_ALIGNMENT_ROWS];
   FP_StateGateEntryIdeaRow entry_idea_rows[FP_STATE_GATE_MAX_ENTRY_IDEA_ROWS];
   FP_StateGateEntryDecisionRow entry_decision_rows[FP_STATE_GATE_MAX_ENTRY_DECISION_ROWS];
   FP_StateGatePaperLedgerRow paper_ledger_rows[FP_STATE_GATE_MAX_PAPER_LEDGER_ROWS];
   FP_StateGatePaperLifecycleRow paper_lifecycle_rows[FP_STATE_GATE_MAX_PAPER_LIFECYCLE_ROWS];
   FP_StateGatePaperResultRow paper_result_rows[FP_STATE_GATE_MAX_PAPER_RESULT_ROWS];
   FP_StateGatePaperPortfolioRow paper_portfolio_rows[FP_STATE_GATE_MAX_PAPER_PORTFOLIO_ROWS];
   FP_StateGatePaperRegimeRow paper_regime_rows[FP_STATE_GATE_MAX_PAPER_REGIME_ROWS];
   FP_StateGatePaperFilterRow paper_filter_rows[FP_STATE_GATE_MAX_PAPER_FILTER_ROWS];
   int rally_row_count;
   int hook_row_count;
   int extreme_candidate_row_count;
   int mtf_alignment_row_count;
   int entry_idea_row_count;
   int entry_decision_row_count;
   int paper_ledger_row_count;
   int paper_lifecycle_row_count;
   int paper_result_row_count;
   int paper_portfolio_row_count;
   int paper_regime_row_count;
   int paper_filter_row_count;
   string paper_portfolio_status;
   string paper_portfolio_key;
   int paper_portfolio_total_results;
   int paper_portfolio_win_like_rows;
   int paper_portfolio_loss_like_rows;
   int paper_portfolio_open_rows;
   int paper_portfolio_waiting_rows;
   int paper_portfolio_ambiguous_rows;
   int paper_portfolio_unknown_rows;
   int paper_portfolio_r_ready_rows;
   int paper_portfolio_r_pending_rows;
   double paper_portfolio_net_delta;
   double paper_portfolio_avg_delta;
   double paper_portfolio_avg_R;
   double paper_portfolio_best_R;
   double paper_portfolio_worst_R;
   string paper_portfolio_distribution;
   string paper_portfolio_execution_status;
   string paper_portfolio_notes;
   string paper_filter_status;
   string paper_filter_key;
   int paper_filter_total_filters;
   int paper_filter_active_filters;
   string paper_filter_best_filter;
   string paper_filter_best_distribution;
   double paper_filter_best_avg_delta;
   double paper_filter_best_avg_R;
   string paper_filter_execution_status;
   string paper_filter_notes;
   string status;
   string reason;
};

struct FP_StateGateRuntime
{
   bool initialized;
   bool minimized;
   bool panel_has_drawn;
   bool export_has_written;
   bool last_run_had_dirty;
   datetime last_processed_closed_bar_time[FP_STATE_GATE_TF_SLOTS];
   datetime previous_closed_bar_time[FP_STATE_GATE_TF_SLOTS];
   bool slot_initialized[FP_STATE_GATE_TF_SLOTS];
   int slot_update_count[FP_STATE_GATE_TF_SLOTS];
   int update_serial;
   datetime last_engine_run_time;
   FP_StateGateSnapshot snapshot;
};

struct FP_StateGateReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   string version;
   string symbol;
   int timeframe_count;
   int slots_checked;
   int available_timeframes;
   int dirty_timeframes;
   int unchanged_timeframes;
   int unavailable_timeframes;
   int rally_rows;
   int hook_rows;
   int contract_rows;
   int extreme_candidate_rows;
   int mtf_alignment_rows;
   int geometry_rows;
   int entry_idea_rows;
   int entry_decision_rows;
   int paper_ledger_rows;
   int paper_lifecycle_rows;
   int paper_result_rows;
   int paper_portfolio_rows;
   int paper_regime_rows;
   int paper_filter_rows;
   int objects_requested;
   int objects_created;
   int object_errors;
   int objects_deleted;
   int files_written;
   int file_errors;
   bool panel_redrawn;
   bool export_attempted;
   bool skipped_no_dirty;
};

void FP_ResetStateGateTimeframeState(FP_StateGateTimeframeState &s)
{
   s.timeframe = PERIOD_CURRENT;
   s.timeframe_label = "TF?";
   s.last_closed_bar_time = 0;
   s.previous_closed_bar_time = 0;
   s.last_closed_bar_close = 0.0;
   s.closed_bar_available = false;
   s.dirty = false;
   s.initialized = false;
   s.bars_available = 0;
   s.update_count = 0;
   s.rally_row_count = 0;
   s.hook_row_count = 0;
   s.extreme_candidate_row_count = 0;
   s.mtf_alignment_row_count = 0;
   s.latest_established_f_summary = "RALLY_VIEW_PENDING";
   s.probable_next_f_summary = "RALLY_VIEW_PENDING";
   s.hook_summary = "HOOK_VIEW_PENDING";
   s.state_key = "STATE_KEY_PENDING";
   s.primary_rally_key = "RALLY_KEY_PENDING";
   s.primary_hook_key = "HOOK_KEY_PENDING";
   s.anatomy_status = "ANATOMY_PENDING";
   s.storage_status = "STORAGE_PENDING";
   s.entry_bridge_status = "ENTRY_BRIDGE_CONTEXT_PENDING";
   s.entry_bridge_readiness = "ENTRY_READINESS_PENDING";
   s.entry_bridge_key = "ENTRY_BRIDGE_KEY_PENDING";
   s.candidate_extreme_status = "CANDIDATE_EXTREME_PENDING";
   s.candidate_extreme_key = "CANDIDATE_EXTREME_KEY_PENDING";
   s.candidate_extreme_source = "CANDIDATE_SOURCE_PENDING";
   s.candidate_direction = "DIRECTION_PENDING";
   s.candidate_scale_context = "SCALE_CONTEXT_PENDING";
   s.x_invalidation_status = "X_INVALIDATION_PENDING";
   s.x_invalidation_key = "X_INVALIDATION_KEY_PENDING";
   s.x_destination_status = "X_DESTINATION_PENDING";
   s.x_destination_key = "X_DESTINATION_KEY_PENDING";
   s.optionality_status = "OPTIONALITY_PENDING";
   s.optionality_key = "OPTIONALITY_KEY_PENDING";
   s.extreme_map_status = "EXTREME_MAP_PENDING";
   s.extreme_map_key = "EXTREME_MAP_KEY_PENDING";
   s.primary_extreme_source = "PRIMARY_EXTREME_PENDING";
   s.primary_extreme_direction = "NO_DIRECTION";
   s.primary_extreme_side = "NO_SIDE";
   s.primary_extreme_role = "NO_ROLE";
   s.primary_extreme_price_status = "NO_PRICE";
   s.primary_extreme_price = 0.0;
   s.primary_extreme_node_id = -1;
   s.primary_extreme_scale_L = 0;
   s.extreme_map_notes = "EXTREME_MAP_PENDING";
   s.mtf_alignment_row_count = 0;
   s.mtf_alignment_status = "MTF_ALIGNMENT_PENDING";
   s.mtf_alignment_key = "MTF_ALIGNMENT_KEY_PENDING";
   s.mtf_parent_timeframe = "NO_PARENT_TF";
   s.mtf_parent_extreme_key = "NO_PARENT_EXTREME";
   s.mtf_parent_direction = "NO_PARENT_DIRECTION";
   s.mtf_parent_side = "NO_PARENT_SIDE";
   s.mtf_direction_relation = "NO_MTF_DIRECTION_RELATION";
   s.mtf_side_relation = "NO_MTF_SIDE_RELATION";
   s.mtf_context_role = "NO_MTF_CONTEXT";
   s.mtf_alignment_notes = "MTF_ALIGNMENT_PENDING";
   s.candidate_entry_price_status = "ENTRY_PRICE_PENDING";
   s.candidate_entry_price = 0.0;
   s.candidate_invalidation_price_status = "INVALIDATION_PRICE_PENDING";
   s.candidate_invalidation_price = 0.0;
   s.candidate_destination_price_status = "DESTINATION_PRICE_PENDING";
   s.candidate_destination_price = 0.0;
   s.risk_distance_status = "RISK_DISTANCE_PENDING";
   s.risk_distance = 0.0;
   s.destination_distance_status = "DESTINATION_DISTANCE_PENDING";
   s.destination_distance = 0.0;
   s.potential_R_status = "POTENTIAL_R_PENDING";
   s.potential_R = 0.0;
   s.geometry_readiness = "ENTRY_GEOMETRY_PENDING_NO_SIGNAL";
   s.geometry_key = "ENTRY_GEOMETRY_KEY_PENDING";
   s.geometry_notes = "ENTRY_GEOMETRY_PENDING";
   s.entry_idea_row_count = 0;
   s.entry_idea_status = "ENTRY_IDEA_PENDING";
   s.entry_idea_readiness = "ENTRY_IDEA_PENDING_NO_SIGNAL";
   s.entry_idea_key = "ENTRY_IDEA_KEY_PENDING";
   s.primary_entry_idea_family = "NO_ENTRY_IDEA_FAMILY";
   s.primary_entry_idea_type = "NO_ENTRY_IDEA_TYPE";
   s.primary_entry_idea_direction = "NO_ENTRY_IDEA_DIRECTION";
   s.primary_entry_idea_source = "NO_ENTRY_IDEA_SOURCE";
   s.primary_entry_idea_role = "NO_ENTRY_IDEA_ROLE";
   s.primary_entry_idea_geometry_status = "NO_ENTRY_IDEA_GEOMETRY";
   s.primary_entry_idea_mtf_context = "NO_ENTRY_IDEA_MTF_CONTEXT";
   s.entry_idea_notes = "ENTRY_IDEA_PENDING";
   s.entry_decision_row_count = 0;
   s.entry_decision_status = "ENTRY_DECISION_PENDING_DRY_RUN";
   s.entry_decision_readiness = "ENTRY_DECISION_PENDING_NO_SIGNAL";
   s.entry_decision_key = "ENTRY_DECISION_KEY_PENDING";
   s.entry_decision_direction = "NO_ENTRY_DECISION_DIRECTION";
   s.entry_decision_type = "NO_ENTRY_DECISION_TYPE";
   s.entry_decision_mode = "DRY_RUN_ONLY";
   s.entry_decision_allowed = false;
   s.entry_decision_price_status = "NO_ENTRY_DECISION_PRICE";
   s.entry_decision_price = 0.0;
   s.entry_decision_invalidation_status = "NO_ENTRY_DECISION_INVALIDATION";
   s.entry_decision_invalidation_price = 0.0;
   s.entry_decision_destination_status = "NO_ENTRY_DECISION_DESTINATION";
   s.entry_decision_destination_price = 0.0;
   s.entry_decision_risk_status = "NO_ENTRY_DECISION_RISK";
   s.entry_decision_potential_R_status = "NO_ENTRY_DECISION_POTENTIAL_R";
   s.entry_decision_block_reason = "ENTRY_DECISION_PENDING";
   s.entry_decision_execution_status = "EXECUTION_DISABLED_DRY_RUN_ONLY";
   s.entry_decision_notes = "ENTRY_DECISION_PENDING";
   s.paper_ledger_row_count = 0;
   s.paper_ledger_status = "PAPER_LEDGER_PENDING";
   s.paper_ledger_record_status = "PAPER_LEDGER_RECORD_PENDING";
   s.paper_ledger_key = "PAPER_LEDGER_KEY_PENDING";
   s.paper_ledger_event_id = "PAPER_EVENT_PENDING";
   s.paper_ledger_mode = "PAPER_DRY_RUN_ONLY";
   s.paper_ledger_direction = "NO_PAPER_DIRECTION";
   s.paper_ledger_type = "NO_PAPER_TYPE";
   s.paper_ledger_entry_price = 0.0;
   s.paper_ledger_invalidation_price = 0.0;
   s.paper_ledger_destination_price = 0.0;
   s.paper_ledger_lifecycle_status = "PAPER_LEDGER_LIFECYCLE_PENDING";
   s.paper_ledger_execution_status = "REAL_EXECUTION_DISABLED_PHASE17_PAPER_ONLY";
   s.paper_ledger_source_decision_key = "NO_SOURCE_DECISION_KEY";
   s.paper_ledger_notes = "PAPER_LEDGER_PENDING";
   s.paper_lifecycle_row_count = 0;
   s.paper_lifecycle_status = "PAPER_LIFECYCLE_PENDING";
   s.paper_lifecycle_key = "PAPER_LIFECYCLE_KEY_PENDING";
   s.paper_lifecycle_event_id = "PAPER_LIFECYCLE_EVENT_PENDING";
   s.paper_lifecycle_path_state = "PAPER_PATH_PENDING";
   s.paper_entry_touch_status = "PAPER_ENTRY_TOUCH_PENDING";
   s.paper_invalidation_touch_status = "PAPER_INVALIDATION_TOUCH_PENDING";
   s.paper_destination_touch_status = "PAPER_DESTINATION_TOUCH_PENDING";
   s.paper_lifecycle_outcome = "PAPER_OUTCOME_PENDING";
   s.paper_lifecycle_execution_status = "REAL_EXECUTION_DISABLED_PHASE18_LIFECYCLE_ONLY";
   s.paper_lifecycle_notes = "PAPER_LIFECYCLE_PENDING";
   s.paper_result_row_count = 0;
   s.paper_result_status = "PAPER_RESULT_PENDING";
   s.paper_result_key = "PAPER_RESULT_KEY_PENDING";
   s.paper_result_outcome = "PAPER_RESULT_OUTCOME_PENDING";
   s.paper_result_direction = "NO_PAPER_RESULT_DIRECTION";
   s.paper_result_type = "NO_PAPER_RESULT_TYPE";
   s.paper_result_entry_price = 0.0;
   s.paper_result_exit_anchor_price = 0.0;
   s.paper_result_price_delta = 0.0;
   s.paper_result_abs_distance = 0.0;
   s.paper_result_r_status = "PAPER_R_PENDING";
   s.paper_result_r_multiple = 0.0;
   s.paper_result_bucket = "PAPER_RESULT_BUCKET_PENDING";
   s.paper_result_execution_status = "REAL_EXECUTION_DISABLED_PHASE19_RESULT_ONLY";
   s.paper_result_notes = "PAPER_RESULT_PENDING";
   s.paper_regime_row_count = 0;
   s.paper_filter_row_count = 0;
   s.paper_regime_status = "PAPER_REGIME_PENDING";
   s.paper_regime_key = "PAPER_REGIME_KEY_PENDING";
   s.paper_regime_context_family = "PAPER_REGIME_CONTEXT_PENDING";
   s.paper_regime_source_context = "PAPER_REGIME_SOURCE_PENDING";
   s.paper_regime_mtf_context = "PAPER_REGIME_MTF_PENDING";
   s.paper_regime_geometry_context = "PAPER_REGIME_GEOMETRY_PENDING";
   s.paper_regime_outcome = "PAPER_REGIME_OUTCOME_PENDING";
   s.paper_regime_result_bucket = "PAPER_REGIME_BUCKET_PENDING";
   s.paper_regime_execution_status = "REAL_EXECUTION_DISABLED_PHASE21_ATTRIBUTION_ONLY";
   s.paper_regime_notes = "PAPER_REGIME_PENDING";
   s.contract_status = "CONTRACT_PENDING";
   s.tracker_status = "reset";
   s.status = "empty";
   s.reason = "reset";
}

void FP_ResetStateGateRallyRow(FP_StateGateRallyRow &r)
{
   r.slot_index = -1;
   r.timeframe = PERIOD_CURRENT;
   r.timeframe_label = "TF?";
   r.last_closed_bar_time = 0;
   r.last_closed_bar_close = 0.0;
   r.status = FP_STATE_GATE_ROW_EMPTY;
   r.source_event_id = -1;
   r.sequence_id = -1;
   r.parent_event_id = -1;
   r.scale_L = 0;
   r.direction = FP_DIR_NONE;
   r.f_level = FP_LEVEL_NONE;
   r.latest_established_f = "F?_PENDING";
   r.probable_next_f = "F?_PENDING";
   r.body_state = "PHASE2_PLACEHOLDER";
   r.flag_stage = "PHASE2_PLACEHOLDER";
   r.post_flag_stage = "PHASE2_PLACEHOLDER";
   r.source_id = "";
   r.label = "Rally View not projected yet";
}

void FP_ResetStateGateHookRow(FP_StateGateHookRow &r)
{
   r.slot_index = -1;
   r.timeframe = PERIOD_CURRENT;
   r.timeframe_label = "TF?";
   r.last_closed_bar_time = 0;
   r.last_closed_bar_close = 0.0;
   r.status = FP_STATE_GATE_ROW_EMPTY;
   r.source_hook_id = -1;
   r.sequence_id = -1;
   r.scale_L = 0;
   r.direction = FP_DIR_NONE;
   r.polarity = "HOOK?_PENDING";
   r.current_node_number = -1;
   r.latest_high_node_id = -1;
   r.latest_high_node_price = 0.0;
   r.latest_low_node_id = -1;
   r.latest_low_node_price = 0.0;
   r.position_label = "PHASE2_PLACEHOLDER";
   r.source_id = "";
   r.label = "Hook View placeholder: projection starts in Level 19 Phase 4";
}


void FP_ResetStateGateExtremeCandidateRow(FP_StateGateExtremeCandidateRow &x)
{
   x.slot_index = -1;
   x.timeframe = PERIOD_CURRENT;
   x.timeframe_label = "TF?";
   x.last_closed_bar_time = 0;
   x.last_closed_bar_close = 0.0;
   x.status = FP_STATE_GATE_ROW_EMPTY;
   x.source_kind = "NO_SOURCE";
   x.source_id = "";
   x.source_row_index = -1;
   x.direction = FP_DIR_NONE;
   x.direction_label = "NO_DIRECTION";
   x.side = "NO_SIDE";
   x.role = "NO_ROLE";
   x.scale_L = 0;
   x.node_id = -1;
   x.price = 0.0;
   x.price_status = "NO_PRICE";
   x.rank = -1;
   x.source_key = "";
   x.readiness = "EXTREME_CANDIDATE_PENDING";
   x.label = "Extreme candidate map pending";
}


void FP_ResetStateGateMtfAlignmentRow(FP_StateGateMtfAlignmentRow &m)
{
   m.child_slot = -1;
   m.parent_slot = -1;
   m.child_timeframe_label = "CHILD?";
   m.parent_timeframe_label = "PARENT?";
   m.child_closed_bar_time = 0;
   m.parent_closed_bar_time = 0;
   m.status = FP_STATE_GATE_ROW_EMPTY;
   m.readiness = "MTF_ALIGNMENT_PENDING";
   m.child_extreme_key = "NO_CHILD_EXTREME";
   m.parent_extreme_key = "NO_PARENT_EXTREME";
   m.child_source = "NO_CHILD_SOURCE";
   m.parent_source = "NO_PARENT_SOURCE";
   m.child_direction = "NO_CHILD_DIRECTION";
   m.parent_direction = "NO_PARENT_DIRECTION";
   m.child_side = "NO_CHILD_SIDE";
   m.parent_side = "NO_PARENT_SIDE";
   m.direction_relation = "NO_DIRECTION_RELATION";
   m.side_relation = "NO_SIDE_RELATION";
   m.context_role = "NO_CONTEXT_ROLE";
   m.child_node_id = -1;
   m.parent_node_id = -1;
   m.child_price = 0.0;
   m.parent_price = 0.0;
   m.child_price_status = "NO_CHILD_PRICE";
   m.parent_price_status = "NO_PARENT_PRICE";
   m.alignment_key = "NO_ALIGNMENT_KEY";
   m.label = "MTF alignment pending";
}


void FP_ResetStateGateEntryIdeaRow(FP_StateGateEntryIdeaRow &e)
{
   e.slot_index = -1;
   e.timeframe = PERIOD_CURRENT;
   e.timeframe_label = "TF?";
   e.last_closed_bar_time = 0;
   e.last_closed_bar_close = 0.0;
   e.status = FP_STATE_GATE_ROW_EMPTY;
   e.readiness = "ENTRY_IDEA_PENDING_NO_SIGNAL";
   e.idea_family = "NO_ENTRY_IDEA_FAMILY";
   e.idea_type = "NO_ENTRY_IDEA_TYPE";
   e.idea_direction = "NO_ENTRY_IDEA_DIRECTION";
   e.idea_source = "NO_ENTRY_IDEA_SOURCE";
   e.idea_role = "NO_ENTRY_IDEA_ROLE";
   e.geometry_status = "NO_ENTRY_GEOMETRY";
   e.mtf_context_role = "NO_MTF_CONTEXT";
   e.extreme_side = "NO_EXTREME_SIDE";
   e.entry_price = 0.0;
   e.invalidation_anchor_price = 0.0;
   e.destination_anchor_price = 0.0;
   e.destination_distance = 0.0;
   e.risk_status = "NO_RISK_MODEL";
   e.potential_R_status = "NO_POTENTIAL_R";
   e.potential_R = 0.0;
   e.idea_key = "NO_ENTRY_IDEA_KEY";
   e.label = "Entry idea pending";
}


void FP_ResetStateGateEntryDecisionRow(FP_StateGateEntryDecisionRow &d)
{
   d.slot_index = -1;
   d.timeframe = PERIOD_CURRENT;
   d.timeframe_label = "TF?";
   d.last_closed_bar_time = 0;
   d.last_closed_bar_close = 0.0;
   d.status = FP_STATE_GATE_ROW_EMPTY;
   d.readiness = "ENTRY_DECISION_PENDING_NO_SIGNAL";
   d.decision_status = "ENTRY_DECISION_PENDING_DRY_RUN";
   d.decision_direction = "NO_ENTRY_DECISION_DIRECTION";
   d.decision_type = "NO_ENTRY_DECISION_TYPE";
   d.decision_mode = "DRY_RUN_ONLY";
   d.decision_allowed = false;
   d.decision_price_status = "NO_ENTRY_DECISION_PRICE";
   d.decision_price = 0.0;
   d.invalidation_status = "NO_INVALIDATION_ANCHOR";
   d.invalidation_price = 0.0;
   d.destination_status = "NO_DESTINATION_ANCHOR";
   d.destination_price = 0.0;
   d.risk_status = "NO_RISK_MODEL";
   d.potential_R_status = "NO_POTENTIAL_R";
   d.source_idea_key = "NO_ENTRY_IDEA_KEY";
   d.source_geometry_key = "NO_GEOMETRY_KEY";
   d.source_mtf_key = "NO_MTF_KEY";
   d.block_reason = "ENTRY_DECISION_PENDING";
   d.execution_status = "EXECUTION_DISABLED_DRY_RUN_ONLY";
   d.decision_key = "NO_ENTRY_DECISION_KEY";
   d.label = "Entry decision pending dry-run only";
}


void FP_ResetStateGatePaperLedgerRow(FP_StateGatePaperLedgerRow &p)
{
   p.slot_index = -1;
   p.timeframe = PERIOD_CURRENT;
   p.timeframe_label = "TF?";
   p.recorded_at = 0;
   p.last_closed_bar_time = 0;
   p.last_closed_bar_close = 0.0;
   p.status = FP_STATE_GATE_ROW_EMPTY;
   p.record_status = "PAPER_LEDGER_RECORD_PENDING";
   p.ledger_mode = "PAPER_DRY_RUN_ONLY";
   p.lifecycle_status = "PAPER_LEDGER_PENDING";
   p.decision_status = "NO_DECISION_STATUS";
   p.decision_readiness = "NO_DECISION_READINESS";
   p.decision_direction = "NO_DECISION_DIRECTION";
   p.decision_type = "NO_DECISION_TYPE";
   p.decision_allowed = false;
   p.entry_price = 0.0;
   p.invalidation_price = 0.0;
   p.destination_price = 0.0;
   p.risk_status = "NO_RISK_MODEL";
   p.potential_R_status = "NO_POTENTIAL_R";
   p.source_decision_key = "NO_SOURCE_DECISION_KEY";
   p.source_idea_key = "NO_SOURCE_IDEA_KEY";
   p.source_geometry_key = "NO_SOURCE_GEOMETRY_KEY";
   p.source_mtf_key = "NO_SOURCE_MTF_KEY";
   p.execution_status = "REAL_EXECUTION_DISABLED_PHASE17_PAPER_ONLY";
   p.block_reason = "PAPER_LEDGER_PENDING";
   p.ledger_key = "NO_PAPER_LEDGER_KEY";
   p.event_id = "NO_PAPER_EVENT_ID";
   p.label = "Paper ledger pending";
}


void FP_ResetStateGatePaperLifecycleRow(FP_StateGatePaperLifecycleRow &p)
{
   p.slot_index = -1;
   p.timeframe = PERIOD_CURRENT;
   p.timeframe_label = "TF?";
   p.evaluated_at = 0;
   p.last_closed_bar_time = 0;
   p.last_closed_bar_close = 0.0;
   p.status = FP_STATE_GATE_ROW_EMPTY;
   p.lifecycle_status = "PAPER_LIFECYCLE_PENDING";
   p.path_state = "PAPER_PATH_PENDING";
   p.entry_touch_status = "PAPER_ENTRY_TOUCH_PENDING";
   p.invalidation_touch_status = "PAPER_INVALIDATION_TOUCH_PENDING";
   p.destination_touch_status = "PAPER_DESTINATION_TOUCH_PENDING";
   p.outcome = "PAPER_OUTCOME_PENDING";
   p.direction = "NO_PAPER_DIRECTION";
   p.decision_type = "NO_PAPER_DECISION_TYPE";
   p.entry_price = 0.0;
   p.invalidation_price = 0.0;
   p.destination_price = 0.0;
   p.entry_touched = false;
   p.invalidation_touched = false;
   p.destination_touched = false;
   p.source_ledger_key = "NO_SOURCE_LEDGER_KEY";
   p.source_decision_key = "NO_SOURCE_DECISION_KEY";
   p.event_id = "NO_PAPER_EVENT_ID";
   p.lifecycle_key = "NO_PAPER_LIFECYCLE_KEY";
   p.execution_status = "REAL_EXECUTION_DISABLED_PHASE18_LIFECYCLE_ONLY";
   p.label = "Paper lifecycle pending";
}


void FP_ResetStateGatePaperResultRow(FP_StateGatePaperResultRow &r)
{
   r.slot_index = -1;
   r.timeframe = PERIOD_CURRENT;
   r.timeframe_label = "TF?";
   r.summarized_at = 0;
   r.last_closed_bar_time = 0;
   r.last_closed_bar_close = 0.0;
   r.status = FP_STATE_GATE_ROW_EMPTY;
   r.result_status = "PAPER_RESULT_PENDING";
   r.outcome = "PAPER_OUTCOME_PENDING";
   r.result_bucket = "PAPER_RESULT_BUCKET_PENDING";
   r.direction = "NO_PAPER_DIRECTION";
   r.decision_type = "NO_PAPER_DECISION_TYPE";
   r.entry_price = 0.0;
   r.exit_anchor_price = 0.0;
   r.destination_price = 0.0;
   r.invalidation_price = 0.0;
   r.price_delta = 0.0;
   r.abs_distance = 0.0;
   r.r_status = "PAPER_R_PENDING";
   r.r_multiple = 0.0;
   r.source_lifecycle_key = "NO_SOURCE_LIFECYCLE_KEY";
   r.source_ledger_key = "NO_SOURCE_LEDGER_KEY";
   r.source_decision_key = "NO_SOURCE_DECISION_KEY";
   r.event_id = "NO_PAPER_EVENT_ID";
   r.result_key = "NO_PAPER_RESULT_KEY";
   r.execution_status = "REAL_EXECUTION_DISABLED_PHASE19_RESULT_ONLY";
   r.label = "Paper result pending";
}


void FP_ResetStateGatePaperPortfolioRow(FP_StateGatePaperPortfolioRow &p)
{
   p.row_index = -1;
   p.summarized_at = 0;
   p.status = FP_STATE_GATE_ROW_EMPTY;
   p.portfolio_status = "PAPER_PORTFOLIO_PENDING";
   p.portfolio_key = "NO_PAPER_PORTFOLIO_KEY";
   p.total_result_rows = 0;
   p.win_like_rows = 0;
   p.loss_like_rows = 0;
   p.open_rows = 0;
   p.waiting_rows = 0;
   p.ambiguous_rows = 0;
   p.unknown_rows = 0;
   p.r_ready_rows = 0;
   p.r_pending_rows = 0;
   p.net_delta = 0.0;
   p.avg_delta = 0.0;
   p.avg_R = 0.0;
   p.best_R = 0.0;
   p.worst_R = 0.0;
   p.result_distribution = "PAPER_DISTRIBUTION_PENDING";
   p.execution_status = "REAL_EXECUTION_DISABLED_PHASE20_PORTFOLIO_ONLY";
   p.label = "Paper portfolio pending";
}


void FP_ResetStateGatePaperRegimeRow(FP_StateGatePaperRegimeRow &r)
{
   r.slot_index = -1;
   r.timeframe = PERIOD_CURRENT;
   r.timeframe_label = "TF?";
   r.attributed_at = 0;
   r.last_closed_bar_time = 0;
   r.last_closed_bar_close = 0.0;
   r.status = FP_STATE_GATE_ROW_EMPTY;
   r.attribution_status = "PAPER_REGIME_PENDING";
   r.context_family = "PAPER_REGIME_CONTEXT_PENDING";
   r.source_context = "PAPER_REGIME_SOURCE_PENDING";
   r.mtf_context = "PAPER_REGIME_MTF_PENDING";
   r.mtf_direction_relation = "NO_MTF_DIRECTION_RELATION";
   r.mtf_side_relation = "NO_MTF_SIDE_RELATION";
   r.geometry_context = "PAPER_REGIME_GEOMETRY_PENDING";
   r.idea_family = "NO_IDEA_FAMILY";
   r.idea_type = "NO_IDEA_TYPE";
   r.decision_type = "NO_DECISION_TYPE";
   r.extreme_source = "NO_EXTREME_SOURCE";
   r.extreme_side = "NO_EXTREME_SIDE";
   r.hook_context = "NO_HOOK_CONTEXT";
   r.rally_context = "NO_RALLY_CONTEXT";
   r.lifecycle_path_state = "NO_LIFECYCLE_PATH";
   r.outcome = "NO_PAPER_OUTCOME";
   r.result_bucket = "NO_RESULT_BUCKET";
   r.price_delta = 0.0;
   r.r_status = "NO_R_STATUS";
   r.r_multiple = 0.0;
   r.source_result_key = "NO_SOURCE_RESULT_KEY";
   r.source_lifecycle_key = "NO_SOURCE_LIFECYCLE_KEY";
   r.source_portfolio_key = "NO_SOURCE_PORTFOLIO_KEY";
   r.attribution_key = "NO_PAPER_REGIME_KEY";
   r.execution_status = "REAL_EXECUTION_DISABLED_PHASE21_ATTRIBUTION_ONLY";
   r.label = "Paper regime attribution pending";
}


void FP_ResetStateGatePaperFilterRow(FP_StateGatePaperFilterRow &f)
{
   f.filter_index = -1;
   f.filter_name = "NO_FILTER";
   f.filter_family = "PAPER_FILTER_PENDING";
   f.filter_status = "PAPER_FILTER_PENDING";
   f.filter_rule = "NO_FILTER_RULE";
   f.rows_before = 0;
   f.rows_after = 0;
   f.win_like_rows = 0;
   f.loss_like_rows = 0;
   f.open_rows = 0;
   f.waiting_rows = 0;
   f.ambiguous_rows = 0;
   f.unknown_rows = 0;
   f.r_ready_rows = 0;
   f.r_pending_rows = 0;
   f.net_delta = 0.0;
   f.avg_delta = 0.0;
   f.avg_R = 0.0;
   f.pass_rate = 0.0;
   f.strongest_context = "NO_CONTEXT";
   f.diagnostic_key = "NO_PAPER_FILTER_KEY";
   f.execution_status = "REAL_EXECUTION_DISABLED_PHASE22_FILTER_ONLY";
   f.label = "Paper filter diagnostic pending";
}

void FP_ResetStateGateSnapshot(FP_StateGateSnapshot &s)
{
   s.initialized = false;
   s.symbol = "";
   s.chart_timeframe = PERIOD_CURRENT;
   s.generated_at = 0;
   s.timeframe_count = FP_STATE_GATE_TF_SLOTS;
   s.dirty_timeframes = 0;
   s.available_timeframes = 0;
   s.unchanged_timeframes = 0;
   s.unavailable_timeframes = 0;
   s.update_serial = 0;
   s.any_dirty = false;
   for(int i=0; i<FP_STATE_GATE_TF_SLOTS; i++)
      FP_ResetStateGateTimeframeState(s.tf_states[i]);
   for(int r=0; r<FP_STATE_GATE_MAX_RALLY_ROWS; r++)
      FP_ResetStateGateRallyRow(s.rally_rows[r]);
   for(int h=0; h<FP_STATE_GATE_MAX_HOOK_ROWS; h++)
      FP_ResetStateGateHookRow(s.hook_rows[h]);
   for(int x=0; x<FP_STATE_GATE_MAX_EXTREME_CANDIDATE_ROWS; x++)
      FP_ResetStateGateExtremeCandidateRow(s.extreme_candidate_rows[x]);
   for(int m=0; m<FP_STATE_GATE_MAX_MTF_ALIGNMENT_ROWS; m++)
      FP_ResetStateGateMtfAlignmentRow(s.mtf_alignment_rows[m]);
   for(int e=0; e<FP_STATE_GATE_MAX_ENTRY_IDEA_ROWS; e++)
      FP_ResetStateGateEntryIdeaRow(s.entry_idea_rows[e]);
   for(int d=0; d<FP_STATE_GATE_MAX_ENTRY_DECISION_ROWS; d++)
      FP_ResetStateGateEntryDecisionRow(s.entry_decision_rows[d]);
   for(int p=0; p<FP_STATE_GATE_MAX_PAPER_LEDGER_ROWS; p++)
      FP_ResetStateGatePaperLedgerRow(s.paper_ledger_rows[p]);
   for(int q=0; q<FP_STATE_GATE_MAX_PAPER_LIFECYCLE_ROWS; q++)
      FP_ResetStateGatePaperLifecycleRow(s.paper_lifecycle_rows[q]);
   for(int z=0; z<FP_STATE_GATE_MAX_PAPER_RESULT_ROWS; z++)
      FP_ResetStateGatePaperResultRow(s.paper_result_rows[z]);
   for(int a=0; a<FP_STATE_GATE_MAX_PAPER_PORTFOLIO_ROWS; a++)
      FP_ResetStateGatePaperPortfolioRow(s.paper_portfolio_rows[a]);
   for(int b=0; b<FP_STATE_GATE_MAX_PAPER_REGIME_ROWS; b++)
      FP_ResetStateGatePaperRegimeRow(s.paper_regime_rows[b]);
   for(int c=0; c<FP_STATE_GATE_MAX_PAPER_FILTER_ROWS; c++)
      FP_ResetStateGatePaperFilterRow(s.paper_filter_rows[c]);
   s.rally_row_count = 0;
   s.hook_row_count = 0;
   s.extreme_candidate_row_count = 0;
   s.mtf_alignment_row_count = 0;
   s.entry_idea_row_count = 0;
   s.entry_decision_row_count = 0;
   s.paper_ledger_row_count = 0;
   s.paper_lifecycle_row_count = 0;
   s.paper_result_row_count = 0;
   s.paper_portfolio_row_count = 0;
   s.paper_regime_row_count = 0;
   s.paper_filter_row_count = 0;
   s.paper_portfolio_status = "PAPER_PORTFOLIO_PENDING";
   s.paper_portfolio_key = "PAPER_PORTFOLIO_KEY_PENDING";
   s.paper_portfolio_total_results = 0;
   s.paper_portfolio_win_like_rows = 0;
   s.paper_portfolio_loss_like_rows = 0;
   s.paper_portfolio_open_rows = 0;
   s.paper_portfolio_waiting_rows = 0;
   s.paper_portfolio_ambiguous_rows = 0;
   s.paper_portfolio_unknown_rows = 0;
   s.paper_portfolio_r_ready_rows = 0;
   s.paper_portfolio_r_pending_rows = 0;
   s.paper_portfolio_net_delta = 0.0;
   s.paper_portfolio_avg_delta = 0.0;
   s.paper_portfolio_avg_R = 0.0;
   s.paper_portfolio_best_R = 0.0;
   s.paper_portfolio_worst_R = 0.0;
   s.paper_portfolio_distribution = "PAPER_DISTRIBUTION_PENDING";
   s.paper_portfolio_execution_status = "REAL_EXECUTION_DISABLED_PHASE20_PORTFOLIO_ONLY";
   s.paper_portfolio_notes = "PAPER_PORTFOLIO_PENDING";
   s.paper_filter_status = "PAPER_FILTER_PENDING";
   s.paper_filter_key = "PAPER_FILTER_KEY_PENDING";
   s.paper_filter_total_filters = 0;
   s.paper_filter_active_filters = 0;
   s.paper_filter_best_filter = "NO_BEST_FILTER";
   s.paper_filter_best_distribution = "NO_FILTER_DISTRIBUTION";
   s.paper_filter_best_avg_delta = 0.0;
   s.paper_filter_best_avg_R = 0.0;
   s.paper_filter_execution_status = "REAL_EXECUTION_DISABLED_PHASE22_FILTER_ONLY";
   s.paper_filter_notes = "PAPER_FILTER_PENDING";
   s.status = "reset";
   s.reason = "reset";
}

void FP_ResetStateGateRuntime(FP_StateGateRuntime &rt)
{
   rt.initialized = false;
   rt.minimized = false;
   rt.panel_has_drawn = false;
   rt.export_has_written = false;
   rt.last_run_had_dirty = false;
   for(int i=0; i<FP_STATE_GATE_TF_SLOTS; i++)
   {
      rt.last_processed_closed_bar_time[i] = 0;
      rt.previous_closed_bar_time[i] = 0;
      rt.slot_initialized[i] = false;
      rt.slot_update_count[i] = 0;
   }
   rt.update_serial = 0;
   rt.last_engine_run_time = 0;
   FP_ResetStateGateSnapshot(rt.snapshot);
}

void FP_ResetStateGateReport(FP_StateGateReport &r)
{
   r.attempted = false;
   r.ok = true;
   r.status = "not_run";
   r.reason = "not_attempted";
   r.version = FP_STATE_GATE_VERSION;
   r.symbol = "";
   r.timeframe_count = 0;
   r.slots_checked = 0;
   r.available_timeframes = 0;
   r.dirty_timeframes = 0;
   r.unchanged_timeframes = 0;
   r.unavailable_timeframes = 0;
   r.rally_rows = 0;
   r.hook_rows = 0;
   r.contract_rows = 0;
   r.extreme_candidate_rows = 0;
   r.mtf_alignment_rows = 0;
   r.geometry_rows = 0;
   r.entry_idea_rows = 0;
   r.entry_decision_rows = 0;
   r.paper_ledger_rows = 0;
   r.paper_lifecycle_rows = 0;
   r.paper_result_rows = 0;
   r.paper_portfolio_rows = 0;
   r.paper_regime_rows = 0;
   r.paper_filter_rows = 0;
   r.objects_requested = 0;
   r.objects_created = 0;
   r.object_errors = 0;
   r.objects_deleted = 0;
   r.files_written = 0;
   r.file_errors = 0;
   r.panel_redrawn = false;
   r.export_attempted = false;
   r.skipped_no_dirty = false;
}

void FP_DefaultStateGateConfig(FP_StateGateConfig &cfg)
{
   cfg.enabled = true;
   cfg.tf1 = PERIOD_M1;
   cfg.tf2 = PERIOD_M10;
   cfg.tf3 = PERIOD_H1;
   cfg.panel_enabled = true;
   cfg.panel_start_minimized = false;
   cfg.panel_corner = CORNER_LEFT_UPPER;
   cfg.panel_x = 16;
   cfg.panel_y = 24;
   cfg.panel_width = 560;
   cfg.panel_font_size = 8;
   cfg.panel_rally_preview_rows_per_tf = 2;
   cfg.panel_hook_preview_rows_per_tf = 2;
   cfg.panel_force_right_upper = false;
   cfg.panel_force_left_upper = true;
   cfg.panel_compact_mode = true;
   cfg.panel_show_closed_bar = true;
   cfg.panel_show_row_counts = true;
   cfg.panel_show_contract_key = true;
   cfg.panel_show_diagnostics = true;
   cfg.max_rally_rows_per_tf = 6;
   cfg.max_hook_rows_per_tf = 10;
   cfg.max_extreme_candidates_per_tf = 8;
   cfg.show_ids = true;
   cfg.show_scale_l = true;
   cfg.export_csv = true;
   cfg.export_overwrite_latest = true;
   cfg.export_contract_csv = true;
   cfg.export_diagnostics_csv = true;
   cfg.export_panel_lines_csv = true;
   cfg.export_entry_bridge_csv = true;
   cfg.export_extreme_candidates_csv = true;
   cfg.export_mtf_alignment_csv = true;
   cfg.export_entry_geometry_csv = true;
   cfg.export_entry_ideas_csv = true;
   cfg.export_entry_decisions_csv = true;
   cfg.export_paper_ledger_csv = true;
   cfg.export_paper_lifecycle_csv = true;
   cfg.export_paper_results_csv = true;
   cfg.export_paper_portfolio_csv = true;
   cfg.export_paper_regime_csv = true;
   cfg.export_paper_filters_csv = true;
   cfg.export_folder = FP_STATE_GATE_DEFAULT_EXPORT_FOLDER;
   cfg.print_audit = true;
   cfg.object_prefix = FP_STATE_GATE_DEFAULT_PREFIX;
}

#endif // __FP_STATE_GATE_TYPES_MQH__
