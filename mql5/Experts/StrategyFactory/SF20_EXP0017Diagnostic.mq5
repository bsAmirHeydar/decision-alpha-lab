#property strict
#property version "20.000"
#include <AlphaLab/StrategyFactory/Integration/SF20_AllIntegration.mqh>
#include <AlphaLab/StrategyFactory/Integration/EXP0017/Fixture/SF20_EXP0017Fixture.mqh>
int OnInit(){SCGDDivergenceCandidate c;SF20_BuildReferenceLegacyCandidate(true,c);SF20_EXP0017Config cfg=SF20_DefaultEXP0017Config();SF01_AnatomyEvent event;SF20_EXP0017MappingRecord mapping;string error;if(!SF20_MapEXP0017Candidate(c,cfg,1783795000000,"exp0017_cycle_group_divergence","1.0.0",event,mapping,error)){Print(error);return INIT_FAILED;}Print("SF20 diagnostic event=",event.event_id," cluster=",event.market_event_cluster_id," source=",event.source_hash," live=false");return INIT_SUCCEEDED;}
