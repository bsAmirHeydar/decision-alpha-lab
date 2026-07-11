#ifndef __SF03_TICK_CACHE_MQH__
#define __SF03_TICK_CACHE_MQH__
#include "SF03_MarketTypes.mqh"

class CSF03TickCache
{
private:
   SF03_TickSnapshot m_items[];
   int Find(const string symbol) const
   {
      for(int i=0;i<ArraySize(m_items);i++)
         if(m_items[i].symbol==symbol) return i;
      return -1;
   }
public:
   int Count(void) const { return ArraySize(m_items); }

   bool Put(const string symbol,const MqlTick &tick,const long received_at_utc_msc,
            const long source_generation,string &error)
   {
      if(!SF01_IsSafeTerminalSymbol(symbol)){ error="invalid tick symbol"; return false; }
      if(received_at_utc_msc<0 || tick.time_msc<0){ error="negative tick time"; return false; }
      if(!MathIsValidNumber(tick.bid) || !MathIsValidNumber(tick.ask) || !MathIsValidNumber(tick.last))
      { error="non-finite tick"; return false; }
      if(tick.ask>0.0 && tick.bid>0.0 && tick.ask<tick.bid)
      { error="ask below bid"; return false; }
      int index=Find(symbol);
      if(index<0)
      {
         index=ArraySize(m_items);
         ArrayResize(m_items,index+1);
      }
      else if(m_items[index].tick.time_msc>tick.time_msc)
      { error="out-of-order tick"; return false; }
      m_items[index].symbol=symbol;
      m_items[index].tick=tick;
      m_items[index].received_at_utc_msc=received_at_utc_msc;
      m_items[index].source_generation=source_generation;
      m_items[index].quality=SF03_QUALITY_VALID;
      error="";
      return true;
   }

   bool Get(const string symbol,const long now_utc_msc,const long max_age_msc,
            SF03_TickSnapshot &out,string &error) const
   {
      const int index=Find(symbol);
      if(index<0){ error="tick not cached"; return false; }
      out=m_items[index];
      const long age=now_utc_msc-out.received_at_utc_msc;
      if(age<0){ out.quality=SF03_QUALITY_INVALID; error="tick from future"; return false; }
      if(max_age_msc>=0 && age>max_age_msc)
      { out.quality=SF03_QUALITY_STALE; error="tick stale"; return false; }
      error="";
      return true;
   }
};
#endif
