#property strict
#property description "Astro-only sect and benefic/malefic pressure executor."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFamilyThresholds.mqh>
#include <Research/DAL_AstroExecutionJournal.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>
#include <Research/DAL_AstroSignalWindows.mqh>

input string          InpAstroCsvFile             = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours     = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe            = PERIOD_M1;
input bool            InpRequireExactBarTime      = true;
input double          InpBeneficSupportMinimum    = 64.0;
input double          InpMaleficPressureMinimum   = 62.0;
input double          InpHouseEdgeMinimum         = 10.0;
input bool            InpUseChartComment          = true;
input string          InpJournalFile              = "astro\\paper\\a0004_sect_benefic_pressure.csv";
input bool            InpJournalUseCommon         = true;
input bool            InpBatchBacktestOnInit      = true;
input bool            InpStopAfterBatch           = true;
input int             InpTimerSeconds             = 5;
input string          InpSignalWindowFile         = "astro\\paper\\a0004_pure_signal_windows.csv";
input bool            InpUseDoctrineThresholds    = true;
input double          InpArmThreshold             = 59.0;
input double          InpEnterThreshold           = 67.0;
input double          InpReduceThreshold          = 53.0;
input double          InpExitThreshold            = 59.0;

DAL_AstroMapStore g_store_sect;
datetime g_last_bar_time_sect = 0;
DAL_AstroExecState g_state_sect;
DAL_AstroThresholdProfile g_thresholds_sect;
int g_batch_journal_handle_sect = INVALID_HANDLE;

bool A0004_ProcessRow(const DAL_AstroMapRow &row, const bool verbose)
{
   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
      return false;

   double benefic_min = InpUseDoctrineThresholds ? g_thresholds_sect.benefic_support_minimum : InpBeneficSupportMinimum;
   double malefic_min = InpUseDoctrineThresholds ? g_thresholds_sect.malefic_pressure_minimum : InpMaleficPressureMinimum;
   double house_edge_min = InpUseDoctrineThresholds ? g_thresholds_sect.house_edge_minimum : InpHouseEdgeMinimum;

   double support_edge = s.benefic_support_score - s.malefic_pressure_score;
   double house_edge = s.house_lift_score - s.house_drag_score;
   string doctrine_state = "neutral";

   if(s.benefic_support_score >= benefic_min && support_edge >= house_edge_min && house_edge >= house_edge_min)
      doctrine_state = "benefic_release";
   else if(s.malefic_pressure_score >= malefic_min && (-support_edge) >= house_edge_min && (-house_edge) >= house_edge_min)
      doctrine_state = "malefic_pressure";

   DAL_AstroPureSignal gated = s;
   if(doctrine_state == "benefic_release")
   {
      if(gated.direction_name != "long")
         gated.entry_signal = "wait";
   }
   else if(doctrine_state == "malefic_pressure")
   {
      if(gated.direction_name != "short")
         gated.entry_signal = "wait";
   }
   else
      gated.entry_signal = "wait";

   double arm_threshold    = InpUseDoctrineThresholds ? g_thresholds_sect.arm_threshold    : InpArmThreshold;
   double enter_threshold  = InpUseDoctrineThresholds ? g_thresholds_sect.enter_threshold  : InpEnterThreshold;
   double reduce_threshold = InpUseDoctrineThresholds ? g_thresholds_sect.reduce_threshold : InpReduceThreshold;
   double exit_threshold   = InpUseDoctrineThresholds ? g_thresholds_sect.exit_threshold   : InpExitThreshold;
   DAL_AstroExecState_Step(g_state_sect, row, gated, arm_threshold, enter_threshold, reduce_threshold, exit_threshold);
   if(g_batch_journal_handle_sect != INVALID_HANDLE)
      DAL_AstroJournal_WriteHandle(g_batch_journal_handle_sect, row, gated, g_state_sect);
   else
      DAL_AstroJournal_Append(InpJournalFile, InpJournalUseCommon, row, gated, g_state_sect);

   if(verbose)
   {
      string txt = "A0004 ASTRO SECT BENEFIC PRESSURE\n";
      txt += "sect=" + s.sect_name + " doctrine=" + doctrine_state + "\n";
      txt += "benefic=" + DoubleToString(s.benefic_support_score, 1) + " malefic=" + DoubleToString(s.malefic_pressure_score, 1) + "\n";
      txt += "lift=" + DoubleToString(s.house_lift_score, 1) + " drag=" + DoubleToString(s.house_drag_score, 1) + "\n";
      txt += "entry=" + gated.entry_signal + " exit=" + gated.exit_signal + "\n";
      txt += DAL_AstroExecState_ToText(g_state_sect);

      if(InpUseChartComment)
         Comment(txt);

      Print("A0004|", TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES),
            "|sect=", s.sect_name,
            "|doctrine=", doctrine_state,
            "|benefic=", DoubleToString(s.benefic_support_score, 1),
            "|malefic=", DoubleToString(s.malefic_pressure_score, 1),
            "|phase=", g_state_sect.phase,
            "|action=", g_state_sect.action);
   }

   return true;
}

void A0004_RunBatch()
{
   if(!g_store_sect.loaded)
      return;

   DAL_AstroExecState_Reset(g_state_sect, "A0004_sect_benefic_pressure");
   DAL_AstroJournal_OpenReset(InpJournalFile, InpJournalUseCommon, g_batch_journal_handle_sect);

   int processed = 0;
   for(int i = 0; i < g_store_sect.row_count; i++)
   {
      if(A0004_ProcessRow(g_store_sect.rows[i], false))
         processed++;
   }

   if(g_batch_journal_handle_sect != INVALID_HANDLE)
   {
      FileClose(g_batch_journal_handle_sect);
      g_batch_journal_handle_sect = INVALID_HANDLE;
   }

   bool windows_ok = DAL_AstroSW_ExportPureWindows(InpSignalWindowFile, InpJournalUseCommon, g_store_sect);
   Print("A0004 BATCH COMPLETE | rows=", g_store_sect.row_count,
         " processed=", processed,
         " windows_export=", windows_ok ? "ok" : "failed",
         " journal=", InpJournalFile,
         " windows=", InpSignalWindowFile);
}

void A0004_ProcessCurrentBar()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time_sect)
      return;
   g_last_bar_time_sect = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store_sect, bar_time, row, InpRequireExactBarTime))
      return;

   A0004_ProcessRow(row, true);
}

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store_sect, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   DAL_AstroExecState_Reset(g_state_sect, "A0004_sect_benefic_pressure");
   DAL_AstroThresholdProfile_Load("A0004_sect_benefic_pressure", g_thresholds_sect);

   if(InpBatchBacktestOnInit)
   {
      A0004_RunBatch();
      if(InpStopAfterBatch)
         ExpertRemove();
      return INIT_SUCCEEDED;
   }

   EventSetTimer(MathMax(1, InpTimerSeconds));
   return INIT_SUCCEEDED;
}

void OnTick() {}
void OnTimer() { A0004_ProcessCurrentBar(); }

void OnDeinit(const int reason)
{
   EventKillTimer();
   Comment("");
}
