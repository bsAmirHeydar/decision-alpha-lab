#ifndef __CGC_ENGINE_MQH__
#define __CGC_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGT_Time.mqh>
#include <IntermarketDivergenceExecution/CG/CGC_Display.mqh>

class CCGC_Engine
{
private:
   SCGTTimeConfig           m_time_config;
   SCGCConfirmationConfig   m_confirmation_config;
   CCGT_TimeAnatomy        m_time;
   CCGC_ConfirmationField   m_confirmation_field;
   CCGC_Display             m_display;
   SCGTGroupDef            m_groups[CGT_GROUP_COUNT];
   bool                     m_show_panel;
   bool                     m_print_on_new_closed_candle;
   long                     m_last_closed_candle_key;

   ENUM_TIMEFRAMES ResolveTimeframe()
   {
      if(m_confirmation_config.confirmation_timeframe==PERIOD_CURRENT)
         return (ENUM_TIMEFRAMES)_Period;
      return m_confirmation_config.confirmation_timeframe;
   }

   datetime LastClosedCandleCloseBroker()
   {
      if(!m_confirmation_config.use_last_closed_candle_boundary)
         return TimeCurrent();

      ENUM_TIMEFRAMES tf=ResolveTimeframe();
      int seconds=PeriodSeconds(tf);
      if(seconds<=0)
         seconds=PeriodSeconds((ENUM_TIMEFRAMES)_Period);
      if(seconds<=0)
         seconds=60;

      datetime open_time=iTime(m_confirmation_config.symbol_a,tf,1);
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

public:
   void Init(SCGTTimeConfig &time_config,SCGCConfirmationConfig &confirmation_config,bool &enabled[],const bool show_panel,const bool print_on_new_closed_candle)
   {
      m_time_config=time_config;
      m_confirmation_config=confirmation_config;
      if(m_confirmation_config.confirmation_timeframe==PERIOD_CURRENT)
         m_confirmation_config.confirmation_timeframe=(ENUM_TIMEFRAMES)_Period;
      m_show_panel=show_panel;
      m_print_on_new_closed_candle=print_on_new_closed_candle;
      m_last_closed_candle_key=-1;

      InitRegistry(enabled);
      m_time.Configure(m_time_config);
      m_confirmation_field.Configure(m_confirmation_config);
   }

   bool Pulse()
   {
      datetime live_broker_now=TimeCurrent();
      datetime observation_broker=LastClosedCandleCloseBroker();

      SCGTTimeSnapshot time_snapshot;
      m_time.BuildTimeSnapshot(observation_broker,time_snapshot);

      SCGCGroupConfirmationState states[];
      SCGCFinalSignal flat_signals[];
      int group_start[];
      int group_count[];
      ArrayResize(states,0);
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
         SCGCGroupConfirmationState state;
         int signal_count=m_confirmation_field.BuildFinalSignalsForGroup(time_snapshot,cycle,signals,state);

         int g=ArraySize(states);
         ArrayResize(states,g+1);
         ArrayResize(group_start,g+1);
         ArrayResize(group_count,g+1);
         states[g]=state;

         int start=ArraySize(flat_signals);
         group_start[g]=start;
         group_count[g]=signal_count;
         if(signal_count>0)
         {
            ArrayResize(flat_signals,start+signal_count);
            for(int c=0;c<signal_count;c++)
               flat_signals[start+c]=signals[c];
         }
      }

      if(m_show_panel)
         Comment(m_display.BuildPanel(time_snapshot,m_confirmation_config,states,flat_signals,group_start,group_count,m_confirmation_field,live_broker_now));

      if(m_print_on_new_closed_candle)
      {
         long closed_key=(long)(observation_broker/60);
         if(closed_key!=m_last_closed_candle_key)
         {
            m_last_closed_candle_key=closed_key;
            Print(m_display.BuildPrintSummary(time_snapshot,states));
         }
      }
      return true;
   }

   void Clear()
   {
      Comment("");
   }
};

#endif
