#ifndef __DAL_E0009_TYPES_MQH__
#define __DAL_E0009_TYPES_MQH__

#include <DecisionAlphaLab/Common/DAL_Common.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>

enum ENUM_DAL_E0009_HTF_123_DIRECTION
{
   DAL_E0009_123_NONE = 0,
   DAL_E0009_123_HIGHER_HIGHS = 1, // last 3 HTF HIGH nodes are higher than each other; counter entry = SELL on M1 HIGH hooks
   DAL_E0009_123_LOWER_LOWS = -1   // last 3 HTF LOW nodes are lower than each other; counter entry = BUY on M1 LOW hooks
};

// Backward-compatible aliases for old release-100 names.
#define DAL_E0009_123_BULLISH DAL_E0009_123_HIGHER_HIGHS
#define DAL_E0009_123_BEARISH DAL_E0009_123_LOWER_LOWS

enum ENUM_DAL_E0009_COUNTER_MODE
{
   DAL_E0009_COUNTER_OPPOSITE_123 = 0, // default: trade against the 1->3 HTF 123 direction
   DAL_E0009_COUNTER_BOTH_FOR_TEST = 1
};

enum ENUM_DAL_E0009_EXIT_MODE
{
   DAL_E0009_EXIT_FIXED_R = 0,
   DAL_E0009_EXIT_HTF_POINT_2 = 1,
   DAL_E0009_EXIT_NO_TP = 2
};

struct DALE0009HTF123State
{
   bool valid;
   string reason;

   ENUM_TIMEFRAMES tf;
   ENUM_DAL_E0009_HTF_123_DIRECTION direction;

   DALLRuleNode p1;
   DALLRuleNode p2;
   DALLRuleNode p3;

   datetime closed_time;
   int age_bars;
   double amplitude;
};

struct DALE0009HookSignal
{
   bool valid;
   string reason;

   int direction;                 // +1 buy, -1 sell
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
   int htf_L;
   int m1_L;
   double zone_ratio;
   int htf_max_age_bars;
   int m1_max_hook_age_bars;
   double fixed_r;
   bool require_fresh_m1_hook_after_htf_close;
   bool one_order_per_hook;
   double buy_entry_spread_mult;
   double sell_stop_spread_mult;
   ENUM_DAL_E0009_COUNTER_MODE counter_mode;
   ENUM_DAL_E0009_EXIT_MODE exit_mode;
};

void DAL_E0009_Reset123(DALE0009HTF123State &s)
{
   s.valid = false;
   s.reason = "not_built";
   s.tf = PERIOD_CURRENT;
   s.direction = DAL_E0009_123_NONE;

   s.p1.id = -1;
   s.p2.id = -1;
   s.p3.id = -1;
   s.p1.index = -1;
   s.p2.index = -1;
   s.p3.index = -1;
   s.p1.active_from_index = -1;
   s.p2.active_from_index = -1;
   s.p3.active_from_index = -1;
   s.p1.time = 0;
   s.p2.time = 0;
   s.p3.time = 0;
   s.p1.active_from_time = 0;
   s.p2.active_from_time = 0;
   s.p3.active_from_time = 0;
   s.p1.type = DAL_NODE_HIGH;
   s.p2.type = DAL_NODE_HIGH;
   s.p3.type = DAL_NODE_HIGH;
   s.p1.price = 0.0;
   s.p2.price = 0.0;
   s.p3.price = 0.0;
   s.p1.confirmed = false;
   s.p2.confirmed = false;
   s.p3.confirmed = false;

   s.closed_time = 0;
   s.age_bars = 0;
   s.amplitude = 0.0;
}

void DAL_E0009_ResetHook(DALE0009HookSignal &h)
{
   h.valid = false;
   h.reason = "not_built";
   h.direction = 0;
   h.hook_node.id = -1;
   h.hook_node.index = -1;
   h.hook_node.active_from_index = -1;
   h.hook_node.time = 0;
   h.hook_node.active_from_time = 0;
   h.hook_node.type = DAL_NODE_LOW;
   h.hook_node.price = 0.0;
   h.hook_node.confirmed = false;

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
   if(d == DAL_E0009_123_HIGHER_HIGHS) return "THREE_HIGHER_HIGHS_COUNTER_SELL";
   if(d == DAL_E0009_123_LOWER_LOWS) return "THREE_LOWER_LOWS_COUNTER_BUY";
   return "NONE";
}

string DAL_E0009ExitModeName(const ENUM_DAL_E0009_EXIT_MODE m)
{
   if(m == DAL_E0009_EXIT_FIXED_R) return "FIXED_R";
   if(m == DAL_E0009_EXIT_HTF_POINT_2) return "HTF_POINT_2";
   if(m == DAL_E0009_EXIT_NO_TP) return "NO_TP";
   return "UNKNOWN";
}

#endif
