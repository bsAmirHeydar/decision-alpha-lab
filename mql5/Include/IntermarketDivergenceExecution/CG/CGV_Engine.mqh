#ifndef __CGV_ENGINE_MQH__
#define __CGV_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGT_Time.mqh>
#include <IntermarketDivergenceExecution/CG/CGV_Display.mqh>
#include <IntermarketDivergenceExecution/CG/CGV_Drawing.mqh>

class CCGV_Engine
{
private:
   SCGTTimeConfig           m_time_config;
   SCGVVisualLedgerConfig   m_visual_config;
   SCGCConfirmationConfig   m_confirmation_config;
   CCGT_TimeAnatomy         m_time;
   CCGC_ConfirmationField   m_confirmation_field;
   CCGV_Drawing             m_drawing;
   CCGV_Ledger              m_ledger;
   CCGV_Display             m_display;
   SCGTGroupDef             m_groups[CGT_GROUP_COUNT];
   bool                     m_show_panel;
   bool                     m_print_on_new_closed_candle;
   long                     m_last_closed_candle_key;
   bool                     m_historical_backfill_done;
   int                      m_last_backfill_observation_count;
   int                      m_last_backfill_drawn_count;
   int                      m_last_backfill_ledger_count;

   ENUM_TIMEFRAMES ResolveTimeframe()
   {
      if(m_visual_config.confirmation_timeframe==PERIOD_CURRENT)
         return (ENUM_TIMEFRAMES)_Period;
      return m_visual_config.confirmation_timeframe;
   }

   int ResolveTimeframeSeconds()
   {
      ENUM_TIMEFRAMES tf=ResolveTimeframe();
      int seconds=PeriodSeconds(tf);
      if(seconds<=0)
         seconds=PeriodSeconds((ENUM_TIMEFRAMES)_Period);
      if(seconds<=0)
         seconds=60;
      return seconds;
   }

   datetime LastClosedCandleCloseBroker()
   {
      if(!m_visual_config.use_last_closed_candle_boundary)
         return TimeCurrent();

      ENUM_TIMEFRAMES tf=ResolveTimeframe();
      int seconds=ResolveTimeframeSeconds();

      datetime open_time=iTime(m_visual_config.symbol_a,tf,1);
      if(open_time<=0)
         open_time=iTime(_Symbol,tf,1);
      if(open_time<=0)
         return TimeCurrent();

      datetime close_time=open_time+seconds;
      datetime now=TimeCurrent();
      if(close_time>now)
         return now;
      return close_time;
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

   void BuildConfirmationConfig()
   {
      m_confirmation_config.symbol_a=m_visual_config.symbol_a;
      m_confirmation_config.symbol_b=m_visual_config.symbol_b;
      m_confirmation_config.broker_utc_offset_hours=m_visual_config.broker_utc_offset_hours;
      m_confirmation_config.confirmation_timeframe=m_visual_config.confirmation_timeframe;
      m_confirmation_config.use_last_closed_candle_boundary=m_visual_config.use_last_closed_candle_boundary;
      m_confirmation_config.max_groups_shown=m_visual_config.max_groups_shown;
      m_confirmation_config.max_signals_per_group_shown=m_visual_config.max_signals_per_group_shown;
      m_confirmation_config.require_m1_history=m_visual_config.require_m1_history;
      m_confirmation_config.show_only_groups_with_final_states=m_visual_config.show_only_groups_with_final_states;
      m_confirmation_config.show_invalidated_double_hunts=m_visual_config.show_invalidated_double_hunts;
      m_confirmation_config.show_prices=m_visual_config.show_prices;
      m_confirmation_config.show_stop_reference_preview=m_visual_config.show_stop_reference_preview;
      m_confirmation_config.enable_protected_reference_retirement=m_visual_config.enable_protected_reference_retirement;
      m_confirmation_config.retire_reference_when_protected_hunts=m_visual_config.retire_reference_when_protected_hunts;
      m_confirmation_config.allow_repeated_divergence_while_protected_survives=m_visual_config.allow_repeated_divergence_while_protected_survives;
      m_confirmation_config.suppress_retired_reference_signals=m_visual_config.suppress_retired_reference_signals;
      m_confirmation_config.reset_lifecycle_at_new_trading_day=m_visual_config.reset_lifecycle_at_new_trading_day;
      m_confirmation_config.max_protected_reference_records=m_visual_config.max_protected_reference_records;
   }

   void ResetVisualState(SCGVGroupVisualLedgerState &s,SCGCGroupConfirmationState &source)
   {
      s.group_name=source.group_name;
      s.group_minutes=source.group_minutes;
      s.enabled=source.enabled;
      s.inside_trading_day=source.inside_trading_day;
      s.current_cycle_number=source.current_cycle_number;
      s.previous_cycle_count=source.previous_cycle_count;
      s.final_state_count=source.final_state_count;
      s.confirmed_count=source.confirmed_tradeable_count;
      s.invalidated_count=source.invalidated_double_hunt_count;
      s.drawn_count=0;
      s.skipped_draw_count=0;
      s.ledger_written_count=0;
      s.ledger_duplicate_count=0;
      s.buy_count=source.buy_confirmed_count;
      s.sell_count=source.sell_confirmed_count;
      s.current_cycle_start_ny=source.current_cycle_start_ny;
      s.current_cycle_end_ny=source.current_cycle_end_ny;
   }

   bool IsNewClosedCandle(const datetime observation_broker)
   {
      long closed_key=(long)(observation_broker/60);
      if(closed_key!=m_last_closed_candle_key)
      {
         m_last_closed_candle_key=closed_key;
         return true;
      }
      return false;
   }

   bool ProcessObservation(const datetime observation_broker,
                           const bool allow_ledger,
                           const bool update_panel,
                           const bool allow_print,
                           const datetime live_broker_now,
                           int &drawn_total,
                           int &ledger_total)
   {
      drawn_total=0;
      ledger_total=0;

      SCGTTimeSnapshot time_snapshot;
      m_time.BuildTimeSnapshot(observation_broker,time_snapshot);

      SCGVGroupVisualLedgerState visual_states[];
      SCGCFinalSignal flat_signals[];
      int group_start[];
      int group_count[];
      ArrayResize(visual_states,0);
      ArrayResize(flat_signals,0);
      ArrayResize(group_start,0);
      ArrayResize(group_count,0);

      for(int i=0;i<CGT_GROUP_COUNT;i++)
      {
         if(!m_groups[i].enabled)
            continue;

         SCGTCycleSnapshot cycle;
         m_time.BuildCycleSnapshot(time_snapshot,m_groups[i],cycle);

         SCGCFinalSignal signals[];
         SCGCGroupConfirmationState confirmation_state;
         int signal_count=m_confirmation_field.BuildFinalSignalsForGroup(time_snapshot,cycle,signals,confirmation_state);

         int g=ArraySize(visual_states);
         ArrayResize(visual_states,g+1);
         ArrayResize(group_start,g+1);
         ArrayResize(group_count,g+1);
         ResetVisualState(visual_states[g],confirmation_state);

         int start=ArraySize(flat_signals);
         group_start[g]=start;
         group_count[g]=signal_count;

         if(signal_count>0)
         {
            ArrayResize(flat_signals,start+signal_count);
            for(int c=0;c<signal_count;c++)
            {
               flat_signals[start+c]=signals[c];
               if(m_visual_config.enable_drawing)
               {
                  if(m_drawing.DrawSignal(signals[c]))
                  {
                     visual_states[g].drawn_count++;
                     drawn_total++;
                  }
                  else
                     visual_states[g].skipped_draw_count++;
               }
               if(allow_ledger && m_visual_config.enable_ledger)
               {
                  SCGVLedgerWriteResult wr=m_ledger.AppendSignal(signals[c]);
                  if(wr.written)
                  {
                     visual_states[g].ledger_written_count++;
                     ledger_total++;
                  }
                  if(wr.duplicate)
                     visual_states[g].ledger_duplicate_count++;
               }
            }
         }
      }

      if(update_panel)
      {
         if(m_show_panel)
            Comment(m_display.BuildPanel(time_snapshot,m_visual_config,visual_states,flat_signals,group_start,group_count,live_broker_now));
         else
            Comment("");
      }

      if(allow_print)
         Print(m_display.BuildPrintSummary(time_snapshot,visual_states));

      return true;
   }

   int CollectBackfillObservationTimes(datetime &observation_times[])
   {
      ArrayResize(observation_times,0);
      if(!m_visual_config.enable_historical_visual_backfill)
         return 0;

      int max_bars=m_visual_config.historical_backfill_max_closed_candles;
      if(max_bars<1)
         max_bars=1;
      int lookback_days=m_visual_config.historical_backfill_lookback_trading_days;
      if(lookback_days<1)
         lookback_days=1;

      ENUM_TIMEFRAMES tf=ResolveTimeframe();
      int seconds=ResolveTimeframeSeconds();
      datetime latest_close=LastClosedCandleCloseBroker();
      datetime cutoff=(datetime)(latest_close - lookback_days*24*60*60);
      int bars=iBars(m_visual_config.symbol_a,tf);
      if(bars<=1)
         bars=iBars(_Symbol,tf);
      if(bars<=1)
         return 0;

      for(int shift=1;shift<bars && ArraySize(observation_times)<max_bars;shift++)
      {
         datetime open_time=iTime(m_visual_config.symbol_a,tf,shift);
         if(open_time<=0)
            open_time=iTime(_Symbol,tf,shift);
         if(open_time<=0)
            continue;
         datetime close_time=(datetime)(open_time+seconds);
         if(close_time>latest_close)
            continue;
         if(close_time<cutoff)
            break;
         int n=ArraySize(observation_times);
         ArrayResize(observation_times,n+1);
         observation_times[n]=close_time;
      }
      return ArraySize(observation_times);
   }

   void RunHistoricalVisualBackfill()
   {
      if(m_historical_backfill_done)
         return;
      m_historical_backfill_done=true;
      m_last_backfill_observation_count=0;
      m_last_backfill_drawn_count=0;
      m_last_backfill_ledger_count=0;

      if(!m_visual_config.enable_historical_visual_backfill)
         return;

      datetime observation_times[];
      int count=CollectBackfillObservationTimes(observation_times);
      if(count<=0)
      {
         if(m_visual_config.historical_backfill_print_summary)
            Print("EXP0017 Phase06 historical visual backfill: no closed candles found for scan.");
         return;
      }

      // Process oldest -> newest so the first confirmed visual for a given signal id is kept in place.
      for(int i=count-1;i>=0;i--)
      {
         if(m_visual_config.max_historical_visual_draws>0 && m_last_backfill_drawn_count>=m_visual_config.max_historical_visual_draws)
            break;
         int drawn=0;
         int ledger=0;
         ProcessObservation(observation_times[i],m_visual_config.historical_backfill_write_ledger,false,false,TimeCurrent(),drawn,ledger);
         m_last_backfill_observation_count++;
         m_last_backfill_drawn_count+=drawn;
         m_last_backfill_ledger_count+=ledger;
      }

      if(m_visual_config.historical_backfill_print_summary)
      {
         Print(StringFormat("EXP0017 Phase06 historical visual backfill complete: observations=%d drawn=%d ledger=%d lookback_days=%d max_closed_candles=%d keep_first=%s",
                            m_last_backfill_observation_count,
                            m_last_backfill_drawn_count,
                            m_last_backfill_ledger_count,
                            m_visual_config.historical_backfill_lookback_trading_days,
                            m_visual_config.historical_backfill_max_closed_candles,
                            (m_visual_config.keep_first_visual_for_same_signal_id ? "true" : "false")));
         if(m_visual_config.max_historical_visual_draws>0 && m_last_backfill_drawn_count>=m_visual_config.max_historical_visual_draws)
            Print(StringFormat("EXP0017 Phase06 historical visual backfill stopped at visual draw cap: cap=%d drawn=%d",m_visual_config.max_historical_visual_draws,m_last_backfill_drawn_count));
      }
   }

public:
   void Init(SCGTTimeConfig &time_config,SCGVVisualLedgerConfig &visual_config,bool &enabled[],const bool show_panel,const bool print_on_new_closed_candle)
   {
      m_time_config=time_config;
      m_visual_config=visual_config;
      if(m_visual_config.confirmation_timeframe==PERIOD_CURRENT)
         m_visual_config.confirmation_timeframe=(ENUM_TIMEFRAMES)_Period;
      m_show_panel=show_panel;
      m_print_on_new_closed_candle=print_on_new_closed_candle;
      m_last_closed_candle_key=-1;
      m_historical_backfill_done=false;
      m_last_backfill_observation_count=0;
      m_last_backfill_drawn_count=0;
      m_last_backfill_ledger_count=0;

      BuildConfirmationConfig();
      InitRegistry(enabled);
      m_time.Configure(m_time_config);
      m_confirmation_field.Configure(m_confirmation_config);
      m_drawing.Configure(m_visual_config);
      m_ledger.Configure(m_visual_config);

      if(m_visual_config.clear_objects_on_init)
         m_drawing.ClearPhaseObjects();
   }

   bool Pulse()
   {
      RunHistoricalVisualBackfill();

      datetime live_broker_now=TimeCurrent();
      datetime observation_broker=LastClosedCandleCloseBroker();
      bool new_closed_candle=IsNewClosedCandle(observation_broker);

      int drawn=0;
      int ledger=0;
      ProcessObservation(observation_broker,(new_closed_candle && m_visual_config.enable_ledger),true,(m_print_on_new_closed_candle && new_closed_candle),live_broker_now,drawn,ledger);
      return true;
   }

   void Clear()
   {
      Comment("");
      if(m_visual_config.clear_objects_on_deinit)
         m_drawing.ClearPhaseObjects();
   }
};

#endif
