#ifndef __DAL_E0009_TYPES_MQH__
#define __DAL_E0009_TYPES_MQH__

#include <DecisionAlphaLab/Common/DAL_Common.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>

enum ENUM_DAL_E0009_HTF_123_DIRECTION
{
   DAL_E0009_123_NONE = 0,
   DAL_E0009_123_HIGHER_HIGHS = 1,
   DAL_E0009_123_LOWER_LOWS = -1
};

#define DAL_E0009_123_BULLISH DAL_E0009_123_HIGHER_HIGHS
#define DAL_E0009_123_BEARISH DAL_E0009_123_LOWER_LOWS

enum ENUM_DAL_E0009_COUNTER_MODE
{
   DAL_E0009_COUNTER_OPPOSITE_123 = 0,
   DAL_E0009_COUNTER_BOTH_FOR_TEST = 1
};

enum ENUM_DAL_E0009_EXIT_MODE
{
   DAL_E0009_EXIT_FIXED_R = 0,
   DAL_E0009_EXIT_TF_MONOTONIC_PATTERN = 1,
   DAL_E0009_EXIT_NO_TP = 2
};

#define DAL_E0009_EXIT_HTF_THIRD_OPPOSITE_SWING DAL_E0009_EXIT_TF_MONOTONIC_PATTERN
#define DAL_E0009_EXIT_HTF_POINT_2 DAL_E0009_EXIT_FIXED_R

enum ENUM_DAL_E0009_ORDER_MODE
{
   DAL_E0009_ORDER_LIMIT_REVISIT = 0,
   DAL_E0009_ORDER_STOP_RECLAIM = 1,
   DAL_E0009_ORDER_MARKET_ON_CONFIRM = 2,
   DAL_E0009_ORDER_AUTO = 3
};

enum ENUM_DAL_E0009_SIGNAL_ORDER_KIND
{
   DAL_E0009_KIND_NONE = 0,
   DAL_E0009_KIND_MARKET = 1,
   DAL_E0009_KIND_LIMIT = 2,
   DAL_E0009_KIND_STOP = 3
};

struct DALE0009PatternState
{
   bool valid;
   string reason;

   ENUM_TIMEFRAMES tf;
   ENUM_DAL_E0009_HTF_123_DIRECTION direction;

   int required_count;
   DALLRuleNode p1;
   DALLRuleNode p2;
   DALLRuleNode p3;

   datetime closed_time;
   int age_bars;
   double amplitude;
};

#define DALE0009HTF123State DALE0009PatternState

struct DALE0009HookSignal
{
   bool valid;
   string reason;

   int direction;
   ENUM_DAL_E0009_ORDER_MODE order_mode;
   ENUM_DAL_E0009_SIGNAL_ORDER_KIND order_kind;

   DALLRuleNode hook_node;

   double zone_lower;
   double zone_upper;

   double entry;
   double sl;
   double tp;
   double risk_distance;
   double potential_r;

   string comment;
};

struct DALE0009Config
{
   int setup_L;
   double zone_ratio;

   int m1_max_hook_age_bars;
   bool require_fresh_m1_hook_after_setup_close;
   bool reject_hunted_m1_hook;
   int max_hook_candidates_per_bar;

   bool use_micro_only_filter;
   double max_hook_risk_to_setup_amplitude;
   int micro_avg_range_bars;
   double max_hook_risk_to_m1_avg_range;
   int max_hook_risk_points;

   double fixed_r;
   int exit_node_count;

   double buy_entry_spread_mult;
   double sell_stop_spread_mult;

   ENUM_DAL_E0009_COUNTER_MODE counter_mode;
   ENUM_DAL_E0009_EXIT_MODE exit_mode;
   ENUM_DAL_E0009_ORDER_MODE order_mode;
};

struct DALE0009Diagnostics
{
   int macro_ok;
   int macro_missing;
   int macro_conflict;

   int setup_ok;
   int setup_missing;
   int setup_conflict;

   int m1_map_ok;
   int m1_map_failed;

   int hook_seen;
   int hook_after_time_reject;
   int hook_age_reject;
   int hook_zone_failed;
   int hook_hunted_reject;
   int hook_micro_reject;
   int hook_built;

   int geometry_reject;
   int risk_reject;
   int cap_reject;
   int duplicate_skip;

   int planned;
   int sent_or_plan;
};

void DAL_E0009_ResetDiagnostics(DALE0009Diagnostics &d)
{
   d.macro_ok = 0;
   d.macro_missing = 0;
   d.macro_conflict = 0;
   d.setup_ok = 0;
   d.setup_missing = 0;
   d.setup_conflict = 0;
   d.m1_map_ok = 0;
   d.m1_map_failed = 0;
   d.hook_seen = 0;
   d.hook_after_time_reject = 0;
   d.hook_age_reject = 0;
   d.hook_zone_failed = 0;
   d.hook_hunted_reject = 0;
   d.hook_micro_reject = 0;
   d.hook_built = 0;
   d.geometry_reject = 0;
   d.risk_reject = 0;
   d.cap_reject = 0;
   d.duplicate_skip = 0;
   d.planned = 0;
   d.sent_or_plan = 0;
}

void DAL_E0009_ResetNode(DALLRuleNode &n, const ENUM_DALNodeType type)
{
   n.id = -1;
   n.index = -1;
   n.active_from_index = -1;
   n.time = 0;
   n.active_from_time = 0;
   n.type = type;
   n.price = 0.0;
   n.confirmed = false;
}

void DAL_E0009_ResetPattern(DALE0009PatternState &s)
{
   s.valid = false;
   s.reason = "not_built";
   s.tf = PERIOD_CURRENT;
   s.direction = DAL_E0009_123_NONE;
   s.required_count = 0;
   DAL_E0009_ResetNode(s.p1, DAL_NODE_HIGH);
   DAL_E0009_ResetNode(s.p2, DAL_NODE_HIGH);
   DAL_E0009_ResetNode(s.p3, DAL_NODE_HIGH);
   s.closed_time = 0;
   s.age_bars = 0;
   s.amplitude = 0.0;
}

void DAL_E0009_Reset123(DALE0009HTF123State &s)
{
   DAL_E0009_ResetPattern(s);
}

void DAL_E0009_ResetHook(DALE0009HookSignal &h)
{
   h.valid = false;
   h.reason = "not_built";
   h.direction = 0;
   h.order_mode = DAL_E0009_ORDER_AUTO;
   h.order_kind = DAL_E0009_KIND_NONE;
   DAL_E0009_ResetNode(h.hook_node, DAL_NODE_LOW);
   h.zone_lower = 0.0;
   h.zone_upper = 0.0;
   h.entry = 0.0;
   h.sl = 0.0;
   h.tp = 0.0;
   h.risk_distance = 0.0;
   h.potential_r = 0.0;
   h.comment = "";
}

string DAL_E0009DirectionName(const ENUM_DAL_E0009_HTF_123_DIRECTION d)
{
   if(d == DAL_E0009_123_HIGHER_HIGHS) return "RISING_HIGHS_MODE_SELL";
   if(d == DAL_E0009_123_LOWER_LOWS) return "FALLING_LOWS_MODE_BUY";
   return "NONE";
}

int DAL_E0009TradeDirectionFromPattern(const DALE0009PatternState &state)
{
   if(!state.valid)
      return 0;
   if(state.direction == DAL_E0009_123_HIGHER_HIGHS)
      return -1;
   if(state.direction == DAL_E0009_123_LOWER_LOWS)
      return +1;
   return 0;
}

string DAL_E0009ExitModeName(const ENUM_DAL_E0009_EXIT_MODE m)
{
   if(m == DAL_E0009_EXIT_FIXED_R) return "FIXED_R";
   if(m == DAL_E0009_EXIT_TF_MONOTONIC_PATTERN) return "EXIT_TF_MONOTONIC_PATTERN";
   if(m == DAL_E0009_EXIT_NO_TP) return "NO_TP";
   return "UNKNOWN";
}

string DAL_E0009OrderModeName(const ENUM_DAL_E0009_ORDER_MODE m)
{
   if(m == DAL_E0009_ORDER_LIMIT_REVISIT) return "LIMIT_REVISIT";
   if(m == DAL_E0009_ORDER_STOP_RECLAIM) return "STOP_RECLAIM";
   if(m == DAL_E0009_ORDER_MARKET_ON_CONFIRM) return "MARKET_ON_CONFIRM";
   if(m == DAL_E0009_ORDER_AUTO) return "AUTO";
   return "UNKNOWN";
}

string DAL_E0009OrderKindName(const ENUM_DAL_E0009_SIGNAL_ORDER_KIND k)
{
   if(k == DAL_E0009_KIND_MARKET) return "MARKET";
   if(k == DAL_E0009_KIND_LIMIT) return "LIMIT";
   if(k == DAL_E0009_KIND_STOP) return "STOP";
   return "NONE";
}

#endif
