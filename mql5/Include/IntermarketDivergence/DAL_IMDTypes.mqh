#ifndef __DAL_IMD_TYPES_MQH__
#define __DAL_IMD_TYPES_MQH__

#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/LRule/DAL_LRuleTypes.mqh>
#include <Common/DAL_Common.mqh>

enum DAL_IMDLevelSide
{
   IMD_LEVEL_LOW  = 0,
   IMD_LEVEL_HIGH = 1
};

enum DAL_IMDDivergenceSide
{
   IMD_DIV_NONE = 0,
   IMD_DIV_HIGH = 1,   // origin breaks/touches high, destination does not -> usually bearish/SELL context
   IMD_DIV_LOW  = -1   // origin breaks/touches low, destination does not -> usually bullish/BUY context
};

enum DAL_IMDTradeBias
{
   IMD_BIAS_NONE = 0,
   IMD_BIAS_BUY  = 1,
   IMD_BIAS_SELL = -1
};

enum DAL_IMDLevelSource
{
   IMD_LEVEL_PREVIOUS_CANDLE      = 0,
   IMD_LEVEL_ROLLING_LOOKBACK     = 1,
   IMD_LEVEL_L_NODE               = 2,
   IMD_LEVEL_CURRENT_SESSION      = 3,
   IMD_LEVEL_PREVIOUS_SESSION     = 4,
   IMD_LEVEL_CURRENT_DAY          = 5,
   IMD_LEVEL_PREVIOUS_DAY         = 6
};

enum DAL_IMDTriggerMode
{
   IMD_TRIGGER_WICK_TOUCH         = 0,
   IMD_TRIGGER_CLOSE_BREAK        = 1,
   IMD_TRIGGER_HUNT_REJECT_CLOSE  = 2
};

enum DAL_IMDOriginBarMode
{
   IMD_ORIGIN_CLOSED_BARS_ONLY    = 0,
   IMD_ORIGIN_INCLUDE_LIVE_BAR    = 1
};

enum DAL_IMDWindowEndReason
{
   IMD_WINDOW_NONE                = 0,
   IMD_WINDOW_FIXED_END           = 1,
   IMD_WINDOW_DEST_LATE_CONFIRM   = 2,
   IMD_WINDOW_NEXT_DIVERGENCE     = 3,
   IMD_WINDOW_DATA_END            = 4
};

struct DAL_IMDBarPair
{
   datetime time;
   DALBar a;
   DALBar b;
};

struct DAL_IMDReferenceLevel
{
   bool ok;
   double price;
   string source;
   int source_index;
   datetime source_time;
   int node_id;
   datetime active_from_time;
   double session_high;
   double session_low;
   datetime session_start;
   datetime session_end;
};

struct DAL_IMDProbeState
{
   bool origin_triggered;
   bool destination_triggered;
   bool destination_triggered_in_lag;
   datetime destination_confirm_time;
   int destination_confirm_index;
   double origin_ref_price;
   double destination_ref_price;
   int origin_ref_index;
   int destination_ref_index;
   datetime origin_ref_time;
   datetime destination_ref_time;
   int origin_node_id;
   int destination_node_id;
   double origin_probe_high;
   double origin_probe_low;
   double origin_probe_close;
   double destination_probe_high;
   double destination_probe_low;
   double destination_probe_close;
   double origin_break_points;
   double destination_break_points;
};

struct DAL_IMDDivergenceEvent
{
   int id;
   string pair_label;
   string origin_symbol;
   string destination_symbol;
   ENUM_TIMEFRAMES timeframe;
   int step_every_bars;
   int step_offset_bars;
   int index;
   datetime evaluation_time;
   datetime valid_from_time;
   datetime valid_until_time;
   datetime valid_until_exclusive_time;
   DAL_IMDDivergenceSide divergence_side;
   DAL_IMDTradeBias suggested_bias;
   DAL_IMDLevelSource origin_level_source;
   DAL_IMDLevelSource destination_level_source;
   DAL_IMDTriggerMode trigger_mode;
   int destination_lag_bars;
   int signal_valid_bars;
   double origin_ref_price;
   double destination_ref_price;
   datetime origin_ref_time;
   datetime destination_ref_time;
   int origin_ref_index;
   int destination_ref_index;
   int origin_node_id;
   int destination_node_id;
   double origin_open;
   double origin_high;
   double origin_low;
   double origin_close;
   double destination_open;
   double destination_high;
   double destination_low;
   double destination_close;
   double origin_break_points;
   double destination_break_points;
   double divergence_gap_points;
   double normalized_gap_ratio;
   datetime destination_confirm_time;
   DAL_IMDWindowEndReason window_end_reason;
   string note;
};

struct DAL_IMDEvaluatedStep
{
   int index;
   datetime time;
   string origin_symbol;
   string destination_symbol;
   string side;
   bool origin_triggered;
   bool destination_triggered;
   bool destination_triggered_in_lag;
   double origin_ref;
   double destination_ref;
   double origin_high;
   double origin_low;
   double destination_high;
   double destination_low;
};

string DAL_IMD_TimeStr(const datetime t)
{
   if(t <= 0) return "";
   return TimeToString(t, TIME_DATE | TIME_MINUTES);
}

string DAL_IMD_LevelSideToString(const DAL_IMDLevelSide side)
{
   return side == IMD_LEVEL_HIGH ? "HIGH" : "LOW";
}

string DAL_IMD_DivergenceSideToString(const DAL_IMDDivergenceSide side)
{
   if(side == IMD_DIV_HIGH) return "HIGH_DIVERGENCE";
   if(side == IMD_DIV_LOW) return "LOW_DIVERGENCE";
   return "NONE";
}

string DAL_IMD_BiasToString(const DAL_IMDTradeBias bias)
{
   if(bias == IMD_BIAS_BUY) return "BUY";
   if(bias == IMD_BIAS_SELL) return "SELL";
   return "NONE";
}

string DAL_IMD_LevelSourceToString(const DAL_IMDLevelSource src)
{
   if(src == IMD_LEVEL_PREVIOUS_CANDLE) return "PREVIOUS_CANDLE";
   if(src == IMD_LEVEL_ROLLING_LOOKBACK) return "ROLLING_LOOKBACK";
   if(src == IMD_LEVEL_L_NODE) return "L_NODE";
   if(src == IMD_LEVEL_CURRENT_SESSION) return "CURRENT_SESSION";
   if(src == IMD_LEVEL_PREVIOUS_SESSION) return "PREVIOUS_SESSION";
   if(src == IMD_LEVEL_CURRENT_DAY) return "CURRENT_DAY";
   if(src == IMD_LEVEL_PREVIOUS_DAY) return "PREVIOUS_DAY";
   return "UNKNOWN";
}

string DAL_IMD_TriggerModeToString(const DAL_IMDTriggerMode mode)
{
   if(mode == IMD_TRIGGER_CLOSE_BREAK) return "CLOSE_BREAK";
   if(mode == IMD_TRIGGER_HUNT_REJECT_CLOSE) return "HUNT_REJECT_CLOSE";
   return "WICK_TOUCH";
}

string DAL_IMD_WindowEndReasonToString(const DAL_IMDWindowEndReason reason)
{
   if(reason == IMD_WINDOW_FIXED_END) return "FIXED_END";
   if(reason == IMD_WINDOW_DEST_LATE_CONFIRM) return "DEST_LATE_CONFIRM";
   if(reason == IMD_WINDOW_NEXT_DIVERGENCE) return "NEXT_DIVERGENCE";
   if(reason == IMD_WINDOW_DATA_END) return "DATA_END";
   return "NONE";
}

#endif
