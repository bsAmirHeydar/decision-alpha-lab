#ifndef __DAL_STC_ENUMS_MQH__
#define __DAL_STC_ENUMS_MQH__
#property strict

enum STC_RuntimeMode
{
   STC_MODE_RESEARCH_BACKTEST = 0,
   STC_MODE_PAPER_LIVE        = 1,
   STC_MODE_AUTO_TRADE        = 2
};

enum STC_CandleCheckTf
{
   STC_CHECK_M1  = 1,
   STC_CHECK_M3  = 3,
   STC_CHECK_M5  = 5,
   STC_CHECK_M10 = 10,
   STC_CHECK_M15 = 15,
   STC_CHECK_M30 = 30
};

enum STC_Direction
{
   STC_DIR_NONE = 0,
   STC_DIR_BUY  = 1,
   STC_DIR_SELL = 2
};

enum STC_Side
{
   STC_SIDE_NONE = 0,
   STC_SIDE_HIGH = 1,
   STC_SIDE_LOW  = 2
};

enum STC_InitStatus
{
   STC_INIT_OK = 0,
   STC_INIT_CONFIG_ERROR = 1,
   STC_INIT_SYMBOL_ERROR = 2,
   STC_INIT_FOLDER_ERROR = 3,
   STC_INIT_INSTANCE_LOCK_ERROR = 4
};

enum STC_MCycle
{
   STC_M_NONE = 0,
   STC_M1     = 1,
   STC_M2     = 2,
   STC_M3     = 3
};

enum STC_WCycle
{
   STC_W_NONE = 0,
   STC_W1     = 1,
   STC_W2     = 2,
   STC_W3     = 3,
   STC_W4     = 4
};

enum STC_TimePhase
{
   STC_PHASE_PRE_DAY_OR_POST_CLOSE = 0,
   STC_PHASE_ACTIVE_M              = 1,
   STC_PHASE_M_GAP                 = 2,
   STC_PHASE_HARD_CLOSE_ZONE       = 3
};

string STC_RuntimeModeText(const STC_RuntimeMode mode)
{
   if(mode == STC_MODE_RESEARCH_BACKTEST) return "RESEARCH_BACKTEST";
   if(mode == STC_MODE_PAPER_LIVE)        return "PAPER_LIVE";
   if(mode == STC_MODE_AUTO_TRADE)        return "AUTO_TRADE";
   return "UNKNOWN";
}

string STC_CheckTfText(const STC_CandleCheckTf tf)
{
   if(tf == STC_CHECK_M1)  return "M1";
   if(tf == STC_CHECK_M3)  return "M3";
   if(tf == STC_CHECK_M5)  return "M5";
   if(tf == STC_CHECK_M10) return "M10";
   if(tf == STC_CHECK_M15) return "M15";
   if(tf == STC_CHECK_M30) return "M30";
   return "UNKNOWN";
}

string STC_DirectionText(const STC_Direction direction)
{
   if(direction == STC_DIR_BUY)  return "BUY";
   if(direction == STC_DIR_SELL) return "SELL";
   return "NONE";
}

string STC_SideText(const STC_Side side)
{
   if(side == STC_SIDE_HIGH) return "HIGH";
   if(side == STC_SIDE_LOW)  return "LOW";
   return "NONE";
}

string STC_MCycleText(const STC_MCycle cycle)
{
   if(cycle == STC_M1) return "M1";
   if(cycle == STC_M2) return "M2";
   if(cycle == STC_M3) return "M3";
   return "NONE";
}

string STC_WCycleText(const STC_WCycle cycle)
{
   if(cycle == STC_W1) return "W1";
   if(cycle == STC_W2) return "W2";
   if(cycle == STC_W3) return "W3";
   if(cycle == STC_W4) return "W4";
   return "NONE";
}

string STC_TimePhaseText(const STC_TimePhase phase)
{
   if(phase == STC_PHASE_ACTIVE_M) return "ACTIVE_M";
   if(phase == STC_PHASE_M_GAP) return "M_GAP_NO_ENTRY_NO_DETECTION";
   if(phase == STC_PHASE_HARD_CLOSE_ZONE) return "HARD_CLOSE_ZONE";
   return "PRE_DAY_OR_POST_CLOSE";
}

#endif
