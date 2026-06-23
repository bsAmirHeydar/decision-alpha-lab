#ifndef __DAL_E0008_TYPES_MQH__
#define __DAL_E0008_TYPES_MQH__

#include <Common/DAL_Common.mqh>
#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/LRule/DAL_LRuleTypes.mqh>
#include <M0001/DAL_M0001Types.mqh>

enum ENUM_DAL_E0008_ENTRY_MODE
{
   DAL_E0008_ENTRY_MICRO_NODE_REVISIT = 0,      // tiny-stop entry on the latest same-side micro node
   DAL_E0008_ENTRY_LOCAL_SOURCE_REVISIT = 1,    // entry on local context source zone
   DAL_E0008_ENTRY_LOCAL_SECONDARY_NODE = 2,    // entry on same-side secondary node created during first source touch
   DAL_E0008_ENTRY_EARLY_LADDER_STEP = 3,       // early continuation step after source launch
   DAL_E0008_ENTRY_ALL_MODES = 10
};

enum ENUM_DAL_E0008_STOP_MODE
{
   DAL_E0008_STOP_MICRO_NODE = 0,
   DAL_E0008_STOP_LOCAL_SOURCE_ZONE_BACK = 1,
   DAL_E0008_STOP_LOCAL_SOURCE_NODE = 2,
   DAL_E0008_STOP_SECONDARY_NODE = 3
};

enum ENUM_DAL_E0008_TARGET_MODE
{
   DAL_E0008_TARGET_CONTEXT_DESTINATION = 0,     // TP = big-context destination
   DAL_E0008_TARGET_FIXED_R = 1,
   DAL_E0008_TARGET_NTH_OPPOSITE_NODE = 2,
   DAL_E0008_TARGET_NONE = 3
};

enum ENUM_DAL_E0008_CONTEXT_ROLE
{
   DAL_E0008_CONTEXT_NONE = 0,
   DAL_E0008_CONTEXT_SOURCE = 1,
   DAL_E0008_CONTEXT_SOURCE_REVISIT = 2,
   DAL_E0008_CONTEXT_EARLY_LADDER = 3,
   DAL_E0008_CONTEXT_DESTINATION = 4
};

struct DALE0008SourcePolicy
{
   int L;
   double zone_ratio;
   int exit_gap;
   int max_events;

   // Research/live switch:
   // 0 = no future survival requirement.
   // 500 = oracle purple-class probing.
   int min_source_survival_bars;

   double min_first_reaction_r;
   bool require_first_touch_not_hunted;
   bool allow_already_second_revisit_for_research;
   int max_source_age_bars;
};

struct DALE0008MTFPolicy
{
   int min_aligned_contexts;
   bool reject_if_any_context_conflicts;
   bool require_local_context;
   double min_context_score;
};

struct DALE0008ExecutionPolicy
{
   ENUM_DAL_E0008_ENTRY_MODE entry_mode;
   ENUM_DAL_E0008_STOP_MODE stop_mode;
   ENUM_DAL_E0008_TARGET_MODE target_mode;

   double min_potential_r;
   double fixed_reward_r;
   int opposite_node_tp_count;

   double buy_entry_spread_mult;
   double sell_stop_spread_mult;

   int micro_L;
   int max_micro_node_age_bars;
};

struct DALE0008ExposurePolicy
{
   int max_buy_pending;
   int max_sell_pending;
   int max_buy_positions;
   int max_sell_positions;
};

struct DALE0008ContextState
{
   bool valid;
   string reason;

   ENUM_TIMEFRAMES tf;
   int direction;                         // +1: bullish source from LOW, -1: bearish source from HIGH
   ENUM_DAL_E0008_CONTEXT_ROLE role;

   int node_id;
   int event_id;
   int revisit_id;
   ENUM_DALNodeType node_type;

   datetime node_time;
   datetime touch_time;
   datetime exit_time;
   int entry_index;
   int exit_index;

   double node_price;
   double zone_lower;
   double zone_upper;
   double zone_height;

   bool first_touch_hunted;
   bool has_second_revisit;
   double first_reaction_r;
   int survival_bars;
   int source_age_bars;

   double destination_price;
   double context_score;
};

struct DALE0008MicroTrigger
{
   bool valid;
   string reason;

   ENUM_DAL_E0008_ENTRY_MODE entry_mode;
   int direction;

   int node_id;
   ENUM_DALNodeType node_type;
   datetime node_time;

   double node_price;
   double zone_lower;
   double zone_upper;

   bool has_secondary_node;
   DALLRuleNode secondary_node;
   double secondary_zone_lower;
   double secondary_zone_upper;

   double entry;
   double sl;
   double risk_distance;
};

struct DALE0008TradePlan
{
   bool valid;
   string reason;

   int direction;
   ENUM_DAL_E0008_ENTRY_MODE entry_mode;
   ENUM_DAL_E0008_STOP_MODE stop_mode;
   ENUM_DAL_E0008_TARGET_MODE target_mode;

   ENUM_TIMEFRAMES context_tf;
   ENUM_TIMEFRAMES local_tf;

   int context_node_id;
   int local_node_id;
   int micro_node_id;

   double entry;
   double sl;
   double tp;
   double risk_distance;
   double destination_price;
   double potential_r;

   string comment;
};

void DAL_E0008_DefaultSourcePolicy(DALE0008SourcePolicy &p)
{
   p.L = 2;
   p.zone_ratio = 0.90;
   p.exit_gap = 6;
   p.max_events = 2000;

   p.min_source_survival_bars = 0;
   p.min_first_reaction_r = 2.0;
   p.require_first_touch_not_hunted = true;
   p.allow_already_second_revisit_for_research = false;
   p.max_source_age_bars = 2500;
}

void DAL_E0008_DefaultMTFPolicy(DALE0008MTFPolicy &p)
{
   p.min_aligned_contexts = 2;
   p.reject_if_any_context_conflicts = true;
   p.require_local_context = true;
   p.min_context_score = 0.0;
}

void DAL_E0008_DefaultExecutionPolicy(DALE0008ExecutionPolicy &p)
{
   p.entry_mode = DAL_E0008_ENTRY_MICRO_NODE_REVISIT;
   p.stop_mode = DAL_E0008_STOP_MICRO_NODE;
   p.target_mode = DAL_E0008_TARGET_CONTEXT_DESTINATION;

   p.min_potential_r = 50.0;
   p.fixed_reward_r = 100.0;
   p.opposite_node_tp_count = 3;

   p.buy_entry_spread_mult = 1.0;
   p.sell_stop_spread_mult = 1.0;

   p.micro_L = 2;
   p.max_micro_node_age_bars = 250;
}

void DAL_E0008_DefaultExposurePolicy(DALE0008ExposurePolicy &p)
{
   p.max_buy_pending = 1;
   p.max_sell_pending = 1;
   p.max_buy_positions = 1;
   p.max_sell_positions = 1;
}

void DAL_E0008_ResetContext(DALE0008ContextState &c)
{
   c.valid = false;
   c.reason = "not_built";
   c.tf = PERIOD_CURRENT;
   c.direction = 0;
   c.role = DAL_E0008_CONTEXT_NONE;

   c.node_id = -1;
   c.event_id = -1;
   c.revisit_id = -1;
   c.node_type = DAL_NODE_LOW;

   c.node_time = 0;
   c.touch_time = 0;
   c.exit_time = 0;
   c.entry_index = -1;
   c.exit_index = -1;

   c.node_price = 0.0;
   c.zone_lower = 0.0;
   c.zone_upper = 0.0;
   c.zone_height = 0.0;

   c.first_touch_hunted = false;
   c.has_second_revisit = false;
   c.first_reaction_r = 0.0;
   c.survival_bars = 0;
   c.source_age_bars = 0;

   c.destination_price = 0.0;
   c.context_score = 0.0;
}

void DAL_E0008_ResetMicroTrigger(DALE0008MicroTrigger &t)
{
   t.valid = false;
   t.reason = "not_built";
   t.entry_mode = DAL_E0008_ENTRY_MICRO_NODE_REVISIT;
   t.direction = 0;

   t.node_id = -1;
   t.node_type = DAL_NODE_LOW;
   t.node_time = 0;

   t.node_price = 0.0;
   t.zone_lower = 0.0;
   t.zone_upper = 0.0;

   t.has_secondary_node = false;
   t.secondary_node.id = -1;
   t.secondary_node.index = -1;
   t.secondary_node.active_from_index = -1;
   t.secondary_node.time = 0;
   t.secondary_node.active_from_time = 0;
   t.secondary_node.type = DAL_NODE_LOW;
   t.secondary_node.price = 0.0;
   t.secondary_node.confirmed = false;
   t.secondary_zone_lower = 0.0;
   t.secondary_zone_upper = 0.0;

   t.entry = 0.0;
   t.sl = 0.0;
   t.risk_distance = 0.0;
}

void DAL_E0008_ResetTradePlan(DALE0008TradePlan &p)
{
   p.valid = false;
   p.reason = "not_built";
   p.direction = 0;
   p.entry_mode = DAL_E0008_ENTRY_MICRO_NODE_REVISIT;
   p.stop_mode = DAL_E0008_STOP_MICRO_NODE;
   p.target_mode = DAL_E0008_TARGET_CONTEXT_DESTINATION;

   p.context_tf = PERIOD_CURRENT;
   p.local_tf = PERIOD_CURRENT;

   p.context_node_id = -1;
   p.local_node_id = -1;
   p.micro_node_id = -1;

   p.entry = 0.0;
   p.sl = 0.0;
   p.tp = 0.0;
   p.risk_distance = 0.0;
   p.destination_price = 0.0;
   p.potential_r = 0.0;

   p.comment = "";
}

string DAL_E0008EntryModeName(const ENUM_DAL_E0008_ENTRY_MODE m)
{
   if(m == DAL_E0008_ENTRY_MICRO_NODE_REVISIT) return "MICRO_NODE_REVISIT";
   if(m == DAL_E0008_ENTRY_LOCAL_SOURCE_REVISIT) return "LOCAL_SOURCE_REVISIT";
   if(m == DAL_E0008_ENTRY_LOCAL_SECONDARY_NODE) return "LOCAL_SECONDARY_NODE";
   if(m == DAL_E0008_ENTRY_EARLY_LADDER_STEP) return "EARLY_LADDER_STEP";
   if(m == DAL_E0008_ENTRY_ALL_MODES) return "ALL_MODES";
   return "UNKNOWN";
}

string DAL_E0008StopModeName(const ENUM_DAL_E0008_STOP_MODE m)
{
   if(m == DAL_E0008_STOP_MICRO_NODE) return "MICRO_NODE";
   if(m == DAL_E0008_STOP_LOCAL_SOURCE_ZONE_BACK) return "LOCAL_SOURCE_ZONE_BACK";
   if(m == DAL_E0008_STOP_LOCAL_SOURCE_NODE) return "LOCAL_SOURCE_NODE";
   if(m == DAL_E0008_STOP_SECONDARY_NODE) return "SECONDARY_NODE";
   return "UNKNOWN";
}

string DAL_E0008TargetModeName(const ENUM_DAL_E0008_TARGET_MODE m)
{
   if(m == DAL_E0008_TARGET_CONTEXT_DESTINATION) return "CONTEXT_DESTINATION";
   if(m == DAL_E0008_TARGET_FIXED_R) return "FIXED_R";
   if(m == DAL_E0008_TARGET_NTH_OPPOSITE_NODE) return "NTH_OPPOSITE_NODE";
   if(m == DAL_E0008_TARGET_NONE) return "NONE";
   return "UNKNOWN";
}

string DAL_E0008RoleName(const ENUM_DAL_E0008_CONTEXT_ROLE r)
{
   if(r == DAL_E0008_CONTEXT_SOURCE) return "SOURCE";
   if(r == DAL_E0008_CONTEXT_SOURCE_REVISIT) return "SOURCE_REVISIT";
   if(r == DAL_E0008_CONTEXT_EARLY_LADDER) return "EARLY_LADDER";
   if(r == DAL_E0008_CONTEXT_DESTINATION) return "DESTINATION";
   return "NONE";
}

#endif
