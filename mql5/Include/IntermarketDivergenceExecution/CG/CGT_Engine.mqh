#ifndef __CGT_ENGINE_MQH__
#define __CGT_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGT_Display.mqh>

class CCGT_Engine
{
private:
   SCGTGroupDef    m_groups[CGT_GROUP_COUNT];
   SCGTTimeConfig  m_config;
   CCGT_TimeAnatomy m_time;
   CCGT_Display     m_display;
   bool             m_show_panel;
   bool             m_print_on_new_minute;
   long             m_last_minute_key;

   void SetGroup(const int index,const ECGTGroupId id,const string name,const int minutes,const bool enabled)
   {
      m_groups[index].id=id;
      m_groups[index].name=name;
      m_groups[index].minutes=minutes;
      m_groups[index].enabled=enabled;
   }

public:
   void Init(SCGTTimeConfig &config,bool &enabled[],const bool show_panel,const bool print_on_new_minute)
   {
      m_config=config;
      m_time.Configure(m_config);
      m_show_panel=show_panel;
      m_print_on_new_minute=print_on_new_minute;
      m_last_minute_key=-1;

      SetGroup(CGT_CG3M,   CGT_CG3M,   "cg_3m",   3,   enabled[CGT_CG3M]);
      SetGroup(CGT_CG5M,   CGT_CG5M,   "cg_5m",   5,   enabled[CGT_CG5M]);
      SetGroup(CGT_CG9M,   CGT_CG9M,   "cg_9m",   9,   enabled[CGT_CG9M]);
      SetGroup(CGT_CG10M,  CGT_CG10M,  "cg_10m",  10,  enabled[CGT_CG10M]);
      SetGroup(CGT_CG15M,  CGT_CG15M,  "cg_15m",  15,  enabled[CGT_CG15M]);
      SetGroup(CGT_CG18M,  CGT_CG18M,  "cg_18m",  18,  enabled[CGT_CG18M]);
      SetGroup(CGT_CG20M,  CGT_CG20M,  "cg_20m",  20,  enabled[CGT_CG20M]);
      SetGroup(CGT_CG24M,  CGT_CG24M,  "cg_24m",  24,  enabled[CGT_CG24M]);
      SetGroup(CGT_CG30M,  CGT_CG30M,  "cg_30m",  30,  enabled[CGT_CG30M]);
      SetGroup(CGT_CG40M,  CGT_CG40M,  "cg_40m",  40,  enabled[CGT_CG40M]);
      SetGroup(CGT_CG45M,  CGT_CG45M,  "cg_45m",  45,  enabled[CGT_CG45M]);
      SetGroup(CGT_CG60M,  CGT_CG60M,  "cg_60m",  60,  enabled[CGT_CG60M]);
      SetGroup(CGT_CG72M,  CGT_CG72M,  "cg_72m",  72,  enabled[CGT_CG72M]);
      SetGroup(CGT_CG90M,  CGT_CG90M,  "cg_90m",  90,  enabled[CGT_CG90M]);
      SetGroup(CGT_CG120M, CGT_CG120M, "cg_120m", 120, enabled[CGT_CG120M]);
      SetGroup(CGT_CG150M, CGT_CG150M, "cg_150m", 150, enabled[CGT_CG150M]);
      SetGroup(CGT_CG180M, CGT_CG180M, "cg_180m", 180, enabled[CGT_CG180M]);
      SetGroup(CGT_CG240M, CGT_CG240M, "cg_240m", 240, enabled[CGT_CG240M]);
      SetGroup(CGT_CG300M, CGT_CG300M, "cg_300m", 300, enabled[CGT_CG300M]);
      SetGroup(CGT_CG360M, CGT_CG360M, "cg_360m", 360, enabled[CGT_CG360M]);
      SetGroup(CGT_CG720M, CGT_CG720M, "cg_720m", 720, enabled[CGT_CG720M]);
   }

   bool Pulse()
   {
      SCGTTimeSnapshot time_snapshot;
      m_time.BuildTimeSnapshot(TimeCurrent(),time_snapshot);

      SCGTCycleSnapshot cycles[];
      ArrayResize(cycles,CGT_GROUP_COUNT);
      int count=0;

      for(int i=0;i<CGT_GROUP_COUNT;i++)
      {
         if(!m_groups[i].enabled)
            continue;
         SCGTCycleSnapshot cycle;
         m_time.BuildCycleSnapshot(time_snapshot,m_groups[i],cycle);
         cycles[count]=cycle;
         count++;
      }
      ArrayResize(cycles,count);

      if(m_show_panel)
         Comment(m_display.BuildPanel(time_snapshot,cycles,m_time));

      if(m_print_on_new_minute)
      {
         long minute_key=(long)(time_snapshot.broker_now/60);
         if(minute_key!=m_last_minute_key)
         {
            m_last_minute_key=minute_key;
            Print(m_display.BuildPrintLine(time_snapshot,cycles,m_time));
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
