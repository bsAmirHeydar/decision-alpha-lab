#ifndef __DAL_COMMON_MQH__
#define __DAL_COMMON_MQH__

enum ENUM_DALNodeType
{
   DAL_NODE_LOW  = 0,
   DAL_NODE_HIGH = 1
};

enum ENUM_DALBaselineKind
{
   DAL_BASELINE_ACTUAL = 0,
   DAL_BASELINE_RANDOM = 1
};

string DAL_NodeTypeToString(const ENUM_DALNodeType type)
{
   return type == DAL_NODE_LOW ? "LOW" : "HIGH";
}

color DAL_NodeColor(const ENUM_DALNodeType type)
{
   return type == DAL_NODE_LOW ? clrLime : clrTomato;
}

string DAL_BoolToString(const bool value)
{
   return value ? "true" : "false";
}

string DAL_CompactTime(const datetime t)
{
   return TimeToString(t, TIME_DATE | TIME_MINUTES);
}

int DAL_ClampInt(const int value, const int low, const int high)
{
   if(value < low) return low;
   if(value > high) return high;
   return value;
}

double DAL_ClampDouble(const double value, const double low, const double high)
{
   if(value < low) return low;
   if(value > high) return high;
   return value;
}

#endif
