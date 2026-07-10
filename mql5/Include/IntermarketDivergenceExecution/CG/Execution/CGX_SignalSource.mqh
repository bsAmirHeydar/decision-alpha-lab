#ifndef __CGX_SIGNAL_SOURCE_MQH__
#define __CGX_SIGNAL_SOURCE_MQH__

#include <IntermarketDivergenceExecution/CG/CGT_Time.mqh>
#include <IntermarketDivergenceExecution/CG/Execution/CGX_Types.mqh>

class CCGX_SignalSource
{
private:
   SCGTTimeConfig         m_time_config;
   SCGCConfirmationConfig m_confirmation_config;
   CCGT_TimeAnatomy       m_time;
   CCGC_ConfirmationField m_confirmation_field;
   SCGTGroupDef           m_groups[CGT_GROUP_COUNT];

   bool HasM1HistoryBounds(const string symbol,const datetime start_broker,const datetime end_broker_exclusive)
   {
      if(symbol=="" || end_broker_exclusive<=start_broker)
         return false;
      if(!SymbolSelect(symbol,true))
         return false;

      MqlRates rates[];
      ArraySetAsSeries(rates,false);
      int copied=CopyRates(symbol,PERIOD_M1,start_broker,end_broker_exclusive-1,rates);
      if(copied<=0)
         return false;
      return (rates[0].time==start_broker && rates[copied-1].time>=end_broker_exclusive-60);
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
   void Configure(SCGTTimeConfig &time_config,SCGCConfirmationConfig &confirmation_config,bool &enabled[])
   {
      m_time_config=time_config;
      m_confirmation_config=confirmation_config;
      if(m_confirmation_config.confirmation_timeframe==PERIOD_CURRENT)
         m_confirmation_config.confirmation_timeframe=(ENUM_TIMEFRAMES)_Period;
      InitRegistry(enabled);
      m_time.Configure(m_time_config);
      m_confirmation_field.Configure(m_confirmation_config);
   }

   ENUM_TIMEFRAMES ConfirmationTimeframe()
   {
      return m_confirmation_config.confirmation_timeframe;
   }

   string ClockSymbol()
   {
      return m_confirmation_config.symbol_a;
   }

   datetime LastClosedCandleCloseBroker()
   {
      ENUM_TIMEFRAMES tf=m_confirmation_config.confirmation_timeframe;
      int seconds=PeriodSeconds(tf);
      if(seconds<=0)
         return 0;

      datetime open_time=iTime(m_confirmation_config.symbol_a,tf,1);
      if(open_time<=0)
         open_time=iTime(m_confirmation_config.symbol_b,tf,1);
      if(open_time<=0)
         return 0;

      datetime close_time=(datetime)(open_time+seconds);
      datetime now=TimeCurrent();
      if(close_time>now)
         return 0;
      return close_time;
   }

   bool CollectCurrentTradingDayClosedBoundaries(const datetime latest_closed_broker,datetime &boundaries[])
   {
      ArrayResize(boundaries,0);
      if(latest_closed_broker<=0)
         return false;

      SCGTTimeSnapshot snapshot;
      m_time.BuildTimeSnapshot(latest_closed_broker,snapshot);
      datetime start_broker=snapshot.trading_day_start_ny
                            -(snapshot.new_york_utc_offset_hours*3600)
                            +(m_time_config.broker_utc_offset_hours*3600);
      ENUM_TIMEFRAMES tf=m_confirmation_config.confirmation_timeframe;
      int seconds=PeriodSeconds(tf);
      if(seconds<=0 || latest_closed_broker<=start_broker)
         return false;

      if(m_confirmation_config.require_m1_history)
      {
         if(!HasM1HistoryBounds(m_confirmation_config.symbol_a,start_broker,latest_closed_broker) ||
            !HasM1HistoryBounds(m_confirmation_config.symbol_b,start_broker,latest_closed_broker))
            return false;
      }

      MqlRates rates[];
      ArraySetAsSeries(rates,false);
      int copied=CopyRates(m_confirmation_config.symbol_a,tf,start_broker,latest_closed_broker-1,rates);
      if(copied<=0)
         return false;

      for(int i=0;i<copied;i++)
      {
         datetime close_time=(datetime)(rates[i].time+seconds);
         if(close_time<=start_broker || close_time>latest_closed_broker)
            continue;
         int n=ArraySize(boundaries);
         if(n>0 && boundaries[n-1]==close_time)
            continue;
         ArrayResize(boundaries,n+1);
         boundaries[n]=close_time;
      }
      return (ArraySize(boundaries)>0);
   }

   int BuildConfirmedSignals(const datetime observation_broker,SCGCFinalSignal &signals[],int &group_indices[],datetime &trading_day_start_ny)
   {
      ArrayResize(signals,0);
      ArrayResize(group_indices,0);
      trading_day_start_ny=0;
      if(observation_broker<=0)
         return 0;

      SCGTTimeSnapshot time_snapshot;
      m_time.BuildTimeSnapshot(observation_broker,time_snapshot);
      trading_day_start_ny=time_snapshot.trading_day_start_ny;
      if(!time_snapshot.inside_trading_day)
         return 0;

      for(int i=0;i<CGT_GROUP_COUNT;i++)
      {
         if(!m_groups[i].enabled)
            continue;

         SCGTCycleSnapshot cycle;
         m_time.BuildCycleSnapshot(time_snapshot,m_groups[i],cycle);

         SCGCFinalSignal group_signals[];
         SCGCGroupConfirmationState state;
         int count=m_confirmation_field.BuildFinalSignalsForGroup(time_snapshot,cycle,group_signals,state);
         for(int j=0;j<count;j++)
         {
            if(group_signals[j].status!=CGC_STATUS_CONFIRMED_TRADEABLE)
               continue;
            int n=ArraySize(signals);
            ArrayResize(signals,n+1);
            ArrayResize(group_indices,n+1);
            signals[n]=group_signals[j];
            group_indices[n]=i;
         }
      }
      return ArraySize(signals);
   }
};

#endif
