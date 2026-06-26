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

   // Correct F1 core topology:
   // Bullish: Start LOW -> H1 high = end of leg 1 -> W low = correction -> H2 high = end of leg 2 / prior-high break.
   // Bearish: Start HIGH -> H1 low  = end of leg 1 -> W high = correction -> H2 low  = end of leg 2 / prior-low break.
   M0007_F1Node Start;
   M0007_F1Node H1;
   M0007_F1Node W;
   M0007_F1Node H2;

   // Legacy slots are kept only for compatibility with older logs/reports.
   // They are no longer part of the F1 definition.
   M0007_F1Node N1;
   M0007_F1Node R12;
   M0007_F1Node N2;

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
