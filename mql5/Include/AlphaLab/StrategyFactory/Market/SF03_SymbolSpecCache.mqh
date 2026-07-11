#ifndef __SF03_SYMBOL_SPEC_CACHE_MQH__
#define __SF03_SYMBOL_SPEC_CACHE_MQH__
#include "ISF03_MarketSource.mqh"
#include "../Ports/ISF02_SymbolSpecPort.mqh"

class CSF03SymbolSpecCache : public ISF02SymbolSpecPort
{
private:
   ISF03MarketSource *m_source;
   SF03_SymbolSpecSnapshot m_items[];
   bool m_initialized;
   bool m_started;
   long m_generation;

   int Find(const string symbol) const
   {
      for(int i=0;i<ArraySize(m_items);i++)
         if(m_items[i].symbol==symbol) return i;
      return -1;
   }

   bool EqualMaterial(const SF03_SymbolSpecSnapshot &a,const SF03_SymbolSpecSnapshot &b) const
   {
      return a.digits==b.digits && a.point==b.point && a.tick_size==b.tick_size &&
             a.tick_value==b.tick_value && a.contract_size==b.contract_size &&
             a.volume_min==b.volume_min && a.volume_max==b.volume_max &&
             a.volume_step==b.volume_step && a.stops_level_points==b.stops_level_points &&
             a.freeze_level_points==b.freeze_level_points && a.filling_mode==b.filling_mode &&
             a.order_mode==b.order_mode && a.trade_mode==b.trade_mode;
   }

public:
   CSF03SymbolSpecCache(void)
   {
      m_source=NULL;
      m_initialized=false;
      m_started=false;
      m_generation=0;
   }
   void BindSource(ISF03MarketSource *value){ m_source=value; }
   string ServiceId(void) const { return "sf03.symbol_spec_cache"; }
   ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_SYMBOL_SPEC; }

   bool Initialize(const SF02_RuntimeConfig &config,string &error)
   {
      if(CheckPointer(m_source)==POINTER_INVALID){ error="source not bound"; return false; }
      m_initialized=true; error=""; return true;
   }
   bool Start(string &error)
   {
      if(!m_initialized){ error="not initialized"; return false; }
      m_started=true; error=""; return true;
   }
   void Stop(void){ m_started=false; }
   void Shutdown(void){ m_started=false; m_initialized=false; ArrayResize(m_items,0); }

   SF02_ServiceHealth Health(const long now_utc_msc) const
   {
      SF02_ServiceHealth out;
      out.service_id=ServiceId();
      out.service_kind=ServiceKind();
      out.observed_at_utc_msc=now_utc_msc;
      out.status=(m_initialized && m_started)?SF02_HEALTH_HEALTHY:SF02_HEALTH_DEGRADED;
      out.detail=(m_initialized && m_started)?"running":"not running";
      return out;
   }

   bool Refresh(const string symbol,string &error)
   {
      SF03_SymbolSpecSnapshot incoming;
      if(!m_source.ReadSymbolSpec(symbol,incoming,error)) return false;
      int index=Find(symbol);
      if(index<0)
      {
         index=ArraySize(m_items);
         ArrayResize(m_items,index+1);
         m_generation++;
         incoming.specification_generation=m_generation;
         m_items[index]=incoming;
      }
      else if(!EqualMaterial(m_items[index],incoming))
      {
         m_generation++;
         incoming.specification_generation=m_generation;
         m_items[index]=incoming;
      }
      else
      {
         incoming.specification_generation=m_items[index].specification_generation;
         m_items[index]=incoming;
      }
      error="";
      return true;
   }

   bool GetSnapshot(const string symbol,SF03_SymbolSpecSnapshot &spec,string &error)
   {
      int index=Find(symbol);
      if(index<0)
      {
         if(!Refresh(symbol,error)) return false;
         index=Find(symbol);
      }
      spec=m_items[index];
      error="";
      return true;
   }

   bool Get(const string symbol,SF02_SymbolSpec &spec,string &error)
   {
      SF03_SymbolSpecSnapshot full;
      if(!GetSnapshot(symbol,full,error)) return false;
      spec.symbol=full.symbol;
      spec.point=full.point;
      spec.tick_size=full.tick_size;
      spec.tick_value=full.tick_value;
      spec.volume_min=full.volume_min;
      spec.volume_max=full.volume_max;
      spec.volume_step=full.volume_step;
      spec.stops_level_points=full.stops_level_points;
      spec.freeze_level_points=full.freeze_level_points;
      spec.specification_generation=full.specification_generation;
      error="";
      return true;
   }
};
#endif
