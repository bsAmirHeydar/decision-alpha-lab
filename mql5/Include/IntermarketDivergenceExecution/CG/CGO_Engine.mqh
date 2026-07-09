#ifndef __CGO_ENGINE_MQH__
#define __CGO_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGT_Time.mqh>
#include <IntermarketDivergenceExecution/CG/CGC_ConfirmationField.mqh>
#include <IntermarketDivergenceExecution/CG/CGO_OutcomeField.mqh>
#include <IntermarketDivergenceExecution/CG/CGO_Ledger.mqh>
#include <IntermarketDivergenceExecution/CG/CGO_Display.mqh>

class CCGO_Engine
{
private:
   SCGTTimeConfig m_time_config;
   SCGCConfirmationConfig m_confirmation_config;
   SCGOOutcomeConfig m_outcome_config;
   CCGT_TimeAnatomy m_time;
   CCGC_ConfirmationField m_confirmation_field;
   CCGO_OutcomeField m_outcome_field;
   CCGO_OutcomeLedger m_ledger;
   CCGO_Display m_display;
   SCGTGroupDef m_groups[CGT_GROUP_COUNT];
   SCGOStudySummary m_summary;
   long m_last_latest_key;

   void ResetSummary()
   {
      ZeroMemory(m_summary);
   }

   ENUM_TIMEFRAMES ResolveConfirmationTimeframe()
   {
      if(m_confirmation_config.confirmation_timeframe==PERIOD_CURRENT)
         return (ENUM_TIMEFRAMES)_Period;
      return m_confirmation_config.confirmation_timeframe;
   }

   void SetGroup(const int index,const string name,const int minutes,const bool enabled)
   {
      m_groups[index].id=(ECGTGroupId)index;
      m_groups[index].name=name;
      m_groups[index].minutes=minutes;
      m_groups[index].enabled=enabled;
   }

   void InitRegistry(bool &enabled[])
   {
      SetGroup(CGT_CG3M,   "cg_3m",   3,   enabled[CGT_CG3M]);
      SetGroup(CGT_CG5M,   "cg_5m",   5,   enabled[CGT_CG5M]);
      SetGroup(CGT_CG9M,   "cg_9m",   9,   enabled[CGT_CG9M]);
      SetGroup(CGT_CG10M,  "cg_10m",  10,  enabled[CGT_CG10M]);
      SetGroup(CGT_CG15M,  "cg_15m",  15,  enabled[CGT_CG15M]);
      SetGroup(CGT_CG18M,  "cg_18m",  18,  enabled[CGT_CG18M]);
      SetGroup(CGT_CG20M,  "cg_20m",  20,  enabled[CGT_CG20M]);
      SetGroup(CGT_CG24M,  "cg_24m",  24,  enabled[CGT_CG24M]);
      SetGroup(CGT_CG30M,  "cg_30m",  30,  enabled[CGT_CG30M]);
      SetGroup(CGT_CG40M,  "cg_40m",  40,  enabled[CGT_CG40M]);
      SetGroup(CGT_CG45M,  "cg_45m",  45,  enabled[CGT_CG45M]);
      SetGroup(CGT_CG60M,  "cg_60m",  60,  enabled[CGT_CG60M]);
      SetGroup(CGT_CG72M,  "cg_72m",  72,  enabled[CGT_CG72M]);
      SetGroup(CGT_CG90M,  "cg_90m",  90,  enabled[CGT_CG90M]);
      SetGroup(CGT_CG120M, "cg_120m", 120, enabled[CGT_CG120M]);
      SetGroup(CGT_CG150M, "cg_150m", 150, enabled[CGT_CG150M]);
      SetGroup(CGT_CG180M, "cg_180m", 180, enabled[CGT_CG180M]);
      SetGroup(CGT_CG240M, "cg_240m", 240, enabled[CGT_CG240M]);
      SetGroup(CGT_CG300M, "cg_300m", 300, enabled[CGT_CG300M]);
      SetGroup(CGT_CG360M, "cg_360m", 360, enabled[CGT_CG360M]);
      SetGroup(CGT_CG720M, "cg_720m", 720, enabled[CGT_CG720M]);
   }

   datetime ObservationCloseTimeFromShift(const int shift)
   {
      ENUM_TIMEFRAMES tf=ResolveConfirmationTimeframe();
      int seconds=PeriodSeconds(tf);
      if(seconds<=0) seconds=60;
      datetime open=iTime(m_confirmation_config.symbol_a,tf,shift);
      if(open<=0) open=iTime(_Symbol,tf,shift);
      if(open<=0) return 0;
      return open+seconds;
   }

   void AccumulateRowStats(SCGOOutcomeRow &row,const bool wrote,const bool duplicate)
   {
      if(duplicate) m_summary.rows_duplicate++;
      if(row.availability==CGO_OUTCOME_COMPLETE)
      {
         m_summary.rows_ready++;
         if(wrote) m_summary.rows_written++;
         if(row.direction==CGC_DIRECTION_BUY) m_summary.buy_rows++;
         if(row.direction==CGC_DIRECTION_SELL) m_summary.sell_rows++;
         if(row.stop_hit_intraday) m_summary.stop_hit_rows++;
         m_summary.average_cycle_end_r+=row.cycle_end_r;
         m_summary.average_day_end_r+=row.day_end_r;
         m_summary.average_mfe_r+=row.mfe_r;
      }
      else if(row.availability==CGO_OUTCOME_MISSING_DATA) m_summary.rows_missing_data++;
      else if(row.availability==CGO_OUTCOME_PENDING_FUTURE) m_summary.rows_pending_future++;
      else if(row.availability==CGO_OUTCOME_ZERO_RISK) m_summary.rows_zero_risk++;
   }

   void FinalizeAverages()
   {
      if(m_summary.rows_ready<=0) return;
      m_summary.average_cycle_end_r/=m_summary.rows_ready;
      m_summary.average_day_end_r/=m_summary.rows_ready;
      m_summary.average_mfe_r/=m_summary.rows_ready;
   }

   void ProcessObservation(const datetime observation_broker,const bool allow_write)
   {
      if(observation_broker<=0) return;
      m_summary.observations++;
      SCGTTimeSnapshot time_snapshot;
      m_time.BuildTimeSnapshot(observation_broker,time_snapshot);

      for(int i=0;i<CGT_GROUP_COUNT;i++)
      {
         if(!m_groups[i].enabled) continue;
         SCGTCycleSnapshot cycle;
         m_time.BuildCycleSnapshot(time_snapshot,m_groups[i],cycle);
         SCGCFinalSignal signals[];
         SCGCGroupConfirmationState state;
         int count=m_confirmation_field.BuildFinalSignalsForGroup(time_snapshot,cycle,signals,state);
         if(count<=0) continue;
         for(int s=0;s<count;s++)
         {
            if(signals[s].status!=CGC_STATUS_CONFIRMED_TRADEABLE)
               continue;
            m_summary.confirmed_signals_seen++;
            SCGOOutcomeRow row;
            if(m_outcome_field.BuildOutcome(signals[s],row))
            {
               bool duplicate=false;
               bool wrote=false;
               if(allow_write && m_outcome_config.enable_ledger && m_summary.rows_written<m_outcome_config.max_rows_to_write)
                  wrote=m_ledger.WriteRow(row,duplicate);
               AccumulateRowStats(row,wrote,duplicate);
            }
         }
      }
   }

public:
   void Init(SCGTTimeConfig &time_config,SCGCConfirmationConfig &confirmation_config,SCGOOutcomeConfig &outcome_config,bool &enabled[])
   {
      m_time_config=time_config;
      m_confirmation_config=confirmation_config;
      if(m_confirmation_config.confirmation_timeframe==PERIOD_CURRENT)
         m_confirmation_config.confirmation_timeframe=(ENUM_TIMEFRAMES)_Period;
      m_outcome_config=outcome_config;
      if(m_outcome_config.max_rows_to_write<1) m_outcome_config.max_rows_to_write=5000;
      m_last_latest_key=-1;
      InitRegistry(enabled);
      m_time.Configure(m_time_config);
      m_confirmation_field.Configure(m_confirmation_config);
      m_outcome_field.Configure(m_outcome_config);
      m_ledger.Configure(m_outcome_config);
      m_ledger.ResetFileIfNeeded();
      m_ledger.EnsureHeader();
      ResetSummary();
   }

   void RunHistoricalStudy(const int lookback_trading_days,const int max_closed_candles)
   {
      ResetSummary();
      int max_candles=max_closed_candles;
      if(max_candles<1) max_candles=300;
      ENUM_TIMEFRAMES tf=ResolveConfirmationTimeframe();
      int seconds=PeriodSeconds(tf);
      if(seconds<=0) seconds=60;
      int cap_by_days=lookback_trading_days*24*60*60/seconds;
      if(cap_by_days>0 && cap_by_days<max_candles) max_candles=cap_by_days;
      if(max_candles<1) max_candles=1;

      for(int shift=max_candles; shift>=1; shift--)
      {
         datetime observation=ObservationCloseTimeFromShift(shift);
         if(observation<=0) continue;
         ProcessObservation(observation,true);
      }
      FinalizeAverages();
      if(m_outcome_config.print_summary)
         Print(m_display.BuildSummary(m_summary));
      if(m_outcome_config.show_chart_panel)
         Comment(m_display.BuildSummary(m_summary));
   }

   void ProcessLatestClosedCandle()
   {
      datetime observation=ObservationCloseTimeFromShift(1);
      if(observation<=0) return;
      long key=(long)(observation/60);
      if(key==m_last_latest_key) return;
      m_last_latest_key=key;
      ResetSummary();
      ProcessObservation(observation,true);
      FinalizeAverages();
      if(m_outcome_config.print_summary)
         Print(m_display.BuildSummary(m_summary));
      if(m_outcome_config.show_chart_panel)
         Comment(m_display.BuildSummary(m_summary));
   }

   void Clear()
   {
      Comment("");
   }
};

#endif
