#ifndef __FC6_TYPES_MQH__
#define __FC6_TYPES_MQH__
#property strict

// ============================================================================
// FlagCounting V6 - Canonical data model
// ----------------------------------------------------------------------------
// This module is deliberately self-contained. It does not reuse the old VNext
// scanner because the V6 contract is sequence/state based, not sliding-window
// based.  The names are prefixed with FC6_ to avoid collision with older modules.
// ============================================================================

#define FC6_MAX_INTERNAL_NODES 4
#define FC6_MAX_REASON_LEN     160

enum FC6_NodeKind
{
   FC6_NODE_NONE = 0,
   FC6_NODE_HIGH = 1,
   FC6_NODE_LOW  = -1
};

enum FC6_Direction
{
   FC6_DIR_NONE    = 0,
   FC6_DIR_BULLISH = 1,
   FC6_DIR_BEARISH = -1
};

enum FC6_Level
{
   FC6_LEVEL_NONE = 0,
   FC6_LEVEL_ND   = 10,
   FC6_LEVEL_F1   = 1,
   FC6_LEVEL_F2   = 2,
   FC6_LEVEL_F3   = 3
};

enum FC6_Status
{
   FC6_STATUS_RAW_SEED        = 0,
   FC6_STATUS_LIVE_BODY       = 1,
   FC6_STATUS_POST_FLAG       = 2,
   FC6_STATUS_QUALIFIED       = 3,
   FC6_STATUS_CONFIRMED       = 4,
   FC6_STATUS_COMPLETED       = 5,
   FC6_STATUS_LOCKED          = 6,
   FC6_STATUS_INVALIDATED     = 7
};

enum FC6_BranchMode
{
   FC6_BRANCH_NONE            = 0,
   FC6_BRANCH_NORMAL_INTERNAL = 1,
   FC6_BRANCH_WAIST_BREAK     = 2,
   FC6_BRANCH_ND_HOOK         = 3,
   FC6_BRANCH_EXTENSION       = 4
};

enum FC6_DrawKind
{
   FC6_DRAW_FLAG_BODY         = 1,
   FC6_DRAW_PROBABLE_LEG      = 2,
   FC6_DRAW_HOOK_ARC          = 3,
   FC6_DRAW_LABEL_ONLY        = 4
};

struct FC6_Node
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

struct FC6_InternalPack
{
   int       count;
   FC6_Node  n1;
   FC6_Node  n2;
   FC6_Node  n3;
   FC6_Node  n4;
   FC6_Node  mid12;
   FC6_Node  mid23;
   FC6_Node  mid34;
   bool      has_mid12;
   bool      has_mid23;
   bool      has_mid34;
   bool      is_nd;
   double    nd_retrace_ratio;
};

struct FC6_FlagEvent
{
   int       event_id;
   int       sequence_id;
   int       parent_event_id;
   int       chain_index;
   int       scale_L;
   int       direction;
   int       level;
   int       status;
   int       branch_mode;
   int       draw_kind;

   FC6_Node  origin;
   FC6_Node  leg1;
   FC6_Node  waist;
   FC6_Node  leg2;
   FC6_Node  confirm;
   FC6_Node  invalid;
   FC6_Node  extension_end;

   FC6_InternalPack internal_pack;

   bool      has_origin;
   bool      has_leg1;
   bool      has_waist;
   bool      has_leg2;
   bool      has_confirm;
   bool      has_invalid;
   bool      has_extension;

   double    flag_size;
   double    parent_flag_size;
   double    size_ratio;
   int       leg1_L;
   int       parent_leg1_L;

   string    reason;
};

struct FC6_HookBranch
{
   int       branch_id;
   int       sequence_id;
   int       scale_L;
   int       direction;
   int       status;
   int       node_count;
   FC6_Node  start_node;
   FC6_Node  extreme_node;
   FC6_Node  resolve_node;
   FC6_Node  n1;
   FC6_Node  n2;
   FC6_Node  n3;
   FC6_Node  n4;
   double    retrace_ratio;
   bool      is_nd;
   string    reason;
};

struct FC6_Config
{
   bool   include_pending_nodes;
   bool   scan_f1;
   bool   scan_f2;
   bool   scan_f3;
   bool   scan_hooks;
   bool   show_invalidated_in_audit;
   bool   keep_confirmed_f1_f2_after_boundary_hit;
   bool   require_f1_phase_boundary;

   int    min_L;
   int    max_L;
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

struct FC6_DetectResult
{
   int nodes_total;
   int hooks_total;
   int events_total;
   int f1_total;
   int f2_total;
   int f3_total;
   int nd_total;
};

void FC6_ResetNode(FC6_Node &n)
{
   n.id = -1;
   n.L = 0;
   n.kind = FC6_NODE_NONE;
   n.index_start = -1;
   n.index_end = -1;
   n.index_anchor = -1;
   n.time_start = 0;
   n.time_end = 0;
   n.time_anchor = 0;
   n.price = 0.0;
   n.confirmed = false;
}

FC6_Node FC6_MakeNode(const int id,
                      const int L,
                      const int kind,
                      const int i0,
                      const int i1,
                      const int ia,
                      const datetime t0,
                      const datetime t1,
                      const datetime ta,
                      const double price,
                      const bool confirmed)
{
   FC6_Node n;
   n.id = id;
   n.L = L;
   n.kind = kind;
   n.index_start = i0;
   n.index_end = i1;
   n.index_anchor = ia;
   n.time_start = t0;
   n.time_end = t1;
   n.time_anchor = ta;
   n.price = price;
   n.confirmed = confirmed;
   return n;
}

bool FC6_NodeValid(const FC6_Node &n)
{
   return (n.kind != FC6_NODE_NONE && n.index_anchor >= 0 && n.time_anchor > 0);
}

void FC6_ResetInternalPack(FC6_InternalPack &p)
{
   p.count = 0;
   FC6_ResetNode(p.n1);
   FC6_ResetNode(p.n2);
   FC6_ResetNode(p.n3);
   FC6_ResetNode(p.n4);
   FC6_ResetNode(p.mid12);
   FC6_ResetNode(p.mid23);
   FC6_ResetNode(p.mid34);
   p.has_mid12 = false;
   p.has_mid23 = false;
   p.has_mid34 = false;
   p.is_nd = false;
   p.nd_retrace_ratio = 0.0;
}

void FC6_ResetFlagEvent(FC6_FlagEvent &e)
{
   e.event_id = -1;
   e.sequence_id = -1;
   e.parent_event_id = -1;
   e.chain_index = 0;
   e.scale_L = 0;
   e.direction = FC6_DIR_NONE;
   e.level = FC6_LEVEL_NONE;
   e.status = FC6_STATUS_RAW_SEED;
   e.branch_mode = FC6_BRANCH_NONE;
   e.draw_kind = FC6_DRAW_FLAG_BODY;

   FC6_ResetNode(e.origin);
   FC6_ResetNode(e.leg1);
   FC6_ResetNode(e.waist);
   FC6_ResetNode(e.leg2);
   FC6_ResetNode(e.confirm);
   FC6_ResetNode(e.invalid);
   FC6_ResetNode(e.extension_end);
   FC6_ResetInternalPack(e.internal_pack);

   e.has_origin = false;
   e.has_leg1 = false;
   e.has_waist = false;
   e.has_leg2 = false;
   e.has_confirm = false;
   e.has_invalid = false;
   e.has_extension = false;

   e.flag_size = 0.0;
   e.parent_flag_size = 0.0;
   e.size_ratio = 0.0;
   e.leg1_L = 0;
   e.parent_leg1_L = 0;
   e.reason = "";
}

void FC6_ResetHookBranch(FC6_HookBranch &h)
{
   h.branch_id = -1;
   h.sequence_id = -1;
   h.scale_L = 0;
   h.direction = FC6_DIR_NONE;
   h.status = FC6_STATUS_LIVE_BODY;
   h.node_count = 0;
   FC6_ResetNode(h.start_node);
   FC6_ResetNode(h.extreme_node);
   FC6_ResetNode(h.resolve_node);
   FC6_ResetNode(h.n1);
   FC6_ResetNode(h.n2);
   FC6_ResetNode(h.n3);
   FC6_ResetNode(h.n4);
   h.retrace_ratio = 0.0;
   h.is_nd = false;
   h.reason = "";
}

string FC6_NodeKindToString(const int kind)
{
   if(kind == FC6_NODE_HIGH) return "HIGH";
   if(kind == FC6_NODE_LOW) return "LOW";
   return "NONE";
}

string FC6_DirectionToString(const int d)
{
   if(d == FC6_DIR_BULLISH) return "bullish";
   if(d == FC6_DIR_BEARISH) return "bearish";
   return "none";
}

string FC6_LevelToString(const int level)
{
   if(level == FC6_LEVEL_F1) return "F1";
   if(level == FC6_LEVEL_F2) return "F2";
   if(level == FC6_LEVEL_F3) return "F3";
   if(level == FC6_LEVEL_ND) return "ND";
   return "F?";
}

string FC6_StatusToString(const int status)
{
   if(status == FC6_STATUS_RAW_SEED) return "raw_seed";
   if(status == FC6_STATUS_LIVE_BODY) return "live_body";
   if(status == FC6_STATUS_POST_FLAG) return "post_flag";
   if(status == FC6_STATUS_QUALIFIED) return "qualified";
   if(status == FC6_STATUS_CONFIRMED) return "confirmed";
   if(status == FC6_STATUS_COMPLETED) return "completed";
   if(status == FC6_STATUS_LOCKED) return "locked";
   if(status == FC6_STATUS_INVALIDATED) return "invalidated";
   return "unknown";
}

string FC6_BranchModeToString(const int mode)
{
   if(mode == FC6_BRANCH_NORMAL_INTERNAL) return "normal_internal";
   if(mode == FC6_BRANCH_WAIST_BREAK) return "waist_break";
   if(mode == FC6_BRANCH_ND_HOOK) return "nd_hook";
   if(mode == FC6_BRANCH_EXTENSION) return "extension";
   return "none";
}

bool FC6_IsBullish(const int d) { return d == FC6_DIR_BULLISH; }
bool FC6_IsBearish(const int d) { return d == FC6_DIR_BEARISH; }

int FC6_AdverseNodeKind(const int direction)
{
   if(direction == FC6_DIR_BULLISH) return FC6_NODE_LOW;
   if(direction == FC6_DIR_BEARISH) return FC6_NODE_HIGH;
   return FC6_NODE_NONE;
}

int FC6_FavorableNodeKind(const int direction)
{
   if(direction == FC6_DIR_BULLISH) return FC6_NODE_HIGH;
   if(direction == FC6_DIR_BEARISH) return FC6_NODE_LOW;
   return FC6_NODE_NONE;
}

bool FC6_StrictBreaksAbove(const double price, const double level, const double eps)
{
   return price > level + eps;
}

bool FC6_StrictBreaksBelow(const double price, const double level, const double eps)
{
   return price < level - eps;
}

bool FC6_BreaksBoundary(const FC6_Node &n, const double boundary, const int direction_to_break, const double eps)
{
   if(direction_to_break == FC6_DIR_BULLISH) return FC6_StrictBreaksAbove(n.price, boundary, eps);
   if(direction_to_break == FC6_DIR_BEARISH) return FC6_StrictBreaksBelow(n.price, boundary, eps);
   return false;
}

double FC6_FlagSize(const FC6_Node &origin, const FC6_Node &leg2)
{
   if(!FC6_NodeValid(origin) || !FC6_NodeValid(leg2)) return 0.0;
   return MathAbs(leg2.price - origin.price);
}

bool FC6_PriceEqual(const double a, const double b, const double eps)
{
   return MathAbs(a - b) <= eps;
}

bool FC6_SameNodeIdentity(const FC6_Node &a, const FC6_Node &b, const double eps)
{
   if(a.kind != b.kind) return false;
   if(a.time_start != b.time_start) return false;
   if(a.time_end != b.time_end) return false;
   if(a.time_anchor != b.time_anchor) return false;
   return FC6_PriceEqual(a.price, b.price, eps);
}

bool FC6_SameBodyIdentity(const FC6_FlagEvent &a, const FC6_FlagEvent &b, const double eps)
{
   return a.level == b.level &&
          a.direction == b.direction &&
          FC6_SameNodeIdentity(a.origin, b.origin, eps) &&
          FC6_SameNodeIdentity(a.leg1, b.leg1, eps) &&
          FC6_SameNodeIdentity(a.waist, b.waist, eps) &&
          FC6_SameNodeIdentity(a.leg2, b.leg2, eps);
}

void FC6_DefaultConfig(FC6_Config &cfg)
{
   cfg.include_pending_nodes = false;
   cfg.scan_f1 = true;
   cfg.scan_f2 = true;
   cfg.scan_f3 = true;
   cfg.scan_hooks = true;
   cfg.show_invalidated_in_audit = true;
   cfg.keep_confirmed_f1_f2_after_boundary_hit = false;
   cfg.require_f1_phase_boundary = true;
   cfg.min_L = 2;
   cfg.max_L = 21;
   cfg.max_events = 3000;
   cfg.max_hooks = 3000;
   cfg.max_roots_per_scale_direction = 0;
   cfg.render_lookback_bars = 2500;
   cfg.boundary_epsilon_points = 0.0;
   cfg.f2_min_parent_size_ratio = 1.0;
   cfg.f3_min_parent_size_ratio = 0.70;
   cfg.f3_leg1_L_min_ratio = 0.80;
   cfg.nd_min_retrace_ratio = 0.50;
   cfg.nd_allow_below_half_cycle = false;
   cfg.verbose_logs = false;
}

#endif // __FC6_TYPES_MQH__
