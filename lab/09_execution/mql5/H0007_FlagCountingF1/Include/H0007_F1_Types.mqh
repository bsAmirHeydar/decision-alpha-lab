#property strict

enum H0007_NodeType
{
   H0007_NODE_LOW  = -1,
   H0007_NODE_NONE = 0,
   H0007_NODE_HIGH = 1
};

enum H0007_F1Direction
{
   H0007_DIR_BEARISH = -1,
   H0007_DIR_NONE    = 0,
   H0007_DIR_BULLISH = 1
};

enum H0007_F1Status
{
   H0007_STATUS_OPEN        = 0,
   H0007_STATUS_INVALIDATED = 1,
   H0007_STATUS_CONFIRMED   = 2
};

enum H0007_BreakMode
{
   H0007_BREAK_WICK  = 0,
   H0007_BREAK_CLOSE = 1
};

struct H0007_F1Node
{
   int             index;
   datetime        time;
   double          price;
   H0007_NodeType  type;
   int             L;
};

struct H0007_F1Event
{
   H0007_F1Direction direction;
   H0007_F1Status    status;

   int    L_used;
   string matched_L_values;
   double score;

   H0007_F1Node H1;
   H0007_F1Node W;
   H0007_F1Node H2;
   H0007_F1Node N1;
   H0007_F1Node R12;
   H0007_F1Node N2;

   int      internal_trigger_index;
   datetime internal_trigger_time;
   double   internal_trigger_price;

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

string H0007_DirectionToString(H0007_F1Direction d)
{
   if(d == H0007_DIR_BULLISH) return "BULLISH";
   if(d == H0007_DIR_BEARISH) return "BEARISH";
   return "NONE";
}

string H0007_StatusToString(H0007_F1Status s)
{
   if(s == H0007_STATUS_CONFIRMED) return "CONFIRMED";
   if(s == H0007_STATUS_INVALIDATED) return "INVALIDATED";
   return "OPEN";
}

bool H0007_StringHasL(const string csv, const int L)
{
   string token = IntegerToString(L);
   string parts[];
   int n = StringSplit(csv, ',', parts);
   for(int i=0; i<n; i++)
      if(parts[i] == token)
         return true;
   return false;
}

string H0007_AddLToCsv(string csv, const int L)
{
   if(csv == "") return IntegerToString(L);
   if(H0007_StringHasL(csv, L)) return csv;
   return csv + "," + IntegerToString(L);
}
