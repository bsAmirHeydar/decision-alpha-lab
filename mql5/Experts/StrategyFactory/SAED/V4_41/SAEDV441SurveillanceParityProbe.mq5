#property strict
#property version "1.00"
#property description "SAEDV441 static surveillance/retirement parity probe; no order or network authority."
#include <StrategyFactory/SAED/V4_41/SAEDV441Authority.mqh>
#include <StrategyFactory/SAED/V4_41/SAEDV441Observation.mqh>
#include <StrategyFactory/SAED/V4_41/SAEDV441RetirementRecord.mqh>
int OnInit()
{
   SAEDV441AuthorityRecord a; a.record_id="AUTH"; a.content_hash="REFERENCE"; a.research_only=true; a.live_side_effect_allowed=false;
   return SAEDV441ValidateAuthority(a) ? INIT_SUCCEEDED : INIT_FAILED;
}
void OnTick() { }
