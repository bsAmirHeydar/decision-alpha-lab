#ifndef __DAL_E0007_TYPES_MQH__
#define __DAL_E0007_TYPES_MQH__

#include <Common/DAL_Common.mqh>
#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/LRule/DAL_LRuleTypes.mqh>
#include <M0001/DAL_M0001Types.mqh>

// E0007 is a template executor for the "purple source -> local extreme -> rally"
// family. It is deliberately modular because the research language is still
// evolving. The default L is 2 because the purple-zone examples were generated
// with L=2.

enum ENUM_DAL_E0007_ENTRY_MODE
{
   DAL_E0007_ENTRY_FIRST_TOUCH_CONTEXT = 0,       // research mode: entry on the original source zone after first non-death touch is known
   DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT = 1,     // preferred: first touch proves source, next revisit is traded
   DAL_E0007_ENTRY_SECONDARY_NODE_ZONE = 2,       // revisit entry anchored to same-side node created during the first touch/base
   DAL_E0007_ENTRY_EARLY_LADDER_STEP = 3,         // continuation step after source has launched
   DAL_E0007_ENTRY_ALL_MODES = 10
};

enum ENUM_DAL_E0007_STOP_MODE
{
   DAL_E0007_STOP_ORIGIN_ZONE_BACK = 0,
   DAL_E0007_STOP_ORIGIN_NODE = 1,
   DAL_E0007_STOP_SECONDARY_NODE = 2,
   DAL_E0007_STOP_MICRO_EXTREME = 3
};

enum ENUM_DAL_E0007_TARGET_MODE
{
   DAL_E0007_TARGET_NONE = 0,
   DAL_E0007_TARGET_FIXED_R = 1,
   DAL_E0007_TARGET_NTH_OPPOSITE_INTERNAL_NODE = 2
};

enum ENUM_DAL_E0007_ROLE
{
   DAL_E0007_ROLE_UNKNOWN = 0,
   DAL_E0007_ROLE_SOURCE = 1,
   DAL_E0007_ROLE_SOURCE_REVISIT = 2,
   DAL_E0007_ROLE_EARLY_LADDER_STEP = 3,
   DAL_E0007_ROLE_REJECTED = 9
};

struct DALE0007SourcePolicy
{
   int L;
   double zone_ratio;
   int exit_gap;
   int max_events;

   // These two values are the first anti-overfit gates.
   // survival_bars=0 means live/no-future mode. survival_bars=500 turns the
   // template into an oracle research mode for "purple class" backtest probing.
   int min_source_survival_bars;
   double min_first_reaction_r;

   // Source/revisit shape gates.
   bool require_first_touch_not_hunted;
   bool require_second_revisit_for_entry;
   bool allow_first_touch_research_entry;
   int max_touch_age_bars;

   // Destination/asymmetry gate.
   bool use_destination_r_filter;
   int destination_lookback_bars;
   double min_potential_r;

   // Optional HTF bias is intentionally a coarse gate here. The atlas/reporter
   // should later replace this with a full HookContext state.
   bool use_htf_bias_filter;
   ENUM_TIMEFRAMES htf_timeframe;
   int htf_L;
   int htf_lookback_bars;
};

struct DALE0007PricingPolicy
{
   ENUM_DAL_E0007_ENTRY_MODE entry_mode;
   ENUM_DAL_E0007_STOP_MODE stop_mode;
   ENUM_DAL_E0007_TARGET_MODE target_mode;

   double buy_entry_spread_mult;
   double sell_stop_spread_mult;
   double fixed_reward_r;
   int opposite_node_tp_count;
};

struct DALE0007ExposurePolicy
{
   int max_buy_pending;
   int max_sell_pending;
   int max_buy_positions;
   int max_sell_positions;
};

struct DALE0007Candidate
{
   bool valid;
   string reason;

   ENUM_DAL_E0007_ROLE role;
   ENUM_DAL_E0007_ENTRY_MODE entry_mode;

   int direction;                         // +1 buy from LOW source, -1 sell from HIGH source
   int source_event_id;
   int source_revisit_id;
   int origin_node_id;
   ENUM_DALNodeType origin_type;

   datetime origin_time;
   datetime source_touch_time;
   datetime source_confirm_time;
   int source_entry_index;
   int source_exit_index;

   double origin_node_price;
   double origin_zone_lower;
   double origin_zone_upper;
   double zone_height;

   bool has_secondary_node;
   DALLRuleNode secondary_node;
   double secondary_zone_lower;
   double secondary_zone_upper;

   double first_reaction_r;
   int survival_bars;
   bool first_touch_hunted;
   bool second_revisit_exists;

   double entry;
   double sl;
   double tp;
   double risk_distance;

   double destination_price;
   double potential_r;
   string comment;
};

void DAL_E0007_DefaultSourcePolicy(DALE0007SourcePolicy &p)
{
   p.L = 2;
   p.zone_ratio = 0.90;
   p.exit_gap = 6;
   p.max_events = 2000;

   p.min_source_survival_bars = 0;
   p.min_first_reaction_r = 2.0;

   p.require_first_touch_not_hunted = true;
   p.require_second_revisit_for_entry = true;
   p.allow_first_touch_research_entry = false;
   p.max_touch_age_bars = 2500;

   p.use_destination_r_filter = true;
   p.destination_lookback_bars = 1500;
   p.min_potential_r = 40.0;

   p.use_htf_bias_filter = false;
   p.htf_timeframe = PERIOD_H1;
   p.htf_L = 2;
   p.htf_lookback_bars = 1500;
}

void DAL_E0007_DefaultPricingPolicy(DALE0007PricingPolicy &p)
{
   p.entry_mode = DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT;
   p.stop_mode = DAL_E0007_STOP_SECONDARY_NODE;
   p.target_mode = DAL_E0007_TARGET_NTH_OPPOSITE_INTERNAL_NODE;

   p.buy_entry_spread_mult = 1.0;
   p.sell_stop_spread_mult = 1.0;
   p.fixed_reward_r = 0.0;
   p.opposite_node_tp_count = 3;
}

void DAL_E0007_DefaultExposurePolicy(DALE0007ExposurePolicy &p)
{
   p.max_buy_pending = 1;
   p.max_sell_pending = 1;
   p.max_buy_positions = 1;
   p.max_sell_positions = 1;
}

void DAL_E0007_ResetCandidate(DALE0007Candidate &c)
{
   c.valid = false;
   c.reason = "not_built";
   c.role = DAL_E0007_ROLE_UNKNOWN;
   c.entry_mode = DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT;

   c.direction = 0;
   c.source_event_id = -1;
   c.source_revisit_id = -1;
   c.origin_node_id = -1;
   c.origin_type = DAL_NODE_LOW;

   c.origin_time = 0;
   c.source_touch_time = 0;
   c.source_confirm_time = 0;
   c.source_entry_index = -1;
   c.source_exit_index = -1;

   c.origin_node_price = 0.0;
   c.origin_zone_lower = 0.0;
   c.origin_zone_upper = 0.0;
   c.zone_height = 0.0;

   c.has_secondary_node = false;
   c.secondary_node.id = -1;
   c.secondary_node.index = -1;
   c.secondary_node.active_from_index = -1;
   c.secondary_node.time = 0;
   c.secondary_node.active_from_time = 0;
   c.secondary_node.type = DAL_NODE_LOW;
   c.secondary_node.price = 0.0;
   c.secondary_node.confirmed = false;
   c.secondary_zone_lower = 0.0;
   c.secondary_zone_upper = 0.0;

   c.first_reaction_r = 0.0;
   c.survival_bars = 0;
   c.first_touch_hunted = false;
   c.second_revisit_exists = false;

   c.entry = 0.0;
   c.sl = 0.0;
   c.tp = 0.0;
   c.risk_distance = 0.0;

   c.destination_price = 0.0;
   c.potential_r = 0.0;
   c.comment = "";
}

string DAL_E0007EntryModeName(const ENUM_DAL_E0007_ENTRY_MODE mode)
{
   if(mode == DAL_E0007_ENTRY_FIRST_TOUCH_CONTEXT) return "FIRST_TOUCH_CONTEXT";
   if(mode == DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT) return "SOURCE_SECOND_REVISIT";
   if(mode == DAL_E0007_ENTRY_SECONDARY_NODE_ZONE) return "SECONDARY_NODE_ZONE";
   if(mode == DAL_E0007_ENTRY_EARLY_LADDER_STEP) return "EARLY_LADDER_STEP";
   if(mode == DAL_E0007_ENTRY_ALL_MODES) return "ALL_MODES";
   return "UNKNOWN";
}

string DAL_E0007StopModeName(const ENUM_DAL_E0007_STOP_MODE mode)
{
   if(mode == DAL_E0007_STOP_ORIGIN_ZONE_BACK) return "ORIGIN_ZONE_BACK";
   if(mode == DAL_E0007_STOP_ORIGIN_NODE) return "ORIGIN_NODE";
   if(mode == DAL_E0007_STOP_SECONDARY_NODE) return "SECONDARY_NODE";
   if(mode == DAL_E0007_STOP_MICRO_EXTREME) return "MICRO_EXTREME";
   return "UNKNOWN";
}

string DAL_E0007RoleName(const ENUM_DAL_E0007_ROLE role)
{
   if(role == DAL_E0007_ROLE_SOURCE) return "SOURCE";
   if(role == DAL_E0007_ROLE_SOURCE_REVISIT) return "SOURCE_REVISIT";
   if(role == DAL_E0007_ROLE_EARLY_LADDER_STEP) return "EARLY_LADDER_STEP";
   if(role == DAL_E0007_ROLE_REJECTED) return "REJECTED";
   return "UNKNOWN";
}

#endif
