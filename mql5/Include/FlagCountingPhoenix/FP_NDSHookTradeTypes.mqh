#ifndef __FP_NDS_HOOK_TRADE_TYPES_MQH__
#define __FP_NDS_HOOK_TRADE_TYPES_MQH__
#property strict

#include "FP_NDSEntryTypes.mqh"

#define FP_NDS_HOOK_TRADE_VERSION "NDS-HOOK-TRADE-03"
#define FP_NDS_HOOK_TRADE_SCHEMA_VERSION "nds_hook_trade_v3"
#define FP_NDS_HOOK_TERMINAL_F123_SCHEMA_VERSION "nds_hook_limit_f123_exit_v1"
#define FP_NDS_HOOK_864_CYCLE_R1_SCHEMA_VERSION "nds_hook_864_cycle_r1_v2"
#define FP_NDS_HOOK_864_ENTRY_RATIO 0.864
#define FP_NDS_HOOK_864_MIN_X_COUNT 3
#define FP_NDS_HOOK_864_MAX_X_COUNT 4
#define FP_NDS_HOOK_864_REWARD_R 1.0
#define FP_NDS_HOOK_864_CLOSURE_RATIO 0.50

enum FP_NDSHookTradeProfile
{
   // Existing Phase 52 behavior. Preserved as the default for backward
   // compatibility: terminal limit entry and same-direction F123 exit.
   FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123 = 0,

   // Integrated NDS profile requested by the architect: canonical Hook cycle
   // with exactly 3 or 4 counted X nodes, limit at the 86.4% crown-to-origin
   // level, structural stop behind the Hook cycle, and attached fixed 1R TP.
   FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1 = 1
};

enum FP_NDSHookTradeSizingMode
{
   FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME = 0,
   FP_NDS_HOOK_TRADE_SIZE_RISK_CASH = 1
};

enum FP_NDSHookTradeAction
{
   FP_NDS_HOOK_TRADE_ACTION_NONE = 0,
   FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT = 1,
   FP_NDS_HOOK_TRADE_ACTION_LIMIT_SENT = 2,
   FP_NDS_HOOK_TRADE_ACTION_PENDING_HELD = 3,
   FP_NDS_HOOK_TRADE_ACTION_POSITION_HELD = 4,
   FP_NDS_HOOK_TRADE_ACTION_PENDING_CANCELLED = 5,
   FP_NDS_HOOK_TRADE_ACTION_POSITION_CLOSED_F3 = 6,
   FP_NDS_HOOK_TRADE_ACTION_BLOCKED = 7
};

struct FP_NDSHookTradeConfig
{
   bool enabled;
   bool send_live_orders;
   bool allow_hook_after_hook;
   bool allow_hook_after_f3;
   bool require_closed_hook;
   bool one_attempt_per_hook;
   bool reset_used_setups_on_init;
   bool cancel_pending_on_death;
   bool require_full_f123_after_entry;
   bool export_csv;
   bool print_summary;

   FP_NDSHookTradeProfile profile;

   // HOOK_864_CYCLE_R1 profile parameters. The profile is intentionally
   // narrow; defaults encode the approved setup and preserve no inference.
   double hook_entry_ratio;
   int hook_entry_min_x_count;
   int hook_entry_max_x_count;
   bool hook_entry_require_confirmed_terminal;
   bool hook_entry_require_level_untouched;
   bool hook_entry_require_phase04_x_closed;
   double hook_entry_closure_ratio;
   double fixed_reward_r;

   FP_NDSHookTradeSizingMode sizing_mode;
   double fixed_volume;
   double risk_cash;
   double commission_per_lot_round_turn;
   bool allow_min_lot_if_risk_too_small;

   int stop_buffer_points;
   double stop_spread_multiplier;
   int max_deviation_points;
   int entry_lock_timeout_seconds;
   long magic;
   string comment_prefix;
   string folder;
};

struct FP_NDSHookTradeSetup
{
   bool available;
   bool eligible;
   bool already_used;
   string status;
   string reason;

   int sequence_id;
   int direction;
   string direction_label;
   string family;
   string profile_label;
   bool valid_after_hook;
   bool valid_after_f3;
   datetime structure_time;

   int x_count;
   double origin_price;
   double crown_price;
   double terminal_price;
   double terminal_retracement_ratio;
   double entry_ratio;
   bool entry_level_untouched;
   bool phase04_evidence_found;
   bool phase04_x_closed;
   datetime x_closure_time;
   double x_closure_price;
   double x_closure_threshold_price;
   bool cycle_dead_after_terminal;
   bool first_864_touch_found;
   datetime first_864_touch_time;
   double first_864_touch_price;

   double entry_price;
   double death_price;
   double stop_price;
   double target_price;
   double risk_distance;
   double reward_distance;
   double reward_r;
   double volume;
   string setup_key;
   string broker_comment;
};

struct FP_NDSHookTradeExitSignal
{
   bool found;
   int event_id;
   int sequence_id;
   int direction;
   datetime f1_start_time;
   datetime f2_start_time;
   datetime f3_terminal_time;
   double f3_terminal_price;
   string reason;
};


struct FP_NDSHookTradeCandidateFunnel
{
   int sequences_total;
   int canonical_valid;
   int valid_family;
   int family_allowed;
   int confirmed_terminal;
   int crown_valid;
   int x3_x4;
   int mature_or_capped;
   int phase04_evidence_found;
   int phase04_x_closed;
   int alive_after_closure;
   int first_864_untouched;
   int execution_ready;
   string dominant_blocker;
};

struct FP_NDSHookTradeReport
{
   datetime generated_at;
   string version;
   string schema_version;
   string symbol;
   ENUM_TIMEFRAMES period;

   bool attempted;
   bool ok;
   FP_NDSHookTradeAction action;
   string action_label;
   string status;
   string reason;

   int managed_pending_count;
   int managed_position_count;
   int foreign_symbol_position_count;
   ulong order_ticket;
   ulong position_ticket;
   ulong close_ticket;

   FP_NDSHookTradeSetup setup;
   FP_NDSHookTradeCandidateFunnel funnel;
   FP_NDSHookTradeExitSignal exit_signal;
   string state_key;
};

void FP_ResetNDSHookTradeConfig(FP_NDSHookTradeConfig &cfg)
{
   cfg.enabled = false;
   cfg.send_live_orders = false;
   cfg.allow_hook_after_hook = true;
   cfg.allow_hook_after_f3 = true;
   cfg.require_closed_hook = true;
   cfg.one_attempt_per_hook = true;
   cfg.reset_used_setups_on_init = false;
   cfg.cancel_pending_on_death = true;
   cfg.require_full_f123_after_entry = true;
   cfg.export_csv = true;
   cfg.print_summary = true;

   cfg.profile = FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123;
   cfg.hook_entry_ratio = FP_NDS_HOOK_864_ENTRY_RATIO;
   cfg.hook_entry_min_x_count = FP_NDS_HOOK_864_MIN_X_COUNT;
   cfg.hook_entry_max_x_count = FP_NDS_HOOK_864_MAX_X_COUNT;
   cfg.hook_entry_require_confirmed_terminal = true;
   cfg.hook_entry_require_level_untouched = true;
   cfg.hook_entry_require_phase04_x_closed = true;
   cfg.hook_entry_closure_ratio = FP_NDS_HOOK_864_CLOSURE_RATIO;
   cfg.fixed_reward_r = FP_NDS_HOOK_864_REWARD_R;

   cfg.sizing_mode = FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME;
   cfg.fixed_volume = 0.01;
   cfg.risk_cash = 100.0;
   cfg.commission_per_lot_round_turn = 0.0;
   cfg.allow_min_lot_if_risk_too_small = false;

   cfg.stop_buffer_points = 1;
   cfg.stop_spread_multiplier = 1.0;
   cfg.max_deviation_points = 20;
   cfg.entry_lock_timeout_seconds = 30;
   cfg.magic = 310052;
   cfg.comment_prefix = "NDSH";
   cfg.folder = "FlagCountingPhoenix";
}

void FP_ResetNDSHookTradeSetup(FP_NDSHookTradeSetup &s)
{
   s.available = false;
   s.eligible = false;
   s.already_used = false;
   s.status = "RESET";
   s.reason = "reset";
   s.sequence_id = -1;
   s.direction = FP_DIR_NONE;
   s.direction_label = "NONE";
   s.family = "NONE";
   s.profile_label = "NONE";
   s.valid_after_hook = false;
   s.valid_after_f3 = false;
   s.structure_time = 0;
   s.x_count = 0;
   s.origin_price = 0.0;
   s.crown_price = 0.0;
   s.terminal_price = 0.0;
   s.terminal_retracement_ratio = 0.0;
   s.entry_ratio = 0.0;
   s.entry_level_untouched = false;
   s.phase04_evidence_found = false;
   s.phase04_x_closed = false;
   s.x_closure_time = 0;
   s.x_closure_price = 0.0;
   s.x_closure_threshold_price = 0.0;
   s.cycle_dead_after_terminal = false;
   s.first_864_touch_found = false;
   s.first_864_touch_time = 0;
   s.first_864_touch_price = 0.0;
   s.entry_price = 0.0;
   s.death_price = 0.0;
   s.stop_price = 0.0;
   s.target_price = 0.0;
   s.risk_distance = 0.0;
   s.reward_distance = 0.0;
   s.reward_r = 0.0;
   s.volume = 0.0;
   s.setup_key = "";
   s.broker_comment = "";
}

void FP_ResetNDSHookTradeExitSignal(FP_NDSHookTradeExitSignal &x)
{
   x.found = false;
   x.event_id = -1;
   x.sequence_id = -1;
   x.direction = FP_DIR_NONE;
   x.f1_start_time = 0;
   x.f2_start_time = 0;
   x.f3_terminal_time = 0;
   x.f3_terminal_price = 0.0;
   x.reason = "none";
}


void FP_ResetNDSHookTradeCandidateFunnel(FP_NDSHookTradeCandidateFunnel &f)
{
   f.sequences_total = 0;
   f.canonical_valid = 0;
   f.valid_family = 0;
   f.family_allowed = 0;
   f.confirmed_terminal = 0;
   f.crown_valid = 0;
   f.x3_x4 = 0;
   f.mature_or_capped = 0;
   f.phase04_evidence_found = 0;
   f.phase04_x_closed = 0;
   f.alive_after_closure = 0;
   f.first_864_untouched = 0;
   f.execution_ready = 0;
   f.dominant_blocker = "not_evaluated";
}

void FP_ResetNDSHookTradeReport(FP_NDSHookTradeReport &r)
{
   r.generated_at = TimeCurrent();
   r.version = FP_NDS_HOOK_TRADE_VERSION;
   r.schema_version = FP_NDS_HOOK_TRADE_SCHEMA_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.attempted = false;
   r.ok = false;
   r.action = FP_NDS_HOOK_TRADE_ACTION_NONE;
   r.action_label = "NONE";
   r.status = "RESET";
   r.reason = "reset";
   r.managed_pending_count = 0;
   r.managed_position_count = 0;
   r.foreign_symbol_position_count = 0;
   r.order_ticket = 0;
   r.position_ticket = 0;
   r.close_ticket = 0;
   FP_ResetNDSHookTradeSetup(r.setup);
   FP_ResetNDSHookTradeCandidateFunnel(r.funnel);
   FP_ResetNDSHookTradeExitSignal(r.exit_signal);
   r.state_key = "";
}

#endif // __FP_NDS_HOOK_TRADE_TYPES_MQH__
