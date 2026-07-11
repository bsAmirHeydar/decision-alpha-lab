#ifndef __SF10_SELECTED_PASS_COLLECTOR_MQH__
#define __SF10_SELECTED_PASS_COLLECTOR_MQH__
#include "SF10_OptimizationFrames.mqh"

struct SF10_SelectedPassPolicy
{
   int maximum_passes;
   double minimum_score;
   double minimum_expectancy_r;
   long minimum_unique_events;
};

class CSF10SelectedPassCollector
{
private:
   SF10_PassSummary m_items[];
   SF10_SelectedPassPolicy m_policy;
public:
   void Configure(const SF10_SelectedPassPolicy &policy){m_policy=policy;ArrayResize(m_items,0);}
   int Count(void) const{return ArraySize(m_items);}
   SF10_PassSummary Item(const int index) const{return m_items[index];}
   bool Consider(const SF10_PassSummary &s)
   {
      if(s.status!=SF10_PASS_VALID||s.objective_score<m_policy.minimum_score||
         s.metrics.expectancy_r<m_policy.minimum_expectancy_r||s.metrics.unique_event_count<m_policy.minimum_unique_events)return false;
      int n=ArraySize(m_items);ArrayResize(m_items,n+1);m_items[n]=s;
      for(int i=n;i>0;i--)
      {
         if(m_items[i].objective_score<=m_items[i-1].objective_score)break;
         SF10_PassSummary tmp=m_items[i-1];m_items[i-1]=m_items[i];m_items[i]=tmp;
      }
      if(ArraySize(m_items)>m_policy.maximum_passes)ArrayResize(m_items,m_policy.maximum_passes);
      return true;
   }
   bool ExportCsv(const string filename,string &error) const
   {
      const int h=FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI,',');
      if(h==INVALID_HANDLE){error="cannot open selected-pass CSV: "+IntegerToString(GetLastError());return false;}
      FileWrite(h,"rank","public_id","score","status","unique_events","filled","fill_rate","expectancy_r","profit_factor","max_drawdown_r","best_trade_share","summary_hash");
      for(int i=0;i<ArraySize(m_items);i++)
      {
         const SF10_PassSummary s=m_items[i];
         FileWrite(h,i+1,s.public_id,s.objective_score,SF10_PassStatusName(s.status),s.metrics.unique_event_count,s.metrics.filled_count,
                   s.metrics.fill_rate,s.metrics.expectancy_r,s.metrics.profit_factor,s.metrics.maximum_drawdown_r,s.metrics.best_trade_share,s.summary_hash);
      }
      FileClose(h);error="";return true;
   }
};
#endif
