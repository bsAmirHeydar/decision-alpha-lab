#property strict
#property description "UCEE-I07 trainer SDK capability and contract diagnostic. No training or order authority."
#include <AlphaLab/StrategyFactory/TrainerSDK/UCEI07_All.mqh>
int OnInit(){CUCEI07TrainerRegistry registry;CUCEI07ReferenceCatalog catalog;string reason;if(!catalog.RegisterAll(registry,reason)){Print("UCE-I07 registry failed: ",reason);return INIT_FAILED;}Print("UCE-I07 registry size=",registry.Size()," snapshot=",registry.SnapshotHash());return INIT_SUCCEEDED;}
void OnTick(){}
