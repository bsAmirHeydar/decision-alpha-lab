#ifndef __SF09_PATH_TRACKER_MQH__
#define __SF09_PATH_TRACKER_MQH__
#include "SF09_OutcomeEnums.mqh"
#include "SF09_PriceObservation.mqh"

struct SF09_PathEvent
{
   long sequence;
   ENUM_SF09_PATH_EVENT_KIND kind;
   SF01_MarketTimestamp event_time;
   double price;
   double favorable_points;
   double adverse_points;
   string event_hash;
};

class CSF09PathTracker
{
private:
   SF09_PathEvent m_events[SF09_MAX_PATH_EVENTS];
   int m_count;
   int m_capacity;
   ENUM_SF01_DIRECTION m_direction;
   double m_entry_price;
   double m_risk_points;
   double m_mfe_points;
   double m_mae_points;
   SF01_MarketTimestamp m_mfe_time;
   SF01_MarketTimestamp m_mae_time;
   string m_path_hash;
public:
   CSF09PathTracker(void){Reset();}
   void Reset(void)
   {
      m_count=0;m_capacity=SF09_MAX_PATH_EVENTS;m_direction=SF01_DIRECTION_NONE;m_entry_price=0.0;m_risk_points=0.0;
      m_mfe_points=0.0;m_mae_points=0.0;m_path_hash="path_empty";
   }
   bool Initialize(const ENUM_SF01_DIRECTION direction,const double entry_price,const double risk_points,const int capacity,string &error)
   {
      Reset();
      if((direction!=SF01_DIRECTION_LONG&&direction!=SF01_DIRECTION_SHORT)||entry_price<=0.0||risk_points<=0.0||capacity<=0||capacity>SF09_MAX_PATH_EVENTS)
      {error="invalid path tracker initialization";return false;}
      m_direction=direction;m_entry_price=entry_price;m_risk_points=risk_points;m_capacity=capacity;error="";return true;
   }
   bool Append(const ENUM_SF09_PATH_EVENT_KIND kind,const SF01_MarketTimestamp &time,const double price,const double favorable,const double adverse,string &error)
   {
      if(m_count>=m_capacity){error="path event capacity reached";return false;}
      SF09_PathEvent e;e.sequence=m_count;e.kind=kind;e.event_time=time;e.price=price;e.favorable_points=favorable;e.adverse_points=adverse;
      e.event_hash=SF01_StableId("pevt",m_path_hash+"|"+IntegerToString(e.sequence)+"|"+IntegerToString((int)kind)+"|"+
                                      IntegerToString(time.utc_epoch_milliseconds)+"|"+SF01_CanonicalDouble(price)+"|"+
                                      SF01_CanonicalDouble(favorable)+"|"+SF01_CanonicalDouble(adverse));
      m_events[m_count]=e;m_count++;m_path_hash=e.event_hash;error="";return true;
   }
   bool Update(const SF09_PriceObservation &o,string &error)
   {
      double favorable=0.0,adverse=0.0;
      if(m_direction==SF01_DIRECTION_LONG){favorable=MathMax(0.0,o.high_price-m_entry_price);adverse=MathMax(0.0,m_entry_price-o.low_price);}
      else {favorable=MathMax(0.0,m_entry_price-o.low_price);adverse=MathMax(0.0,o.high_price-m_entry_price);}
      if(favorable>m_mfe_points){m_mfe_points=favorable;m_mfe_time=o.observed_at;if(!Append(SF09_PATH_FAVORABLE_EXTREME,o.observed_at,o.close_price,favorable,adverse,error))return false;}
      if(adverse>m_mae_points){m_mae_points=adverse;m_mae_time=o.observed_at;if(!Append(SF09_PATH_ADVERSE_EXTREME,o.observed_at,o.close_price,favorable,adverse,error))return false;}
      error="";return true;
   }
   double MFEPoints(void) const{return m_mfe_points;}
   double MAEPoints(void) const{return m_mae_points;}
   double MFER(void) const{return (m_risk_points>0.0)?m_mfe_points/m_risk_points:0.0;}
   double MAER(void) const{return (m_risk_points>0.0)?m_mae_points/m_risk_points:0.0;}
   int Count(void) const{return m_count;}
   string PathHash(void) const{return m_path_hash;}
};

#endif
