#property strict
#property description "Astro-only live execution shell. Routes pure astro state into optional broker orders."

#include <Trade/Trade.mqh>
#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFamilyThresholds.mqh>
#include <Research/DAL_AstroExecutionJournal.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>

input string          InpAstroCsvFile         = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe        = PERIOD_M1;
input bool            InpRequireExactBarTime  = true;
input bool            InpEnableLiveOrders     = false;
input double          InpLots                 = 0.01;
input int             InpSlippagePoints       = 30;
input long            InpMagic                = 900090;
input string          InpJournalFile          = "astro\\paper\\a0090_live_shell.csv";
input bool            InpJournalUseCommon     = true;
input bool            InpUseDoctrineThresholds = true;
input double          InpArmThreshold         = 58.0;
input double          InpEnterThreshold       = 68.0;
input double          InpReduceThreshold      = 52.0;
input double          InpExitThreshold        = 60.0;
input bool            InpUseChartComment      = true;

CTrade g_trade;
DAL_AstroMapStore g_store_shell;
DAL_AstroExecState g_state_shell;
DAL_AstroThresholdProfile g_thresholds_shell;
datetime g_last_bar_time_shell = 0;

bool DAL_AstroShell_HasPosition(const string symbol, const long magic, int &position_type)
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;
      position_type = (int)PositionGetInteger(POSITION_TYPE);
      return true;
   }
   position_type = -1;
   return false;
}

void DAL_AstroShell_CloseAll(const string symbol, const long magic)
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;
      g_trade.PositionClose(ticket, InpSlippagePoints);
   }
}

void DAL_AstroShell_Execute(const DAL_AstroExecState &state)
{
   int position_type = -1;
   bool has_position = DAL_AstroShell_HasPosition(_Symbol, InpMagic, position_type);
   if(!InpEnableLiveOrders)
      return;

   if(state.action == "exit" || state.action == "reduce")
   {
      if(has_position)
         DAL_AstroShell_CloseAll(_Symbol, InpMagic);
      return;
   }

   if(state.action != "enter")
      return;

   if(has_position)
      DAL_AstroShell_CloseAll(_Symbol, InpMagic);

   g_trade.SetExpertMagicNumber(InpMagic);
   g_trade.SetDeviationInPoints(InpSlippagePoints);

   if(state.position_direction == "long")
      g_trade.Buy(InpLots, _Symbol);
   else if(state.position_direction == "short")
      g_trade.Sell(InpLots, _Symbol);
}

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store_shell, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   DAL_AstroExecState_Reset(g_state_shell, "A0090_live_shell");
   DAL_AstroThresholdProfile_Load("A0090_live_shell", g_thresholds_shell);
   g_trade.SetExpertMagicNumber(InpMagic);
   g_trade.SetDeviationInPoints(InpSlippagePoints);
   return INIT_SUCCEEDED;
}

void OnTick()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time_shell)
      return;
   g_last_bar_time_shell = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store_shell, bar_time, row, InpRequireExactBarTime))
      return;

   DAL_AstroPureSignal signal;
   if(!DAL_AstroPureSignal_Calc(row, signal) || !signal.valid)
      return;

   double arm_threshold = InpUseDoctrineThresholds ? g_thresholds_shell.arm_threshold : InpArmThreshold;
   double enter_threshold = InpUseDoctrineThresholds ? g_thresholds_shell.enter_threshold : InpEnterThreshold;
   double reduce_threshold = InpUseDoctrineThresholds ? g_thresholds_shell.reduce_threshold : InpReduceThreshold;
   double exit_threshold = InpUseDoctrineThresholds ? g_thresholds_shell.exit_threshold : InpExitThreshold;
   DAL_AstroExecState_Step(g_state_shell, row, signal, arm_threshold, enter_threshold, reduce_threshold, exit_threshold);
   DAL_AstroJournal_Append(InpJournalFile, InpJournalUseCommon, row, signal, g_state_shell);
   DAL_AstroShell_Execute(g_state_shell);

   if(InpUseChartComment)
   {
      string txt = "A0090 ASTRO LIVE SHELL\n";
      txt += "orders=" + (InpEnableLiveOrders ? "enabled" : "disabled") + "\n";
      txt += DAL_AstroPureSignal_ToText(row, signal) + "\n";
      txt += DAL_AstroExecState_ToText(g_state_shell);
      Comment(txt);
   }
}

void OnDeinit(const int reason)
{
   Comment("");
}
