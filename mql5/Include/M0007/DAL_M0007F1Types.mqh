#ifndef __DAL_M0007_F1_TYPES_MQH__
#define __DAL_M0007_F1_TYPES_MQH__
#property strict

enum M0007_NodeType
{
   M0007_NODE_LOW  = -1,
   M0007_NODE_NONE = 0,
   M0007_NODE_HIGH = 1
};

enum M0007_F1Direction
{
   M0007_DIR_BEARISH = -1,
   M0007_DIR_NONE    = 0,
   M0007_DIR_BULLISH = 1
};

enum M0007_F1Status
{
   M0007_STATUS_OPEN        = 0,
   M0007_STATUS_INVALIDATED = 1,
   M0007_STATUS_CONFIRMED   = 2
};

enum M0007_BreakMode
{
   M0007_BREAK_WICK  = 0,
   M0007_BREAK_CLOSE = 1
};

struct M0007_F1Node
{
   int             index;
   datetime        time;
   double          price;
   M0007_NodeType  type;
   int             L;
};

struct M0007_F1Event
{
   M0007_F1Direction direction;
   M0007_F1Status    status;

   int    L_used;
   string matched_L_values;
   double score;

   // Core F1 topology. These four nodes are the mechanical truth.
   //
   // Bullish:
   //   Start LOW  -> H1 HIGH = end of leg 1 -> W LOW  = correction -> H2 HIGH = end of leg 2 / sweep of H1.
   //
   // Bearish:
   //   Start HIGH -> H1 LOW  = end of leg 1 -> W HIGH = correction -> H2 LOW  = end of leg 2 / sweep of H1.
   //
   // Start is not visual/synthetic. It is stored by the detector and must be used by the renderer.
   M0007_F1Node Start;
   M0007_F1Node H1;
   M0007_F1Node W;
   M0007_F1Node H2;

   // Internal count after leg 2.
   //
   // Bullish F1:
   //   N1 = first internal LOW after H2
   //   N2 = later internal LOW below N1
   //
   // Bearish F1:
   //   N1 = first internal HIGH after H2
   //   N2 = later internal HIGH above N1
   //
   // These are the chart labels "1" and "2". They are NOT leg-1/leg-2 labels.
   M0007_F1Node N1;
   M0007_F1Node R12; // optional compatibility slot; not part of the current visual count.
   M0007_F1Node N2;

   bool has_internal_1;
   bool has_internal_2;
   bool internal_12_valid;

   // If the post-leg2 internal 1/2 breaks the flag waist/correction level, the F1 is not valid.
   int      waist_break_index;
   datetime waist_break_time;
   double   waist_break_price;

   int      internal_trigger_index;
   datetime internal_trigger_time;
   double   internal_trigger_price;

   // Leg-2 break confirmation.
   // A four-node F1 candidate is not fully confirmed until price breaks the leg-2 extreme
   // after H2/L2, unless the caller explicitly disables that rule.
   int      leg2_break_index;
   datetime leg2_break_time;
   double   leg2_break_price;

   int      confirm_index;
   datetime confirm_time;
   double   confirm_price;

   int      invalidation_index;
   datetime invalidation_time;
   double   invalidation_price;

   int    bars_structure;
   int    bars_to_trigger;
   int    bars_to_confirm;
   string signature;
};

void M0007_ResetF1Node(M0007_F1Node &n)
{
   n.index = -1;
   n.time  = 0;
   n.price = 0.0;
   n.type  = M0007_NODE_NONE;
   n.L     = 0;
}

void M0007_InitF1Event(M0007_F1Event &e)
{
   e.direction = M0007_DIR_NONE;
   e.status = M0007_STATUS_OPEN;

   e.L_used = 0;
   e.matched_L_values = "";
   e.score = 0.0;

   M0007_ResetF1Node(e.Start);
   M0007_ResetF1Node(e.H1);
   M0007_ResetF1Node(e.W);
   M0007_ResetF1Node(e.H2);
   M0007_ResetF1Node(e.N1);
   M0007_ResetF1Node(e.R12);
   M0007_ResetF1Node(e.N2);

   e.has_internal_1 = false;
   e.has_internal_2 = false;
   e.internal_12_valid = false;

   e.waist_break_index = -1;
   e.waist_break_time = 0;
   e.waist_break_price = 0.0;

   e.internal_trigger_index = -1;
   e.internal_trigger_time = 0;
   e.internal_trigger_price = 0.0;

   e.leg2_break_index = -1;
   e.leg2_break_time = 0;
   e.leg2_break_price = 0.0;

   e.confirm_index = -1;
   e.confirm_time = 0;
   e.confirm_price = 0.0;

   e.invalidation_index = -1;
   e.invalidation_time = 0;
   e.invalidation_price = 0.0;

   e.bars_structure = 0;
   e.bars_to_trigger = -1;
   e.bars_to_confirm = -1;
   e.signature = "";
}

string M0007_DirectionToString(M0007_F1Direction d)
{
   if(d == M0007_DIR_BULLISH) return "BULLISH";
   if(d == M0007_DIR_BEARISH) return "BEARISH";
   return "NONE";
}

string M0007_StatusToString(M0007_F1Status s)
{
   if(s == M0007_STATUS_CONFIRMED) return "CONFIRMED";
   if(s == M0007_STATUS_INVALIDATED) return "INVALIDATED";
   return "OPEN";
}

bool M0007_StringHasL(const string csv, const int L)
{
   string token = IntegerToString(L);
   string parts[];
   int n = StringSplit(csv, ',', parts);
   for(int i=0; i<n; i++)
      if(parts[i] == token)
         return true;
   return false;
}

string M0007_AddLToCsv(string csv, const int L)
{
   if(csv == "") return IntegerToString(L);
   if(M0007_StringHasL(csv, L)) return csv;
   return csv + "," + IntegerToString(L);
}

#endif
