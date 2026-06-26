#ifndef __DAL_IMD_TYPES_MQH__
#define __DAL_IMD_TYPES_MQH__
#property strict

enum IMD_DataSource
{
   IMD_DS_BROKER_SERIES = 0,
   IMD_DS_EXTERNAL_CSV  = 1
};

enum IMD_RunMode
{
   IMD_RUN_BACKTEST_BATCH = 0,
   IMD_RUN_LIVE_MONITOR   = 1
};

enum IMD_LevelFamily
{
   IMD_LEVEL_PREVIOUS_CANDLE = 0,
   IMD_LEVEL_ROLLING_LOOKBACK = 1,
   IMD_LEVEL_CURRENT_SESSION = 2,
   IMD_LEVEL_PREVIOUS_SESSION = 3
};

enum IMD_TriggerMode
{
   IMD_TRIGGER_WICK_TOUCH = 0,
   IMD_TRIGGER_CLOSE_BREAK = 1,
   IMD_TRIGGER_HUNT_REJECT_CLOSE = 2
};

enum IMD_DivergenceSide
{
   IMD_DIV_HIGH = 0,
   IMD_DIV_LOW  = 1
};

enum IMD_Bias
{
   IMD_BIAS_NONE = 0,
   IMD_BIAS_BUY  = 1,
   IMD_BIAS_SELL = 2
};

struct IMD_Bar
{
   datetime time;
   double open;
   double high;
   double low;
   double close;
   long volume;
};

struct IMD_LevelPair
{
   bool ok;
   double high;
   double low;
   datetime high_time;
   datetime low_time;
   int high_index;
   int low_index;
   string source_name;
};

struct IMD_Event
{
   int id;
   string pair_label;
   string origin_symbol;
   string destination_symbol;
   int bar_index;
   datetime evaluation_time;
   datetime valid_from_time;
   datetime valid_until_time;
   IMD_DivergenceSide side;
   IMD_Bias suggested_bias;
   IMD_LevelFamily level_family;
   IMD_TriggerMode trigger_mode;
   int step_every_bars;
   int step_offset_bars;
   int destination_lag_bars;
   int signal_valid_bars;
   double origin_ref_price;
   double destination_ref_price;
   datetime origin_ref_time;
   datetime destination_ref_time;
   int origin_ref_index;
   int destination_ref_index;
   double origin_break_points;
   double destination_break_points;
   double divergence_gap_points;
   bool destination_late_confirmed;
   datetime destination_confirm_time;
   double entry_close;
   double mfe_points;
   double mae_points;
   double return_points;
   int bars_to_mfe;
   int bars_to_mae;
   string note;
};

string IMD_BoolText(const bool v)
{
   return v ? "true" : "false";
}

string IMD_SideText(const IMD_DivergenceSide side)
{
   return side == IMD_DIV_HIGH ? "HIGH_DIVERGENCE" : "LOW_DIVERGENCE";
}

string IMD_BiasText(const IMD_Bias bias)
{
   if(bias == IMD_BIAS_BUY) return "BUY";
   if(bias == IMD_BIAS_SELL) return "SELL";
   return "NONE";
}

string IMD_LevelFamilyText(const IMD_LevelFamily f)
{
   if(f == IMD_LEVEL_PREVIOUS_CANDLE) return "PREVIOUS_CANDLE";
   if(f == IMD_LEVEL_ROLLING_LOOKBACK) return "ROLLING_LOOKBACK";
   if(f == IMD_LEVEL_CURRENT_SESSION) return "CURRENT_SESSION";
   if(f == IMD_LEVEL_PREVIOUS_SESSION) return "PREVIOUS_SESSION";
   return "UNKNOWN";
}

string IMD_TriggerModeText(const IMD_TriggerMode m)
{
   if(m == IMD_TRIGGER_WICK_TOUCH) return "WICK_TOUCH";
   if(m == IMD_TRIGGER_CLOSE_BREAK) return "CLOSE_BREAK";
   if(m == IMD_TRIGGER_HUNT_REJECT_CLOSE) return "HUNT_REJECT_CLOSE";
   return "UNKNOWN";
}

IMD_Bias IMD_DefaultBiasForSide(const IMD_DivergenceSide side)
{
   return side == IMD_DIV_HIGH ? IMD_BIAS_SELL : IMD_BIAS_BUY;
}

int IMD_MinuteOfDay(const datetime t)
{
   MqlDateTime dt;
   TimeToStruct(t, dt);
   return dt.hour * 60 + dt.min;
}

int IMD_DateKey(const datetime t)
{
   MqlDateTime dt;
   TimeToStruct(t, dt);
   return dt.year * 10000 + dt.mon * 100 + dt.day;
}

void IMD_InitEvent(IMD_Event &e)
{
   e.id = -1;
   e.pair_label = "";
   e.origin_symbol = "";
   e.destination_symbol = "";
   e.bar_index = -1;
   e.evaluation_time = 0;
   e.valid_from_time = 0;
   e.valid_until_time = 0;
   e.side = IMD_DIV_HIGH;
   e.suggested_bias = IMD_BIAS_NONE;
   e.level_family = IMD_LEVEL_PREVIOUS_CANDLE;
   e.trigger_mode = IMD_TRIGGER_WICK_TOUCH;
   e.step_every_bars = 1;
   e.step_offset_bars = 0;
   e.destination_lag_bars = 0;
   e.signal_valid_bars = 0;
   e.origin_ref_price = 0.0;
   e.destination_ref_price = 0.0;
   e.origin_ref_time = 0;
   e.destination_ref_time = 0;
   e.origin_ref_index = -1;
   e.destination_ref_index = -1;
   e.origin_break_points = 0.0;
   e.destination_break_points = 0.0;
   e.divergence_gap_points = 0.0;
   e.destination_late_confirmed = false;
   e.destination_confirm_time = 0;
   e.entry_close = 0.0;
   e.mfe_points = 0.0;
   e.mae_points = 0.0;
   e.return_points = 0.0;
   e.bars_to_mfe = 0;
   e.bars_to_mae = 0;
   e.note = "";
}

#endif
