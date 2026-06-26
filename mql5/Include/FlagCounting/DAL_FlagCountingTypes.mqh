#ifndef __DAL_FLAG_COUNTING_TYPES_MQH__
#define __DAL_FLAG_COUNTING_TYPES_MQH__
#property strict

enum FC_Direction
{
   FC_DIR_NONE    = 0,
   FC_DIR_BULLISH = 1,
   FC_DIR_BEARISH = -1
};

enum FC_NodeKind
{
   FC_NODE_NONE = 0,
   FC_NODE_HIGH = 1,
   FC_NODE_LOW  = -1
};

enum FC_FlagLevel
{
   FC_LEVEL_NONE = 0,
   FC_LEVEL_F1   = 1,
   FC_LEVEL_F2   = 2,
   FC_LEVEL_F3   = 3
};

enum FC_FlagStatus
{
   FC_STATUS_OPEN        = 0,
   FC_STATUS_CONFIRMED   = 1,
   FC_STATUS_INVALIDATED = 2
};

enum FC_BranchType
{
   FC_BRANCH_NONE        = 0,
   FC_BRANCH_INTERNAL12  = 1,
   FC_BRANCH_WAIST_BREAK = 2
};

struct FC_Node
{
   int      index;
   datetime time;
   double   price;
   int      kind;
};

struct FC_FlagEvent
{
   int level;
   int direction;
   int status;
   int branch_type;

   int parent_event_index;
   int parent_origin_index;
   int parent_level;

   int chain_id;
   int chain_step;

   FC_Node origin;
   FC_Node leg1;
   FC_Node waist;
   FC_Node leg2;
   FC_Node n1;
   FC_Node n2;

   bool has_n1;
   bool has_n2;

   int      confirm_index;
   datetime confirm_time;
   double   confirm_price;

   int      pre_branch_leg2_break_index;
   datetime pre_branch_leg2_break_time;
   double   pre_branch_leg2_break_price;

   int      invalid_index;
   datetime invalid_time;
   double   invalid_price;

   double   body_size;
   double   parent_body_size;
   double   parent_size_ratio;
};

void FC_InitNode(FC_Node &n)
{
   n.index = -1;
   n.time  = 0;
   n.price = 0.0;
   n.kind  = FC_NODE_NONE;
}

FC_Node FC_MakeNode(const int index, const datetime time, const double price, const int kind)
{
   FC_Node n;
   n.index = index;
   n.time  = time;
   n.price = price;
   n.kind  = kind;
   return n;
}

void FC_InitFlagEvent(FC_FlagEvent &e)
{
   e.level = FC_LEVEL_NONE;
   e.direction = FC_DIR_NONE;
   e.status = FC_STATUS_OPEN;
   e.branch_type = FC_BRANCH_NONE;

   e.parent_event_index = -1;
   e.parent_origin_index = -1;
   e.parent_level = FC_LEVEL_NONE;

   e.chain_id = -1;
   e.chain_step = 0;

   FC_InitNode(e.origin);
   FC_InitNode(e.leg1);
   FC_InitNode(e.waist);
   FC_InitNode(e.leg2);
   FC_InitNode(e.n1);
   FC_InitNode(e.n2);

   e.has_n1 = false;
   e.has_n2 = false;

   e.confirm_index = -1;
   e.confirm_time = 0;
   e.confirm_price = 0.0;

   e.pre_branch_leg2_break_index = -1;
   e.pre_branch_leg2_break_time = 0;
   e.pre_branch_leg2_break_price = 0.0;

   e.invalid_index = -1;
   e.invalid_time = 0;
   e.invalid_price = 0.0;

   e.body_size = 0.0;
   e.parent_body_size = 0.0;
   e.parent_size_ratio = 0.0;
}

string FC_DirectionToString(const int direction)
{
   if(direction == FC_DIR_BULLISH) return "BULLISH";
   if(direction == FC_DIR_BEARISH) return "BEARISH";
   return "NONE";
}

string FC_StatusToString(const int status)
{
   if(status == FC_STATUS_CONFIRMED) return "CONFIRMED";
   if(status == FC_STATUS_INVALIDATED) return "INVALIDATED";
   return "OPEN";
}

string FC_BranchToString(const int branch_type)
{
   if(branch_type == FC_BRANCH_INTERNAL12) return "INTERNAL12";
   if(branch_type == FC_BRANCH_WAIST_BREAK) return "WAIST_BREAK";
   return "NONE";
}

string FC_LevelToString(const int level)
{
   if(level == FC_LEVEL_F1) return "F1";
   if(level == FC_LEVEL_F2) return "F2";
   if(level == FC_LEVEL_F3) return "F3";
   if(level > 0) return "F" + IntegerToString(level);
   return "F?";
}

bool FC_IsBullish(const FC_FlagEvent &e)
{
   return e.direction == FC_DIR_BULLISH;
}

bool FC_IsBearish(const FC_FlagEvent &e)
{
   return e.direction == FC_DIR_BEARISH;
}

double FC_BodySizeFromNodes(const FC_Node &origin, const FC_Node &leg2)
{
   if(origin.index < 0 || leg2.index < 0) return 0.0;
   return MathAbs(leg2.price - origin.price);
}

double FC_FlagBodySize(const FC_FlagEvent &e)
{
   return FC_BodySizeFromNodes(e.origin, e.leg2);
}

#endif
