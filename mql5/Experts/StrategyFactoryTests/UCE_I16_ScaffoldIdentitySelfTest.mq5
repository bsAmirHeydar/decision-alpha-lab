#property strict
#include <AlphaLab/StrategyFactory/ContextOnboarding/UCEI16_All.mqh>
int OnInit(){ UCEI16_Manifest m; m.manifest_id="fixture";m.context_id="fixture";m.context_spec_hash=StringInit(64,'a');m.tournament_template_hash=StringInit(64,'b');m.core_snapshot_hash=StringInit(64,'c');m.artifact_count=15; return UCEI16_ValidateManifest(m)?INIT_SUCCEEDED:INIT_FAILED; }
void OnTick(){}
