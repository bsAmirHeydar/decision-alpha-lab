#ifndef __FCN_TYPES_MQH__
#define __FCN_TYPES_MQH__
#property strict

enum FCN_Direction
{
   FCN_DIR_NONE    = 0,
   FCN_DIR_BULLISH = 1,
   FCN_DIR_BEARISH = -1
};

enum FCN_NodeKind
{
   FCN_NODE_NONE = 0,
   FCN_NODE_HIGH = 1,
   FCN_NODE_LOW  = -1
};

enum FCN_Level
{
   FCN_LEVEL_ND = 0,
   FCN_LEVEL_F1 = 1,
   FCN_LEVEL_F2 = 2,
   FCN_LEVEL_F3 = 3
};

enum FCN_Status
{
   FCN_STATUS_LIVE      = 0,
   FCN_STATUS_CONFIRMED = 1,
   FCN_STATUS_INVALID   = 2,
   FCN_STATUS_TERMINAL  = 3
};

enum FCN_BranchMode
{
   FCN_BRANCH_NONE        = 0,
   FCN_BRANCH_INTERNAL12  = 1,
   FCN_BRANCH_WAIST_BREAK = 2,
   FCN_BRANCH_PARTIAL_1   = 3
};

struct FCN_Node
{
   int index;
   datetime time;
   double price;
   int kind;
};

struct FCN_Event
{
   int event_id;
   int sequence_id;
   int parent_event_id;
   int chain_step;
   int scale_L;
   int level;
   int direction;
   int status;
   int branch_mode;

   FCN_Node origin;
   FCN_Node leg1;
   FCN_Node waist;
   FCN_Node leg2;
   FCN_Node internal1;
   FCN_Node internal2;
   FCN_Node confirm;
   FCN_Node invalid;

   bool has_internal1;
   bool has_internal2;
   bool has_confirm;
   bool has_invalid;
   bool has_pre_branch_leg2_break;

   double size;
   double parent_size;
   double size_ratio;
   double nd_close_ratio;
   string reason;
};

struct FCN_Config
{
   bool scan_f1;
   bool scan_f2;
   bool scan_f3;
   bool require_parent_confirmed;
   bool require_f2_parent_size;
   double f2_min_parent_size_ratio;
   bool scan_nd;
   bool detect_all_nd;
   int max_nd_per_scale;
   int nd_min_nodes;
   int nd_max_nodes;
   double nd_min_close_ratio;
   int max_events;
   int max_roots_per_scale;
   bool verbose_logs;
};

string FCN_DirectionToString(const int direction)
{
   if(direction == FCN_DIR_BULLISH) return "bullish";
   if(direction == FCN_DIR_BEARISH) return "bearish";
   return "none";
}

string FCN_LevelToString(const int level)
{
   if(level == FCN_LEVEL_F1) return "F1";
   if(level == FCN_LEVEL_F2) return "F2";
   if(level == FCN_LEVEL_F3) return "F3";
   if(level == FCN_LEVEL_ND) return "ND";
   return "F?";
}

string FCN_StatusToString(const int status)
{
   if(status == FCN_STATUS_LIVE) return "live";
   if(status == FCN_STATUS_CONFIRMED) return "confirmed";
   if(status == FCN_STATUS_INVALID) return "invalid";
   if(status == FCN_STATUS_TERMINAL) return "terminal";
   return "unknown";
}

string FCN_BranchToString(const int branch)
{
   if(branch == FCN_BRANCH_INTERNAL12) return "internal12";
   if(branch == FCN_BRANCH_WAIST_BREAK) return "waist_break";
   if(branch == FCN_BRANCH_PARTIAL_1) return "partial_1";
   return "none";
}

void FCN_ResetNode(FCN_Node &n)
{
   n.index = -1;
   n.time = 0;
   n.price = 0.0;
   n.kind = FCN_NODE_NONE;
}

FCN_Node FCN_MakeNode(const int index, const datetime time, const double price, const int kind)
{
   FCN_Node n;
   n.index = index;
   n.time = time;
   n.price = price;
   n.kind = kind;
   return n;
}

void FCN_ResetEvent(FCN_Event &e)
{
   e.event_id = -1;
   e.sequence_id = -1;
   e.parent_event_id = -1;
   e.chain_step = 0;
   e.scale_L = 0;
   e.level = FCN_LEVEL_ND;
   e.direction = FCN_DIR_NONE;
   e.status = FCN_STATUS_LIVE;
   e.branch_mode = FCN_BRANCH_NONE;
   FCN_ResetNode(e.origin);
   FCN_ResetNode(e.leg1);
   FCN_ResetNode(e.waist);
   FCN_ResetNode(e.leg2);
   FCN_ResetNode(e.internal1);
   FCN_ResetNode(e.internal2);
   FCN_ResetNode(e.confirm);
   FCN_ResetNode(e.invalid);
   e.has_internal1 = false;
   e.has_internal2 = false;
   e.has_confirm = false;
   e.has_invalid = false;
   e.has_pre_branch_leg2_break = false;
   e.size = 0.0;
   e.parent_size = 0.0;
   e.size_ratio = 0.0;
   e.nd_close_ratio = 0.0;
   e.reason = "";
}

bool FCN_IsBullish(const FCN_Event &e)
{
   return e.direction == FCN_DIR_BULLISH;
}

bool FCN_IsBearish(const FCN_Event &e)
{
   return e.direction == FCN_DIR_BEARISH;
}

bool FCN_BreaksAbove(const FCN_Node &n, const double level)
{
   return n.price > level;
}

bool FCN_BreaksBelow(const FCN_Node &n, const double level)
{
   return n.price < level;
}

double FCN_BodySize(const FCN_Node &origin, const FCN_Node &leg2)
{
   return MathAbs(leg2.price - origin.price);
}

bool FCN_IsValidNode(const FCN_Node &n)
{
   return n.index >= 0 && n.time > 0 && n.kind != FCN_NODE_NONE;
}

#endif
