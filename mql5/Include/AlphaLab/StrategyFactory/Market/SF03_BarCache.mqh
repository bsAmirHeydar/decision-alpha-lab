#ifndef __SF03_BAR_CACHE_MQH__
#define __SF03_BAR_CACHE_MQH__
#include "SF03_MarketTypes.mqh"

class CSF03BarSeries
{
private:
   string m_symbol;
   int m_timeframe_seconds;
   int m_capacity;
   SF01_BarRecord m_bars[];
   bool m_has_gap;
   long m_generation;
public:
   CSF03BarSeries(void)
   {
      m_symbol="";
      m_timeframe_seconds=0;
      m_capacity=2048;
      m_has_gap=false;
      m_generation=0;
   }
   bool Configure(const string symbol,const int timeframe_seconds,const int capacity,string &error)
   {
      if(!SF01_IsSafeTerminalSymbol(symbol)){ error="invalid series symbol"; return false; }
      if(timeframe_seconds<=0 || capacity<2){ error="invalid series config"; return false; }
      m_symbol=symbol;
      m_timeframe_seconds=timeframe_seconds;
      m_capacity=capacity;
      error="";
      return true;
   }
   string Symbol(void) const { return m_symbol; }
   int TimeframeSeconds(void) const { return m_timeframe_seconds; }
   bool HasGap(void) const { return m_has_gap; }
   long Generation(void) const { return m_generation; }
   int Count(void) const { return ArraySize(m_bars); }

   ENUM_SF03_BAR_UPDATE_RESULT Upsert(const SF01_BarRecord &bar,string &error)
   {
      if(bar.symbol!=m_symbol || bar.timeframe_seconds!=m_timeframe_seconds)
      { error="bar key mismatch"; return SF03_BAR_REJECTED; }
      if(!SF01_ValidateBarRecord(bar,error)) return SF03_BAR_REJECTED;
      const int count=ArraySize(m_bars);
      if(count>0)
      {
         const SF01_BarRecord last=m_bars[count-1];
         if(bar.open_time.utc_epoch_milliseconds<last.open_time.utc_epoch_milliseconds)
         { error="out-of-order bar"; return SF03_BAR_REJECTED; }
         if(bar.open_time.utc_epoch_milliseconds==last.open_time.utc_epoch_milliseconds)
         {
            if(SF01_BarCanonicalIdentity(bar)==SF01_BarCanonicalIdentity(last) &&
               bar.open_price==last.open_price && bar.high_price==last.high_price &&
               bar.low_price==last.low_price && bar.close_price==last.close_price &&
               bar.tick_volume==last.tick_volume)
            { error=""; return SF03_BAR_DUPLICATE; }
            m_bars[count-1]=bar;
            m_generation++;
            error="";
            return SF03_BAR_REPLACED;
         }
         const long expected=last.open_time.utc_epoch_milliseconds+
                             ((long)m_timeframe_seconds*1000L);
         if(bar.open_time.utc_epoch_milliseconds>expected) m_has_gap=true;
      }
      int target=count;
      if(count>=m_capacity)
      {
         for(int i=1;i<count;i++) m_bars[i-1]=m_bars[i];
         target=count-1;
      }
      else ArrayResize(m_bars,count+1);
      m_bars[target]=bar;
      m_generation++;
      error="";
      return m_has_gap?SF03_BAR_GAP_INSERTED:SF03_BAR_INSERTED;
   }

   bool Latest(SF01_BarRecord &bar,string &error) const
   {
      const int n=ArraySize(m_bars);
      if(n<=0){ error="series empty"; return false; }
      bar=m_bars[n-1];
      error="";
      return true;
   }

   int CopyRecent(const int requested,SF01_BarRecord &out[]) const
   {
      const int n=ArraySize(m_bars);
      int take=requested;
      if(take<0) take=0;
      if(take>n) take=n;
      ArrayResize(out,take);
      const int start=n-take;
      for(int i=0;i<take;i++) out[i]=m_bars[start+i];
      return take;
   }
};

class CSF03BarCache
{
private:
   CSF03BarSeries *m_series[];
   int Find(const string symbol,const int timeframe_seconds) const
   {
      for(int i=0;i<ArraySize(m_series);i++)
      {
         if(CheckPointer(m_series[i])==POINTER_INVALID) continue;
         if(m_series[i].Symbol()==symbol && m_series[i].TimeframeSeconds()==timeframe_seconds) return i;
      }
      return -1;
   }
public:
   ~CSF03BarCache(void){ Clear(); }
   void Clear(void)
   {
      for(int i=0;i<ArraySize(m_series);i++)
         if(CheckPointer(m_series[i])!=POINTER_INVALID) delete m_series[i];
      ArrayResize(m_series,0);
   }
   bool Ensure(const string symbol,const int timeframe_seconds,const int capacity,string &error)
   {
      if(Find(symbol,timeframe_seconds)>=0){ error=""; return true; }
      CSF03BarSeries *series=new CSF03BarSeries();
      if(CheckPointer(series)==POINTER_INVALID){ error="allocation failed"; return false; }
      if(!series.Configure(symbol,timeframe_seconds,capacity,error))
      { delete series; return false; }
      const int n=ArraySize(m_series);
      ArrayResize(m_series,n+1);
      m_series[n]=series;
      error="";
      return true;
   }
   ENUM_SF03_BAR_UPDATE_RESULT Upsert(const SF01_BarRecord &bar,string &error)
   {
      int index=Find(bar.symbol,bar.timeframe_seconds);
      if(index<0)
      {
         if(!Ensure(bar.symbol,bar.timeframe_seconds,2048,error)) return SF03_BAR_REJECTED;
         index=Find(bar.symbol,bar.timeframe_seconds);
      }
      return m_series[index].Upsert(bar,error);
   }
   bool Latest(const string symbol,const int timeframe_seconds,SF01_BarRecord &bar,string &error) const
   {
      const int index=Find(symbol,timeframe_seconds);
      if(index<0){ error="series not registered"; return false; }
      return m_series[index].Latest(bar,error);
   }
   bool HasGap(const string symbol,const int timeframe_seconds) const
   {
      const int index=Find(symbol,timeframe_seconds);
      return index>=0 && m_series[index].HasGap();
   }
   long Generation(const string symbol,const int timeframe_seconds) const
   {
      const int index=Find(symbol,timeframe_seconds);
      return index<0?0:m_series[index].Generation();
   }
   int CopyRecent(const string symbol,const int timeframe_seconds,const int requested,SF01_BarRecord &out[]) const
   {
      const int index=Find(symbol,timeframe_seconds);
      if(index<0){ ArrayResize(out,0); return 0; }
      return m_series[index].CopyRecent(requested,out);
   }
};
#endif
