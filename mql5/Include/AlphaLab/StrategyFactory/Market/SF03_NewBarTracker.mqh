#ifndef __SF03_NEW_BAR_TRACKER_MQH__
#define __SF03_NEW_BAR_TRACKER_MQH__
#include "SF03_MarketTypes.mqh"

struct SF03_NewBarState
{
   string symbol;
   int timeframe_seconds;
   long last_open_utc_msc;
   string last_bar_id;
};

class CSF03NewBarTracker
{
private:
   SF03_NewBarState m_states[];
   int Find(const string symbol,const int timeframe_seconds) const
   {
      for(int i=0;i<ArraySize(m_states);i++)
         if(m_states[i].symbol==symbol && m_states[i].timeframe_seconds==timeframe_seconds) return i;
      return -1;
   }
public:
   bool Observe(const SF01_BarRecord &bar,bool &is_new_bar,string &error)
   {
      is_new_bar=false;
      if(!SF01_ValidateBarRecord(bar,error)) return false;
      const string id=SF01_BarId(bar);
      int index=Find(bar.symbol,bar.timeframe_seconds);
      if(index<0)
      {
         index=ArraySize(m_states);
         ArrayResize(m_states,index+1);
         m_states[index].symbol=bar.symbol;
         m_states[index].timeframe_seconds=bar.timeframe_seconds;
         m_states[index].last_open_utc_msc=bar.open_time.utc_epoch_milliseconds;
         m_states[index].last_bar_id=id;
         is_new_bar=true;
         error="";
         return true;
      }
      if(bar.open_time.utc_epoch_milliseconds<m_states[index].last_open_utc_msc)
      { error="historical regression"; return false; }
      if(id==m_states[index].last_bar_id){ error=""; return true; }
      if(bar.open_time.utc_epoch_milliseconds==m_states[index].last_open_utc_msc)
      {
         m_states[index].last_bar_id=id;
         error="";
         return true;
      }
      m_states[index].last_open_utc_msc=bar.open_time.utc_epoch_milliseconds;
      m_states[index].last_bar_id=id;
      is_new_bar=true;
      error="";
      return true;
   }
};
#endif
