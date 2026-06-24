#ifndef __DAL_DISTRIBUTION_ENGINEERING_TYPES_MQH__
#define __DAL_DISTRIBUTION_ENGINEERING_TYPES_MQH__

// Decision Alpha Lab
// H0008 / EXP0012 - Distribution Engineering
// MQL5-only reusable research types for conditional sequence extraction.
// This file is research-only. It does not send orders.

#define DAL_DE_MAX_K        10
#define DAL_DE_K_SIZE       11
#define DAL_DE_MAX_GROUPS   512
#define DAL_DE_R_BUCKETS    15
#define DAL_DE_INF          1.0e100

// -----------------------------------------------------------------------------
// Enums
// -----------------------------------------------------------------------------

enum DAL_DETradeLayer
{
   DAL_DE_LAYER_UNKNOWN = 0,
   DAL_DE_LAYER_PROBE   = 1,
   DAL_DE_LAYER_LIVE    = 2
};

enum DAL_DEOutcomeClass
{
   DAL_DE_OUTCOME_LOSS = -1,
   DAL_DE_OUTCOME_FLAT = 0,
   DAL_DE_OUTCOME_WIN  = 1
};

// -----------------------------------------------------------------------------
// Small helpers
// -----------------------------------------------------------------------------

int DAL_DE_MinInt(const int a, const int b)
{
   return (a < b ? a : b);
}

int DAL_DE_MaxInt(const int a, const int b)
{
   return (a > b ? a : b);
}

double DAL_DE_SafeDiv(const double numerator, const double denominator, const double fallback = 0.0)
{
   if(MathAbs(denominator) <= 0.0)
      return fallback;
   return numerator / denominator;
}

string DAL_DE_BoolText(const bool v)
{
   return (v ? "true" : "false");
}

string DAL_DE_TfText(const ENUM_TIMEFRAMES tf)
{
   return IntegerToString((int)tf);
}

string DAL_DE_CleanKeyPart(string value)
{
   if(value == "")
      value = "NA";
   StringReplace(value, "|", "/");
   StringReplace(value, "=", ":");
   StringReplace(value, ",", ";");
   StringReplace(value, "\n", " ");
   StringReplace(value, "\r", " ");
   return value;
}

string DAL_DE_KeyAppend(const string key, const string name, const string value)
{
   string clean_name  = DAL_DE_CleanKeyPart(name);
   string clean_value = DAL_DE_CleanKeyPart(value);

   if(key == "" || key == "ALL" || key == "UNSPECIFIED")
      return clean_name + "=" + clean_value;

   return key + "|" + clean_name + "=" + clean_value;
}

string DAL_DE_KeyAppendInt(const string key, const string name, const int value)
{
   return DAL_DE_KeyAppend(key, name, IntegerToString(value));
}

string DAL_DE_KeyAppendBool(const string key, const string name, const bool value)
{
   return DAL_DE_KeyAppend(key, name, DAL_DE_BoolText(value));
}

string DAL_DE_KeyAppendDoubleBucket(
   const string key,
   const string name,
   const double value,
   const double low_thr,
   const double high_thr
)
{
   string bucket = "mid";
   if(value < low_thr)
      bucket = "low";
   else if(value > high_thr)
      bucket = "high";

   return DAL_DE_KeyAppend(key, name, bucket);
}

int DAL_DE_HourOf(const datetime t)
{
   if(t <= 0)
      return -1;

   MqlDateTime dt;
   if(!TimeToStruct(t, dt))
      return -1;
   return dt.hour;
}

// R distribution buckets.
//  0 <= -3R
//  1 (-3,-2]
//  2 (-2,-1]
//  3 (-1,-0.5]
//  4 (-0.5,0)
//  5 == 0
//  6 (0,0.5)
//  7 [0.5,1)
//  8 [1,2)
//  9 [2,3)
// 10 [3,5)
// 11 [5,10)
// 12 [10,25)
// 13 [25,100)
// 14 >= 100R
int DAL_DE_RBucketIndex(const double r)
{
   if(r <= -3.0) return 0;
   if(r <= -2.0) return 1;
   if(r <= -1.0) return 2;
   if(r <= -0.5) return 3;
   if(r <   0.0) return 4;
   if(r ==  0.0) return 5;
   if(r <   0.5) return 6;
   if(r <   1.0) return 7;
   if(r <   2.0) return 8;
   if(r <   3.0) return 9;
   if(r <   5.0) return 10;
   if(r <  10.0) return 11;
   if(r <  25.0) return 12;
   if(r < 100.0) return 13;
   return 14;
}

string DAL_DE_RBucketName(const int idx)
{
   if(idx == 0)  return "r<=-3";
   if(idx == 1)  return "-3<r<=-2";
   if(idx == 2)  return "-2<r<=-1";
   if(idx == 3)  return "-1<r<=-0.5";
   if(idx == 4)  return "-0.5<r<0";
   if(idx == 5)  return "r=0";
   if(idx == 6)  return "0<r<0.5";
   if(idx == 7)  return "0.5<=r<1";
   if(idx == 8)  return "1<=r<2";
   if(idx == 9)  return "2<=r<3";
   if(idx == 10) return "3<=r<5";
   if(idx == 11) return "5<=r<10";
   if(idx == 12) return "10<=r<25";
   if(idx == 13) return "25<=r<100";
   return "r>=100";
}

// -----------------------------------------------------------------------------
// Trade outcome record
// -----------------------------------------------------------------------------

struct DAL_DETradeOutcome
{
   string           strategy_id;
   string           execution_id;
   string           symbol;
   ENUM_TIMEFRAMES  timeframe;
   long             magic;

   ulong            position_id;
   ulong            deal_id;

   int              direction;        // +1 buy, -1 sell, 0 unknown
   DAL_DETradeLayer layer;            // probe/live/unknown

   datetime         entry_time;
   datetime         exit_time;

   double           entry_price;
   double           exit_price;
   double           stop_price;
   double           target_price;

   double           risk_money;       // money risk at entry. Needed for R from PnL.
   double           volume;

   double           gross_profit;
   double           commission;
   double           swap;
   double           net_profit;

   double           r_result;         // realized result in R units
   double           mfe_r;            // maximum favorable excursion in R
   double           mae_r;            // maximum adverse excursion in R

   int              bars_to_exit;
   int              seconds_to_exit;

   bool             is_win;
   bool             is_loss;
   bool             is_flat;
   bool             is_probe;
   bool             is_live;

   string           feature_key;      // causal/filter key built before entry
   string           note;
};

void DAL_DETradeOutcome_Reset(DAL_DETradeOutcome &o)
{
   o.strategy_id     = "";
   o.execution_id    = "";
   o.symbol          = "";
   o.timeframe       = PERIOD_CURRENT;
   o.magic           = 0;

   o.position_id     = 0;
   o.deal_id         = 0;

   o.direction       = 0;
   o.layer           = DAL_DE_LAYER_UNKNOWN;

   o.entry_time      = 0;
   o.exit_time       = 0;

   o.entry_price     = 0.0;
   o.exit_price      = 0.0;
   o.stop_price      = 0.0;
   o.target_price    = 0.0;

   o.risk_money      = 0.0;
   o.volume          = 0.0;

   o.gross_profit    = 0.0;
   o.commission      = 0.0;
   o.swap            = 0.0;
   o.net_profit      = 0.0;

   o.r_result        = 0.0;
   o.mfe_r           = 0.0;
   o.mae_r           = 0.0;

   o.bars_to_exit    = 0;
   o.seconds_to_exit = 0;

   o.is_win          = false;
   o.is_loss         = false;
   o.is_flat         = true;
   o.is_probe        = false;
   o.is_live         = false;

   o.feature_key     = "UNSPECIFIED";
   o.note            = "";
}

void DAL_DETradeOutcome_SetLayer(DAL_DETradeOutcome &o, const DAL_DETradeLayer layer)
{
   o.layer    = layer;
   o.is_probe = (layer == DAL_DE_LAYER_PROBE);
   o.is_live  = (layer == DAL_DE_LAYER_LIVE);
}

void DAL_DETradeOutcome_ClassifyByR(
   DAL_DETradeOutcome &o,
   const double win_threshold_r = 1.0,
   const double loss_threshold_r = -1.0
)
{
   o.is_win  = false;
   o.is_loss = false;
   o.is_flat = false;

   if(o.r_result >= win_threshold_r)
      o.is_win = true;
   else if(o.r_result <= loss_threshold_r)
      o.is_loss = true;
   else
      o.is_flat = true;
}

void DAL_DETradeOutcome_SetRFromMoney(DAL_DETradeOutcome &o)
{
   if(o.risk_money > 0.0)
      o.r_result = o.net_profit / o.risk_money;
}

#endif // __DAL_DISTRIBUTION_ENGINEERING_TYPES_MQH__
