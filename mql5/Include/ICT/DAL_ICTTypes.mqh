#ifndef __DAL_ICT_TYPES_MQH__
#define __DAL_ICT_TYPES_MQH__

#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/LRule/DAL_LRuleTypes.mqh>
#include <Common/DAL_Common.mqh>

enum DAL_ICTSweepMode
{
   ICT_SWEEP_TOUCH = 0,
   ICT_SWEEP_HUNT  = 1
};

enum DAL_ICTTargetMode
{
   ICT_TARGET_TOUCH = 0,
   ICT_TARGET_HUNT  = 1
};

enum DAL_ICTDirection
{
   ICT_DIR_NONE = 0,
   ICT_DIR_BUY  = 1,
   ICT_DIR_SELL = -1
};

enum DAL_ICTFvgKind
{
   ICT_FVG_NONE    = 0,
   ICT_FVG_BULLISH = 1,
   ICT_FVG_BEARISH = -1
};

enum DAL_ICTExitReason
{
   ICT_EXIT_NONE       = 0,
   ICT_EXIT_TP         = 1,
   ICT_EXIT_SL         = 2,
   ICT_EXIT_NEXT_SWEEP = 3,
   ICT_EXIT_CSV_END    = 4
};

struct DAL_ICTSweepEvent
{
   int id;
   int index;
   datetime time;
   DAL_ICTDirection setup_direction; // HIGH sweep -> SELL; LOW sweep -> BUY
   ENUM_DALNodeType node_type;
   int node_array_index;
   int node_id;
   int node_index;
   datetime node_time;
   datetime node_active_from_time;
   double node_price;
   double zone_low;
   double zone_high;
   double trigger_level;
   double bar_open;
   double bar_high;
   double bar_low;
   double bar_close;
   double sweep_extreme;
   bool is_hunt;
};

struct DAL_ICTFVG
{
   int id;
   int index;
   datetime time;
   DAL_ICTFvgKind kind;
   double zone_low;
   double zone_high;
   double width;
   int left_index;
   int middle_index;
   int right_index;
};

struct DAL_ICTIFVGEvent
{
   int id;
   int index;
   datetime time;
   int fvg_id;
   DAL_ICTDirection setup_direction;
   double zone_low;
   double zone_high;
   double inversion_close;
   double touch_depth_pct;
};

struct DAL_ICTCISDEvent
{
   int id;
   int index;
   datetime time;
   DAL_ICTDirection setup_direction;
   int leg_start_index;
   datetime leg_start_time;
   double leg_start_open;
   double confirm_close;
};

struct DAL_ICTEntrySignal
{
   int id;
   string symbol;
   ENUM_TIMEFRAMES timeframe;
   int L;
   DAL_ICTDirection direction;
   int sweep_id;
   datetime sweep_time;
   datetime valid_from_time;
   datetime valid_until_time;
   datetime valid_until_exclusive_time;
   int next_sweep_index;
   datetime next_sweep_time;
   int fvg_id;
   datetime fvg_time;
   double fvg_low;
   double fvg_high;
   int ifvg_index;
   datetime ifvg_time;
   int cisd_index;
   datetime cisd_time;
   int leg_start_index;
   datetime leg_start_time;
   double leg_start_open;
   datetime entry_time;
   double entry_price;
   double sl_price;
   double target_price;
   int target_node_id;
   datetime target_node_time;
   double target_node_price;
   double risk_points;
   double reward_points;
   double rr;
   datetime exit_time;
   DAL_ICTExitReason exit_reason;
   double exit_price;
   double pnl_r;
   int bars_to_exit;
};

string DAL_ICT_DirectionToString(const DAL_ICTDirection direction)
{
   if(direction == ICT_DIR_BUY) return "BUY";
   if(direction == ICT_DIR_SELL) return "SELL";
   return "NONE";
}

string DAL_ICT_SweepModeToString(const DAL_ICTSweepMode mode)
{
   return mode == ICT_SWEEP_HUNT ? "HUNT" : "TOUCH";
}

string DAL_ICT_TargetModeToString(const DAL_ICTTargetMode mode)
{
   return mode == ICT_TARGET_HUNT ? "HUNT" : "TOUCH";
}

string DAL_ICT_FvgKindToString(const DAL_ICTFvgKind kind)
{
   if(kind == ICT_FVG_BULLISH) return "BULLISH_FVG";
   if(kind == ICT_FVG_BEARISH) return "BEARISH_FVG";
   return "NONE";
}

string DAL_ICT_ExitReasonToString(const DAL_ICTExitReason reason)
{
   if(reason == ICT_EXIT_TP) return "TP";
   if(reason == ICT_EXIT_SL) return "SL";
   if(reason == ICT_EXIT_NEXT_SWEEP) return "NEXT_SWEEP";
   if(reason == ICT_EXIT_CSV_END) return "CSV_END";
   return "NONE";
}

string DAL_ICT_TimeStr(const datetime t)
{
   if(t <= 0) return "";
   return TimeToString(t, TIME_DATE | TIME_MINUTES);
}

#endif
