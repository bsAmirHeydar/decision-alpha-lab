#property strict
#include <AlphaLab/EXP0019/FaerieProtocol/I05/FP_I05_All.mqh>
int OnInit(){
 if(FP_I05_Registry::ContractCount()!=12) return INIT_FAILED;
 FP_I05_ReferenceLevel r; r.reference_id="R"; r.pair_id="P"; r.canonical_symbol="ES"; r.price=1.0; r.extreme_utc_ms=60000; r.semantic_hash="HASH"; r.state=FP_I05_REF_FRESH; r.created_utc_ms=0; r.last_transition_utc_ms=0;
 if(!FP_I05_ReferenceEngine::ApplyHunterTouch(r,120000) || r.state!=FP_I05_REF_HUNTER_SEEN) return INIT_FAILED;
 if(!FP_I05_ReferenceEngine::ApplyProtectedTouch(r,180000) || r.state!=FP_I05_REF_CONSUMED_BY_PROTECTED) return INIT_FAILED;
 Print("FP-I05 SELF TEST PASS"); return INIT_SUCCEEDED;
}
void OnTick(){}
