#property strict
#property version "1.00"
#include <AlphaLab/StrategyFactory/ContextPackage/UCE02_All.mqh>
int OnInit()
{
   CUCE02EXP0017ReferencePackage package;UCE02_EXP0017ContextInput input;input.canonical_event_id="sf20_evt_001";input.parent_event_id="sf20_parent_001";input.event_time_ms=1711000000000;input.known_time_ms=1711000001000;input.confirmation_time_ms=1711000001000;input.observation_cut_ms=1711000001000;input.decision_time_ms=1711000001001;input.hunter_symbol="US100";input.clean_symbol="US500";input.group_minutes=60;input.direction="short";input.hunter_reference_price=18000.0;input.clean_reference_price=5200.0;input.hunter_current_extreme=18025.0;input.clean_current_extreme=5201.0;input.trading_day="2024-03-21";input.current_cycle_start_ms=1710997200000;
   UCE02_ContextObservation observation;string error="";if(!package.Observe(input,observation,error)){Print("FAIL: ",error);return INIT_FAILED;}PrintFormat("PASS: EXP0017 context observation id=%s hash=%s",observation.observation_id,observation.observation_hash);return INIT_SUCCEEDED;
}
void OnTick(){}
