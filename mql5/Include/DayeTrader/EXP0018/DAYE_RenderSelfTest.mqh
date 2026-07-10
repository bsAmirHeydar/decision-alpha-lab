#ifndef __EXP0018_DAYE_RENDER_SELF_TEST_MQH__
#define __EXP0018_DAYE_RENDER_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_RenderAudit.mqh>

void DAYE_BuildP08TestPeriod(DAYE_PairedPeriodSnapshot &period)
{
   ZeroMemory(period);
   period.schema_version=DAYE_PERIOD_AGG_SCHEMA_VERSION;
   period.period_instance_id="REF-1";
   period.completeness=DAYE_PERIOD_COMPLETENESS_COMPLETE;
   period.symbol_a.canonical_symbol="SPX";
   period.symbol_a.completeness=DAYE_PERIOD_COMPLETENESS_COMPLETE;
   period.symbol_a.high=110.0; period.symbol_a.low=90.0;
   period.symbol_a.high_first_time_utc=1000; period.symbol_a.high_last_time_utc=1060;
   period.symbol_a.low_first_time_utc=1120; period.symbol_a.low_last_time_utc=1180;
   period.symbol_a.high_first_source_bar_id="SPX-H-FIRST"; period.symbol_a.high_last_source_bar_id="SPX-H-LAST";
   period.symbol_a.low_first_source_bar_id="SPX-L-FIRST"; period.symbol_a.low_last_source_bar_id="SPX-L-LAST";
   period.symbol_b.canonical_symbol="NDX";
   period.symbol_b.completeness=DAYE_PERIOD_COMPLETENESS_COMPLETE;
   period.symbol_b.high=210.0; period.symbol_b.low=190.0;
   period.symbol_b.high_first_time_utc=1000; period.symbol_b.high_last_time_utc=1060;
   period.symbol_b.low_first_time_utc=1120; period.symbol_b.low_last_time_utc=1180;
   period.symbol_b.high_first_source_bar_id="NDX-H-FIRST"; period.symbol_b.high_last_source_bar_id="NDX-H-LAST";
   period.symbol_b.low_first_source_bar_id="NDX-L-FIRST"; period.symbol_b.low_last_source_bar_id="NDX-L-LAST";
}

void DAYE_BuildP08TestUse(const DAYE_HuntSide side,DAYE_ReferenceUseRecord &use)
{
   ZeroMemory(use);
   use.schema_version=DAYE_LIFECYCLE_SCHEMA_VERSION;
   use.status=DAYE_USE_STATUS_ACCEPTED; use.is_accepted=true; use.is_historical_immutable=true;
   use.use_id="USE-1"; use.reference_id="REF-ID"; use.relationship_id="DAYE_LN"; use.source_alias="LN";
   use.is_major=true; use.chart_label="LN"; use.side=side;
   use.hunter_broker_symbol="SPXUSD"; use.hunter_canonical_symbol="SPX";
   use.protected_broker_symbol="NDXUSD"; use.protected_canonical_symbol="NDX";
   use.reference_period_instance_id="REF-1"; use.host_bar_open_utc=1300; use.host_bar_close_utc=1360;
   use.hunter_reference_price=(side==DAYE_HUNT_SIDE_HIGH)?110.0:90.0;
   use.confirmation_endpoint_price=(side==DAYE_HUNT_SIDE_HIGH)?111.0:89.0;
}

bool DAYE_RunEmbeddedRenderSelfTests(void)
{
   DAYE_PairedPeriodSnapshot periods[]; ArrayResize(periods,1); DAYE_BuildP08TestPeriod(periods[0]);
   DAYE_ReferenceUseRecord use;
   datetime t=0; double extreme_price=0.0; string bar_id="",reason="";

   DAYE_BuildP08TestUse(DAYE_HUNT_SIDE_HIGH,use);
   if(!DAYE_ResolveReferenceAnchor(use,periods,DAYE_EXTREME_ANCHOR_FIRST_OCCURRENCE,t,extreme_price,bar_id,reason) || t!=1000 || extreme_price!=110.0 || bar_id!="SPX-H-FIRST") return false;
   if(!DAYE_ResolveReferenceAnchor(use,periods,DAYE_EXTREME_ANCHOR_LAST_OCCURRENCE,t,extreme_price,bar_id,reason) || t!=1060 || extreme_price!=110.0 || bar_id!="SPX-H-LAST") return false;

   DAYE_BuildP08TestUse(DAYE_HUNT_SIDE_LOW,use);
   if(!DAYE_ResolveReferenceAnchor(use,periods,DAYE_EXTREME_ANCHOR_FIRST_OCCURRENCE,t,extreme_price,bar_id,reason) || t!=1120 || extreme_price!=90.0 || bar_id!="SPX-L-FIRST") return false;
   if(!DAYE_ResolveReferenceAnchor(use,periods,DAYE_EXTREME_ANCHOR_LAST_OCCURRENCE,t,extreme_price,bar_id,reason) || t!=1180 || extreme_price!=90.0 || bar_id!="SPX-L-LAST") return false;

   string line1=DAYE_BuildRenderLineName("USE-1");
   string line2=DAYE_BuildRenderLineName("USE-1");
   string line3=DAYE_BuildRenderLineName("USE-2");
   if(line1!=line2 || line1==line3 || StringFind(line1,DAYE_RENDER_OBJECT_PREFIX)!=0) return false;
   if(DAYE_BuildRenderProjectionId("USE-1",100)==DAYE_BuildRenderProjectionId("USE-1",101)) return false;
   return true;
}

#endif
