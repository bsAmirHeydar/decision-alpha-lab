#ifndef __DAL_E0006_TYPES_MQH__
#define __DAL_E0006_TYPES_MQH__

#include <DecisionAlphaLab/Common/DAL_Common.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>

// E0006 modular contracts. These structs are deliberately input-free so any EA,
// validation script, or future research executor can reuse the same atomic logic.

enum ENUM_DAL_E0006_STOP_ANCHOR
{
   DAL_E0006_STOP_ZONE_BACK = 0,
   DAL_E0006_STOP_NODE_PRICE = 1
};

enum ENUM_DAL_E0006_ENTRY_PHASE
{
   DAL_E0006_ENTRY_ANY_VALID_ZONE = 0,
   DAL_E0006_ENTRY_REVISIT_ONLY = 1
};

struct DALE0006PricingPolicy
{
   double reward_r;                         // 0 = no initial fixed-R TP
   double buy_entry_spread_mult;            // BUY entry = LOW zone upper + spread * mult
   double sell_stop_spread_mult;            // SELL stop = stop anchor + spread * mult
   double sell_tp_spread_mult;              // used only when reward_r > 0
   ENUM_DAL_E0006_STOP_ANCHOR stop_anchor;
};

struct DALE0006InternalHuntPolicy
{
   bool enabled;
   int required_hunts;
   bool same_side_only;
};

struct DALE0006RevisitPolicy
{
   ENUM_DAL_E0006_ENTRY_PHASE entry_phase;
   bool first_cycle_must_qualify;
   int revisit_required_hunts;              // 0 = inherit internal hunt policy requirement
};

struct DALE0006ExitPolicy
{
   bool use_internal_opposite_node_tp;
   int opposite_node_count;                 // BUY counts HIGH nodes; SELL counts LOW nodes
   bool modify_position_tp_on_new_bar;
};

struct DALE0006ExposurePolicy
{
   int max_buy_pending;                     // 0 = unlimited
   int max_sell_pending;                    // 0 = unlimited
   int max_buy_open_before_block;           // 0 = disabled
   int max_sell_open_before_block;          // 0 = disabled
   bool delete_side_pending_when_open_cap_hit;
};

struct DALE0006ZoneOrderPlan
{
   bool valid;
   string reason;

   int node_id;
   int node_index;
   ENUM_DALNodeType node_type;
   int direction;                           // +1 buy, -1 sell
   datetime node_time;
   datetime active_from_time;

   double node_price;
   double live_extreme;
   double zone_lower;
   double zone_upper;
   double spread;

   double entry;
   double sl;
   double tp;
   double reward_r;
   double risk_distance;

   int internal_hunt_count;
   int internal_hunt_required;
   bool internal_hunt_passed;

   bool revisit_required;
   bool revisit_passed;
   int first_cycle_hunts;
   int revisit_cycle_hunts;
   int first_touch_event_id;
   int revisit_event_id;

   string comment;
};

void DAL_E0006_DefaultPricingPolicy(DALE0006PricingPolicy &p)
{
   p.reward_r = 0.0;
   p.buy_entry_spread_mult = 1.0;
   p.sell_stop_spread_mult = 1.0;
   p.sell_tp_spread_mult = 1.0;
   p.stop_anchor = DAL_E0006_STOP_ZONE_BACK;
}

void DAL_E0006_DefaultInternalHuntPolicy(DALE0006InternalHuntPolicy &p)
{
   p.enabled = true;
   p.required_hunts = 3;
   p.same_side_only = true;
}

void DAL_E0006_DefaultRevisitPolicy(DALE0006RevisitPolicy &p)
{
   p.entry_phase = DAL_E0006_ENTRY_ANY_VALID_ZONE;
   p.first_cycle_must_qualify = true;
   p.revisit_required_hunts = 0;
}

void DAL_E0006_DefaultExitPolicy(DALE0006ExitPolicy &p)
{
   p.use_internal_opposite_node_tp = true;
   p.opposite_node_count = 3;
   p.modify_position_tp_on_new_bar = true;
}

void DAL_E0006_DefaultExposurePolicy(DALE0006ExposurePolicy &p)
{
   p.max_buy_pending = 0;
   p.max_sell_pending = 0;
   p.max_buy_open_before_block = 0;
   p.max_sell_open_before_block = 0;
   p.delete_side_pending_when_open_cap_hit = true;
}

void DAL_E0006_ResetZoneOrderPlan(DALE0006ZoneOrderPlan &s)
{
   s.valid = false;
   s.reason = "not_built";
   s.node_id = -1;
   s.node_index = -1;
   s.node_type = DAL_NODE_LOW;
   s.direction = 0;
   s.node_time = 0;
   s.active_from_time = 0;
   s.node_price = 0.0;
   s.live_extreme = 0.0;
   s.zone_lower = 0.0;
   s.zone_upper = 0.0;
   s.spread = 0.0;
   s.entry = 0.0;
   s.sl = 0.0;
   s.tp = 0.0;
   s.reward_r = 0.0;
   s.risk_distance = 0.0;
   s.internal_hunt_count = 0;
   s.internal_hunt_required = 0;
   s.internal_hunt_passed = false;
   s.revisit_required = false;
   s.revisit_passed = false;
   s.first_cycle_hunts = 0;
   s.revisit_cycle_hunts = 0;
   s.first_touch_event_id = -1;
   s.revisit_event_id = -1;
   s.comment = "";
}

string DAL_E0006_StopAnchorToString(const ENUM_DAL_E0006_STOP_ANCHOR anchor)
{
   if(anchor == DAL_E0006_STOP_NODE_PRICE)
      return "NODE_PRICE";
   return "ZONE_BACK";
}

string DAL_E0006_EntryPhaseToString(const ENUM_DAL_E0006_ENTRY_PHASE phase)
{
   if(phase == DAL_E0006_ENTRY_REVISIT_ONLY)
      return "REVISIT_ONLY";
   return "ANY_VALID_ZONE";
}

#endif
