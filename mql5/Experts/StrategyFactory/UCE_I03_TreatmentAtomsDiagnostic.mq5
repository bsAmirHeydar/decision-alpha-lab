#property strict
#property description "UCEE-I03 treatment atom catalog and side-aware geometry diagnostic"
#include <AlphaLab/StrategyFactory/TreatmentAtoms/UCEI03_All.mqh>
int OnInit(){CUCEI03Catalog catalog;string error;if(!catalog.Build(error)){Print("UCE-I03 catalog build failed: ",error);return INIT_FAILED;}UCEI03_ConformanceTelemetry telemetry;if(!UCEI03_RunCatalogConformance(catalog,telemetry,error)){Print("UCE-I03 conformance failed: ",error);return INIT_FAILED;}Print("UCE-I03 ready atoms=",catalog.Count()," entry=",catalog.entry.Count()," stop=",catalog.stop.Count()," target=",catalog.target.Count()," trailing=",catalog.trailing.Count()," management=",catalog.management.Count()," sizing=",catalog.sizing.Count());return INIT_SUCCEEDED;}
void OnTick(){}
