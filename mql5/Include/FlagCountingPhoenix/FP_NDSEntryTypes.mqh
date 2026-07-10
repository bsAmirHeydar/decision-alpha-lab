#ifndef __FP_NDS_ENTRY_TYPES_MQH__
#define __FP_NDS_ENTRY_TYPES_MQH__
#property strict

#include "FP_NDSStructureSnapshot.mqh"

#define FP_NDS_ENTRY_VERSION "NDS-ENTRY-TRANSITION-01"
#define FP_NDS_ENTRY_SCHEMA_VERSION "nds_entry_transition_v1"
#define FP_NDS_ENTRY_DEFAULT_FOLDER "FlagCountingPhoenix"

// This layer is intentionally broker-neutral.  All profiles remain NO-SEND.
enum FP_NDSEntryContractProfile
{
   FP_NDS_ENTRY_PROFILE_PRE_CANON_BLOCKED = 0,
   FP_NDS_ENTRY_PROFILE_DIAGNOSTIC_MANUAL_GEOMETRY = 1,
   FP_NDS_ENTRY_PROFILE_CANONICAL_ZONE_ADAPTER = 2
};

enum FP_NDSTradeDirectionPolicy
{
   FP_NDS_TRADE_DIRECTION_UNRESOLVED = 0,
   FP_NDS_TRADE_DIRECTION_FOLLOW_HOOK = 1,
   FP_NDS_TRADE_DIRECTION_REVERSE_HOOK = 2
};

enum FP_NDSEntryOrderModel
{
   FP_NDS_ORDER_MODEL_UNRESOLVED = 0,
   FP_NDS_ORDER_MODEL_LIMIT_FIRST_EDGE = 1,
   FP_NDS_ORDER_MODEL_LIMIT_MID_ZONE = 2,
   FP_NDS_ORDER_MODEL_LIMIT_NEAR_DEATH = 3,
   FP_NDS_ORDER_MODEL_MARKET_AFTER_CONFIRMATION = 4,
   FP_NDS_ORDER_MODEL_LADDER_LIMIT = 5
};

enum FP_NDSStopModel
{
   FP_NDS_STOP_MODEL_UNRESOLVED = 0,
   FP_NDS_STOP_MODEL_BEYOND_ZONE = 1,
   FP_NDS_STOP_MODEL_BEYOND_ORIGIN = 2,
   FP_NDS_STOP_MODEL_BEYOND_DEATH_BOUNDARY = 3,
   FP_NDS_STOP_MODEL_MANUAL_DIAGNOSTIC = 4
};

enum FP_NDSTargetModel
{
   FP_NDS_TARGET_MODEL_UNRESOLVED = 0,
   FP_NDS_TARGET_MODEL_CROWN = 1,
   FP_NDS_TARGET_MODEL_ORIGIN = 2,
   FP_NDS_TARGET_MODEL_NEXT_STRUCTURE = 3,
   FP_NDS_TARGET_MODEL_FIXED_R = 4,
   FP_NDS_TARGET_MODEL_MANUAL_DIAGNOSTIC = 5
};

enum FP_NDSEntryPipelineStage
{
   FP_NDS_ENTRY_STAGE_RESET = 0,
   FP_NDS_ENTRY_STAGE_STRUCTURE_CAPTURED = 1,
   FP_NDS_ENTRY_STAGE_SETUP_CANDIDATE = 2,
   FP_NDS_ENTRY_STAGE_TRADE_PLAN_READY = 3,
   FP_NDS_ENTRY_STAGE_COMMAND_PREVIEW_READY = 4,
   FP_NDS_ENTRY_STAGE_BLOCKED = -1
};

struct FP_NDSEntryConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;

   FP_NDSEntryContractProfile contract_profile;
   FP_NDSTradeDirectionPolicy trade_direction_policy;
   FP_NDSEntryOrderModel order_model;
   FP_NDSStopModel stop_model;
   FP_NDSTargetModel target_model;

   bool require_valid_hook_family;
   bool require_closed_hook;
   bool require_zone_canon_locked;
   bool zone_canon_locked;
   bool require_trade_contract_locked;
   bool trade_contract_locked;
   bool command_preview_only;

   double manual_zone_lower;
   double manual_zone_upper;
   double manual_entry_price;
   double manual_stop_price;
   double manual_target_price;
   double min_rr;
   int expiry_bars;

   long preview_magic;
   string preview_comment;
   string folder;
};

struct FP_NDSStructureRow
{
   bool available;
   bool eligible;
   string status;
   string block_reason;

   int sequence_id;
   int scale_l;
   int hook_direction;
   string hook_direction_label;
   string validity_family;
   string post_f3_subfamily;
   bool valid_after_hook;
   bool valid_after_opposing_f3;
   bool valid_hook_family;
   bool sequence_valid;
   bool hook_failed;
   bool hook_closed;
   bool near_death_confirmed;
   bool resolve_confirmed;

   int origin_bar_index;
   datetime origin_time;
   double origin_price;
   int crown_node_id;
   datetime crown_time;
   double crown_price;
   int terminal_node_id;
   datetime terminal_time;
   double terminal_price;
   double death_boundary_price;
   double completion_pct;

   int parent_hook_sequence_id;
   int opposing_f3_event_id;
   int opposing_f3_terminal_bar_index;
   datetime opposing_f3_terminal_time;
   double opposing_f3_terminal_price;

   string structure_key;
};

struct FP_NDSZoneRow
{
   bool available;
   bool canonical;
   string status;
   string block_reason;
   string zone_id;
   string source_mode;

   double lower_price;
   double upper_price;
   double width;
   double entry_edge_price;
   double death_edge_price;
   double planned_entry_price;
   double planned_stop_price;
   double planned_target_price;

   bool boundaries_valid;
   bool directional_geometry_valid;
   string zone_key;
};

struct FP_NDSSetupRow
{
   bool candidate_created;
   bool ready;
   string status;
   string block_reason;
   string setup_id;
   string setup_family;
   string source_structure_key;
   string source_zone_key;

   int trade_direction;
   string trade_direction_label;
   FP_NDSEntryOrderModel order_model;
   FP_NDSStopModel stop_model;
   FP_NDSTargetModel target_model;

   int created_bar_index;
   datetime created_time;
   int expiry_bars;
   int expires_bar_index;
   string setup_key;
};

struct FP_NDSTradePlanRow
{
   bool ready;
   string status;
   string block_reason;
   string plan_id;
   string source_setup_id;

   int trade_direction;
   string trade_direction_label;
   double entry_price;
   double stop_price;
   double target_price;
   double risk_distance;
   double reward_distance;
   double rr;
   double min_rr_required;

   double requested_risk_fraction;
   double requested_volume;
   string sizing_status;
   string plan_key;
};

struct FP_NDSCommandPreviewRow
{
   bool built;
   bool send_allowed;
   string status;
   string block_reason;
   string command_id;
   string source_plan_id;

   string command_action;
   string order_type_preview;
   string symbol;
   int trade_direction;
   string trade_direction_label;
   double volume;
   double price;
   double sl;
   double tp;
   int expiry_bars;
   long magic;
   string comment;
   string command_key;
   string execution_status;
};

struct FP_NDSEntryPipelineRow
{
   datetime generated_at;
   string version;
   string schema_version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   FP_NDSEntryPipelineStage stage;
   string stage_label;
   string status;
   string block_reason;

   FP_NDSStructureRow structure;
   FP_NDSZoneRow zone;
   FP_NDSSetupRow setup;
   FP_NDSTradePlanRow plan;
   FP_NDSCommandPreviewRow command;

   string no_send_contract;
   string pipeline_key;
};

struct FP_NDSEntryReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool structure_written;
   bool setup_written;
   bool plan_written;
   bool command_written;
   bool summary_written;
};

void FP_ResetNDSEntryConfig(FP_NDSEntryConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;

   cfg.contract_profile = FP_NDS_ENTRY_PROFILE_PRE_CANON_BLOCKED;
   cfg.trade_direction_policy = FP_NDS_TRADE_DIRECTION_UNRESOLVED;
   cfg.order_model = FP_NDS_ORDER_MODEL_UNRESOLVED;
   cfg.stop_model = FP_NDS_STOP_MODEL_UNRESOLVED;
   cfg.target_model = FP_NDS_TARGET_MODEL_UNRESOLVED;

   cfg.require_valid_hook_family = true;
   cfg.require_closed_hook = true;
   cfg.require_zone_canon_locked = true;
   cfg.zone_canon_locked = false;
   cfg.require_trade_contract_locked = true;
   cfg.trade_contract_locked = false;
   cfg.command_preview_only = true;

   cfg.manual_zone_lower = 0.0;
   cfg.manual_zone_upper = 0.0;
   cfg.manual_entry_price = 0.0;
   cfg.manual_stop_price = 0.0;
   cfg.manual_target_price = 0.0;
   cfg.min_rr = 0.0;
   cfg.expiry_bars = 0;

   cfg.preview_magic = 310001;
   cfg.preview_comment = "DAL_NDS_ENTRY_PREVIEW_ONLY";
   cfg.folder = FP_NDS_ENTRY_DEFAULT_FOLDER;
}

void FP_ResetNDSStructureRow(FP_NDSStructureRow &r)
{
   r.available = false;
   r.eligible = false;
   r.status = "NDS_STRUCTURE_RESET";
   r.block_reason = "RESET";
   r.sequence_id = -1;
   r.scale_l = 0;
   r.hook_direction = 0;
   r.hook_direction_label = "HOOK_DIRECTION_NONE";
   r.validity_family = "NONE";
   r.post_f3_subfamily = "NONE";
   r.valid_after_hook = false;
   r.valid_after_opposing_f3 = false;
   r.valid_hook_family = false;
   r.sequence_valid = false;
   r.hook_failed = false;
   r.hook_closed = false;
   r.near_death_confirmed = false;
   r.resolve_confirmed = false;
   r.origin_bar_index = -1;
   r.origin_time = 0;
   r.origin_price = 0.0;
   r.crown_node_id = -1;
   r.crown_time = 0;
   r.crown_price = 0.0;
   r.terminal_node_id = -1;
   r.terminal_time = 0;
   r.terminal_price = 0.0;
   r.death_boundary_price = 0.0;
   r.completion_pct = 0.0;
   r.parent_hook_sequence_id = -1;
   r.opposing_f3_event_id = -1;
   r.opposing_f3_terminal_bar_index = -1;
   r.opposing_f3_terminal_time = 0;
   r.opposing_f3_terminal_price = 0.0;
   r.structure_key = "";
}

void FP_ResetNDSZoneRow(FP_NDSZoneRow &r)
{
   r.available = false;
   r.canonical = false;
   r.status = "NDS_ZONE_RESET";
   r.block_reason = "RESET";
   r.zone_id = "";
   r.source_mode = "NONE";
   r.lower_price = 0.0;
   r.upper_price = 0.0;
   r.width = 0.0;
   r.entry_edge_price = 0.0;
   r.death_edge_price = 0.0;
   r.planned_entry_price = 0.0;
   r.planned_stop_price = 0.0;
   r.planned_target_price = 0.0;
   r.boundaries_valid = false;
   r.directional_geometry_valid = false;
   r.zone_key = "";
}

void FP_ResetNDSSetupRow(FP_NDSSetupRow &r)
{
   r.candidate_created = false;
   r.ready = false;
   r.status = "NDS_SETUP_RESET";
   r.block_reason = "RESET";
   r.setup_id = "";
   r.setup_family = "NONE";
   r.source_structure_key = "";
   r.source_zone_key = "";
   r.trade_direction = FP_DIR_NONE;
   r.trade_direction_label = "TRADE_DIRECTION_NONE";
   r.order_model = FP_NDS_ORDER_MODEL_UNRESOLVED;
   r.stop_model = FP_NDS_STOP_MODEL_UNRESOLVED;
   r.target_model = FP_NDS_TARGET_MODEL_UNRESOLVED;
   r.created_bar_index = -1;
   r.created_time = 0;
   r.expiry_bars = 0;
   r.expires_bar_index = -1;
   r.setup_key = "";
}

void FP_ResetNDSTradePlanRow(FP_NDSTradePlanRow &r)
{
   r.ready = false;
   r.status = "NDS_TRADE_PLAN_RESET";
   r.block_reason = "RESET";
   r.plan_id = "";
   r.source_setup_id = "";
   r.trade_direction = FP_DIR_NONE;
   r.trade_direction_label = "TRADE_DIRECTION_NONE";
   r.entry_price = 0.0;
   r.stop_price = 0.0;
   r.target_price = 0.0;
   r.risk_distance = 0.0;
   r.reward_distance = 0.0;
   r.rr = 0.0;
   r.min_rr_required = 0.0;
   r.requested_risk_fraction = 0.0;
   r.requested_volume = 0.0;
   r.sizing_status = "SIZING_DISABLED_NO_CAPITAL_AUTHORITY";
   r.plan_key = "";
}

void FP_ResetNDSCommandPreviewRow(FP_NDSCommandPreviewRow &r)
{
   r.built = false;
   r.send_allowed = false;
   r.status = "NDS_COMMAND_RESET";
   r.block_reason = "RESET";
   r.command_id = "";
   r.source_plan_id = "";
   r.command_action = "NO_ACTION";
   r.order_type_preview = "ORDER_TYPE_UNRESOLVED";
   r.symbol = "";
   r.trade_direction = FP_DIR_NONE;
   r.trade_direction_label = "TRADE_DIRECTION_NONE";
   r.volume = 0.0;
   r.price = 0.0;
   r.sl = 0.0;
   r.tp = 0.0;
   r.expiry_bars = 0;
   r.magic = 0;
   r.comment = "";
   r.command_key = "";
   r.execution_status = "NO_SEND_NDS_COMMAND_PREVIEW_ONLY";
}

void FP_ResetNDSEntryPipelineRow(FP_NDSEntryPipelineRow &r)
{
   r.generated_at = 0;
   r.version = FP_NDS_ENTRY_VERSION;
   r.schema_version = FP_NDS_ENTRY_SCHEMA_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";
   r.attempted = false;
   r.stage = FP_NDS_ENTRY_STAGE_RESET;
   r.stage_label = "RESET";
   r.status = "NDS_ENTRY_PIPELINE_RESET";
   r.block_reason = "RESET";
   FP_ResetNDSStructureRow(r.structure);
   FP_ResetNDSZoneRow(r.zone);
   FP_ResetNDSSetupRow(r.setup);
   FP_ResetNDSTradePlanRow(r.plan);
   FP_ResetNDSCommandPreviewRow(r.command);
   r.no_send_contract = "NDS_ENTRY_TRANSITION_NO_ORDER_NO_BROKER_NO_VOLUME_NO_CAPITAL_AUTHORITY";
   r.pipeline_key = "";
}

void FP_ResetNDSEntryReport(FP_NDSEntryReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.structure_written = false;
   r.setup_written = false;
   r.plan_written = false;
   r.command_written = false;
   r.summary_written = false;
}

#endif // __FP_NDS_ENTRY_TYPES_MQH__
