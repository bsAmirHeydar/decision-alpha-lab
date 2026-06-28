#ifndef __FP_TYPES_MQH__
#define __FP_TYPES_MQH__
#property strict

// ============================================================================
// FlagCounting Phoenix - Types and canonical helpers
// ----------------------------------------------------------------------------
// Clean rebuild namespace: FP_*
// This package intentionally does not include or depend on FlagCounting,
// FlagCountingVNext, or FlagCountingV6 modules.
// ============================================================================

#define FP_MAX_INTERNAL_NODES 4
#define FP_REASON_LEN         192

// ----------------------------- Core enums ----------------------------------

enum FP_NodeKind
{
   FP_NODE_NONE = 0,
   FP_NODE_HIGH = 1,
   FP_NODE_LOW  = -1
};

enum FP_Direction
{
   FP_DIR_NONE    = 0,
   FP_DIR_BULLISH = 1,
   FP_DIR_BEARISH = -1
};

enum FP_Level
{
   FP_LEVEL_NONE = 0,
   FP_LEVEL_F1   = 1,
   FP_LEVEL_F2   = 2,
   FP_LEVEL_F3   = 3,
   FP_LEVEL_ND   = 10
};

enum FP_Status
{
   FP_STATUS_NONE        = 0,
   FP_STATUS_SEED        = 1,
   FP_STATUS_LIVE_LEG    = 2,
   FP_STATUS_LIVE_BODY   = 3,
   FP_STATUS_POST_FLAG   = 4,
   FP_STATUS_QUALIFIED   = 5,
   FP_STATUS_CONFIRMED   = 6,
   FP_STATUS_COMPLETED   = 7,
   FP_STATUS_LOCKED      = 8,
   FP_STATUS_INVALIDATED = 9
};

enum FP_BranchKind
{
   FP_BRANCH_NONE            = 0,
   FP_BRANCH_NORMAL_INTERNAL = 1,
   FP_BRANCH_WAIST_BREAK     = 2,
   FP_BRANCH_ND_HOOK         = 3,
   FP_BRANCH_EXTENSION       = 4
};

enum FP_RenderKind
{
   FP_RENDER_NONE       = 0,
   FP_RENDER_FLAG_BODY  = 1,
   FP_RENDER_PROBABLE   = 2,
   FP_RENDER_HOOK_ARC   = 3,
   FP_RENDER_LABEL_ONLY = 4
};

// ------------------------------- Data model --------------------------------

struct FP_Node
{
   int       id;
   int       L;
   int       kind;
   int       index_start;
   int       index_end;
   int       index_anchor;
   datetime  time_start;
   datetime  time_end;
   datetime  time_anchor;
   double    price;
   bool      confirmed;
};

struct FP_InternalPack
{
   int      count;
   FP_Node  n1;
   FP_Node  n2;
   FP_Node  n3;
   FP_Node  n4;
   FP_Node  mid12;
   FP_Node  mid23;
   FP_Node  mid34;
   bool     has_mid12;
   bool     has_mid23;
   bool     has_mid34;
   bool     valid12;
   bool     is_nd;
   double   retrace_ratio;
};

struct FP_HookBranch
{
   int      branch_id;
   int      scale_L;
   int      direction;
   int      status;
   int      node_count;
   // First counted same-side branch node. Kept as the semantic branch start
   // used by F1 phase boundary logic. Do not replace this with the cycle
   // boundary; otherwise downstream sequence ownership changes.
   FP_Node  start_node;

   // True visual/cycle boundary. The gray Hook/ND arc starts here. This is
   // the nearest older same-side node that is strictly beyond the resolve node
   // in the adverse direction; it must not be strictly broken before resolve.
   FP_Node  cycle_start_node;
   bool     has_cycle_start;

   FP_Node  extreme_node;
   FP_Node  resolve_node;
   FP_Node  n1;
   FP_Node  n2;
   FP_Node  n3;
   FP_Node  n4;
   double   retrace_ratio;
   bool     is_nd;
   string   reason;
};

struct FP_FlagEvent
{
   int      event_id;
   int      sequence_id;
   int      parent_event_id;
   int      parent_sequence_id;
   int      chain_index;
   int      scale_L;
   int      direction;
   int      level;
   int      status;
   int      branch_kind;
   int      render_kind;

   FP_Node  origin;
   FP_Node  leg1;
   FP_Node  waist;
   FP_Node  leg2;
   FP_Node  confirm;
   FP_Node  invalid;
   FP_Node  extension_end;

   FP_InternalPack internal_pack;

   bool     has_origin;
   bool     has_leg1;
   bool     has_waist;
   bool     has_leg2;
   bool     has_confirm;
   bool     has_invalid;
   bool     has_extension;

   int      pos_origin;
   int      pos_leg1;
   int      pos_waist;
   int      pos_leg2;
   int      pos_confirm;
   int      pos_invalid;
   int      pos_extension_end;

   double   flag_size;
   double   parent_flag_size;
   double   size_ratio;
   int      leg1_L;
   int      parent_leg1_L;

   bool     from_phase_boundary;
   bool     from_fail_open;
   bool     visible_main;
   string   reason;
};

struct FP_Config
{
   bool   include_pending_nodes;
   bool   scan_hooks;
   bool   scan_f1;
   bool   scan_f2;
   bool   scan_f3;
   bool   show_invalidated_in_audit;
   bool   keep_confirmed_f1f2_after_boundary_hit;

   bool   require_f1_phase_boundary;
   bool   allow_f1_fail_open_when_no_hook;
   bool   enforce_single_chain_per_direction_scale;
   bool   enforce_single_chain_per_direction_global;
   bool   absorb_pre_internal_extensions;
   bool   hide_superseded_parent_states;
   bool   compact_hook_rendering;

   int    max_events;
   int    max_hooks;
   int    max_roots_per_scale_direction;
   int    render_lookback_bars;

   double boundary_epsilon_points;
   double f2_min_parent_size_ratio;
   double f3_min_parent_size_ratio;
   double f3_leg1_L_min_ratio;
   double nd_min_retrace_ratio;
   bool   nd_allow_below_half_cycle;

   bool   verbose_logs;
};

struct FP_DetectResult
{
   int nodes_total;
   int hooks_total;
   int events_total;
   int visible_events_total;
   int f1_total;
   int f2_total;
   int f3_total;
   int nd_total;
   int invalid_total;
};

// ------------------------------ Reset helpers ------------------------------

void FP_ResetNode(FP_Node &n)
{
   n.id = -1;
   n.L = 0;
   n.kind = FP_NODE_NONE;
   n.index_start = -1;
   n.index_end = -1;
   n.index_anchor = -1;
   n.time_start = 0;
   n.time_end = 0;
   n.time_anchor = 0;
   n.price = 0.0;
   n.confirmed = false;
}

void FP_ResetInternalPack(FP_InternalPack &p)
{
   p.count = 0;
   FP_ResetNode(p.n1);
   FP_ResetNode(p.n2);
   FP_ResetNode(p.n3);
   FP_ResetNode(p.n4);
   FP_ResetNode(p.mid12);
   FP_ResetNode(p.mid23);
   FP_ResetNode(p.mid34);
   p.has_mid12 = false;
   p.has_mid23 = false;
   p.has_mid34 = false;
   p.valid12 = false;
   p.is_nd = false;
   p.retrace_ratio = 0.0;
}

void FP_ResetHook(FP_HookBranch &h)
{
   h.branch_id = -1;
   h.scale_L = 0;
   h.direction = FP_DIR_NONE;
   h.status = FP_STATUS_NONE;
   h.node_count = 0;
   FP_ResetNode(h.start_node);
   FP_ResetNode(h.cycle_start_node);
   h.has_cycle_start = false;
   FP_ResetNode(h.extreme_node);
   FP_ResetNode(h.resolve_node);
   FP_ResetNode(h.n1);
   FP_ResetNode(h.n2);
   FP_ResetNode(h.n3);
   FP_ResetNode(h.n4);
   h.retrace_ratio = 0.0;
   h.is_nd = false;
   h.reason = "";
}

void FP_ResetFlagEvent(FP_FlagEvent &e)
{
   e.event_id = -1;
   e.sequence_id = -1;
   e.parent_event_id = -1;
   e.parent_sequence_id = -1;
   e.chain_index = 0;
   e.scale_L = 0;
   e.direction = FP_DIR_NONE;
   e.level = FP_LEVEL_NONE;
   e.status = FP_STATUS_NONE;
   e.branch_kind = FP_BRANCH_NONE;
   e.render_kind = FP_RENDER_NONE;

   FP_ResetNode(e.origin);
   FP_ResetNode(e.leg1);
   FP_ResetNode(e.waist);
   FP_ResetNode(e.leg2);
   FP_ResetNode(e.confirm);
   FP_ResetNode(e.invalid);
   FP_ResetNode(e.extension_end);
   FP_ResetInternalPack(e.internal_pack);

   e.has_origin = false;
   e.has_leg1 = false;
   e.has_waist = false;
   e.has_leg2 = false;
   e.has_confirm = false;
   e.has_invalid = false;
   e.has_extension = false;

   e.pos_origin = -1;
   e.pos_leg1 = -1;
   e.pos_waist = -1;
   e.pos_leg2 = -1;
   e.pos_confirm = -1;
   e.pos_invalid = -1;
   e.pos_extension_end = -1;

   e.flag_size = 0.0;
   e.parent_flag_size = 0.0;
   e.size_ratio = 0.0;
   e.leg1_L = 0;
   e.parent_leg1_L = 0;

   e.from_phase_boundary = false;
   e.from_fail_open = false;
   e.visible_main = true;
   e.reason = "";
}

void FP_DefaultConfig(FP_Config &cfg)
{
   cfg.include_pending_nodes = false;
   cfg.scan_hooks = true;
   cfg.scan_f1 = true;
   cfg.scan_f2 = true;
   cfg.scan_f3 = true;
   cfg.show_invalidated_in_audit = false;
   cfg.keep_confirmed_f1f2_after_boundary_hit = false;

   cfg.require_f1_phase_boundary = true;
   cfg.allow_f1_fail_open_when_no_hook = true;
   cfg.enforce_single_chain_per_direction_scale = false;
   cfg.enforce_single_chain_per_direction_global = false;
   cfg.absorb_pre_internal_extensions = true;
   cfg.hide_superseded_parent_states = true;
   cfg.compact_hook_rendering = true;

   cfg.max_events = 6000;
   cfg.max_hooks = 6000;
   cfg.max_roots_per_scale_direction = 0;
   cfg.render_lookback_bars = 0;

   cfg.boundary_epsilon_points = 0.0;
   cfg.f2_min_parent_size_ratio = 1.0;
   cfg.f3_min_parent_size_ratio = 0.70;
   cfg.f3_leg1_L_min_ratio = 0.80;
   cfg.nd_min_retrace_ratio = 0.50;
   cfg.nd_allow_below_half_cycle = false;

   cfg.verbose_logs = false;
}

void FP_ResetDetectResult(FP_DetectResult &r)
{
   r.nodes_total = 0;
   r.hooks_total = 0;
   r.events_total = 0;
   r.visible_events_total = 0;
   r.f1_total = 0;
   r.f2_total = 0;
   r.f3_total = 0;
   r.nd_total = 0;
   r.invalid_total = 0;
}

// ------------------------------ String helpers -----------------------------

string FP_NodeKindName(const int kind)
{
   if(kind == FP_NODE_HIGH) return "HIGH";
   if(kind == FP_NODE_LOW)  return "LOW";
   return "NONE";
}

string FP_DirectionName(const int direction)
{
   if(direction == FP_DIR_BULLISH) return "bull";
   if(direction == FP_DIR_BEARISH) return "bear";
   return "none";
}

string FP_LevelName(const int level)
{
   if(level == FP_LEVEL_F1) return "F1";
   if(level == FP_LEVEL_F2) return "F2";
   if(level == FP_LEVEL_F3) return "F3";
   if(level == FP_LEVEL_ND) return "ND";
   return "F?";
}

string FP_StatusName(const int status)
{
   if(status == FP_STATUS_SEED)        return "seed";
   if(status == FP_STATUS_LIVE_LEG)    return "live_leg";
   if(status == FP_STATUS_LIVE_BODY)   return "live_body";
   if(status == FP_STATUS_POST_FLAG)   return "post_flag";
   if(status == FP_STATUS_QUALIFIED)   return "qualified";
   if(status == FP_STATUS_CONFIRMED)   return "confirmed";
   if(status == FP_STATUS_COMPLETED)   return "completed";
   if(status == FP_STATUS_LOCKED)      return "locked";
   if(status == FP_STATUS_INVALIDATED) return "invalidated";
   return "none";
}

string FP_BoolName(const bool v)
{
   return (v ? "true" : "false");
}

// ------------------------------ Comparators --------------------------------

double FP_EpsilonPrice(const double points)
{
   return MathMax(0.0, points) * _Point;
}

bool FP_AlmostEqual(const double a, const double b, const double eps)
{
   return MathAbs(a - b) <= eps;
}

// In this contract equality never counts as break.  Price must cross strictly.
bool FP_BreaksAbove(const double price, const double boundary, const double eps)
{
   return (price > boundary + eps);
}

bool FP_BreaksBelow(const double price, const double boundary, const double eps)
{
   return (price < boundary - eps);
}

bool FP_NodeBreaksBoundary(const FP_Node &n, const int direction, const double boundary, const double eps)
{
   if(direction == FP_DIR_BULLISH)
      return (n.kind == FP_NODE_LOW && FP_BreaksBelow(n.price, boundary, eps));
   if(direction == FP_DIR_BEARISH)
      return (n.kind == FP_NODE_HIGH && FP_BreaksAbove(n.price, boundary, eps));
   return false;
}

bool FP_NodeBreaksFlagEnd(const FP_Node &n, const int direction, const double flag_end, const double eps)
{
   if(direction == FP_DIR_BULLISH)
      return (n.kind == FP_NODE_HIGH && FP_BreaksAbove(n.price, flag_end, eps));
   if(direction == FP_DIR_BEARISH)
      return (n.kind == FP_NODE_LOW && FP_BreaksBelow(n.price, flag_end, eps));
   return false;
}

int FP_OriginKindForDirection(const int direction)
{
   if(direction == FP_DIR_BULLISH) return FP_NODE_LOW;
   if(direction == FP_DIR_BEARISH) return FP_NODE_HIGH;
   return FP_NODE_NONE;
}

int FP_OppositeKind(const int kind)
{
   if(kind == FP_NODE_HIGH) return FP_NODE_LOW;
   if(kind == FP_NODE_LOW)  return FP_NODE_HIGH;
   return FP_NODE_NONE;
}

bool FP_IsMoreAdverse(const int direction, const double a, const double b, const double eps)
{
   // True if a is deeper/more adverse than b for the direction.
   if(direction == FP_DIR_BULLISH) return FP_BreaksBelow(a, b, eps);
   if(direction == FP_DIR_BEARISH) return FP_BreaksAbove(a, b, eps);
   return false;
}

bool FP_IsMoreFavorable(const int direction, const double a, const double b, const double eps)
{
   if(direction == FP_DIR_BULLISH) return FP_BreaksAbove(a, b, eps);
   if(direction == FP_DIR_BEARISH) return FP_BreaksBelow(a, b, eps);
   return false;
}

int FP_AddNode(FP_Node &arr[], const FP_Node &n)
{
   int sz = ArraySize(arr);
   ArrayResize(arr, sz + 1);
   arr[sz] = n;
   return sz;
}

int FP_AddHook(FP_HookBranch &arr[], const FP_HookBranch &h)
{
   int sz = ArraySize(arr);
   ArrayResize(arr, sz + 1);
   arr[sz] = h;
   return sz;
}

int FP_AddEvent(FP_FlagEvent &arr[], const FP_FlagEvent &e)
{
   int sz = ArraySize(arr);
   ArrayResize(arr, sz + 1);
   arr[sz] = e;
   return sz;
}

bool FP_SameNodeIdentity(const FP_Node &a, const FP_Node &b)
{
   return (a.id == b.id && a.L == b.L && a.kind == b.kind && a.index_anchor == b.index_anchor && a.price == b.price);
}

bool FP_SameBodyIdentity(const FP_FlagEvent &a, const FP_FlagEvent &b)
{
   if(a.level != b.level) return false;
   if(a.direction != b.direction) return false;
   if(!FP_SameNodeIdentity(a.origin, b.origin)) return false;
   if(!FP_SameNodeIdentity(a.leg1, b.leg1)) return false;
   if(!FP_SameNodeIdentity(a.waist, b.waist)) return false;
   if(!FP_SameNodeIdentity(a.leg2, b.leg2)) return false;
   return true;
}

#endif // __FP_TYPES_MQH__
