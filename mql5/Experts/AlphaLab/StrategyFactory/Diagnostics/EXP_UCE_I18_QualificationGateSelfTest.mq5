#property strict
#include <AlphaLab/StrategyFactory/Qualification/QualificationCatalog.mqh>
#include <AlphaLab/StrategyFactory/Qualification/QualificationGate.mqh>
#include <AlphaLab/StrategyFactory/Qualification/QualificationCompileEvidence.mqh>
int OnInit(){ ALCompileEvidence e; e.target="diagnostic"; e.source_hash=StringRepeat("a",64); e.log_hash=StringRepeat("b",64); e.output_hash=StringRepeat("c",64); e.exit_code=0; e.errors=0; e.warnings=0; if(!ALCompileEvidencePasses(e,0)) return INIT_FAILED; Print("UCE-I18 qualification gate self-test passed; order authority=",AL_QUALIFICATION_ORDER_AUTHORITY); return INIT_SUCCEEDED; }
void OnTick(){}
