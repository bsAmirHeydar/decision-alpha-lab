#ifndef __EXP0018_DAYE_RENDER_PROJECTION_MQH__
#define __EXP0018_DAYE_RENDER_PROJECTION_MQH__

#include <DayeTrader/EXP0018/DAYE_RenderIdentity.mqh>

int DAYE_FindPairedPeriodForRender(const DAYE_PairedPeriodSnapshot &periods[],const string period_instance_id)
{
   for(int i=ArraySize(periods)-1;i>=0;i--)
      if(periods[i].period_instance_id==period_instance_id) return i;
   return -1;
}

bool DAYE_SelectHunterSymbolPeriod(const DAYE_PairedPeriodSnapshot &period,
                                   const string hunter_canonical_symbol,
                                   DAYE_SymbolPeriodSnapshot &snapshot)
{
   if(period.symbol_a.canonical_symbol==hunter_canonical_symbol)
   {
      snapshot=period.symbol_a;
      return true;
   }
   if(period.symbol_b.canonical_symbol==hunter_canonical_symbol)
   {
      snapshot=period.symbol_b;
      return true;
   }
   return false;
}

bool DAYE_ResolveReferenceAnchor(const DAYE_ReferenceUseRecord &use,
                                 const DAYE_PairedPeriodSnapshot &periods[],
                                 const DAYE_ExtremeAnchorPolicy policy,
                                 datetime &anchor_time_utc,
                                 double &resolved_extreme_price,
                                 string &source_bar_id,
                                 string &reason_code)
{
   anchor_time_utc=0;
   resolved_extreme_price=0.0;
   source_bar_id="";
   reason_code="";
   int index=DAYE_FindPairedPeriodForRender(periods,use.reference_period_instance_id);
   if(index<0)
   {
      reason_code="reference_period_not_present_in_current_source_lookback";
      return false;
   }
   DAYE_SymbolPeriodSnapshot snapshot;
   if(!DAYE_SelectHunterSymbolPeriod(periods[index],use.hunter_canonical_symbol,snapshot))
   {
      reason_code="hunter_symbol_not_found_inside_reference_period";
      return false;
   }
   if(snapshot.completeness!=DAYE_PERIOD_COMPLETENESS_COMPLETE)
   {
      reason_code="reference_period_is_not_complete";
      return false;
   }

   if(use.side==DAYE_HUNT_SIDE_HIGH)
   {
      resolved_extreme_price=snapshot.high;
      if(policy==DAYE_EXTREME_ANCHOR_LAST_OCCURRENCE)
      {
         anchor_time_utc=snapshot.high_last_time_utc;
         source_bar_id=snapshot.high_last_source_bar_id;
      }
      else
      {
         anchor_time_utc=snapshot.high_first_time_utc;
         source_bar_id=snapshot.high_first_source_bar_id;
      }
   }
   else if(use.side==DAYE_HUNT_SIDE_LOW)
   {
      resolved_extreme_price=snapshot.low;
      if(policy==DAYE_EXTREME_ANCHOR_LAST_OCCURRENCE)
      {
         anchor_time_utc=snapshot.low_last_time_utc;
         source_bar_id=snapshot.low_last_source_bar_id;
      }
      else
      {
         anchor_time_utc=snapshot.low_first_time_utc;
         source_bar_id=snapshot.low_first_source_bar_id;
      }
   }
   else
   {
      reason_code="unknown_hunt_side";
      return false;
   }

   if(anchor_time_utc<=0 || resolved_extreme_price<=0.0 || source_bar_id=="")
   {
      reason_code="reference_extreme_time_or_source_bar_id_unavailable";
      return false;
   }
   return true;
}

bool DAYE_BuildRenderGeometry(const DAYE_ReferenceUseRecord &use,
                              const DAYE_PairedPeriodSnapshot &periods[],
                              const DAYE_RenderConfig &config,
                              const DAYE_TimeConfig &time_config,
                              DAYE_RenderGeometry &geometry)
{
   ZeroMemory(geometry);
   geometry.side=use.side;
   geometry.extreme_anchor_policy=config.extreme_anchor_policy;

   string reason="";
   double resolved_extreme_price=0.0;
   if(!DAYE_ResolveReferenceAnchor(use,periods,config.extreme_anchor_policy,
                                   geometry.reference_time_utc,resolved_extreme_price,geometry.reference_source_bar_id,reason))
   {
      geometry.reason_code=reason;
      return false;
   }
   geometry.confirmation_time_utc=use.host_bar_open_utc;
   geometry.reference_price=use.hunter_reference_price;
   double price_tolerance=MathMax(MathAbs(resolved_extreme_price),MathAbs(use.hunter_reference_price))*1.0e-10;
   if(price_tolerance<=0.0) price_tolerance=1.0e-10;
   if(MathAbs(resolved_extreme_price-use.hunter_reference_price)>price_tolerance)
   {
      geometry.reason_code="hunter_reference_price_mismatch_period_extreme";
      return false;
   }
   geometry.confirmation_price=use.confirmation_endpoint_price;

   bool replay_safe_a=true,replay_safe_b=true;
   if(!DAYE_UtcToBrokerRenderTime(geometry.reference_time_utc,time_config,geometry.reference_time_broker,replay_safe_a,reason))
   {
      geometry.reason_code="reference_utc_to_broker_failed:"+reason;
      return false;
   }
   if(!DAYE_UtcToBrokerRenderTime(geometry.confirmation_time_utc,time_config,geometry.confirmation_time_broker,replay_safe_b,reason))
   {
      geometry.reason_code="confirmation_utc_to_broker_failed:"+reason;
      return false;
   }

   if(geometry.reference_time_broker<=0 || geometry.confirmation_time_broker<=0 ||
      geometry.confirmation_time_broker<=geometry.reference_time_broker)
   {
      geometry.reason_code="render_times_not_strictly_chronological";
      return false;
   }
   if(geometry.reference_price<=0.0 || geometry.confirmation_price<=0.0)
   {
      geometry.reason_code="render_prices_must_be_positive";
      return false;
   }

   geometry.label_time_broker=(datetime)(((long)geometry.reference_time_broker+(long)geometry.confirmation_time_broker)/2);
   geometry.label_price=(geometry.reference_price+geometry.confirmation_price)/2.0;
   geometry.is_valid=true;
   geometry.reason_code="geometry_resolved_from_accepted_use_and_hunter_reference_extreme";
   return true;
}

#endif
